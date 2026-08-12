# Case: Qt 6 QML Control Panel

**Fixture:** `evals/fixtures/qt6-qml`

## Pressure scenario

Design a keyboard, pointer, and touch-capable equipment control panel using the project's existing Qt Quick Controls style. It must adapt between 800×480 and desktop windows while exposing live status and guarded commands.

## Baseline failure risks without this Skill

- Translates QWidget/QSS patterns into imperative QML.
- Explicitly imports multiple Qt Quick Controls styles.
- Uses geometry animation for decoration and ignores reduced motion.
- Hides safety status to achieve visual minimalism.

## Required behavior with this Skill

- Report `QML/C++ / Qt 6 / Qt Quick/QML / Qt Quick Controls` with evidence.
- Preserve the existing compile-time or runtime style selection mechanism.
- Use properties, bindings, states, models/delegates, and Qt Quick Layouts.
- Adapt information priority by width; keep safety state persistent and pair color with icon/text.
- Review focus navigation, mirroring, touch/pointer coexistence, cancellation, confirmation, and latency feedback.

## Pass conditions

- No QSS or QWidget implementation advice unless explicitly discussing a separate subsystem.
- No style mixing or decorative motion that impairs control.
- Fixed embedded constraints and resizable desktop behavior are distinguished.
