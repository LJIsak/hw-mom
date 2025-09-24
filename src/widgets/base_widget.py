from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from typing import Optional
from theme_manager import theme

class BaseWidget(QWidget):
    """
    Base class for all widgets. Widgets should read and plot data from the global SystemMetrics 
    instance that always runs in the background. This instance contains all the metrics data, such
    as cpu_history, ping_history, etc.
    
    Widgets should be created by specifying a string that determines which metric to read. For 
    example, if the string is "gpu_memory_history", the widget will access data by calling
    SystemMetrics.get_metric_from_string("gpu_memory_history"). That way we can use the same 
    widget classes for different metrics.

    If the widget requires plotting a relative value (such as the circle or graph widget), the 
    widget should use the corresponding max value from SystemMetrics (e.g. max_gpu_memory for 
    GPU memory widgets).

    Args:
        metric_str (str): The metric string identifier (e.g. "cpu_usage", "gpu_memory_history")
        system_metrics: The global SystemMetrics instance
        parent (Optional[QWidget]): Parent widget
    """
    def __init__(self, metric_str: str, system_metrics, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.metric_str = metric_str
        self.system_metrics = system_metrics
        self.color_scheme = 'A'  # Default color scheme
        
        # Enable the appropriate collector based on the metric string
        if 'cpu' in metric_str:
            self.system_metrics.collect_cpu_enabled = True
        elif 'gpu' in metric_str:
            self.system_metrics.collect_gpu_enabled = True
        elif 'memory' in metric_str:
            self.system_metrics.collect_memory_enabled = True
        elif 'fan_speed' in metric_str:
            self.system_metrics.collect_fan_enabled = True
        elif 'ping' in metric_str:
            self.system_metrics.collect_ping_enabled = True

        # Setup layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.setLayout(self.layout)

    def get_max_value(self) -> float:
        """Returns the max value based on the metric string. Use to calculate relative values."""
        if 'cpu' in self.metric_str:
            return self.system_metrics.max_cpu_usage
        elif 'gpu_memory' in self.metric_str:
            return self.system_metrics.max_gpu_memory
        elif 'gpu_temp' in self.metric_str:
            return self.system_metrics.max_gpu_temp
        elif 'gpu' in self.metric_str:
            return self.system_metrics.max_gpu_usage
        elif 'memory' in self.metric_str:
            return self.system_metrics.max_system_memory
        elif 'fan_speed' in self.metric_str:
            return self.system_metrics.max_fan_speed
        elif 'ping' in self.metric_str:
            return self.system_metrics.max_ping
        return 100.0  # Default max value

    def get_history(self):
        """Gets the full history for this widget's metric."""
        return self.system_metrics.get_metric_from_string(self.metric_str)

    def get_average_value(self):
        """
        Gets the average of the last 4 values from the history. 
        Used for the circle and text widgets.
        """
        history = self.get_history()
        if len(history) >= 4:
            return sum(history[-4:]) / 4
        return history[-1] if history else 0

    def set_color_scheme(self, scheme: str):
        """Set the color scheme for this widget."""
        self.color_scheme = scheme
        self.update()  # Trigger a repaint

    def get_chart_color(self) -> QColor:
        """Get the appropriate chart color based on color scheme."""
        if self.color_scheme == 'B':
            return theme.get_color("color_accent_2")
        elif self.color_scheme == 'C':
            return theme.get_color("color_accent_3")
        return theme.get_color("color_accent_1")  # Default to chart color for scheme A 