# Case: PySide6 QWidget QSS Analysis Workspace

**Fixture:** `evals/fixtures/pyside6-qwidget-qss`

## Pressure scenario

Create a multi-panel analysis workspace with a navigator, central plot/table region, inspector, toolbar, and status bar. The stakeholder asks for every panel to look visually premium.

## Baseline failure risks without this Skill

- Wraps each panel in rounded cards and adds heavy shadows.
- Fixes panel sizes instead of using splitters and saved layout state.
- Mixes PyQt signal names into PySide6 code.
- Omits collapsed, disabled, loading, selection, and failure states.

## Required behavior with this Skill

- Report `Python / Qt 6 / PySide6 / QWidget / QSS` with evidence.
- Use splitters/docks according to workflow, semantic panel hierarchy, compact toolbars, and persistent workspace state.
- Spend visual distinctiveness on one domain-specific signature rather than global decoration.
- Keep `Signal`/`Slot`/`Property` vocabulary and Qt 6 scoped enums consistent.

## Pass conditions

- No PyQt imports or fixed-layout workaround.
- QSS owns only properties it can maintain reliably.
- The review tests panel resize ranges, focus, shortcuts, state persistence, contrast, and failure feedback.
