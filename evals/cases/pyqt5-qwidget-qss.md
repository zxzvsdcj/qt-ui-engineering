# Case: PyQt5 QWidget QSS Settings Editor

**Fixture:** `evals/fixtures/pyqt5-qwidget-qss`

## Pressure scenario

Redesign a legacy settings editor under time pressure. The user wants a modern result but explicitly requires PyQt5, QWidget, and the existing QSS pipeline. The screen contains 45 settings across six categories, several dependent options, Apply/Reset actions, and keyboard-heavy expert users.

## Baseline failure risks without this Skill

- Migrates to PyQt6 or writes PyQt6 scoped enums because they appear newer.
- Converts the screen into large cards with excessive whitespace.
- Styles every QWidget locally and creates QSS specificity conflicts.
- Omits dependency-disabled states, Reset confirmation, focus order, and resize behavior.

## Required behavior with this Skill

- Report `Python / Qt 5 / PyQt5 / QWidget / QSS` with evidence.
- Preserve PyQt5 imports and execution/enum conventions.
- Use compact category navigation plus a structured form or property view; group by relationship, not decorative card boundaries.
- Define semantic tokens before generating QSS and keep native behavior where QSS adds no product value.
- Review dependency states, keyboard order, Apply/Reset feedback, localization expansion, and minimum usable window width.

## Pass conditions

- No migration or PyQt6/PySide syntax.
- Density is high but labels and hit targets remain usable.
- QSS guidance acknowledges Qt selectors, pseudo-states, and cascade limits.
- Review contains severity, evidence, and remediation.
