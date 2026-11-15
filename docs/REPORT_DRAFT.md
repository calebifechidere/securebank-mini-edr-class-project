# SECUREBANK MINI EDR - CLASS REPORT (DRAFT)

> **Status: Draft for group verification.** Replace placeholders, run the software on your own class machine, insert real annotated screenshots, and record the contributions of all participating classmates before final submission. The verification figures below are from an isolated developer test environment, not a claim of testing on the class's computer.

## 1. Cover page

**Project:** SecureBank Mini EDR - Endpoint Detection and Response Training Prototype
**Programme:** Tech4Youth Advanced ICT Skills Training Programme - Cybersecurity Operations (Week 6)
**Learning centre:** [Insert learning centre]
**Tutor:** [Insert tutor name]
**Presentation date:** Monday, 16 November 2026
**Contributors:** [Insert the actual names of all 20 learners and their roles]

## 2. Executive summary

SecureBank Mini EDR is a local, Python-based training prototype that demonstrates endpoint visibility, simple rule-based detection, incident investigation, and safe response recording. It watches only a dedicated folder containing fictional `.txt` files. A user can generate a normal single-file change, followed by a short burst affecting five different files. Each event is logged with its timestamp, action, filename, size, and SHA-256 digest. A threshold rule raises a HIGH alert when five different files change within ten seconds. The analyst can review the evidence, acknowledge the incident and mark containment as simulated. The system creates an event timeline and incident summary. It does not provide full endpoint protection or perform real containment.

## 3. Introduction and problem statement

SecureBank's fictional scenario calls for a way to notice unusual activity on workstations. A basic file-monitoring prototype allows beginners to see how telemetry becomes an event, how a rule decides to generate an alert, and how an analyst responds. A raw file modification is not necessarily malicious. The prototype therefore separates event collection from alert generation and displays evidence that supports further investigation. It uses a narrow, permission-safe training scope, rather than monitoring real private files or interfering with the host computer.

## 4. Project aims and objectives

**Aim:** Build one integrated class prototype demonstrating the visibility, detection, investigation and response workflow of EDR.

**Objectives:** (1) Monitor a dedicated fictional training folder. (2) Log newly created, modified or deleted `.txt` files. (3) Detect five distinct file changes in ten seconds. (4) Show incident severity, reason and supporting events. (5) Allow acknowledgement and simulated containment. (6) Export the event timeline and a readable incident summary. (7) Demonstrate both a normal and a suspicious activity scenario.

## 5. System architecture

`training_files/` -> polling collector -> `runtime/events.jsonl` -> rolling 10-second detection window -> `runtime/alerts.json` -> analyst investigation -> acknowledgement / simulated containment -> audit history and incident report.

The collector uses file modification timestamps, sizes and SHA-256 fingerprints to identify changes. The detector applies an explainable rule to a rolling ten-second window. The CLI menu displays events and incidents, while JSON and text files retain a record for review. The response feature changes only incident status and does not kill processes, quarantine files or disable network access.

## 6. Tools and environment

- **Operating system:** Kali Linux, Parrot OS, Ubuntu or another approved computer with Python 3.9+; also works with Windows Python 3.
- **Programming language:** Python 3 (standard library only).
- **Libraries:** `pathlib`, `hashlib`, `datetime`, `json`, `threading`, `time`, `collections`, `uuid`, `os`.
- **Interface:** Terminal menu; no GUI required.
- **Start command:** `python3 main.py`
- **Test command:** `python3 -m unittest discover -s tests -v`
- **Optional self-demo:** `python3 main.py --quick-demo`

## 7. Development methodology

The application was broken into the file monitor, event store, detector, analyst response, and reporting functions. A narrow training directory was created with six fictional sample files. The initial scan forms the baseline so launching the application does not immediately trigger an alert. Subsequent snapshots are compared to identify changes. The detector evaluates distinct changed filenames in a rolling window and applies a cooldown to avoid duplicate alerts. A state-only response workflow preserves an audit trail. Finally, unit tests exercise expected behavior and boundary conditions.

## 8. Tests and results

**Developer validation (isolated environment, 13 November 2026):** Thirteen unit tests passed. In a separate quick demonstration, a single-file update generated one MODIFIED event and **zero new alerts**. Five rapid distinct-file updates generated **one new HIGH alert**. The incident contained affected filenames and supporting event references. A simulated response changed the alert status without modifying training files.

**Class's own demonstration results:** [Insert the test date, workstation, actual screenshots, generated report path, and observations once the group runs the application. Do not present the isolated developer test as the class's own observation.]

## 9. Alert investigation and response

A HIGH alert identifies the burst rule, its detection window, the number of distinct changed files, affected filenames and supporting event IDs. The analyst first inspects the timeline to confirm that a burst occurred. The analyst can mark the incident ACKNOWLEDGED. A subsequent action sets the state to CONTAINMENT_SIMULATED, with an audit entry recording the analyst and time. This is a workflow demonstration only; the program does not isolate a device or suspend processes.

## 10. Challenges, false positives, and limitations

- A legitimate bulk edit to five sample files could trigger the same high alert as a suspicious scripted edit (false positive).
- A suspicious action that modifies only one file may be missed (false negative).
- Polling can miss changes occurring and reverting entirely between scans.
- The monitor sees only `.txt` files inside the training folder, not processes, network traffic, real devices or operating-system telemetry.
- The incident store is local and lacks enterprise security controls such as tamper-resistant central logging, centrally managed endpoint agents, and threat-intelligence integration.
- Containment is intentionally simulated, not real.

## 11. Conclusion and lessons learned

The prototype demonstrates how endpoint telemetry can support detection and analyst decision-making. Its strongest educational value is the transparent chain from observed file activity to evidence-supported alert and simulated response. The exercise also shows that alerts are not proof of malicious intent. Practical EDR requires careful thresholds, investigation, permission boundaries and validation of detection accuracy. The prototype is appropriate for a class demonstration but must not be described as a production EDR solution.

## 12. Contributions and references

**Contributions:** [Insert real student names, responsibilities, and evidence of their contribution. See `docs/TEAM_CONTRIBUTIONS_TEMPLATE.md`.]

**References:**
- Tech4Youth. (2026). *Week 6 Practical Assignment: Build a Simple Endpoint Detection and Response System* [Tutor-provided course assignment].
- Python Software Foundation. (n.d.). *Python standard library documentation*. https://docs.python.org/3/library/
- Python Software Foundation. (n.d.). *pathlib - Object-oriented filesystem paths*. https://docs.python.org/3/library/pathlib.html
- Python Software Foundation. (n.d.). *hashlib - Secure hashes and message digests*. https://docs.python.org/3/library/hashlib.html

## Appendix: Evidence to insert before submission

- **Figure 1:** Monitor starts with fictional SecureBank baseline; caption and explanation.
- **Figure 2:** Normal one-file change recorded, without an alert; caption and explanation.
- **Figure 3:** Suspicious burst across five files with HIGH alert; caption and explanation.
- **Figure 4:** Incident investigation, affected files and event IDs; caption and explanation.
- **Figure 5:** Acknowledgement and simulated containment status; caption and explanation.
- **Figure 6:** Exported event timeline and final report; caption and explanation.
- **Figure 7:** Unit-test output on the class workstation; caption and explanation.
