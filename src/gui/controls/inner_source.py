from .innerSource.music_source import music_source
from music.music_player import music_player
from .innerSource.notice_source import notice_source
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout
from gui.screens import screens

        
"""内部源层（公告、音乐等）"""
class inner_source:
    def __init__(self, screen: screens):
        self.music_control = music_source(screen)
        self.notice_control = notice_source(screen)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.music_control.widget)
        self.layout.addWidget(self.notice_control.widget)
        self.layout.setAlignment(
            self.music_control.widget, Qt.AlignmentFlag.AlignBottom
        )
        self.layout.setAlignment(
            self.notice_control.widget, Qt.AlignmentFlag.AlignBottom
        )
        
        self.music = music_player(self.music_control)
        # self.music.setSourceAndPlay()

        return
