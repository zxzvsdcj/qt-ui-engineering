# QPalette, QStyle, and QProxyStyle Adapter

## QPalette

Use `QPalette` when semantic colors should participate in native widget painting. Map design roles to documented `ColorRole` values and preserve `Active`, `Inactive`, and `Disabled` color groups.

- Start from the current application/style palette and change only owned roles.
- Do not assume all native/platform styles honor every palette role identically.
- Verify selected text/background, links, tooltips, placeholders, disabled content, and inactive windows.
- Do not flatten disabled/inactive groups into one active palette.

See the [QPalette documentation](https://doc.qt.io/qt-6/qpalette.html).

## QStyle and QProxyStyle

Use native `QStyle` metrics and standard icons where they meet the product need. Use `QProxyStyle` only for a focused, testable change to metrics, hints, icons, geometry, or painting that palette/QSS cannot express safely.

- Delegate unmodified behavior to the base style.
- Keep overrides narrow and document the affected controls/states.
- Test across every supported platform style and DPI.
- Avoid building a complete custom style for a small visual preference.

## Ownership decision

| Need | Preferred owner |
|---|---|
| Native semantic foreground/background | `QPalette` |
| Supported component skin/state | QSS |
| Pixel metric, style hint, standard icon, custom painting | `QStyle`/`QProxyStyle` |
| Declarative Qt Quick control theme | Qt Quick Controls style/QML tokens |

Do not assign the same property to multiple owners. A QSS rule can override palette/native painting in ways that make palette changes appear broken.
