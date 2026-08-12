# Typography

## Roles before sizes

Define a small role set: body, label, data, caption, section title, and window/page title. Prefer three or four active sizes on one screen. Use weight, alignment, case, and color deliberately; do not use size alone for hierarchy.

## Platform and brand

- Prefer the platform/system font when no brand requirement exists.
- Introduce a custom font only when licensing, packaging, glyph coverage, and fallback are solved.
- Use a characterful face with restraint; technical data often benefits from a dedicated tabular or monospace role.
- Follow the project's existing typography tokens before creating new ones.

## Readability

- Derive sizes from font metrics and platform scaling instead of treating raw pixels as universal.
- Body and label text must remain readable at the expected viewing distance.
- Use line height appropriate to the content; data rows can be tighter than prose.
- Align numeric columns for comparison and use tabular numerals when supported.
- Use elision only when the full value remains available through expansion, tooltip, detail panel, or copy action.

## Resize, localization, and DPI

- Test large system text and the target DPI range.
- Expect translated strings to expand; avoid fixed widths for user-visible text.
- Mirror directional layout and icons for RTL where required.
- Do not embed translatable text in images.
- Prefer layouts and size hints over fixed text geometry.

## Review

Check font availability, fallback glyphs, truncation, disabled contrast, numeric alignment, focus readability, and whether too many roles create noise.
