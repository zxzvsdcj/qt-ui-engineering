# QWidget Adapter

## Use this adapter when

The affected UI uses `QApplication`, `QWidget`, `QMainWindow`, Qt Widgets views, layouts, dialogs, docks, or toolbars. Load one binding/C++ adapter and any detected styling adapter with it.

## Window and region structure

- Use `QMainWindow` only when the product needs its central widget, menus, toolbars, docks, or status bar.
- Use ordinary `QWidget` composition for contained panels and reusable controls.
- Use `QSplitter` for user-controlled peer regions; set meaningful minimum sizes and stretch factors.
- Use `QDockWidget` when panels must move, detach, hide, or participate in saved workspaces.
- Use `QStackedWidget` for one navigation context showing one page at a time.
- Use `QTabWidget` for alternate views of one context, not the application's entire information architecture by default.

## Layout and sizing

- Prefer `QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, and `QFormLayout` over manual geometry.
- Set layout margins and spacing from density tokens; avoid stacking redundant margins through nested containers.
- Treat `sizeHint()`, `minimumSizeHint()`, `QSizePolicy`, stretch, and content metrics as a system.
- Use fixed sizes only for genuinely fixed assets or hardware surfaces.
- Let user-visible text expand. Test long translations and large system fonts.
- Do not add an outer `QScrollArea` to conceal a layout that cannot resize.

## Data and repeated content

Use Model/View (`QTableView`, `QTreeView`, `QListView`, models, proxies, delegates, selection models) for repeated or large data. Avoid one child widget per row when a view/delegate represents the same interaction.

- Keep sorting/filter scope and selection visible.
- Put row-level commands in delegates or context/toolbar actions according to frequency.
- Keep model data semantic; avoid storing presentation-only strings when roles can provide structured values.
- Test empty, partial, loading, stale, large, and error states.

## Interaction

- Set tab order to match visual order where Qt's automatic order is insufficient.
- Use actions so menus, toolbars, shortcuts, and context menus share command state.
- Keep visible focus; do not erase it with QSS.
- Return focus after closing dialogs and validate Escape/Cancel behavior.
- Persist window, splitter, dock, column, and workspace state only when it benefits repeated work.

## Review failures

- absolute positioning in a resizable desktop window;
- unnecessary fixed width/height values;
- excessive wrapper widgets used only for decoration;
- widget-per-record data surfaces;
- local `setStyleSheet()` calls that create competing theme ownership;
- disabled controls without an explanation or recovery path;
- a visually compact layout that clips at high DPI or large text.
