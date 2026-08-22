import math
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QFrame
from PySide6.QtGui import QFont
from gui.screens import screens

notice_title_font_size = 24
notice_label_font_size = 18

class notice_title:
    def __init__(self, screen: screens):
        self.widget = QLabel("Notice")
        self.widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.widget.setFixedHeight(
            int(notice_title_font_size * 1.5))
        self.widget.setFont(QFont(
            "Noto Serif",
            int(screen.px_to_pt(notice_title_font_size))))
        return


class notice_label:
    def __init__(self, screen: screens):
        self.source_change()
        
        self.widget = QLabel(self.file_data)
        self.widget.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.widget.setFont(QFont(
            "Noto Serif",
            int(screen.px_to_pt(notice_label_font_size))))
        return

    def source_change(self) -> None:
        self.file_path = os.getenv("NOTICE_FILE", "notice.txt")
        with open(self.file_path, mode="r") as file:
            self.file_data = file.read()
        return

class notice_source:
    def __init__(self, screen: screens):
        self.notice_title = notice_title(screen)
        self.notice_label = notice_label(screen)

        self.splitter = QFrame()
        self.splitter.setFrameShape(QFrame.Shape.HLine)
        self.splitter.setStyleSheet("color: #6f6f6f;")
        self.splitter.setLineWidth(2)
        
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.notice_title.widget)
        self.layout.addWidget(self.splitter)
        self.layout.addWidget(self.notice_label.widget)
        
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget.setStyleSheet("background: #1f1f1f;")
        self.widget.setFixedSize(
            math.ceil(screen.available_size().width() / 2),
            math.ceil(screen.available_size().height() -
                      screen.preview_size().height())
        )
