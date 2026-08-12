# Design Tokens

## Context

| Field | Value |
|---|---|
| Product / surface | |
| Target platform and theme | |
| Density level | Compact / Standard / Comfortable |
| Token owner | Palette / QSS / QStyle / QML style |

## Primitive tokens

| Token | Value | Constraint |
|---|---|---|
| `color.neutral.0` | | Raw palette only; feature code does not consume it |
| `space.1` | | Smallest supported rhythm unit |
| `radius.1` | | Use only where shape communicates grouping/affordance |

## Semantic tokens

| Token | Light | Dark | High contrast | Meaning |
|---|---|---|---|---|
| `surface.window` | | | | Top-level work surface |
| `surface.panel` | | | | Peer panel |
| `text.primary` | | | | Primary content |
| `text.muted` | | | | Secondary metadata |
| `action.primary` | | | | Interactive accent only |
| `focus.visible` | | | | Keyboard focus indicator |
| `status.success` | | | | Paired with icon/text |
| `status.warning` | | | | Paired with icon/text |
| `status.danger` | | | | Paired with icon/text |

## Typography and density

| Role | Family | Point size / metric | Weight | Line/row rule |
|---|---|---:|---:|---|
| Body | | | | |
| Label | | | | |
| Data | | | | |
| Caption | | | | |
| Section title | | | | |

| Spacing role | Value | Relationship |
|---|---:|---|
| `space.inline-tight` | | Icon–label / bound metadata |
| `space.control-gap` | | One action group |
| `space.group` | | Fields/rows in one section |
| `space.section` | | Related sections |
| `space.region` | | Major work regions |

## Component and state mapping

| Component role | Default | Hover | Focus | Pressed/selected | Disabled | Error/loading |
|---|---|---|---|---|---|---|
| Primary action | | | | | | |
| Field | | | | | | |
| Data row | | | | | | |

## Adapter mapping

| Semantic role | QPalette | QSS | QStyle/QProxyStyle | QML / Controls style |
|---|---|---|---|---|
| | | | | |

Every implemented property has one owner. Record exceptions and their rationale below the table.
