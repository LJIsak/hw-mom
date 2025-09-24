from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor
from theme_manager import theme

class ResizeHandle(QWidget):
    def __init__(self, parent, position: str):
        super().__init__(parent)
        self.position = position
        self.setFixedSize(16, 16)
        self.setCursor(self._get_cursor())
        
        self.is_dragging = False
        self.start_pos = None

    def _get_cursor(self) -> Qt.CursorShape:
        """Get cursor shape based on handle position"""
        if self.position in ['top', 'bottom']:
            return Qt.CursorShape.SizeVerCursor
        elif self.position in ['left', 'right']:
            return Qt.CursorShape.SizeHorCursor
        elif self.position in ['top_left', 'bottom_right']:
            return Qt.CursorShape.SizeFDiagCursor
        elif self.position in ['top_right', 'bottom_left']:
            return Qt.CursorShape.SizeBDiagCursor
        return Qt.CursorShape.ArrowCursor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Use theme color for the handle
        handle_color = theme.get_color("color_font_primary")
        
        # Change color on hover
        if self.underMouse():
            handle_color = handle_color.lighter(120)
            
        painter.setBrush(handle_color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Draw ellipse with a small margin
        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawEllipse(rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.start_pos = event.globalPosition().toPoint()
            if hasattr(self.parent(), '_emit_resize_started'):
                self.parent()._emit_resize_started(self.position)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = event.globalPosition().toPoint() - self.start_pos
            if hasattr(self.parent(), '_emit_resizing'):
                self.parent()._emit_resizing(self.position, delta)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_dragging:
            self.is_dragging = False
            if hasattr(self.parent(), '_emit_resize_finished'):
                self.parent()._emit_resize_finished()
        super().mouseReleaseEvent(event)
