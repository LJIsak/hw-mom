from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from theme_manager import theme

class Card(QFrame):
    def __init__(self, parent=None, widget_type=None, transparent=False, color_scheme='A', accent_scheme='A'):
        super().__init__(parent)
        self.setObjectName("card")
        self.transparent = transparent
        self.color_scheme = color_scheme
        self.accent_scheme = accent_scheme
        
        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.layout)
        
        # Add widget if specified
        if widget_type:
            self.widget = widget_type(self, accent_scheme=accent_scheme)
            self.layout.addWidget(self.widget)
        
        # Set up the card's appearance
        self._update_style()
        
        if not transparent:
            # Add shadow effect only for non-transparent cards
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(20) # 15
            shadow.setXOffset(0)
            shadow.setYOffset(2)
            shadow.setColor(QColor(0, 0, 0, 30)) # 30
            self.setGraphicsEffect(shadow)
    
    def _update_style(self):
        """Update the card's style based on current theme"""
        if self.transparent:
            bg_color = "transparent"
        else:
            # Use different background color based on scheme
            color_key = "card_background_2" if self.color_scheme == 'B' else "card_background"
            bg_color = theme.get_color(color_key).name()
        
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {bg_color};
                border-radius: 12px;
                margin: 8px;
            }}
            
            QPushButton#removeButton {{
                background-color: {theme.get_color("card_remove_button").name()};
                border-radius: 12px;
                color: white;
                font-size: 14px;
                font-weight: normal;
                border: none;
                min-width: 24px;
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
                margin: 0px;
                padding: 0px;
                padding-bottom: 0px;
            }}
            
            QPushButton#removeButton:hover {{
                background-color: {theme.get_color("card_remove_button_hover").name()};
            }}
            
            QPushButton#removeButton:pressed {{
                background-color: {theme.get_color("card_remove_button_pressed").name()};
            }}
        """)
    
    def add_remove_button(self, callback):
        """Add a remove button to the card"""
        remove_btn = QPushButton("✖")
        remove_btn.setObjectName("removeButton")
        remove_btn.clicked.connect(callback)
        
        # Position the button absolutely within the card
        remove_btn.setParent(self)
        remove_btn.move(self.width() - 32, 8)
        
        # Make sure button stays on top and repositions on card resize
        remove_btn.raise_()
        self.resizeEvent = lambda e: remove_btn.move(self.width() - 32, 8)
        
        # Hide by default
        remove_btn.hide()
        
        # Store reference to the button
        self.remove_btn = remove_btn 