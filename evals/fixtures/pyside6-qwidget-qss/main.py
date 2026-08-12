from pathlib import Path

from PySide6.QtWidgets import QApplication, QSplitter


app = QApplication([])
splitter = QSplitter()
splitter.setStyleSheet(Path("theme.qss").read_text(encoding="utf-8"))
