# Theme Ownership Guide

| Requirement | Owner | Reason |
|---|---|---|
| Native widget semantic colors | `QPalette` | Participates in native painting and color groups |
| Supported widget skin/state | QSS | Declarative selector/state customization |
| Style metric, hint, icon, painting | `QStyle`/`QProxyStyle` | Native style extension point |
| Qt Quick control appearance | Controls style/QML tokens | Declarative framework ownership |
| Layout and information density | QWidget layouts or Qt Quick Layouts | Styling cannot repair structure |

## Conflict example

If `QPalette.ButtonText` defines button text while application QSS also sets `QPushButton { color: ... }`, QSS becomes the visible owner. Updating the palette may appear ineffective. Assign the role to one mechanism and remove the competing override.

## Switching themes

- Swap semantic mappings, not component meaning.
- Reapply/repolish only through the project's established theme manager.
- Verify native, inactive, disabled, focus, selection, and complex-widget sub-controls after switching.
- Do not claim a theme is correct from token files alone; render and interact with it.
