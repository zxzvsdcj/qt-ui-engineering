#!/usr/bin/env python3
"""Validate the qt-ui-engineering Skill without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


UNIVERSAL_REFERENCES = (
    "design-philosophy.md",
    "information-density.md",
    "visual-system.md",
    "typography.md",
    "color-system.md",
    "spacing-and-layout.md",
    "interaction-and-feedback.md",
    "desktop-ux.md",
    "accessibility.md",
    "anti-ai-slop.md",
    "stack-detection.md",
    "ui-review-checklist.md",
)
ADAPTER_REFERENCES = (
    "qwidget.md",
    "qt-quick-qml.md",
    "qt-designer.md",
    "qss.md",
    "qpalette-qstyle.md",
    "pyqt5.md",
    "pyqt6.md",
    "pyside2.md",
    "pyside6.md",
    "qt5-cpp.md",
    "qt6-cpp.md",
)
CASE_NAMES = (
    "pyqt5-qwidget-qss",
    "pyqt6-qwidget-qss",
    "pyside2-qwidget",
    "pyside6-qwidget-qss",
    "qt6-qml",
    "qt5-cpp-qwidget",
)
WIDGET_RULE_NAMES = (
    "0-meta.md",
    "08-ux-interaction.md",
    "09-icon-system.md",
    "10-hidpi_cross_platform.md",
    "11-window_dialog.md",
    "12-model_view.md",
    "13-ui_state_persistence.md",
    "14-resource_deploy.md",
)
SNIPPET_NAMES = (
    "hidpi_init.py",
    "custom_dialog_template.py",
    "tableview_model_demo.py",
    "ui_persistence_helper.py",
    "resource_loader.py",
)
WIDGET_EVAL_NAMES = (
    "widget-comprehensive-persistence",
    "widget-hidpi-dialog-qrc",
    "widget-large-table-model-view",
)
REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    *(f"references/{name}" for name in UNIVERSAL_REFERENCES),
    *(f"references/adapters/{name}" for name in ADAPTER_REFERENCES),
    "templates/design-tokens.md",
    "templates/ui-design-brief.md",
    "templates/ui-review.md",
    "examples/qwidget/README.md",
    "examples/qml/README.md",
    "examples/themes/README.md",
    "evals/rubric.md",
    *(f"evals/cases/{name}.md" for name in CASE_NAMES),
    *(f"evals/cases/{name}.md" for name in WIDGET_EVAL_NAMES),
    "evals/evals.json",
    "evals/expected/stack-detection.json",
    "evals/fixtures/pyqt5-qwidget-qss/app.py",
    "evals/fixtures/pyqt5-qwidget-qss/theme.qss",
    "evals/fixtures/pyqt6-qwidget-qss/pyproject.toml",
    "evals/fixtures/pyqt6-qwidget-qss/app.py",
    "evals/fixtures/pyside2-qwidget/requirements.txt",
    "evals/fixtures/pyside2-qwidget/main.py",
    "evals/fixtures/pyside6-qwidget-qss/main.py",
    "evals/fixtures/pyside6-qwidget-qss/theme.qss",
    "evals/fixtures/qt6-qml/CMakeLists.txt",
    "evals/fixtures/qt6-qml/main.cpp",
    "evals/fixtures/qt6-qml/Main.qml",
    "evals/fixtures/qt5-cpp-qwidget/CMakeLists.txt",
    "evals/fixtures/qt5-cpp-qwidget/app.pro",
    "evals/fixtures/qt5-cpp-qwidget/main.cpp",
    "scripts/detect_qt_stack.py",
    "scripts/validate_skill.py",
    *(f".cursor/rules/qt-ui-engineering/{name}" for name in WIDGET_RULE_NAMES),
    *(f"snippets/{name}" for name in SNIPPET_NAMES),
    "tests/test_detect_qt_stack.py",
    "tests/test_skill_contract.py",
    "tests/test_validate_skill.py",
    "tests/test_widget_upgrade_contract.py",
)
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:TBD|TODO|FIXME)\b|implement\s+later|fill\s+in\s+details",
    re.IGNORECASE,
)
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CURSOR_RULE_GLOBS = (
    "**/*.py",
    "**/*.cpp",
    "**/*.h",
    "**/*.ui",
    "**/*.qrc",
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def validate_required_files(root: Path) -> list[ValidationIssue]:
    return [
        ValidationIssue("required-file", relative, "Required file is missing.")
        for relative in REQUIRED_FILES
        if not (root / relative).is_file()
    ]


def _parse_frontmatter(path: Path) -> tuple[dict[str, str], list[ValidationIssue]]:
    if not path.is_file():
        return {}, []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, [
            ValidationIssue(
                "frontmatter", path.name, "SKILL.md must start with YAML frontmatter."
            )
        ]
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, [
            ValidationIssue("frontmatter", path.name, "Frontmatter is not closed.")
        ]

    values: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values, []


def _cursor_rule_files(root: Path):
    directory = root / ".cursor" / "rules"
    if directory.is_dir():
        yield from sorted(directory.rglob("*.md"))


def validate_cursor_rules(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path in _cursor_rule_files(root):
        values, frontmatter_issues = _parse_frontmatter(path)
        if frontmatter_issues:
            issues.append(
                ValidationIssue(
                    "cursor-rule-frontmatter",
                    _relative(path, root),
                    "Cursor rule must start with closed YAML frontmatter.",
                )
            )
            continue

        content = path.read_text(encoding="utf-8")
        if not values.get("description") or any(
            f'"{glob}"' not in content for glob in CURSOR_RULE_GLOBS
        ):
            issues.append(
                ValidationIssue(
                    "cursor-rule-frontmatter",
                    _relative(path, root),
                    "Cursor rule requires description and the standard Qt file globs.",
                )
            )
    return issues


def validate_frontmatter(root: Path) -> list[ValidationIssue]:
    path = root / "SKILL.md"
    values, issues = _parse_frontmatter(path)
    if issues or not path.is_file():
        return issues

    name = values.get("name", "")
    description = values.get("description", "")
    if not name:
        issues.append(ValidationIssue("frontmatter-name", "SKILL.md", "name is required."))
    elif len(name) > 64 or not SKILL_NAME_PATTERN.fullmatch(name):
        issues.append(
            ValidationIssue(
                "frontmatter-name",
                "SKILL.md",
                "name must be at most 64 lowercase letters, numbers, or hyphens.",
            )
        )
    if not description:
        issues.append(
            ValidationIssue(
                "frontmatter-description", "SKILL.md", "description is required."
            )
        )
    else:
        if len(description) > 1024:
            issues.append(
                ValidationIssue(
                    "frontmatter-description",
                    "SKILL.md",
                    "description must be at most 1024 characters.",
                )
            )
        if not description.startswith("Use when"):
            issues.append(
                ValidationIssue(
                    "frontmatter-description-trigger",
                    "SKILL.md",
                    "description must start with 'Use when'.",
                )
            )
    return issues


def validate_skill_line_count(root: Path) -> list[ValidationIssue]:
    path = root / "SKILL.md"
    if not path.is_file():
        return []
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    if line_count >= 500:
        return [
            ValidationIssue(
                "skill-line-count",
                "SKILL.md",
                f"SKILL.md has {line_count} lines; it must have fewer than 500.",
            )
        ]
    return []


def _instruction_markdown_files(root: Path):
    direct = [root / "SKILL.md", root / "README.md", root / "evals" / "rubric.md"]
    for path in direct:
        if path.is_file():
            yield path
    yield from _cursor_rule_files(root)
    for directory in (
        root / "references",
        root / "templates",
        root / "examples",
        root / "evals" / "cases",
    ):
        if directory.is_dir():
            yield from sorted(directory.rglob("*.md"))


def validate_markdown_links(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    resolved_root = root.resolve()
    for path in _instruction_markdown_files(root):
        content = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_PATTERN.finditer(content):
            target = match.group(1).strip().strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            destination = (path.parent / target_path).resolve()
            try:
                destination.relative_to(resolved_root)
            except ValueError:
                issues.append(
                    ValidationIssue(
                        "broken-link",
                        _relative(path, root),
                        f"Relative link escapes the project root: {target}",
                    )
                )
                continue
            if not destination.exists():
                issues.append(
                    ValidationIssue(
                        "broken-link",
                        _relative(path, root),
                        f"Relative link does not resolve: {target}",
                    )
                )
    return issues


def validate_placeholders(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path in _instruction_markdown_files(root):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if PLACEHOLDER_PATTERN.search(line):
                issues.append(
                    ValidationIssue(
                        "placeholder",
                        _relative(path, root),
                        f"Placeholder marker on line {line_number}.",
                    )
                )
    return issues


def validate_expected_cases(root: Path) -> list[ValidationIssue]:
    path = root / "evals" / "expected" / "stack-detection.json"
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [ValidationIssue("expected-json", _relative(path, root), str(error))]

    issues: list[ValidationIssue] = []
    expected_names = set(CASE_NAMES)
    actual_names = set(payload) if isinstance(payload, dict) else set()
    if actual_names != expected_names:
        issues.append(
            ValidationIssue(
                "expected-cases",
                _relative(path, root),
                "Expected detection keys must match the six required cases.",
            )
        )
    return issues


def validate_skill(root: Path) -> list[ValidationIssue]:
    root = Path(root).resolve()
    issues: list[ValidationIssue] = []
    issues.extend(validate_required_files(root))
    issues.extend(validate_frontmatter(root))
    issues.extend(validate_cursor_rules(root))
    issues.extend(validate_skill_line_count(root))
    issues.extend(validate_markdown_links(root))
    issues.extend(validate_placeholders(root))
    issues.extend(validate_expected_cases(root))
    return sorted(issues, key=lambda item: (item.path, item.code, item.message))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the Qt UI Engineering Skill.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    issues = validate_skill(args.root)
    if issues:
        for issue in issues:
            print(f"{issue.code}: {issue.path}: {issue.message}")
        return 1
    print("OK: qt-ui-engineering skill is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
