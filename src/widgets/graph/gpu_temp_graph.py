from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.graph_widget import GraphWidget

class GPUTempGraphWidget(GraphWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("GPU Temp", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        self.history = []  # Store GPU temp history
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_graph()
    
    def update_graph(self):
        """Update with new GPU temperature data"""
        temp = self.metrics.get_gpu_temp()
        if temp is not None:
            self.history.append(temp)
            # Keep only last 60 seconds
            if len(self.history) > 60:
                self.history = self.history[-60:]
            self.graph_area.set_values(self.history)
            self.graph_area.update() 