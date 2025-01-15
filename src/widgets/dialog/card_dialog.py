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
            "Memory Widget",
            "CPU Widget",
            "CPU Graph",
            "GPU Graph",
            "GPU Temp Graph",
            "CPU Temp",
            "GPU Usage",
            "GPU Temp",
            "Separator"
        ])
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Dialog buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the dialog values"""
        return {
            'position': (self.row_pos_spin.value(), self.col_pos_spin.value()),
            'size': (self.row_spin.value(), self.col_spin.value()),
            'type': self.type_combo.currentText()
        } 