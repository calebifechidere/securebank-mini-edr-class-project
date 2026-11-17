
"""SecureBank Cyber Intelligence — desktop command centre."""

from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel,
    QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView
)

from securebank_edr.core import MiniEDR


APP_STYLE = """
QMainWindow, QWidget {
    background-color: #0b0e17;
    color: #e6eaf2;
    font-family: 'DejaVu Sans';
    font-size: 12px;
}
QFrame#Sidebar {
    background-color: #101522;
    border-right: 1px solid #27334a;
}
QFrame#Topbar {
    background-color: #101522;
    border-bottom: 1px solid #27334a;
}
QFrame#Panel, QFrame#Metric {
    background-color: #141b2a;
    border: 1px solid #293750;
    border-radius: 9px;
}
QLabel#Brand {
    color: #ffffff;
    font-size: 17px;
    font-weight: bold;
}
QLabel#Eyebrow {
    color: #8192ad;
    font-size: 10px;
    font-weight: bold;
}
QLabel#MetricValue {
    color: #ffffff;
    font-size: 27px;
    font-weight: bold;
}
QLabel#PanelTitle {
    color: #dce6f5;
    font-size: 13px;
    font-weight: bold;
}
QLabel#Muted {
    color: #8290a8;
}
QPushButton {
    background-color: #18243a;
    color: #cbd8ec;
    border: 1px solid #304767;
    border-radius: 5px;
    padding: 9px 12px;
    text-align: left;
}
QPushButton:hover {
    background-color: #203451;
    border-color: #4d83c9;
}
QPushButton#ActiveNav {
    background-color: #18345a;
    color: #ffffff;
    border: 1px solid #3478c8;
    font-weight: bold;
}
QPushButton#Primary {
    background-color: #1765b5;
    color: white;
    border: 1px solid #3989dc;
    font-weight: bold;
}
QPushButton#Primary:hover {
    background-color: #247bd1;
}
QPushButton#Danger {
    background-color: #3a2029;
    color: #ffb5bd;
    border: 1px solid #713b49;
}
QTableWidget {
    background-color: #111827;
    alternate-background-color: #151e2e;
    color: #dce6f5;
    border: none;
    gridline-color: #26334a;
    selection-background-color: #24466d;
}
QHeaderView::section {
    background-color: #192337;
    color: #8fa4c2;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #30405a;
    font-weight: bold;
}
QTableWidget::item {
    padding: 6px;
}
"""


class MetricCard(QFrame):
    def __init__(self, title, value, accent="#55a7ff"):
        super().__init__()
        self.setObjectName("Metric")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 13, 16, 13)
        layout.setSpacing(7)

        label = QLabel(title.upper())
        label.setObjectName("Eyebrow")

        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("MetricValue")
        self.value_label.setStyleSheet(f"color: {accent};")

        layout.addWidget(label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        self.value_label.setText(str(value))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        workspace = Path(__file__).resolve().parents[2]
        self.edr = MiniEDR(workspace)

        self.setWindowTitle("SecureBank | Cyber Intelligence")
        self.resize(1440, 900)
        self.setMinimumSize(1050, 700)
        self.setStyleSheet(APP_STYLE)

        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.build_sidebar(), 0)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(22, 0, 22, 18)
        content_layout.setSpacing(16)

        content_layout.addWidget(self.build_topbar())
        content_layout.addWidget(self.build_heading())
        content_layout.addLayout(self.build_metrics())
        content_layout.addLayout(self.build_work_area(), 1)

        main_layout.addWidget(content, 1)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_dashboard)
        self.refresh_timer.start(1500)

        self.refresh_dashboard()

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 22, 15, 18)
        layout.setSpacing(10)

        brand = QLabel("◈  SECUREBANK")
        brand.setObjectName("Brand")
        layout.addWidget(brand)

        sub = QLabel("CYBER INTELLIGENCE")
        sub.setObjectName("Eyebrow")
        layout.addWidget(sub)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #293750;")
        layout.addWidget(line)
        layout.addSpacing(14)

        nav_items = [
            "⌂   Command Center",
            "◉   File Monitoring",
            "⚑   Security Alerts",
            "⌕   Investigations",
            "⬡   Incident Response",
            "▤   Intelligence Reports",
        ]

        for index, item in enumerate(nav_items):
            button = QPushButton(item)
            if index == 0:
                button.setObjectName("ActiveNav")
            layout.addWidget(button)

        layout.addStretch()

        scope = QLabel(
            "OPERATIONAL SCOPE\n\n"
            "LOCAL TRAINING LAB\n"
            "TXT FILE MONITORING\n\n"
            "NO REAL CONTAINMENT"
        )
        scope.setObjectName("Eyebrow")
        scope.setWordWrap(True)
        scope.setStyleSheet(
            "background: #151e2e; padding: 12px; "
            "border: 1px solid #293750; border-radius: 6px;"
        )
        layout.addWidget(scope)

        version = QLabel("SECUREBANK EDR  |  v1.0")
        version.setObjectName("Muted")
        layout.addWidget(version)

        return sidebar

    def build_topbar(self):
        bar = QFrame()
        bar.setObjectName("Topbar")
        bar.setFixedHeight(55)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 0)

        section = QLabel("OPERATIONS  /  COMMAND CENTER")
        section.setObjectName("Eyebrow")

        self.connection_label = QLabel("●  SYSTEM STANDBY")
        self.connection_label.setStyleSheet("color: #e3b45d;")

        layout.addWidget(section)
        layout.addStretch()
        layout.addWidget(self.connection_label)

        return bar

    def build_heading(self):
        area = QWidget()
        layout = QVBoxLayout(area)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(5)

        title = QLabel("Cyber Intelligence Command Center")
        title.setStyleSheet("font-size: 23px; font-weight: bold; color: white;")

        subtitle = QLabel(
            "SECUREBANK SECURITY OPERATIONS  /  TRAINING ENVIRONMENT"
        )
        subtitle.setObjectName("Eyebrow")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return area

    def build_metrics(self):
        layout = QGridLayout()
        layout.setSpacing(12)

        self.event_card = MetricCard("Total Events", 0)
        self.alert_card = MetricCard("Total Incidents", 0, "#f0b75b")
        self.high_card = MetricCard("New Incidents", 0, "#f16c76")
        self.file_card = MetricCard("Files Modified", 0, "#63c8b0")

        cards = [
            self.event_card, self.alert_card,
            self.high_card, self.file_card
        ]

        for column, card in enumerate(cards):
            layout.addWidget(card, 0, column)

        return layout

    def build_work_area(self):
        layout = QGridLayout()
        layout.setSpacing(14)

        activity = QFrame()
        activity.setObjectName("Panel")
        activity_layout = QVBoxLayout(activity)
        activity_layout.setContentsMargins(15, 15, 15, 15)

        activity_title = QLabel("FILE ACTIVITY  /  EVENT TIMELINE")
        activity_title.setObjectName("PanelTitle")
        activity_layout.addWidget(activity_title)

        activity_note = QLabel(
            "Recent events recorded inside the designated training folder."
        )
        activity_note.setObjectName("Muted")
        activity_layout.addWidget(activity_note)

        self.event_table = QTableWidget(0, 4)
        self.event_table.setHorizontalHeaderLabels(
            ["TIME (UTC)", "EVENT", "FILE", "EVENT ID"]
        )
        self.event_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.event_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.event_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.event_table.setAlternatingRowColors(True)
        activity_layout.addWidget(self.event_table)

        operations = QFrame()
        operations.setObjectName("Panel")
        operations.setFixedWidth(290)

        operations_layout = QVBoxLayout(operations)
        operations_layout.setContentsMargins(15, 15, 15, 15)
        operations_layout.setSpacing(12)

        ops_title = QLabel("OPERATIONS CONTROL")
        ops_title.setObjectName("PanelTitle")
        operations_layout.addWidget(ops_title)

        ops_note = QLabel("Monitoring and controlled training actions")
        ops_note.setObjectName("Muted")
        ops_note.setWordWrap(True)
        operations_layout.addWidget(ops_note)

        self.monitor_button = QPushButton("▶   Start Monitoring")
        self.monitor_button.setObjectName("Primary")
        self.monitor_button.clicked.connect(self.toggle_monitoring)
        operations_layout.addWidget(self.monitor_button)

        normal_button = QPushButton("Simulate Normal Activity")
        normal_button.clicked.connect(self.simulate_normal)
        operations_layout.addWidget(normal_button)

        suspicious_button = QPushButton("Simulate Suspicious Activity")
        suspicious_button.setObjectName("Danger")
        suspicious_button.clicked.connect(self.simulate_suspicious)
        operations_layout.addWidget(suspicious_button)

        operations_layout.addSpacing(10)

        incident_title = QLabel("INCIDENT QUEUE")
        incident_title.setObjectName("PanelTitle")
        operations_layout.addWidget(incident_title)

        self.incident_table = QTableWidget(0, 3)
        self.incident_table.setHorizontalHeaderLabels(
            ["SEVERITY", "STATUS", "INCIDENT"]
        )
        self.incident_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.incident_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.incident_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        operations_layout.addWidget(self.incident_table, 1)

        layout.addWidget(activity, 0, 0)
        layout.addWidget(operations, 0, 1)

        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 1)

        return layout

    def toggle_monitoring(self):
        if self.edr._thread and self.edr._thread.is_alive():
            self.edr.stop()
            self.monitor_button.setText("▶   Start Monitoring")
            self.connection_label.setText("●  SYSTEM STANDBY")
            self.connection_label.setStyleSheet("color: #e3b45d;")
        else:
            self.edr.start()
            self.monitor_button.setText("■   Stop Monitoring")
            self.connection_label.setText("●  MONITORING ACTIVE")
            self.connection_label.setStyleSheet("color: #63c8b0;")

        self.refresh_dashboard()

    def simulate_normal(self):
        if not (self.edr._thread and self.edr._thread.is_alive()):
            self.connection_label.setText("●  START MONITORING FIRST")
            self.connection_label.setStyleSheet("color: #e3b45d;")
            return

        self.edr.simulate_normal()
        self.refresh_dashboard()

    def simulate_suspicious(self):
        if not (self.edr._thread and self.edr._thread.is_alive()):
            self.connection_label.setText("●  START MONITORING FIRST")
            self.connection_label.setStyleSheet("color: #e3b45d;")
            return

        self.edr.simulate_suspicious()
        self.refresh_dashboard()

    def refresh_dashboard(self):
        stats = self.edr.summary()

        self.event_card.set_value(stats["events_total"])
        self.alert_card.set_value(stats["alerts_total"])
        self.high_card.set_value(stats["alerts_new"])
        self.file_card.set_value(stats["modified"])

        with self.edr._lock:
            events = list(self.edr.events[-15:])
            incidents = list(self.edr.alerts[-12:])

        self.event_table.setRowCount(len(events))

        for row, event in enumerate(reversed(events)):
            values = [
                event["timestamp_utc"],
                event["event_type"],
                event["file"],
                event["event_id"],
            ]
            for column, value in enumerate(values):
                self.event_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

        self.incident_table.setRowCount(len(incidents))

        for row, incident in enumerate(reversed(incidents)):
            values = [
                incident["severity"],
                incident["status"],
                incident["incident_id"],
            ]
            for column, value in enumerate(values):
                self.incident_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

    def closeEvent(self, event):
        self.refresh_timer.stop()
        self.edr.stop()
        event.accept()


def main():
    app = QApplication([])
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()



