from gui.screens import screens
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QHBoxLayout)
from PySide6.QtGui import QFont
import os

"""头部源层（直播标题、日期时间、延迟等）"""
class header:
    def __init__(self, screen: screens):
        header_height = int(os.getenv("HEADER_HEIGHT", default="30"))
        self.widget = QLabel("Title")
        self.widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget.setFixedHeight(header_height)
        self.widget.setFont(QFont(
            "Noto Serif",
            int(screen.px_to_pt(header_height * 0.8)),
            QFont.Weight.Bold, True))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.widget)
