# SecureBank Mini EDR - Step-by-Step Presentation Guide

## Project details
- Programme: Tech4Youth Advanced ICT Skills Training Programme - Cybersecurity Operations (Week 6)
- Learning centre: ESUT ICT and Innovation Hub
- Tutor: Mr. Noso
- Lead student: Godwin Caleb Ifechidere
- Evidence capture date: 17 November 2026

## A. Explain the project simply

SecureBank is a fictional bank. This Python program watches one dedicated folder containing fictional `.txt` training files. It records file changes, checks whether several different files change within a short period, raises an alert when the rule is met, and lets an analyst record a safe simulated response.

The five stages are:
1. Visibility - observe activity in the training folder.
2. Detection - apply a clear rule to recorded activity.
3. Alerting - create an alert when the rule is met.
4. Investigation and response - review evidence, acknowledge the incident, and simulate containment.
5. Reporting - save the event timeline, audit history, and incident summary.

This is a classroom prototype, not a complete endpoint protection product.

## B. Detection rule

The detector uses a rolling 10-second window:

| Different files changed | Result |
|---|---|
| 1-2 files | No alert |
| 3-4 files | MEDIUM alert |
| 5 or more files | HIGH alert |

The files must be different. Repeatedly changing one file does not count as multiple distinct files. A MEDIUM incident can escalate to HIGH as the same incident. A 12-second cooldown suppresses duplicate alerts from rapid consecutive bursts.

## C. What the system monitors

- Only `.txt` files inside `training_files/`.
- It compares file modification time, size, and SHA-256 fingerprint.
- It records created, modified, and deleted file events.
- Created and modified files count toward the burst rule; deletions are logged but do not count.
- File contents are not stored in the event log.
- It does not monitor processes, network traffic, or other folders.

## D. Prepare and run

From the project root:

```bash
python3 --version
python3 -m unittest discover -s tests -v
python3 main.py
```

No administrator privileges, third-party packages, or internet connection are required.

## E. Live demonstration script

### 1. Introduce the application

Say: "This is SecureBank Mini EDR. It monitors only fictional text files in a dedicated training folder. It records file activity, applies a detection rule, raises alerts when the rule is met, and allows an analyst to investigate and record a safe response."

Point to the monitoring path printed at startup.

### 2. Demonstrate normal activity

- Enter `1` to update one fictional sample file.
- Enter `3` to view the event timeline.
- Enter `4` to view alerts.

Say: "The system recorded the file modification, but one changed file is below the alert threshold. This demonstrates that not every event is suspicious."

Expected observation: one MODIFIED event and no new alert.

### 3. Demonstrate suspicious activity

- Enter `2` to update five different fictional files quickly.
- Enter `3` to view the event timeline.
- Enter `4` to view the HIGH alert.

Say: "Five different files changed within ten seconds. The rule classified this burst as HIGH and attached supporting event IDs for investigation."

### 4. Investigate the incident

- Copy the incident ID shown in the alert.
- Enter `5` and paste the incident ID.
- Point out severity, status, rule reason, affected filenames, supporting event IDs, timestamps, file sizes, and SHA-256 hashes.

Say: "An alert is not proof of an attack. The analyst checks the supporting evidence and decides whether the activity is expected or requires escalation."

### 5. Acknowledge the incident

- Enter `6` and provide the same incident ID.

Say: "Acknowledgement records that an analyst has taken responsibility for reviewing the incident. The action is retained in the audit log."

### 6. Simulate containment

- Enter `7` and provide the same incident ID.

Say: "This is a simulation only. The application changes the incident status and records the action. It does not isolate a real computer, stop processes, disable network access, or quarantine files."

### 7. Export the report

- Enter `8`.
- Point out the event counts, alert status, report path, and response history.
- Open the generated text report.
- Enter `9` to exit.

Say: "The report preserves the event sequence, alert reason, affected files, and response actions for later review."

## F. Explain the architecture

```text
training_files/
      |
      v
Polling collector and baseline
      |
      v
runtime/events.jsonl
      |
      v
Rolling 10-second detection rule
      |
      +--> 1-2 files: no alert
      +--> 3-4 files: MEDIUM
      +--> 5+ files: HIGH
      |
      v
runtime/alerts.json
      |
      v
Chronological evidence retrieval
      |
      v
Analyst investigation
      |
      v
Acknowledgement / simulated containment
      |
      v
Audit log and incident report
```

## G. Important questions the tutor may ask

**What does EDR mean?**  
Endpoint Detection and Response. It is a security approach for monitoring endpoint activity, detecting suspicious patterns, investigating alerts, and supporting response.

**What is an endpoint?**  
A computer or device connected to an organisation's systems or network.

**What is a baseline?**  
The initial snapshot of the sample files. It gives the application a starting point for detecting later changes.

**What is telemetry?**  
Recorded metadata about activity, such as timestamp, event type, filename, file size, and SHA-256 fingerprint.

**Why does one file change not trigger an alert?**  
One or two distinct files are below the threshold. Three or four trigger MEDIUM; five or more trigger HIGH.

**What is a false positive?**  
Legitimate bulk activity that changes three or more files within ten seconds may trigger an alert.

**What is a false negative?**  
Suspicious activity affecting fewer than three files or occurring slowly may not trigger this rule.

**What is SHA-256 used for?**  
It creates a digital fingerprint used to help identify content changes. It does not reveal or decrypt the file contents.

**Does the application provide real containment?**  
No. It records `CONTAINMENT_SIMULATED` and adds an audit entry. It does not isolate a real endpoint.

**What does cooldown do?**  
It suppresses duplicate alerts from rapid consecutive bursts. It also supports a MEDIUM-to-HIGH escalation workflow without creating a second incident.

## H. Limitations to state clearly

- It monitors only `.txt` files in one dedicated folder.
- It uses polling and may miss very short-lived changes.
- A legitimate bulk update may create a false positive.
- Smaller or slower suspicious activity may be missed.
- It does not inspect processes, network traffic, or operating-system telemetry.
- Containment is simulated only.
- It is a teaching prototype, not production EDR software.

## I. Evidence captured for this report

Eleven screenshots are included in `evidence/` and discussed in `docs/EVIDENCE_INDEX.md`. The main incident investigation sequence uses incident `INC-20261117061448-6CB317`. A separate audit/export run uses `INC-20261117065154-405D15`, and a separate threshold demonstration uses `INC-20261117070153-960CB9`. Keep these runs distinct when explaining the evidence.

## J. Presentation timing from the assignment brief

| Segment | Suggested time |
|---|---:|
| Introduction | 3 minutes |
| Architecture | 4 minutes |
| Live demonstration | 8 minutes |
| Class contributions | 10-15 minutes |
| Questions | 5 minutes |

Every learner should be able to explain their actual contribution. Complete the contribution record in `docs/TEAM_CONTRIBUTIONS_TEMPLATE.md`.
