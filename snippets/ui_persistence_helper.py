"""QSettings封装：保存窗口、Dock、Splitter、表头和主题状态。"""

from __future__ import annotations

import sys

try:
    from PySide6.QtCore import QSettings, Qt
    from PySide6.QtGui import QCloseEvent
    from PySide6.QtWidgets import (
        QApplication,
        QDockWidget,
        QHeaderView,
        QLabel,
        QMainWindow,
        QPushButton,
        QSplitter,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    BINDING = "PySide6"
except ImportError:
    from PyQt6.QtCore import QSettings, Qt
    from PyQt6.QtGui import QCloseEvent
    from PyQt6.QtWidgets import (
        QApplication,
        QDockWidget,
        QHeaderView,
        QLabel,
        QMainWindow,
        QPushButton,
        QSplitter,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    BINDING = "PyQt6"


class UiStateStore:
    def __init__(
        self, organization: str, application: str, version: int = 1
    ) -> None:
        self.settings = QSettings(organization, application)
        self.version = version
        self.prefix = f"ui/v{version}"

    def _key(self, suffix: str) -> str:
        return f"{self.prefix}/{suffix}"

    def save_main_window(self, window: QMainWindow) -> None:
        self.settings.setValue(self._key("window/geometry"), window.saveGeometry())
        self.settings.setValue(
            self._key("window/state"), window.saveState(self.version)
        )

    def restore_main_window(self, window: QMainWindow) -> bool:
        geometry = self.settings.value(self._key("window/geometry"))
        state = self.settings.value(self._key("window/state"))
        geometry_ok = geometry is not None and window.restoreGeometry(geometry)
        state_ok = state is not None and window.restoreState(state, self.version)
        return bool(geometry_ok and state_ok)

    def save_splitter(self, name: str, splitter: QSplitter) -> None:
        self.settings.setValue(self._key(f"splitter/{name}"), splitter.saveState())

    def restore_splitter(self, name: str, splitter: QSplitter) -> bool:
        state = self.settings.value(self._key(f"splitter/{name}"))
        return bool(state is not None and splitter.restoreState(state))

    def save_header(self, name: str, header: QHeaderView) -> None:
        self.settings.setValue(self._key(f"header/{name}"), header.saveState())

    def restore_header(self, name: str, header: QHeaderView) -> bool:
        state = self.settings.value(self._key(f"header/{name}"))
        return bool(state is not None and header.restoreState(state))

    def set_theme(self, theme: str) -> None:
        self.settings.setValue(self._key("theme"), theme)

    def theme(self, default: str = "light") -> str:
        return str(self.settings.value(self._key("theme"), default))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"UI状态持久化示例（{BINDING}）")
        self.resize(960, 640)
        self.setMinimumSize(640, 420)
        self.state_store = UiStateStore("QtUiEngineering", "UiPersistenceDemo")
        self._theme = self.state_store.theme()

        self.splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.splitter.addWidget(QTextEdit("主要工作区", self.splitter))
        self.splitter.addWidget(QTextEdit("检查器", self.splitter))
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        theme_button = QPushButton("切换明暗主题", self)
        theme_button.clicked.connect(self.toggle_theme)
        content = QWidget(self)
        layout = QVBoxLayout(content)
        layout.addWidget(theme_button)
        layout.addWidget(self.splitter)
        self.setCentralWidget(content)

        dock = QDockWidget("输出", self)
        dock.setObjectName("outputDock")
        dock.setWidget(QLabel("Dock布局会随主窗口状态保存。", dock))
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

        self.apply_theme()
        self.state_store.restore_main_window(self)
        self.state_store.restore_splitter("workspace", self.splitter)

    def toggle_theme(self) -> None:
        self._theme = "dark" if self._theme == "light" else "light"
        self.state_store.set_theme(self._theme)
        self.apply_theme()

    def apply_theme(self) -> None:
        if self._theme == "dark":
            self.setStyleSheet("QWidget { color: #f4f4f4; background: #202124; }")
        else:
            self.setStyleSheet("")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.state_store.save_main_window(self)
        self.state_store.save_splitter("workspace", self.splitter)
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
