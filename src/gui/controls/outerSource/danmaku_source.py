from collections import deque
from PySide6.QtCore import (QAbstractListModel, QModelIndex,
                            QPersistentModelIndex, Qt, QPoint, QSize, Slot)
from PySide6.QtWidgets import (QListView, QStyledItemDelegate,
                               QStyle, QApplication)
from PySide6.QtGui import (QFont, QTextDocument, QPainter)
from gui.screens import screens
from typing import Any
from services.signals import signal_bus

danmake_font_size = 12

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

        margin = 10
        rect = option.rect

        doc = QTextDocument()
        doc.setPlainText(text)
        doc.setDefaultFont(option.font)
        doc.setTextWidth(rect.width() - margin * 2)

        painter.save()
        painter.translate(rect.topLeft() + QPoint(margin, margin))
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        text = index.data()
        if not text:
            return QSize(0, 0)

        margin = 10
        width = option.rect.width()

        if width <= 0 and option.widget:
            viewport = option.widget.viewport()
            if viewport:
                width = viewport.width()
        
        if width <= 0:
            width = 200

        doc = QTextDocument()
        doc.setPlainText(text)
        doc.setTextWidth(width - margin * 2)

        height = int(doc.size().height()) + margin * 2
        return QSize(width, max(30, height))

class danmaku_list(QAbstractListModel):
    def __init__(self, max_count: int = 50) -> None:
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

class danmaku_source:
    def __init__(self, screen: screens):
        self.danmaku_count = 0
        self.model = danmaku_list(max_count=20)
        self.widget = QListView()
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
            screen.preview_size().height()
        )

        signal_bus.danmaku_source.connect(self.upload_danmaku)
        return

    @Slot(str, str)
    def upload_danmaku(self, user: str, msg: str):
        global danmaku_count
        danmaku = f"{self.danmaku_count + 1} : {user} >> {msg}"
        self.danmaku_count += 1
        self.model.add(danmaku)
        self.widget.scrollToBottom()
        return
