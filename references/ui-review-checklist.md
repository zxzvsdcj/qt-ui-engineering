# UI Review Checklist

## Finding format

Every actionable finding contains:

- severity: `Blocking`, `Major`, `Minor`, or `Enhancement`;
- observable evidence and affected screen/component;
- user or engineering consequence;
- detected stack and relevant adapter;
- concrete remediation and verification.

## Visual system

- Visual direction is specific to the product and consistent.
- Typography roles, colors, borders, radii, elevation, and icons use tokens.
- Alignment and grouping reflect actual information relationships.
- Focus, selection, and hierarchy remain distinct in every theme.

## Information density

- No functionless large gaps, empty cards, or oversized titles.
- Frequent information and actions remain visible.
- Dense regions stay scannable and do not reduce readable text or usable targets.
- Tables, trees, forms, inspectors, and split views match the data relationships.

## Interaction and feedback

- Relevant default, hover, focus, pressed, selected, checked, disabled, loading, empty, stale, success, warning, and error states exist.
- Destructive actions communicate consequence and recovery.
- Long work shows progress/cancellation in the appropriate surface.
- Errors preserve context and explain recovery.

## Desktop behavior

- Window and panel resize ranges remain usable.
- Keyboard order, shortcuts, Escape, context menus, and focus return work.
- DPI, text scaling, saved layout state, and multiple input methods are verified.
- Large data uses appropriate models and incremental behavior.

## Accessibility

- Accessible names/roles are meaningful.
- Focus is visible and no keyboard trap exists.
- Meaning does not rely on color alone.
- Contrast, large text, localization expansion, and RTL are checked as required.

## Qt implementation

- APIs and imports match the detected binding and Qt version.
- QWidget, QML, and Designer ownership boundaries are correct.
- Styling uses only supported QSS/QPalette/QStyle/Qt Quick mechanisms.
- Theme mechanisms do not override the same property unpredictably.
- Existing project conventions and tests are preserved.

## Verdict

List Blocking and Major findings first. A design does not pass while a Blocking finding remains. Separate subjective visual improvements from deterministic Qt/API defects.
