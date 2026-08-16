from gui.controls.header import header
from gui.controls.innerSource import inner_source
from gui.controls.outerSource import outer_source

from dotenv import load_dotenv
import os
from PySide6.QtCore import (QSize)
from PySide6.QtWidgets import (QWidget, QVBoxLayout)
from PySide6.QtGui import (QGuiApplication, QScreen)

class interface:
    def __init__(self, screen: QScreen):
        primary_screen_size = QGuiApplication.primaryScreen().size()
        
        load_dotenv()
        screen_scale = float(os.getenv("SCREEN_SCALE", default="1.0"))
        preview_height = screen.size().height() - 48
        preview_size = QSize(int(
            float(primary_screen_size.width()) *
            preview_height /
            primary_screen_size.height()),
            preview_height
        )

        title_cls = header(screen)
        outer_source_cls = outer_source(
            preview_size, screen_scale
        )
        inner_source_cls = inner_source(
            preview_size, screen_scale
        )
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_cls.layout)
        main_layout.addLayout(outer_source_cls.layout)
        main_layout.addLayout(inner_source_cls.layout)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.widget = QWidget()
        self.widget.setLayout(main_layout)
        self.widget.setStyleSheet("background: #000000;")
