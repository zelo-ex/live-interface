from music.playlist import playlist
import math
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtWidgets import (QLabel, QWidget, QVBoxLayout,
                               QHBoxLayout, QProgressBar, QStatusBar)

class progress_bar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: #2f2f2f;")
        self.setRange(0, 100)
        self.setValue(50)
        

class status_bar(QStatusBar):
    def __init__(self, song: str):
        super().__init__()
        music_status_duration = QLabel("Duration: 00:00/00:00")
        music_status_title = QLabel(
            f"Title: {song}"
        )
        self.addWidget(music_status_duration)
        self.addWidget(music_status_title)
        

class music_source:
    def __init__(self, preview_size: QSize,
                 screen_scale: float):
        self.playlist = playlist()
        now_song = self.playlist.now_song()[0]
        
        self.progressBar = progress_bar()
        self.statusTab = status_bar(now_song)
        
        layout = QVBoxLayout()
        layout.addWidget(self.progressBar)
        layout.addWidget(self.statusTab)
        layout.setAlignment(
            self.progressBar,
            Qt.AlignmentFlag.AlignBottom
        )
        layout.setAlignment(
            self.statusTab,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )
        
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.widget.setStyleSheet("background: #1f1f1f;")
        self.widget.setFixedSize(
            math.ceil(preview_size.width() / 2),
            math.ceil(preview_size.height() -
                      screen_scale * float(preview_size.height()))
        )


class notice_source:
    def __init__(self, preview_size: QSize,
                 screen_scale: float, notices: str):
        notice_label = QLabel(notices)
        notice_label.setFixedSize(
            math.ceil(preview_size.width() / 2),
            math.ceil(preview_size.height() -
                      screen_scale * float(preview_size.height()))
        )
        self.widget = notice_label
        self.widget.setStyleSheet("background: #1f1f1f;")
        
        
"""内部源层（公告、音乐等）"""
class inner_source:
    def __init__(self, preview_size: QSize,
                 screen_scale: float):
        music_control = music_source(
            preview_size, screen_scale)
        notice_control = notice_source(
            preview_size, screen_scale,
            "Notice\r\nThis is a notice...")

        self.layout = QHBoxLayout()
        self.layout.addWidget(music_control.widget)
        self.layout.addWidget(notice_control.widget)
        self.layout.setAlignment(
            music_control.widget, Qt.AlignmentFlag.AlignBottom
        )
        self.layout.setAlignment(
            notice_control.widget, Qt.AlignmentFlag.AlignBottom
        )
        
