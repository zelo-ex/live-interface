import gui.screens as screens
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QHBoxLayout)
from PySide6.QtGui import (QFont, QScreen)

"""头部源层（直播标题、日期时间、延迟等）"""
class header:
    def __init__(self, screen: QScreen):
        title_label = QLabel("Title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFixedHeight(30)
        title_label.setFont(QFont(
            "Noto Serif",
            int(screens.px_to_pt(25, screen)),
            QFont.Weight.Bold, True))

        self.layout = QHBoxLayout()
        self.layout.addWidget(title_label)
