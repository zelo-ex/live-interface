from PySide6.QtWidgets import QListWidget
from gui.screens import screens

class danmaku_source:
    def __init__(self, screen: screens):
        self.widget = QListWidget()
        self.widget.setStyleSheet("background: #2f2f2f;")
        self.widget.setFixedSize(
            screen.available_size().width() -
            screen.preview_size().width(),
            screen.preview_size().height()
        )
