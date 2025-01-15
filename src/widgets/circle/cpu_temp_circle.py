from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.circle_widget import CircleWidget

class CPUTempWidget(CircleWidget):
    def __init__(self, parent=None):
        super().__init__("CPU Temp", parent)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed CPU temperature"""
        temp = self.metrics.get_cpu_temp()
        if temp is not None:
            self.circular_progress.set_value(
                f"{int(temp)}°C",
                min(temp / 100.0, 1.0)  # Clamp to max 100%
            )
        else:
            self.circular_progress.set_value("N/A", 0) 