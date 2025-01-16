from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.circle_widget import CircleWidget

class GPUWidget(CircleWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("GPU", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed GPU usage"""
        usage = self.metrics.get_gpu_usage()
        if usage is not None:
            self.circular_progress.set_value(
                f"{usage:.1f}%",
                usage / 100.0
            )
        else:
            self.circular_progress.set_value("N/A", 0) 