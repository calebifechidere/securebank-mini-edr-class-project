# SecureBank Mini EDR — System Architecture

## Data flow

```text
Dedicated, fictional training_files/ (.txt only)
                  |
                  v
   Python polling collector (0.5 s)
   Baseline: mtime_ns, size, SHA-256
                  |
                  v
          Structured event log
          runtime/events.jsonl
                  |
                  v
    Rolling-window detection rule
      >= 3 files: MEDIUM, >= 5: HIGH
                  |
       +----------+----------+
       |                     |
    No match              Rule match
       |                     |
    Keep event             MEDIUM / HIGH alert
                             |
                     runtime/alerts.json
                             |
                     Analyst investigation
                             |
                   Acknowledge incident
                             |
                    Simulate containment
                    (status only; no real
                      endpoint action)
                             |
                        Audit log +
                      incident summary
```

## Components

| Module | Responsibility |
|---|---|
| `main.py` | Start the application. |
| `securebank_edr/core.py` | Training-file scanning, SHA-256 state comparison, telemetry, detection, response, and persistence. |
| `securebank_edr/cli.py` | Menu, safe activity simulator, and display of alert evidence. |
| `tests/test_edr.py` | Regression tests for normal/suspicious activity, persistence, scope and safe response. |
| `training_files/` | Dedicated directory containing fictional `.txt` files. |
| `runtime/` | Logs, JSON incident store, and generated human-readable reports. |

## Event fields

`event_id`, `timestamp_utc`, `event_type`, `file`, `size_bytes`, `sha256`

## Incident fields

`incident_id`, `timestamp_utc`, `title`, `severity`, `status`, `rule`, `rule_reason`, `affected_files`, `supporting_event_ids`, `actions`, `escalated_from` (only present when a MEDIUM incident was upgraded to HIGH)

## Threat model and trust boundaries

The app runs locally on the learner's workstation and does not require root privileges. Only `.txt` files under the designated training directory are inspected, and symlinked targets are excluded. The prototype makes no claim of tamper resistance. It does not read system-wide endpoint telemetry. No data is transmitted over the network.

## Detection tradeoffs

The rule is transparent and suitable for beginner explanation. It detects visible bursts of different file changes, but cannot determine malicious intent. A legitimate script updating three or more sample files may be a false positive. A suspicious actor changing only a single file may not trigger the rule. The window, cooldown, HIGH threshold (`threshold`) and MEDIUM threshold (`medium_threshold`) are constructor parameters of `MiniEDR` in `core.py`, so tests can change them.
