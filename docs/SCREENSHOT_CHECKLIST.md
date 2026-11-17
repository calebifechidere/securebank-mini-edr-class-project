# Screenshot and evidence checklist - supplied evidence set

The project lead supplied 11 screenshots. They have been reviewed, renamed consistently, and included in `evidence/`. The report appendix contains each screenshot with a caption and explanation.

| Figure | Evidence | Status |
|---:|---|---|
| 1 | Automated test suite - 24 tests passed | Supplied |
| 2 | Application startup and monitoring scope | Supplied |
| 3 | Normal file modification recorded without alert | Supplied |
| 4 | Five-file suspicious burst and event timeline | Supplied |
| 5 | Incident investigation - supporting evidence, part 1 | Supplied |
| 6 | Incident investigation - supporting evidence, part 2 | Supplied |
| 7 | Incident acknowledgement and simulated containment | Supplied |
| 8 | Incident summary and report export - second run | Supplied |
| 9 | Generated incident report contents - first run | Supplied |
| 10 | Analyst audit trail - second run | Supplied |
| 11 | MEDIUM-to-HIGH escalation and cooldown demonstration | Supplied |

## Important evidence notes

- Figures 5-7 and 9 use incident `INC-20261117061448-6CB317`.
- Figures 8 and 10 use a separate incident `INC-20261117065154-405D15`.
- Figure 11 is a separate threshold demonstration using incident `INC-20261117070153-960CB9`.
- Figure 1 shows the integrated test run from `SecureBank-Fix.TfwHx3`, while the main live demonstration screenshots show `Defence/securebank-mini-EDR`.
- For maximum consistency, rerun `python3 -m unittest discover -s tests -v` from the final project folder and capture a fresh test screenshot there.

Every screenshot should remain captioned and discussed in the final PDF. Do not combine evidence from different incident IDs into one timeline.
