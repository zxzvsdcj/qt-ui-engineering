# Qt UI Engineering Evaluation Rubric

Score the agent's complete response, including its stack report, design decisions, implementation guidance, and self-review. Deterministic checks prove file structure and stack detection; this rubric evaluates judgment that cannot be reduced to a regex.

## Scoring

| Dimension | Weight | Full-credit evidence | Zero-credit condition |
|---|---:|---|---|
| Qt correctness | 20 | Uses only APIs, imports, framework patterns, and styling mechanisms valid for the detected stack | Mixes bindings/major versions or proposes an incompatible framework implementation |
| Task efficiency | 15 | Frequent actions are obvious, short, keyboard-aware, and placed near their working context | Buries primary work behind decorative navigation or repeated modal flows |
| Information density | 15 | Uses screen area efficiently while preserving scanability, hit targets, and hierarchy | Produces landing-page whitespace or an unreadably compressed interface |
| Readability and hierarchy | 10 | Content priority, grouping, labels, typography roles, and alignment are explicit | Relies on scale/whitespace decoration without meaningful structure |
| Interaction completeness | 10 | Covers focus, hover when relevant, pressed, selected, disabled, loading, empty, success, and error behavior | Describes only the resting visual state |
| Accessibility | 10 | Covers keyboard order, visible focus, accessible names, contrast, scaling, and non-color cues | Removes focus, requires pointer-only discovery, or uses color alone for meaning |
| Visual specificity | 10 | Visual direction follows the product domain and includes one restrained, justified signature | Reuses a generic SaaS/dashboard aesthetic without product rationale |
| Maintainability | 5 | Separates semantic tokens from framework translation and follows existing project patterns | Hardcodes scattered styling or introduces an unrequested compatibility layer |
| Review evidence | 5 | Findings name severity, evidence, consequence, and concrete remediation | Gives unprioritized taste opinions without observable evidence |

## Result

- Pass: at least 80/100.
- Automatic failure: Qt correctness is 0, any unrequested stack migration occurs, or a Blocking review finding remains unresolved.
- Record deterministic failures separately from subjective scoring.

## Severity

- **Blocking:** prevents task completion, uses the wrong Qt stack, breaks accessibility, or risks destructive action.
- **Major:** materially reduces efficiency, clarity, interaction completeness, or maintainability.
- **Minor:** localized inconsistency with limited task impact.
- **Enhancement:** optional improvement that has a product-specific benefit.
