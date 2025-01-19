from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.text_widget import TextWidget

class PingTextWidget(TextWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("Ping", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed ping time"""
        ping_time = self.metrics.get_ping()
        if ping_time is not None:
            self.value_label.set_value(f"{ping_time}ms")
        else:
            self.value_label.set_value("N/A") 