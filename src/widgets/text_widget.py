from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from .base_widget import BaseWidget
from theme_manager import theme
from typing import Optional

class TextValueLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._update_style()
        
        # Set anti-aliased font
        value_font = self.font()
        value_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.setFont(value_font)
        
        # Center alignment
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def _update_style(self):
        """Update the label style with current theme colors"""
        self.setStyleSheet(f"""
            QLabel {{
                color: {theme.get_color("text_big").name()};
                font-size: 48px;
                font-weight: 500;
                padding: 8px;
            }}
        """)
    
    def set_value(self, text):
        self.setText(text)
        self._update_style()

class TextWidget(BaseWidget):
    """
    A widget that displays a metric value as large text.
    
    Args:
        metric_str (str): The metric to display (e.g. "cpu_usage", "memory_usage")
        system_metrics: The global SystemMetrics instance
        title (str): The title shown above the text
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
        
        # Create value label
        self.value_label = TextValueLabel()
        
        # Add widgets to layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.value_label, 1)

        # Setup update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(system_metrics.update_interval)
        
        # Initial update
        self.update_display()

    def update_display(self):
        """Update the displayed text value."""
        current = self.get_current_value()
        
        # Format the display value based on the metric type
        if 'memory' in self.metric_str:
            display_text = f"{current:.1f}GB"
        elif any(x in self.metric_str for x in ['cpu', 'gpu']):
            display_text = f"{current:.0f}%"
        elif 'ping' in self.metric_str:
            display_text = f"{current:.0f}ms"
        elif 'temp' in self.metric_str:
            display_text = f"{current:.0f}°C"
        else:
            display_text = f"{current:.1f}"
            
        self.value_label.set_value(display_text) 