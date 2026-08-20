from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication
import os
import math

class screens:
    def __init__(self, enablePrimaryScreen: bool,
                 usePrimaryScreenSize: bool):
        self.screens = QApplication.screens()
        self.usePrimaryScreenSize = usePrimaryScreenSize

        self.non_primary = []
        self.primary_screen = QGuiApplication.primaryScreen()
        for s in self.screens:
            if s.serialNumber != self.primary_screen.serialNumber:
                self.non_primary.append(s)
        
        if (not enablePrimaryScreen) and len(self.non_primary):
            self.screen = self.non_primary[0]
        else:
            self.screen = self.screens[0]
        return

    def standard_size(self) -> QSize:
        return QGuiApplication.primaryScreen().size()

    def window_size(self) -> QSize:
        if self.usePrimaryScreenSize:
            return self.standard_size()
        return self.screen.size()

    def available_size(self) -> QSize:
        header_height = int(os.getenv("HEADER_HEIGHT", default="30"))
        window_size = self.window_size()
        return QSize (
            window_size.width(),
            window_size.height() - header_height
        )

    def preview_size(self) -> QSize:
        screen_scale = float(os.getenv("SCREEN_SCALE", default="1.0"))
        standard_size = self.standard_size()
        return QSize (
            math.ceil(screen_scale * standard_size.width()),
            math.ceil(screen_scale * standard_size.height())
        )

    def pt_to_px(self, pt: float) -> float:
        dpi = self.screen.logicalDotsPerInch()
        return pt * (dpi / 72.0)

    def px_to_pt(self, px: float) -> float:
        dpi = self.screen.logicalDotsPerInch()
        return px / (dpi / 72.0)
