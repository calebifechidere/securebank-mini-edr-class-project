import unittest

from securebank_edr.incident_analysis import (
    analyze_incident,
    sort_events
)


class TestIncidentAnalysis(unittest.TestCase):

    def setUp(self):
        self.incident = {
            "title": "Unusual burst of file changes",
            "severity": "HIGH",
            "rule_reason": "Five files changed within 10 seconds."
        }

        self.events = [
            {
                "event_id": "EVT002",
                "timestamp_utc": "2026-11-17T10:02:00Z",
                "event_type": "MODIFIED",
                "file": "account.txt"
            },
            {
                "event_id": "EVT001",
                "timestamp_utc": "2026-11-17T10:01:00Z",
                "event_type": "CREATED",
                "file": "customer.txt"
            }
        ]

    def test_events_are_sorted(self):
        result = sort_events(self.events)

        self.assertEqual(
            result[0]["event_id"],
            "EVT001"
        )

    def test_correct_event_count(self):
        result = analyze_incident(
            self.incident,
            self.events
        )

        self.assertEqual(result["event_count"], 2)

    def test_correct_affected_file_count(self):
        result = analyze_incident(
            self.incident,
            self.events
        )

        self.assertEqual(len(result["affected_files"]), 2)

    def test_severity_is_preserved(self):
        result = analyze_incident(
            self.incident,
            self.events
        )

        self.assertEqual(result["severity"], "HIGH")

    def test_uncertainty_is_included(self):
        result = analyze_incident(
            self.incident,
            self.events
        )

        self.assertIn("uncertainty", result)

    def test_recommendations_are_included(self):
        result = analyze_incident(
            self.incident,
            self.events
        )

        self.assertGreater(
            len(result["recommendations"]),
            0
        )

    def test_empty_evidence(self):
        result = analyze_incident(
            self.incident,
            []
        )

        self.assertEqual(result["event_count"], 0)


if __name__ == "__main__":
    unittest.main()
