# Qt Quick and QML Adapter

## Use this adapter when

The affected UI contains `.qml`, `import QtQuick`, `QtQuick.Controls`, `QQmlApplicationEngine`, or a Qt Quick module. Do not translate QWidget composition or QSS into QML.

## Declarative structure

- Express UI state as properties and bindings rather than imperative synchronization.
- Use Qt Quick Layouts for resizable structure; reserve anchors for clear local relationships.
- Use models and delegates for repeated data. Keep delegate state derived from model/selection state.
- Use named components for reusable behavior and a theme singleton/module for semantic tokens.
- Keep visual state in `states`, bindings, and control properties; avoid scattered JavaScript mutations.

## Qt Quick Controls style ownership

First determine whether the project selects a style at compile time or runtime. Preserve that mechanism.

- Compile-time style imports support optimized, explicit style selection.
- Runtime selection may use `QQuickStyle`, the `-style` argument, environment, or `qtquickcontrols2.conf`.
- Do not explicitly import multiple styles in one application; import order can produce unexpected theming and control selection.
- Customize controls through documented style APIs or a coherent custom style, not arbitrary per-screen overrides.

See [Qt Quick Controls styles](https://doc.qt.io/qt-6/qtquickcontrols-styles.html) and verify the project's exact Qt version.

## Adaptive layout and input

- Define primary screen/window size and supported resize range.
- At narrower widths, collapse or navigate secondary regions while preserving primary status and commands.
- Set focus scopes, tab/backtab navigation, shortcut behavior, and visible `activeFocus` treatment.
- Support pointer, keyboard, touch, or hardware input required by the target; hover cannot be the only disclosure path.
- Use `LayoutMirroring` and explicit directional-icon mirroring for RTL where required.

## Motion and performance

- Animate state or causality, not decoration.
- Prefer transforms and opacity when they produce the intended effect without layout churn.
- Avoid large numbers of simultaneous animations and expensive delegate work.
- Provide an instant reduced-motion path through a project-level preference when motion is nonessential.

## Review failures

- imperative code that manually keeps properties in sync;
- fixed coordinates for a resizable surface;
- QSS selectors or QWidget APIs in QML guidance;
- multiple explicit Controls style imports;
- delegates that own business data or launch unbounded work;
- hidden safety/status information in a minimalist layout.
