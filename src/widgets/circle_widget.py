from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush
import math
from .base_widget import BaseWidget
from theme_manager import theme
from typing import Optional

class CircularProgressLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create the value label
        self.value_label = QLabel("--")
        self._update_label_style()
        
        # Set anti-aliased font for value
        value_font = self.value_label.font()
        value_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.value_label.setFont(value_font)
        
        # Center the label in this widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Initialize progress value
        self.progress = 0
        
        # Set size policy to expand
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
    
    def _update_label_style(self):
        """Update the label style with current theme colors"""
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {theme.get_color("text_big").name()};
                font-size: 32px;
                font-weight: 500;
            }}
        """)
    
    def set_value(self, text, progress):
        self.value_label.setText(text)
        self.progress = progress
        self._update_label_style()  # Update style when value changes
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate the circle dimensions
        size = min(self.width(), self.height())
        rect = QRectF(
            (self.width() - size) / 2 + 4,
            (self.height() - size) / 2 + 4,
            size - 8,
            size - 8
        )
        
        # Draw background circle
        background_color = theme.get_color("chart_legend")
        background_color.setAlpha(40)
        painter.setPen(QPen(background_color, 4))
        painter.drawArc(rect, 0, 360 * 16)
        
        # Draw progress
        if self.progress > 0:
            # Get accent color from parent CircleWidget
            progress_color = self.parent()._get_accent_color()
            painter.setPen(QPen(progress_color, 4))
            angle = int(self.progress * 360 * 16)
            painter.drawArc(rect, 90 * 16, angle)
            
            # Calculate dot position (adjusted for counter-clockwise)
            progress_angle = (90 + self.progress * 360) * math.pi / 180
            radius = (size - 8) / 2
            center_x = self.width() / 2
            center_y = self.height() / 2
            
            dot_x = center_x + radius * math.cos(progress_angle)
            dot_y = center_y - radius * math.sin(progress_angle)
            
            # Draw dot
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(progress_color))  # Use same accent color for dot
            dot_size = 12
            painter.drawEllipse(
                QPointF(dot_x, dot_y),
                dot_size/2,
                dot_size/2
            )

class CircleWidget(BaseWidget):
    """
    A circular widget that shows a progress indicator and value.
    Displays the current value of a metric as both a number and a circular progress bar.
    
    Args:
        metric_str (str): The metric to display (e.g. "cpu_usage", "memory_usage")
        system_metrics: The global SystemMetrics instance
        title (str): The title shown above the circle
        parent (Optional[QWidget]): Parent widget
        accent_scheme (str): Color scheme to use ('A', 'B', or 'C')
    """
    def __init__(self, 
                 metric_str: str,
                 system_metrics,
                 title: str,
                 parent: Optional[QWidget] = None,
                 accent_scheme: str = 'A'):
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
        
        # Create circular progress with value
        self.circular_progress = CircularProgressLabel(self)
        
        # Add widgets to main layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.circular_progress, 1)

        # Setup update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(system_metrics.update_interval)
        
        # Initial update
        self.update_display()
    
    def update_display(self):
        """Update the displayed value and progress."""
        # Get history data by replacing '_usage' with '_history' in get_metric_from_string():
        history_metric = self.metric_str.replace('_usage', '_history')
        history = self.system_metrics.get_metric_from_string(history_metric)
        
        # Calculate a single 'current' value based on the size of history:
        if isinstance(history, (int, float)):
            current = history
        elif len(history) >= 8:
            current = sum(history[-8:]) / 8
        else:
            current = history[-1] if history else 0
        
        max_val = self.get_max_value()
        
        # Calculate relative value (0-1)
        relative = current / max_val if max_val > 0 else 0
        
        # Format the display value based on the metric type
        if 'memory' in self.metric_str:
            display_text = f"{current:.1f}GB"
        elif 'temp' in self.metric_str:
            display_text = f"{current:.0f}°C"
        elif any(x in self.metric_str for x in ['cpu', 'gpu']):
            display_text = f"{current:.0f}%"
        elif 'ping' in self.metric_str:
            display_text = f"{current:.0f}ms"
        else:
            display_text = f"{current:.1f}"
        
        self.circular_progress.set_value(display_text, relative)
    
    def _get_accent_color(self):
        """Get the appropriate accent color based on scheme"""
        if self.accent_scheme == 'B':
            color_key = "chart_2"
        elif self.accent_scheme == 'C':
            color_key = "chart_3"
        else:
            color_key = "chart"
        return theme.get_color(color_key) 