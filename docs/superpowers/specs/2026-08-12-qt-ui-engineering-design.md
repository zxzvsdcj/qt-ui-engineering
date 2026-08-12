# Qt UI Engineering Skill — Design Specification

**Date:** 2026-08-12  
**Status:** Approved
**Project root:** `E:/cursor/qt-ui-engineering`  
**Skill name:** `qt-ui-engineering`

## 1. Purpose

Create a reusable Agent Skill for designing, implementing, reviewing, and improving user interfaces across the Qt ecosystem. The Skill must preserve the project's existing Qt technology stack while applying one coherent product-design system to Qt 5, Qt 6, Python bindings, C++, QWidget, Qt Quick/QML, Qt Designer, and the supported styling mechanisms.

The Skill is not a Qt API encyclopedia and is not a Web frontend design prompt. Its value is a stable workflow that combines:

- distinctive, product-specific visual direction;
- Qt-native architecture and interaction patterns;
- information-dense desktop efficiency;
- context-aware implementation adapters;
- repeatable visual, interaction, accessibility, and maintainability review.

## 2. Success criteria

The project is complete when all of the following are true:

1. `SKILL.md` has valid frontmatter, is under 500 lines, explains when the Skill applies, and routes the agent to only the references needed for the detected stack.
2. The Skill distinguishes universal design decisions from framework, binding, language, and Qt-version implementation decisions.
3. The supplied detector correctly classifies the six required evaluation fixtures:
   - PyQt5 + QWidget + QSS
   - PyQt6 + QWidget + QSS
   - PySide2 + QWidget
   - PySide6 + QWidget + QSS
   - Qt 6 + QML
   - Qt 5 + C++ + QWidget
4. The detector never silently resolves conflicting evidence; it reports conflicts or uncertainty for agent review.
5. Guidance never mixes PyQt and PySide imports, Qt 5 and Qt 6 APIs, or QWidget and QML implementation patterns.
6. Guidance explicitly prohibits unsolicited migrations between bindings, Qt versions, languages, or UI frameworks.
7. Information-Density First, Desktop Efficiency, and Anti-AI-Slop are operational rules with reviewable criteria, not slogans.
8. The project includes reusable design-brief, design-token, and UI-review templates.
9. Automated tests cover detector behavior and Skill structural validation, and pass using only the Python standard library.
10. The final repository contains no placeholders, broken internal links, invented Qt APIs, or undeclared third-party dependencies.

## 3. Scope

### Included

- Universal Qt product UI design principles.
- Information architecture, visual hierarchy, typography, color, spacing, density, interaction states, desktop UX, and accessibility.
- Project inspection and evidence-based stack detection.
- QWidget, Qt Quick/QML, and Qt Designer guidance.
- QSS, QPalette, QStyle/QProxyStyle, and Qt Quick Controls styling guidance.
- PyQt5, PyQt6, PySide2, PySide6, Qt 5 C++, and Qt 6 C++ compatibility notes.
- A design and implementation workflow plus a formal review checklist.
- Six fixture-based evaluations and deterministic local validation.

### Excluded

- Installing Qt SDKs or Python Qt bindings.
- Shipping complete production GUI applications for every supported stack.
- Automatically migrating an existing project to another Qt stack.
- Replacing official Qt documentation with exhaustive copied API documentation.
- Creating a universal compatibility abstraction across PyQt, PySide, Qt 5, and Qt 6.
- Adding third-party Python dependencies solely for Skill validation.

## 4. Architecture

### Layer 1 — Universal design system

This layer is independent of language, binding, and Qt UI framework. It defines:

- product purpose and visual direction;
- information architecture and hierarchy;
- Information-Density First;
- typography, color, spacing, borders, radii, elevation, control sizing, and states;
- navigation, feedback, empty/loading/error states, and interaction behavior;
- desktop efficiency, adaptive layouts, accessibility, and Anti-AI-Slop;
- review criteria shared by every Qt implementation.

### Layer 2 — Qt UI framework adapters

This layer translates the design intent into framework-appropriate patterns:

- `QWidget`: layouts, size policies, Model/View, splitters, docks, toolbars, tabs, property panels, and desktop window structure.
- `Qt Quick/QML`: declarative component composition, properties, bindings, states, layouts, models/delegates, and Qt Quick Controls styling.
- `Qt Designer`: safe ownership of generated UI artifacts, promotion/custom widgets, and separation of generated and handwritten code.
- Styling adapters: QSS, QPalette, QStyle/QProxyStyle, and QML/Qt Quick Controls themes.

### Layer 3 — language, binding, and version adapters

This layer records only meaningful implementation differences and constraints for:

- PyQt5 and PyQt6;
- PySide2 and PySide6;
- Qt 5 C++ and Qt 6 C++.

It must not duplicate the universal design system or the complete framework guidance.

## 5. Project-inspection and stack-detection model

The workflow inspects existing files before proposing or changing UI code. Evidence sources, in descending confidence, are:

1. imports/includes in source files and QML import versions;
2. declared dependencies in `pyproject.toml`, requirements files, setup metadata, CMake, qmake `.pro`, and `.pri` files;
3. UI artifacts such as `.ui`, `.qml`, `.qss`, and QWidget class usage;
4. user-provided platform and architecture constraints.

The detector emits a machine-readable report with:

- language;
- Qt major version;
- Python binding, when applicable;
- UI framework;
- styling systems;
- architecture hints;
- target-platform hints;
- evidence with source paths;
- warnings and conflicts.

Unknown fields remain `unknown`; they are not guessed. Conflicting bindings or incompatible Qt-major evidence produce warnings and a non-success validation state. The agent then asks one focused question only if reading more project context cannot resolve the conflict.

The detector is advisory. It does not edit files, install dependencies, import Qt modules, or execute project code.

## 6. Core design policy

### Information-Density First

In the presence of readable typography, scanability, interaction reachability, and clear visual hierarchy, maximize useful information per unit of screen area. Avoid functionless blank regions, excessively loose component spacing, oversized visual intervals, and decorative whitespace.

High information density does not mean crowding. Density must not be increased by shrinking text below readable sizes, reducing practical hit targets, erasing grouping, or weakening hierarchy. Space must express grouping, rhythm, priority, and interaction boundaries.

Desktop structures such as toolbars, splitters, tabs, tables, trees, inspectors, property panels, status bars, context menus, keyboard shortcuts, and multi-panel workflows are preferred when they improve task throughput.

### Anti-AI-Slop

The Skill rejects visual decisions made only because they are common in generated SaaS dashboards: universal card wrapping, arbitrary gradients, giant headings, excessive blank space, excessive radii and shadows, emoji icons, and decorative elements without product meaning.

Every visual direction must be justified by the product, users, content, platform, and task frequency. Native desktop conventions and operational efficiency take precedence over landing-page aesthetics.

### Technology preservation

The agent implements the best result within the detected stack. It must not migrate PyQt5 to PyQt6, PySide2 to PySide6, QWidget to QML, QML to QWidget, or C++ to Python unless the user explicitly requests a migration.

## 7. Execution workflow encoded by the Skill

1. Inspect relevant project files and existing UI patterns.
2. Detect the Qt stack and state evidence, uncertainty, and constraints.
3. Clarify the product task, users, target platform, and success criteria when not inferable.
4. Define information architecture before visual styling.
5. Choose a deliberate visual direction suitable for the product.
6. Define or align design tokens.
7. Design density, layout, navigation, and interaction behavior.
8. Select Qt-native components and the exact adapters for the current stack.
9. Implement the smallest change consistent with existing project patterns.
10. Review visual quality, information density, interaction states, desktop behavior, accessibility, Qt correctness, and maintainability.
11. Refine only issues supported by the review.

For implementation tasks, the agent must follow the host project's testing and verification rules. The Skill itself does not override project instructions.

## 8. File structure

```text
E:/cursor/qt-ui-engineering/
├── SKILL.md
├── README.md
├── docs/
│   ├── Qt_UI_Skills_会话完整记录.md
│   └── superpowers/specs/
│       └── 2026-08-12-qt-ui-engineering-design.md
├── references/
│   ├── design-philosophy.md
│   ├── information-density.md
│   ├── visual-system.md
│   ├── typography.md
│   ├── color-system.md
│   ├── spacing-and-layout.md
│   ├── interaction-and-feedback.md
│   ├── desktop-ux.md
│   ├── accessibility.md
│   ├── anti-ai-slop.md
│   ├── stack-detection.md
│   ├── ui-review-checklist.md
│   └── adapters/
│       ├── qwidget.md
│       ├── qt-quick-qml.md
│       ├── qt-designer.md
│       ├── qss.md
│       ├── qpalette-qstyle.md
│       ├── pyqt5.md
│       ├── pyqt6.md
│       ├── pyside2.md
│       ├── pyside6.md
│       ├── qt5-cpp.md
│       └── qt6-cpp.md
├── templates/
│   ├── design-tokens.md
│   ├── ui-design-brief.md
│   └── ui-review.md
├── examples/
│   ├── qwidget/README.md
│   ├── qml/README.md
│   └── themes/README.md
├── evals/
│   ├── rubric.md
│   ├── cases/
│   │   ├── pyqt5-qwidget-qss.md
│   │   ├── pyqt6-qwidget-qss.md
│   │   ├── pyside2-qwidget.md
│   │   ├── pyside6-qwidget-qss.md
│   │   ├── qt6-qml.md
│   │   └── qt5-cpp-qwidget.md
│   ├── expected/
│   │   └── stack-detection.json
│   └── fixtures/
│       └── six isolated minimal project trees
├── scripts/
│   ├── detect_qt_stack.py
│   └── validate_skill.py
└── tests/
    ├── test_detect_qt_stack.py
    └── test_validate_skill.py
```

Empty placeholder directories are not allowed. Example directories contain concise reference examples or explanations that serve the Skill without becoming separate sample applications.

## 9. Main Skill routing

`SKILL.md` contains:

- valid `name` and third-person `description` frontmatter;
- triggers covering Qt UI design, implementation, redesign, theming, review, QSS, QWidget, QML, Qt Quick, Qt Designer, PyQt, PySide, and Qt C++;
- the mandatory inspect/detect/design/adapt/implement/review workflow;
- routing tables from task type and detected stack to exact references;
- stop conditions for missing context, conflicting stack evidence, and requested migrations;
- concise quality gates and expected response format.

It omits `disable-model-invocation` so Qt UI work can trigger it automatically.

## 10. Templates and examples

- `design-tokens.md`: semantic token schema for color, typography, spacing, radii, borders, elevation, control sizes, density, and states. It remains technology-neutral and documents adapter mappings.
- `ui-design-brief.md`: product purpose, user, platform, tasks, density, layout, visual direction, existing constraints, and success criteria.
- `ui-review.md`: repeatable review report with severity, evidence, affected stack, and concrete remediation.
- Example notes demonstrate token translation and framework-specific implementation boundaries without pretending one code sample is portable across all Qt stacks.

## 11. Evaluation and testing

### Automated tests

Tests use `unittest`, `tempfile`, `pathlib`, and other Python standard-library modules. Test order is:

1. write detector and validator expectations;
2. run them and observe failure because implementations are absent;
3. implement the minimum scripts;
4. rerun until green.

Detector tests cover positive classification, unknown evidence, conflicts, and no execution/import side effects. Validator tests cover frontmatter, line count, required files, broken Markdown links, forbidden placeholders, and required evaluation fixtures.

### Skill evaluations

Each case supplies a representative user request and isolated fixture. The expected result evaluates:

- detection correctness;
- no API or binding mixing;
- universal-design consistency;
- correct adapter selection;
- Information-Density First;
- absence of AI-Slop patterns;
- UI-review completeness.

The rubric scores Qt correctness, information density, readability, hierarchy, desktop UX, accessibility, visual specificity, interaction completeness, and maintainability. Deterministic checks validate structure and stack selection; aesthetic quality remains a rubric-based agent evaluation and is not misrepresented as fully automated.

## 12. Documentation research policy

Implementation must synthesize design ideas rather than copy source text. Research will prioritize current primary sources:

- Qt official Agent Skills and Qt UI documentation;
- Anthropic's official frontend-design Skill;
- Microsoft's official frontend design-review guidance when available;
- other actively maintained primary-source design Skills only when they add a distinct practice.

External wording is paraphrased, source provenance is documented, and no long copyrighted passages are included. Version-sensitive Qt claims are verified against official documentation.

## 13. Error handling and risks

- **Ambiguous stacks:** report evidence and uncertainty instead of guessing.
- **Mixed repositories:** detection reports multiple stack profiles when separable; otherwise warns that the project requires scoped inspection.
- **QSS limitations:** guidance never treats QSS as browser CSS or recommends unsupported CSS custom properties.
- **Qt API drift:** adapters contain focused differences and direct the agent to current official docs rather than freezing exhaustive API tables.
- **Over-expansion:** examples remain minimal, and no full application or new dependency is added without a demonstrated evaluation need.
- **Aesthetic subjectivity:** rubric-based review is explicitly separated from deterministic validation.

## 14. Delivery

Final delivery includes:

1. the complete Skill project;
2. a concise README with installation/use instructions;
3. the final directory tree;
4. the stack-detection strategy;
5. the relationship between universal design and adapters;
6. a minimal invocation example;
7. research/source notes;
8. test and evaluation results;
9. known limitations and remaining risks.
