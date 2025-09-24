from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, QPoint
from PyQt6.QtGui import QColor, QPainter, QDrag, QPixmap, QEnterEvent
from theme_manager import theme
from .resize_handle import ResizeHandle

class RemoveButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("×", parent)  # Using × symbol for remove
        self.setObjectName("removeButton")
        self.setFixedSize(24, 24)
        self._update_style()
        self.hide()  # Hidden by default, shown in edit mode
    
    def _update_style(self):
        """Update button style with current theme colors"""
        base_color = theme.get_color("color_accent_2")
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
    resize_started = pyqtSignal(str)
    resizing = pyqtSignal(str, QPoint)
    resize_finished = pyqtSignal()

    def __init__(self, widget=None, color_scheme='A'):
        super().__init__()
        self.setObjectName("card")
        # print(f"Creating card with color scheme: {color_scheme}")  # Debug
        self.color_scheme = color_scheme
        
        # Draggable state
        self.is_draggable = False
        self.start_pos = None

        # Edit mode state
        self.is_in_edit_mode = False
        self.setMouseTracking(True)
        
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
        shadow.setBlurRadius(32)
        shadow.setXOffset(2)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 10))
        self.setGraphicsEffect(shadow)
        
        # Create remove button
        # self.remove_btn = RemoveButton(self)
        self._create_resize_handles()
    
    def set_draggable(self, draggable: bool):
        """Set the draggable state of the card."""
        self.is_draggable = draggable

    def set_edit_mode(self, in_edit_mode: bool):
        """Set the card's edit mode state."""
        self.is_in_edit_mode = in_edit_mode
        # Ensure handles are hidden when leaving edit mode
        if not in_edit_mode:
            self.set_resizable(False)

    def set_resizable(self, resizable: bool):
        """Show or hide resize handles."""
        for handle in self.handles:
            handle.setVisible(resizable)

    def enterEvent(self, event: QEnterEvent):
        """Show resize handles on hover when in edit mode."""
        if self.is_in_edit_mode:
            self.set_resizable(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Hide resize handles when mouse leaves."""
        self.set_resizable(False)
        self.unsetCursor()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle mouse press to initiate a drag."""
        # Do not start drag if a resize handle was clicked.
        child = self.childAt(event.pos())
        if isinstance(child, ResizeHandle):
            super().mousePressEvent(event)
            return
            
        if self.is_draggable and event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move to perform the drag and drop and update cursor."""
        # --- Handle cursor change on hover ---
        if self.is_in_edit_mode and not event.buttons():
            margin = 16
            active_rect = self.rect().adjusted(margin, margin, -margin, -margin)
            child = self.childAt(event.pos())
            is_over_handle = isinstance(child, ResizeHandle)

            if active_rect.contains(event.pos()) and not is_over_handle:
                self.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.unsetCursor()
        
        # --- Handle drag-and-drop initiation ---
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
            pixmap = QPixmap(self.size()*0.88)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setOpacity(0.7)
            
            # Use the card's background color
            brush_color = theme.get_color("color_widget")
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

            # Reset cursor after drag is finished
            self.unsetCursor()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release to reset cursor if drag didn't start."""
        if self.is_draggable and event.button() == Qt.MouseButton.LeftButton:
            # After a click, reset cursor to hover state
            if self.is_in_edit_mode:
                margin = 16
                active_rect = self.rect().adjusted(margin, margin, -margin, -margin)
                child = self.childAt(event.pos())
                is_over_handle = isinstance(child, ResizeHandle)

                if active_rect.contains(event.pos()) and not is_over_handle:
                    self.setCursor(Qt.CursorShape.OpenHandCursor)
                else:
                    self.unsetCursor()
        super().mouseReleaseEvent(event)

    def _update_style(self):
        """Update the card's style based on current theme"""
        # All cards use the same background color now
        bg_color = theme.get_color("color_widget").name()
        
        self.setStyleSheet(f"""
            QFrame#card {{
                background-color: {bg_color};
                border-radius: 12px;
                margin: 16px;
            }}
        """)

        if hasattr(self.widget, '_update_style'):
            self.widget._update_style()
    
    def resizeEvent(self, event):
        """Handle resize of cards during edit mode."""
        super().resizeEvent(event)
        self._position_resize_handles()

    def _create_resize_handles(self):
        """Create resize handles for each edge."""
        self.handles = []
        positions = ['top', 'bottom', 'left', 'right']
        for pos in positions:
            handle = ResizeHandle(self, pos)
            handle.hide()
            self.handles.append(handle)

    def _position_resize_handles(self):
        """Position resize handles on the card's edges."""
        if not self.handles:
            return
            
        w, h = self.width(), self.height()
        handle_size = self.handles[0].width()
        offset = handle_size // 2
        margin = 16

        positions = {
            'top': (w // 2 - offset, margin - offset),
            'bottom': (w // 2 - offset, h - margin - offset),
            'left': (margin - offset, h // 2 - offset),
            'right': (w - margin - offset, h // 2 - offset)
        }

        for handle in self.handles:
            x, y = positions[handle.position]
            handle.move(x, y)
    
    def _emit_resize_started(self, position: str):
        """Emit resize_started signal."""
        self.resize_started.emit(position)

    def _emit_resizing(self, position: str, delta: QPoint):
        """Emit resizing signal."""
        self.resizing.emit(position, delta)

    def _emit_resize_finished(self):
        """Emit resize_finished signal."""
        self.resize_finished.emit()