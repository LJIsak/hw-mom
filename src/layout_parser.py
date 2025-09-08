import re
from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class WidgetConfig:
    widget_type: str
    metric: str
    start_x: int
    end_x: int
    start_y: int
    end_y: int
    color_scheme: str = 'A'
    fontsize: Optional[int] = None

class LayoutParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.widgets: List[WidgetConfig] = []
        self.theme_str = 'light'  # Default
        self.grid_size_cols = 6
        self.grid_size_rows = 5
        self.parse_file(filepath)

    @property
    def n_rows(self):
        return self.grid_size_rows

    @property
    def n_cols(self):
        return self.grid_size_cols

    def parse_file(self, filepath: str):
        """Parse a layout file and store the layout information."""
        with open(filepath) as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('theme:'):
                self.theme_str = line.split('theme:')[1].strip()
            elif line.startswith('size:'):
                size_str = line.split('size:')[1].strip()
                self.grid_size_cols, self.grid_size_rows = map(int, size_str.split('x'))
            else:
                try:
                    self._parse_widget_line(line)
                except Exception as e:
                    print(f"Error parsing widget line: '{line}'. Error: {e}")
    
    def _parse_widget_line(self, line: str):
        """Parse a single widget definition line."""
        properties = {}
        parts = [p.strip() for p in line.split(',')]
        for part in parts:
            key, value = part.split('=', 1)
            properties[key.strip()] = value.strip()
        
        widget = WidgetConfig(
            widget_type=properties['widget'],
            metric=properties['metric'],
            start_x=int(properties['start_x']),
            end_x=int(properties['end_x']),
            start_y=int(properties['start_y']),
            end_y=int(properties['end_y']),
            color_scheme=properties.get('color_scheme', 'A').upper(),
            fontsize=int(properties['fontsize']) if 'fontsize' in properties else None
        )
        self.widgets.append(widget)
