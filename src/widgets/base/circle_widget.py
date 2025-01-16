from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QSizePolicy
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush
import math
from .base_widget import BaseWidget
from theme_manager import theme

class CircularProgressLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create the value label
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet(f"""
            QLabel {{
                color: {theme.get_color("text_big").name()};
                font-size: 32px;
                font-weight: 500;
            }}
        """)
        
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
    
    def set_value(self, text, progress):
        self.value_label.setText(text)
        self.progress = progress
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
        painter.setPen(QPen(theme.get_color("chart_empty"), 4))
        painter.drawArc(rect, 0, 360 * 16)
        
        # Draw progress
        if self.progress > 0:
            progress_color = QColor(theme.get_color("chart"))
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
            painter.setBrush(QBrush(progress_color))
            dot_size = 12
            painter.drawEllipse(
                QPointF(dot_x, dot_y),
                dot_size/2,
                dot_size/2
            )

class CircleWidget(BaseWidget):
    def __init__(self, title: str, parent=None, accent_scheme='A'):
        super().__init__(parent)
        self.accent_scheme = accent_scheme
        
        # Create header label
        self.header = QLabel(title)
        self.header.setStyleSheet("""
            QLabel {
                color: #660d0b17;
                font-size: 12px;
                font-weight: 400;
            }
        """)
        self.header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Set anti-aliased font for header
        header_font = self.header.font()
        header_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.header.setFont(header_font)
        
        # Create circular progress with value
        self.circular_progress = CircularProgressLabel()
        
        # Add widgets to main layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.circular_progress, 1) 
    
    def _get_accent_color(self):
        """Get the appropriate accent color based on scheme"""
        color_key = "chart_2" if self.accent_scheme == 'B' else "chart"
        return theme.get_color(color_key) 