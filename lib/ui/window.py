import os
import webbrowser

import requests
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QScrollArea, QGraphicsOpacityEffect,
    QLineEdit, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices
from lib.ui.ui_setting_loader import UISettingsLoader
from lib.utils.github_version import GitHubVersionWidget
from lib.utils.version import CAVersion

class MainWindowCA(QWidget):
    topbar_style_background = "font-size: 14px; color: #FFD966; background: transparent; border: none;"
    remote_thanks_content = "All the contributors"
    main_frame_style_base = "color: #F5F5F5; font-size: 16px;"
    button_style_full = """
            QPushButton {
                color: #000000;                  /* black text */
                background-color: #FFD966;       /* yellow background */
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFC700;       /* slightly brighter yellow on hover */
            }
        """
    button_style_border = """
        QPushButton {
            color: #FFFFFF;                   /* white text */
            background-color: transparent;    /* transparent */
            border: 2px solid #FFD966;       /* yellow border */
            border-radius: 4px;
            padding: 4px 10px;                /* reduce padding to compensate border */
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgba(255, 217, 102, 0.2); /* subtle yellow overlay */
        }
    """
    i_am_updated = (True, None)
    def __init__(self, settings: UISettingsLoader):
        super().__init__()
        self.i_am_updated = GitHubVersionWidget.check_update_api()
        self.settings = settings

        self.mood_input = QLineEdit()
        self.frequency_box = QComboBox()
        self.adaptive_checkbox = QCheckBox()

        try:
            resp = requests.get("https://ca.panthila.ch/special_thanks.php", timeout=5)
            self.remote_thanks_content = resp.text
        except Exception:
            self.remote_thanks_content = "All the contributors"

        # ---- Window setup ----
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(self.settings.window_opacity)
        self.setFixedSize(self.settings.window_width, self.settings.window_height)
        self.setGeometry(
            getattr(self.settings, "window_x", 100),  # x
            getattr(self.settings, "window_y", 100),  # y
            self.settings.window_width,
            self.settings.window_height
        )

        self.always_on_top = False
        self._drag_active = False
        self._drag_position = QPoint()

        # ---- Main layout direttamente su self ----
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Sfondo del widget principale ----
        self.setStyleSheet("""
            background-color: rgba(60, 55, 45, 220);
            border-radius: 8px;
        """)

        # ---- Top bar ----
        self.top_bar_widget = QWidget()
        top_bar_layout = QHBoxLayout(self.top_bar_widget)
        top_bar_layout.setSpacing(5)
        top_bar_layout.setContentsMargins(8, 0, 8, 0)  # piccolo padding solo laterale

        # ---- Pinned Button ----
        self.pin_btn: QPushButton = QPushButton()
        self.pin_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/thumbtack.png")))
        self.pin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pin_btn.setFixedSize(24, 24)
        self.pin_btn.clicked.connect(self.toggle_pin)
        if self.settings.always_on_top:
            self.toggle_pin()
        top_bar_layout.addWidget(self.pin_btn)

        # ---- Main Frame ---
        self.main_frame: QPushButton = QPushButton("Moodspace Wallpaper")
        self.main_frame.setFixedHeight(32)
        self.main_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.main_frame.setCheckable(True)
        self.main_frame.setStyleSheet(self.topbar_style_background)
        self.main_frame.clicked.connect(self.show_main_frame)
        top_bar_layout.addWidget(self.main_frame)

        top_bar_layout.addStretch()

        if self.i_am_updated[0]:
            # ---- Update button ----
            self.update_btn: QPushButton = QPushButton()
            self.update_btn.setFixedSize(32, 32)
            self.update_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/cloud-download-alt.png")))
            self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.update_btn.setStyleSheet(self.topbar_style_background)
            self.update_btn.clicked.connect(
                lambda: webbrowser.open(f"{GitHubVersionWidget.REPO_WEB}/releases"))
            # ---- Blink effect ----
            opacity = QGraphicsOpacityEffect(self.update_btn)
            self.update_btn.setGraphicsEffect(opacity)

            self.blink_anim = QPropertyAnimation(opacity, b"opacity")
            self.blink_anim.setDuration(800)
            self.blink_anim.setStartValue(1.0)
            self.blink_anim.setEndValue(0.2)
            self.blink_anim.setLoopCount(-1)
            self.blink_anim.start()

            top_bar_layout.addWidget(self.update_btn)

        # ---- Setting button ----
        self.settings_btn: QPushButton = QPushButton()
        self.settings_btn.setFixedSize(32, 32)
        self.settings_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/settings-sliders.png")))
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.setStyleSheet(self.topbar_style_background)
        self.settings_btn.clicked.connect(self.show_settings)
        top_bar_layout.addWidget(self.settings_btn)

        # ---- About button ----
        self.about_btn: QPushButton = QPushButton()
        self.about_btn.setFixedSize(32, 32)
        self.about_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/info.png")))
        self.about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_btn.setStyleSheet(self.topbar_style_background)
        self.about_btn.clicked.connect(self.show_about)
        top_bar_layout.addWidget(self.about_btn)

        # ---- Thanks button ----
        self.thanks_btn: QPushButton = QPushButton()
        self.thanks_btn.setFixedSize(32, 32)
        self.thanks_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/handmade.png")))
        self.thanks_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.thanks_btn.setStyleSheet(self.topbar_style_background)
        self.thanks_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://www.paypal.com/donate/?hosted_button_id=5HECGEZY3EXPY")
            )
        )
        top_bar_layout.addWidget(self.thanks_btn)

        # ---- Close Button ----
        self.close_btn: QPushButton = QPushButton()
        self.close_btn.setToolTip("Close")
        self.close_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/circle-xmark.png")))
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet("""
            QPushButton {
                color: #FF5555;
                background: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                color: #FF0000;
            }
        """)
        self.close_btn.clicked.connect(self.attempt_close)  # Close windows
        top_bar_layout.addWidget(self.close_btn)

        main_layout.addWidget(self.top_bar_widget)

        # ---- Yellow separator ----
        line = QWidget()
        line.setFixedHeight(2)
        line.setStyleSheet("background-color: #FFD966;")
        main_layout.addWidget(line)

        # ---- Content area ----
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)
        self.show_main_frame()
        self.__apply_settings_to_ui()

    def __apply_settings_to_ui(self):
        app = getattr(self.settings, "app_data", {})
        if hasattr(self, "mood_input"):
            self.mood_input.setText(app.get("mood", ""))
        if hasattr(self, "frequency_box"):
            freq = app.get("frequency", "1 hour")
            index = self.frequency_box.findText(freq)
            if index >= 0:
                self.frequency_box.setCurrentIndex(index)
        if hasattr(self, "adaptive_checkbox"):
            self.adaptive_checkbox.setChecked(app.get("adaptive", False))

    def __on_settings_changed(self):
        self.settings.save(app_data={
            "mood": self.mood_input.text(),
            "frequency": self.frequency_box.currentText(),
            "adaptive": self.adaptive_checkbox.isChecked()
        })

    # ---- Close Attempt ----
    def attempt_close(self):
        text = "Are you sure you want to exit the application?"
        w = QWidget()
        w.setObjectName("close")
        l = QVBoxLayout(w)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(self.main_frame_style_base)

        # Stretch to center the label vertically
        l.addStretch()
        l.addWidget(label)

        # Horizontal layout for Yes / No buttons
        btn_layout = QHBoxLayout()

        yes_btn: QPushButton = QPushButton("Yes")
        yes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        yes_btn.setStyleSheet(self.button_style_full)
        yes_btn.clicked.connect(self.save_and_close)  # Close the app if Yes

        no_btn: QPushButton = QPushButton("No")
        no_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        no_btn.setStyleSheet(self.button_style_border)
        no_btn.clicked.connect(lambda: self.show_stack_page("main"))  # Return to main page if No

        # Add buttons to horizontal layout
        btn_layout.addStretch()
        btn_layout.addWidget(yes_btn)
        btn_layout.addSpacing(20)
        btn_layout.addWidget(no_btn)
        btn_layout.addStretch()

        # Add button layout to vertical layout
        l.addLayout(btn_layout)
        l.addStretch()

        # Show this confirmation page in the stacked widget
        self.show_stack_page("close", w)

    def save_and_close(self):
        geom = self.geometry()
        self.settings.window_width = geom.width()
        self.settings.window_height = geom.height()
        self.settings.window_x = geom.x()
        self.settings.window_y = geom.y()
        self.settings.always_on_top = self.always_on_top
        self.settings.save(app_data={
            "mood": self.mood_input.text(),
            "frequency": self.frequency_box.currentText(),
            "adaptive": self.adaptive_checkbox.isChecked()
        })
        self.close()

    # ---- Pin toggle ----
    def toggle_pin(self):
        self.always_on_top = not self.always_on_top
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        if self.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
            self.pin_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/thumbtack_release.png")))
        else:
            self.pin_btn.setIcon(QIcon(os.path.abspath("resources/ui_icons/thumbtack.png")))
        self.setWindowFlags(flags)
        self.show()

    # ---- Drag window ----
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # drag solo se clicchi nella top_bar vuota
            if self.top_bar_widget.geometry().contains(event.pos()):
                # controlla che NON clicchi su pulsanti
                child = self.childAt(event.pos())
                if child in (self.pin_btn,):
                    return
                self._drag_active = True
                self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_active:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_active = False

    def show_stack_page(self, name: str, widget: QWidget = None):
        for i in range(self.stack.count()):
            w = self.stack.widget(i)
            if w.objectName() == name:
                self.stack.setCurrentIndex(i)
                return
        # Page not found
        if widget is not None:
            self.stack.addWidget(widget)
            self.stack.setCurrentWidget(widget)

    def show_about(self):
        version = CAVersion.get_latest_release_version()
        w = QWidget()
        w.setObjectName("about")
        l = QVBoxLayout(w)
        label = QLabel()
        label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        label.setStyleSheet(self.main_frame_style_base)
        error_version = (
            f'<div style="font-size:12px; color:#F3A495; margin:0; padding:0;">'
            f'--- Please update to new version {self.i_am_updated[1]} ---'
            f'</div>'
            if self.i_am_updated[0]
            else ""
        )
        label.setText(
            f'<div style="font-size:22px; font-weight:bold; margin:0; padding:0;">'
            f'Moodspace Wallpaer v{version}'
            f'</div>'
            f'{error_version}'
            f'<div style="margin-top:10px; font-size:15px; font-weight:bold;">'
            f'Special thanks to:'
            f'</div>'
            f'<div>'
            f'{self.remote_thanks_content}'
            f'</div>'
        )
        label.setWordWrap(True)
        l.addWidget(label)
        l.setContentsMargins(10, 5, 10, 0)

        # ---- SCROLL ----
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #4A2E1F;   /* marrone scuro */
                background-color: #1E1E1E;
            }
            QScrollBar:vertical {
                background: #1E1E1E;
                width: 10px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #C9A227;        /* giallo */
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

        self.show_stack_page("about", w)

    def show_settings(self):
        text = "bla bla SETTINGS"
        w = QWidget()
        w.setObjectName("settings")
        l = QVBoxLayout(w)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        l.setContentsMargins(10, 5, 10, 0)
        label.setStyleSheet(self.main_frame_style_base)
        l.addWidget(label)
        l.addStretch()
        self.show_stack_page("settings", w)

    def show_main_frame(self):
        """Main dashboard: mood-based wallpaper controls."""

        w = QWidget()
        w.setObjectName("main")
        layout = QVBoxLayout(w)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        # -----------------------------
        # Title / description
        # -----------------------------
        title = QLabel("Moodspace Wallpaper")
        title.setStyleSheet(self.main_frame_style_base)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(title)

        subtitle = QLabel("Tell us your mood and we will find the right wallpapers for you.")
        subtitle.setStyleSheet("color: #CCCCCC; font-size: 13px;")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # -----------------------------
        # Mood input
        # -----------------------------
        mood_label = QLabel("What would you like?")
        mood_label.setStyleSheet(self.main_frame_style_base)
        layout.addWidget(mood_label)

        self.mood_input = QLineEdit()
        self.mood_input.textChanged.connect(self.__on_settings_changed)
        self.mood_input.setPlaceholderText("e.g. calm, cyberpunk city, cozy night, nature vibes...")
        self.mood_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #FFD966;
                background-color: rgba(0, 0, 0, 80);
                color: #FFFFFF;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.mood_input)

        # -----------------------------
        # Frequency selector
        # -----------------------------
        freq_label = QLabel("Wallpaper change frequency")
        freq_label.setStyleSheet(self.main_frame_style_base)
        layout.addWidget(freq_label)

        self.frequency_box = QComboBox()
        self.frequency_box.currentIndexChanged.connect(self.__on_settings_changed)
        self.frequency_box.addItems([
            "30 minutes",
            "1 hour",
            "2 hours",
            "3 hours"
        ])
        self.frequency_box.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #FFD966;
                background-color: rgba(0, 0, 0, 80);
                color: #FFFFFF;
            }
            QComboBox QAbstractItemView {
                background-color: #2A2A2A;
                color: #FFFFFF;
                selection-background-color: #FFD966;
            }
        """)
        layout.addWidget(self.frequency_box)

        # -----------------------------
        # Day/Night adaptive toggle
        # -----------------------------
        self.adaptive_checkbox = QCheckBox("Enable adaptive wallpapers (day / night)")
        self.adaptive_checkbox.stateChanged.connect(self.__on_settings_changed)
        self.adaptive_checkbox.setStyleSheet("""
            QCheckBox {
                color: #FFFFFF;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #FFD966;
                background: transparent;
            }
            QCheckBox::indicator:checked {
                background-color: #FFD966;
                border: 1px solid #FFD966;
            }
        """)
        layout.addWidget(self.adaptive_checkbox)

        # -----------------------------
        # Check Now Button
        # -----------------------------
        layout.addSpacing(20)
        self.check_wallpaper_btn = QPushButton("Check now wallpaper")
        self.check_wallpaper_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.check_wallpaper_btn.setStyleSheet(self.button_style_full)
        self.check_wallpaper_btn.clicked.connect(self.check_now_wallpaper)

        layout.addWidget(self.check_wallpaper_btn)

        # -----------------------------
        # Stretch filler
        # -----------------------------
        layout.addStretch()

        # Show in stacked widget
        self.show_stack_page("main", w)

    def check_now_wallpaper(self):
        print("Checking wallpaper now...")