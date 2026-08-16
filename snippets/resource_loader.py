"""统一资源加载封装：qrc优先，外部文件作为受控兜底。"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from PySide6.QtCore import QFile, QIODevice
    from PySide6.QtGui import QIcon
    from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

    BINDING = "PySide6"
except ImportError:
    from PyQt6.QtCore import QFile, QIODevice
    from PyQt6.QtGui import QIcon
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

    BINDING = "PyQt6"


DEFAULT_EXTERNAL_ROOT = Path(__file__).resolve().parent / "resources"


def resolve_resource(
    path: str, external_root: str | Path | None = None
) -> str:
    """返回可用的qrc标识或绝对外部路径；找不到时给出明确错误。"""
    if path.startswith(":/"):
        if QFile.exists(path):
            return path
        raise FileNotFoundError(f"qrc resource not found: {path}")

    normalized = path.replace("\\", "/").lstrip("/")
    qrc_candidate = f":/{normalized}"
    if QFile.exists(qrc_candidate):
        return qrc_candidate

    root = Path(external_root) if external_root is not None else DEFAULT_EXTERNAL_ROOT
    candidate = (root / normalized).resolve()
    if candidate.is_file():
        return str(candidate)
    raise FileNotFoundError(
        f"resource not found in qrc or external root: {path} ({root})"
    )


def resource_exists(path: str, external_root: str | Path | None = None) -> bool:
    try:
        resolve_resource(path, external_root)
    except FileNotFoundError:
        return False
    return True


def load_stylesheet(
    path: str, external_root: str | Path | None = None
) -> str:
    resolved = resolve_resource(path, external_root)
    if resolved.startswith(":/"):
        file = QFile(resolved)
        mode = QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text
        if not file.open(mode):
            raise OSError(f"unable to open qrc stylesheet: {resolved}")
        try:
            return bytes(file.readAll()).decode("utf-8")
        finally:
            file.close()
    return Path(resolved).read_text(encoding="utf-8")


def load_icon(path: str, external_root: str | Path | None = None) -> QIcon:
    resolved = resolve_resource(path, external_root)
    icon = QIcon(resolved)
    if icon.isNull():
        raise ValueError(f"resource is not a readable icon: {resolved}")
    return icon


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"资源加载示例（{BINDING}）")
        self.resize(640, 420)
        self.setMinimumSize(480, 320)
        self.setCentralWidget(QLabel("使用resolve_resource加载qrc或外部资源。"))


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
