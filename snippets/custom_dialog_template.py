"""标准Qt Widget自定义QDialog脚手架，演示模态与非模态生命周期。"""

from __future__ import annotations

import sys

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import (
        QApplication,
        QDialog,
        QDialogButtonBox,
        QFormLayout,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )

    BINDING = "PySide6"
except ImportError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtWidgets import (
        QApplication,
        QDialog,
        QDialogButtonBox,
        QFormLayout,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )

    BINDING = "PyQt6"


class SettingsDialog(QDialog):
    """适合短表单；标准按钮会按平台惯例排列。"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("连接设置")
        self.setMinimumWidth(360)

        self.name_edit = QLineEdit(self)
        self.endpoint_edit = QLineEdit(self)

        form = QFormLayout()
        form.addRow("名称：", self.name_edit)
        form.addRow("地址：", self.endpoint_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            parent=self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        ok_button = buttons.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setDefault(True)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"QDialog模板（{BINDING}）")
        self.resize(640, 420)
        self.setMinimumSize(480, 320)
        self._settings_dialog: SettingsDialog | None = None

        modal_button = QPushButton("打开模态表单")
        modal_button.clicked.connect(self.open_modal_dialog)
        modeless_button = QPushButton("打开非模态表单")
        modeless_button.clicked.connect(self.open_modeless_dialog)

        content = QWidget(self)
        layout = QVBoxLayout(content)
        layout.addWidget(modal_button)
        layout.addWidget(modeless_button)
        layout.addStretch(1)
        self.setCentralWidget(content)

    def open_modal_dialog(self) -> None:
        dialog = SettingsDialog(self)
        dialog.exec()

    def open_modeless_dialog(self) -> None:
        if self._settings_dialog is not None:
            self._settings_dialog.show()
            self._settings_dialog.raise_()
            self._settings_dialog.activateWindow()
            return

        dialog = SettingsDialog(self)
        dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        dialog.finished.connect(self._clear_modeless_dialog)
        self._settings_dialog = dialog
        dialog.show()

    def _clear_modeless_dialog(self, _result: int) -> None:
        self._settings_dialog = None


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
