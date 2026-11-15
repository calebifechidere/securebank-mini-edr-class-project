"""Tests for the MEDIUM/HIGH severity tiers. Run: python3 -m unittest discover -s tests -v"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from securebank_edr.core import MiniEDR


class SeverityTierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name) / "SecureBank-Mini-EDR"
        self.clock_value = [100.0]
        self.edr = MiniEDR(self.base, monotonic=lambda: self.clock_value[0])
        self.edr.initialize_baseline()

    def _change(self, start, stop, tag):
        """Append a harmless line to training files [start:stop], then scan once."""
        files = sorted(self.edr.training.glob("*.txt"))
        self.assertGreaterEqual(len(files), stop)
        for path in files[start:stop]:
            with path.open("a", encoding="utf-8") as fh:
                fh.write(f"\n{tag}\n")
        self.edr.scan_once()

    def test_two_files_do_not_alert(self):
        self._change(0, 2, "two")
        self.assertEqual(self.edr.summary()["alerts_total"], 0)

    def test_three_files_raise_medium_alert(self):
        self._change(0, 3, "three")
        self.assertEqual(self.edr.summary()["alerts_total"], 1)
        self.assertEqual(self.edr.alerts[-1]["severity"], "MEDIUM")
        self.assertEqual(len(self.edr.alerts[-1]["affected_files"]), 3)

    def test_four_files_stay_medium(self):
        self._change(0, 4, "four")
        self.assertEqual(self.edr.summary()["alerts_total"], 1)
        self.assertEqual(self.edr.alerts[-1]["severity"], "MEDIUM")

    def test_five_files_end_as_one_high_incident(self):
        self._change(0, 5, "five")
        self.assertEqual(self.edr.summary()["alerts_total"], 1)
        alert = self.edr.alerts[-1]
        self.assertEqual(alert["severity"], "HIGH")
        self.assertGreaterEqual(len(alert["supporting_event_ids"]), 5)

    def test_medium_escalates_to_high_as_the_same_incident(self):
        self._change(0, 3, "first")
        first_id = self.edr.alerts[-1]["incident_id"]
        self.assertEqual(self.edr.alerts[-1]["severity"], "MEDIUM")
        self._change(3, 5, "second")
        self.assertEqual(self.edr.summary()["alerts_total"], 1)
        alert = self.edr.alerts[-1]
        self.assertEqual(alert["incident_id"], first_id)
        self.assertEqual(alert["severity"], "HIGH")
        self.assertEqual(alert["escalated_from"], "MEDIUM")
        self.assertGreaterEqual(len(alert["affected_files"]), 5)

    def test_repeated_edits_to_one_file_do_not_alert(self):
        # Documented blind spot: the rule counts DISTINCT files.
        for i in range(10):
            self._change(0, 1, f"repeat-{i}")
        self.assertEqual(self.edr.summary()["alerts_total"], 0)

    def test_invalid_medium_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            MiniEDR(self.base, medium_threshold=1)
        with self.assertRaises(ValueError):
            MiniEDR(self.base, threshold=5, medium_threshold=6)


if __name__ == "__main__":
    unittest.main()
