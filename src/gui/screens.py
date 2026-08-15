from PySide6.QtGui import QScreen

def pt_to_px(pt: float, screen: QScreen) -> float:
    dpi = screen.logicalDotsPerInch()
    return pt * (dpi / 72.0)

def px_to_pt(px: float, screen: QScreen) -> float:
    dpi = screen.logicalDotsPerInch()
    return px / (dpi / 72.0)
