from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QSizePolicy, QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPalette, QColor, QIcon
from widgets.base_card import Card
from widgets.card_dialog import AddCardDialog
from widgets.circle_widget import CircleWidget
from widgets.graph_widget import GraphWidget
from widgets.text_widget import TextWidget
from widgets.separator_card import SeparatorCard
from theme_manager import theme
from collectors.system_metrics import SystemMetrics
from layout_parser import LayoutParser
from pathlib import Path


class AddCardButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setObjectName("addCardButton")
        self.setFixedSize(36, 36)
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
                border-radius: 18px;
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
        self.setFixedSize(36, 36)
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
                border-radius: 18px;
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
        self.setMinimumSize(128, 64)
        self.resize(640, 480)  # Set default starting size
        self.setWindowIcon(QIcon(str(Path(__file__).parent / "assets" / "icon.png")))
        
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
        
        # Load default layout
        self._load_layout()
    
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
        self.add_button.clicked.connect(self._add_card_from_dialog)
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
        margin_x = 24
        margin_y = self.height() - 24
        margin_x_right = self.width() - margin_x
        
        # Position add button (bottom right)
        self.add_button.move(
            margin_x_right - self.add_button.width(), 
            margin_y - self.add_button.height())
        
        # Position edit button to the left of add button
        self.edit_button.move(
            self.add_button.x() - self.edit_button.width() - 12, 
            margin_y - self.edit_button.height())
        
        # Position theme button (bottom left)
        self.theme_button.move(
            margin_x + self.theme_button.width() - 16, 
            margin_y - self.theme_button.height())
    
    def resizeEvent(self, event):
        """
        Handle window resize to reposition floating buttons and enforce equal grid cell sizes.
        """
        super().resizeEvent(event)
        if hasattr(self, 'add_button'):
            self._position_floating_buttons()

        # Enforce uniform grid cell sizes based on the current main widget size.
        margins = self.main_widget.layout().contentsMargins()
        spacing = self.grid_layout.spacing()
        available_height = (self.main_widget.height() - margins.top() - margins.bottom() 
                            - spacing * (self.grid_size[0] - 1))
        available_width = (self.main_widget.width() - margins.left() - margins.right() 
                           - spacing * (self.grid_size[1] - 1))
        cell_height = available_height / self.grid_size[0]
        cell_width = available_width / self.grid_size[1]

        for row in range(self.grid_size[0]):
            self.grid_layout.setRowMinimumHeight(row, int(cell_height))
        for col in range(self.grid_size[1]):
            self.grid_layout.setColumnMinimumWidth(col, int(cell_width))
    
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
            "circle": CircleWidget,
            "graph": GraphWidget,
            "text": TextWidget,
            "separator": None
        }
        return widget_types.get(widget_type)
    
    def _format_title(self, metric_str: str) -> str:
        """Format metric string into a proper title."""
        # Mapping of metric strings to display titles
        metric_titles = {
            'cpu': 'CPU',
            'memory': 'Memory',
            'gpu': 'GPU',
            'gpu_temp': 'GPU Temp',
            'gpu_memory': 'GPU Memory',
            'ping': 'Ping'
        }
        
        # Return mapped title or fallback to formatted string
        return metric_titles.get(metric_str, metric_str.replace('_', ' ').title())
    
    def _add_card_from_dialog(self):
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

            # Use metric string directly without suffix
            metric_str = values['metric_str']

            self._place_card(
                size=values['size'],
                requested_position=values['position'],
                widget_class=widget_class,
                metric_str=metric_str,
                is_separator=False,
                color_scheme=values['color_scheme'],
                accent_scheme=values['accent_scheme']
            )

    def _place_card(
            self, size, requested_position, widget_class, metric_str, is_separator=False, 
            color_scheme='A', accent_scheme='A'):
        """Place a card in the grid at the specified position."""
        row, col = requested_position
        
        # Create and add the card
        self._create_and_add_card(
            row, col, size, widget_class, metric_str,
            is_separator, color_scheme, accent_scheme
        )

    def _create_and_add_card(
            self, row, col, size, widget_class, metric_str, is_separator=False, 
            color_scheme='A', accent_scheme='A'):
        """Create and add a card to the specified position."""
        if is_separator:
            card = SeparatorCard(self)
        else:
            # Get base title before adding suffix
            base_metric = metric_str.replace('_usage', '').replace('_history', '')
            title = self._format_title(base_metric)
            
            # Create the widget with the metric string and system metrics
            widget = widget_class(
                metric_str=metric_str,
                system_metrics=self.system_metrics,
                title=title,
                accent_scheme=accent_scheme
            )
            
            # Create the card with the widget
            card = Card(widget=widget, color_scheme=color_scheme)
        
        # Set size policy for all cards
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Add remove button and connect it
        card.remove_btn.clicked.connect(lambda: self._remove_card(card))
        card.remove_btn.setVisible(self.edit_button.isChecked())
        
        # Add to grid and track position
        self.grid_layout.addWidget(card, row, col, size[0], size[1])
        
        # Update position tracking
        for r in range(row, row + size[0]):
            for c in range(col, col + size[1]):
                self.grid_positions[(r, c)] = card
        
        self.cards.append(card)
        print(f"Added {'separator' if is_separator else widget_class.__name__} card at " 
              f"position ({row}, {col}) with size {size}") # Debug

    def _remove_card(self, card):
        """Remove a card from the grid. Called when the remove button is clicked in edit mode."""
        # Find and remove all positions occupied by this card
        positions_to_remove = []
        for pos, c in self.grid_positions.items():
            if c == card:
                positions_to_remove.append(pos)
        
        for pos in positions_to_remove:
            del self.grid_positions[pos]
        
        # Remove from cards list and layout
        self.cards.remove(card)
        self.grid_layout.removeWidget(card)
        card.deleteLater()

    def _compactify_grid(self):
        """Remove empty rows and columns from the grid. Called after a card is removed."""

    def _load_layout(self):
        """Load and apply the default layout."""
        layout_path = Path(__file__).parent / "settings" / "default_layout.txt"
        parser = LayoutParser(str(layout_path))
        
        try:
            # Set theme
            theme.set_theme(parser.theme_str)
            self._update_theme()
            self.theme_button.setChecked(parser.theme_str == 'dark')
            
            # Set grid size from parser
            self.grid_size = (parser.n_rows, parser.n_cols)
            print(f"Grid size: {self.grid_size}") # Debug
            
            # Set uniform stretch factors for grid
            for col in range(self.grid_size[1]):
                self.grid_layout.setColumnStretch(col, 1)
            for row in range(self.grid_size[0]):
                self.grid_layout.setRowStretch(row, 1)
            
            # Create widgets from parsed config
            for widget_config in parser.widgets:
                # Handle separator differently
                if widget_config.is_separator:
                    self._place_card(
                        size=(widget_config.rowSpan, widget_config.colSpan),
                        requested_position=(widget_config.fromRow, widget_config.fromCol),
                        widget_class=None,
                        metric_str=None,
                        is_separator=True,
                        color_scheme=widget_config.color_scheme.upper()
                    )
                    continue
                
                # Get widget class for non-separator widgets
                widget_class = self._get_widget_info(widget_config.widget_type)
                if not widget_class:
                    print(f"Invalid widget type: {widget_config.widget_type}")  # Debug
                    continue
                
                # Use metric string directly without suffix
                metric_str = widget_config.metric
                
                # Place the card
                self._place_card(
                    size=(widget_config.rowSpan, widget_config.colSpan),
                    requested_position=(widget_config.fromRow, widget_config.fromCol),
                    widget_class=widget_class,
                    metric_str=metric_str,
                    is_separator=False,
                    color_scheme=widget_config.color_scheme.upper()
                )
        
        except Exception as e:
            print(f"Error loading layout: {e}")
            # Create a default widget if layout loading fails
            self._place_card(
                size=(1, 1),
                requested_position=(0, 0),
                widget_class=self._get_widget_info("circle"),
                metric_str="cpu",
                color_scheme='A'
            )
