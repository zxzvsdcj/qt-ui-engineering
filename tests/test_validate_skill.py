import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_skill import REQUIRED_FILES, validate_skill


CURSOR_RULE_HEADER = (
    "---\n"
    "description: Qt Widget engineering rule.\n"
    'globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]\n'
    "---\n"
)


def write_valid_skill(root: Path) -> None:
    expected_cases = {
        name: {
            "status": "ok",
            "language": "Python",
            "qt_major": 6,
            "binding": "PyQt6",
            "ui_frameworks": ["QWidget"],
            "styling": [],
        }
        for name in (
            "pyqt5-qwidget-qss",
            "pyqt6-qwidget-qss",
            "pyside2-qwidget",
            "pyside6-qwidget-qss",
            "qt6-qml",
            "qt5-cpp-qwidget",
        )
    }

    for relative in REQUIRED_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative == "SKILL.md":
            path.write_text(
                "---\n"
                "name: qt-ui-engineering\n"
                "description: Use when designing or reviewing Qt user interfaces.\n"
                "---\n"
                "# Qt UI Engineering\n"
                "[Design](references/design-philosophy.md)\n",
                encoding="utf-8",
            )
        elif relative == "evals/expected/stack-detection.json":
            path.write_text(
                json.dumps(expected_cases, indent=2), encoding="utf-8"
            )
        elif relative.startswith(".cursor/rules/"):
            path.write_text(
                CURSOR_RULE_HEADER + "# Valid Cursor rule\n\nComplete guidance.\n",
                encoding="utf-8",
            )
        elif path.suffix == ".md":
            path.write_text("# Valid reference\n\nComplete guidance.\n", encoding="utf-8")
        elif path.suffix == ".json":
            path.write_text("{}\n", encoding="utf-8")
        else:
            path.write_text("# validation fixture\n", encoding="utf-8")


def issue_codes(root: Path) -> set[str]:
    return {issue.code for issue in validate_skill(root)}


class ValidateSkillTests(unittest.TestCase):
    def test_frontmatter_description_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            skill = root / "SKILL.md"
            skill.write_text(
                "---\nname: qt-ui-engineering\n---\n# Skill\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("frontmatter-description", codes)

    def test_description_must_start_with_use_when(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            skill = root / "SKILL.md"
            skill.write_text(
                "---\n"
                "name: qt-ui-engineering\n"
                "description: Designs Qt interfaces.\n"
                "---\n# Skill\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("frontmatter-description-trigger", codes)

    def test_skill_md_must_be_under_five_hundred_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            skill = root / "SKILL.md"
            skill.write_text("\n".join(["line"] * 500), encoding="utf-8")

            codes = issue_codes(root)

        self.assertIn("skill-line-count", codes)

    def test_broken_relative_markdown_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            skill = root / "SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8")
                + "\n[Missing](references/missing.md)\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("broken-link", codes)

    def test_placeholder_in_instruction_surface_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            reference = root / "references" / "design-philosophy.md"
            reference.write_text("# Design\n\nTODO: finish this.\n", encoding="utf-8")

            codes = issue_codes(root)

        self.assertIn("placeholder", codes)

    def test_cursor_rule_without_standard_frontmatter_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            rule = root / ".cursor" / "rules" / "qt-ui-engineering" / "bad.md"
            rule.parent.mkdir(parents=True, exist_ok=True)
            rule.write_text("# Missing frontmatter\n", encoding="utf-8")

            codes = issue_codes(root)

        self.assertIn("cursor-rule-frontmatter", codes)

    def test_placeholder_in_cursor_rule_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            rule = root / ".cursor" / "rules" / "qt-ui-engineering" / "bad.md"
            rule.parent.mkdir(parents=True, exist_ok=True)
            rule.write_text(
                CURSOR_RULE_HEADER + "# Rule\n\n" + "FIX" + "ME: incomplete.\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("placeholder", codes)

    def test_historical_docs_are_excluded_from_placeholder_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            historical = root / "docs" / "history.md"
            historical.parent.mkdir(parents=True, exist_ok=True)
            historical.write_text("TODO appeared in an old conversation.", encoding="utf-8")

            codes = issue_codes(root)

        self.assertNotIn("placeholder", codes)

    def test_missing_required_file_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            (root / "references" / "accessibility.md").unlink()

            codes = issue_codes(root)

        self.assertIn("required-file", codes)

    def test_complete_minimal_skill_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)

            issues = validate_skill(root)

        self.assertEqual([], issues)

    def test_local_conversation_record_is_not_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            local_record = root / "docs" / "Qt_UI_Skills_会话完整记录.md"

            issues = validate_skill(root)

            self.assertFalse(local_record.exists())

        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
