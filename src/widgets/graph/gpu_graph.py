from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.graph_widget import GraphWidget

class GPUGraphWidget(GraphWidget):
    def __init__(self, parent=None):
        super().__init__("GPU Usage", parent)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        self.history = []  # Store GPU history since SystemMetrics doesn't
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_graph()
    
    def update_graph(self):
        """Update with new GPU usage data"""
        usage = self.metrics.get_gpu_usage()
        if usage is not None:
            self.history.append(usage)
            # Keep only last 60 seconds
            if len(self.history) > 60:
                self.history = self.history[-60:]
            self.graph_area.set_values(self.history)
            self.graph_area.update() 