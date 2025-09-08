from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QColor, QPainter, QDrag, QPixmap
from theme_manager import theme

class RemoveButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("×", parent)  # Using × symbol for remove
        self.setObjectName("removeButton")
        self.setFixedSize(24, 24)
        self._update_style()
        self.hide()  # Hidden by default, shown in edit mode
    
    def _update_style(self):
        """Update button style with current theme colors"""
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
            QPushButton#removeButton {{
                background-color: {base_color.name()};
                border-radius: 12px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                padding-bottom: 4px;
            }}
            QPushButton#removeButton:hover {{
                background-color: {hover_color.name()};
            }}
            QPushButton#removeButton:pressed {{
                background-color: {pressed_color.name()};
            }}
        """)

class Card(QFrame):
    def __init__(self, widget=None, color_scheme='A'):
        super().__init__()
        self.setObjectName("card")
        # print(f"Creating card with color scheme: {color_scheme}")  # Debug
        self.color_scheme = color_scheme
        
        # Draggable state
        self.is_draggable = False
        self.start_pos = None
        
        # Create layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(self.layout)
        
        # Add widget if specified
        if widget:
            self.widget = widget
            # Pass color scheme to widget
            if hasattr(widget, 'set_color_scheme'):
                widget.set_color_scheme(color_scheme)
            self.layout.addWidget(widget)
        
        # Set up the card's appearance
        self._update_style()
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 16))
        self.setGraphicsEffect(shadow)
        
        # Create remove button
        self.remove_btn = RemoveButton(self)
    
    def set_draggable(self, draggable: bool):
        """Set the draggable state of the card."""
        self.is_draggable = draggable

    def mousePressEvent(self, event):
        """Handle mouse press to initiate a drag."""
        if self.is_draggable and event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move to perform the drag and drop."""
        if (self.is_draggable and 
            event.buttons() == Qt.MouseButton.LeftButton and
            self.start_pos is not None and
            (event.pos() - self.start_pos).manhattanLength() > 10):
            
            drag = QDrag(self)
            mime_data = QMimeData()

            # Use the card's object ID to uniquely identify it during the drag
            mime_data.setText(f'card-drag:{id(self)}')
            drag.setMimeData(mime_data)

            # Create a semi-transparent pixmap of the widget for the drag preview
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setOpacity(0.7)
            
            # Use the card's background color
            brush_color = theme.get_color("card_background")
            painter.setBrush(brush_color)
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw the rounded rectangle
            border_radius = 12
            painter.drawRoundedRect(pixmap.rect(), border_radius, border_radius)
            
            painter.end()
            
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())

            # Start the drag operation
            drag.exec(Qt.DropAction.MoveAction)
            self.start_pos = None

        super().mouseMoveEvent(event)

    def _update_style(self):
        """Update the card's style based on current theme"""
        # All cards use the same background color now
        bg_color = theme.get_color("card_background").name()
        
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {bg_color};
                border-radius: 12px;
                margin: 8px;
            }}
        """)
    
    def resizeEvent(self, event):
        """Handle resize to position remove button"""
        super().resizeEvent(event)
        # Position remove button in top-right corner
        self.remove_btn.move(
            self.width() - self.remove_btn.width() - 8,
            8
        ) 