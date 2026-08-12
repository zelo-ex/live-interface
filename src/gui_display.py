from dotenv import load_dotenv
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
import math
from PySide6.QtCore import (Qt, QSize)
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel,
                               QWidget, QVBoxLayout, QHBoxLayout,
                               QListWidget, QProgressBar, QStatusBar)
from PySide6.QtGui import (QGuiApplication, QFont, QScreen)

def pt_to_px(pt: float, screen: QScreen) -> float:
    dpi = screen.logicalDotsPerInch()
    return pt * (dpi / 72.0)

def px_to_pt(px: float, screen: QScreen) -> float:
    dpi = screen.logicalDotsPerInch()
    return px / (dpi / 72.0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint)

    def interface_init(self):
        primary_screen_size = QGuiApplication.primaryScreen().size()
        source_size = self.window().size()
        source_size.setHeight(source_size.height() - 30)
        load_dotenv()
        screen_scale = float(os.getenv("SCREEN_SCALE", default="1.0"))

        # 头部源层（直播标题、日期时间、延迟等）
        title_label = QLabel("Title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFixedHeight(30)
        title_label.setFont(QFont(
            "Noto Serif", int(px_to_pt(25, self.screen())),
            QFont.Weight.Bold, True
        ))

        title_layout = QHBoxLayout()
        title_layout.addWidget(title_label)

        # 外部源层（OBS截流、弹幕拉取等）
        preview_size = QSize(int(
            float(primary_screen_size.width()) *
            source_size.height() /
            primary_screen_size.height()),
            source_size.height()
        )
        preview = QLabel("Screen Video Stream Closed")
        preview.setStyleSheet("background: #2f2f2f;")
        preview.setFixedSize(
            math.ceil(screen_scale * float(preview_size.width())),
            math.ceil(screen_scale * float(preview_size.height()))
        )
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview.setFont(QFont(
            "Noto Serif", 30, QFont.Weight.Bold, True
        ))
        
        danmaku_list = QListWidget()
        danmaku_list.setStyleSheet("background: #7f7f7f;")
        danmaku_list.setFixedHeight(
            math.ceil(screen_scale * float(source_size.height()))
        )
        
        outer_source_layout = QHBoxLayout()
        outer_source_layout.addWidget(preview)
        outer_source_layout.addWidget(danmaku_list)
        outer_source_layout.setAlignment(
            preview, Qt.AlignmentFlag.AlignTop
        )
        outer_source_layout.setAlignment(
            danmaku_list, Qt.AlignmentFlag.AlignTop
        )

        # 内部源层（公告、音乐等）
        music_progress = QProgressBar()
        music_progress.setStyleSheet("background: #2f2f2f;")
        music_progress.setRange(0, 100)
        music_progress.setValue(50)

        music_status_tab = QStatusBar()
        music_status_duration = QLabel("Duration: 00:00/00:00")
        music_status_title = QLabel(
            "Title: a music title"
        )
        music_status_tab.addWidget(music_status_duration)
        music_status_tab.addWidget(music_status_title)
        
        music_layout = QVBoxLayout()
        music_layout.addWidget(music_progress)
        music_layout.addWidget(music_status_tab)
        music_layout.setAlignment(
            music_progress,
            Qt.AlignmentFlag.AlignBottom
        )
        music_layout.setAlignment(
            music_status_tab,
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )
        
        music_widget = QWidget()
        music_widget.setLayout(music_layout)
        music_widget.setStyleSheet("background: #1f1f1f;")
        
        notice_label = QLabel("Notice\r\nhelloworld")
        notice_label.setFixedWidth(
            math.ceil(screen_scale * float(preview_size.width()))
        )

        inner_source_layout = QHBoxLayout()
        inner_source_layout.addWidget(music_widget)
        inner_source_layout.addWidget(notice_label)
        inner_source_layout.setAlignment(
            notice_label,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(title_layout)
        main_layout.addLayout(outer_source_layout)
        main_layout.addLayout(inner_source_layout)
        
        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)
        central.setStyleSheet("background: #000000;")


class GUIDisplay:
    def __init__(self):
        self.app = QApplication(sys.argv)
        screens = QApplication.screens()

        non_primary = []
        primary_screen = QGuiApplication.primaryScreen()
        for s in screens:
            if s.serialNumber != primary_screen.serialNumber:
                non_primary.append(s)
        
        # if non_primary:
        #     self.screen = non_primary[0]
        # else:
            self.screen = screens[0]

        self.window = MainWindow()
        self.window.winId()
        self.window.windowHandle().setScreen(self.screen)
        geo = self.screen.availableGeometry()
        self.window.move(geo.x(), geo.y())
        self.window.resize(geo.width(), geo.height())

    def run(self):
        self.window.interface_init()
        self.window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    gui = GUIDisplay()
    gui.run()
