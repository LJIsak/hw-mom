from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PySide6.QtCore import Qt
from widgets.number_widget import NumberWidget
from widgets.bar_widget import BarWidget
from widgets.circle_widget import CircleWidget
from widgets.graph_widget import GraphWidget
from collectors.system_metrics import SystemMetricsCollector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hardware Monitor")
        self.setMinimumSize(800, 600)
        
        # Initialize the metrics collector
        self.metrics_collector = SystemMetricsCollector()
        
        # Setup the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Create a grid layout for widgets
        grid_layout = QGridLayout()
        
        # Add widgets
        cpu_number = NumberWidget("CPU Usage", self.metrics_collector)
        ram_bar = BarWidget("RAM Usage", self.metrics_collector)
        cpu_circle = CircleWidget("CPU Load", self.metrics_collector)
        performance_graph = GraphWidget("Performance", self.metrics_collector)
        
        grid_layout.addWidget(cpu_number, 0, 0)
        grid_layout.addWidget(ram_bar, 0, 1)
        grid_layout.addWidget(cpu_circle, 0, 2)
        grid_layout.addWidget(performance_graph, 1, 0, 1, 3)
        
        layout.addLayout(grid_layout)
        
        # Style the window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)