# Case: Qt 5 C++ QWidget Inspector

**Fixture:** `evals/fixtures/qt5-cpp-qwidget`

## Pressure scenario

Modernize a Qt 5 C++ diagnostics inspector built with CMake, QWidget, and native styling. The codebase cannot upgrade Qt this release and must remain responsive with large object trees.

## Baseline failure risks without this Skill

- Changes CMake targets to Qt6 or proposes a Python binding.
- Uses Qt 6-only API examples.
- Builds nested widgets instead of a model-backed tree and detail panel.
- Applies a global stylesheet that erases platform conventions.

## Required behavior with this Skill

- Report `C++ / Qt 5 / QWidget` with evidence.
- Preserve `Qt5::Widgets`, Qt 5 API conventions, and native style ownership.
- Use Model/View, a splitter, compact search/filter controls, context actions, and status feedback.
- Verify exact minor-version APIs against Qt documentation before implementation.

## Pass conditions

- No Qt 6 CMake/API or Python examples presented as implementation.
- Efficient tree inspection and keyboard workflow drive the layout.
- Review covers large-model performance, selection, focus, resize, error, and disabled states.
