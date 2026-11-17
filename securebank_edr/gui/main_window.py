"""SecureBank EDR — local training-lab security operations interface."""

from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPolygonF
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from securebank_edr.core import MiniEDR


APP_STYLE = """
QMainWindow, QWidget {
    background-color: #080f0c;
    color: #e5f2e9;
    font-family: 'DejaVu Sans';
    font-size: 12px;
}
QFrame#Sidebar {
    background-color: #0b1510;
    border-right: 1px solid #1b3a2a;
}
QFrame#Topbar {
    background-color: #0c1711;
    border-bottom: 1px solid #1b3a2a;
}
QFrame#Panel, QFrame#Metric {
    background-color: #101d15;
    border: 1px solid #244a34;
    border-radius: 9px;
}
QLabel#Brand { color: #f3fff6; font-size: 18px; font-weight: bold; }
QLabel#Eyebrow { color: #83a891; font-size: 10px; font-weight: bold; }
QLabel#MetricValue { color: #55e08b; font-size: 27px; font-weight: bold; }
QLabel#PanelTitle { color: #e1f4e7; font-size: 13px; font-weight: bold; }
QLabel#Muted { color: #91a99a; }
QLabel#PageTitle { color: #f3fff6; font-size: 24px; font-weight: bold; }
QPushButton {
    background-color: #14251a;
    color: #cce5d3;
    border: 1px solid #2a5038;
    border-radius: 6px;
    padding: 9px 11px;
    text-align: left;
}
QPushButton:hover { background-color: #1b3525; border-color: #42a968; }
QPushButton#ActiveNav {
    background-color: #173c27;
    color: #ffffff;
    border: 1px solid #39b96b;
    font-weight: bold;
}
QPushButton#Primary {
    background-color: #17683a;
    color: #ffffff;
    border: 1px solid #35b96a;
    font-weight: bold;
}
QPushButton#Primary:hover { background-color: #20864a; }
QPushButton#Danger {
    background-color: #382019;
    color: #ffc0a8;
    border: 1px solid #8b4935;
}
QPushButton:disabled { color: #617568; background-color: #101a13; border-color: #1b3022; }
QComboBox {
    background: #122219; color: #dff2e5; border: 1px solid #2a5038;
    border-radius: 5px; padding: 7px;
}
QComboBox QAbstractItemView { background: #122219; color: #dff2e5; selection-background-color: #205c36; }
QTableWidget {
    background-color: #0d1911;
    alternate-background-color: #112017;
    color: #d9eee0;
    border: 1px solid #1c3928;
    gridline-color: #1d3828;
    selection-background-color: #205b37;
    selection-color: #ffffff;
}
QHeaderView::section {
    background-color: #17291d;
    color: #92b59e;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #2a5038;
    font-weight: bold;
}
QTableWidget::item { padding: 6px; }
"""


class MetricCard(QFrame):
    def __init__(self, title, value, accent="#55e08b"):
        super().__init__()
        self.setObjectName("Metric")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
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


class ActivityGlobe(QWidget):
    """Cinematic, illustrative rotating globe for the isolated local training lab."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.phase = 0.0
        self.sweep_phase = 0.0
        self.setMinimumHeight(205)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.advance)
        self.timer.start(45)

    def advance(self):
        self.phase = (self.phase + 1.15) % 360
        self.sweep_phase = (self.sweep_phase + 2.4) % 360
        self.update()

    def _continent(self, painter, points, fill, outline):
        polygon = QPolygonF([QPointF(x, y) for x, y in points])
        painter.setBrush(QBrush(QColor(fill)))
        painter.setPen(QPen(QColor(outline), 1.1))
        painter.drawPolygon(polygon)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor("#0d1911"))

        cx = rect.width() * 0.50
        cy = rect.height() * 0.53
        radius = min(rect.width() * 0.235, rect.height() * 0.405)

        # Atmospheric halo and outer orbital rings.
        halo = QColor("#36d879")
        for i, alpha in ((0, 18), (7, 10), (15, 5)):
            halo_color = QColor(halo)
            halo_color.setAlpha(alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(halo_color))
            painter.drawEllipse(QRectF(cx-radius-i, cy-radius-i, 2*(radius+i), 2*(radius+i)))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor("#347e50"), 1.0))
        painter.drawEllipse(QRectF(cx-radius-9, cy-radius-9, 2*(radius+9), 2*(radius+9)))
        painter.setPen(QPen(QColor("#1c5132"), 1.0))
        painter.drawArc(QRectF(cx-radius-17, cy-radius-17, 2*(radius+17), 2*(radius+17)), 205*16, 130*16)

        globe = QRectF(cx-radius, cy-radius, radius*2, radius*2)
        painter.setPen(QPen(QColor("#286844"), 1.2))
        painter.setBrush(QBrush(QColor("#092316")))
        painter.drawEllipse(globe)

        # All map detail is clipped to the globe. The simplified land shapes are illustrative.
        painter.save()
        clip = painter.clipPath()
        from PySide6.QtGui import QPainterPath
        globe_path = QPainterPath()
        globe_path.addEllipse(globe)
        painter.setClipPath(globe_path)

        # Subtle latitude and longitude graticule.
        painter.setBrush(Qt.BrushStyle.NoBrush)
        for factor in (0.34, 0.67):
            painter.setPen(QPen(QColor(39, 111, 69, 115), 0.8))
            h = radius * factor
            painter.drawEllipse(QRectF(cx-radius, cy-h, radius*2, h*2))
        for factor in (0.28, 0.56, 0.82):
            painter.setPen(QPen(QColor(39, 111, 69, 100), 0.8))
            w = radius * factor
            painter.drawEllipse(QRectF(cx-w, cy-radius, w*2, radius*2))
        painter.setPen(QPen(QColor(43, 123, 76, 115), 0.8))
        painter.drawLine(int(cx-radius), int(cy), int(cx+radius), int(cy))

        # A slowly shifting equirectangular silhouette gives the globe a clear world-map read.
        painter.save()
        rotation = self.phase * 3.14159265 / 180.0
        squeeze = 0.58 + 0.42 * abs(__import__("math").cos(rotation))
        drift = __import__("math").sin(rotation) * radius * 0.62
        painter.translate(cx + drift, cy)
        painter.scale(squeeze, 1.0)
        painter.translate(-cx, -cy)
        base_x, base_y = cx-radius*0.93, cy-radius*0.69
        sx, sy = radius*1.86, radius*1.38
        def pts(values):
            return [(base_x + x*sx, base_y + y*sy) for x, y in values]
        land = QColor("#1a7542")
        edge = QColor("#56d889")
        # North America
        self._continent(painter, pts([(0.08,0.13),(0.15,0.08),(0.23,0.10),(0.29,0.18),(0.27,0.25),(0.23,0.29),(0.21,0.38),(0.16,0.42),(0.13,0.34),(0.10,0.29),(0.07,0.22)]), "#17643a", "#45bd75")
        # South America
        self._continent(painter, pts([(0.25,0.43),(0.31,0.45),(0.34,0.53),(0.32,0.63),(0.29,0.75),(0.25,0.91),(0.22,0.82),(0.23,0.70),(0.20,0.59)]), "#17643a", "#45bd75")
        # Europe and Asia
        self._continent(painter, pts([(0.43,0.18),(0.49,0.13),(0.57,0.15),(0.62,0.12),(0.70,0.15),(0.78,0.18),(0.87,0.24),(0.91,0.31),(0.85,0.36),(0.77,0.34),(0.72,0.40),(0.66,0.37),(0.61,0.42),(0.56,0.35),(0.50,0.34),(0.46,0.29)]), "#17643a", "#45bd75")
        # Africa
        self._continent(painter, pts([(0.48,0.39),(0.57,0.39),(0.62,0.47),(0.59,0.59),(0.55,0.72),(0.50,0.67),(0.47,0.55),(0.44,0.46)]), "#17643a", "#45bd75")
        # India / south-east Asia
        self._continent(painter, pts([(0.65,0.40),(0.70,0.42),(0.73,0.50),(0.70,0.55),(0.67,0.49)]), "#17643a", "#45bd75")
        # Australia
        self._continent(painter, pts([(0.79,0.69),(0.87,0.67),(0.91,0.72),(0.88,0.79),(0.82,0.81),(0.78,0.76)]), "#17643a", "#45bd75")
        painter.restore()

        # Rotating luminous scan sweep and a few restrained data points.
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.sweep_phase)
        sweep_pen = QPen(QColor(95, 255, 157, 150), 2.0)
        painter.setPen(sweep_pen)
        painter.drawArc(QRectF(-radius+5, -radius+5, 2*(radius-5), 2*(radius-5)), -18*16, 58*16)
        painter.setPen(Qt.PenStyle.NoPen)
        for angle, distance in ((18,0.67),(92,0.82),(155,0.52),(246,0.73)):
            painter.save()
            painter.rotate(angle)
            glow = QColor(105, 255, 165, 100)
            painter.setBrush(QBrush(glow))
            painter.drawEllipse(QRectF(distance*radius-4, -4, 8, 8))
            painter.setBrush(QBrush(QColor("#a0ffc1")))
            painter.drawEllipse(QRectF(distance*radius-1.5, -1.5, 3, 3))
            painter.restore()
        painter.restore()
        painter.restore()

        # Small HUD annotations keep the visual grounded in the local lab.
        painter.setPen(QColor("#83e8a8"))
        painter.drawText(12, 19, "LOCAL TRAINING LAB  /  SIMULATED VISUAL")
        painter.setPen(QColor("#779684"))
        painter.drawText(12, rect.height()-10, "ILLUSTRATIVE GLOBE  •  NO LIVE GLOBAL TELEMETRY")
        painter.setPen(QPen(QColor("#2b6540"), 1))
        painter.drawLine(12, 29, 150, 29)


class MainWindow(QMainWindow):
    NAV_ITEMS = [
        ("⌂   Command Centre", "Command Centre"),
        ("◉   File Monitoring", "File Monitoring"),
        ("⚑   Security Alerts", "Security Alerts"),
        ("⌕   Investigations", "Investigations"),
        ("⬡   Incident Response", "Incident Response"),
        ("▤   Intelligence Reports", "Intelligence Reports"),
    ]

    def __init__(self):
        super().__init__()
        workspace = Path(__file__).resolve().parents[2]
        self.edr = MiniEDR(workspace)
        self._current_incident_id = None
        self._nav_buttons = []

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
        content_layout.setSpacing(13)
        content_layout.addWidget(self.build_topbar())
        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(self.build_command_centre())
        self.page_stack.addWidget(self.build_file_monitoring())
        self.page_stack.addWidget(self.build_security_alerts())
        self.page_stack.addWidget(self.build_investigations())
        self.page_stack.addWidget(self.build_incident_response())
        self.page_stack.addWidget(self.build_reports())
        content_layout.addWidget(self.page_stack, 1)
        main_layout.addWidget(content, 1)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_dashboard)
        self.refresh_timer.start(1500)
        self.refresh_dashboard()

    def panel(self, title=None, note=None):
        frame = QFrame()
        frame.setObjectName("Panel")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 13, 14, 13)
        layout.setSpacing(9)
        if title:
            heading = QLabel(title.upper())
            heading.setObjectName("PanelTitle")
            layout.addWidget(heading)
        if note:
            description = QLabel(note)
            description.setObjectName("Muted")
            description.setWordWrap(True)
            layout.addWidget(description)
        return frame, layout

    def page_heading(self, title, subtitle):
        area = QWidget()
        layout = QVBoxLayout(area)
        layout.setContentsMargins(0, 5, 0, 2)
        layout.setSpacing(4)
        heading = QLabel(title)
        heading.setObjectName("PageTitle")
        note = QLabel(subtitle)
        note.setObjectName("Eyebrow")
        layout.addWidget(heading)
        layout.addWidget(note)
        return area

    def make_table(self, headers, stretch=True):
        table = QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch if stretch else QHeaderView.ResizeMode.ResizeToContents
        )
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(False)
        return table

    def set_table(self, table, rows):
        table.setRowCount(len(rows))
        for row_index, values in enumerate(rows):
            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value if value is not None else "—"))
                table.setItem(row_index, column, item)

    def build_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(228)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 22, 15, 18)
        layout.setSpacing(9)

        brand = QLabel("◈  SECUREBANK")
        brand.setObjectName("Brand")
        layout.addWidget(brand)
        sub = QLabel("CYBER INTELLIGENCE")
        sub.setObjectName("Eyebrow")
        layout.addWidget(sub)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #244a34;")
        layout.addWidget(line)
        layout.addSpacing(10)

        for index, (label, _) in enumerate(self.NAV_ITEMS):
            button = QPushButton(label)
            button.setObjectName("ActiveNav" if index == 0 else "")
            button.clicked.connect(lambda checked=False, page=index: self.show_page(page))
            self._nav_buttons.append(button)
            layout.addWidget(button)
        layout.addStretch()

        scope = QLabel(
            "OPERATIONAL SCOPE\n\nLOCAL TRAINING LAB\nTXT FILE MONITORING\n\nNO REAL CONTAINMENT"
        )
        scope.setObjectName("Eyebrow")
        scope.setWordWrap(True)
        scope.setStyleSheet(
            "background: #13251a; padding: 12px; border: 1px solid #244a34; border-radius: 6px;"
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
        self.section_label = QLabel("OPERATIONS  /  COMMAND CENTRE")
        self.section_label.setObjectName("Eyebrow")
        self.connection_label = QLabel("●  SYSTEM STANDBY")
        self.connection_label.setStyleSheet("color: #d9b45e;")
        layout.addWidget(self.section_label)
        layout.addStretch()
        layout.addWidget(self.connection_label)
        return bar

    def show_page(self, index):
        if not 0 <= index < self.page_stack.count():
            return
        self.page_stack.setCurrentIndex(index)
        title = self.NAV_ITEMS[index][1].upper()
        self.section_label.setText(f"OPERATIONS  /  {title}")
        for button_index, button in enumerate(self._nav_buttons):
            button.setObjectName("ActiveNav" if button_index == index else "")
            button.style().unpolish(button)
            button.style().polish(button)
        self.refresh_dashboard()

    def build_command_centre(self):
        page = QWidget()
        root = QVBoxLayout(page)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(12)
        root.addWidget(self.page_heading(
            "Cyber Intelligence Command Centre",
            "SECUREBANK SECURITY OPERATIONS  /  LOCAL TRAINING ENVIRONMENT"
        ))

        metrics = QGridLayout()
        metrics.setSpacing(11)
        self.event_card = MetricCard("Total Events", 0)
        self.alert_card = MetricCard("Total Incidents", 0, "#e8bf63")
        self.high_card = MetricCard("New Incidents", 0, "#ff8c72")
        self.file_card = MetricCard("Files Modified", 0, "#62d9a0")
        for column, card in enumerate((self.event_card, self.alert_card, self.high_card, self.file_card)):
            metrics.addWidget(card, 0, column)
        root.addLayout(metrics)

        lower = QGridLayout()
        lower.setSpacing(12)
        activity_panel, activity_layout = self.panel(
            "Local activity visual",
            "A decorative status visual for this isolated training workspace."
        )
        self.activity_globe = ActivityGlobe()
        activity_layout.addWidget(self.activity_globe)
        lower.addWidget(activity_panel, 0, 0)

        events_panel, events_layout = self.panel("Recent file events", "Latest events recorded by the local EDR engine.")
        self.event_table = self.make_table(["TIME (UTC)", "EVENT", "FILE", "EVENT ID"])
        events_layout.addWidget(self.event_table)
        lower.addWidget(events_panel, 1, 0)

        ops_panel, ops_layout = self.panel("Operations control", "Training actions only run while monitoring is active.")
        self.monitor_button = QPushButton("▶   Start Monitoring")
        self.monitor_button.setObjectName("Primary")
        self.monitor_button.clicked.connect(self.toggle_monitoring)
        ops_layout.addWidget(self.monitor_button)
        normal_button = QPushButton("Simulate Normal Activity")
        normal_button.clicked.connect(self.simulate_normal)
        ops_layout.addWidget(normal_button)
        suspicious_button = QPushButton("Simulate Suspicious Activity")
        suspicious_button.setObjectName("Danger")
        suspicious_button.clicked.connect(self.simulate_suspicious)
        ops_layout.addWidget(suspicious_button)
        ops_layout.addSpacing(6)
        queue_title = QLabel("INCIDENT QUEUE")
        queue_title.setObjectName("PanelTitle")
        ops_layout.addWidget(queue_title)
        self.incident_table = self.make_table(["SEVERITY", "STATUS", "INCIDENT"])
        self.incident_table.itemSelectionChanged.connect(self.open_selected_incident)
        ops_layout.addWidget(self.incident_table, 1)
        lower.addWidget(ops_panel, 0, 1, 2, 1)
        lower.setColumnStretch(0, 3)
        lower.setColumnStretch(1, 2)
        lower.setRowStretch(0, 1)
        lower.setRowStretch(1, 2)
        root.addLayout(lower, 1)
        return page

    def build_file_monitoring(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.page_heading(
            "File Monitoring",
            "CREATED, MODIFIED AND DELETED FILE EVENTS WITHIN THE DESIGNATED TRAINING FOLDER"
        ))
        panel, panel_layout = self.panel("File activity ledger", "No files outside the configured training folder are monitored.")
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("Event type"))
        self.file_filter = QComboBox()
        self.file_filter.addItems(["All events", "CREATED", "MODIFIED", "DELETED"])
        self.file_filter.currentTextChanged.connect(self.refresh_dashboard)
        filter_row.addWidget(self.file_filter)
        filter_row.addStretch()
        panel_layout.addLayout(filter_row)
        self.file_table = self.make_table(["TIME (UTC)", "EVENT", "FILE", "SIZE (BYTES)", "SHA-256", "EVENT ID"])
        panel_layout.addWidget(self.file_table)
        layout.addWidget(panel, 1)
        return page

    def build_security_alerts(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.page_heading("Security Alerts", "DETECTION OUTPUT GENERATED BY THE LOCAL TRAINING ENGINE"))
        panel, panel_layout = self.panel("Incident register", "Select an incident and open it in Investigations for supporting evidence.")
        filters = QHBoxLayout()
        self.alert_severity_filter = QComboBox()
        self.alert_severity_filter.addItems(["All severities", "MEDIUM", "HIGH"])
        self.alert_status_filter = QComboBox()
        self.alert_status_filter.addItems(["All statuses", "NEW", "ACKNOWLEDGED", "CONTAINMENT_SIMULATED"])
        self.alert_severity_filter.currentTextChanged.connect(self.refresh_dashboard)
        self.alert_status_filter.currentTextChanged.connect(self.refresh_dashboard)
        filters.addWidget(QLabel("Severity"))
        filters.addWidget(self.alert_severity_filter)
        filters.addSpacing(12)
        filters.addWidget(QLabel("Status"))
        filters.addWidget(self.alert_status_filter)
        filters.addStretch()
        panel_layout.addLayout(filters)
        self.alert_table = self.make_table(["TIME (UTC)", "SEVERITY", "STATUS", "TITLE", "AFFECTED FILES", "INCIDENT ID"])
        self.alert_table.itemDoubleClicked.connect(self.open_alert_from_table)
        panel_layout.addWidget(self.alert_table)
        layout.addWidget(panel, 1)
        return page

    def build_investigations(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.page_heading("Investigations", "INCIDENT CONTEXT AND CHRONOLOGICAL SUPPORTING EVIDENCE"))
        selector_panel, selector_layout = self.panel("Select incident")
        row = QHBoxLayout()
        self.investigation_select = QComboBox()
        self.investigation_select.currentIndexChanged.connect(self.load_investigation)
        row.addWidget(self.investigation_select, 1)
        self.investigation_open_response = QPushButton("Open Incident Response")
        self.investigation_open_response.clicked.connect(lambda: self.show_page(4))
        row.addWidget(self.investigation_open_response)
        selector_layout.addLayout(row)
        layout.addWidget(selector_panel)

        detail_panel, detail_layout = self.panel("Incident details")
        self.investigation_details = QLabel("Choose an incident to inspect its details.")
        self.investigation_details.setWordWrap(True)
        self.investigation_details.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        detail_layout.addWidget(self.investigation_details)
        layout.addWidget(detail_panel)

        evidence_panel, evidence_layout = self.panel("Evidence timeline", "Evidence is limited to the event records linked to the selected incident.")
        self.evidence_table = self.make_table(["TIME (UTC)", "EVENT", "FILE", "SIZE (BYTES)", "SHA-256", "EVENT ID"])
        evidence_layout.addWidget(self.evidence_table)
        layout.addWidget(evidence_panel, 1)
        return page

    def build_incident_response(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.page_heading("Incident Response", "ANALYST ACKNOWLEDGEMENT AND SIMULATED CONTAINMENT ONLY"))
        panel, panel_layout = self.panel("Response workflow", "This educational prototype records response actions. It does not isolate devices, stop processes or block network traffic.")
        row = QHBoxLayout()
        self.response_select = QComboBox()
        self.response_select.currentIndexChanged.connect(self.update_response_status)
        row.addWidget(self.response_select, 1)
        panel_layout.addLayout(row)
        self.response_details = QLabel("Select an incident to view its current status.")
        self.response_details.setWordWrap(True)
        panel_layout.addWidget(self.response_details)
        buttons = QHBoxLayout()
        self.acknowledge_button = QPushButton("Acknowledge Incident")
        self.acknowledge_button.setObjectName("Primary")
        self.acknowledge_button.clicked.connect(self.acknowledge_incident)
        self.containment_button = QPushButton("Record Simulated Containment")
        self.containment_button.setObjectName("Danger")
        self.containment_button.clicked.connect(self.simulate_containment)
        buttons.addWidget(self.acknowledge_button)
        buttons.addWidget(self.containment_button)
        panel_layout.addLayout(buttons)
        self.response_message = QLabel("Response actions are written to the project's local audit trail.")
        self.response_message.setObjectName("Muted")
        self.response_message.setWordWrap(True)
        panel_layout.addWidget(self.response_message)
        layout.addWidget(panel, 0)
        layout.addStretch(1)
        return page

    def build_reports(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.page_heading("Intelligence Reports", "LOCAL REPORT EXPORTS FROM THE TRAINING ENGINE"))
        panel, panel_layout = self.panel("Report generation", "Generate a human-readable report from the EDR event, alert and response records.")
        buttons = QHBoxLayout()
        export_button = QPushButton("Generate Intelligence Report")
        export_button.setObjectName("Primary")
        export_button.clicked.connect(self.generate_report)
        refresh_button = QPushButton("Refresh Report List")
        refresh_button.clicked.connect(self.refresh_report_list)
        open_button = QPushButton("Open Selected Report")
        open_button.clicked.connect(self.open_selected_report)
        buttons.addWidget(export_button)
        buttons.addWidget(refresh_button)
        buttons.addWidget(open_button)
        panel_layout.addLayout(buttons)
        self.report_message = QLabel("Reports are stored in the project's runtime/reports directory.")
        self.report_message.setObjectName("Muted")
        self.report_message.setWordWrap(True)
        panel_layout.addWidget(self.report_message)
        self.report_table = self.make_table(["REPORT FILE", "SIZE (BYTES)", "LAST MODIFIED"])
        self.report_table.itemSelectionChanged.connect(self.update_report_selection)
        panel_layout.addWidget(self.report_table)
        layout.addWidget(panel, 1)
        return page

    def monitoring_is_active(self):
        thread = getattr(self.edr, "_thread", None)
        return bool(thread and thread.is_alive())

    def toggle_monitoring(self):
        if self.monitoring_is_active():
            self.edr.stop()
            self.monitor_button.setText("▶   Start Monitoring")
            self.connection_label.setText("●  SYSTEM STANDBY")
            self.connection_label.setStyleSheet("color: #d9b45e;")
        else:
            self.edr.start()
            self.monitor_button.setText("■   Stop Monitoring")
            self.connection_label.setText("●  MONITORING ACTIVE")
            self.connection_label.setStyleSheet("color: #55e08b;")
        self.refresh_dashboard()

    def simulate_normal(self):
        if not self.monitoring_is_active():
            self.connection_label.setText("●  START MONITORING FIRST")
            self.connection_label.setStyleSheet("color: #d9b45e;")
            return
        self.edr.simulate_normal()
        self.refresh_dashboard()

    def simulate_suspicious(self):
        if not self.monitoring_is_active():
            self.connection_label.setText("●  START MONITORING FIRST")
            self.connection_label.setStyleSheet("color: #d9b45e;")
            return
        self.edr.simulate_suspicious()
        self.refresh_dashboard()

    def current_incident_id(self, combo):
        value = combo.currentData()
        return value if value else None

    def populate_incident_combos(self, incidents):
        current_investigation = self.current_incident_id(self.investigation_select)
        current_response = self.current_incident_id(self.response_select)
        for combo, current in ((self.investigation_select, current_investigation), (self.response_select, current_response)):
            combo.blockSignals(True)
            combo.clear()
            for incident in reversed(incidents):
                incident_id = incident.get("incident_id", "")
                title = incident.get("title", "Security incident")
                severity = incident.get("severity", "UNKNOWN")
                status = incident.get("status", "UNKNOWN")
                combo.addItem(f"{severity}  |  {status}  |  {title}  |  {incident_id}", incident_id)
            if current:
                idx = combo.findData(current)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
            combo.blockSignals(False)

    def refresh_dashboard(self):
        stats = self.edr.summary()
        self.event_card.set_value(stats["events_total"])
        self.alert_card.set_value(stats["alerts_total"])
        self.high_card.set_value(stats["alerts_new"])
        self.file_card.set_value(stats["modified"])

        with self.edr._lock:
            events = list(self.edr.events)
            incidents = list(self.edr.alerts)

        recent_events = list(reversed(events[-15:]))
        self.set_table(self.event_table, [
            (event.get("timestamp_utc", ""), event.get("event_type", ""),
             event.get("file", ""), event.get("event_id", ""))
            for event in recent_events
        ])
        recent_incidents = list(reversed(incidents[-12:]))
        self.set_table(self.incident_table, [
            (item.get("severity", ""), item.get("status", ""), item.get("incident_id", ""))
            for item in recent_incidents
        ])

        selected_file_type = self.file_filter.currentText()
        filtered_events = events if selected_file_type == "All events" else [
            item for item in events if item.get("event_type") == selected_file_type
        ]
        self.set_table(self.file_table, [
            (item.get("timestamp_utc", ""), item.get("event_type", ""), item.get("file", ""),
             item.get("size_bytes", ""), item.get("sha256", ""), item.get("event_id", ""))
            for item in reversed(filtered_events[-300:])
        ])

        severity_filter = self.alert_severity_filter.currentText()
        status_filter = self.alert_status_filter.currentText()
        filtered_alerts = incidents
        if severity_filter != "All severities":
            filtered_alerts = [x for x in filtered_alerts if x.get("severity") == severity_filter]
        if status_filter != "All statuses":
            filtered_alerts = [x for x in filtered_alerts if x.get("status") == status_filter]
        self.set_table(self.alert_table, [
            (item.get("timestamp_utc", ""), item.get("severity", ""), item.get("status", ""),
             item.get("title", ""), len(item.get("affected_files", [])), item.get("incident_id", ""))
            for item in reversed(filtered_alerts)
        ])

        self.populate_incident_combos(incidents)
        self.load_investigation()
        self.update_response_status()
        if hasattr(self, "report_table"):
            self.refresh_report_list()

    def open_selected_incident(self):
        selected = self.incident_table.selectedItems()
        if not selected:
            return
        incident_id = self.incident_table.item(selected[0].row(), 2).text()
        index = self.investigation_select.findData(incident_id)
        if index >= 0:
            self.investigation_select.setCurrentIndex(index)
        self.show_page(3)

    def open_alert_from_table(self, item):
        row = item.row()
        incident_id_item = self.alert_table.item(row, 5)
        if not incident_id_item:
            return
        incident_id = incident_id_item.text()
        index = self.investigation_select.findData(incident_id)
        if index >= 0:
            self.investigation_select.setCurrentIndex(index)
        self.show_page(3)

    def load_investigation(self, *_):
        if not hasattr(self, "investigation_select"):
            return
        incident_id = self.current_incident_id(self.investigation_select)
        self._current_incident_id = incident_id
        if not incident_id:
            self.investigation_details.setText("No incidents are available yet. Run a controlled training simulation while monitoring is active.")
            self.set_table(self.evidence_table, [])
            return
        incident = self.edr.get_incident(incident_id)
        if not incident:
            self.investigation_details.setText("The selected incident could not be found.")
            self.set_table(self.evidence_table, [])
            return
        files = incident.get("affected_files", [])
        details = (
            f"Incident: {incident.get('incident_id', '')}\n"
            f"Title: {incident.get('title', '')}\n"
            f"Severity: {incident.get('severity', '')}     Status: {incident.get('status', '')}\n"
            f"Detection rule: {incident.get('rule', '')}\n"
            f"Reason: {incident.get('rule_reason', '')}\n"
            f"Affected files: {', '.join(files) if files else 'No file list recorded'}"
        )
        self.investigation_details.setText(details)
        try:
            evidence = self.edr.get_incident_evidence(incident_id)
        except (KeyError, ValueError):
            evidence = []
        self.set_table(self.evidence_table, [
            (item.get("timestamp_utc", ""), item.get("event_type", ""), item.get("file", ""),
             item.get("size_bytes", ""), item.get("sha256", ""), item.get("event_id", ""))
            for item in evidence
        ])

    def update_response_status(self, *_):
        if not hasattr(self, "response_select"):
            return
        incident_id = self.current_incident_id(self.response_select)
        incident = self.edr.get_incident(incident_id) if incident_id else None
        if not incident:
            self.response_details.setText("No incident selected. New incidents will appear here automatically.")
            self.acknowledge_button.setEnabled(False)
            self.containment_button.setEnabled(False)
            return
        status = incident.get("status", "NEW")
        self.response_details.setText(
            f"Incident: {incident_id}\nSeverity: {incident.get('severity', 'UNKNOWN')}\nCurrent status: {status}\n\n"
            "Acknowledgement records analyst review. Simulated containment records a training response only."
        )
        self.acknowledge_button.setEnabled(status == "NEW")
        self.containment_button.setEnabled(status == "ACKNOWLEDGED")

    def acknowledge_incident(self):
        incident_id = self.current_incident_id(self.response_select)
        if not incident_id:
            return
        try:
            self.edr.respond(incident_id, "ACKNOWLEDGED")
            self.response_message.setText(f"Acknowledgement recorded for {incident_id}.")
        except (KeyError, ValueError) as exc:
            self.response_message.setText(f"Could not record acknowledgement: {exc}")
        self.refresh_dashboard()

    def simulate_containment(self):
        incident_id = self.current_incident_id(self.response_select)
        if not incident_id:
            return
        try:
            self.edr.respond(incident_id, "CONTAINMENT_SIMULATED")
            self.response_message.setText(f"Simulated containment recorded for {incident_id}. No real system containment was performed.")
        except (KeyError, ValueError) as exc:
            self.response_message.setText(f"Could not record simulated containment: {exc}")
        self.refresh_dashboard()

    def report_directory(self):
        default_directory = Path(__file__).resolve().parents[2] / "runtime" / "reports"
        return Path(getattr(self.edr, "reports_dir", default_directory))

    def refresh_report_list(self):
        if not hasattr(self, "report_table"):
            return
        directory = self.report_directory()
        reports = sorted(directory.glob("*.txt"), key=lambda path: path.stat().st_mtime, reverse=True) if directory.exists() else []
        self._report_paths = reports
        self.set_table(self.report_table, [
            (path.name, path.stat().st_size, path.stat().st_mtime_ns)
            for path in reports
        ])
        for row, path in enumerate(reports):
            from datetime import datetime
            modified = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            self.report_table.item(row, 2).setText(modified)

    def generate_report(self):
        try:
            report_path = Path(self.edr.export_report())
            self.report_message.setText(f"Report generated: {report_path}")
            self.refresh_report_list()
        except (OSError, ValueError, RuntimeError) as exc:
            self.report_message.setText(f"Report generation failed: {exc}")

    def update_report_selection(self):
        if not hasattr(self, "report_table"):
            return
        selected = self.report_table.selectedItems()
        if selected:
            self.report_message.setText(f"Selected report: {selected[0].text()}")

    def open_selected_report(self):
        selected = self.report_table.selectedItems()
        if not selected:
            self.report_message.setText("Select a report from the list first.")
            return
        row = selected[0].row()
        if row >= len(getattr(self, "_report_paths", [])):
            return
        path = self._report_paths[row]
        try:
            with path.open("r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError as exc:
            self.report_message.setText(f"Could not read report: {exc}")
            return
        QMessageBox.information(self, path.name, content[:12000] or "This report is empty.")

    def closeEvent(self, event):
        self.refresh_timer.stop()
        self.activity_globe.timer.stop()
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
