# QSS Adapter

## Use this adapter when

The project contains `.qss`, calls `setStyleSheet`, or intentionally uses Qt Style Sheets for QWidget styling.

## QSS is not browser CSS

Qt Style Sheets have Qt-specific supported properties, selectors, sub-controls, pseudo-states, cascade, and inheritance. They do not support CSS custom properties or `!important`, and many browser layout/effect properties have no Qt equivalent. Verify every property and sub-control in the [Qt Style Sheet reference](https://doc.qt.io/qt-6/stylesheet-reference.html).

## Architecture

1. Keep primitive and semantic tokens in a data structure or template input.
2. Render one coherent application/component QSS artifact from those tokens.
3. Scope component variants with object names or dynamic properties where semantic roles differ.
4. Keep feature code free of scattered raw QSS strings.

Qt does not natively evaluate a Web declaration such as `var(--surface-panel)`. Render semantic tokens into valid QSS before applying the stylesheet.

## Selectors and state

- Type selectors apply to Qt classes; inheritance does not make a subclass selector more specific.
- Object ID selectors use `#objectName` and should represent stable semantic roles.
- Dynamic-property selectors are useful for variants; changing the property may require unpolish/polish or stylesheet reapplication.
- Pseudo-states cover supported Qt states such as hover, focus, pressed, checked, selected, disabled, and active.
- Complex widgets expose documented sub-controls. If one sub-control/property is customized, the remaining parts may also need complete styling.

See [Qt Style Sheet syntax](https://doc.qt.io/qt-6/stylesheet-syntax.html).

## Restraint

- Preserve native metrics, focus, and platform behavior unless the product design requires ownership.
- Prefer `QPalette` for semantic colors that should propagate through native painting.
- Prefer `QProxyStyle` for documented metrics or painting behavior that QSS cannot express reliably.
- Avoid deep descendant selectors, fragile object-name chains, and local child stylesheets that override the application cascade.
- Verify every theme and interactive state in a rendered application.

## Forbidden assumptions

- `:root`, CSS variables, flexbox, grid, media queries, transitions, filters, backdrop blur, and arbitrary box shadows are not general QSS features.
- QSS cannot repair incorrect layouts or Model/View architecture.
- Web selector intuition is not evidence that a Qt selector/sub-control exists.
