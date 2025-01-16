from PyQt6.QtCore import QTimer
from collectors.system_metrics import SystemMetrics
from ..base.graph_widget import GraphWidget

class CPUGraphWidget(GraphWidget):
    def __init__(self, parent=None, accent_scheme='A'):
        super().__init__("CPU", parent, accent_scheme=accent_scheme)
        
        # Initialize metrics collector
        self.metrics = SystemMetrics()
        
        # Set up update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Update every second
        
        # Initial update
        self.update_graph()
    
    def update_graph(self):
        """Update with new CPU usage data"""
        usage = self.metrics.get_cpu_usage()  # This also updates the history
        history = self.metrics.get_cpu_history()
        self.graph_area.set_values(history)
        self.graph_area.update() 