import os
from .controls.interface import interface
from .screens import screens
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint)
        return

class GUIDisplay:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.screen = screens(enablePrimaryScreen=True,
                              usePrimaryScreenSize=True)

        self.window = MainWindow()
        self.window.winId()
        self.window.windowHandle().setScreen(self.screen.screen)
        geo = self.screen.screen.availableGeometry()
        self.window.move(geo.x(), geo.y())
        self.window.resize(self.screen.window_size())

    def run(self):
        central = interface(self.screen)
        self.window.setCentralWidget(central.widget)
        self.window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    gui = GUIDisplay()
    gui.run()
