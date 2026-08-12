# Information-Density First

## Principle

In the presence of readable typography, scanability, interaction reachability, and clear hierarchy, increase useful information per unit of screen area. Space is functional: it separates groups, establishes rhythm, protects focus, and defines interaction boundaries.

High information density is not crowding. Never increase density by making text unreadable, reducing practical hit targets, hiding frequent actions, or flattening hierarchy.

## Density decisions

Use the densest level that keeps the target workflow comfortable:

| Level | Suitable work | Characteristics |
|---|---|---|
| Compact | expert tools, tables, property editors, monitoring | short rows, inline actions, strong grouping, keyboard-first |
| Standard | general desktop productivity | moderate controls, balanced scanning and explanation |
| Comfortable | onboarding, occasional settings, touch-biased use | larger targets and explanations, still no decorative voids |

Do not apply one level universally. A compact data grid can coexist with a standard toolbar and a comfortable destructive confirmation.

## Increase density through structure

- Replace repeated cards with tables, trees, forms, tabs, or split views when relationships support them.
- Use labels, dividers, alignment, and shared headers before adding large gaps.
- Put filters and actions near the data they affect.
- Use columns for comparable values and rows for repeated entities.
- Collapse secondary inspectors or advanced groups; do not hide primary status.
- Use status bars for persistent background state instead of blocking dialogs.
- Use Model/View for large or repeated data instead of one widget per record.

## Spacing rhythm

Start with relationship-based roles, then map them to project tokens:

- `space.inline-tight`: icon–label or tightly bound metadata.
- `space.control-gap`: controls in one action group.
- `space.group`: fields or rows within one semantic section.
- `space.section`: distinct but related sections.
- `space.region`: major navigation/work regions.

The common 4/8/12/16/24 rhythm is a starting point, not a mandate. DPI, font metrics, touch requirements, platform style, and existing tokens decide final values.

## Crowding checks

A dense layout fails when:

- labels truncate before values with no recovery path;
- keyboard focus becomes hard to locate;
- pointer/touch targets overlap or demand precision;
- every boundary has equal visual weight;
- controls lose state differentiation;
- translated or large-font text breaks the workflow;
- scanning requires reading every label.

Fix information architecture and alignment before shrinking anything.

## Whitespace audit

For each large gap, name its function. Keep it only when it establishes grouping, priority, rhythm, safe touch separation, or visual focus. Remove or reduce gaps whose only rationale is “modern,” “premium,” or “minimal.”
