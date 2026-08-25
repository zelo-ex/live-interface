from typing import List

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication
import os
import math

class screens:
    def __init__(self, enablePrimaryScreen: bool,
                 usePrimaryScreenSize: bool):
        self.radioViewerSize: List[float] = [16.0, 9.0]
        
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

    # 主屏幕标准大小
    def standard_size(self) -> QSize:
        return QGuiApplication.primaryScreen().size()

    # 直播界面窗口大小
    def window_size(self) -> QSize:
        size = QSize()
        if self.usePrimaryScreenSize:
            size = self.standard_size()
        else:
            size = self.screen.size()
        # size.setWidth(
        #     math.ceil(size.height() /
        #         self.radioViewerSize[1] *
        #         self.radioViewerSize[0])
        # )
        size.setHeight(
            math.ceil(size.width() /
                      self.radioViewerSize[0] *
                      self.radioViewerSize[1])
        )
        return size

    # 窗口可用大小（排除标题栏的可用空间）
    def available_size(self) -> QSize:
        header_height = int(os.getenv("HEADER_HEIGHT", default="30"))
        window_size = self.window_size()
        return QSize (
            window_size.width(),
            window_size.height() - header_height
        )

    def preview_size(self) -> QSize:
        scale = self.available_size().height() / self.standard_size().height()
        return QSize(
            math.ceil(self.standard_size().width() * scale),
            math.ceil(self.standard_size().height() * scale)
        )

    def pt_to_px(self, pt: float) -> float:
        dpi = self.screen.logicalDotsPerInch()
        return pt * (dpi / 72.0)

    def px_to_pt(self, px: float) -> float:
        dpi = self.screen.logicalDotsPerInch()
        return px / (dpi / 72.0)
