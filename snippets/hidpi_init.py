"""PySide6/PyQt6通用的Qt 6 Hi-DPI应用入口模板。"""

from __future__ import annotations

import sys

try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

    BINDING = "PySide6"
except ImportError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QGuiApplication
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

    BINDING = "PyQt6"


def create_application(argv: list[str]) -> QApplication:
    """在创建QApplication前确定小数缩放策略。"""
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(argv)
    app.setApplicationName("HiDPI Widget Demo")
    return app


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Hi-DPI初始化示例（{BINDING}）")
        # Qt Widget几何使用逻辑像素；布局仍可随字体和屏幕缩放伸缩。
        self.resize(960, 640)
        self.setMinimumSize(640, 420)
        self.setCentralWidget(QLabel("Qt 6会自动执行High-DPI缩放。"))


def main() -> int:
    app = create_application(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
