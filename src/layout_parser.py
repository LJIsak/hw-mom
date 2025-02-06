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
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.widgets = [] # list of WidgetConfig objects
        self.layout_str = ''
        self.theme_str = ''
        self.row_strings = []
        self.n_rows = 0
        self.n_cols = 0
        self.occupancy_matrix = []
        self.parse_file(filepath)
        self.parse_widgets()

    def parse_file(self, filepath: str):
        """Parse a layout file and store the layout information in class attributes."""
        # Read file contents
        with open(filepath) as f:
            self.layout_str = f.read()

        # Remove trailing linebreaks from layout_str:
        self.layout_str = self.layout_str.rstrip()

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
        self.n_cols = 1
        for row_str in self.row_strings:
            n_cols_in_row = 0
            for substring in row_str.split('x')[1:]:
                # Catch errors where the 'x' is not adjacent to numbers (e.g. for text widgets).
                try:
                    n_cols_in_row += int(substring[0])
                except:
                    continue
            self.n_cols = max(self.n_cols, n_cols_in_row)
        
        # Create occupancy matrix to keep track of widget positions more easily
        self.occupancy_matrix = [[0]*self.n_cols for _ in range(self.n_rows)]

    def parse_widgets(self):
        """Parse widget configurations from the row strings and store them in self.widgets."""
        # Iterate over all rows:
        for row_idx, row_str in enumerate(self.row_strings):
            widget_strings = [s.strip('[') for s in row_str.split(']')[:-1]]

            # Iterate over all widgets in the row while tracking columns:
            current_col = 0
            for widget_str in widget_strings:
                widget_str = widget_str.rstrip() # removes trailing whitespaces

                # If widget string is empty, it indicates occupancy from above. If so, 
                # increament the column tracker until an empty space is found or row ends.
                if widget_str == '':
                    while self.occupancy_matrix[row_idx][current_col]:
                        current_col += 1
                        if current_col == self.n_cols:
                            break
                    continue

                color = 'A' if 'color' not in widget_str else widget_str.split('color')[-1][-1]
                widget = WidgetConfig(
                    widget_type=widget_str.split(' ')[0],
                    metric='separator' if 'separator' in widget_str else widget_str.split(' ')[1],
                    fromRow=row_idx,
                    fromCol=current_col,
                    rowSpan=int(widget_str.split('x')[-2][-1]), # first char before last 'x'
                    colSpan=int(widget_str.split('x')[-1][-0]), # first char after last 'x'
                    color_scheme=color,
                    is_separator=True if 'separator' in widget_str else False
                )
                self.widgets.append(widget)

                # Populate occupancy matrix:
                for r in range(widget.fromRow, widget.fromRow + widget.rowSpan):
                    for c in range(widget.fromCol, widget.fromCol + widget.colSpan):
                        self.occupancy_matrix[r][c] = 1

                # Skip ahead colSpan columns when tracking current column:
                current_col += widget.colSpan
