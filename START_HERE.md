# Start here - SecureBank Mini EDR

## Project details
- Programme: Tech4Youth Advanced ICT Skills Training Programme - Cybersecurity Operations (Week 6)
- Learning centre: ESUT ICT and Innovation Hub
- Tutor: Mr. Noso
- Lead student: Godwin Caleb Ifechidere

## Run and verify
From the project root:

```bash
python3 --version
python3 -m unittest discover -s tests -v
python3 main.py
```

## Live demonstration sequence
1. Choose `1` to simulate one normal file modification.
2. Choose `3` to view the event timeline and `4` to confirm no alert from the one-file change.
3. Choose `2` to simulate five rapid changes across distinct sample files.
4. Choose `4` to view the alert, then `5` to investigate using the incident ID.
5. Choose `6` to acknowledge the incident.
6. Choose `7` to record simulated containment.
7. Choose `8` to export the incident report.
8. Choose `9` to exit.

## Detection levels
- 1-2 distinct files in 10 seconds: no alert.
- 3-4 distinct files: MEDIUM.
- 5 or more distinct files: HIGH.
- A MEDIUM incident may escalate to HIGH as the same incident.
- Cooldown: 12 seconds.

## Important safety boundary
The project monitors only fictional `.txt` files in `training_files/`. The containment function changes the incident status only. It does not isolate a real device or change operating-system settings.

## Documentation
- `docs/REPORT_DRAFT.md` - written class report.
- `docs/PRESENTATION_GUIDE.md` - step-by-step demonstration and tutor questions.
- `docs/PRESENTATION_QUICK_CHEATSHEET.md` - short presenter reference.
- `docs/TEAM_CONTRIBUTIONS_TEMPLATE.md` - participant and contribution record.
- `docs/SCREENSHOT_CHECKLIST.md` - evidence checklist.
- `docs/EVIDENCE_INDEX.md` - captions and notes for the supplied screenshots.
- `reports/SecureBank-Mini-EDR-Class-Report.pdf` - formatted report with screenshot appendix.
