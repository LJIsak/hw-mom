from typing import List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class WidgetConfig:
    widget_type: str
    metric: str
    fromRow: int # Can be passed directly to QGridLayout::addWidget
    fromCol: int # Can be passed directly to QGridLayout::addWidget
    rowSpan: int # Can be passed directly to QGridLayout::addWidget
    colSpan: int # Can be passed directly to QGridLayout::addWidget
    color_scheme: str
    is_separator: bool = False

class LayoutParser:
    """
    Parse a layout file and store the layout information in class attributes.

    Example usage:
        parser = LayoutParser('settings/default_layout.txt')
        widgets = parser.widgets

    The parser.widgets above will yield a list of WidgetConfig objects that look something like:
        [WidgetConfig(widget_type='circle', metric='cpu', fromRow=0, fromCol=0, rowSpan=1, colSpan=1, color_scheme='a', is_separator=False),
        WidgetConfig(widget_type='circle', metric='gpu_temp', fromRow=0, fromCol=1, rowSpan=1, colSpan=1, color_scheme='b', is_separator=False),
        WidgetConfig(widget_type='circle', metric='gpu_memory', fromRow=0, fromCol=2, rowSpan=2, colSpan=1, color_scheme='c', is_separator=False),
        WidgetConfig(widget_type='', metric='separator', fromRow=1, fromCol=0, rowSpan=1, colSpan=2, color_scheme='A', is_separator=True)]
    """
    def __init__(self, filepath: str):
        self.widgets = [] # list of WidgetConfig objects
        self.layout_str = ''
        self.theme_str = ''
        self.row_strings = []
        self.n_rows = 0
        self.n_cols = 0
        self.filepath = filepath
        self.parse_file(filepath)
        self.parse_widgets()

    def parse_file(self, filepath: str):
        """Parse a layout file and store the layout information in class attributes."""
        # Read file contents
        with open(filepath) as f:
            self.layout_str = f.read()

        # Split into rows and handle theme
        if 'theme:' in self.layout_str:
            self.theme_str = self.layout_str.split('theme:')[1].strip().split('\n')[0]
            self.row_strings = self.layout_str.split('\n')[1:]
        else:
            self.theme_str = 'light'
            self.row_strings = self.layout_str.split('\n')

        # Calculate grid dimensions
        self.n_rows = len(self.row_strings)
        
        # Find maximum columns by summing widget widths in each row
        for row_str in self.row_strings:
            n_cols_in_row = 0
            for substring in row_str.split('x')[1:]:
                n_cols_in_row += int(substring[0])
            self.n_cols = max(self.n_cols, n_cols_in_row)
        
    def parse_widgets(self):
        """Parse widget configurations from the row strings and store them in self.widgets."""
        # Iterate over all rows:
        for r, row_str in enumerate(self.row_strings):
            widget_strings = [s.strip('[') for s in row_str.split(']')[:-1]]

            # Iterate over all widgets in the row:
            from_col = 0
            for widget_str in widget_strings:
                # Remove trailing whitespace from widget_str. Continue if string is empty:
                widget_str = widget_str.rstrip()
                if widget_str == '':
                    continue

                color = 'A' if 'color' not in widget_str else widget_str.split('color')[-1][-1]
                temp_widget = WidgetConfig(
                    widget_type=widget_str.split(' ')[0],
                    metric='separator' if 'separator' in widget_str else widget_str.split(' ')[1],
                    fromRow=r,
                    fromCol=from_col,
                    rowSpan=int(widget_str.split('x')[0][-1]),
                    colSpan=int(widget_str.split('x')[1][0]),
                    color_scheme=color,
                    is_separator='separator' in widget_str
                )
                self.widgets.append(temp_widget)

                # Update from_col to the end of the current widget:
                from_col += temp_widget.colSpan
