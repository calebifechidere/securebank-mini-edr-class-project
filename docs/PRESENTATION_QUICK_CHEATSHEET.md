# SecureBank Mini EDR - Presenter Quick Cheat Sheet

## One-sentence explanation
A Python program that monitors fictional training files, records changes, raises MEDIUM alerts for 3-4 distinct files and HIGH alerts for 5 or more within ten seconds, and supports evidence-based investigation and simulated response.

## The five stages
1. Visibility - monitor `training_files/`.
2. Detection - count distinct file changes within ten seconds.
3. Alert - 1-2 files: none; 3-4: MEDIUM; 5+: HIGH.
4. Investigation and response - retrieve evidence, acknowledge, and simulate containment.
5. Reporting - export the event timeline and incident summary.

## Live menu sequence
| Menu | Action | What to explain |
|---:|---|---|
| 1 | Simulate normal activity | One file changes; an event is logged but no alert is expected. |
| 3 | View event timeline | Show timestamp, event type, filename, and event ID. |
| 4 | View alerts | Confirm no alert after one file change. |
| 2 | Simulate suspicious activity | Five different sample files are updated quickly. |
| 4 | View alerts | Show the HIGH alert and its reason. |
| 5 | Investigate incident | Enter the incident ID; show affected files and supporting event IDs. |
| 6 | Acknowledge incident | Status becomes `ACKNOWLEDGED`. |
| 7 | Simulate containment | Status becomes `CONTAINMENT_SIMULATED`; no real endpoint action occurs. |
| 8 | Export report | Show summary and generated report path. |
| 9 | Exit | Close the application. |

## Remember these numbers
- Polling interval: 0.5 seconds.
- Detection window: 10 seconds.
- MEDIUM threshold: 3 distinct files.
- HIGH threshold: 5 distinct files.
- Cooldown: 12 seconds.
- MEDIUM can escalate to HIGH as the same incident.
- Supplied integrated test evidence: 24 tests passed.

## Evidence run IDs
- Main investigation / acknowledgement / report: `INC-20261117061448-6CB317`.
- Separate audit/export run: `INC-20261117065154-405D15`.
- Separate escalation/cooldown demonstration: `INC-20261117070153-960CB9`.

## Where records are saved
- `runtime/events.jsonl` - observed file events.
- `runtime/alerts.json` - alerts and incident status.
- `runtime/audit.jsonl` - analyst actions.
- `runtime/reports/` - exported text reports.

## Key limitation
This is a classroom prototype. It watches only the dedicated training folder, does not inspect processes or network traffic, and simulates containment by changing incident status only.
