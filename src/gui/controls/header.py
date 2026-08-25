from dotenv import dotenv_values

from gui.screens import screens
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QHBoxLayout)
from PySide6.QtGui import QFont
import os

"""头部源层（直播标题、日期时间、延迟等）"""
class header:
    def __init__(self, screen: screens):
        header_height = int(os.getenv("HEADER_HEIGHT", default="30"))
        header_content = os.getenv("HEADER_CONTENT", "title")
        self.widget = QLabel(header_content)
        self.widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget.setFixedHeight(header_height)
        self.widget.setFont(QFont(
            "Noto Serif",
            int(screen.px_to_pt(header_height * 0.8)),
            QFont.Weight.Bold, True))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.widget)

    def update_header(self):
        latest_dict = dotenv_values(".env")
        header_content = latest_dict.get("HEADER_CONTENT")
        if header_content is None:
            header_content = "title"
        self.widget.setText(header_content)
        print(header_content)
