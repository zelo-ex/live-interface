from PySide6.QtCore import QObject, Signal

class SignalBus(QObject):
    danmaku_source = Signal(str, str)
    music_source = Signal(str, int)
    event_source = Signal(str)

signal_bus = SignalBus()
