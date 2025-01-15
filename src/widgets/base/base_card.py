from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter

class Card(QFrame):
    def __init__(self, parent=None, widget_type=None, transparent=False):
        super().__init__(parent)
        self.setObjectName("card")
        
        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.layout)
        
        # Add widget if specified
        if widget_type:
            self.widget = widget_type(self)
            self.layout.addWidget(self.widget)
        
        # Set up the card's appearance
        if transparent:
            self.setStyleSheet("""
                QFrame#card {
                    background-color: transparent;
                    margin: 8px;
                }
                
                QPushButton#removeButton {
                    background-color: #db7240;
                    border-radius: 12px;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    min-width: 24px;
                    max-width: 24px;
                    min-height: 24px;
                    max-height: 24px;
                    margin: 0px;
                    padding: 0px;
                    padding-bottom: 0px;
                }
                
                QPushButton#removeButton:hover {
                    background-color: #c95f2c;
                }
                
                QPushButton#removeButton:pressed {
                    background-color: #db7240;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#card {
                    background-color: #fefefe;
                    border-radius: 12px;
                    margin: 8px;
                }
                
                QPushButton#removeButton {
                    background-color: #db7240;
                    border-radius: 12px;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    min-width: 24px;
                    max-width: 24px;
                    min-height: 24px;
                    max-height: 24px;
                    margin: 0px;
                    padding: 0px;
                    padding-bottom: 0px;
                }
                
                QPushButton#removeButton:hover {
                    background-color: #c95f2c;
                }
                
                QPushButton#removeButton:pressed {
                    background-color: #db7240;
                }
            """)
            
            # Add shadow effect only for non-transparent cards
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(2)
            shadow.setColor(QColor(0, 0, 0, 30))
            self.setGraphicsEffect(shadow)
    
    def add_remove_button(self, callback):
        """Add a remove button to the card"""
        remove_btn = QPushButton("×")
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