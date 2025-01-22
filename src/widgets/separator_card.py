from .base_card import Card

class SeparatorCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent, transparent=True) 