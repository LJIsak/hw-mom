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
            self._current_theme = self._themes.get('dark', {})  # Default to dark theme
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading themes: {e}")
            self._themes = {}
            self._current_theme = {
                "font_size_primary": 32,
                "font_size_secondary": 16,
                "color_font_primary": "#ffffff",
                "color_font_secondary": "#d1d1d1",
                "color_font_legend": "#555555",
                "color_background": "#202020",
                "color_widget": "#191919",
                "color_accent_1": "#f59121",
                "color_accent_2": "#9d2062",
                "color_accent_3": "#39b8e3"
            }
    
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
    
    def get_font_size_primary(self) -> int:
        """Return the base font size from the current theme (defaulting to 32 if not specified)."""
        return self._current_theme.get("font_size_primary", 32)

    def get_font_size_secondary(self) -> int:
        """Return the secondary font size from the current theme (defaulting to 12 if not specified)."""
        return self._current_theme.get("font_size_secondary", 12)

# Global theme manager instance
theme = ThemeManager() 