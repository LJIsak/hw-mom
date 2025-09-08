from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from theme_manager import theme

class PlaceholderCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("placeholderCard")
        self.setAcceptDrops(False)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.add_button = QPushButton("+", self)
        self.add_button.setObjectName("placeholderButton")
        self.add_button.setFixedSize(48, 48)
        
        layout.addWidget(self.add_button)
        
        self._update_style()

    def _update_style(self):
        button_bg_color = theme.get_color("background")
        button_text_color = theme.get_color("text_small")
        
        self.setStyleSheet(f"""
            QFrame#placeholderCard {{
                background: transparent;
                border: none;
                border-radius: 12px;
            }}
            QPushButton#placeholderButton {{
                background-color: {button_bg_color.name()};
                border: none;
                border-radius: 24px;
                color: {button_text_color.name()};
                font-size: 28px;
                font-weight: bold;
            }}
            QPushButton#placeholderButton:hover {{
                background-color: {theme.get_color("card_background").name()};
            }}
        """)
