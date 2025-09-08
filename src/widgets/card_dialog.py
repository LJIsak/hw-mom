from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox,
                            QComboBox, QDialogButtonBox, QGroupBox, QButtonGroup,
                            QRadioButton, QFormLayout, QWidget)

class AddCardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Card")
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the dialog UI"""
        layout = QVBoxLayout()
        
        # Widget type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Widget Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Circle Widget",
            "Graph Widget",
            "Text Widget",
        ])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Connect type_combo to a handler
        self.type_combo.currentTextChanged.connect(self._handle_widget_type_change)
        
        # Metric selection
        self.metric_layout = QHBoxLayout()
        self.metric_layout.addWidget(QLabel("Metric:"))
        self.metric_combo = QComboBox()
        self.metric_combo.addItems([
            "Memory Usage",     # memory
            "CPU Usage",        # cpu
            "GPU Usage",        # gpu_usage
            "GPU Temperature",  # gpu_temp
            "GPU Memory",       # gpu_memory
            "Fan Speed",        # fan_speed
            "Ping"              # ping
        ])
        self.metric_layout.addWidget(self.metric_combo)
        layout.addLayout(self.metric_layout)
        
        # Size group
        self.size_group = QGroupBox("Size")
        size_layout = QHBoxLayout()
        
        # Row span (height)
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel("Height:"))
        self.row_spin = QSpinBox()
        self.row_spin.setMinimum(1)
        self.row_spin.setMaximum(4)
        row_layout.addWidget(self.row_spin)
        size_layout.addLayout(row_layout)
        
        # Column span (width)
        col_layout = QHBoxLayout()
        col_layout.addWidget(QLabel("Width:"))
        self.col_spin = QSpinBox()
        self.col_spin.setMinimum(1)
        self.col_spin.setMaximum(4)
        col_layout.addWidget(self.col_spin)
        size_layout.addLayout(col_layout)
        
        self.size_group.setLayout(size_layout)
        layout.addWidget(self.size_group)
        
        # Position group
        pos_group = QGroupBox("Position")
        pos_layout = QHBoxLayout()
        
        # Row position
        row_pos_layout = QHBoxLayout()
        row_pos_layout.addWidget(QLabel("Row:"))
        self.row_pos_spin = QSpinBox()
        self.row_pos_spin.setMinimum(1)
        self.row_pos_spin.setMaximum(99)
        row_pos_layout.addWidget(self.row_pos_spin)
        pos_layout.addLayout(row_pos_layout)
        
        # Column position
        col_pos_layout = QHBoxLayout()
        col_pos_layout.addWidget(QLabel("Column:"))
        self.col_pos_spin = QSpinBox()
        self.col_pos_spin.setMinimum(1)
        self.col_pos_spin.setMaximum(99)
        col_pos_layout.addWidget(self.col_pos_spin)
        pos_layout.addLayout(col_pos_layout)
        
        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)
        
        # Add style selections group
        self.style_group = QGroupBox("Style")
        style_layout = QFormLayout()
        
        # Background color selection
        bg_widget = QWidget()
        bg_layout = QHBoxLayout(bg_widget)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        self.bg_group = QButtonGroup()
        self.bg_a = QRadioButton("A")
        self.bg_b = QRadioButton("B")
        self.bg_a.setChecked(True)
        self.bg_group.addButton(self.bg_a, 1)
        self.bg_group.addButton(self.bg_b, 2)
        bg_layout.addWidget(self.bg_a)
        bg_layout.addWidget(self.bg_b)
        bg_layout.addStretch()
        
        # Accent color selection
        accent_widget = QWidget()
        accent_layout = QHBoxLayout(accent_widget)
        accent_layout.setContentsMargins(0, 0, 0, 0)
        self.accent_group = QButtonGroup()
        self.accent_a = QRadioButton("A")
        self.accent_b = QRadioButton("B")
        self.accent_c = QRadioButton("C")
        self.accent_a.setChecked(True)
        self.accent_group.addButton(self.accent_a, 1)
        self.accent_group.addButton(self.accent_b, 2)
        self.accent_group.addButton(self.accent_c, 3)
        accent_layout.addWidget(self.accent_a)
        accent_layout.addWidget(self.accent_b)
        accent_layout.addWidget(self.accent_c)
        accent_layout.addStretch()
        
        style_layout.addRow("Background:", bg_widget)
        style_layout.addRow("Accent:", accent_widget)
        
        self.style_group.setLayout(style_layout)
        layout.addWidget(self.style_group)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        
        # Initial state update
        self._handle_widget_type_change(self.type_combo.currentText())

    def _handle_widget_type_change(self, widget_type):
        """Show/hide metric selection based on widget type."""
        is_separator = (widget_type == "Separator")
        
        # Iterate over widgets in metric_layout and hide them
        for i in range(self.metric_layout.count()):
            widget = self.metric_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(not is_separator)
        
        # Also hide/show style and size groups
        self.size_group.setVisible(not is_separator)
        self.style_group.setVisible(not is_separator)

    def _get_metric_str(self, display_name: str) -> str:
        """Convert display name to metric string."""
        metric_map = {
            "CPU Usage": "cpu",
            "Memory Usage": "memory",
            "GPU Usage": "gpu",
            "GPU Temperature": "gpu_temp",
            "GPU Memory": "gpu_memory",
            "Fan Speed": "fan_speed",
            "Ping": "ping"
        }
        return metric_map.get(display_name, "")

    def get_values(self):
        """Get the dialog values."""
        widget_type_text = self.type_combo.currentText().split(' ')[0].lower()
        
        return {
            'size': (self.row_spin.value(), self.col_spin.value()),
            'position': (self.row_pos_spin.value() - 1, self.col_pos_spin.value() - 1),
            'widget_type': widget_type_text,
            'metric_str': self._get_metric_str(self.metric_combo.currentText()),
            'color_scheme': 'B' if self.bg_b.isChecked() else 'A',
            'accent_scheme': (
                'C' if self.accent_c.isChecked() 
                else 'B' if self.accent_b.isChecked() 
                else 'A'
            )
        } 