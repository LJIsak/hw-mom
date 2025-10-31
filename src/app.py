from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QSizePolicy, QPushButton, QVBoxLayout, QFrame)
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPalette, QColor, QIcon
from widgets.base_card import Card
from widgets.card_dialog import AddCardDialog
from widgets.circle_widget import CircleWidget
from widgets.graph_widget import GraphWidget
from widgets.text_widget import TextWidget
from widgets.resize_preview import ResizePreview
from widgets.landing_preview import LandingPreview
from theme_manager import theme
from collectors.system_metrics import SystemMetrics
from layout_parser import LayoutParser
from pathlib import Path
from typing import Optional
from functools import partial


class SettingsButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("⚙", parent)
        self.setObjectName("settingsButton")
        self.setFixedSize(36, 36)
        self.setCheckable(True)
        self._update_colors()
    
    def _update_colors(self):
        # Get base color and create darker version
        base_color = theme.get_color("color_widget")
        text_color = theme.get_color("color_font_secondary")
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
            QPushButton#settingsButton {{
                background-color: {base_color.name()};
                border-radius: 18px;
                color: {text_color.name()};
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding-top: -4px;
            }}
            QPushButton#settingsButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#settingsButton:pressed, QPushButton#settingsButton:checked {{
                background-color: {pressed_color.name()};
                color: {text_color.name()};
            }}
        """)

class ThemeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("☀", parent)
        self.setObjectName("themeButton")
        self.setFixedSize(36, 36)
        self.setCheckable(True)
        self._update_colors()

    def _update_colors(self):
        # Get base color and create darker version
        text_color = theme.get_color("color_font_secondary")
        base_color = theme.get_color("color_widget")
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
                border-radius: 18px;
                color: {text_color.name()};
                font-size: 20px;
                font-weight: bold;
                border: none;
                
                padding-top: -4px;
            }}
            QPushButton#themeButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#themeButton:pressed {{
                background-color: {pressed_color.name()};
            }}
        """)


class EmptyCellButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setObjectName("emptyCellButton")
        self.setFixedSize(28, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_colors()

    def _update_colors(self):
        text_color = theme.get_color("color_font_secondary")
        accent_color = theme.get_color("color_accent_1")
        hover_color = QColor(accent_color)
        hover_color.setAlpha(200)
        pressed_color = QColor(accent_color)
        pressed_color.setAlpha(255)

        self.setStyleSheet(f"""
            QPushButton#emptyCellButton {{
                background-color: transparent;
                border: none;
                border-radius: 14px;
                color: {text_color.name()};
                font-size: 20px;
                font-weight: bold;
                padding: 1px 3px 6px 3px;
            }}
            QPushButton#emptyCellButton:hover {{
                background-color: rgba({hover_color.red()}, {hover_color.green()}, {hover_color.blue()}, {hover_color.alpha()});
                color: {text_color.name()};
            }}
            QPushButton#emptyCellButton:pressed {{
                background-color: rgba({pressed_color.red()}, {pressed_color.green()}, {pressed_color.blue()}, {pressed_color.alpha()});
                color: {text_color.name()};
            }}
        """)

class MainWindow(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HW-Mom")
        self.setMinimumSize(128, 64)
        self.resize(640, 480)  # Set default starting size
        self.setWindowIcon(QIcon(str(Path(__file__).parent / "assets" / "icon.png")))
        self.setAcceptDrops(True)
        
        # Create the global SystemMetrics instance
        self.system_metrics = SystemMetrics()
        
        # Setup metrics update timer
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.system_metrics.update)
        self.metrics_timer.start(self.system_metrics.update_interval)
        
        # Create main widget and set it as central
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Add resize preview and landing preview widgets
        self.resize_preview = ResizePreview(self.main_widget)
        self.landing_preview = LandingPreview(self.main_widget)
        
        # Set the background color
        palette = self.main_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, theme.get_color("color_background"))
        self.main_widget.setAutoFillBackground(True)
        self.main_widget.setPalette(palette)
        
        # Initialize grid tracking
        self.grid_positions = {}  # {(row, col): card_widget}
        self.empty_cell_buttons = {}
        self._empty_cell_refresh_queued = False
        
        # Track cards for edit mode
        self.cards = []
        
        # Track resizing state
        self.resizing_card = None
        self.resize_handle_pos = None
        self.resize_start_geom = None
        self.current_resize_geom = None
        
        # Set initial grid size
        self.grid_size = (5, 6)  # Starting with a 5x6 grid
        
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
        self.grid_layout.setSpacing(0) # Spacing now handled by card

        # Add layouts to main layout
        main_layout.addLayout(self.grid_layout)
        self.main_widget.setLayout(main_layout)
    
    def _add_floating_buttons(self):
        """Add floating action buttons"""
        # Edit mode button
        self.settings_button = SettingsButton(self)
        self.settings_button.clicked.connect(self._toggle_edit_mode)
        self.settings_button.raise_()
        
        # Theme toggle button
        self.theme_button = ThemeButton(self)
        self.theme_button.clicked.connect(self._toggle_theme)
        self.theme_button.raise_()
        self.theme_button.hide()
        
        self._position_floating_buttons()
    
    def _position_floating_buttons(self):
        """Position the floating buttons"""
        # Get common bottom position for all buttons
        margin_x = 24
        margin_y = self.height() - 24
        margin_x_right = self.width() - margin_x
        
        # Position settings button (bottom right)
        self.settings_button.move(
            margin_x_right - self.settings_button.width(), 
            margin_y - self.settings_button.height())
        
        # Position theme button to the left of the settings button
        self.theme_button.move(
            self.settings_button.x() - self.theme_button.width() - 12,
            margin_y - self.theme_button.height())
    
    def resizeEvent(self, event):
        """
        Handle window resize to reposition floating buttons and enforce equal grid cell sizes.
        """
        super().resizeEvent(event)
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

        self._refresh_empty_cell_buttons()
    
    def _toggle_edit_mode(self):
        """Toggle visibility of remove buttons on all cards"""
        show = self.settings_button.isChecked()
        self.theme_button.setVisible(show)
        for card in self.cards:
            if hasattr(card, 'set_draggable'):
                card.set_draggable(show)
            if hasattr(card, 'set_edit_mode'):
                card.set_edit_mode(show)
        self._refresh_empty_cell_buttons()
        
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
        palette.setColor(QPalette.ColorRole.Window, theme.get_color("color_background"))
        self.main_widget.setPalette(palette)
        
        # Update all cards
        for card in self.cards:
            card._update_style()
            
        # Update all buttons
        self.settings_button._update_colors()
        self.theme_button._update_colors()
        for button in self.empty_cell_buttons.values():
            button._update_colors()
        
    def _refresh_empty_cell_buttons(self):
        """Recreate or reposition add-card buttons for empty grid cells."""
        if not hasattr(self, 'grid_layout'):
            return

        self._empty_cell_refresh_queued = False

        layout_geom = self.grid_layout.geometry()
        if layout_geom.width() <= 0 or layout_geom.height() <= 0:
            self._queue_empty_cell_refresh()
            return

        show_buttons = getattr(self, 'settings_button', None) and self.settings_button.isChecked()

        # Remove buttons that correspond to occupied or out-of-range cells
        for pos, button in list(self.empty_cell_buttons.items()):
            row, col = pos
            if (
                pos in self.grid_positions or
                row >= self.grid_size[0] or
                col >= self.grid_size[1]
            ):
                button.hide()
                button.deleteLater()
                del self.empty_cell_buttons[pos]

        needs_retry = False

        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                if (row, col) in self.grid_positions:
                    continue

                cell_rect = self.grid_layout.cellRect(row, col)
                button = self.empty_cell_buttons.get((row, col))
                if cell_rect.width() <= 0 or cell_rect.height() <= 0:
                    needs_retry = True
                    if button:
                        button.setVisible(bool(show_buttons))
                        if show_buttons:
                            button.raise_()
                    continue

                if button is None:
                    button = EmptyCellButton(self.main_widget)
                    button.clicked.connect(partial(self._handle_empty_cell_clicked, row, col))
                    self.empty_cell_buttons[(row, col)] = button

                center = cell_rect.center()
                button.move(
                    layout_geom.x() + center.x() - button.width() // 2,
                    layout_geom.y() + center.y() - button.height() // 2
                )
                button.setVisible(bool(show_buttons))
                if show_buttons:
                    button.raise_()

        if not show_buttons:
            for button in self.empty_cell_buttons.values():
                button.hide()

        if needs_retry:
            self._queue_empty_cell_refresh()

    def _queue_empty_cell_refresh(self):
        """Schedule a deferred refresh for empty cell buttons."""
        if not self._empty_cell_refresh_queued:
            self._empty_cell_refresh_queued = True
            QTimer.singleShot(0, self._refresh_empty_cell_buttons)

    def _handle_empty_cell_clicked(self, row: int, col: int):
        """Handle requests to add a card from an empty grid cell."""
        self._add_card_from_dialog((row, col))

        
    def _get_widget_info(self, widget_type: str) -> type:
        """Get the widget class for a given widget type."""
        widget_types = {
            "circle": CircleWidget,
            "graph": GraphWidget,
            "text": TextWidget,
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
    
    def _add_card_from_dialog(self, initial_position: Optional[tuple[int, int]] = None):
        """Show dialog and add card based on user input"""
        dialog = AddCardDialog(self)
        if initial_position:
            dialog.row_pos_spin.setValue(initial_position[0] + 1)
            dialog.col_pos_spin.setValue(initial_position[1] + 1)
        if dialog.exec():
            values = dialog.get_values()
            
            # Get widget class
            widget_class = self._get_widget_info(values['widget_type'])
            if not widget_class:
                print(f"Invalid widget type: {values['widget_type']}")
                return

            # Use metric string directly without suffix
            metric_str = values['metric_str']

            self._place_card(
                size=values['size'],
                requested_position=values['position'],
                widget_class=widget_class,
                metric_str=metric_str,
                color_scheme=values['color_scheme'],
                accent_scheme=values['accent_scheme']
            )
            self._refresh_empty_cell_buttons()

    def _place_card(
            self, size, requested_position, widget_class, metric_str,
            color_scheme='A', accent_scheme='A'):
        """Place a card in the grid at the specified position."""
        row, col = requested_position
        
        # Create and add the card
        self._create_and_add_card(
            row, col, size, widget_class, metric_str,
            color_scheme, accent_scheme
        )

    def _create_and_add_card(
            self, row, col, size, widget_class, metric_str,
            color_scheme='A', accent_scheme='A'):
        """Create and add a card to the specified position."""
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
        
        # Connect resize signals
        card.resize_started.connect(lambda pos, c=card: self._handle_resize_started(c, pos))
        card.resizing.connect(lambda pos, delta, c=card: self._handle_resizing(c, pos, delta))
        card.resize_finished.connect(lambda c=card: self._handle_resize_finished(c))
        
        # Set size policy for all cards
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Ensure new cards inherit current edit mode and draggable state
        is_edit_mode = self.settings_button.isChecked()
        if hasattr(card, 'set_draggable'):
            card.set_draggable(is_edit_mode)
        if hasattr(card, 'set_edit_mode'):
            card.set_edit_mode(is_edit_mode)

        # Add remove button and connect it
        card.remove_btn.clicked.connect(lambda: self._remove_card(card))
        card.remove_btn.setVisible(self.settings_button.isChecked())
        
        # Add to grid and track position
        self.grid_layout.addWidget(card, row, col, size[0], size[1])
        
        # Update position tracking
        for r in range(row, row + size[0]):
            for c in range(col, col + size[1]):
                self.grid_positions[(r, c)] = card
        
        self.cards.append(card)
        self._refresh_empty_cell_buttons()
        # print(f"Added {widget_class.__name__} card at " 
        #       f"position ({row}, {col}) with size {size}") # Debug

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
        self._refresh_empty_cell_buttons()

    def _compactify_grid(self):
        """Remove empty rows and columns from the grid. Called after a card is removed."""

    def dragEnterEvent(self, event):
        """Accept drag events from cards."""
        if event.mimeData().text().startswith('card-drag:'):
            event.acceptProposedAction()
            self.landing_preview.show()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """Hide the landing preview when the drag leaves the window."""
        self.landing_preview.hide()
        event.accept()

    def _nearest_cell(self, pos_in_grid: QPoint) -> tuple[int, int]:
        """Return (row, col) of the cell whose center is closest to the given position in grid coords."""
        best_r, best_c = 0, 0
        best_dist = None
        for r in range(self.grid_size[0]):
            for c in range(self.grid_size[1]):
                rect = self.grid_layout.cellRect(r, c)
                center = rect.center()
                dx = pos_in_grid.x() - center.x()
                dy = pos_in_grid.y() - center.y()
                d2 = dx*dx + dy*dy
                if best_dist is None or d2 < best_dist:
                    best_dist = d2
                    best_r, best_c = r, c
        return best_r, best_c

    def _index_from_position(self, pos_in_grid: QPoint) -> tuple[float, float]:
        """Map a grid-space position to continuous (row_index, col_index) using cell centers with linear interpolation."""
        # Build center coordinates for rows and columns
        row_centers = [self.grid_layout.cellRect(r, 0).center().y() for r in range(self.grid_size[0])]
        col_centers = [self.grid_layout.cellRect(0, c).center().x() for c in range(self.grid_size[1])]

        def interp(centers: list[float], value: float) -> float:
            if value <= centers[0]:
                return 0.0
            if value >= centers[-1]:
                return float(len(centers) - 1)
            for i in range(len(centers) - 1):
                a = centers[i]
                b = centers[i + 1]
                if a <= value <= b:
                    t = (value - a) / max(b - a, 1e-6)
                    return i + t
            return float(len(centers) - 1)

        row_idx = interp(row_centers, float(pos_in_grid.y()))
        col_idx = interp(col_centers, float(pos_in_grid.x()))
        return row_idx, col_idx

    def _candidate_top_left(self, pos_in_grid: QPoint, row_span: int, col_span: int) -> tuple[int, int]:
        """Given pointer position and spans, compute a top-left so that the item's center aligns with the cursor, clamped to fit the grid."""
        row_center_idx, col_center_idx = self._index_from_position(pos_in_grid)
        top_left_r = int(round(row_center_idx - (row_span - 1) / 2))
        top_left_c = int(round(col_center_idx - (col_span - 1) / 2))
        # Clamp to grid bounds
        top_left_r = max(0, min(top_left_r, self.grid_size[0] - row_span))
        top_left_c = max(0, min(top_left_c, self.grid_size[1] - col_span))
        return top_left_r, top_left_c

    def dragMoveEvent(self, event):
        """Show and position the landing preview."""
        mime_text = event.mimeData().text()
        if not mime_text.startswith('card-drag:'):
            event.ignore()
            return
            
        try:
            card_id = int(mime_text.split(':')[1])
        except (IndexError, ValueError):
            event.ignore()
            return

        card = self._get_card_from_id(card_id)
        if not card:
            event.ignore()
            return
        idx = self.grid_layout.indexOf(card)
        _, _, row_span, col_span = self.grid_layout.getItemPosition(idx)

        # Map pointer position into grid layout coordinate space
        pos_in_window = event.position().toPoint()
        pos_in_widget = self.main_widget.mapFrom(self, pos_in_window)
        pos_in_grid = QPoint(pos_in_widget.x(), pos_in_widget.y())

        # Compute best top-left position based on nearest cell and clamp to fit span
        target_row, target_col = self._candidate_top_left(pos_in_grid, row_span, col_span)
        
        # Check if the drop is valid
        dragged_card = self._get_card_from_id(card_id)
        if self._is_drop_area_free(target_row, target_col, row_span, col_span, dragged_card):
            self._update_landing_preview(target_row, target_col, row_span, col_span)
            self.landing_preview.show()
            self.landing_preview.raise_()
            event.acceptProposedAction()
        else:
            self.landing_preview.hide()
            event.ignore()

    def dropEvent(self, event):
        """Perform move on drop and hide indicator."""
        self.landing_preview.hide()
        mime_text = event.mimeData().text()
        if not mime_text.startswith('card-drag:'):
            event.ignore()
            return
        try:
            card_id = int(mime_text.split(':')[1])
        except (IndexError, ValueError):
            event.ignore()
            return
        source_card = self._get_card_from_id(card_id)
        if not source_card:
            event.ignore()
            return
        idx = self.grid_layout.indexOf(source_card)
        if idx == -1:
            event.ignore()
            return
        _, _, row_span, col_span = self.grid_layout.getItemPosition(idx)

        # Map pointer position into grid layout coordinate space
        pos_in_window = event.position().toPoint()
        pos_in_widget = self.main_widget.mapFrom(self, pos_in_window)
        grid_geom = self.grid_layout.geometry()
        pos_in_grid = QPoint(pos_in_widget.x() - grid_geom.x(), pos_in_widget.y() - grid_geom.y())

        # Determine top-left candidate near the pointer and clamp to fit span
        target_row, target_col = self._candidate_top_left(pos_in_grid, row_span, col_span)

        if not self._is_drop_area_free(target_row, target_col, row_span, col_span, source_card):
            event.ignore()
            return

        # Move the card
        positions_to_remove = [pos for pos, c in self.grid_positions.items() if c == source_card]
        for pos in positions_to_remove:
            del self.grid_positions[pos]
        self.grid_layout.removeWidget(source_card)
        self.grid_layout.addWidget(source_card, target_row, target_col, row_span, col_span)
        for r in range(target_row, target_row + row_span):
            for c in range(target_col, target_col + col_span):
                self.grid_positions[(r, c)] = source_card
        self._refresh_empty_cell_buttons()
        event.acceptProposedAction()

    def _handle_resize_started(self, card, position):
        if self.resizing_card:
            return  # Avoid starting a new resize if one is in progress
        
        idx = self.grid_layout.indexOf(card)
        if idx != -1:
            r, c, rs, cs = self.grid_layout.getItemPosition(idx)
            self.resizing_card = card
            self.resize_handle_pos = position
            self.resize_start_geom = (r, c, rs, cs)
            self.current_resize_geom = (r, c, rs, cs)
            
            # Show preview at the current card's geometry
            self._update_resize_preview(r, c, rs, cs)
            self.resize_preview.show()
            self.resize_preview.raise_()

    def _handle_resizing(self, card, position, delta):
        if not self.resizing_card or card is not self.resizing_card:
            return

        cell_width = self.grid_layout.cellRect(0, 0).width()
        cell_height = self.grid_layout.cellRect(0, 0).height()
        
        # Prevent division by zero if grid isn't fully formed yet
        if cell_width == 0 or cell_height == 0:
            return

        # Calculate change in grid cells
        dc = round(delta.x() / cell_width)
        dr = round(delta.y() / cell_height)
        
        r, c, rs, cs = self.resize_start_geom
        
        # Calculate new geometry based on which handle is being dragged
        if self.resize_handle_pos == 'right':
            cs = max(1, cs + dc)
        elif self.resize_handle_pos == 'left':
            c = min(max(0, c + dc), c + cs - 1)
            cs = max(1, cs - dc)
        elif self.resize_handle_pos == 'bottom':
            rs = max(1, rs + dr)
        elif self.resize_handle_pos == 'top':
            r = min(max(0, r + dr), r + rs - 1)
            rs = max(1, rs - dr)
        
        # If geometry is valid and has changed, update the preview
        if (r, c, rs, cs) != self.current_resize_geom:
            if self._is_drop_area_free(r, c, rs, cs, self.resizing_card):
                self.current_resize_geom = (r, c, rs, cs)
                self._update_resize_preview(r, c, rs, cs)

    def _handle_resize_finished(self, card):
        if not self.resizing_card:
            return
            
        self.resize_preview.hide()

        # Get the final geometry from the preview
        r, c, rs, cs = self.current_resize_geom
        start_r, start_c, _, _ = self.resize_start_geom

        # Update card only if the geometry has changed
        if (r, c, rs, cs) != self.resize_start_geom:
            # Remove old positions
            positions_to_remove = [pos for pos, c in self.grid_positions.items() if c == self.resizing_card]
            for pos in positions_to_remove:
                del self.grid_positions[pos]
            
            # Update layout
            self.grid_layout.removeWidget(self.resizing_card)
            self.grid_layout.addWidget(self.resizing_card, r, c, rs, cs)

            # Add new positions
            for i in range(r, r + rs):
                for j in range(c, c + cs):
                    self.grid_positions[(i, j)] = self.resizing_card

        # Reset resizing state
        self.resizing_card = None
        self.resize_handle_pos = None
        self.resize_start_geom = None
        self.current_resize_geom = None
        self._refresh_empty_cell_buttons()

    def _update_resize_preview(self, r, c, rs, cs):
        """Update the geometry of the resize preview widget."""
        # Calculate the top-left corner of the starting cell
        start_rect = self.grid_layout.cellRect(r, c)
        
        # Calculate the bottom-right corner of the ending cell
        end_rect = self.grid_layout.cellRect(r + rs - 1, c + cs - 1)
        
        # Combine to get the full geometry in grid layout coordinates
        preview_rect = start_rect.united(end_rect)
        
        self.resize_preview.setGeometry(preview_rect)

    def _update_landing_preview(self, r, c, rs, cs):
        """Update the geometry of the landing preview widget."""
        start_rect = self.grid_layout.cellRect(r, c)
        end_rect = self.grid_layout.cellRect(r + rs - 1, c + cs - 1)
        preview_rect = start_rect.united(end_rect)
        
        # Adjust for card margin
        margin = 16
        preview_rect.adjust(margin, margin, -margin, -margin)
        
        self.landing_preview.setGeometry(preview_rect)

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
            # print(f"Grid size: {self.grid_size}") # Debug
            
            # Set uniform stretch factors for grid
            for col in range(self.grid_size[1]):
                self.grid_layout.setColumnStretch(col, 1)
            for row in range(self.grid_size[0]):
                self.grid_layout.setRowStretch(row, 1)
            
            # Create widgets from parsed config
            for widget_config in parser.widgets:
                # Get widget class for non-separator widgets
                widget_class = self._get_widget_info(widget_config.widget_type)
                if not widget_class:
                    print(f"Invalid widget type: {widget_config.widget_type}")
                    continue
                
                # Use metric string directly without suffix
                metric_str = widget_config.metric
                
                # Calculate spans and positions
                from_row = widget_config.start_y
                from_col = widget_config.start_x
                row_span = widget_config.end_y - widget_config.start_y + 1
                col_span = widget_config.end_x - widget_config.start_x + 1
                
                # Place the card
                self._place_card(
                    size=(row_span, col_span),
                    requested_position=(from_row, from_col),
                    widget_class=widget_class,
                    metric_str=metric_str,
                    color_scheme=widget_config.color_scheme
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
        finally:
            self._refresh_empty_cell_buttons()

    def _get_card_from_id(self, card_id: int) -> Optional[Card]:
        """Return the card instance matching the given object id, if any."""
        for card in self.cards:
            if id(card) == card_id:
                return card
        return None

    def _is_drop_area_free(self, target_row: int, target_col: int, row_span: int, col_span: int, dragged_card: Optional[Card]) -> bool:
        """Return True if the rectangle [target_row..row_span, target_col..col_span] is inside bounds and unoccupied (excluding dragged_card)."""
        # Bounds check
        if target_row < 0 or target_col < 0:
            return False
        if target_row + row_span > self.grid_size[0] or target_col + col_span > self.grid_size[1]:
            return False

        # Build occupancy grid excluding the dragged card
        occupied = [[False for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        for card in self.cards:
            if card is dragged_card:
                continue
            idx = self.grid_layout.indexOf(card)
            if idx != -1:
                r, c, rs, cs = self.grid_layout.getItemPosition(idx)
                for i in range(r, r + rs):
                    for j in range(c, c + cs):
                        if 0 <= i < self.grid_size[0] and 0 <= j < self.grid_size[1]:
                            occupied[i][j] = True

        # Check occupancy of target area
        for i in range(target_row, target_row + row_span):
            for j in range(target_col, target_col + col_span):
                if occupied[i][j]:
                    return False
        return True
