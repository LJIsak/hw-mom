from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from theme_manager import theme

class RemoveButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("×", parent)  # Using × symbol for remove
        self.setObjectName("removeButton")
        self.setFixedSize(24, 24)
        self._update_style()
        self.hide()  # Hidden by default, shown in edit mode
    
    def _update_style(self):
        """Update button style with current theme colors"""
        base_color = theme.get_color("edit_mode_button")
        hover_color = QColor(
            int(base_color.red() * 0.8),
            int(base_color.green() * 0.8),
            int(base_color.blue() * 0.8)
        )
        pressed_color = QColor(
            int(hover_color.red() * 0.8),
            int(hover_color.green() * 0.8),
            int(hover_color.blue() * 0.8)
        )
        
        self.setStyleSheet(f"""
            QPushButton#removeButton {{
                background-color: {base_color.name()};
                border-radius: 12px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                padding-bottom: 4px;
            }}
            QPushButton#removeButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#removeButton:pressed {{
                background-color: {pressed_color.name()};
            }}
        """)

class Card(QFrame):
    def __init__(self, widget=None, color_scheme='A'):
        super().__init__()
        self.setObjectName("card")
        print(f"Creating card with color scheme: {color_scheme}")  # Debug
        self.color_scheme = color_scheme
        
        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.layout)
        
        # Add widget if specified
        if widget:
            self.widget = widget
            # Pass color scheme to widget
            if hasattr(widget, 'set_color_scheme'):
                widget.set_color_scheme(color_scheme)
            self.layout.addWidget(widget)
        
        # Set up the card's appearance
        self._update_style()
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 16))
        self.setGraphicsEffect(shadow)
        
        # Create remove button
        self.remove_btn = RemoveButton(self)
    
    def _update_style(self):
        """Update the card's style based on current theme"""
        # All cards use the same background color now
        bg_color = theme.get_color("card_background").name()
        
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {bg_color};
                border-radius: 12px;
                margin: 8px;
            }}
        """)
    
    def resizeEvent(self, event):
        """Handle resize to position remove button"""
        super().resizeEvent(event)
        # Position remove button in top-right corner
        self.remove_btn.move(
            self.width() - self.remove_btn.width() - 8,
            8
        ) 