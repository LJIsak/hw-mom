from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSpinBox, QDialogButtonBox, QComboBox, QGroupBox,
                            QRadioButton, QButtonGroup, QFormLayout, QWidget)
from PyQt6.QtCore import Qt

class AddCardDialog(QDialog):
    def __init__(self, parent=None, max_rows=22, max_cols=40):
        super().__init__(parent)
        self.setWindowTitle("Add Card")
        self.setModal(True)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Size group
        size_group = QGroupBox("Size")
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
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # Position group
        pos_group = QGroupBox("Position")
        pos_layout = QHBoxLayout()
        
        # Row position
        row_pos_layout = QHBoxLayout()
        row_pos_layout.addWidget(QLabel("Row:"))
        self.row_pos_spin = QSpinBox()
        self.row_pos_spin.setMinimum(0)
        self.row_pos_spin.setMaximum(max_rows - 1)
        row_pos_layout.addWidget(self.row_pos_spin)
        pos_layout.addLayout(row_pos_layout)
        
        # Column position
        col_pos_layout = QHBoxLayout()
        col_pos_layout.addWidget(QLabel("Column:"))
        self.col_pos_spin = QSpinBox()
        self.col_pos_spin.setMinimum(0)
        self.col_pos_spin.setMaximum(max_cols - 1)
        col_pos_layout.addWidget(self.col_pos_spin)
        pos_layout.addLayout(col_pos_layout)
        
        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)
        
        # Widget type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Widget Type:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Circle",
            "Graph",
            "Text",
            "Separator"
        ])
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Subtype selection
        subtype_layout = QHBoxLayout()
        subtype_layout.addWidget(QLabel("Widget:"))
        self.subtype_combo = QComboBox()
        subtype_layout.addWidget(self.subtype_combo)
        layout.addLayout(subtype_layout)
        
        # Initialize subtypes
        self._on_type_changed(self.type_combo.currentText())
        
        # Add style selections group
        style_group = QGroupBox("Style")
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
        
        style_group.setLayout(style_layout)
        layout.addWidget(style_group)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def _on_type_changed(self, widget_type):
        """Update subtype options based on selected type"""
        self.subtype_combo.clear()
        
        if widget_type == "Circle":
            self.subtype_combo.addItems([
                "Memory Usage",
                "CPU Usage",
                "GPU Usage",
                "GPU Temperature",
                "GPU Memory"
            ])
        elif widget_type == "Graph":
            self.subtype_combo.addItems([
                "CPU Usage",
                "GPU Usage",
                "GPU Temperature",
                "GPU Memory"
            ])
        elif widget_type == "Text":
            self.subtype_combo.addItems([
                "CPU Usage",
                "Memory Usage",
                "GPU Usage",
                "GPU Temperature",
                "Ping"
            ])
        else:  # Separator
            self.subtype_combo.setEnabled(False)
            return
        
        self.subtype_combo.setEnabled(True)
    
    def get_values(self):
        """Return the dialog values"""
        widget_type = self.type_combo.currentText()
        subtype = self.subtype_combo.currentText()
        
        # Map selection to actual widget type
        type_mapping = {
            ("Circle", "Memory Usage"): "Memory Widget",
            ("Circle", "CPU Usage"): "CPU Widget",
            ("Circle", "GPU Usage"): "GPU Usage",
            ("Circle", "GPU Temperature"): "GPU Temp",
            ("Circle", "GPU Memory"): "GPU Memory",
            ("Graph", "CPU Usage"): "CPU Graph",
            ("Graph", "GPU Usage"): "GPU Graph",
            ("Graph", "GPU Temperature"): "GPU Temp Graph",
            ("Graph", "GPU Memory"): "GPU Memory Graph",
            ("Separator", ""): "Separator",
            ("Text", "CPU Usage"): "CPU Text",
            ("Text", "Memory Usage"): "Memory Text",
            ("Text", "GPU Usage"): "GPU Text",
            ("Text", "GPU Temperature"): "GPU Temp Text",
            ("Text", "Ping"): "Ping Text"
        }
        
        return {
            'position': (self.row_pos_spin.value(), self.col_pos_spin.value()),
            'size': (self.row_spin.value(), self.col_spin.value()),
            'type': type_mapping.get((widget_type, subtype), "Separator"),
            'color_scheme': 'B' if self.bg_b.isChecked() else 'A',
            'accent_scheme': 'C' if self.accent_c.isChecked() else ('B' if self.accent_b.isChecked() else 'A')
        } 