# Visual System and Tokens

## Three token tiers

| Tier | Purpose | Example |
|---|---|---|
| Primitive | raw reusable value; never chosen directly in feature code | `neutral.900`, `space.8` |
| Semantic | product meaning independent of component | `surface.panel`, `text.muted`, `status.danger` |
| Component | a component decision mapped to semantic roles | `table.row.selected-bg`, `button.primary.focus-border` |

Dark, high-contrast, or platform variants normally change semantic mappings; component code continues to use the same roles.

## Required categories

- Color: window, panel, raised, sunken, border, text, muted text, accent, focus, success, warning, danger, selection.
- Typography: body, label, data, caption, section title, window/page title.
- Spacing: inline, control, group, section, region.
- Shape: border widths, radii, separators, elevation/relief.
- Control size: compact, standard, touch-capable.
- Density: row heights, field gaps, panel padding, table cell padding.
- Motion: functional durations and reduced-motion alternative.
- State: hover, focus, pressed, selected, checked, disabled, loading, error.

## Ownership

Assign each visual property one owner:

- native platform style;
- `QPalette` role/group;
- QSS selector/state;
- `QStyle` or `QProxyStyle` metric/painting;
- QML theme property or Qt Quick Controls style.

Do not make multiple mechanisms fight over the same property. Record the mapping in the design-token artifact.

## Token quality rules

- Names describe purpose, not appearance: `text.danger`, not `redText`.
- Feature code consumes semantic or component tokens, not raw hex values.
- Every interactive state has a deliberate mapping or explicitly inherits a verified native state.
- Focus and selection remain distinguishable from hover.
- Disabled content remains legible but clearly unavailable.
- Accent color is not reused decoratively when that would imply interactivity.

Use [the token template](../templates/design-tokens.md) to capture a project-specific system.
