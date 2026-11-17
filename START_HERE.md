# Start here — SecureBank Mini EDR

You can deploy this project later on Kali Linux, Parrot OS, Ubuntu, or another machine with Python 3.9+.

## Quick launch (Kali Linux)

Extract the ZIP, then open a terminal **inside** `SecureBank-Mini-EDR` and run:

```bash
python3 --version
python3 -m unittest discover -s tests -v
python3 main.py
```

Choose **1** for one normal change, **2** for five rapid changes, **4** for alerts, **5** to investigate, **6** to acknowledge, **7** to simulate containment, and **8** to export a report.

## Detection levels

- 1–2 distinct files within 10 seconds: no alert.
- 3–4 distinct files: MEDIUM alert.
- 5 or more distinct files: HIGH alert.
- Detection window: 10 seconds.
- Cooldown: 12 seconds.
- A MEDIUM incident can escalate to HIGH as the same incident.

## What is safe to demonstrate?

All file activity is confined to `training_files/`, which contains fictional SecureBank examples. Never copy real customer records, passwords or private files into the lab. The program logs filenames and hashes, not file content. Containment is a status-only simulation.

## What still needs group work?

The PDF is a **draft** until you add the tutor, learning centre, names and verified contributions of all classmates, and screenshots/results from the actual class machine.

Full details: `README.md` and `docs/PRESENTATION_GUIDE.md`.
