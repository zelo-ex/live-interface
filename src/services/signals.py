from PySide6.QtCore import QObject, Signal

class SignalBus(QObject):
    danmaku_source = Signal(str, str)
    music_source = Signal(str, int)

signal_bus = SignalBus()
