import psutil
import subprocess
from typing import Dict, List, Optional, Tuple
from ping3 import ping

class SystemMetrics:
    """
    Collects metrics and stores them in the internal state. Metrics are only collected if the
    corresponding collector is enabled (off by default and only enabled once widgets are added).
    This system comes with multiple benefits:
    - Prevents multiple calls to the same collector if we e.g. have multiple GPU widgets.
    - Allows us to use a single class for all widgets of the same type (graph/circle/etc.)
    - Stores only a single history for each metric, as opposed to one for each widget.
    """
    def __init__(self):
        self.collect_cpu_enabled = False
        self.collect_gpu_enabled = False
        self.collect_memory_enabled = False
        self.collect_ping_enabled = False
        self.collect_fan_enabled = False

        self.update_interval = 500  # milliseconds
        self.history_size = int(60 / (self.update_interval / 1000))  # 60 seconds of history
        
        # Initialize histories with default values
        self.cpu_history = [0]
        self.gpu_history = [0]
        self.gpu_temp_history = [0]
        self.gpu_memory_history = [0]
        self.system_memory_history = [0]
        self.ping_history = [0]
        self.fan_history = [0]

        # Max values (used to calculate relative usage for circle and graph widgets):
        self.max_system_memory = None
        self.max_cpu_usage = 100 # CPU usage is always percentage based
        self.max_gpu_usage = 100 # GPU usage is always percentage based
        self.max_gpu_memory = None
        self.max_gpu_temp = 100 # Always 100 celcius as max
        self.max_ping = 999 # always 999 ms as max
        self.max_fan_speed = 5000  # Most PC fans max out around 3000-5000 RPM

        # Initialize max values and collect initial metrics
        self.update_max_values()
        self.update()
    
    def update(self):
        """Updates the metrics."""
        if self.collect_cpu_enabled:
            self.collect_cpu_metrics()
        if self.collect_gpu_enabled:
            self.collect_gpu_metrics()
        if self.collect_memory_enabled:
            self.collect_memory_metrics()
        if self.collect_ping_enabled:
            self.collect_ping()
        if self.collect_fan_enabled:
            self.collect_fan_metrics()

    def get_metric_from_string(self, string: str):
        """Returns a metric based on a string."""
        if not string:
            return 0
        
        # CPU
        if string == "cpu_usage":
            self.collect_cpu_enabled = True
            return self.cpu_history[-1] if self.cpu_history else 0
        elif string == "cpu_history":
            self.collect_cpu_enabled = True
            return self.cpu_history
        
        # Memory
        elif string == "memory_usage":
            self.collect_memory_enabled = True
            return self.system_memory_history[-1] if self.system_memory_history else 0
        elif string == "memory_history":
            self.collect_memory_enabled = True
            return self.system_memory_history
        
        # GPU
        elif string == "gpu_temp":
            self.collect_gpu_enabled = True
            return self.gpu_temp_history[-1] if self.gpu_temp_history else 0
        elif string == "gpu_temp_history":
            self.collect_gpu_enabled = True
            return self.gpu_temp_history
        elif string == "gpu_usage":
            self.collect_gpu_enabled = True
            return self.gpu_history[-1] if self.gpu_history else 0
        elif string == "gpu_usage_history":
            self.collect_gpu_enabled = True
            return self.gpu_history
        elif string == "gpu_memory":
            self.collect_gpu_enabled = True
            return self.gpu_memory_history[-1] if self.gpu_memory_history else 0
        elif string == "gpu_memory_history":
            self.collect_gpu_enabled = True
            return self.gpu_memory_history
        
        # Ping
        elif string == "ping":
            self.collect_ping_enabled = True
            return self.ping_history[-1] if self.ping_history else 0
        elif string == "ping_history":
            self.collect_ping_enabled = True
            return self.ping_history
        
        # Fan speed
        elif string == "fan_speed":
            self.collect_fan_enabled = True
            return self.fan_history[-1] if self.fan_history else 0
        elif string == "fan_speed_history":
            self.collect_fan_enabled = True
            return self.fan_history
            
        return 0

    def update_max_values(self):
        """Updates the max values for each metric."""
        # System memory (in GB)
        self.max_system_memory = psutil.virtual_memory().total / (1024**3)
        
        # GPU metrics
        try:
            result = subprocess.run(
                ['nvidia-smi', 
                 '--query-gpu=memory.total', 
                 '--format=csv,noheader,nounits'], 
                capture_output=True, text=True, check=True
            )
            gpu_memory_total = float(result.stdout.strip())
            self.max_gpu_memory = gpu_memory_total / 1024  # Convert to GB
            
        except (subprocess.SubprocessError, ValueError, OSError):
            # If no GPU is found or there's an error, set defaults
            self.max_gpu_memory = 0
            self.max_gpu_usage = 100

    def collect_gpu_metrics(self):
        """Get GPU temperature, memory and utilization using nvidia-smi."""
        try:
            result = subprocess.run(
                ['nvidia-smi', 
                 '--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total', 
                 '--format=csv,noheader,nounits'], 
                capture_output=True, text=True, check=True
            )
            temp, util, mem_used, mem_total = map(float, result.stdout.strip().split(','))
            
            # Update histories
            self.gpu_temp_history.append(temp)
            self.gpu_history.append(util)
            self.gpu_memory_history.append(mem_used / 1024)  # Convert to GB
            
            # Keep only last 60 seconds worth of data
            if len(self.gpu_temp_history) > self.history_size:
                self.gpu_temp_history = self.gpu_temp_history[-self.history_size:]
                self.gpu_history = self.gpu_history[-self.history_size:]
                self.gpu_memory_history = self.gpu_memory_history[-self.history_size:]
                
        except (subprocess.SubprocessError, ValueError, OSError):
            # In case of error, append None or 0
            self.gpu_temp_history.append(0)
            self.gpu_history.append(0)
            self.gpu_memory_history.append(0)
    
    def collect_memory_metrics(self):
        """Get memory usage in GB"""
        mem = psutil.virtual_memory()
        memory_used = mem.used / (1024**3)  # Convert to GB
        
        # Update history
        self.system_memory_history.append(memory_used)
        
        # Keep only last 60 seconds worth of data
        if len(self.system_memory_history) > self.history_size:
            self.system_memory_history = self.system_memory_history[-int(self.history_size):]
    
    def collect_cpu_metrics(self):
        """Get current CPU usage percentage (average of all cores)"""
        # Get per-CPU utilization
        per_cpu = psutil.cpu_percent(percpu=True)
        
        # Calculate average
        avg_usage = sum(per_cpu) / len(per_cpu)
        
        # Update history
        self.cpu_history.append(avg_usage)
        
        # Keep only last 60 seconds worth of data
        if len(self.cpu_history) > self.history_size:
            self.cpu_history = self.cpu_history[-int(self.history_size):]
    
    def collect_ping(self):
        """Get ping time to Google DNS in milliseconds"""
        try:
            response_time = ping('8.8.8.8', timeout=2)
            if response_time is not None:
                # Convert to milliseconds and round to 1 decimal place
                ms = round(response_time * 1000, 1)
                self.ping_history.append(ms)
            else:
                self.ping_history.append(0)
        except Exception:
            self.ping_history.append(0)
            
        # Keep only last 60 seconds worth of data
        if len(self.ping_history) > self.history_size:
            self.ping_history = self.ping_history[-self.history_size:]
    
    def collect_fan_metrics(self):
        """Get fan speeds using psutil."""
        try:
            # Get all fans information
            fans = psutil.sensors_fans()
            
            if fans:
                # Calculate average RPM of all fans
                total_rpm = 0
                fan_count = 0
                
                for fan_name, entries in fans.items():
                    for entry in entries:
                        if entry.current > 0:  # Only count active fans
                            total_rpm += entry.current
                            fan_count += 1
                
                # Calculate average RPM
                avg_rpm = total_rpm / max(fan_count, 1)
                
                # Update history
                self.fan_history.append(avg_rpm)
            else:
                self.fan_history.append(0)
                
        except (AttributeError, IOError, OSError):
            # In case of error, append 0
            self.fan_history.append(0)
        
        # Keep only last 60 seconds worth of data
        if len(self.fan_history) > self.history_size:
            self.fan_history = self.fan_history[-self.history_size:]
    