import psutil

class SystemMetricsCollector:
    def __init__(self):
        self.history_size = 60  # 60 seconds of history
        self.cpu_history = []
        self.ram_history = []
    
    def get_cpu_usage(self):
        return psutil.cpu_percent()
    
    def get_ram_usage(self):
        ram = psutil.virtual_memory()
        return {
            'total': ram.total,
            'used': ram.used,
            'percent': ram.percent
        }
    
    def update(self):
        """Update all metrics"""
        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()
        
        self.cpu_history.append(cpu)
        self.ram_history.append(ram['percent'])
        
        # Keep only the last history_size values
        self.cpu_history = self.cpu_history[-self.history_size:]
        self.ram_history = self.ram_history[-self.history_size:] 