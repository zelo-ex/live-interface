import os
from gui.controls.interface import interface
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow)
from PySide6.QtGui import (QGuiApplication)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint)
        return

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
        central = interface(self.screen)
        self.window.setCentralWidget(central.widget)
        self.window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    gui = GUIDisplay()
    gui.run()
