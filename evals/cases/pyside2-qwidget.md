# Case: PySide2 QWidget Property Inspector

**Fixture:** `evals/fixtures/pyside2-qwidget`

## Pressure scenario

Improve a Qt 5-era technical property inspector without changing its PySide2 binding. Users edit nested objects, compare values, and rely on context menus and keyboard shortcuts.

## Baseline failure risks without this Skill

- Recommends PySide6 migration or uses PySide6 enum examples.
- Replaces dense tree/property patterns with a sparse mobile-style form.
- Ignores mixed-value, validation, undo, and destructive reset states.

## Required behavior with this Skill

- Report `Python / Qt 5 / PySide2 / QWidget` with evidence and no assumed QSS.
- Prefer tree/property Model/View structures, inline editors, a stable toolbar, context actions, and undo-aware feedback.
- Preserve the existing native style unless a verified theme system exists.
- Review edit commitment, focus movement, validation errors, mixed values, reset confirmation, and DPI scaling.

## Pass conditions

- Uses PySide2 names such as `Signal`, `Slot`, and Qt 5 enum conventions only when needed.
- Does not fabricate a QSS requirement.
- Maintains dense expert workflow without shrinking text or controls below usable sizes.
