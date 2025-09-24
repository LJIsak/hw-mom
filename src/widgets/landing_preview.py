from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt
from theme_manager import theme

class LandingPreview(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setVisible(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Use card_background color to match the drag preview
        preview_color = theme.get_color("color_widget")
        
        # Draw background with opacity similar to drag preview (0.7)
        bg_color = QColor(preview_color)
        bg_color.setAlpha(180) 
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        painter.drawRoundedRect(self.rect(), 12, 12)
