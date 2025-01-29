import json
from pathlib import Path
from PyQt6.QtGui import QColor
from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        self._current_theme = {}
        self._themes: Dict[str, Dict[str, Any]] = {}
        self._load_themes()
    
    def _load_themes(self):
        """Load themes from JSON file"""
        theme_path = Path(__file__).parent / "settings" / "themes.json"
        try:
            with open(theme_path, 'r') as f:
                self._themes = json.load(f)
            self._current_theme = self._themes.get('light', {})  # Default to light theme
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading themes: {e}")
            self._themes = {}
            self._current_theme = {}
    
    def get_color(self, key: str) -> QColor:
        """Get a color from the current theme"""
        color_str = self._current_theme.get(key, "#000000")
        if isinstance(color_str, str):
            if color_str.startswith("rgba"):
                # Parse rgba string
                rgba = color_str.strip("rgba()").split(",")
                return QColor(int(rgba[0]), int(rgba[1]), int(rgba[2]), int(float(rgba[3]) * 255))
            else:
                # Parse hex color
                return QColor(color_str)
        return QColor("#000000")
    
    def get_style(self, key: str) -> str:
        """Get a style value from the current theme"""
        return self._current_theme.get(key, "")
    
    def set_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in self._themes:
            self._current_theme = self._themes[theme_name]
        else:
            print(f"Theme '{theme_name}' not found")

# Global theme manager instance
theme = ThemeManager() 