import math
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtWidgets import (QLabel,QHBoxLayout, QListWidget)
from PySide6.QtGui import QFont

"""外部源层（OBS截流、弹幕拉取等）"""
class outer_source:
    def __init__(self, preview_size: QSize, screen_scale: float):
        preview = QLabel("Screen Video Stream Closed")
        preview.setStyleSheet("background: #2f2f2f;")
        preview.setFixedSize(
            math.ceil(screen_scale * float(preview_size.width())),
            math.ceil(screen_scale * float(preview_size.height()))
        )
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview.setFont(QFont(
            "Noto Serif", 30, QFont.Weight.Bold, True
        ))
        
        danmaku_list = QListWidget()
        danmaku_list.setStyleSheet("background: #7f7f7f;")
        danmaku_list.setFixedSize(
            math.ceil(preview_size.width() -
                      screen_scale * float(preview_size.width())),
            math.ceil(screen_scale * float(preview_size.height()))
        )
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(preview)
        self.layout.addWidget(danmaku_list)
        self.layout.setAlignment(
            preview, Qt.AlignmentFlag.AlignTop
        )
        self.layout.setAlignment(
            danmaku_list, Qt.AlignmentFlag.AlignTop
        )
