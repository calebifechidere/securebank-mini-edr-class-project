# Evidence Index - SecureBank Mini EDR

The following screenshots were supplied by the project lead and reviewed for the report. Evidence is dated 17 November 2026 based on visible terminal timestamps.

## Evidence interpretation

### Figure 1: Automated test suite - 24 tests passed.

File: `evidence/01-automated-test-suite-24-tests-passed.png`

The terminal output shows 24 successful unit tests and no failures. The terminal title shows the integrated working-copy folder `SecureBank-Fix.TfwHx3`; rerun the same command from the final submission folder if a single-path evidence set is required.

### Figure 2: Application startup and monitoring scope.

File: `evidence/02-application-startup-and-monitoring-scope.png`

The application starts from `Defence/securebank-mini-EDR` and prints the exact `training_files/` monitoring path. It also shows the normal single-file simulation completing without a new alert.

### Figure 3: Normal file modification recorded without an alert.

File: `evidence/03-normal-file-change-recorded-no-alert.png`

One fictional sample file is modified and appears in the event timeline. The alert view reports that no alert was generated, demonstrating that event visibility and alerting are separate.

### Figure 4: Five-file suspicious burst and event timeline.

File: `evidence/04-five-file-suspicious-burst-and-event-timeline.png`

The simulator reports five fictional sample files updated and one additional alert generated. The timeline shows the five distinct file modifications. The HIGH severity is confirmed in the incident investigation evidence that follows.

### Figure 5: Incident investigation and supporting evidence - part 1.

File: `evidence/05-incident-investigation-supporting-evidence-part-1.png`

Incident `INC-20261117061448-6CB317` is shown as HIGH and NEW. The rule reason, affected filenames, and supporting event IDs are visible.

### Figure 6: Incident investigation and supporting evidence - part 2.

File: `evidence/06-incident-investigation-supporting-evidence-part-2.png`

The remaining event records show timestamps, event types, filenames, file sizes, and SHA-256 fingerprints. The evidence is retrieved using the incident's supporting event IDs.

### Figure 7: Incident acknowledgement and simulated containment.

File: `evidence/07-incident-acknowledgement-and-simulated-containment.png`

For incident `INC-20261117061448-6CB317`, the application records `ACKNOWLEDGED` and then `CONTAINMENT_SIMULATED`. No real endpoint containment is performed.

### Figure 8: Incident summary and report export - separate demonstration run.

File: `evidence/08-incident-summary-and-report-export-second-run.png`

A second isolated run uses incident `INC-20261117065154-405D15`. Option 8 exports a report under the temporary workspace path shown in the screenshot.

### Figure 9: Generated incident report contents - first demonstration run.

File: `evidence/09-generated-incident-report-contents-first-run.png`

The report for incident `INC-20261117061448-6CB317` records six events, one HIGH alert, five affected training files, the response history, and prototype limitations.

### Figure 10: Analyst audit trail - second demonstration run.

File: `evidence/10-analyst-audit-trail-second-run.png`

The audit log for incident `INC-20261117065154-405D15` records acknowledgement at 06:52:29 UTC and simulated containment at 06:52:37 UTC.

### Figure 11: MEDIUM-to-HIGH escalation and cooldown demonstration.

File: `evidence/11-medium-high-escalation-and-cooldown-demonstration.png`

An isolated demonstration shows three file changes producing MEDIUM, then five distinct changes escalating the same incident ID to HIGH. The alert count remains one, and an immediate repeat burst does not create a duplicate alert.

## Evidence integrity and run separation

- Figures 5-7 and Figure 9 relate to incident `INC-20261117061448-6CB317`.
- Figures 8 and 10 relate to a separate isolated run, incident `INC-20261117065154-405D15`. They must not be presented as if they are the same incident as Figures 5-7.
- Figure 11 is a separate severity-escalation demonstration with incident `INC-20261117070153-960CB9`.
- Figure 1 shows the 24-test run from the integrated working-copy folder `SecureBank-Fix.TfwHx3`; Figures 2-10 show the clean project folder or isolated workspaces.
- The screenshots are genuine terminal captures. Captions distinguish the runs and do not combine separate incident IDs.