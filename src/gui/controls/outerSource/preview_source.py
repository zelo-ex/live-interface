from PySide6.QtMultimedia import QScreenCapture, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
from gui.screens import screens

class preview_source:
    def __init__(self, screen: screens):
        # self.widget = QLabel("Screen Video Stream Closed")
        self.capture = QScreenCapture()
        self.capture.setScreen(screen.primary_screen)
        self.capture.setActive(True)

        self.session = QMediaCaptureSession()
        self.session.setScreenCapture(self.capture)

        self.widget = QVideoWidget()
        self.session.setVideoOutput(self.widget)
        self.widget.setFixedSize(screen.preview_size())
        self.widget.setStyleSheet("background: #2f2f2f;")
        # self.widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.widget.setFont(QFont(
        #     "Noto Serif", 30, QFont.Weight.Bold, True
        # ))
        
        return
