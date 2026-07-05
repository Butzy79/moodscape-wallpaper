import json
import os
from PyQt6.QtGui import QGuiApplication


class UISettingsLoader:
    def __init__(self, path="config/settings.json"):
        self.path = path
        self._load()

    # -------------------------
    # Default settings
    # -------------------------
    DEFAULTS = {
        "window": {
            "width": 480,
            "height": 240,
            "opacity": 0.9,
            "always_on_top": False,
            "x": 100,
            "y": 200
        },
        "ui": {
            "top_bar_height_cm": 0.8,
            "background_color": [60, 55, 45],
            "separator_color": [255, 217, 102],
            "font_color": [245, 245, 245]
        },
        "app": {
            "mood": "",
            "frequency": "30",
            "adaptive": "True"
        }
    }

    # -------------------------
    # Public values (ready to use)
    # -------------------------
    window_width: int
    window_height: int
    window_x: int
    window_y: int
    window_opacity: float
    always_on_top: bool
    app_data: dict

    top_bar_height_px: int

    bg_color: tuple
    separator_color: tuple
    font_color: tuple

    # -------------------------
    # Load + merge
    # -------------------------
    def _load(self):
        data = self.DEFAULTS.copy()

        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    user_data = json.load(f)
                data = self._merge_dicts(data, user_data)
            except Exception:
                pass  # usa default silenziosamente

        self._apply(data)

    def _merge_dicts(self, base, override):
        result = base.copy()
        for k, v in override.items():
            if isinstance(v, dict) and k in result:
                result[k] = self._merge_dicts(result[k], v)
            else:
                result[k] = v
        return result

    # -------------------------
    # Apply + validation
    # -------------------------
    def _apply(self, data):
        window = data["window"]
        ui = data["ui"]
        app = data.get("app", {})

        self.window_width = int(window.get("width", 480))
        self.window_height = int(window.get("height", 640))
        self.window_x = int(window.get("x", 200))
        self.window_y = int(window.get("y", 100))
        self.window_opacity = float(window.get("opacity", 0.9))
        self.always_on_top = bool(window.get("always_on_top", False))

        self.top_bar_height_px = self.cm_to_px(
            float(ui.get("top_bar_height_cm", 0.8))
        )

        self.bg_color = tuple(ui.get("background_color", [60, 55, 45]))
        self.separator_color = tuple(ui.get("separator_color", [255, 217, 102]))
        self.font_color = tuple(ui.get("font_color", [245, 245, 245]))
        self.app_data = app

    # -------------------------
    # Utils
    # -------------------------
    def cm_to_px(self, cm: float) -> int:
        screen = QGuiApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch() if screen else 96
        return int((cm / 2.54) * dpi)

    def save(self, app_data=None):
        data = {
            "window": {
                "width": self.window_width,
                "height": self.window_height,
                "opacity": self.window_opacity,
                "always_on_top": self.always_on_top,
                # optionally x, y if already set on the object
                "x": getattr(self, "window_x", self.DEFAULTS["window"]["x"]),
                "y": getattr(self, "window_y", self.DEFAULTS["window"]["y"]),
            },
            "ui": {
                "top_bar_height_cm": round(self.top_bar_height_px * 2.54 / 96, 2),  # approximate cm
                "background_color": list(self.bg_color),
                "separator_color": list(self.separator_color),
                "font_color": list(self.font_color),
            },
            "app": app_data or {}
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        # Write JSON to file
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[UISettingsLoader] Failed to save settings: {e}")