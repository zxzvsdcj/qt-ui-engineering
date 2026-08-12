# Qt 6 C++ Adapter

## Identity

- Language: C++
- Qt major: 6
- Common build targets: `Qt6::Core`, `Qt6::Gui`, `Qt6::Widgets`, `Qt6::Quick`, `Qt6::QuickControls2`

## CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
qt_add_executable(app main.cpp)
target_link_libraries(app PRIVATE Qt6::Widgets)
```

For QML modules, follow the project's `qt_add_qml_module` structure and URI/resource conventions.

## Implementation

- Use scoped enums, Qt 6 module locations, high-DPI defaults, and removed/deprecated API behavior appropriate to the exact minor version.
- Preserve parent ownership, connection style, UI generation, resources, translations, and deployment rules.
- Keep QAction and related Qt 6 module locations correct.
- Verify APIs introduced in later Qt 6 minors before using them; “Qt 6” alone is not sufficient evidence.

## Never mix with

- `Qt5::` targets or Qt 5-only APIs;
- Python binding examples presented as C++ implementation;
- unrequested compatibility layers or build-system migration;
- QWidget/QML implementation substitution without user authorization.
