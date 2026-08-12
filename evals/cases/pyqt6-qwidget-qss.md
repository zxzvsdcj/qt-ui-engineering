# Case: PyQt6 QWidget QSS Monitoring Table

**Fixture:** `evals/fixtures/pyqt6-qwidget-qss`

## Pressure scenario

Design a live operations monitor with thousands of rows, filters, severity states, inline actions, and a detail inspector. The user asks for a dramatic modern dashboard and a quick implementation.

## Baseline failure risks without this Skill

- Builds rows as individual card widgets instead of using Model/View.
- Uses Web CSS variables or unsupported QSS effects.
- Overuses color for severity and omits selection/focus/loading states.
- Prioritizes ornamental charts and whitespace over scanning and filtering.

## Required behavior with this Skill

- Report `Python / Qt 6 / PyQt6 / QWidget / QSS` with evidence.
- Use `QTableView` plus a model, proxy filtering, a splitter-based inspector, toolbar actions, and status feedback.
- Keep frequent filters visible, secondary controls progressively disclosed, and row density adjustable without unreadable text.
- Pair severity colors with text or icons and cover selection, keyboard navigation, empty, reconnecting, stale-data, and error states.

## Pass conditions

- Uses PyQt6 scoped-enum and `exec()` conventions when examples require them.
- No per-row widget/card architecture.
- No invented QSS feature.
- Task efficiency and data scanability outweigh dashboard decoration.
