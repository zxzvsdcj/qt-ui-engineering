---
name: qt-ui-engineering
description: Use when designing, implementing, redesigning, theming, or reviewing Qt interfaces using QWidget, QML or Qt Quick, Qt Designer, PyQt, PySide, Qt C++, QSS, QPalette, QStyle, or QProxyStyle.
---

# Qt UI Engineering

Detect the target from project evidence before changing UI code. Preserve its binding, Qt major version, language, framework, and styling system: **Do not migrate** any of them unless the user explicitly requests it. Do not mix PyQt and PySide, Qt 5 and Qt 6, Widget and QML implementation patterns, or QSS and browser CSS.

## Router

1. Inspect the affected sources and run `python scripts/detect_qt_stack.py <project-root> --pretty` when needed. Read [stack detection](references/stack-detection.md) before acting on `unknown`, `conflict`, or mixed evidence.
2. Load the universal guidance that applies: [design philosophy](references/design-philosophy.md), [Information-Density First](references/information-density.md), [interaction and feedback](references/interaction-and-feedback.md), [accessibility](references/accessibility.md), and [Anti-AI-Slop](references/anti-ai-slop.md).
3. Select only the detected framework adapter: [QWidget](references/adapters/qwidget.md), [Qt Quick/QML](references/adapters/qt-quick-qml.md), [Qt Designer](references/adapters/qt-designer.md), [QSS](references/adapters/qss.md), or [QPalette/QStyle](references/adapters/qpalette-qstyle.md).
4. Select exactly one affected implementation adapter: [PyQt5](references/adapters/pyqt5.md), [PyQt6](references/adapters/pyqt6.md), [PySide2](references/adapters/pyside2.md), [PySide6](references/adapters/pyside6.md), [Qt 5 C++](references/adapters/qt5-cpp.md), or [Qt 6 C++](references/adapters/qt6-cpp.md).
5. For QWidget work, load only the focused canonical guidance: [meta](references/widget/meta.md), [UX interaction](references/widget/ux-interaction.md), [icon system](references/widget/icon-system.md), [Hi-DPI and cross-platform](references/widget/hidpi-cross-platform.md), [windows and dialogs](references/widget/window-dialog.md), [Model-View](references/widget/model-view.md), [UI state persistence](references/widget/ui-state-persistence.md), and [resource deployment](references/widget/resource-deployment.md). Do not apply these Widget patterns to QML or Qt Quick.

## Operating rules

- Read the relevant project files; follow existing patterns and make the smallest change that meets the task.
- **Information-Density First:** maximize useful, scannable, reachable information without crowding, shrinking practical targets, or erasing hierarchy.
- **Anti-AI-Slop:** reject generic card grids, arbitrary gradients, oversized headings, excess whitespace, decorative metrics, emoji icons, and unjustified visual flourishes.
- Design and verify relevant states: hover, focus, pressed, selected, disabled, loading, empty, success, warning, error, stale, resize, DPI/text scaling, keyboard flow, cancellation, and destructive confirmation.
- For reviews, separate deterministic Qt correctness from visual judgment and classify findings as `Blocking`, `Major`, `Minor`, or `Enhancement` with evidence, consequence, affected stack, and remediation.

## Response contract

For substantial work, respond in this order: **Detected stack**, **Design intent**, **Implementation**, **Review**, **Risks**.
