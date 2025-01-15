from PySide6.QtWidgets import QVBoxLayout
from .base_widget import BaseWidget
import pyqtgraph as pg

class GraphWidget(BaseWidget):
    def __init__(self, title, metrics_collector, parent=None):
        super().__init__(title, metrics_collector, parent)
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#313131')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setYRange(0, 100)
        
        # Create line for the plot
        self.curve = self.plot_widget.plot(pen=pg.mkPen(color='#4a9eff', width=2))
        
        self.layout.addWidget(self.plot_widget)
        
        # Set size for the widget
        self.setMinimumSize(400, 200)
        
        # Style the widget
        self.setStyleSheet("""
            GraphWidget {
                background-color: #313131;
                border-radius: 10px;
                margin: 5px;
            }
        """)
    
    def update_data(self):
        self.metrics_collector.update()
        self.curve.setData(self.metrics_collector.cpu_history) 