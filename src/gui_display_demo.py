"""
gui_display.py 的演示示例 —— 展示 PySide6 界面的基本写法。

核心三步：
1. 创建 QApplication（整个程序只有一个）
2. 创建 QWidget 窗口，往里面放控件，用布局排列
3. 调用 app.exec() 进入事件循环

运行：python gui_display_demo.py
"""

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class MainWindow(QWidget):
    """主窗口：继承 QWidget 来组织自己的界面"""

    def __init__(self):
        super().__init__()  # 必须先调用父类的 __init__

        # ---- 设置窗口基本属性 ----
        self.setWindowTitle("音乐播放器")
        self.resize(400, 300)

        # ---- 创建控件 ----
        # QLabel 用来显示文字
        self.song_label = QLabel("当前歌曲：无")
        self.song_label.setAlignment(Qt.AlignCenter)  # 文字居中

        # QPushButton 是可点击的按钮
        self.play_btn = QPushButton("▶ 播放")
        self.pause_btn = QPushButton("⏸ 暂停")
        self.next_btn = QPushButton("⏭ 下一首")

        # ---- 用布局排列控件 ----
        # 布局会自动帮你管理控件的位置和大小，不需要手动写坐标

        # 底部按钮用水平布局（从左到右）
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.play_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.next_btn)

        # 整体用垂直布局（从上到下）
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.song_label)
        main_layout.addLayout(btn_layout)  # 把按钮布局嵌套进来

        self.setLayout(main_layout)  # 把布局应用到窗口

        # ---- 连接信号（事件绑定） ----
        # PySide6 用 信号(signal) + 槽(slot) 机制处理交互
        # 按钮.clicked 是信号，.connect(方法) 是绑定处理函数
        self.play_btn.clicked.connect(self.on_play)
        self.pause_btn.clicked.connect(self.on_pause)
        self.next_btn.clicked.connect(self.on_next)

    # ---- 槽函数（事件处理） ----
    def on_play(self):
        self.song_label.setText("状态：▶ 播放中")

    def on_pause(self):
        self.song_label.setText("状态：⏸ 已暂停")

    def on_next(self):
        self.song_label.setText("状态：⏭ 切到下一首")


class GUIApp:
    """应用入口：负责创建 QApplication 和主窗口"""

    def __init__(self):
        # QApplication 必须在所有 Qt 控件之前创建，整个程序只有一个
        self.app = QApplication(sys.argv)
        self.window = MainWindow()

    def run(self):
        self.window.show()  # 显示窗口（默认是隐藏的！）
        sys.exit(self.app.exec())  # 进入事件循环，窗口关闭时退出


if __name__ == "__main__":
    app = GUIApp()
    app.run()
