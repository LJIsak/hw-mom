from PyQt6.QtWidgets import QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from theme_manager import theme

class SeparatorCard(QFrame):
    """A simple transparent card that acts as a spacer in the grid."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("separator")
        
        # Set size policy to expand in both directions
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Set minimum size to ensure it takes up space
        self.setMinimumSize(32, 32)
        
        # Make it transparent
        self.setStyleSheet("""
            QFrame#separator {
                background: transparent;
                border: none;
            }
        """)
        
        # Add remove button for edit mode
        from .base_card import RemoveButton
        self.remove_btn = RemoveButton(self)
        self.remove_btn.hide()
    
    def _update_style(self):
        # No style update is necessary for the separator.
        pass

    def resizeEvent(self, event):
        """Handle resize to position remove button"""
        super().resizeEvent(event)
        # Position remove button in top-right corner
        if hasattr(self, 'remove_btn'):
            self.remove_btn.move(
                self.width() - self.remove_btn.width() - 8,
                8
            ) 