# PySide2 Adapter

## Identity

- Binding: PySide2 (Qt for Python for Qt 5)
- Qt major: 5
- Imports: `PySide2.QtCore`, `PySide2.QtGui`, `PySide2.QtWidgets`, and required modules
- Qt-specific class API: `Signal`, `Slot`, `Property`

## Conventions

```python
from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import QDialog

alignment = Qt.AlignLeft
dialog = QDialog()
result = dialog.exec_()
```

Preserve the project's signal connection style, overload selection, and ownership/lifetime patterns. Qt object lifetime can differ from ordinary Python objects; keep parents and long-lived references clear.

## UI and resources

- Preserve runtime `QUiLoader`, generated `pyside2-uic` code, or manual-widget construction according to the project.
- Use the existing resource compiler/module workflow.
- Check the exact PySide2 release because available Qt 5 versions and API coverage vary.

## Never mix with

- PyQt `pyqtSignal`/`pyqtSlot` names;
- PySide6 or Qt 6 scoped-enum examples presented as PySide2 requirements;
- unrequested binding migration;
- Qt 6-only QML modules or CMake helpers.
