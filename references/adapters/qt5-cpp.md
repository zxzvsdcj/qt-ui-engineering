# Qt 5 C++ Adapter

## Identity

- Language: C++
- Qt major: 5
- Common build targets: `Qt5::Core`, `Qt5::Gui`, `Qt5::Widgets`, `Qt5::Quick`, `Qt5::QuickControls2`

## CMake

```cmake
find_package(Qt5 REQUIRED COMPONENTS Widgets)
add_executable(app main.cpp)
target_link_libraries(app PRIVATE Qt5::Widgets)
```

Preserve qmake when the project uses `.pro`/`.pri`; do not migrate the build system as a UI side effect.

## Implementation

- Use the exact Qt 5 class/module locations and enum/API forms already supported by the project's minor version.
- Preserve parent ownership, signal/slot connection style, UI compilation, resources, translations, and deployment rules.
- Do not copy Qt 6 CMake helpers such as `qt_add_qml_module` into a Qt 5 project without an explicit migration plan.
- Verify deprecations and platform behavior against the project's exact Qt 5 documentation.

## Never mix with

- `Qt6::` targets or Qt 6-only APIs;
- Python binding examples presented as implementation;
- versionless QML import assumptions that require Qt 6;
- an unrequested CMake/qmake or QWidget/QML migration.
