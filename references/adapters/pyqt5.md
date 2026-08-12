# PyQt5 Adapter

## Identity

- Binding: PyQt5
- Qt major: 5
- Imports: `PyQt5.QtCore`, `PyQt5.QtGui`, `PyQt5.QtWidgets`, and required modules
- Qt-specific class API: `pyqtSignal`, `pyqtSlot`, `pyqtProperty`

## Conventions

```python
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog

alignment = Qt.AlignLeft
dialog = QDialog()
result = dialog.exec_()
```

Follow the existing project when it uses scoped enum access supported by its exact PyQt5/Qt version. Do not rewrite code to PyQt6 conventions for stylistic consistency.

## UI and resources

- Preserve the project's `uic.loadUi`, generated `pyuic5` module, or manual-widget pattern.
- Preserve the established Qt resource workflow and generated module naming.
- Keep QAction and other module imports consistent with PyQt5/Qt 5 locations in the project.

## Never mix with

- `PyQt6`, `PySide2`, or `PySide6` imports;
- PyQt6-only scoped-enum examples presented as PyQt5 requirements;
- unrequested `exec()` migration where the project's supported API uses `exec_()`;
- Qt 6 CMake, QML, or removed/deprecated API assumptions.

Verify uncertain APIs against the installed PyQt5 and Qt 5 documentation rather than inferring them from PyQt6.
