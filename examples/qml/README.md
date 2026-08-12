# QML Token Translation Example

Use the same semantic roles as QWidget, but translate them through QML properties and the existing Qt Quick Controls style.

```qml
pragma Singleton
import QtQuick

QtObject {
    readonly property color surfacePanel: "#25272b"
    readonly property color textPrimary: "#e6e8eb"
    readonly property color focusVisible: "#72a7ff"
    readonly property int spaceGroup: 12
}
```

Register the singleton in the project's QML module, then consume role names in controls/components. Preserve the existing compile-time or runtime Controls style; do not import multiple styles or translate QSS selectors into QML.

Layout and state remain declarative:

```qml
ColumnLayout {
    spacing: Theme.spaceGroup
    Label { color: Theme.textPrimary }
    Button { focusPolicy: Qt.StrongFocus }
}
```

Verify exact module registration syntax against the project's Qt 6 minor version and build system.
