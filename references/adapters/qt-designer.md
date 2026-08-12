# Qt Designer Adapter

## Use this adapter when

The project stores `.ui` files, loads them at runtime, compiles them with `uic`, or uses promoted/custom widgets from Designer.

## Ownership boundary

Choose the existing project pattern and preserve it:

1. **Runtime loading:** the `.ui` file is the source of structure; handwritten code binds behavior after load.
2. **Generated source:** the `.ui` file is the source; generated Python/C++ is disposable and regenerated.
3. **Setup composition:** handwritten subclass owns behavior and calls generated `setupUi`.

Do not hand-edit generated files. Change the `.ui` source or the handwritten wrapper, then regenerate through the project's existing toolchain.

## Designer structure

- Give meaningful `objectName` values to controls used by code, tests, or scoped QSS.
- Use layouts for every resizable container; eliminate accidental fixed geometry.
- Set labels, buddies, tab order, tooltips, accessible names, size policies, and translatable strings deliberately.
- Promote widgets when a stable custom component already exists; do not use promotion to hide unclear ownership.
- Keep resources and icons in the project's established resource pipeline.

## Binding/version boundary

The loader and code-generation tools differ across PyQt, PySide, Qt 5, and Qt 6. Load the exact binding adapter. Never regenerate a PyQt5 project with a PySide6 tool or commit environment-specific generated noise without a project convention.

## Review

Open the `.ui` hierarchy and verify layouts, spacers, size policies, object names, tab order, buddies, translatability, and custom-widget registration. Confirm regeneration produces only expected diffs.
