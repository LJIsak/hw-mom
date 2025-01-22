from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QSizePolicy, QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPalette, QColor
from widgets.base_card import Card
from widgets.card_dialog import AddCardDialog
from widgets.circle_widget import CircleWidget
from widgets.graph_widget import GraphWidget
from widgets.text_widget import TextWidget
from widgets.separator_card import SeparatorCard
from theme_manager import theme
from collectors.system_metrics import SystemMetrics

class AddCardButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setObjectName("addCardButton")
        self.setFixedSize(40, 40)
        self._update_colors()
    
    def _update_colors(self):
        # Get base color and create hover/pressed colors
        base_color = theme.get_color("add_button")
        hover_color = QColor(
            int(base_color.red() * 0.8),
            int(base_color.green() * 0.8),
            int(base_color.blue() * 0.8)
        )
        pressed_color = QColor(
            int(hover_color.red() * 0.8),
            int(hover_color.green() * 0.8),
            int(hover_color.blue() * 0.8)
        )
        self.setStyleSheet(f"""
            QPushButton#addCardButton {{
                background-color: {base_color.name()};
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding-top: -4px;
            }}
            QPushButton#addCardButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#addCardButton:pressed {{
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
            int(base_color.red() * 0.8),
            int(base_color.green() * 0.8),
            int(base_color.blue() * 0.8)
        )
        pressed_color = QColor(
            int(hover_color.red() * 0.8),
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
            int(base_color.red() * 0.8),
            int(base_color.green() * 0.8),
            int(base_color.blue() * 0.8)
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
        self.setMinimumSize(256, 128)
        self.resize(640, 480)  # Set default starting size
        
        # Create the global SystemMetrics instance
        self.system_metrics = SystemMetrics()
        
        # Setup metrics update timer
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.system_metrics.update)
        self.metrics_timer.start(self.system_metrics.update_interval)
        
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
        
        # Set initial grid size
        self.grid_size = (3, 3)  # Starting with a 3x3 grid
        
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
        
        self.main_widget.setLayout(main_layout)
    
    def _add_floating_buttons(self):
        """Add floating action buttons"""
        # Add button
        self.add_button = AddCardButton(self)
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
            self.theme_button.setText("☾") # Moon emoji for dark mode
        else:
            theme.set_theme('light')
            self.theme_button.setText("☀") # Sun emoji for light mode
        
        self._update_theme()
    
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
    
    def _get_widget_info(self, widget_type: str) -> type:
        """Get the widget class for a given widget type."""
        widget_types = {
            "Circle Widget": CircleWidget,
            "Graph Widget": GraphWidget,
            "Text Widget": TextWidget,
            "Separator": None
        }
        return widget_types.get(widget_type)

    def _get_metric_suffix(self, widget_type: str) -> str:
        """Get the appropriate metric suffix based on widget type."""
        if widget_type == "Graph Widget":
            return "_history"
        elif widget_type == "Circle Widget" or widget_type == "Text Widget":
            return "_usage"
        return ""

    def _add_card(self):
        """Show dialog and add card based on user input"""
        dialog = AddCardDialog(self)
        if dialog.exec():
            values = dialog.get_values()
            
            # Get widget class
            widget_class = self._get_widget_info(values['widget_type'])
            if not widget_class:
                # Handle separator
                self._place_card(
                    size=values['size'],
                    requested_position=values['position'],
                    widget_class=None,
                    metric_str=None,
                    is_separator=True,
                    color_scheme=values['color_scheme'],
                    accent_scheme=values['accent_scheme']
                )
                return

            # Get base metric string and add appropriate suffix
            base_metric = values['metric_str']
            metric_suffix = self._get_metric_suffix(values['widget_type'])
            final_metric = base_metric + metric_suffix

            # Debug print to verify metric string
            print(f"Creating widget with metric string: {final_metric}")

            self._place_card(
                size=values['size'],
                requested_position=values['position'],
                widget_class=widget_class,
                metric_str=final_metric,
                is_separator=False,
                color_scheme=values['color_scheme'],
                accent_scheme=values['accent_scheme']
            )
    
    def _format_title(self, metric_str: str) -> str:
        """Format metric string into a proper title."""
        # Mapping of metric strings to display titles
        metric_titles = {
            'cpu_usage': 'CPU',
            'memory_usage': 'Memory',
            'gpu_usage': 'GPU',
            'gpu_temp': 'GPU Temp',
            'gpu_memory': 'GPU Memory',
            'ping': 'Ping'
        }
        
        # Remove _history suffix if present
        base_metric = metric_str.replace('_history', '')
        
        # Return mapped title or fallback to formatted string
        return metric_titles.get(base_metric, base_metric.replace('_', ' ').title())

    def _place_card(self, size, requested_position, widget_class, metric_str,
                   is_separator=False, color_scheme='A', accent_scheme='A'):
        """Place a card in the grid, finding the best position if requested spot is taken."""
        position = self._get_valid_position(requested_position, size)
        if position:
            row, col = position
            self._create_and_add_card(
                row, col, size, widget_class, metric_str,
                is_separator, color_scheme, accent_scheme
            )
            self._update_grid_layout()

    def _get_valid_position(self, requested_position, size):
        """Get a valid position for the card, expanding grid if necessary."""
        row, col = requested_position
        rows, cols = size

        # Expand grid if needed to accommodate the requested position
        needed_rows = row + rows
        needed_cols = col + cols
        
        if needed_rows > self.grid_size[0] or needed_cols > self.grid_size[1]:
            self.grid_size = (
                max(self.grid_size[0], needed_rows),
                max(self.grid_size[1], needed_cols)
            )

        # Check if position is available
        if self._is_position_available(row, col, size):
            return (row, col)

        # If position is taken, find first available position
        for r in range(self.grid_size[0]):
            for c in range(self.grid_size[1]):
                if self._is_position_available(r, c, size):
                    return (r, c)

        # If no position found, add to new row at the bottom
        new_row = self.grid_size[0]
        self.grid_size = (new_row + rows, max(self.grid_size[1], cols))
        return (new_row, 0)

    def _is_position_available(self, row, col, size):
        """Check if a position is available for a card of given size."""
        rows, cols = size
        
        # Check if any position in the range is occupied
        return not any(
            (r, c) in self.grid_positions
            for r in range(row, row + rows)
            for c in range(col, col + cols)
        )

    def _create_and_add_card(self, row, col, size, widget_class, metric_str,
                            is_separator, color_scheme, accent_scheme):
        """Create and add a card to the specified position."""
        if is_separator:
            card = SeparatorCard(self)
        else:
            # Create the widget with the metric string and system metrics
            widget = widget_class(
                metric_str=metric_str,
                system_metrics=self.system_metrics,
                title=self._format_title(metric_str),
                accent_scheme=accent_scheme
            )
            
            # Create the card with the widget
            card = Card(widget=widget, color_scheme=color_scheme)
            card.remove_btn.clicked.connect(lambda: self._remove_card(card))
            card.remove_btn.setVisible(self.edit_button.isChecked())
        
        # Add to grid and track position
        self.grid_layout.addWidget(card, row, col, size[0], size[1])
        
        # Update position tracking
        for r in range(row, row + size[0]):
            for c in range(col, col + size[1]):
                self.grid_positions[(r, c)] = card
        
        self.cards.append(card)

    def _update_grid_layout(self):
        """Update grid layout properties and refresh the display."""
        # Update spacing based on grid size
        base_spacing = 16
        self.grid_layout.setSpacing(base_spacing)
        
        # Remove any empty rows/columns
        self._compact_grid()
        
        # Force layout update
        self.grid_layout.update()
    
    def _compact_grid(self):
        """Remove empty rows and columns from the grid."""
        # Get all occupied positions
        occupied_rows = set()
        occupied_cols = set()
        for pos in self.grid_positions.keys():
            row, col = pos
            occupied_rows.add(row)
            occupied_cols.add(col)
        
        if not occupied_rows or not occupied_cols:
            # If grid is empty, reset to 0x0
            self.grid_size = (0, 0)
            return
        
        # Update grid size to match actual content
        self.grid_size = (
            max(occupied_rows) + 1,
            max(occupied_cols) + 1
        )
    
    def _remove_card(self, card):
        """Remove a card from the grid."""
        # Find and remove all positions occupied by this card
        positions_to_remove = []
        for pos, c in self.grid_positions.items():
            if c == card:
                positions_to_remove.append(pos)
        
        for pos in positions_to_remove:
            del self.grid_positions[pos]
        
        # Remove from cards list
        self.cards.remove(card)
        
        # Remove from layout and delete
        self.grid_layout.removeWidget(card)
        card.deleteLater()
        
        # Update layout
        self._update_grid_layout()
