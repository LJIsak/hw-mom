from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSpinBox, QDialogButtonBox, QComboBox, QGroupBox)
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
                "GPU Temperature"
            ])
        elif widget_type == "Graph":
            self.subtype_combo.addItems([
                "CPU Usage",
                "GPU Usage",
                "GPU Temperature"
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
            ("Graph", "CPU Usage"): "CPU Graph",
            ("Graph", "GPU Usage"): "GPU Graph",
            ("Graph", "GPU Temperature"): "GPU Temp Graph",
            ("Separator", ""): "Separator"
        }
        
        return {
            'position': (self.row_pos_spin.value(), self.col_pos_spin.value()),
            'size': (self.row_spin.value(), self.col_spin.value()),
            'type': type_mapping.get((widget_type, subtype), "Separator")
        } 