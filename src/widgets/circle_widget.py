from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from .base_widget import BaseWidget
import math

class CircleWidget(BaseWidget):
    def __init__(self, title, metrics_collector, parent=None):
        super().__init__(title, metrics_collector, parent)
        
        # Create value label
        self.value_label = QLabel("0%")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(self.value_label)
        
        self.percentage = 0
        self.setMinimumSize(150, 150)
        
        # Style the widget
        self.setStyleSheet("""
            CircleWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                margin: 5px;
            }
        """)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Calculate circle parameters
        center = self.rect().center()
        radius = min(self.width(), self.height()) * 0.35
        
        # Draw background circle
        painter.setPen(QPen(QColor("#3d3d3d"), 10))
        painter.drawEllipse(center, radius, radius)
        
        # Draw progress arc
        painter.setPen(QPen(QColor("#4a9eff"), 10))
        span_angle = -self.percentage * 360 / 100 * 16  # Qt uses 16th of a degree
        painter.drawArc(center.x() - radius, center.y() - radius,
                       radius * 2, radius * 2,
                       90 * 16, span_angle)
    
    def update_data(self):
        cpu_usage = self.metrics_collector.get_cpu_usage()
        self.percentage = cpu_usage
        self.value_label.setText(f"{cpu_usage:.1f}%")
        self.update() 