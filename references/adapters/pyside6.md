# PySide6 Adapter

## Identity

- Binding: PySide6 (Qt for Python for Qt 6)
- Qt major: 6
- Imports: `PySide6.QtCore`, `PySide6.QtGui`, `PySide6.QtWidgets`, and required modules
- Qt-specific class API: `Signal`, `Slot`, `Property`

## Conventions

```python
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QDialog

alignment = Qt.AlignmentFlag.AlignLeft
dialog = QDialog()
result = dialog.exec()
```

Some projects enable `from __feature__ import snake_case, true_property`. Detect and preserve that choice within the affected source; do not mix feature-style calls and conventional bindings casually.

## UI and resources

- Preserve runtime `QUiLoader`, generated `pyside6-uic` code, or manual-widget construction.
- Use the established `pyside6-rcc`/Qt resource and build integration.
- Keep module locations consistent with Qt 6, including QAction in QtGui.

## Never mix with

- PyQt `pyqtSignal`, `pyqtSlot`, or `pyqtProperty`;
- PySide2/Qt 5 enum and execution examples presented as current conventions;
- unrequested `__feature__` conversion;
- compatibility abstractions that obscure the project's actual binding.

Verify exact behavior in the [Qt for Python documentation](https://doc.qt.io/qtforpython-6/).
