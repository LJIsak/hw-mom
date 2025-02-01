from PyQt6.QtWidgets import QSizePolicy
from .base_card import Card, RemoveButton

class SeparatorCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set minimum size and size policy
        self.setMinimumSize(16, 16)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Make transparent
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        
        # Add remove button (will be hidden by default)
        self.remove_btn = RemoveButton(self)
        self.remove_btn.hide() 