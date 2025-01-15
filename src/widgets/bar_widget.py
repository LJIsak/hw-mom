from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import Qt
from .base_widget import BaseWidget

class BarWidget(BaseWidget):
    def __init__(self, title, metrics_collector, parent=None):
        super().__init__(title, metrics_collector, parent)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1f1f1f;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a9eff;
                border-radius: 3px;
            }
        """)
        
        self.layout.addWidget(self.progress_bar)
        
        # Set fixed size for the widget
        self.setMinimumSize(200, 100)
        
        # Style the widget
        self.setStyleSheet("""
            BarWidget {
                background-color: #313131;
                border-radius: 10px;
                margin: 5px;
            }
            QProgressBar {
                border: 2px solid #1f1f1f;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4a9eff;
                border-radius: 3px;
            }
        """)
    
    def update_data(self):
        ram_usage = self.metrics_collector.get_ram_usage()
        self.progress_bar.setValue(int(ram_usage['percent'])) 