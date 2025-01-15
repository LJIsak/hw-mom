from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, Signal

class BaseWidget(QWidget):
    closed = Signal(object)  # Signal emitted when widget is closed
    
    def __init__(self, title, metrics_collector, parent=None):
        super().__init__(parent)
        self.metrics_collector = metrics_collector
        
        # Setup widget layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)
        
        # Create header with title and close button
        header_layout = QHBoxLayout()
        
        # Add title
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(self.title_label)
        
        # Add close button
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(self.close_widget)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: #888;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #fff;
            }
        """)
        header_layout.addWidget(close_button)
        
        self.layout.addLayout(header_layout)
        
        # Setup update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second
    
    def close_widget(self):
        self.timer.stop()
        self.closed.emit(self)
        self.deleteLater()
    
    def update_data(self):
        """Override this method in child classes to update widget data"""
        pass 