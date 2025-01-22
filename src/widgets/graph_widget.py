from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import (QPainter, QPen, QColor, QFont, 
                        QLinearGradient, QPainterPath)
from .base_widget import BaseWidget
from theme_manager import theme
from typing import Optional, List

class GraphArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.values = []
        self.max_points = 60  # Keep 60 seconds of history
    
    def set_values(self, values: List[float]):
        """Update the values to plot"""
        self.values = values[-self.max_points:]  # Keep only last 60 values
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get dimensions
        width = self.width()
        height = self.height()
        padding = 8
        label_width = 25  # Width reserved for labels
        label_spacing = 4  # Space between labels and lines
        
        # Setup font for labels
        font = painter.font()
        font.setPointSize(8)
        font.setBold(True)  # Make labels bold
        painter.setFont(font)
        
        # Draw horizontal lines and labels
        line_color = QColor(theme.get_color("chart_legend"))
        line_color.setAlpha(160)
        
        # Draw horizontal lines for percentages (including 0%)
        for percent in [0, 25, 50, 75, 100]:
            y = int(height - (height - 2 * padding) * (percent / 100) - padding)
            
            # Draw line (start after label_width + spacing)
            painter.setPen(QPen(line_color, 1, Qt.PenStyle.SolidLine))
            painter.drawLine(padding + label_width + label_spacing, y, width - padding, y)
            
            # Draw label (same color as lines, no % sign)
            label_rect = QRectF(0, y - 10, label_width + padding, 20)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, str(percent))
        
        # Calculate points (adjusted for label_width + spacing)
        points = []
        x_step = (width - 2 * padding - label_width - label_spacing) / (self.max_points - 1)
        
        for i, value in enumerate(self.values):
            x = int(width - padding - (len(self.values) - 1 - i) * x_step)
            y = int(height - (height - 2 * padding) * (value / 100) - padding)
            points.append((x, y))
        
        if len(points) > 1:
            # Create gradient for fill
            gradient = QLinearGradient(0, 0, 0, height)
            fill_color = self.parent()._get_accent_color()
            fill_color.setAlpha(128)
            gradient.setColorAt(0, fill_color)
            gradient.setColorAt(1, QColor(fill_color.red(), fill_color.green(), fill_color.blue(), 0))
            
            # Create fill path
            path = QPainterPath()
            path.moveTo(points[0][0], height - padding)  # Start at bottom
            for point in points:
                path.lineTo(point[0], point[1])
            path.lineTo(points[-1][0], height - padding)  # Back to bottom
            path.closeSubpath()
            
            # Fill under the curve
            painter.fillPath(path, gradient)
            
            # PLot graph line
            painter.setPen(QPen(self.parent()._get_accent_color(), 2.5, Qt.PenStyle.SolidLine))
            for i in range(len(points) - 1):
                painter.drawLine(
                    points[i][0], points[i][1],
                    points[i+1][0], points[i+1][1]
                )

class GraphWidget(BaseWidget):
    """
    A widget that displays a metric's history as a line graph with gradient fill.
    Shows the last 60 seconds of data with percentage-based Y-axis labels.
    
    Args:
        metric_str (str): The metric history to display (e.g. "cpu_history", "memory_history")
        system_metrics: The global SystemMetrics instance
        title (str): The title shown above the graph
        parent (Optional[QWidget]): Parent widget
        accent_scheme (str): Color scheme to use ('A', 'B', or 'C')
    """
    def __init__(
            self, metric_str: str, system_metrics, title: str, parent: Optional[QWidget] = None,
            accent_scheme: str = 'A'
        ):
        super().__init__(metric_str, system_metrics, parent)
        self.accent_scheme = accent_scheme
        
        # Create header label
        self.header = QLabel(title)
        self.header.setStyleSheet(f"""
            QLabel {{
                color: {theme.get_color("text_small").name()};
                font-size: 12px;
                font-weight: 400;
            }}
        """)
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Set anti-aliased font for header
        header_font = self.header.font()
        header_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.header.setFont(header_font)
        
        # Create graph area
        self.graph_area = GraphArea(self)
        
        # Add widgets to layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.graph_area, 1)

        # Setup update timer with 1 second interval
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)  # Update every 1000ms (1 second)
        
        # Initial update
        self.update_display()

    def update_display(self):
        """Update the graph with latest history values."""
        history = self.get_current_value()  # This will get the history array
        max_val = self.get_max_value()
        
        # Convert values to percentages relative to max value
        if max_val > 0:
            percentage_values = [min(100, (val / max_val) * 100) for val in history]
        else:
            percentage_values = [0] * len(history)
            
        self.graph_area.set_values(percentage_values)
        self.graph_area.update()  # Force repaint
    
    def _get_accent_color(self):
        """Get the appropriate accent color based on scheme"""
        if self.accent_scheme == 'B':
            color_key = "chart_2"
        elif self.accent_scheme == 'C':
            color_key = "chart_3"
        else:
            color_key = "chart"
        return theme.get_color(color_key) 