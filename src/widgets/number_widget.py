from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from .base_widget import BaseWidget

class NumberWidget(BaseWidget):
    def __init__(self, title, metrics_collector, parent=None):
        super().__init__(title, metrics_collector, parent)
        
        # Create value label
        self.value_label = QLabel("0%")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.value_label)
        
        # Set fixed size for the widget
        self.setMinimumSize(150, 100)
        
        # Style the widget
        self.setStyleSheet("""
            NumberWidget {
                background-color: #313131;
                border-radius: 10px;
                margin: 5px;
            }
        """)
    
    def update_data(self):
        cpu_usage = self.metrics_collector.get_cpu_usage()
        self.value_label.setText(f"{cpu_usage:.1f}%") 