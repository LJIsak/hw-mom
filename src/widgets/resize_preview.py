from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
from theme_manager import theme

class ResizePreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setVisible(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        preview_color = theme.get_color("color_accent_2")
        
        # Draw background
        bg_color = QColor(preview_color)
        bg_color.setAlpha(50)  # Semi-transparent background
        painter.setBrush(bg_color)
        
        # Draw border
        border_color = QColor(preview_color)
        border_color.setAlpha(200)
        painter.setPen(border_color)
        
        painter.drawRoundedRect(self.rect(), 12, 12)
