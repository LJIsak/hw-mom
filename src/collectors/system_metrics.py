import psutil
import subprocess
from typing import Dict, List, Optional, Tuple

class SystemMetrics:
    def __init__(self):
        """Initialize the system metrics collector"""
        self.cpu_history = []
        self.history_size = 60  # 60 seconds of history
    
    def get_gpu_metrics(self) -> Optional[Tuple[float, float]]:
        """Get GPU temperature and utilization using nvidia-smi"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=temperature.gpu,utilization.gpu', 
                 '--format=csv,noheader,nounits'], 
                capture_output=True, text=True, check=True
            )
            temp, util = map(float, result.stdout.strip().split(','))
            return (temp, util)
        except (subprocess.SubprocessError, ValueError, OSError):
            return None
    
    def get_gpu_temp(self) -> Optional[float]:
        """Get GPU temperature"""
        metrics = self.get_gpu_metrics()
        return metrics[0] if metrics else None
    
    def get_gpu_usage(self) -> Optional[float]:
        """Get GPU utilization percentage"""
        metrics = self.get_gpu_metrics()
        return metrics[1] if metrics else None
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage in GB"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total / (1024**3),  # Convert to GB
            'used': mem.used / (1024**3),
            'available': mem.available / (1024**3),
            'percent': mem.percent
        }
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage (average of all cores)"""
        # Get per-CPU utilization with 0 interval (non-blocking)
        per_cpu = psutil.cpu_percent(percpu=True)
        
        # Calculate average
        avg_usage = sum(per_cpu) / len(per_cpu)
        
        # Store in history
        self.cpu_history.append(avg_usage)
        
        # Keep only last 60 seconds
        if len(self.cpu_history) > self.history_size:
            self.cpu_history = self.cpu_history[-self.history_size:]
        
        return avg_usage
    
    def get_cpu_history(self) -> list:
        """Get CPU usage history"""
        return self.cpu_history 
    
    def get_gpu_memory(self) -> Optional[float]:
        """Get GPU memory usage percentage"""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=memory.used,memory.total', 
                 '--format=csv,noheader,nounits'], 
                capture_output=True, text=True, check=True
            )
            used, total = map(float, result.stdout.strip().split(','))
            return (used / total) * 100
        except (subprocess.SubprocessError, ValueError, OSError):
            return None 