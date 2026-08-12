from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMainWindow


app = QApplication([])
window = QMainWindow()
window.setStyleSheet(Path("theme.qss").read_text(encoding="utf-8"))
