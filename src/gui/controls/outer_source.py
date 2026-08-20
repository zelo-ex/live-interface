from .outerSource.preview_source import preview_source
from .outerSource.danmaku_source import danmaku_source
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from gui.screens import screens

"""外部源层（OBS截流、弹幕拉取等）"""
class outer_source:
    def __init__(self, screen: screens):
        self.preview = preview_source(screen)
        self.danmake = danmaku_source(screen)
        
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.preview.widget)
        self.layout.addWidget(self.danmake.widget)
        self.layout.setAlignment(
            self.preview.widget, Qt.AlignmentFlag.AlignTop
        )
        self.layout.setAlignment(
            self.danmake.widget, Qt.AlignmentFlag.AlignTop
        )
