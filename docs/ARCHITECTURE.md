# SecureBank Mini EDR — System Architecture

## Data flow

```text
Dedicated fictional training_files/ (.txt only)
                  |
                  v
       Python polling collector
       Baseline: mtime, size, SHA-256
                  |
                  v
          Structured event log
          runtime/events.jsonl
                  |
                  v
       Rolling 10-second detector
                  |
          +-------+-------+
          |               |
        1–2 files       3+ files
        No alert           |
                    +------+------+
                    |             |
                  3–4           5+
                 MEDIUM        HIGH
                    |             |
                    +------+------+
                           |
                    runtime/alerts.json
                           |
                 Supporting evidence lookup
                           |
                  Analyst investigation
                           |
                   Acknowledge incident
                           |
                   Simulate containment
                    (status only)
                           |
                       Audit log
                           |
                    Incident report
```

## Components

| Module | Responsibility |
|---|---|
| `main.py` | Start the application. |
| `securebank_edr/core.py` | Training-file scanning, SHA-256 state comparison, telemetry, detection, response, and persistence. |
| `securebank_edr/cli.py` | Menu, safe activity simulator, and display of alert evidence. |
| `tests/test_edr.py` | Core regression tests, evidence retrieval, persistence, scope and safe response. |
| `tests/test_severity.py` | MEDIUM/HIGH thresholds, escalation and cooldown tests. |
| `training_files/` | Dedicated directory containing fictional `.txt` files. |
| `runtime/` | Logs, JSON incident store, and generated human-readable reports. |

## Event fields

`event_id`, `timestamp_utc`, `event_type`, `file`, `size_bytes`, `sha256`

## Incident fields

`incident_id`, `timestamp_utc`, `title`, `severity`, `status`, `rule`, `rule_reason`, `affected_files`, `supporting_event_ids`, `actions`

## Incident evidence retrieval

The `get_incident_evidence(incident_id)` method retrieves the original event records referenced by an incident's supporting event IDs. It verifies that the incident and evidence records exist, then returns the events in chronological order. The CLI displays event IDs, timestamps, event types, filenames, file sizes and SHA-256 hashes.

## Threat model and trust boundaries

The app runs locally on the learner's workstation and does not require root privileges. Only `.txt` files under the designated training directory are inspected, and symlinked targets are excluded. The prototype makes no claim of tamper resistance. It does not read system-wide endpoint telemetry. No data is transmitted over the network.

## Detection tradeoffs

The detector uses two thresholds within a rolling 10-second window: 3–4 distinct changed files produce MEDIUM severity, while 5 or more produce HIGH severity. An existing MEDIUM incident can escalate to HIGH without creating a separate incident. A 12-second cooldown suppresses duplicate alerts from rapid consecutive bursts.

The rule is transparent and suitable for beginner explanation, but cannot determine malicious intent. Legitimate bulk updates may trigger false positives, while smaller or slower suspicious changes may be missed.
