# Qt UI Engineering Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable, tested Agent Skill that applies one information-dense product-design system across Qt 5/6, PyQt, PySide, QWidget, Qt Quick/QML, Qt Designer, and Qt C++ without migrating or mixing stacks.

**Architecture:** `SKILL.md` performs inspect → detect → design → adapt → implement → review routing. Universal design references define invariant product and UX rules; framework and binding adapters translate them into the detected stack. Two standard-library Python tools provide static stack detection and deterministic structural validation, while six isolated fixtures and rubric cases exercise the required stacks.

**Tech Stack:** Agent Skills Markdown, Python 3 standard library (`argparse`, `dataclasses`, `json`, `pathlib`, `re`, `unittest`), Git.

## Global Constraints

- Project root is `E:/cursor/qt-ui-engineering`; `SKILL.md` lives at that root.
- Do not add third-party dependencies or import installed Qt packages in validation code.
- Do not migrate or conflate Qt versions, Python bindings, languages, or UI frameworks.
- Keep `SKILL.md` under 500 lines and route detailed knowledge through direct references.
- Preserve `docs/Qt_UI_Skills_会话完整记录.md` without editing its content.
- Use failure-first tests for stack detection and Skill validation.
- Report ambiguous or conflicting evidence; never guess a stack.
- Commit and push each independently verified task to `origin/main`.

---

## File responsibility map

- `scripts/detect_qt_stack.py`: read-only evidence scanner and JSON CLI.
- `scripts/validate_skill.py`: deterministic Skill structure/link/content/evaluation validator.
- `tests/test_detect_qt_stack.py`: detector behavior, six fixtures, conflict, and unknown-state tests.
- `tests/test_validate_skill.py`: frontmatter, line-count, link, placeholder, and full-project validation tests.
- `SKILL.md`: concise trigger, workflow, routing, stop conditions, and quality gates.
- `references/*.md`: universal design decisions independent of implementation technology.
- `references/adapters/*.md`: QWidget/QML/Designer/styling and binding/version-specific translation rules.
- `templates/*.md`: reusable brief, token schema, and review report.
- `examples/*/README.md`: minimal boundary examples; not standalone applications.
- `evals/fixtures/*`: isolated stack-detection inputs.
- `evals/cases/*.md`: agent evaluation prompts and required review assertions.
- `evals/expected/stack-detection.json`: exact detector expectations for six fixtures.
- `evals/rubric.md`: weighted qualitative evaluation separated from deterministic gates.
- `README.md`: installation, architecture, use, validation, sources, and limitations.

---

### Task 1: Static Qt stack detector and six fixtures

**Files:**
- Create: `tests/test_detect_qt_stack.py`
- Create: `scripts/detect_qt_stack.py`
- Create: `evals/fixtures/pyqt5-qwidget-qss/app.py`
- Create: `evals/fixtures/pyqt5-qwidget-qss/theme.qss`
- Create: `evals/fixtures/pyqt6-qwidget-qss/pyproject.toml`
- Create: `evals/fixtures/pyqt6-qwidget-qss/app.py`
- Create: `evals/fixtures/pyside2-qwidget/requirements.txt`
- Create: `evals/fixtures/pyside2-qwidget/main.py`
- Create: `evals/fixtures/pyside6-qwidget-qss/main.py`
- Create: `evals/fixtures/pyside6-qwidget-qss/theme.qss`
- Create: `evals/fixtures/qt6-qml/CMakeLists.txt`
- Create: `evals/fixtures/qt6-qml/main.cpp`
- Create: `evals/fixtures/qt6-qml/Main.qml`
- Create: `evals/fixtures/qt5-cpp-qwidget/app.pro`
- Create: `evals/fixtures/qt5-cpp-qwidget/main.cpp`

**Interfaces:**
- Produces: `Evidence(kind: str, value: str, path: str, line: int)`.
- Produces: `DetectionReport(status, language, qt_major, binding, ui_frameworks, styling, architecture, target_platforms, evidence, warnings)`.
- Produces: `detect_project(root: pathlib.Path) -> DetectionReport`.
- Produces: CLI `python scripts/detect_qt_stack.py <project> [--pretty]`, exit `0` for `ok`/`unknown`, exit `2` for `conflict`.

- [ ] **Step 1: Create isolated fixture evidence**

Use only minimal, valid-identifying text. Examples:

```python
# evals/fixtures/pyqt5-qwidget-qss/app.py
from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication([])
window = QMainWindow()
window.setStyleSheet(open("theme.qss", encoding="utf-8").read())
```

```cmake
# evals/fixtures/qt6-qml/CMakeLists.txt
cmake_minimum_required(VERSION 3.16)
project(QtQuickFixture LANGUAGES CXX)
find_package(Qt6 REQUIRED COMPONENTS Quick QuickControls2)
qt_add_executable(app main.cpp)
qt_add_qml_module(app URI Fixture QML_FILES Main.qml)
```

```cpp
// evals/fixtures/qt6-qml/main.cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>
int main(int argc, char *argv[]) {
    QGuiApplication app(argc, argv);
    QQmlApplicationEngine engine;
    engine.loadFromModule("Fixture", "Main");
    return app.exec();
}
```

```cpp
// evals/fixtures/qt5-cpp-qwidget/main.cpp
#include <QApplication>
#include <QMainWindow>
int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    QMainWindow window;
    window.show();
    return app.exec();
}
```

- [ ] **Step 2: Write detector tests before the implementation exists**

Cover all six expected profiles plus unknown and conflicting bindings:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.detect_qt_stack import detect_project

ROOT = Path(__file__).resolve().parents[1]

class DetectQtStackTests(unittest.TestCase):
    def test_pyqt5_qwidget_qss(self):
        report = detect_project(ROOT / "evals/fixtures/pyqt5-qwidget-qss")
        self.assertEqual("ok", report.status)
        self.assertEqual("PyQt5", report.binding)
        self.assertEqual(5, report.qt_major)
        self.assertIn("QWidget", report.ui_frameworks)
        self.assertIn("QSS", report.styling)

    def test_conflicting_bindings_are_not_silently_resolved(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.py").write_text("from PyQt6.QtWidgets import QWidget", encoding="utf-8")
            (root / "b.py").write_text("from PySide6.QtWidgets import QWidget", encoding="utf-8")
            report = detect_project(root)
        self.assertEqual("conflict", report.status)
        self.assertIsNone(report.binding)
        self.assertTrue(report.warnings)
```

- [ ] **Step 3: Run the detector tests and observe the required failure**

Run: `python -m unittest tests.test_detect_qt_stack -v`  
Expected: `ModuleNotFoundError: No module named 'scripts.detect_qt_stack'`.

- [ ] **Step 4: Implement the minimal static detector**

Use dataclasses, deterministic sorted traversal, ignored build/VCS directories, UTF-8 text reads with replacement, and explicit regex evidence. The core shape is:

```python
@dataclass(frozen=True)
class Evidence:
    kind: str
    value: str
    path: str
    line: int

@dataclass
class DetectionReport:
    status: str
    language: str
    qt_major: int | None
    binding: str | None
    ui_frameworks: list[str]
    styling: list[str]
    architecture: list[str]
    target_platforms: list[str]
    evidence: list[Evidence]
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

def detect_project(root: Path) -> DetectionReport:
    """Inspect text files without importing packages or executing project code."""
```

Binding evidence maps `PyQt5→5`, `PyQt6→6`, `PySide2→5`, `PySide6→6`. `find_package(Qt5|Qt6)` and qmake/CMake declarations supplement source imports. QWidget and QML may coexist without becoming a conflict; multiple Python bindings or both Qt major versions do become a conflict.

- [ ] **Step 5: Run detector tests and CLI smoke checks**

Run: `python -m unittest tests.test_detect_qt_stack -v`  
Expected: all detector tests pass.

Run: `python scripts/detect_qt_stack.py evals/fixtures/qt6-qml --pretty`  
Expected JSON fields include `"status": "ok"`, `"qt_major": 6`, and `"Qt Quick/QML"`.

- [ ] **Step 6: Commit and push Task 1**

```powershell
git add scripts/detect_qt_stack.py tests/test_detect_qt_stack.py evals/fixtures
git commit -m "feat: add static Qt stack detection"
git push
```

---

### Task 2: Main Skill router, universal references, and templates

**Files:**
- Create: `SKILL.md`
- Create: `references/design-philosophy.md`
- Create: `references/information-density.md`
- Create: `references/visual-system.md`
- Create: `references/typography.md`
- Create: `references/color-system.md`
- Create: `references/spacing-and-layout.md`
- Create: `references/interaction-and-feedback.md`
- Create: `references/desktop-ux.md`
- Create: `references/accessibility.md`
- Create: `references/anti-ai-slop.md`
- Create: `references/stack-detection.md`
- Create: `references/ui-review-checklist.md`
- Create: `templates/design-tokens.md`
- Create: `templates/ui-design-brief.md`
- Create: `templates/ui-review.md`

**Interfaces:**
- Consumes: `python scripts/detect_qt_stack.py <project> --pretty`.
- Produces: exact reference routing based on task and detected stack.
- Produces: universal semantic token tiers: primitive → semantic → component.

- [ ] **Step 1: Author `SKILL.md` frontmatter and routing contract**

Use this metadata and no `disable-model-invocation` field:

```yaml
---
name: qt-ui-engineering
description: Designs, implements, reviews, and improves professional Qt user interfaces across PyQt5, PyQt6, PySide2, PySide6, Qt C++, QWidget, Qt Quick/QML, Qt Designer, QSS, QPalette, and QStyle. Use for Qt UI architecture, layouts, theming, design systems, interaction states, accessibility, information-dense desktop UX, visual redesigns, and UI code review.
---
```

The body must contain: non-negotiable inspect-before-design rules; the three layers; the 11-step workflow; task and stack routing tables; conflict/migration stop conditions; Information-Density First; Anti-AI-Slop; review gates; and the expected response sections `Detected stack`, `Design intent`, `Implementation`, `Review`, `Risks`.

- [ ] **Step 2: Author universal design references**

Give each file one responsibility and concrete decisions:

- `design-philosophy.md`: product/audience/task grounding, one justified signature idea, content hierarchy, preservation of existing design language.
- `information-density.md`: density levels, spacing rhythm, grouping, scanability, no functionless whitespace, crowding failure modes.
- `visual-system.md`: primitive/semantic/component tokens and state roles.
- `typography.md`: platform fonts by default, semantic roles, readable scaling, elision/wrapping, localization expansion.
- `color-system.md`: semantic roles, light/dark/high-contrast states, no color-only meaning, palette groups.
- `spacing-and-layout.md`: 4/8/12/16/24 rhythm as a starting scale, relationship-based spacing, resize ranges, split views.
- `interaction-and-feedback.md`: hover/focus/pressed/selected/checked/disabled/loading/error/success, latency and cancellation.
- `desktop-ux.md`: menu/toolbar/status/dock/context menu/shortcuts, resizable workflows, destructive actions.
- `accessibility.md`: keyboard order, focus visibility, accessible names, contrast, text scaling, RTL/localization.
- `anti-ai-slop.md`: forbidden defaults and context-specific visual-direction test.
- `stack-detection.md`: evidence precedence, JSON interpretation, conflict behavior, manual fallback.
- `ui-review-checklist.md`: severity (`Blocking`, `Major`, `Minor`, `Enhancement`), evidence, and eight review dimensions.

- [ ] **Step 3: Author reusable templates**

`design-tokens.md` defines exact tables for primitive, semantic, component, typography, spacing, control size, density, motion, and state tokens. `ui-design-brief.md` records product, users, platform, frequent tasks, existing stack, content hierarchy, density, visual direction, and measurable success. `ui-review.md` records summary, detected stack, findings with severity/evidence/remediation, quality gates, and residual risks.

- [ ] **Step 4: Run manual structural checks**

Run: `(Get-Content SKILL.md).Count`  
Expected: integer below `500`.

Run: `rg -n "TBD|TODO|FIXME|:root|var\(--|box-shadow" SKILL.md references templates`  
Expected: no placeholders; Web-only syntax appears only in explicitly prohibited examples.

- [ ] **Step 5: Commit and push Task 2**

```powershell
git add SKILL.md references templates
git commit -m "feat: define universal Qt UI design workflow"
git push
```

---

### Task 3: Qt framework, styling, binding, and version adapters

**Files:**
- Create: `references/adapters/qwidget.md`
- Create: `references/adapters/qt-quick-qml.md`
- Create: `references/adapters/qt-designer.md`
- Create: `references/adapters/qss.md`
- Create: `references/adapters/qpalette-qstyle.md`
- Create: `references/adapters/pyqt5.md`
- Create: `references/adapters/pyqt6.md`
- Create: `references/adapters/pyside2.md`
- Create: `references/adapters/pyside6.md`
- Create: `references/adapters/qt5-cpp.md`
- Create: `references/adapters/qt6-cpp.md`
- Create: `examples/qwidget/README.md`
- Create: `examples/qml/README.md`
- Create: `examples/themes/README.md`

**Interfaces:**
- Consumes: universal semantic tokens and detected stack.
- Produces: framework-correct implementation rules without cross-stack compatibility shims.

- [ ] **Step 1: Author framework adapters**

`qwidget.md` must cover `QMainWindow`, layouts, `QSizePolicy`, `sizeHint`, splitters/docks/tabs, Model/View, keyboard/focus, DPI and resize testing; it must reject absolute positioning, gratuitous fixed sizes, excessive nesting, and using `QScrollArea` to conceal broken layout.

`qt-quick-qml.md` must cover Qt Quick Layouts, properties/bindings/states, models/delegates, controls styling, focus/navigation, mirroring, and compile-time versus runtime style preservation; it must reject translating QSS or imperative QWidget composition into QML.

`qt-designer.md` must cover `.ui` ownership, generated-code boundaries, promoted widgets, object names as stable styling/test hooks, and regeneration safety.

- [ ] **Step 2: Author styling adapters**

`qss.md` must document supported Qt selectors, sub-controls, pseudo-states, specificity/cascade differences, dynamic-property repolishing, restrained complex-widget overrides, semantic token rendering, and the explicit prohibition on CSS variables, `!important`, arbitrary browser properties, and unverified sub-controls.

`qpalette-qstyle.md` must explain palette color roles/groups, native-style preservation, when `QProxyStyle` is justified, and why QSS, palette, and style ownership must not fight over the same visual property.

- [ ] **Step 3: Author binding/version adapters**

Each adapter contains import namespace, Qt major, enum style, application execution form, signal/slot/property vocabulary, UI loader/resource notes, and a short “never mix with” list. Required examples include:

```python
# PyQt5
from PyQt5.QtCore import Qt, pyqtSignal
alignment = Qt.AlignLeft
result = dialog.exec_()
```

```python
# PyQt6
from PyQt6.QtCore import Qt, pyqtSignal
alignment = Qt.AlignmentFlag.AlignLeft
result = dialog.exec()
```

```python
# PySide6
from PySide6.QtCore import Qt, Signal, Slot, Property
alignment = Qt.AlignmentFlag.AlignLeft
result = dialog.exec()
```

C++ adapters distinguish `find_package(Qt5 REQUIRED COMPONENTS Widgets)` with `target_link_libraries(app PRIVATE Qt5::Widgets)` from the corresponding `Qt6` CMake targets, and state that API details must be verified against the project's exact Qt minor version.

- [ ] **Step 4: Add concise boundary examples**

The QWidget example maps one semantic token set to palette roles and a generated QSS template; the QML example maps the same roles to a singleton/theme object; the themes example compares native palette, QSS, `QProxyStyle`, and Qt Quick Controls ownership. Examples must not claim one implementation is portable to every stack.

- [ ] **Step 5: Audit adapter isolation**

Run: `rg -n "PyQt5|PyQt6|PySide2|PySide6" references/adapters`  
Expected: binding names occur in their own adapter and explicit comparison sections only.

Run: `rg -n ":root|var\(--|!important" references/adapters/qss.md examples`  
Expected: matches only describe forbidden Web CSS patterns.

- [ ] **Step 6: Commit and push Task 3**

```powershell
git add references/adapters examples
git commit -m "feat: add context-aware Qt implementation adapters"
git push
```

---

### Task 4: Six scenario evaluations and expected detections

**Files:**
- Create: `evals/cases/pyqt5-qwidget-qss.md`
- Create: `evals/cases/pyqt6-qwidget-qss.md`
- Create: `evals/cases/pyside2-qwidget.md`
- Create: `evals/cases/pyside6-qwidget-qss.md`
- Create: `evals/cases/qt6-qml.md`
- Create: `evals/cases/qt5-cpp-qwidget.md`
- Create: `evals/expected/stack-detection.json`
- Create: `evals/rubric.md`
- Modify: `tests/test_detect_qt_stack.py`

**Interfaces:**
- Consumes: `DetectionReport.to_dict()` stable profile fields.
- Produces: fixture-name keyed expected profiles and nine-dimension rubric.

- [ ] **Step 1: Write expected profile JSON**

Use exact stable fields, excluding evidence line details:

```json
{
  "pyqt5-qwidget-qss": {"status":"ok","language":"Python","qt_major":5,"binding":"PyQt5","ui_frameworks":["QWidget"],"styling":["QSS"]},
  "pyqt6-qwidget-qss": {"status":"ok","language":"Python","qt_major":6,"binding":"PyQt6","ui_frameworks":["QWidget"],"styling":["QSS"]},
  "pyside2-qwidget": {"status":"ok","language":"Python","qt_major":5,"binding":"PySide2","ui_frameworks":["QWidget"],"styling":[]},
  "pyside6-qwidget-qss": {"status":"ok","language":"Python","qt_major":6,"binding":"PySide6","ui_frameworks":["QWidget"],"styling":["QSS"]},
  "qt6-qml": {"status":"ok","language":"QML/C++","qt_major":6,"binding":null,"ui_frameworks":["Qt Quick/QML"],"styling":["Qt Quick Controls"]},
  "qt5-cpp-qwidget": {"status":"ok","language":"C++","qt_major":5,"binding":null,"ui_frameworks":["QWidget"],"styling":[]}
}
```

- [ ] **Step 2: Add one table-driven expected-profile test**

Load the JSON, run all fixture directories, and compare the exact named stable fields. Run the test and correct detector or fixture evidence one change at a time.

- [ ] **Step 3: Author evaluation cases**

Each case includes: representative user request, fixture path, expected detected stack, required references, prohibited migration/API mixing, Information-Density First assertion, Anti-AI-Slop assertion, interaction/accessibility review, and pass conditions. Case-specific tasks are: data-heavy settings page, monitoring table, legacy property editor, analysis workspace, QML control panel, and Qt 5 C++ inspector.

- [ ] **Step 4: Author weighted rubric**

Use nine dimensions totaling 100: Qt correctness 20, task efficiency 15, information density 15, readability/hierarchy 10, interaction completeness 10, accessibility 10, visual specificity 10, maintainability 5, review evidence 5. Define `Pass >= 80`, no Qt-correctness zero, and no blocking finding.

- [ ] **Step 5: Run tests and commit**

Run: `python -m unittest tests.test_detect_qt_stack -v`  
Expected: all tests pass, including the six-profile table.

```powershell
git add evals tests/test_detect_qt_stack.py
git commit -m "test: add six-stack Qt skill evaluations"
git push
```

---

### Task 5: Deterministic Skill validator

**Files:**
- Create: `tests/test_validate_skill.py`
- Create: `scripts/validate_skill.py`

**Interfaces:**
- Produces: `ValidationIssue(code: str, path: str, message: str)`.
- Produces: `validate_skill(root: pathlib.Path) -> list[ValidationIssue]`.
- Produces: CLI `python scripts/validate_skill.py [root]`, exit `0` with `OK`, exit `1` with issues.

- [ ] **Step 1: Write validator tests before implementation**

Tests create temporary Skill trees from the exported `REQUIRED_FILES` list. A shared `write_valid_skill(root)` helper writes a valid frontmatter document, the required evaluation JSON, and minimal non-placeholder Markdown for every required path. Individual tests then make exactly one mutation and assert the corresponding issue code:

- remove `description` and expect `frontmatter-description`;
- expand `SKILL.md` to 500 body/frontmatter lines and expect `skill-line-count`;
- add `[missing](references/missing.md)` and expect `broken-link`;
- add a forbidden placeholder marker in `references/design-philosophy.md` and expect `placeholder`;
- leave the generated valid tree untouched and expect an empty issue list.

The placeholder scan includes `SKILL.md`, `README.md`, `references`, `templates`, `examples`, and `evals`, but excludes historical conversation, approved specs/plans, and progress records.

- [ ] **Step 2: Run and observe the required import failure**

Run: `python -m unittest tests.test_validate_skill -v`  
Expected: `ModuleNotFoundError: No module named 'scripts.validate_skill'`.

- [ ] **Step 3: Implement minimal validation functions**

Use a frontmatter delimiter parser, Markdown inline-link regex, root-contained path resolution, deterministic traversal, and exact issue codes:

```python
@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str

def validate_skill(root: Path) -> list[ValidationIssue]:
    issues = []
    issues.extend(validate_required_files(root))
    issues.extend(validate_frontmatter(root / "SKILL.md"))
    issues.extend(validate_skill_line_count(root / "SKILL.md", maximum=499))
    issues.extend(validate_markdown_links(root))
    issues.extend(validate_placeholders(root))
    issues.extend(validate_expected_fixtures(root))
    return sorted(issues, key=lambda item: (item.path, item.code, item.message))
```

- [ ] **Step 4: Run tests and validate the real project**

Run: `python -m unittest tests.test_validate_skill -v`  
Expected: all validator unit tests pass.

Run: `python scripts/validate_skill.py .`  
Expected: `OK: qt-ui-engineering skill is structurally valid`.

- [ ] **Step 5: Commit and push Task 5**

```powershell
git add scripts/validate_skill.py tests/test_validate_skill.py
git commit -m "test: add deterministic skill validation"
git push
```

---

### Task 6: README, source audit, and final verification

**Files:**
- Create: `README.md`
- Modify: `findings.md`
- Modify: `progress.md`
- Modify: `task_plan.md`

**Interfaces:**
- Consumes: detector and validator CLIs, approved architecture, source findings.
- Produces: install/use/validation documentation and final evidence.

- [ ] **Step 1: Write README**

Include: purpose, supported matrix, architecture diagram, installation by copying/cloning the repository as a Skill directory, trigger examples, minimal invocation, detector output example, validation commands, source acknowledgments/links, non-goals, and limitations. State that `scripts/detect_qt_stack.py` is advisory and must not replace reading relevant project files.

- [ ] **Step 2: Run full automated verification**

Run: `python -m unittest discover -s tests -v`  
Expected: all tests pass.

Run: `python scripts/validate_skill.py .`  
Expected: `OK: qt-ui-engineering skill is structurally valid`.

Run each fixture through the detector and compare the stable fields with `evals/expected/stack-detection.json`; expected: six matches and zero conflicts.

- [ ] **Step 3: Run content audits**

Run: `rg -n "TBD|TODO|FIXME|implement later|fill in" SKILL.md README.md references templates examples evals`  
Expected: no matches.

Run: `rg -n ":root|var\(--|!important" SKILL.md references templates examples`  
Expected: matches only in explicit warnings against unsupported Web CSS patterns.

Run: `git diff --check`  
Expected: no whitespace errors.

- [ ] **Step 4: Record final evidence and inspect Git state**

Update `task_plan.md` phases to Complete and record exact test counts/commands in `progress.md`. Run `git status --short` and review every changed file before committing.

- [ ] **Step 5: Commit, push, and verify remote**

```powershell
git add README.md findings.md progress.md task_plan.md
git commit -m "docs: complete Qt UI engineering skill delivery"
git push
```

Verify the pushed commit through the GitHub integration and report the repository URL, final commit SHA, tests, known limitations, and the moved conversation-record path.
