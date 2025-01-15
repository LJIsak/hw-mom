from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.circle_widget import CircleWidget

class CPUWidget(CircleWidget):
    def __init__(self, parent=None):
        super().__init__("CPU Usage", parent)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed CPU usage"""
        usage = self.metrics.get_cpu_usage()
        self.circular_progress.set_value(
            f"{usage:.1f}%",
            usage / 100.0  # Convert percentage to fraction
        ) 