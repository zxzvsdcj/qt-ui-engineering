# Spacing and Layout

## Encode relationships

Use smaller gaps inside a relationship and larger gaps between relationships. Alignment, shared headers, separators, and background roles can establish grouping more efficiently than blank space.

Start with a compact scale such as 4/8/12/16/24 logical pixels only when the project has no token system. Adjust for font metrics, DPI, native style metrics, touch targets, and the existing design language.

## Desktop composition

- Reserve stable regions for navigation, primary work, inspection, and persistent status.
- Use splitters when users benefit from allocating space between peer regions.
- Use docks when panels need reconfiguration, detachment, or saved workspaces.
- Use tabs for alternate views of the same context, not unrelated navigation.
- Use forms for heterogeneous fields and tables/trees for repeated or hierarchical entities.
- Keep frequent actions in toolbars or inline with their objects; place infrequent actions in menus or context menus.

## Adaptive behavior

Define the primary window range and intentional transitions:

1. At wide widths, show peer panels when simultaneous comparison matters.
2. At medium widths, collapse secondary inspectors or shorten secondary labels.
3. At narrow supported widths, stack or navigate between secondary regions without hiding primary status.

Do not solve a broken layout by adding an outer scroll area. Do not set fixed sizes unless the content or hardware surface is truly fixed.

## Review

Resize through the supported range and check minimum/maximum sizes, splitter limits, saved geometry, long text, large fonts, empty data, and dense data. No region should become unusable before the documented minimum size.

## Hi-DPI Widget addendum

For QWidget targets, treat layout geometry as logical pixels and derive control height from font metrics, style metrics, and the project's spacing tokens. Prefer point-sized fonts, scalable SVG icons, layout stretch, `sizePolicy`, `minimumSize`, and an initial `resize` over fixed child geometry. A main window must not use `setFixedSize` as a general layout strategy.

Verify 100%, 125%, 150%, and 200% scaling where the target platform supports them, then move the window between displays with different scale factors. Check long translations, larger system fonts, splitter minimums, dock contents, and custom-painted buffers with the correct device pixel ratio. Use `.cursor/rules/qt-ui-engineering/10-hidpi_cross_platform.md` for the complete Widget-only platform contract.
