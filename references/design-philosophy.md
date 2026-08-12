# Design Philosophy

## Ground the interface in the product

Before styling, name the product, its primary users, their frequent tasks, the screen's single main job, and the consequence of failure. Reuse real domain language and content. A visual direction is valid only when it helps those users recognize, compare, decide, or act.

## Make structure carry meaning

- Rank content as primary, secondary, and tertiary.
- Group by task, object, lifecycle, or dependency—not by a desire to create cards.
- Keep primary actions close to the information they affect.
- Use progressive disclosure for infrequent or advanced controls.
- Prefer recognition over recall: expose names, state, and available actions.
- Preserve wayfinding through stable navigation, selection, titles, and back/cancel paths.

## Choose a deliberate visual direction

State a compact direction before implementation:

1. **Tone:** technical, editorial, industrial, calm, playful, safety-critical, or another product-grounded quality.
2. **Material:** the domain's instruments, diagrams, signals, documents, or workflows.
3. **Signature:** one restrained element the product can own, such as a diagnostic status rail or distinctive comparison view.
4. **Restraint:** supporting surfaces remain quiet enough for work.

Do not choose a visual style because it is fashionable or easy to generate. Match complexity to the chosen direction.

## Preserve existing language

In an established project, inventory existing tokens, component roles, object names, icons, shortcuts, and state behavior. Extend them when they are coherent. If a local pattern causes the current problem, document that evidence and change only the affected boundary.

## Design copy as interface material

- Use words the user recognizes, not internal architecture terms.
- Action labels state the result: “Save changes,” not “Submit.”
- Keep an action's name consistent across button, progress, success, and error messages.
- Errors state what happened and how to recover.
- Empty states explain the next useful action.

## Decision test

Before keeping a design choice, answer:

- What user task does it help?
- What information relationship does it express?
- Is it appropriate for the detected Qt target and input methods?
- Would the same choice appear in an unrelated product? If yes, make it more specific or remove it.
