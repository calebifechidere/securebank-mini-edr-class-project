# Screenshot and evidence checklist for class submission

Capture these screenshots from **your actual demo machine**. Do not submit staged screenshots presented as genuine observations.

1. Application menu and monitoring scope (`training_files/`).
2. Normal scenario: one file update plus a recorded event and **no new alert**.
3. Suspicious scenario: five distinct file updates and a **HIGH alert**.
4. Investigation view showing incident ID, timestamp, reason, affected filenames, supporting event IDs.
5. Alert acknowledgement and status change.
6. Simulated containment and audit action (clearly label as simulation).
7. Generated incident report and event timeline from `runtime/reports/`.
8. Successful automated test output from `python3 -m unittest discover -s tests -v`.

Give every screenshot a figure number, caption, and two-sentence interpretation in the PDF. Remove personally identifying information from terminal window titles/paths where appropriate.
