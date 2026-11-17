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

SecureBank Mini EDR is a local Python training prototype demonstrating endpoint visibility, rule-based detection, incident investigation and safe response recording. It monitors a dedicated folder of fictional `.txt` files. Each event records its timestamp, action, filename, file size and SHA-256 digest.

The detector uses a rolling 10-second window. Three or four distinct changed files generate a MEDIUM alert, while five or more generate a HIGH alert. An existing MEDIUM incident can escalate to HIGH as the same incident. Analysts can retrieve supporting event records chronologically, acknowledge an incident and record simulated containment.

The application produces event timelines and incident summaries. It does not provide full endpoint protection or perform real containment.

## 3. Introduction and problem statement

SecureBank's fictional scenario calls for a way to notice unusual activity on workstations. A basic file-monitoring prototype allows beginners to see how telemetry becomes an event, how a rule decides to generate an alert, and how an analyst responds. A raw file modification is not necessarily malicious. The prototype therefore separates event collection from alert generation and displays evidence that supports further investigation. It uses a narrow, permission-safe training scope, rather than monitoring real private files or interfering with the host computer.

## 4. Project aims and objectives

**Aim:** Build one integrated class prototype demonstrating the visibility, detection, investigation and response workflow of EDR.

**Objectives:** (1) Monitor a dedicated fictional training folder. (2) Log created, modified and deleted `.txt` files. (3) Detect 3–4 distinct file changes as MEDIUM and 5 or more as HIGH within ten seconds. (4) Retrieve chronological supporting event records. (5) Support incident escalation, acknowledgement and simulated containment. (6) Export event timelines and incident summaries. (7) Demonstrate normal and suspicious activity.

## 5. System architecture

`training_files/` -> polling collector -> `runtime/events.jsonl` -> rolling 10-second detection window -> MEDIUM/HIGH severity evaluation -> `runtime/alerts.json` -> chronological evidence retrieval -> analyst investigation -> acknowledgement / simulated containment -> audit history and incident report.

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

The application was divided into monitoring, event storage, detection, evidence retrieval, analyst response and reporting functions. The initial scan establishes a baseline from the fictional training files. Later scans compare file modification time, size and SHA-256 fingerprints to identify changes.

The detector counts distinct changed filenames within a rolling ten-second window. Three or four files generate MEDIUM severity; five or more generate HIGH severity. A cooldown suppresses duplicate alerts, while an existing MEDIUM incident can escalate to HIGH. Supporting event IDs retrieve the original records chronologically. Unit tests validate expected behavior and boundary conditions.

## 8. Tests and results

**Integrated validation:** After PR #4 (incident evidence retrieval) and PR #5 (cooldown regression testing) were merged into the main branch, the integrated local working copy passed **24 automated unit tests** using:

`python3 -m unittest discover -s tests -v`

The tests cover baseline behavior, normal and suspicious activity, MEDIUM/HIGH thresholds, incident escalation, cooldown, chronological evidence retrieval, invalid incident handling, persistence, monitoring boundaries, simulated response and report generation.

This result was obtained in the integrated local working copy. The group must run the test suite on the actual presentation computer before reporting those results as independently verified there.

**Class's own demonstration results:** [Insert the test date, workstation, actual screenshots, generated report path and observations once the group runs the application.]

## 9. Alert investigation and response

A MEDIUM or HIGH alert identifies the detection rule, affected files and supporting event IDs. The analyst can retrieve the original event records in chronological order, including timestamps, event types, filenames, file sizes and SHA-256 hashes.

A MEDIUM incident can escalate to HIGH as the same incident when the HIGH threshold is reached within the detection window. The analyst can acknowledge the incident. A subsequent action records `CONTAINMENT_SIMULATED` and adds an audit entry with the analyst and timestamp.

This is a workflow demonstration only. The application does not isolate a device, stop processes, disable network access or quarantine files.

## 10. Challenges, false positives, and limitations

- A legitimate bulk edit to three or more sample files could trigger an alert (false positive).
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
