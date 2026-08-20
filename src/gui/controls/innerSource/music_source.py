from music.playlist import playlist
from gui.screens import screens
import math
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QLabel, QWidget, QVBoxLayout,
                               QSlider, QStatusBar)
from PySide6.QtMultimedia import QMediaPlayer

class slide_bar(QSlider):
    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)
        self.setFixedHeight(50)
        self.setRange(0, 100)
        self.setValue(50)
        self.setStyleSheet("""
        QSlider {
        background: transparent;
        }
        QSlider::sub-page:horizonal {
        border: 1px solid #bbb;
        height: 10px;
        background: #0078d7;
        border-radius: 5px;
        margin: 2px 0;
        }
        QSlider::groove:horizontal {
        border: 1px solid #bbb;
        height: 10px;
        background: #2f2f2f;
        border-radius: 5px;
        margin: 2px 0;
        }
        QSlider::handle:horizontal {
        background: #ffffff;
        border: 1px solid #5c5c5c;
        width: 18px;
        height: 18px;
        margin: -5px 0;
        border-radius: 9px;
        }
        """)
        return

    def set_progress(self, progress: list[int]):
        self.setRange(0, progress[1])
        self.setValue(progress[0])
        return
        

class status_bar(QStatusBar):
    def __init__(self):
        super().__init__()
        self._duration = QLabel()
        self._status = QLabel()
        self._title = QLabel()
        self.addWidget(self._duration, stretch=1)
        self.addWidget(self._status, stretch=1)
        self.addWidget(self._title, stretch=3)
        return

    def set_progress(self, progress):
        # QMediaPlayer 传入的是毫秒，先换算成秒再格式化
        pos_sec = progress[0] // 1000
        dur_sec = progress[1] // 1000
        label1 = [pos_sec // 60, pos_sec % 60]
        label2 = [dur_sec // 60, dur_sec % 60]
        self._duration.setText(
            f"Duration: {label1[0]}:{label1[1]:02d} / "
            f"{label2[0]}:{label2[1]:02d}"
        )
        return

    def set_song_info(self, info: list[str]):
        self._title.setText(
            f"Now: {info[0]} - {info[1]}"
        )
        return

class music_source:
    def __init__(self, screen: screens):
        self.progressBar = slide_bar()
        self.statusTab = status_bar()
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.statusTab)
        self.layout.setAlignment(
            self.progressBar,
            Qt.AlignmentFlag.AlignBottom
        )
        self.layout.setAlignment(
            self.statusTab,
            Qt.AlignmentFlag.AlignBottom
        )
        
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget.setStyleSheet("background: #1f1f1f;")
        self.widget.setFixedSize(
            math.ceil(screen.available_size().width() / 2),
            screen.available_size().height() -
            screen.preview_size().height()
        )
        
        self.init_source()
        return

    # 初始化音乐播放器相关状态
    def init_source(self):
        self.source_progress = [0, 100]
        self.source_info = ["", ""]
        self.playlist = playlist()
        # 立即显示当前歌曲信息，而不是等音频加载成功后才显示
        self.update_source()
        self.update_position(self.source_progress[0])
        self.update_duration(self.source_progress[1])
        self.update_audio_status(
            QMediaPlayer.MediaStatus.LoadingMedia)
        return

    # 加载音乐信息
    def update_source(self):
        self.source_info[0] = self.playlist.now_song()[0]
        self.source_info[1] = self.playlist.now_composer()[0]
        self.statusTab.set_song_info(self.source_info)
        return

    def update_position(self, position: int):
        self.source_progress[0] = position
        self.statusTab.set_progress(self.source_progress)
        self.progressBar.set_progress(self.source_progress)
        return

    def update_duration(self, duration: int):
        self.source_progress[0] = 0
        self.source_progress[1] = duration
        self.statusTab.set_progress(self.source_progress)
        self.progressBar.set_progress(self.source_progress)
        self.update_source()
        return

    def update_audio_status(self, status: QMediaPlayer.MediaStatus):
        status_map = {
            QMediaPlayer.MediaStatus.NoMedia: "No Media",
            QMediaPlayer.MediaStatus.LoadingMedia: "Loading...",
            QMediaPlayer.MediaStatus.LoadedMedia: "Loaded",
            QMediaPlayer.MediaStatus.StalledMedia: "Stalled",
            QMediaPlayer.MediaStatus.BufferingMedia: "Buffering...",
            QMediaPlayer.MediaStatus.BufferedMedia: "Buffered",
            QMediaPlayer.MediaStatus.EndOfMedia: "End Of Media",
            QMediaPlayer.MediaStatus.InvalidMedia: "Invalid Media"
        }
        self.statusTab._status.setText(
            status_map.get(status, "Unknown")
        )
