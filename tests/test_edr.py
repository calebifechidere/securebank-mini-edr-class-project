"""Run from project root: python3 -m unittest discover -s tests -v"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from securebank_edr.core import MiniEDR


class MiniEDRTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / "SecureBank-Mini-EDR"
        self.clock_value = [100.0]
        self.edr = MiniEDR(self.base, monotonic=lambda: self.clock_value[0])
        self.edr.initialize_baseline()

    def test_initial_baseline_generates_no_events_or_alerts(self):
        self.assertEqual(self.edr.scan_once(), [])
        self.assertEqual(self.edr.summary()["events_total"], 0)
        self.assertEqual(self.edr.summary()["alerts_total"], 0)

    def test_normal_single_file_change_does_not_alert(self):
        self.edr.simulate_normal()
        self.assertEqual(self.edr.summary()["modified"], 1)
        self.assertEqual(self.edr.summary()["alerts_total"], 0)

    def test_burst_generates_high_alert(self):
        self.edr.simulate_suspicious()
        self.assertEqual(self.edr.summary()["alerts_total"], 1)
        self.assertEqual(self.edr.alerts[-1]["severity"], "HIGH")
        self.assertGreaterEqual(len(self.edr.alerts[-1]["affected_files"]), 5)
        self.assertEqual(self.edr.alerts[-1]["status"], "NEW")

    def test_alert_contains_supporting_event_references(self):
        self.edr.simulate_suspicious()
        alert = self.edr.alerts[-1]
        all_ids = {ev["event_id"] for ev in self.edr.events}
        self.assertGreaterEqual(len(alert["supporting_event_ids"]), 5)
        self.assertTrue(set(alert["supporting_event_ids"]).issubset(all_ids))

    def test_cannot_simulate_containment_before_acknowledgement(self):
        self.edr.simulate_suspicious()
        identifier = self.edr.alerts[0]["incident_id"]
        with self.assertRaises(ValueError):
            self.edr.respond(identifier, "CONTAINMENT_SIMULATED")
        self.edr.respond(identifier, "ACKNOWLEDGED")
        self.assertEqual(self.edr.respond(identifier, "CONTAINMENT_SIMULATED")["status"], "CONTAINMENT_SIMULATED")

    def test_containment_changes_status_not_training_files(self):
        self.edr.simulate_suspicious()
        before = self.edr._current_snapshot()
        incident_id = self.edr.alerts[0]["incident_id"]
        self.edr.respond(incident_id, "ACKNOWLEDGED")
        self.edr.respond(incident_id, "CONTAINMENT_SIMULATED")
        self.assertEqual(before, self.edr._current_snapshot())
        self.assertTrue(self.edr.audit_file.exists())

    def test_out_of_scope_file_not_monitored(self):
        (self.base / "private.txt").write_text("outside the training folder", encoding="utf-8")
        self.assertEqual(self.edr.scan_once(), [])
        self.assertEqual(self.edr.summary()["events_total"], 0)

    def test_symlink_outside_training_folder_is_excluded(self):
        outside = self.base / "private.txt"
        outside.write_text("not in scope", encoding="utf-8")
        try:
            (self.edr.training / "linked.txt").symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are unavailable")
        self.assertEqual(self.edr.scan_once(), [])

    def test_simulator_refuses_symlinked_training_sample(self):
        outside = self.base / "private.txt"
        outside.write_text("not in scope", encoding="utf-8")
        link = self.edr.training / "account-summary.txt"
        link.unlink()
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are unavailable")
        with self.assertRaises(ValueError):
            self.edr.simulate_normal()
        self.assertEqual(outside.read_text(encoding="utf-8"), "not in scope")

    def test_new_txt_file_is_recorded_but_no_alert(self):
        (self.edr.training / "extra-training.txt").write_text("fictional", encoding="utf-8")
        events = self.edr.scan_once()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "CREATED")
        self.assertEqual(self.edr.summary()["alerts_total"], 0)

    def test_event_and_incident_history_persist(self):
        self.edr.simulate_suspicious()
        second = MiniEDR(self.base)
        self.assertEqual(len(second.events), 5)
        self.assertEqual(len(second.alerts), 1)
        self.assertEqual(second.alerts[0]["status"], "NEW")

    def test_report_includes_alert_reason_and_limitations(self):
        self.edr.simulate_suspicious()
        report = self.edr.export_report()
        content = report.read_text(encoding="utf-8")
        self.assertIn("INCIDENT SUMMARY", content)
        self.assertIn("5 distinct", content)
        self.assertIn("LIMITATIONS", content)

    def test_deletion_logged_but_not_counted_as_burst_trigger(self):
        for filename in ["account-summary.txt", "customer-sample.txt", "ledger-sample.txt", "branch-notes.txt", "staff-training.txt"]:
            (self.edr.training / filename).unlink()
        self.edr.scan_once()
        self.assertEqual(self.edr.summary()["deleted"], 5)
        self.assertEqual(self.edr.summary()["alerts_total"], 0)


    def test_incident_evidence_returns_supporting_events(self):
        self.edr.simulate_suspicious()
        incident = self.edr.alerts[-1]

        evidence = self.edr.get_incident_evidence(
            incident["incident_id"]
        )

        self.assertEqual(
            len(evidence),
            len(incident["supporting_event_ids"])
        )

        evidence_ids = {event["event_id"] for event in evidence}

        self.assertEqual(
            evidence_ids,
            set(incident["supporting_event_ids"])
        )

    def test_incident_evidence_is_chronological(self):
        self.edr.simulate_suspicious()
        incident = self.edr.alerts[-1]

        evidence = self.edr.get_incident_evidence(
            incident["incident_id"]
        )

        timestamps = [
            event["timestamp_utc"] for event in evidence
        ]

        self.assertEqual(timestamps, sorted(timestamps))

    def test_incident_evidence_rejects_unknown_incident(self):
        with self.assertRaises(KeyError):
            self.edr.get_incident_evidence("INVALID-ID")


if __name__ == "__main__":
    unittest.main()
