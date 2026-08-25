from collections import deque
from PySide6.QtCore import (QAbstractListModel, QModelIndex,
                            QPersistentModelIndex, Qt, QPoint, QSize, Slot)
from PySide6.QtWidgets import (QAbstractItemView, QListView, QStyledItemDelegate,
                               QStyle, QApplication)
from PySide6.QtGui import (QFont, QTextDocument, QPainter,
                           QMouseEvent, QKeyEvent)
from gui.screens import screens
from typing import Any
from services.signals import signal_bus
import math

danmake_font_size = 10
danmaku_control_margin = 5

class wrap_delegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        if option.widget:
            style = option.widget.style()
        else:
            style = QApplication.style()
        style.drawPrimitive(
            QStyle.PrimitiveElement.PE_PanelItemViewItem,
            option,
            painter,
            option.widget
        )

        text = index.data()
        if not text:
            return

        rect = option.rect

        doc = QTextDocument()
        doc.setPlainText(text)
        doc.setDefaultFont(option.font)
        doc.setTextWidth(rect.width() - danmaku_control_margin * 2)

        painter.save()
        painter.translate(rect.topLeft() +
                          QPoint(danmaku_control_margin, danmaku_control_margin))
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        text = index.data()
        if not text:
            return QSize(0, 0)

        width = option.rect.width()

        if width <= 0 and option.widget:
            viewport = option.widget.viewport()
            if viewport:
                width = viewport.width()
        
        if width <= 0:
            width = 200

        doc = QTextDocument()
        doc.setPlainText(text)
        doc.setTextWidth(width - danmaku_control_margin * 2)

        height = int(doc.size().height()) + danmaku_control_margin * 2
        return QSize(width, height)

class danmaku_list(QAbstractListModel):
    def __init__(self, max_count: int = 20) -> None:
        super().__init__()
        self._items = deque(maxlen=max_count)
        return

    def add(self, danmuke_item: str) -> None:
        if len(self._items) == self._items.maxlen:
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self._items.popleft()
            self.endRemoveRows()
        
        row = len(self._items)
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.append(danmuke_item)
        self.endInsertRows()
        return

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self._items[index.row()]
        return None

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        _ = parent
        return len(self._items)

class danmaku_view(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    
    def mousePressEvent(self, event: QMouseEvent, /) -> None:
        _ = event
        pass
        # return super().mousePressEvent(event)

    def mouseReleaseEvent(self, e: QMouseEvent, /) -> None:
        _ = e
        pass
        # return super().mouseReleaseEvent(e)

    def keyPressEvent(self, event: QKeyEvent, /) -> None:
        _ = event
        pass
        # return super().keyPressEvent(event)

class danmaku_source:
    def __init__(self, screen: screens):
        self.danmaku_count = 0
        self.model = danmaku_list(max_count=10)
        self.widget = danmaku_view()
        self.widget.setModel(self.model)
        self.widget.setItemDelegate(wrap_delegate())
        self.widget.setUniformItemSizes(False)
        self.widget.setStyleSheet("background: #2f2f2f;")
        self.widget.setFont(QFont(
            "Noto Serif", danmake_font_size
        ))
        self.widget.setFixedSize(
            screen.available_size().width() -
            screen.preview_size().width(),
            math.ceil(screen.available_size().height() / 2)
        )
        self.widget.setCurrentIndex(QModelIndex())

        signal_bus.danmaku_source.connect(self.upload_danmaku)
        return

    @Slot(str, str)
    def upload_danmaku(self, user: str, msg: str):
        danmaku = f"{self.danmaku_count + 1} : {user} >> {msg}"
        self.danmaku_count += 1
        self.model.add(danmaku)
        self.widget.scrollToBottom()
        return
