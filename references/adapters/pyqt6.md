# PyQt6 Adapter

## Identity

- Binding: PyQt6
- Qt major: 6
- Imports: `PyQt6.QtCore`, `PyQt6.QtGui`, `PyQt6.QtWidgets`, and required add-on modules
- Qt-specific class API: `pyqtSignal`, `pyqtSlot`, `pyqtProperty`

## Conventions

```python
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QDialog

alignment = Qt.AlignmentFlag.AlignLeft
dialog = QDialog()
result = dialog.exec()
```

PyQt6 uses Python enum/flag classes for named enums and removes `exec_()`/`print_()` forms. Use scoped enum names from the exact class and module documented for the project's PyQt6 version.

## UI and resources

- Preserve the project's `uic.loadUi`, generated `pyuic6` module, or manual-widget pattern.
- `pyrcc6` is not part of the PyQt6 toolset; preserve the repository's actual Qt resource/build approach instead of assuming the PyQt5 workflow.
- Qt 6 moved some classes between modules; for example, QAction is in QtGui. Copy existing imports or verify official docs.

See [Riverbank's PyQt6/PyQt5 differences](https://www.riverbankcomputing.com/static/Docs/PyQt6/pyqt5_differences.html).

## Never mix with

- PyQt5/PySide imports or `Signal` aliases presented as PyQt API;
- unscoped Qt 5 enum examples presented as universal;
- `exec_()` or removed PyQt5 tooling;
- unrequested Qt 5 compatibility wrappers.
