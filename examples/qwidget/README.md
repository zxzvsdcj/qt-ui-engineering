# QWidget Token Translation Example

This example shows ownership boundaries, not a portable theme implementation.

## Universal roles

```text
surface.window
surface.panel
text.primary
text.muted
action.primary
focus.visible
selection.background
selection.text
```

## Translation

1. Map native semantic colors to `QPalette` roles/groups.
2. Render component skins and supported states into one QSS artifact only when required.
3. Use `QProxyStyle` only for a documented metric/painting gap.
4. Keep layout, sizing, Model/View, and interaction behavior in QWidget code—not QSS.

```python
TOKENS = {
    "surface_panel": "#25272b",
    "text_primary": "#e6e8eb",
    "focus_visible": "#72a7ff",
}

QSS_TEMPLATE = """
QFrame[role="panel"] {{
    background: {surface_panel};
    color: {text_primary};
}}
QPushButton:focus {{
    border: 1px solid {focus_visible};
}}
"""

qss = QSS_TEMPLATE.format(**TOKENS)
```

The binding adapter supplies imports and enum/execution syntax. The project decides how tokens are loaded and themes are switched.
