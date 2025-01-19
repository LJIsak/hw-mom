from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .base_widget import BaseWidget
from theme_manager import theme

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
    def __init__(self, title: str, parent=None, accent_scheme='A'):
        super().__init__(parent)
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