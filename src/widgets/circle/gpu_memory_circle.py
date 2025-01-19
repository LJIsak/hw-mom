from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.circle_widget import CircleWidget

class GPUMemoryWidget(CircleWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("GPU Memory", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(500)  # Update every 500ms
        
        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed GPU memory usage"""
        memory_percent = self.metrics.get_gpu_memory()
        if memory_percent is not None:
            # For now, just show the percentage since we don't have GB values
            self.circular_progress.set_value(
                f"{int(memory_percent)}%",
                memory_percent / 100.0  # Convert percentage to fraction
            )
        else:
            self.circular_progress.set_value("N/A", 0) 