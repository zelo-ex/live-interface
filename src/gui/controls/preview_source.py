from PySide6.QtMultimedia import QScreenCapture, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
from gui.screens import screens
from PySide6.QtWidgets import (QStackedWidget, QVBoxLayout, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class preview_source:
    def __init__(self, screen: screens):
        self.showPreview = True
        
        self.capture = QScreenCapture()
        self.capture.setScreen(screen.primary_screen)
        self.capture.setActive(True)

        self.session = QMediaCaptureSession()
        self.session.setScreenCapture(self.capture)

        self.widget_video = QVideoWidget()
        self.session.setVideoOutput(self.widget_video)
        self.widget_video.setFixedSize(screen.preview_size())
        self.widget_video.setStyleSheet("background: #2f2f2f;")
        
        self.widget_preview = QLabel("Screen Video Stream Closed")
        self.widget_preview.setFixedSize(screen.preview_size())
        self.widget_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget_preview.setFont(QFont(
            "Noto Serif", 30, QFont.Weight.Bold, True
        ))

        self.scenes = QStackedWidget()
        self.scenes.addWidget(self.widget_video)
        self.scenes.addWidget(self.widget_preview)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scenes)
        self.layout.setAlignment(
            self.widget_preview, Qt.AlignmentFlag.AlignTop
        )
        
        return

    def switch_scene(self) -> None:
        if self.showPreview:
            self.scenes.setCurrentIndex(1)
            self.capture.setActive(False)
        else:
            self.capture.setActive(True)
            self.scenes.setCurrentIndex(0)
        self.showPreview = not self.showPreview
        return
