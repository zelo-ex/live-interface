from .header import header
from .inner_source import inner_source
from .outer_source import outer_source
from gui.screens import screens
from services.signals import signal_bus
from PySide6.QtWidgets import (QWidget, QVBoxLayout)
from PySide6.QtCore import Slot

class interface:
    def __init__(self, screen: screens):
        self.title_cls = header(screen)
        self.outer_source_cls = outer_source(screen)
        self.inner_source_cls = inner_source(screen)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.title_cls.layout)
        self.layout.addLayout(self.outer_source_cls.layout)
        self.layout.addLayout(self.inner_source_cls.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget.setStyleSheet("background: #000000;")

        signal_bus.event_source.connect(self.event_apply)
        return

    @Slot(str)
    def event_apply(self, event: str):
        if event == "noticeReload":
            self.inner_source_cls.notice_control.notice_label.source_change()
        elif event == "headerReload":
            self.title_cls.update_header()
        return
