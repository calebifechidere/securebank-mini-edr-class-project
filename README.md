# SecureBank Mini EDR

**A safe, offline Endpoint Detection and Response (EDR) teaching prototype built in Python 3.**

> **Educational scope:** This is not commercial antivirus/EDR software. It monitors only fictional `.txt` files in its own `training_files/` directory. It does not monitor unrelated folders, collect credentials, store file contents in logs, kill processes, disable networking, or perform real containment.

## 1. What it demonstrates

| EDR principle | Prototype feature |
|---|---|
| Visibility | Polls a dedicated fictional training folder for created, modified, and deleted `.txt` files. |
| Detection | 1-2 distinct files: no alert; 3-4: MEDIUM; 5 or more: HIGH within a rolling 10-second window. |
| Investigation | Retrieves supporting event records chronologically, including event IDs, timestamps, filenames, sizes, and SHA-256 hashes. |
| Response | Allows an analyst to acknowledge an incident and record containment as simulated. |
| Reporting | Saves structured JSON events/alerts, an audit trail, and a human-readable incident summary. |

The project uses Python's standard library. No package installation or internet connection is required.

## 2. Run the project

From the project root:

```bash
python3 --version
python3 -m unittest discover -s tests -v
python3 main.py
```

The terminal menu lets the user simulate normal and suspicious file activity, view the event timeline and alerts, investigate incidents, acknowledge an incident, simulate containment, and export a report.



## 2.1 Optional Desktop GUI

The project also includes an optional PySide6 desktop graphical interface.

### Install the GUI dependency

On Kali Linux:

```bash
sudo apt update
sudo apt install python3-pyside6.qtcore python3-pyside6.qtgui python3-pyside6.qtwidgets
```

### Launch the GUI

From the project root:

```bash
python3 -m securebank_edr.gui.main_window
```

The GUI provides a desktop dashboard with monitoring controls, event activity, incident overview, and operational metrics.

The original command-line interface remains available:

```bash
python3 main.py
```


## 3. Detection logic

- The initial scan creates a baseline of the fictional training files.
- The collector compares modification time, file size, and SHA-256 fingerprints.
- The detector counts distinct created or modified filenames in a rolling 10-second window.
- 1-2 distinct files: no alert.
- 3-4 distinct files: MEDIUM incident.
- 5 or more distinct files: HIGH incident.
- A MEDIUM incident can escalate to HIGH as the same incident.
- A 12-second cooldown suppresses duplicate alerts from rapid consecutive bursts.
- Deletions are logged but do not count toward the burst threshold.

## 4. Response workflow

```text
NEW -> ACKNOWLEDGED -> CONTAINMENT_SIMULATED
```

Containment changes the recorded incident status and writes an audit entry. It does not isolate a device, stop processes, disable network access, or quarantine files.

## 5. Project structure

```text
SecureBank-Mini-EDR/
├── main.py
├── securebank_edr/
├── training_files/
├── tests/
├── docs/
├── reports/
├── evidence/
├── runtime/                 # generated locally; not committed
└── README.md
```

## 6. Validation

The integrated project test output supplied for this report shows **24 automated tests passed**. The tests cover normal activity, suspicious bursts, MEDIUM/HIGH thresholds, escalation, cooldown, supporting evidence retrieval, response workflow, persistence, monitoring boundaries, and report generation.

The captured live demonstration includes:
- Application startup and monitoring scope.
- A normal one-file modification recorded without a new alert.
- A five-file burst that generated an alert and supporting evidence.
- Incident investigation, acknowledgement, and simulated containment.
- Incident report export and analyst audit records.
- A separate severity demonstration showing MEDIUM-to-HIGH escalation under the same incident ID and duplicate suppression during cooldown.

See `docs/REPORT_DRAFT.md` for the written report, `docs/PRESENTATION_GUIDE.md` for the demonstration script, and `docs/EVIDENCE_INDEX.md` for screenshot captions and evidence notes.

## 7. Class team and submission details

- **Programme:** Tech4Youth Advanced ICT Skills Training Programme - Cybersecurity Operations (Week 6)
- **Learning centre:** ESUT ICT and Innovation Hub
- **Tutor:** Mr. Noso
- **Lead student / repository owner:** Godwin Caleb Ifechidere

Eleven participant identities were supplied for this update. The assignment brief refers to 20 learners, so the remaining nine names and individual contribution details must be confirmed by the class before final submission. See `docs/TEAM_CONTRIBUTIONS_TEMPLATE.md`.

## 8. Limitations

- Folder-only monitoring: it does not monitor the whole computer, processes, network connections, or operating-system telemetry.
- Polling-based collection may miss very short-lived changes between scans.
- Threshold rules can produce false positives during legitimate bulk updates and false negatives for slower or smaller activity.
- Local logs are not tamper-resistant enterprise logging.
- Containment is simulated only.

## 9. Responsible use

Use only the fictional sample files supplied in this project. Do not point the monitor at private files or business systems. Do not describe this educational prototype as a production EDR solution.

## References

- Tech4Youth. (2026). *Week 6 Practical Assignment: Build a Simple Endpoint Detection and Response System* [Tutor-provided assignment].
- Python Software Foundation. *Python standard library documentation*. https://docs.python.org/3/library/
- Python Software Foundation. *pathlib - Object-oriented filesystem paths*. https://docs.python.org/3/library/pathlib.html
- Python Software Foundation. *hashlib - Secure hashes and message digests*. https://docs.python.org/3/library/hashlib.html
