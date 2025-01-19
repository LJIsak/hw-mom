from PyQt6.QtWidgets import (QMainWindow, QWidget, QGridLayout, QSizePolicy, 
                            QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPalette, QColor
from widgets.base.base_card import Card
from widgets.dialog.card_dialog import AddCardDialog
from widgets.circle.memory_circle import MemoryWidget
from widgets.circle.cpu_circle import CPUWidget
from widgets.circle.gpu_circle import GPUWidget
from widgets.circle.cpu_temp_circle import CPUTempWidget
from widgets.circle.gpu_temp_circle import GPUTempWidget
from widgets.graph.cpu_graph import CPUGraphWidget
from widgets.graph.gpu_graph import GPUGraphWidget
from widgets.base.separator_card import SeparatorCard
from widgets.graph.gpu_temp_graph import GPUTempGraphWidget
from widgets.graph.gpu_memory_graph import GPUMemoryGraphWidget
from theme_manager import theme
from widgets.text.cpu_text import CPUTextWidget
from widgets.text.ping_text import PingTextWidget

class FloatingButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setObjectName("floatingButton")
        self.setFixedSize(40, 40)
        self._update_colors()
    
    def _update_colors(self):
        # Get base color and create hover/pressed colors
        base_color = theme.get_color("add_button")
        hover_color = QColor(
            int(base_color.red() * 0.9),
            int(base_color.green() * 0.9),
            int(base_color.blue() * 0.9)
        )
        pressed_color = QColor(
            int(hover_color.red() * 0.8),
            int(hover_color.green() * 0.8),
            int(hover_color.blue() * 0.8)
        )
        self.setStyleSheet(f"""
            QPushButton#floatingButton {{
                background-color: {base_color.name()};
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding-top: -4px;
            }}
            QPushButton#floatingButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#floatingButton:pressed {{
                background-color: {pressed_color.name()};
            }}
        """)

class EditModeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("-", parent)
        self.setObjectName("editModeButton")
        self.setFixedSize(40, 40)
        self.setCheckable(True)
        self._update_colors()
    
    def _update_colors(self):
        # Get base color and create darker version
        base_color = theme.get_color("edit_mode_button")
        hover_color = QColor(
            int(base_color.red() * 0.9),
            int(base_color.green() * 0.9),
            int(base_color.blue() * 0.9)
        )
        pressed_color = QColor(
            int(hover_color.red() * 1.0),
            int(hover_color.green() * 0.8),
            int(hover_color.blue() * 0.8)
        )
        self.setStyleSheet(f"""
            QPushButton#editModeButton {{
                background-color: {base_color.name()};
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding-top: -4px;
            }}
            QPushButton#editModeButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#editModeButton:pressed, QPushButton#editModeButton:checked {{
                background-color: {pressed_color.name()};
            }}
        """)

class ThemeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("☀", parent)
        self.setObjectName("themeButton")
        self.setFixedSize(28, 28)
        self.setCheckable(True)
        self._update_colors()

    def _update_colors(self):
        # Get base color and create darker version
        text_color = theme.get_color("text_small")
        base_color = theme.get_color("card_background")
        hover_color = QColor(
            int(base_color.red() * 0.9),
            int(base_color.green() * 0.9),
            int(base_color.blue() * 0.9)
        )
        pressed_color = QColor(
            int(hover_color.red() * 0.8),
            int(hover_color.green() * 0.8),
            int(hover_color.blue() * 0.8)
        )
        self.setStyleSheet(f"""
            QPushButton#themeButton {{
                background-color: {base_color.name()};
                border-radius: 14px;
                color: {text_color.name()};
                font-size: 14px;
                font-weight: normal;
                border: none;
                padding-top: -1px;
            }}
            QPushButton#themeButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#themeButton:pressed {{
                background-color: {pressed_color.name()};
            }}
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HW-Mom")
        self.setMinimumSize(640, 480)
        
        # Create main widget and set it as central
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Set the background color
        palette = self.main_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, theme.get_color("background"))
        self.main_widget.setAutoFillBackground(True)
        self.main_widget.setPalette(palette)
        
        # Initialize grid tracking
        self.grid_positions = {}  # {(row, col): card_widget}
        
        # Track cards for edit mode
        self.cards = []
        
        # Initialize UI
        self._init_ui()
        
        # Add floating buttons last so they're on top
        self._add_floating_buttons()
        
        # Initial theme
        self._update_theme()
    
    def _init_ui(self):
        """Initialize the user interface"""
        # Create main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        
        # Create grid layout for cards
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(16)
        
        # Add layouts to main layout
        main_layout.addLayout(self.grid_layout)
        
        # Add initial demo cards
        self._add_demo_cards()
        
        self.main_widget.setLayout(main_layout)
    
    def _add_floating_buttons(self):
        """Add floating action buttons"""
        # Add button
        self.add_button = FloatingButton(self)
        self.add_button.clicked.connect(self._add_card)
        self.add_button.raise_()
        
        # Edit mode button
        self.edit_button = EditModeButton(self)
        self.edit_button.clicked.connect(self._toggle_edit_mode)
        self.edit_button.raise_()
        
        # Theme toggle button
        self.theme_button = ThemeButton(self)
        self.theme_button.clicked.connect(self._toggle_theme)
        self.theme_button.raise_()
        
        self._position_floating_buttons()
    
    def _position_floating_buttons(self):
        """Position the floating buttons"""
        # Get common bottom position for all buttons
        bottom_margin = 32
        bottom_y = self.height() - bottom_margin - self.add_button.height()
        
        # Position add button (bottom right)
        add_button_x = self.width() - self.add_button.width() - 32
        self.add_button.move(add_button_x, bottom_y)
        
        # Position edit button to the left of add button
        self.edit_button.move(add_button_x - self.edit_button.width() - 16, bottom_y)
        
        # Position theme button (bottom left)
        self.theme_button.move(32, bottom_y + self.theme_button.height()//2)
    
    def resizeEvent(self, event):
        """Handle window resize to reposition floating buttons"""
        super().resizeEvent(event)
        if hasattr(self, 'add_button'):
            self._position_floating_buttons()
    
    def _toggle_edit_mode(self):
        """Toggle visibility of remove buttons on all cards"""
        show = self.edit_button.isChecked()
        for card in self.cards:
            if hasattr(card, 'remove_btn'):
                card.remove_btn.setVisible(show)
    
    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.theme_button.isChecked():
            theme.set_theme('dark')
            self.theme_button.setText("☾")  # Moon emoji for dark mode
        else:
            theme.set_theme('light')
            self.theme_button.setText("☀")  # Sun emoji for light mode
        
        self._update_theme()
        
        # Update button colors
        self.add_button._update_colors()
        self.edit_button._update_colors()
    
    def _update_theme(self):
        """Update the application theme"""
        # Update background color
        palette = self.main_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, theme.get_color("background"))
        self.main_widget.setPalette(palette)
        
        # Update all cards
        for card in self.cards:
            card._update_style()
            
        # Update all buttons
        self.add_button._update_colors()
        self.edit_button._update_colors()
        self.theme_button._update_colors()
    
    def _add_demo_cards(self):
        """Add initial demo cards"""
        # Define the initial layout
        demo_layout = [
            # First row: Memory (with accent B), CPU, GPU Temp (1x1 each)
            [(0, 0, 1, 1, MemoryWidget, False, 'A', 'A'),
             (0, 1, 1, 1, CPUWidget, False, 'B', 'B'),
             (0, 2, 1, 1, GPUTempWidget, False, 'A', 'B')],
            
            # Second row: CPU Graph (1x2) and GPU Temp Graph (1x1)
            [(1, 0, 1, 2, CPUGraphWidget, False, 'A', 'C'),
             (1, 2, 1, 1, GPUTempGraphWidget, False, 'A', 'B')],
            
            # Third row: Separator (1x3)
            [(2, 0, 1, 3, None, True)]  # Last True indicates transparent
        ]
        
        # Calculate grid size from layout
        max_row = 0
        max_col = 0
        
        # Process each row in the layout
        for row in demo_layout:
            for item in row:
                row, col, row_span, col_span, *_ = item
                max_row = max(max_row, row + row_span)
                max_col = max(max_col, col + col_span)
        
        # Set grid size with some room for expansion
        self.grid_size = (max_row + 1, max_col + 1)
        
        # Add the cards
        for row in demo_layout:
            for item in row:
                if len(item) == 8:  # Full spec with color and accent schemes
                    row, col, row_span, col_span, widget_type, transparent, color_scheme, accent_scheme = item
                elif len(item) == 7:  # With color scheme
                    row, col, row_span, col_span, widget_type, transparent, color_scheme = item
                    accent_scheme = 'A'
                elif len(item) == 6:  # With transparency
                    row, col, row_span, col_span, widget_type, transparent = item
                    color_scheme = 'A'
                    accent_scheme = 'A'
                else:  # Basic spec
                    row, col, row_span, col_span, widget_type = item
                    transparent = False
                    color_scheme = 'A'
                    accent_scheme = 'A'
                
                self.add_card(
                    row=row,
                    col=col,
                    size=(row_span, col_span),
                    widget_type=widget_type,
                    transparent=transparent,
                    color_scheme=color_scheme,
                    accent_scheme=accent_scheme
                )
    
    def add_card(self, row, col, size=(1, 1), widget_type=None, transparent=False, color_scheme='A', accent_scheme='A'):
        """Add a card at the specified position"""
        if not self._is_position_available(row, col, size):
            return False
        
        # Create card with widget if specified
        card = Card(widget_type=widget_type, transparent=transparent, 
                   color_scheme=color_scheme, accent_scheme=accent_scheme)
        
        # Set size based on grid spans
        base_width = 200
        base_height = 150
        width = base_width * size[1]
        height = base_height * size[0]
        card.setMinimumSize(width, height)
        
        # Add remove button to card
        card.add_remove_button(lambda: self._remove_card(row, col, size))
        
        # Add to layout and track position
        self.grid_layout.addWidget(card, row, col, size[0], size[1])
        
        # Track occupied positions
        for r in range(row, row + size[0]):
            for c in range(col, col + size[1]):
                self.grid_positions[(r, c)] = card
        
        # Track card for edit mode
        self.cards.append(card)
        
        return True
    
    def _remove_card(self, row, col, size):
        """Remove a card and free up its grid positions"""
        if (row, col) not in self.grid_positions:
            return
        
        card = self.grid_positions[(row, col)]
        
        # Remove from tracking lists
        if card in self.cards:
            self.cards.remove(card)
        
        # Remove from grid tracking
        for r in range(row, row + size[0]):
            for c in range(col, col + size[1]):
                self.grid_positions.pop((r, c), None)
        
        # Remove from layout and delete
        self.grid_layout.removeWidget(card)
        card.deleteLater()
    
    def _is_position_available(self, row, col, size):
        """Check if a position is available for a card of given size"""
        if row + size[0] > self.grid_size[0] or col + size[1] > self.grid_size[1]:
            return False
            
        for r in range(row, row + size[0]):
            for c in range(col, col + size[1]):
                if (r, c) in self.grid_positions:
                    return False
        return True
    
    def _add_card(self):
        """Show dialog and add card based on user input"""
        dialog = AddCardDialog(self, max_rows=self.grid_size[0], max_cols=self.grid_size[1])
        if dialog.exec():
            values = dialog.get_values()
            size = values['size']
            position = values['position']
            color_scheme = values['color_scheme']
            
            # Map widget type string to class
            widget_types = {
                "Memory Widget": MemoryWidget,
                "CPU Widget": CPUWidget,
                "CPU Graph": CPUGraphWidget,
                "GPU Graph": GPUGraphWidget,
                "GPU Memory Graph": GPUMemoryGraphWidget,
                "GPU Temp Graph": GPUTempGraphWidget,
                "CPU Temp": CPUTempWidget,
                "GPU Usage": GPUWidget,
                "GPU Temp": GPUTempWidget,
                "Separator": lambda parent: None,
                "CPU Text": CPUTextWidget,
                "Ping Text": PingTextWidget,
                # Add other widget types here
            }
            widget_type = widget_types.get(values['type'])
            
            # Check if it's a separator
            is_separator = values['type'] == "Separator"
            
            # Check if the position is available
            row, col = position
            if self._is_position_available(row, col, size):
                self.add_card(row, col, size, widget_type=widget_type, 
                            transparent=is_separator, color_scheme=color_scheme,
                            accent_scheme=values['accent_scheme'])
                self._update_grid_layout()
            else:
                # If requested position isn't available, find the first available one
                new_position = self._find_available_position(size)
                if new_position:
                    row, col = new_position
                    self.add_card(row, col, size, widget_type=widget_type, 
                                transparent=is_separator, color_scheme=color_scheme,
                                accent_scheme=values['accent_scheme'])
                    self._update_grid_layout()
    
    def _find_available_position(self, size):
        """Find first available position that fits the card size"""
        rows, cols = size
        
        # Check each possible position
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                # Check if this position works
                can_fit = True
                
                # Make sure we're not exceeding grid bounds
                if row + rows > self.grid_size[0] or col + cols > self.grid_size[1]:
                    continue
                
                # Check if all required positions are free
                for r in range(row, row + rows):
                    for c in range(col, col + cols):
                        if (r, c) in self.grid_positions:
                            can_fit = False
                            break
                    if not can_fit:
                        break
                
                if can_fit:
                    return (row, col)
        
        # If we get here, we need to expand the grid
        return self._expand_grid_for_size(size)
    
    def _expand_grid_for_size(self, size):
        """Expand grid if necessary and return new position"""
        rows, cols = size
        
        # Find the first empty row
        empty_row = 0
        while any((empty_row, c) in self.grid_positions 
                 for c in range(self.grid_size[1])):
            empty_row += 1
        
        # If we need more columns, expand the grid
        if self.grid_size[1] < cols:
            self.grid_size = (self.grid_size[0], cols)
        
        # If we need more rows, expand the grid
        if empty_row + rows > self.grid_size[0]:
            self.grid_size = (empty_row + rows, self.grid_size[1])
        
        return (empty_row, 0)
    
    def _update_grid_layout(self):
        """Update grid layout properties based on current content"""
        # Update spacing based on grid size
        base_spacing = 16
        self.grid_layout.setSpacing(base_spacing)
        
        # Emit layout changed signal
        self.grid_layout.update()
