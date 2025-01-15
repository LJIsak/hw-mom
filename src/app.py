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

class FloatingButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("+", parent)
        self.setObjectName("floatingButton")
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton#floatingButton {
                background-color: #a5c588;
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding-top: -4px;
            }
            QPushButton#floatingButton:hover {
                background-color: #8fad74;
            }
            QPushButton#floatingButton:pressed {
                background-color: #c95f2c;
            }
        """)

class EditModeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("-", parent)
        self.setObjectName("editModeButton")
        self.setFixedSize(40, 40)
        self.setCheckable(True)  # Make the button toggleable
        self.setStyleSheet("""
            QPushButton#editModeButton {
                background-color: #f0bb8b;
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                padding-top: -4px;
            }
            QPushButton#editModeButton:hover {
                background-color: #e3a368;
            }
            QPushButton#editModeButton:pressed, QPushButton#editModeButton:checked {
                background-color: #cc7f39;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hardware Monitor")
        self.setMinimumSize(640, 480)
        
        # Create main widget and set it as central
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # Set the background color
        palette = self.main_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f2e4d4"))
        self.main_widget.setAutoFillBackground(True)
        self.main_widget.setPalette(palette)
        
        # Initialize grid tracking
        self.grid_positions = {}  # {(row, col): card_widget}
        self.grid_size = (22, 40)  # As per requirements
        
        # Track cards for edit mode
        self.cards = []
        
        # Initialize UI
        self._init_ui()
        
        # Add floating buttons last so they're on top
        self._add_floating_buttons()
    
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
        
        self._position_floating_buttons()
    
    def _position_floating_buttons(self):
        """Position the floating buttons"""
        # Position add button
        add_button_x = self.width() - self.add_button.width() - 32
        add_button_y = self.height() - self.add_button.height() - 32
        self.add_button.move(add_button_x, add_button_y)
        
        # Position edit button to the left of add button
        self.edit_button.move(
            add_button_x - self.edit_button.width() - 16,  # 16px spacing between buttons
            add_button_y
        )
    
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
    
    def _add_demo_cards(self):
        """Add initial demo cards"""
        # First row: Memory widget, CPU widget, and GPU temp
        self.add_card(row=0, col=0, size=(1, 1), widget_type=MemoryWidget)
        self.add_card(row=0, col=1, size=(1, 1), widget_type=CPUWidget)
        self.add_card(row=0, col=2, size=(1, 1), widget_type=GPUTempWidget)
        
        # Second row: CPU Graph and GPU Graph, each spanning 2 columns
        self.add_card(row=1, col=0, size=(1, 2), widget_type=CPUGraphWidget)
        self.add_card(row=1, col=2, size=(1, 2), widget_type=GPUTempGraphWidget)
        
        # Third row: Separator spanning all columns
        self.add_card(row=2, col=0, size=(1, 4), transparent=True)
    
    def add_card(self, row, col, size=(1, 1), widget_type=None, transparent=False):
        """Add a card at the specified position"""
        if not self._is_position_available(row, col, size):
            return False
        
        # Create card with widget if specified
        card = Card(widget_type=widget_type, transparent=transparent)
        
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
            
            # Map widget type string to class
            widget_types = {
                "Memory Widget": MemoryWidget,
                "CPU Widget": CPUWidget,
                "CPU Graph": CPUGraphWidget,
                "GPU Graph": GPUGraphWidget,
                "GPU Temp Graph": GPUTempGraphWidget,
                "CPU Temp": CPUTempWidget,
                "GPU Usage": GPUWidget,
                "GPU Temp": GPUTempWidget,
                "Separator": lambda parent: None,
                # Add other widget types here
            }
            widget_type = widget_types.get(values['type'])
            
            # Check if it's a separator
            is_separator = values['type'] == "Separator"
            
            # Check if the position is available
            row, col = position
            if self._is_position_available(row, col, size):
                self.add_card(row, col, size, widget_type=widget_type, transparent=is_separator)
                self._update_grid_layout()
            else:
                # If requested position isn't available, find the first available one
                new_position = self._find_available_position(size)
                if new_position:
                    row, col = new_position
                    self.add_card(row, col, size, widget_type=widget_type, transparent=is_separator)
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
