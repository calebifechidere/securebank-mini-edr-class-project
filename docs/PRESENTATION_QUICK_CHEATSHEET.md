# SecureBank Mini EDR — Presenter Quick Cheat Sheet

## One-sentence explanation
A Python program that watches a folder of fictional text files, records changes, alerts when five different files change within ten seconds, and lets an analyst record acknowledgement and simulated containment.

## The five stages
1. Visibility — monitor `training_files/`.
2. Detection — apply the five-distinct-files-in-ten-seconds rule.
3. Alert — create a HIGH incident with evidence references.
4. Investigation and response — review the evidence, acknowledge and simulate containment.
5. Reporting — export the event timeline and incident summary.

## Live menu sequence
| Menu choice | Action | What to explain |
|---:|---|---|
| 1 | Simulate normal activity | One file changes; an event is logged, but no HIGH alert is expected. |
| 3 | View event timeline | Point to timestamp, event type, filename and event ID. |
| 4 | View alerts | Confirm no alert after one file change, then show the HIGH alert after the burst. |
| 2 | Simulate suspicious activity | Five different sample files are updated quickly. |
| 5 | Investigate incident | Enter the incident ID; show reason, affected files and supporting event IDs. |
| 6 | Acknowledge incident | Status becomes `ACKNOWLEDGED`. |
| 7 | Simulate containment | Status becomes `CONTAINMENT_SIMULATED`; no real endpoint action occurs. |
| 8 | Export report | Show summary and the generated report path. |
| 9 | Exit | Close the application cleanly. |

## Remember these numbers
- Polling interval: 0.5 seconds.
- Detection window: 10 seconds.
- Threshold: 5 distinct created or modified `.txt` files.
- Cooldown: 12 seconds.

## Where records are saved
- `runtime/events.jsonl` — observed file events.
- `runtime/alerts.json` — alerts and incident status.
- `runtime/audit.jsonl` — analyst actions.
- `runtime/reports/` — exported text reports.

## Key limitation to say clearly
This is a classroom prototype. It watches only the dedicated training folder, does not inspect processes or network traffic, and simulates containment by changing the incident status only.

## If the tutor asks why an alert may be wrong
A legitimate bulk update could modify five files within ten seconds and trigger a false positive. A suspicious activity that changes fewer than five files or happens slowly could be missed.
