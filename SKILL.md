---
name: qt-ui-engineering
description: Use when designing, implementing, redesigning, theming, or reviewing user interfaces in Qt projects that use QWidget, QML or Qt Quick, Qt Designer, PyQt, PySide, Qt C++, QSS, QPalette, QStyle, or QProxyStyle.
---

# Qt UI Engineering

## Overview

Create Qt interfaces from one product-specific design system, then translate that system through the project's existing Qt framework, binding, language, and version. Preserve Qt-native behavior and desktop efficiency while making deliberate visual choices.

## Non-negotiable rules

1. Read the relevant project files before proposing or changing UI code.
2. Detect the actual stack from evidence. State uncertainty; never guess.
3. Do not migrate a binding, Qt major version, language, UI framework, or styling system unless the user explicitly asks for migration.
4. Do not mix PyQt with PySide, Qt 5 with Qt 6, QWidget with QML implementation patterns, or QSS with browser-only CSS.
5. Follow existing project patterns and make the smallest change that satisfies the UI task.
6. Design every operational state, not only the resting screenshot.

## Start with project evidence

Inspect manifests and UI sources: `pyproject.toml`, requirements files, `setup.py`, `CMakeLists.txt`, `.pro`, `.pri`, `.py`, `.cpp`, `.h`, `.qml`, `.ui`, and `.qss`.

For a first-pass report, run:

```text
python scripts/detect_qt_stack.py <project-root> --pretty
```

Read [stack detection](references/stack-detection.md) before acting on `unknown`, `conflict`, or a mixed repository. The script is advisory; confirm its evidence in the files you will modify.

Before substantial design work, establish only the context not already known:

- product, users, frequent tasks, and content priority;
- target platform, window or screen range, DPI, and viewing distance;
- keyboard, pointer, touch, hardware, or assistive input;
- locale, text expansion, and RTL requirements;
- existing design system, tokens, theme ownership, and UI architecture;
- measurable success criteria.

Small edits such as changing copy or moving one action do not require a new design brief. They still require stack correctness and relevant state/accessibility checks.

## Three layers

### 1. Universal design

Apply these independently of implementation technology:

- [Design philosophy](references/design-philosophy.md)
- [Information-Density First](references/information-density.md)
- [Visual system and tokens](references/visual-system.md)
- [Typography](references/typography.md)
- [Color system](references/color-system.md)
- [Spacing and layout](references/spacing-and-layout.md)
- [Interaction and feedback](references/interaction-and-feedback.md)
- [Desktop UX](references/desktop-ux.md)
- [Accessibility](references/accessibility.md)
- [Anti-AI-Slop](references/anti-ai-slop.md)

### 2. Qt UI framework and styling

Load only the adapters detected in the project:

| Evidence | Required adapter |
|---|---|
| QWidget or Qt Widgets classes | [QWidget](references/adapters/qwidget.md) |
| QML, QtQuick, Qt Quick Controls | [Qt Quick/QML](references/adapters/qt-quick-qml.md) |
| `.ui`, `uic`, promoted widgets | [Qt Designer](references/adapters/qt-designer.md) |
| `.qss`, `setStyleSheet` | [QSS](references/adapters/qss.md) |
| `QPalette`, `QStyle`, `QProxyStyle` | [QPalette/QStyle](references/adapters/qpalette-qstyle.md) |

### 3. Binding, language, and Qt version

Load exactly one implementation adapter for each affected source unit:

| Detected stack | Required adapter |
|---|---|
| PyQt5 | [PyQt5](references/adapters/pyqt5.md) |
| PyQt6 | [PyQt6](references/adapters/pyqt6.md) |
| PySide2 | [PySide2](references/adapters/pyside2.md) |
| PySide6 | [PySide6](references/adapters/pyside6.md) |
| Qt 5 C++ | [Qt 5 C++](references/adapters/qt5-cpp.md) |
| Qt 6 C++ | [Qt 6 C++](references/adapters/qt6-cpp.md) |

A repository may contain multiple legitimate targets. Scope detection and adapter selection to the target being changed; do not create a universal compatibility wrapper unless requested.

## Workflow

1. Inspect relevant files and existing UI patterns.
2. Report detected stack, evidence, uncertainty, and constraints.
3. Define the user task and measurable success.
4. Rank information as primary, secondary, and tertiary.
5. Choose a product-specific visual direction and one restrained signature.
6. Reuse or define semantic design tokens.
7. Design density, layout, navigation, resizing, and all states.
8. Select Qt-native components and the exact adapters.
9. Implement within the existing stack and architecture.
10. Review with the [UI review checklist](references/ui-review-checklist.md).
11. Fix evidenced issues, verify behavior, and state residual Risks.

Use [the design brief](templates/ui-design-brief.md), [design tokens](templates/design-tokens.md), and [the review report](templates/ui-review.md) when the task is large enough to benefit from persistent artifacts.

## Information-Density First

Maximize useful information per unit of screen area while preserving readability, scanability, interaction reachability, and visual hierarchy. Use space to communicate grouping, rhythm, priority, and interaction boundaries. Large decorative gaps, oversized headings, and empty containers are not default signs of quality.

High density is not crowding. Do not shrink text, reduce practical hit targets, erase grouping, or conceal frequent actions. Prefer information architecture, compact rhythm, Model/View, splitters, toolbars, tables, trees, inspectors, status bars, shortcuts, and contextual actions when they improve the workflow.

## Anti-AI-Slop

Reject generic choices made only because generated dashboards commonly use them: card-wrapping every region, arbitrary gradients, giant headings, excessive blank space, excessive radii or shadows, emoji icons, and decorative metrics. Every distinctive choice must be justified by the product domain and task. Spend boldness on one coherent signature; keep the operational surface disciplined.

## Quality gates

### Visual and density

- Content priority is visible without relying only on size or blank space.
- Spacing expresses relationships; no functionless whitespace remains.
- Typography, color, borders, radii, and elevation come from semantic roles.
- The result is product-specific rather than a transferable dashboard template.

### Interaction and desktop behavior

- Cover relevant hover, focus, pressed, selected, checked, disabled, loading, empty, success, warning, error, and stale states.
- Verify resize ranges, DPI/text scaling, keyboard order, shortcuts, context menus, cancellation, destructive confirmation, and feedback latency.
- Frequent actions remain visible and close to their work context.

### Accessibility and implementation

- Focus is visible; controls have accessible names; meaning does not depend on color alone.
- Text and essential UI contrast are checked against the project's accessibility target.
- The implementation uses only APIs and styling features valid for the detected stack.
- Theme ownership is clear; QSS, palette, native style, and QML style do not fight over the same property.

## Review mode

For audits, do not redesign immediately. Report findings as `Blocking`, `Major`, `Minor`, or `Enhancement`, each with observable evidence, user consequence, affected stack, and concrete remediation. Separate deterministic Qt correctness from subjective visual judgment.

## Response contract

For substantial work, report in this order:

1. **Detected stack** — language, Qt version, binding, framework, styling, evidence, uncertainty.
2. **Design intent** — user task, information hierarchy, density, visual direction, token decisions.
3. **Implementation** — files and stack-specific patterns used.
4. **Review** — state, desktop, accessibility, visual, and maintainability results.
5. **Risks** — unverified version details, environment limits, and residual issues.

## Common mistakes

| Mistake | Correction |
|---|---|
| Assuming Qt means PyQt6 | Detect language, binding, and major version independently. |
| Treating QSS as CSS | Use only documented Qt selectors, properties, states, and sub-controls. |
| Styling before information architecture | Rank content and frequent actions first. |
| Equating whitespace with quality | Give every gap a grouping, rhythm, or focus purpose. |
| Equating density with compression | Improve structure before reducing size or spacing. |
| Reviewing by taste alone | Attach evidence, consequence, severity, and remediation. |
