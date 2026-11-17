
import os
import threading
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication
    from securebank_edr.gui import main_window
except ImportError:
    QApplication = None
    main_window = None


class FakeThread:
    def __init__(self):
        self.active = True

    def is_alive(self):
        return self.active


class FakeEDR:
    def __init__(self, workspace):
        self._thread = None
        self._lock = threading.RLock()
        self.events = []
        self.alerts = []
        self.normal_calls = 0
        self.suspicious_calls = 0
        self.stopped = False

    def summary(self):
        return {
            "events_total": len(self.events),
            "alerts_total": len(self.alerts),
            "alerts_new": 0,
            "modified": 0,
        }

    def start(self):
        self._thread = FakeThread()

    def stop(self):
        if self._thread:
            self._thread.active = False
        self.stopped = True

    def simulate_normal(self):
        self.normal_calls += 1

    def simulate_suspicious(self):
        self.suspicious_calls += 1


@unittest.skipIf(
    QApplication is None,
    "PySide6 is not installed"
)
class GUITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.patcher = patch.object(
            main_window, "MiniEDR", FakeEDR
        )
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.window = main_window.MainWindow()
        self.addCleanup(self.window.close)

    def test_window_opens(self):
        self.assertEqual(
            self.window.windowTitle(),
            "SecureBank | Cyber Intelligence"
        )
        self.assertIsNotNone(self.window.centralWidget())

    def test_dashboard_tables_exist(self):
        self.assertIsNotNone(self.window.event_table)
        self.assertIsNotNone(self.window.incident_table)

    def test_monitoring_can_start_and_stop(self):
        self.window.toggle_monitoring()

        self.assertEqual(
            self.window.connection_label.text(),
            "●  MONITORING ACTIVE"
        )

        self.window.toggle_monitoring()

        self.assertEqual(
            self.window.connection_label.text(),
            "●  SYSTEM STANDBY"
        )

    def test_simulation_requires_monitoring(self):
        self.window.simulate_normal()

        self.assertEqual(
            self.window.connection_label.text(),
            "●  START MONITORING FIRST"
        )
        self.assertEqual(
            self.window.edr.normal_calls, 0
        )

    def test_simulations_work_when_monitoring(self):
        self.window.toggle_monitoring()

        self.window.simulate_normal()
        self.window.simulate_suspicious()

        self.assertEqual(
            self.window.edr.normal_calls, 1
        )
        self.assertEqual(
            self.window.edr.suspicious_calls, 1
        )

    def test_closing_window_stops_monitoring(self):
        self.window.toggle_monitoring()

        class FakeCloseEvent:
            accepted = False

            def accept(self):
                self.accepted = True

        event = FakeCloseEvent()
        self.window.closeEvent(event)

        self.assertTrue(event.accepted)
        self.assertTrue(self.window.edr.stopped)


if __name__ == "__main__":
    unittest.main()


