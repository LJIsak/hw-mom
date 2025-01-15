from PySide6.QtWidgets import (QToolBar, QComboBox, QPushButton, 
                              QWidget, QHBoxLayout)
from PySide6.QtCore import Signal

class WidgetToolbar(QWidget):
    add_widget = Signal(str)  # Signal emitted when a new widget should be added
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)
        
        # Create widget type selector
        self.widget_selector = QComboBox()
        self.widget_selector.addItems([
            "Number Widget",
            "Bar Widget",
            "Circle Widget",
            "Graph Widget"
        ])
        layout.addWidget(self.widget_selector)
        
        # Create add button
        add_button = QPushButton("Add Widget")
        add_button.clicked.connect(self.on_add_clicked)
        layout.addWidget(add_button)
        
        # Add stretch to push everything to the left
        layout.addStretch()
        
        # Style
        self.setStyleSheet("""
            QComboBox {
                background-color: #1f1f1f;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QPushButton {
                background-color: #4a9eff;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #3a8eef;
            }
            QWidget {
                background-color: #1f1f1f;
            }
        """)
    
    def on_add_clicked(self):
        widget_type = self.widget_selector.currentText()
        self.add_widget.emit(widget_type) 