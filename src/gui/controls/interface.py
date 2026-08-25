from .header import header
from .preview_source import preview_source
from .plugins_source import plugins_source
from gui.screens import screens
from services.signals import signal_bus
from PySide6.QtWidgets import (QHBoxLayout, QWidget, QVBoxLayout)
from PySide6.QtCore import Slot

class interface:
    def __init__(self, screen: screens):
        self.title_cls = header(screen)
        self.preview_cls = preview_source(screen)
        self.plugins_cls = plugins_source(screen)
        
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.title_cls.layout)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.preview_cls.layout)
        self.mainLayout.addLayout(self.plugins_cls.layout)
        self.layout.addLayout(self.mainLayout)
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
            self.plugins_cls.notice_control.notice_label.load_source()
            self.plugins_cls.notice_control.notice_label.source_change()
        elif event == "headerReload":
            self.title_cls.update_header()
        elif event == "switchScene":
            self.preview_cls.switch_scene()
        return
