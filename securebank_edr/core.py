"""Core monitoring, alerting, safe-response simulation and reporting.
_-----------55
Security boundary: the monitor observes only .txt files inside the explicitly
selected training folder. It never collects file contents in logs and never
kills processes, isolates an endpoint or disables network connectivity.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional
import hashlib
import json
import os
import threading
import time
import uuid


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    tmp.replace(path)


class MiniEDR:
    """Polling monitor with a simple distinct-file burst detector.

    Detection: >= threshold *different* TXT files created or modified within
    window_seconds. A short cooldown suppresses duplicate alerts from one
    burst. A new instance starts with a fresh baseline, avoiding startup noise.
    """

    def __init__(
        self,
        workspace: Path,
        threshold: int = 5,
        window_seconds: float = 10.0,
        cooldown_seconds: float = 12.0,
        poll_interval: float = 0.5,
        monotonic: Callable[[], float] = time.monotonic,
        medium_threshold: int = 3,
    ) -> None:
        if threshold < 2 or window_seconds <= 0 or cooldown_seconds < 0 or poll_interval <= 0:
            raise ValueError("Invalid detector settings")
        if not 2 <= medium_threshold <= threshold:
            raise ValueError("medium_threshold must be between 2 and threshold")
        self.workspace = Path(workspace).resolve()
        self.training = self.workspace / "training_files"
        self.runtime = self.workspace / "runtime"
        self.events_file = self.runtime / "events.jsonl"
        self.alerts_file = self.runtime / "alerts.json"
        self.audit_file = self.runtime / "audit.jsonl"
        self.reports_dir = self.runtime / "reports"
        self.threshold = threshold
        self.medium_threshold = medium_threshold
        self.window_seconds = window_seconds
        self.cooldown_seconds = cooldown_seconds
        self.poll_interval = poll_interval
        self._clock = monotonic
        self._lock = threading.RLock()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._snapshot: dict[str, tuple[int, int, str]] = {}
        self._recent: deque[tuple[float, dict]] = deque()
        self._last_alert_time = float("-inf")
        self._last_alert: Optional[dict] = None
        self.events: list[dict] = []
        self.alerts: list[dict] = []
        self._initialized = False
        self._ensure_directories()
        self._read_history()

    def _ensure_directories(self) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)
        if self.training.is_symlink():
            raise ValueError("Training directory must not be a symlink")
        self.training.mkdir(parents=True, exist_ok=True)
        if self.runtime.is_symlink() or self.reports_dir.is_symlink():
            raise ValueError("Runtime storage must not use symlinked directories")
        self.runtime.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        for output in (self.events_file, self.alerts_file, self.audit_file):
            if output.is_symlink():
                raise ValueError("Runtime storage must not use symlinked files")
        # These files are fictional sample records, never personal/real data.
        samples = {
            "account-summary.txt": "Fictional SecureBank training account summary.\n",
            "customer-sample.txt": "Fictional customer test record: CUSTOMER-DEMO-01.\n",
            "ledger-sample.txt": "Fictional training ledger. No real transactions.\n",
            "branch-notes.txt": "SecureBank training branch notes.\n",
            "staff-training.txt": "Fictional training-only staff record.\n",
            "operations-sample.txt": "Fictional SecureBank operations sample.\n",
        }
        for name, content in samples.items():
            path = self.training / name
            if path.is_symlink():
                raise ValueError("Training sample must not be a symlink: " + name)
            if not path.exists():
                path.write_text(content, encoding="utf-8")

    def _read_history(self) -> None:
        if self.events_file.exists():
            for line in self.events_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        self.events.append(json.loads(line))
                    except json.JSONDecodeError:
                        raise ValueError(f"Invalid JSON line in {self.events_file}")
        if self.alerts_file.exists():
            data = json.loads(self.alerts_file.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                raise ValueError("Alerts store is not a JSON list")
            self.alerts = data

    def _iter_safe_files(self):
        root = self.training.resolve()
        for file in sorted(self.training.rglob("*.txt")):
            # Symlinked files and directories are excluded; only training files.
            if file.is_symlink() or any(parent.is_symlink() for parent in file.parents if parent != root):
                continue
            try: 
                resolved = file.resolve(strict=True)
                if os.path.commonpath([str(root), str(resolved)]) != str(root):
                    continue
                if resolved.is_file():
                    yield file
            except (OSError, ValueError):
                continue

    @staticmethod
    def _signature(file: Path) -> tuple[int, int, str]:
        st = file.stat()
        hasher = hashlib.sha256()
        with file.open("rb") as stream:
            for part in iter(lambda: stream.read(65536), b""):
                hasher.update(part)
        return (st.st_mtime_ns, st.st_size, hasher.hexdigest())

    def _current_snapshot(self) -> dict[str, tuple[int, int, str]]:
        found = {}
        for file in self._iter_safe_files():
            try:
                found[file.relative_to(self.training).as_posix()] = self._signature(file)
            except (FileNotFoundError, PermissionError, OSError):
                # Files may change during a scan; retry on the next poll.
                continue
        return found

    def initialize_baseline(self) -> None:
        with self._lock:
            self._snapshot = self._current_snapshot()
            self._initialized = True

    def _append_line(self, file: Path, record: dict) -> None:
        with file.open("a", encoding="utf-8") as output:
            output.write(json.dumps(record, sort_keys=True) + "\n")

    def _register_event(self, action: str, relpath: str, signature: Optional[tuple]) -> None:
        ev = {
            "event_id": make_id("EVT"),
            "timestamp_utc": utc_now(),
            "event_type": action,
            "file": relpath,
            "size_bytes": signature[1] if signature else None,
            "sha256": signature[2] if signature else None,
        }
        self.events.append(ev)
        self._append_line(self.events_file, ev)
        if action in ("CREATED", "MODIFIED"):
            self._check_detection(ev)
    def _reason(self, count: int, severity: str) -> str:
        return (f"{count} distinct training .txt files changed within "
                f"{self.window_seconds:g} seconds ({severity}; "
                f"MEDIUM threshold: {self.medium_threshold}, "
                f"HIGH threshold: {self.threshold}).")


    def _check_detection(self, ev: dict) -> None:
        now = self._clock()
        self._recent.append((now, ev))
        while self._recent and now - self._recent[0][0] > self.window_seconds:
            self._recent.popleft()
        distinct_files = {e["file"] for _, e in self._recent}
        count = len(distinct_files)
        if count < self.medium_threshold:
            return
        severity = "HIGH" if count >= self.threshold else "MEDIUM"
        evidence = list(self._recent)

        if now - self._last_alert_time < self.cooldown_seconds:
            # Same burst: upgrade the open MEDIUM alert if it has grown to HIGH.
            last = self._last_alert
            if last is not None and last["severity"] == "MEDIUM" and severity == "HIGH":
                last["severity"] = "HIGH"
                last["escalated_from"] = "MEDIUM"
                last["rule_reason"] = self._reason(count, severity)
                last["affected_files"] = sorted(distinct_files)
                last["supporting_event_ids"] = [e["event_id"] for _, e in evidence]
                write_json_atomic(self.alerts_file, self.alerts)
                self._recent.clear()
            return

        alert = {
            "incident_id": make_id("INC"),
            "timestamp_utc": utc_now(),
            "title": "Unusual burst of training-file changes",
            "severity": severity,
            "status": "NEW",
            "rule": "DISTINCT_FILE_CHANGE_BURST",
            "rule_reason": self._reason(count, severity),
            "affected_files": sorted(distinct_files),
            "supporting_event_ids": [e["event_id"] for _, e in evidence],
            "actions": [],
        }
        self.alerts.append(alert)
        write_json_atomic(self.alerts_file, self.alerts)
        self._last_alert = alert
        self._last_alert_time = now
        if severity == "HIGH":
            self._recent.clear()   # MEDIUM keeps its events so the burst can escalate

    def scan_once(self) -> list[dict]:
        """Perform a single polling scan; return newly generated events."""
        with self._lock:
            now = self._current_snapshot()
            if not self._initialized:
                self._snapshot = now
                self._initialized = True
                return []
            old = self._snapshot
            before = len(self.events)
            for path, sig in now.items():
                if path not in old:
                    self._register_event("CREATED", path, sig)
                elif sig != old[path]:
                    self._register_event("MODIFIED", path, sig)
            for path in sorted(set(old) - set(now)):
                self._register_event("DELETED", path, None)
            self._snapshot = now
            return self.events[before:]

    def start(self) -> None:
        with self._lock:
            if self._thread and self._thread.is_alive():
                return
            self.initialize_baseline()
            self._stop.clear()
            self._thread = threading.Thread(target=self._monitor_loop, name="securebank-folder-monitor", daemon=True)
            self._thread.start()

    def _monitor_loop(self) -> None:
        while not self._stop.wait(self.poll_interval):
            try:
                self.scan_once()
            except Exception as exc:
                # Never silently hide a monitoring failure.
                with self._lock:
                    self._append_line(self.audit_file, {"timestamp_utc": utc_now(), "event": "MONITOR_ERROR", "details": str(exc)})

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self.poll_interval + 2)

    def _demo_path(self, name: str) -> Path:
        """Resolve only one known sample filename and reject symlink redirection."""
        allowed = {
            "account-summary.txt", "customer-sample.txt", "ledger-sample.txt",
            "branch-notes.txt", "staff-training.txt", "operations-sample.txt",
        }
        if name not in allowed:
            raise ValueError("Demo file not allowed")
        path = self.training / name
        if self.training.is_symlink() or path.is_symlink():
            raise ValueError("Refusing to write to symlinked demo location")
        if path.parent.resolve() != self.training.resolve():
            raise ValueError("Demo file is outside training directory")
        return path

    def simulate_normal(self) -> None:
        """One harmless change to a fictional sample file."""
        path = self._demo_path("account-summary.txt")
        with self._lock:
            with path.open("a", encoding="utf-8") as out:
                out.write(f"Demo: normal single-file update at {utc_now()}\n")
            self.scan_once()

    def simulate_suspicious(self) -> None:
        """Five harmless updates for a reproducible high-priority alert."""
        with self._lock:
            names = ["account-summary.txt", "customer-sample.txt", "ledger-sample.txt", "branch-notes.txt", "staff-training.txt"]
            for name in names:
                with self._demo_path(name).open("a", encoding="utf-8") as out:
                    out.write(f"Demo: synthetic rapid-change event at {utc_now()} ({uuid.uuid4().hex[:6]})\n")
            self.scan_once()

    def get_incident(self, incident_id: str) -> Optional[dict]:
        with self._lock:
            return next((a for a in self.alerts if a["incident_id"] == incident_id), None)


    def get_incident_evidence(self, incident_id: str) -> list[dict]:
    """Retrieve all supporting events for an incident in chronological order."""
    with self._lock:
        incident = self.get_incident(incident_id)

        if incident is None:
            raise KeyError("Incident not found")

        supporting_ids = incident["supporting_event_ids"]

        event_lookup = {
            event["event_id"]: event
            for event in self.events
        }

        missing_ids = [
            event_id
            for event_id in supporting_ids
            if event_id not in event_lookup
        ]

        if missing_ids:
            raise ValueError(
                f"Supporting evidence records missing: {missing_ids}"
            )

        evidence = [
            event_lookup[event_id].copy()
            for event_id in supporting_ids
        ]

        evidence.sort(key=lambda event: event["timestamp_utc"])

        return evidence
    

    def respond(self, incident_id: str, response: str, analyst: str = "training-analyst") -> dict:
        """Change recorded incident state; never perform actual containment."""
        if response not in ("ACKNOWLEDGED", "CONTAINMENT_SIMULATED"):
            raise ValueError("Unsupported response")
        with self._lock:
            incident = self.get_incident(incident_id)
            if incident is None:
                raise KeyError("Incident not found")
            if response == "CONTAINMENT_SIMULATED" and incident["status"] == "NEW":
                raise ValueError("Acknowledge the incident before simulating containment")
            action = {
                "timestamp_utc": utc_now(),
                "analyst": analyst,
                "action": response,
                "note": "Training-state change only; no process killed, network disabled, or files quarantined.",
            }
            incident["status"] = response
            incident["actions"].append(action)
            self._append_line(self.audit_file, {"event": "ANALYST_ACTION", "incident_id": incident_id, **action})
            write_json_atomic(self.alerts_file, self.alerts)
            return incident

    def summary(self) -> dict:
        with self._lock:
            return {
                "events_total": len(self.events),
                "created": sum(x["event_type"] == "CREATED" for x in self.events),
                "modified": sum(x["event_type"] == "MODIFIED" for x in self.events),
                "deleted": sum(x["event_type"] == "DELETED" for x in self.events),
                "alerts_total": len(self.alerts),
                "alerts_new": sum(x["status"] == "NEW" for x in self.alerts),
                "alerts_acknowledged": sum(x["status"] == "ACKNOWLEDGED" for x in self.alerts),
                "alerts_containment_simulated": sum(x["status"] == "CONTAINMENT_SIMULATED" for x in self.alerts),
            }

    def export_report(self) -> Path:
        with self._lock:
            report = self.reports_dir / f"incident-summary-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.txt"
            stats = self.summary()
            lines = [
                "SECUREBANK MINI EDR - INCIDENT SUMMARY",
                f"Generated UTC: {utc_now()}",
                "Training lab only. This prototype monitors .txt files in the training_files folder.",
                "Safe response is simulated. No real endpoint containment is performed.",
                "",
                "COUNTS",
            ]
            lines += [f"{key}: {value}" for key, value in stats.items()]
            lines += ["", "RECENT EVENT TIMELINE"]
            for event in self.events[-30:]:
                lines.append(f"{event['timestamp_utc']} | {event['event_type']:<8} | {event['file']}")
            lines += ["", "ALERTS / RESPONSE HISTORY"]
            for incident in self.alerts:
                lines += [
                    f"{incident['incident_id']} | {incident['severity']} | {incident['status']}",
                    f"Reason: {incident['rule_reason']}",
                    f"Files: {', '.join(incident['affected_files'])}",
                    f"Event references: {', '.join(incident['supporting_event_ids'])}",
                ]
                for action in incident["actions"]:
                    lines.append(f"  {action['timestamp_utc']} | {action['analyst']}: {action['action']}")
            lines += ["", "LIMITATIONS", "Folder-only, polling-based monitoring; burst threshold can cause false positives; no real host-wide EDR or containment."]
            report.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return report
