from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.graph_widget import GraphWidget

class GPUMemoryGraphWidget(GraphWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("GPU Memory", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Initialize history
        self.history = []  # Store GPU memory history
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_graph()
    
    def update_graph(self):
        """Update with new GPU memory usage data"""
        memory_percent = self.metrics.get_gpu_memory()
        if memory_percent is not None:
            # Add new value to history
            self.history.append(memory_percent)
            
            # Keep only last 60 values (1 minute of history)
            if len(self.history) > 60:
                self.history = self.history[-60:]
            
            # Update graph
            self.graph_area.set_values(self.history)
            self.graph_area.update() 