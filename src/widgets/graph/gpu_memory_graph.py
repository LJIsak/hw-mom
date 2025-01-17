from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.graph_widget import GraphWidget

class GPUMemoryGraphWidget(GraphWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("GPU Memory", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        self.history = []  # Store GPU memory history
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(500)  # Update every half second
        
        # Initial update
        self.update_graph()
    
    def update_graph(self):
        """Update with new GPU memory data"""
        usage = self.metrics.get_gpu_memory()
        if usage is not None:
            self.history.append(usage)
            # Keep only last 60 seconds
            if len(self.history) > 60:
                self.history = self.history[-60:]
            self.graph_area.set_values(self.history)
            self.graph_area.update() 