from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.text_widget import TextWidget

class CPUTextWidget(TextWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("CPU", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(500)  # Update every 500ms
        
        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed CPU usage"""
        usage = self.metrics.get_cpu_usage()
        self.value_label.set_value(f"{int(usage)}%") 