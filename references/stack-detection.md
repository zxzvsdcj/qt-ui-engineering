# Stack Detection

## Evidence order

1. Imports, includes, QML imports, and APIs in the files being changed.
2. Declared dependencies in Python packaging, CMake, qmake, and requirements files.
3. UI artifacts: `.ui`, `.qml`, `.qss`, resources, generated UI modules.
4. User-stated target, platform, and constraints.

Run `python scripts/detect_qt_stack.py <project-root> --pretty` for a deterministic first pass. Then read the reported evidence in the relevant source files.

## Report fields

- `status`: `ok`, `unknown`, or `conflict`.
- `language`: detected source languages.
- `qt_major`: one evidence-backed major version or `null`.
- `binding`: one Python binding or `null`.
- `ui_frameworks`: QWidget and/or Qt Quick/QML.
- `styling`: QSS, Qt Designer, and/or Qt Quick Controls evidence.
- `architecture`: observed patterns such as Model/View.
- `target_platforms`: compile/config hints, not guaranteed deployment targets.
- `evidence`: file and line records.
- `warnings`: conflicts or unreadable files.

## Decisions

- `unknown`: inspect more project context. Ask one focused question only when local evidence cannot answer it.
- `conflict`: do not choose a binding or major version. Determine whether the repository contains separate targets and scope the task to one target.
- Multiple QWidget and QML frameworks can be a valid hybrid; select adapters per affected source unit.
- A dependency declaration is not proof that a feature uses that library. Source evidence has higher relevance.

## Limitations

The detector is static and deliberately conservative. It does not import packages, execute build systems, infer installed runtime versions, resolve generated files, or prove the deployment platform. It is an aid to inspection, not a substitute for it.
