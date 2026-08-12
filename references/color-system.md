# Color System

## Semantic roles

Define color by function:

- window/background, panel/surface, raised, sunken;
- outline, separator, focus indicator;
- primary text, secondary/muted text, disabled text;
- interactive accent and accent text;
- selected background/text;
- success, warning, danger, and informational state.

Map roles to the project's design language. Do not mix vocabularies from multiple design systems without an explicit crosswalk.

## State and meaning

- Color is never the only carrier of status; add text, shape, pattern, or icon.
- Hover, focus, selection, and pressed states must remain distinguishable.
- Interactive accent must not decorate noninteractive surfaces in a misleading way.
- Warning and danger colors are reserved for meaningful consequence.
- Charts and status sets need distinguishable ordering under color-vision deficiencies.

## Themes

Design semantic mappings for light, dark, high-contrast, and disabled/inactive conditions as required. Do not create dark mode by mechanically inverting colors. Preserve hierarchy, state contrast, focus visibility, and native platform expectations.

For QWidget projects, decide whether each role belongs to `QPalette`, QSS, or custom style painting. Preserve `Active`, `Inactive`, and `Disabled` palette groups where palette owns the role.

## Verification

Check the project's accessibility target for text and essential UI contrast. Verify real rendered states rather than only token pairs: antialiasing, disabled roles, selection, overlays, and platform styling can change the result.
