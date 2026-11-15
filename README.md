# SecureBank Mini EDR

**A safe, offline Endpoint Detection and Response (EDR) teaching prototype built in Python 3.**

> **Educational scope:** This is not commercial antivirus/EDR software. It monitors **only fictional `.txt` files** in its own `training_files/` directory. It never intentionally collects credentials, monitors unrelated folders, stores file contents in logs, kills processes, disables networking, or performs real containment.

## 1. What it does

| EDR principle | Prototype feature |
|---|---|
| **Visibility** | Polls a dedicated fictional training folder for created, modified, and deleted `.txt` files. |
| **Detection** | Raises a HIGH alert when **5 different training files are created/modified within 10 seconds**. |
| **Investigation** | Shows the affected filenames, event IDs, rule, reason, severity, and an event timeline. |
| **Response** | Analyst can acknowledge an incident and mark containment as **simulated**. |
| **Reporting** | Saves structured JSON events/alerts and an incident-summary text report. |

Uses **only Python's standard library**. No package installation or internet connection is needed.

## 2. Install and run on Kali Linux / Parrot OS / Ubuntu

1. Download and extract the project ZIP.
2. Open a terminal in the extracted `SecureBank-Mini-EDR` folder.
3. Check Python (recommended Python 3.9+):

```bash
python3 --version
```

4. Start the interactive application:

```bash
python3 main.py
```

5. The terminal menu lets you generate normal/suspicious sample activity, view events, investigate alerts, acknowledge incidents, simulate containment, and export reports.

No `pip install`, administrator privileges, or network access is required.

### Quick demonstration without menu

```bash
python3 main.py --quick-demo
```

This makes one normal file change and then a burst across five fictional files; it prints events and alerts, and writes a report. To use a fresh isolated workspace for an independent demo:

```bash
python3 main.py --workspace ~/SecureBank-Demo-Run --quick-demo
```

### Windows PowerShell (optional)

```powershell
py -3 main.py
```

## 3. Live demonstration sequence (for class)

1. Start the app with `python3 main.py` (the original sample files become the baseline; no alert is raised).
2. Choose **1** for one normal file update; choose **3** to show the recorded event, then **4** to confirm no new alert.
3. Choose **2** to make five rapid changes; choose **4** to show the HIGH-severity incident.
4. Choose **5** and paste the incident ID to investigate the supporting events and affected files.
5. Choose **6** to acknowledge the incident; choose **7** to simulate containment. The app changes only the recorded incident status.
6. Choose **8** to export the event timeline and final incident summary. Find the report under `runtime/reports/`.
7. Capture screenshots of the actual demo on your group's computer for the final PDF report.

> If an earlier burst occurred less than 12 seconds ago, the detector's cooldown suppresses a duplicate alert. This is intentional. Wait before demonstrating a second burst.

## 4. Project structure

```text
SecureBank-Mini-EDR/
├── main.py                     # Entry point
├── securebank_edr/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py                 # Polling, telemetry, detection, response, storage
│   └── cli.py                  # CLI menu and demo generator
├── training_files/            # Fictional .txt samples ONLY
├── tests/
│   └── test_edr.py             # Automated regression tests
├── docs/
│   ├── ARCHITECTURE.md
│   ├── REPORT_DRAFT.md
│   ├── PRESENTATION_GUIDE.md
│   ├── PRESENTATION_QUICK_CHEATSHEET.md
│   ├── TEAM_CONTRIBUTIONS_TEMPLATE.md
│   └── SCREENSHOT_CHECKLIST.md
├── reports/
│   └── SecureBank-Mini-EDR-Class-Report.pdf  # Editable draft content in docs/REPORT_DRAFT.md
├── runtime/                   # Created on first run (not tracked by Git)
│   ├── events.jsonl
│   ├── alerts.json
│   ├── audit.jsonl
│   └── reports/
├── .gitignore
└── README.md
```

## 5. Detection logic

- A file's **mtime, size, and SHA-256** fingerprint are compared against the previous polling snapshot.
- Each new or modified `.txt` file generates an event with timestamp, type, relative path, size, and SHA-256. File contents are **never stored in the event log**.
- The detector keeps changes from the previous **10 seconds**, using a monotonic clock.
- If **5 distinct filenames** were changed in that window, it creates one HIGH-severity incident with the supporting event IDs.
- A **12-second cooldown** suppresses immediate duplicate alerts.
- Deletion is recorded as telemetry but is not an alert trigger in this beginner prototype.
- Initial sample files are included in the startup baseline, so app launch alone raises no alert.

**Detection-rule pseudocode:**

```text
for each observed file event:
    log event
    if event is CREATED or MODIFIED:
        add event to rolling 10-second window
        remove expired events
        if changed_distinct_files >= 5 and cooldown_elapsed:
            generate HIGH alert with evidence
```

## 6. Safe response model

An incident progresses through:

```text
NEW --> ACKNOWLEDGED --> CONTAINMENT_SIMULATED
```

Simulation changes the incident status and writes an audit record. It **never** quarantines real files, modifies system settings, stops processes, or interferes with an actual endpoint.

## 7. Test the implementation

From the extracted project root:

```bash
python3 -m unittest discover -s tests -v
```

Automated tests cover baseline behavior, normal changes, burst detection, supporting evidence, response workflow, persistence, out-of-scope folders, symlink exclusion, report export and deletion behavior.

See `docs/PRESENTATION_GUIDE.md` for a beginner-friendly explanation and step-by-step live demonstration script. Use `docs/PRESENTATION_QUICK_CHEATSHEET.md` during the presentation and `docs/SCREENSHOT_CHECKLIST.md` to capture evidence.

## 8. Limitations and false positives

- **Folder-only:** Does not monitor the whole computer, running processes, network connections or registry.
- **Polling:** Very fast changes between polls may be missed. It is not an OS audit or kernel telemetry sensor.
- **Threshold-based:** Legitimate batch edits can trigger a false positive; smaller suspicious changes may be missed.
- **Not tamper-resistant:** Training files, log files and Python code can be modified by someone with local filesystem access.
- **No real containment:** Analyst response is simulated by a status update.
- **No central console or threat intelligence:** This is a classroom proof of concept, not an enterprise endpoint product.

## 9. Responsible use

Use only fictional training data in this project folder. Don't point the monitor at private files or business systems. Do not claim this project offers complete endpoint security.

## 10. Assignment and group submission

This project package includes a report draft and a contribution template. Before submitting the class report:

- Add the class members, tutor, programme and learning centre.
- Run the application on your class's machine and capture **real** normal/suspicious scenario screenshots.
- Record results that you actually observed on the presentation machine.
- Complete the contribution log and present **one** integrated application as required.

## References

- Python standard library: https://docs.python.org/3/library/
- Python `pathlib`: https://docs.python.org/3/library/pathlib.html
- Python `hashlib`: https://docs.python.org/3/library/hashlib.html
- Assignment: Tech4Youth, Cybersecurity Operations, Week 6 practical assignment (supplied by tutor).
