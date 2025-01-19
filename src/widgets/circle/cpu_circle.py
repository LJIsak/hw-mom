from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.circle_widget import CircleWidget

class CPUWidget(CircleWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("CPU", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(500) # Use 1000 to update every second
        
        self.measurements = []  # Store recent measurements
        self.measurement_interval = 0.5  # Assuming 0.5s update interval
        self.averaging_window = 8  # Number of measurements to average (4 seconds / 0.5s = 8)

        # Initial update
        self.update_value()
    
    def update_value(self):
        """Update the displayed CPU usage"""
        usage = self.metrics.get_cpu_usage()
        # Add new measurement to history
        self.measurements.append(usage)
        
        # Keep only the measurements we need for our window
        if len(self.measurements) > self.averaging_window:
            self.measurements.pop(0)
        
        # Calculate average of recent measurements
        avg_usage = sum(self.measurements) / len(self.measurements)
        
        self.circular_progress.set_value(
            f"{int(avg_usage)}%",
            avg_usage / 100.0  # Convert percentage to fraction
        ) 