# SecureBank Mini EDR — Step-by-Step Presentation Guide

This guide explains the application in beginner-friendly language and gives a repeatable live demonstration sequence. The class must use one shared application and each learner must be ready to explain their genuine contribution.

## A. Understand the project in one minute

SecureBank is a fictional bank. The class is building a small Python program that watches one dedicated folder containing fictional `.txt` training files. It records file changes, checks whether several different files change within a short period, raises an alert when the rule is met, and lets an analyst record a safe simulated response.

The prototype demonstrates five stages:

1. **Visibility:** observe activity in the training folder.
2. **Detection:** apply a clear rule to the recorded activity.
3. **Alerting:** show an alert when the rule is met.
4. **Investigation and response:** review the evidence, acknowledge the incident and simulate containment.
5. **Reporting:** save an event timeline and incident summary.

It is a classroom prototype, not a complete endpoint protection product.

## B. Important terms to understand

| Term | Simple meaning in this project |
|---|---|
| Endpoint | A computer or laptop that needs protection. |
| EDR | Endpoint Detection and Response: monitoring activity, identifying suspicious patterns and supporting a response. |
| Monitoring | Checking the training folder repeatedly for changes. |
| Baseline | The first snapshot of the sample files when the application starts. It gives the program a starting point for comparison. |
| Telemetry | Recorded details about activity, such as time, filename, file size and file hash. |
| Event | One observed action, such as a file being created, modified or deleted. |
| Detection rule | The condition used to decide whether recorded events are unusual. |
| Alert | A warning created when the rule is met. An alert is a reason to investigate, not proof of an attack. |
| Investigation | Reviewing the alert, timestamps, affected files and supporting event IDs. |
| Response | The action an analyst records after reviewing an alert. In this prototype, containment is simulated only. |
| Audit record | A record of the analyst action and when it was taken. |
| False positive | Normal activity incorrectly triggers an alert. |
| False negative | Suspicious activity happens but the rule does not detect it. |

## C. Know exactly what the program monitors

- It watches only `.txt` files inside `training_files/` in the project directory.
- It checks the folder about every 0.5 seconds while running.
- It compares each file's modification time, size and SHA-256 fingerprint with the previous snapshot.
- It records file creation, modification and deletion events.
- Created and modified files are counted by the detection rule. Deletions are logged but do not count toward the burst rule.
- It does not save the contents of the files in the event log.
- It does not monitor the whole computer, processes, network traffic or other folders.

## D. Understand the detection rule

The rule is deliberately simple and explainable:

> Raise one HIGH alert when **five or more different `.txt` files** are created or modified within a **rolling 10-second window**.

The word **different** matters. Changing the same file five times does not count as five different files. The detector counts distinct file paths.

A 12-second cooldown prevents repeated alerts from one burst. If a second suspicious simulation does not create a new alert immediately, wait at least 12 seconds and try again.

## E. Prepare the computer before the presentation

1. Extract the ZIP file.
2. Open a terminal inside the `SecureBank-Mini-EDR` folder.
3. Check Python:

   ```bash
   python3 --version
   ```

4. For a clean first demonstration only, clear previously generated runtime records:

   ```bash
   rm -rf runtime
   ```

   This removes only the application's generated logs and reports. It does not remove the training files or source code.

5. Run the automated tests:

   ```bash
   python3 -m unittest discover -s tests -v
   ```

6. Start the application:

   ```bash
   python3 main.py
   ```

No administrator privileges, external packages or internet connection are required.

## F. Live demonstration — follow these exact steps

### Step 1: Introduce the system

Say: “This is SecureBank Mini EDR. SecureBank is a fictional organisation. Our prototype monitors only the sample text files in the `training_files` folder. It demonstrates how file activity becomes events, how a detection rule creates an alert, and how an analyst records a response.”

Show the printed monitoring path and explain that the original sample files form the baseline.

### Step 2: Demonstrate normal activity

1. At the menu, enter `1` and press Enter.
2. The program updates one fictional sample file.
3. Enter `3` to view the event timeline.
4. Point out the `MODIFIED` event, timestamp, filename and event ID.
5. Enter `4` to view alerts. There should be no new HIGH alert from this one-file change.

Say: “The system has visibility because it recorded the change. It did not raise a HIGH alert because one changed file is below the threshold of five different files.”

### Step 3: Demonstrate suspicious activity

1. Enter `2` and press Enter.
2. The program rapidly updates five different fictional sample files.
3. Enter `3` to show the events.
4. Enter `4` to show the HIGH alert.
5. Read the rule reason and point out the five affected filenames.

Say: “The detection rule found five different files changed within ten seconds. It generated a HIGH alert and attached supporting event IDs so the analyst can trace the evidence.”

### Step 4: Investigate the alert

1. From option `4`, copy the incident ID shown on the alert line.
2. Enter `5`.
3. Paste the incident ID and press Enter.
4. Point out the severity, status, reason, affected files and supporting event IDs.

Say: “An alert is not proof that an attack happened. The analyst reviews the timestamps and affected files to decide whether the activity is expected or needs further investigation.”

### Step 5: Acknowledge the alert

1. Enter `6`.
2. Paste the same incident ID.
3. The status should change to `ACKNOWLEDGED`.

Say: “Acknowledgement records that an analyst has taken responsibility for reviewing the incident. The action is also written to the audit log.”

### Step 6: Simulate containment

1. Enter `7`.
2. Paste the same incident ID.
3. The status should change to `CONTAINMENT_SIMULATED`.

Say: “This is only a simulation. The program changes the incident status and records the analyst action. It does not isolate a real computer, stop processes, disable network access or quarantine files.”

### Step 7: Generate the report

1. Enter `8`.
2. Show the summary counts.
3. Point out the path to the generated report under `runtime/reports/`.
4. Open the report in a text editor and show the event timeline and incident response history.
5. Enter `9` to exit when finished.

Say: “The report preserves the event sequence, alert reason, affected files and response actions for later review.”

## G. Understand the files created by the application

| Path | What it contains |
|---|---|
| `training_files/` | Fictional sample text files watched by the program. |
| `runtime/events.jsonl` | One JSON record per observed file event. |
| `runtime/alerts.json` | Alert and incident details, including status. |
| `runtime/audit.jsonl` | Analyst acknowledgement and simulated-response actions. |
| `runtime/reports/` | Human-readable incident summary reports. |

## H. Explain the architecture

Use this sequence when pointing at the architecture diagram:

`training_files/` → **collector** → **event log** → **detection rule** → **alert** → **analyst investigation** → **response record** → **report**.

- The **collector** checks the files and identifies differences from the last snapshot.
- The **event log** stores the observation and supporting metadata.
- The **detection rule** counts distinct created or modified files in the ten-second window.
- The **alert** stores the reason and event references.
- The **analyst** reviews the evidence and records an action.
- The **report** presents the event and incident history.

## I. Questions the tutor may ask

**1. What does EDR mean?**

Endpoint Detection and Response. It is a security approach used to monitor endpoint activity, detect suspicious behaviour and support investigation and response.

**2. What is an endpoint?**

A device such as a workstation, desktop or laptop that connects to an organisation's systems or network.

**3. What is telemetry in this project?**

The metadata collected about file activity: timestamp, event type, relative filename, file size and SHA-256 fingerprint.

**4. Why do you need a baseline?**

The baseline records the starting state of the sample files. Without it, the program would not know which files were already present before monitoring began.

**5. Why does one changed file not trigger an alert?**

The rule requires five different files to be created or modified within ten seconds. One file is below that threshold.

**6. Why did you choose five files in ten seconds?**

It is a simple demonstration threshold supplied by the project design. It makes the normal and suspicious scenarios easy to reproduce and explain. It is not a universal security rule.

**7. What is a false positive?**

A legitimate bulk update that changes five files within ten seconds could trigger the alert even though no attack occurred.

**8. What is a false negative?**

An unusual action that changes fewer than five files, or changes them slowly, may not trigger this rule.

**9. What is SHA-256 used for?**

It creates a digital fingerprint of a file's contents. The program compares the fingerprint between scans to help identify content changes. It does not decrypt or reveal the file contents.

**10. Does this application provide real containment?**

No. It only changes the incident status to `CONTAINMENT_SIMULATED` and records the action. It does not alter the operating system or isolate the device.

**11. What are the limitations?**

It monitors only text files in one folder, uses periodic polling, applies one threshold rule, may produce false positives or miss activity, and does not inspect processes or network traffic.

**12. How did you test it?**

The supplied automated test suite checks baseline behaviour, normal changes, burst detection, evidence references, response order, logging, report generation and monitoring boundaries. The group must also run and capture the demonstration on its own presentation machine.

## J. Suggested presentation timing from the tutor's brief

| Segment | Suggested time | What to cover |
|---|---:|---|
| Introduction | 3 minutes | EDR and the fictional SecureBank problem. |
| Architecture | 4 minutes | Monitoring, collection, detection, alert and response. |
| Live demonstration | 8 minutes | Baseline, normal activity, suspicious activity, alert and response. |
| Class contributions | 10–15 minutes | Each learner explains their actual contribution. |
| Questions | 5 minutes | Rules, evidence, false positives and limitations. |

## K. Final checklist before submission

- [ ] Run the program on the actual class presentation computer.
- [ ] Run the automated tests and capture the real terminal output.
- [ ] Capture the baseline and normal-activity scenario.
- [ ] Capture the suspicious five-file scenario and HIGH alert.
- [ ] Capture investigation, acknowledgement and simulated containment.
- [ ] Capture the generated report.
- [ ] Add a caption and explanation for every screenshot in the PDF.
- [ ] Add the tutor, learning centre, presentation date and all actual student names.
- [ ] Complete the contribution record truthfully.
- [ ] Ensure every learner can explain at least one part of the system.
