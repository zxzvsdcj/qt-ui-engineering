# Interaction and Feedback

## State inventory

For every interactive control or data surface, decide which states apply:

- default, hover, focus, pressed;
- selected, checked, mixed;
- disabled, read-only, unavailable;
- loading, empty, stale, reconnecting;
- success, warning, validation error, operation error.

Native styling may already implement a state. Verify it instead of restyling automatically.

## Feedback timing

- Direct manipulation should acknowledge input immediately.
- Short work can use local busy feedback; longer work needs progress, cancellation when safe, and a nonblocking location when the user can continue.
- Background work belongs in persistent status surfaces rather than repeated modal dialogs.
- Never blank the whole operational screen for a local refresh.

## Error prevention and recovery

- Disable invalid actions only when the reason is visible or discoverable.
- Validate close to the affected field and preserve the user's input.
- Offer undo for reversible work.
- Confirm destructive or irreversible actions and name the object/consequence.
- Keep Cancel, Back, Close, or Escape behavior predictable.

## Motion

Motion communicates state, relationship, or causality; it is not decoration. Use short, localized transitions and provide an instant reduced-motion path when the product supports animation. Do not animate geometry when it creates layout churn or harms interaction.

## Review

Exercise the complete state matrix with keyboard and pointer, then touch/hardware input where required. Check focus return after dialogs, modal escape, cancellation races, repeated actions, offline/reconnect behavior, and actionable error copy.
