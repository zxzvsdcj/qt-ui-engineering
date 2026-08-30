---
name: qt-ui-engineering
description: Use when designing, implementing, redesigning, theming, or reviewing Qt interfaces using QWidget, QML or Qt Quick, Qt Designer, PyQt, PySide, Qt C++, QSS, QPalette, QStyle, or QProxyStyle.
---

# Qt UI Engineering

Detect the target from project evidence before changing UI code. Preserve its binding, Qt major version, language, framework, and styling system: **Do not migrate** any of them unless the user explicitly requests it. Do not mix PyQt and PySide, Qt 5 and Qt 6, Widget and QML implementation patterns, or QSS and browser CSS.

## Router

1. Inspect the affected sources and run `python scripts/detect_qt_stack.py <project-root> --pretty` when needed. Read [stack detection](references/stack-detection.md) before acting on `unknown`, `conflict`, or mixed evidence.
2. Load universal guidance only for the matching concern: for product intent, hierarchy, and product decisions, read [design philosophy](references/design-philosophy.md); for information density, read [Information-Density First](references/information-density.md); for a visual system, read [visual system](references/visual-system.md); for typography, read [typography](references/typography.md); for a color system or theming, read [color system](references/color-system.md); for spacing or layout, read [spacing and layout](references/spacing-and-layout.md); for interaction or feedback, read [interaction and feedback](references/interaction-and-feedback.md); for desktop UX, read [desktop UX](references/desktop-ux.md); for accessibility, read [accessibility](references/accessibility.md); for anti-AI-slop review, read [Anti-AI-Slop](references/anti-ai-slop.md); and for a UI review, read [UI review checklist](references/ui-review-checklist.md). Do not bulk-load universal references.
3. Load every detected framework or styling adapter relevant to the affected source files and task: [QWidget](references/adapters/qwidget.md), [Qt Quick/QML](references/adapters/qt-quick-qml.md), [Qt Designer](references/adapters/qt-designer.md), [QSS](references/adapters/qss.md), and [QPalette/QStyle](references/adapters/qpalette-qstyle.md). Do not load an adapter solely because it exists elsewhere in the repository.
4. For each affected source file, select exactly one binding, language, and Qt-version adapter: [PyQt5](references/adapters/pyqt5.md), [PyQt6](references/adapters/pyqt6.md), [PySide2](references/adapters/pyside2.md), [PySide6](references/adapters/pyside6.md), [Qt 5 C++](references/adapters/qt5-cpp.md), or [Qt 6 C++](references/adapters/qt6-cpp.md); do not mix stacks within that source file.
5. For QWidget implementation, route by concern. Do not load all Widget references: for Widget architecture, read [meta](references/widget/meta.md); for Widget interaction, read [UX interaction](references/widget/ux-interaction.md); for Widget icon decisions, read [icon system](references/widget/icon-system.md); for Widget Hi-DPI and cross-platform behavior, read [Hi-DPI and cross-platform](references/widget/hidpi-cross-platform.md); for a Widget window or dialog, read [windows and dialogs](references/widget/window-dialog.md); for Widget model-view data, read [Model-View](references/widget/model-view.md); for Widget state persistence, read [UI state persistence](references/widget/ui-state-persistence.md); and for Widget resource deployment, read [resource deployment](references/widget/resource-deployment.md). Do not apply these Widget patterns to QML or Qt Quick.
6. For substantial tasks or persistent artifacts, load only the needed template: for design tokens, use [design tokens](templates/design-tokens.md); for a design brief, use [UI design brief](templates/ui-design-brief.md); and for a review artifact, use [UI review](templates/ui-review.md).
7. For PySide6 or PyQt6 QWidget implementation only, load a matching snippet: for Hi-DPI initialization, use [Hi-DPI initialization](snippets/hidpi_init.py); for a custom dialog, use [custom dialog](snippets/custom_dialog_template.py); for a large data table, use [large data table](snippets/tableview_model_demo.py); for UI state persistence, use [UI state persistence](snippets/ui_persistence_helper.py); and for resource loading, use [resource loading](snippets/resource_loader.py). Do not use these snippets for a different binding, Qt version, or QML implementation.

## Operating rules

- Read the relevant project files; follow existing patterns and make the smallest change that meets the task.
- **Information-Density First:** maximize useful, scannable, reachable information without crowding, shrinking practical targets, or erasing hierarchy.
- **Anti-AI-Slop:** reject generic card grids, arbitrary gradients, oversized headings, excess whitespace, decorative metrics, emoji icons, and unjustified visual flourishes.
- Design and verify relevant states: hover, focus, pressed, selected, disabled, loading, empty, success, warning, error, stale, resize, DPI/text scaling, keyboard flow, cancellation, and destructive confirmation.
- For reviews, separate deterministic Qt correctness from visual judgment and classify findings as `Blocking`, `Major`, `Minor`, or `Enhancement` with evidence, consequence, affected stack, and remediation.

## Response contract

For substantial work, respond in this order: **Detected stack**, **Design intent**, **Implementation**, **Review**, **Risks**.
