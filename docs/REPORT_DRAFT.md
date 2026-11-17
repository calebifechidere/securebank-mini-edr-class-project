# SecureBank Mini EDR
## Class Project Report

**Project:** SecureBank Mini EDR - Endpoint Detection and Response Training Prototype  
**Programme:** Tech4Youth Advanced ICT Skills Training Programme - Cybersecurity Operations (Week 6)  
**Learning centre:** ESUT ICT and Innovation Hub  
**Tutor:** Mr. Noso  
**Lead student:** Godwin Caleb Ifechidere  
**Report / evidence date:** 17 November 2026  

> **Roster note:** Eleven participant identities were supplied for this report update. The assignment brief refers to 20 learners; the remaining nine names and individual contribution details must be confirmed before final submission. The report does not invent names or allocate work without evidence.

## 1. Executive summary

SecureBank Mini EDR is a local Python training prototype that demonstrates the core workflow of Endpoint Detection and Response: endpoint visibility, event collection, rule-based detection, alert generation, investigation, response recording, and reporting. It monitors only a dedicated folder containing fictional `.txt` files. The collector compares file modification time, size, and SHA-256 fingerprints and records observed changes as structured events.

The detector uses a rolling ten-second window. One or two distinct changed files do not generate an alert; three or four generate MEDIUM severity; five or more generate HIGH severity. An existing MEDIUM incident can escalate to HIGH without creating a separate incident. A 12-second cooldown suppresses duplicate alerts from rapid consecutive bursts. The analyst can retrieve supporting events chronologically, acknowledge an incident, and record containment as simulated.

The supplied evidence includes a 24-test successful automated test run, normal and suspicious activity demonstrations, incident investigation, acknowledgement, simulated containment, report export, audit history, and a separate severity escalation/cooldown demonstration. This is an educational prototype, not a production EDR platform.

## 2. Introduction and problem statement

The fictional SecureBank scenario requires a way to notice unusual activity on employee endpoints. Without monitoring, a rapid series of changes to files may go unnoticed. An EDR workflow helps an organisation collect endpoint telemetry, identify patterns that may be suspicious, create alerts, and support an analyst's investigation and response.

The class project demonstrates this workflow in a safe and limited environment. It uses fictional sample files rather than real customer information and does not interfere with the host operating system. A file change alone is not proof of an attack; the analyst must examine the event sequence and supporting evidence before deciding what action is appropriate.

## 3. Aim and objectives

**Aim:** To build one integrated class prototype that demonstrates visibility, detection, investigation, response recording, and reporting.

**Objectives:**
1. Monitor a dedicated folder containing fictional training files.
2. Record created, modified, and deleted `.txt` file events.
3. Detect three or four distinct changed files as MEDIUM and five or more as HIGH within ten seconds.
4. Retrieve the supporting event records in chronological order.
5. Support MEDIUM-to-HIGH escalation, acknowledgement, and simulated containment.
6. Export event timelines and incident summaries.
7. Demonstrate both normal activity and suspicious activity.
8. Validate the integrated application using automated tests.

## 4. System architecture

The project follows this data flow:

```text
training_files/ (fictional .txt files)
             |
             v
Python polling collector and baseline
             |
             v
runtime/events.jsonl (event records)
             |
             v
Rolling 10-second detection window
             |
       +-----+------------------+
       |                        |
    1-2 files                 3+ files
    No alert                     |
                         +-------+-------+
                         |               |
                       3-4             5+
                     MEDIUM          HIGH
                         |               |
                         +-------+-------+
                                 |
                                 v
                       runtime/alerts.json
                                 |
                                 v
                    Chronological evidence lookup
                                 |
                                 v
                      Analyst investigation
                                 |
                                 v
                    Acknowledge / simulate response
                                 |
                                 v
                        runtime/audit.jsonl
                                 |
                                 v
                      Incident summary report
```

### Main components

| Component | Responsibility |
|---|---|
| `main.py` | Application entry point. |
| `securebank_edr/core.py` | Monitoring, baseline comparison, event collection, detection, evidence retrieval, response state, and persistence. |
| `securebank_edr/cli.py` | Terminal menu and demonstration actions. |
| `training_files/` | Fictional `.txt` files monitored by the prototype. |
| `runtime/events.jsonl` | Structured file activity records. |
| `runtime/alerts.json` | Alert and incident records. |
| `runtime/audit.jsonl` | Analyst response actions. |
| `runtime/reports/` | Human-readable incident summary reports. |
| `tests/` | Automated tests for monitoring, detection, escalation, cooldown, evidence, and response. |

## 5. Tools and environment

- Operating system used in the captured demonstration: Kali Linux.
- Programming language: Python 3.
- Dependencies: Python standard library; no third-party packages required.
- Interface: terminal-based menu.
- Main launch command: `python3 main.py`.
- Test command: `python3 -m unittest discover -s tests -v`.
- Monitoring scope: local `.txt` files inside the project's `training_files/` directory.

The captured application startup screenshot shows the project path `~/Downloads/Defence/securebank-mini-EDR` and the monitoring path beneath that project directory.

## 6. Development methodology

The application was organised into monitoring, event storage, detection, investigation, response, and reporting functions. At startup, the initial scan establishes a baseline of the fictional training files. Subsequent scans compare each file's modification time, size, and SHA-256 fingerprint with the previous snapshot. Differences are recorded as events with a timestamp, event type, relative filename, file size, and fingerprint.

The detector evaluates distinct created or modified filenames in a rolling ten-second window. The thresholds are:
- 1-2 distinct files: no alert.
- 3-4 distinct files: MEDIUM.
- 5 or more distinct files: HIGH.

A MEDIUM incident can escalate to HIGH as the same incident when further distinct changes reach the HIGH threshold. A 12-second cooldown suppresses duplicate alerts from rapid consecutive bursts. The incident stores supporting event IDs, which are used to retrieve the original event records chronologically.

## 7. Testing and results

### 7.1 Automated testing

The supplied terminal screenshot records **24 automated tests passed** with no failures. The suite covers:
- Initial baseline without alerts.
- Normal single-file change without an alert.
- Suspicious multi-file burst detection.
- MEDIUM and HIGH severity thresholds.
- Escalation of a MEDIUM incident to HIGH as the same incident.
- Cooldown behaviour during rapid consecutive bursts.
- Chronological incident evidence retrieval.
- Unknown incident and missing evidence handling.
- Event and incident persistence.
- Safe simulated containment.
- Monitoring scope and symlink handling.
- Incident report generation.

**Evidence qualification:** The test screenshot's terminal title shows the integrated working-copy path `~/Downloads/SecureBank-Fix.TfwHx3`. The live demonstration screenshots show the clean project path `~/Downloads/Defence/securebank-mini-EDR`. For a perfectly consistent final evidence set, the class should rerun the test command from the final project folder and replace Figure 1 with that capture if required by the tutor.

### 7.2 Normal activity demonstration

The application was started from the clean project folder. The normal simulation updated one fictional sample file. The event appeared in the timeline as a MODIFIED event, and the alert view reported that no alert was generated. This demonstrates that the collector records activity while the detector avoids raising an alert for a single-file change.

### 7.3 Suspicious activity demonstration

The suspicious simulation updated five distinct fictional sample files rapidly. The application reported one additional alert and displayed the related event timeline. The subsequent incident investigation identified the incident as HIGH severity and displayed the rule reason, affected files, and supporting event IDs.

### 7.4 Severity escalation and cooldown demonstration

A separate isolated demonstration showed three distinct file changes producing a MEDIUM incident. After two additional distinct files changed, the same incident ID was displayed with HIGH severity. The total alert count remained one. A further immediate suspicious burst during cooldown did not increase the alert count. This demonstrates escalation and duplicate-alert suppression.

## 8. Incident investigation and response

### 8.1 Main investigation run

The primary investigation evidence relates to incident:

**Incident ID:** `INC-20261117061448-6CB317`  
**Severity:** HIGH  
**Initial status shown during investigation:** NEW  
**Rule reason:** Five distinct training `.txt` files changed within ten seconds.

The affected files were:
- `account-summary.txt`
- `branch-notes.txt`
- `customer-sample.txt`
- `ledger-sample.txt`
- `staff-training.txt`

The investigation view displayed five supporting event IDs and the corresponding timestamps, event types, filenames, file sizes, and SHA-256 fingerprints. The analyst then acknowledged the incident and recorded `CONTAINMENT_SIMULATED`. The exported report for this run records six total events, one alert, and the response history.

### 8.2 Separate audit/export run

A separate isolated demonstration used incident `INC-20261117065154-405D15`. Its audit log records:
- `ACKNOWLEDGED` at 2026-11-17 06:52:29 UTC.
- `CONTAINMENT_SIMULATED` at 2026-11-17 06:52:37 UTC.

The corresponding report-export screenshot shows the report being generated in a temporary workspace. This is a separate run and is not the same incident as the primary investigation above.

### 8.3 Meaning of the response

Acknowledgement records that an analyst has taken responsibility for reviewing the incident. Simulated containment changes the incident's recorded status and writes an audit entry. It does not isolate a computer, kill a process, disable network access, or quarantine a real file.

## 9. Challenges, false positives, and limitations

- A legitimate bulk update affecting three or more files within ten seconds may trigger an alert (false positive).
- Suspicious activity affecting fewer than three files, or occurring slowly, may not trigger the rule (false negative).
- Polling may miss a file change that occurs and reverts between scans.
- The monitor sees only `.txt` files in the dedicated training folder.
- It does not inspect processes, network connections, memory, registry activity, or operating-system telemetry.
- Local logs are not tamper-resistant enterprise records.
- The prototype has no central management console or threat-intelligence integration.
- Containment is intentionally simulated only.

## 10. Conclusion and lessons learned

SecureBank Mini EDR demonstrates how a small monitoring program can convert endpoint activity into structured events, apply a transparent detection rule, raise alerts, retrieve supporting evidence, and record analyst response actions. The project shows the importance of separating event collection from alerting and of investigating an alert rather than assuming it proves malicious activity.

The class also demonstrated severity escalation, cooldown, evidence retrieval, and report generation. The main lesson is that useful security monitoring requires clear scope, understandable detection logic, traceable evidence, safe response procedures, testing, and honest communication of limitations. The prototype is suitable for teaching and demonstration, but it is not a production EDR solution.

## 11. Student roster and contributions

The following 11 participant identities were supplied for this report. Individual responsibilities have not been assigned in this document because verified contribution details were not supplied. Each learner should complete the contribution record in `docs/TEAM_CONTRIBUTIONS_TEMPLATE.md`.

1. **Godwin Caleb Ifechidere** - `@calebifechidere`
2. **Full name not supplied** - `@benardemerald8-ship-it`
3. **Full name not supplied** - `@edenchris-design`
4. **Full name not supplied** - `@erulydia2-lab`
5. **Eya George Ibezimako** - `@iamalex-geoege`
6. **Shepherd** - `@Ireogueche`
7. **John Josiah** - `@johnjosiah765`
8. **Full name not supplied** - `@kingziipromise-hub`
9. **Full name not supplied** - `@MARVEL-102`
10. **Full name not supplied** - `@okaforchiamaka8716-creator`
11. **Ifechukwu Michael Ozoigwe** - `@Phantom-Vector`

**Outstanding roster item:** The assignment brief refers to 20 learners. Nine additional names have not yet been supplied. The full class list and each learner's actual contribution should be confirmed before the final class submission.

## 12. References

1. Tech4Youth. (2026). *Week 6 Practical Assignment: Build a Simple Endpoint Detection and Response System* [Tutor-provided assignment].
2. Python Software Foundation. *Python standard library documentation*. https://docs.python.org/3/library/
3. Python Software Foundation. *pathlib - Object-oriented filesystem paths*. https://docs.python.org/3/library/pathlib.html
4. Python Software Foundation. *hashlib - Secure hashes and message digests*. https://docs.python.org/3/library/hashlib.html

## Appendix A. Demonstration screenshots

Each screenshot is captioned and discussed in the PDF appendix. See `docs/EVIDENCE_INDEX.md` for the evidence inventory and run-separation notes.

**Evidence integrity:** The primary investigation, second audit/export run, and severity escalation demonstration have different incident IDs. They are presented as separate runs and must not be combined into one incident timeline.
