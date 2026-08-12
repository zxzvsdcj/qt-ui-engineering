# Accessibility

## Required behavior

- All interactive elements are reachable in a logical keyboard order.
- Focus is visible and is not conveyed only by subtle color change.
- Controls, icons, groups, and data views expose meaningful accessible names and roles.
- Pointer hover is supplementary; essential information has a keyboard/nonpointer path.
- Status, error, warning, and selection do not rely on color alone.
- Text remains readable under platform scaling and high DPI.
- Dialogs and overlays have predictable focus entry, Escape behavior, and focus return.

## Layout and language

- Support translated text expansion without clipping or overlapping controls.
- Mirror layout and directional icons for RTL when required.
- Use locale-aware date, time, number, and measurement formatting.
- Avoid culturally ambiguous icons for consequential actions.
- Do not embed user-visible text in images.

## Contrast and targets

Use the project's declared accessibility target. When none exists, check WCAG 2.2 AA contrast as a practical baseline: 4.5:1 for normal text and 3:1 for large text and essential UI boundaries. Verify rendered states, not only source token values.

Target size depends on platform and input. Preserve comfortable pointer targets and increase them for touch; never increase density by demanding precision input.

## Qt implementation review

Check focus policy/order, shortcut conflicts, accessible names/descriptions, model/view announcements, disabled/read-only distinction, palette groups, high-contrast behavior, large text, and screen-reader behavior available on the target platform.

Accessibility APIs and platform behavior vary by Qt version. Verify consequential implementation details against official documentation for the detected stack.
