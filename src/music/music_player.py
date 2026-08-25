from PySide6.QtCore import QUrl, Slot
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from gui.controls.pluginsSource.music_source import music_source
from services.signals import signal_bus

class music_player:
    def __init__(self, audio_widget: music_source):
        self.widget = audio_widget
        # QMediaPlayer / QAudioOutput 必须挂到 QWidget 上，
        # 否则这个 music_player 对象一旦被 GC，播放器就会被销毁，
        # 歌曲会永远停在 Loading 状态
        self.player = QMediaPlayer(self.widget.widget)
        self.audio_output = QAudioOutput(self.widget.widget)
        self.player.setAudioOutput(self.audio_output)

        # 连续加载失败的次数，用于避免全部歌曲都加载失败时死循环
        self._consecutive_errors = 0

        self.player.positionChanged.connect(
            self.widget.update_position)
        self.player.durationChanged.connect(
            self.widget.update_duration)
        self.player.mediaStatusChanged.connect(
            self.update_media_status)
        self.player.errorOccurred.connect(
            self.handle_error)

        signal_bus.music_source.connect(self.parse_signal)

        return

    def update_media_status(self, status: QMediaPlayer.MediaStatus):
        # 一旦有歌曲加载成功，就重置连续失败计数
        if status in (
                QMediaPlayer.MediaStatus.LoadedMedia,
                QMediaPlayer.MediaStatus.BufferingMedia,
                QMediaPlayer.MediaStatus.BufferedMedia):
            self._consecutive_errors = 0
        self.widget.update_audio_status(status)
        if status is QMediaPlayer.MediaStatus.EndOfMedia:
            self.widget.playlist.move(1)
            self.setSourceAndPlay()

    def handle_error(self, error, error_string):
        print(f"Media error: {error} - {error_string}")
        total = self.widget.playlist.now_playlist()[1]
        if total <= 1:
            return
        self._consecutive_errors += 1
        if self._consecutive_errors >= total:
            print("All songs failed to load, giving up.")
            return
        # 当前文件加载失败（如文件缺失），自动跳到下一首
        self.widget.playlist.move(1)
        self.setSourceAndPlay()

    def setSourceAndPlay(self):
        filename = self.widget.playlist.now_filename()[0]
        self.player.setSource(QUrl.fromLocalFile(filename))
        print(filename)
        self.player.play()

    @Slot(str, int)
    def parse_signal(self, command: str, offset: int) -> None:
        if (command == "prev"):
            self.widget.playlist.move(-offset)
            self.setSourceAndPlay()
        elif (command == "next"):
            self.widget.playlist.move(offset)
            self.setSourceAndPlay()
        elif (command == "play"): self.player.play()
        elif (command == "pause"): self.player.pause()
        elif (command == "restart"): self.player.setPosition(0)
        else: print("error occur")
        return
