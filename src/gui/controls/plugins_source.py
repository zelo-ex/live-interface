from .pluginsSource.music_source import music_source
from .pluginsSource.notice_source import notice_source
from .pluginsSource.danmaku_source import danmaku_source
from music.music_player import music_player
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout
from gui.screens import screens

        
"""内部源层（公告、音乐等）"""
class plugins_source:
    def __init__(self, screen: screens):
        self.notice_control = notice_source(screen)
        self.music_control = music_source(screen)
        self.danmaku_source = danmaku_source(screen)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.notice_control.widget)
        self.layout.addWidget(self.music_control.widget)
        self.layout.addWidget(self.danmaku_source.widget)
        self.layout.setAlignment(
            self.notice_control.widget, Qt.AlignmentFlag.AlignTop
        )
        self.layout.setAlignment(
            self.music_control.widget, Qt.AlignmentFlag.AlignTop
        )
        self.layout.setAlignment(
            self.danmaku_source.widget, Qt.AlignmentFlag.AlignTop
        )
        
        self.music = music_player(self.music_control)
        self.music.setSourceAndPlay()

        return
