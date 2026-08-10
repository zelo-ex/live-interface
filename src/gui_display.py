import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow,
                               QWidget, QVBoxLayout, QHBoxLayout)
from PySide6.QtGui import QGuiApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        # central = QWidget()
        # layout = QVBoxLayout()
        # label = QLabel("Hello World")
        # layout.addWidget(label)
        # central.setLayout(layout)
        # self.setCentralWidget(central)
        # self.statusBar().showMessage("就绪")
        central = QWidget()

        # 内部源层（公告、音乐等）
        inner_source_layout = QHBoxLayout()

        # 外部源层（OBS截流、弹幕拉取等）
        outer_source_layout = QHBoxLayout()
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(inner_source_layout)
        main_layout.addLayout(outer_source_layout)
        central.setLayout(main_layout)
        self.setCentralWidget(central)


class GUIDisplay:
    def __init__(self):
        self.app = QApplication(sys.argv)
        screens = QApplication.screens()

        non_primary = []
        for s in screens:
            if s.serialNumber != QGuiApplication.primaryScreen().serialNumber:
                non_primary.append(s)
        
        if non_primary:
            self.screen = non_primary[0]
        else:
            self.screen = screens[0]

        self.window = MainWindow()
        self.window.winId()
        self.window.windowHandle().setScreen(self.screen)
        geo = self.screen.availableGeometry()
        self.window.move(geo.x(), geo.y())
        self.window.resize(geo.width(), geo.height())

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    gui = GUIDisplay()
    gui.run()
