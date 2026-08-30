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
WIDGET_WRAPPER_TARGETS = {
    "0-meta.md": "meta.md",
    "08-ux-interaction.md": "ux-interaction.md",
    "09-icon-system.md": "icon-system.md",
    "10-hidpi_cross_platform.md": "hidpi-cross-platform.md",
    "11-window_dialog.md": "window-dialog.md",
    "12-model_view.md": "model-view.md",
    "13-ui_state_persistence.md": "ui-state-persistence.md",
    "14-resource_deploy.md": "resource-deployment.md",
}


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
        elif relative == "agents/openai.yaml":
            path.write_text(
                "interface:\n"
                '  display_name: "Qt UI Engineering"\n'
                '  short_description: "Design and review native Qt interfaces"\n'
                '  default_prompt: "Use $qt-ui-engineering to improve this Qt interface."\n',
                encoding="utf-8",
            )
        elif relative.startswith(".cursor/rules/"):
            name = Path(relative).name
            target = WIDGET_WRAPPER_TARGETS[name]
            path.write_text(
                CURSOR_RULE_HEADER
                + "# Valid Cursor rule\n\n"
                + f"Read [the canonical guidance](../../../references/widget/{target}).\n",
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
    def test_widget_upgrade_artifacts_are_required(self):
        required = set(REQUIRED_FILES)
        expected = {
            "agents/openai.yaml",
            ".cursor/rules/qt-ui-engineering/14-resource_deploy.md",
            *(f"references/widget/{target}" for target in WIDGET_WRAPPER_TARGETS.values()),
            "snippets/tableview_model_demo.py",
            "evals/cases/widget-large-table-model-view.md",
            "evals/evals.json",
            "tests/test_widget_upgrade_contract.py",
        }

        self.assertTrue(expected.issubset(required))

    def test_openai_metadata_requires_quoted_non_empty_interface_fields(self):
        invalid_metadata = (
            "interface:\n"
            '  display_name: "Qt UI Engineering"\n'
            '  default_prompt: "Use $qt-ui-engineering"\n',
            "interface:\n"
            '  display_name: "Qt UI Engineering"\n'
            '  short_description: ""\n'
            '  default_prompt: "Use $qt-ui-engineering"\n',
            "interface:\n"
            "  display_name: Qt UI Engineering\n"
            '  short_description: "Design and review native Qt interfaces"\n'
            '  default_prompt: "Use $qt-ui-engineering"\n',
        )

        for metadata in invalid_metadata:
            with self.subTest(metadata=metadata), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_valid_skill(root)
                metadata_path = root / "agents" / "openai.yaml"
                metadata_path.parent.mkdir(parents=True, exist_ok=True)
                metadata_path.write_text(metadata, encoding="utf-8")

                codes = issue_codes(root)

            self.assertIn("openai-metadata", codes)

    def test_openai_metadata_ignores_nested_interface_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            metadata_path = root / "agents" / "openai.yaml"
            metadata_path.write_text(
                "interface:\n"
                '  display_name: "Qt UI Engineering"\n'
                '  short_description: "Design and review native Qt interfaces"\n'
                '  default_prompt: ""\n'
                "  options:\n"
                '    default_prompt: "Use $qt-ui-engineering"\n',
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("openai-metadata", codes)

    def test_openai_metadata_requires_a_top_level_interface_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            metadata_path = root / "agents" / "openai.yaml"
            metadata_path.write_text(
                "plugin:\n"
                "  interface:\n"
                '    display_name: "Qt UI Engineering"\n'
                '    short_description: "Design and review native Qt interfaces"\n'
                '    default_prompt: "Use $qt-ui-engineering to improve this Qt interface."\n',
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("openai-metadata", codes)

    def test_openai_metadata_requires_skill_token_in_default_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            metadata_path = root / "agents" / "openai.yaml"
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata_path.write_text(
                "interface:\n"
                '  display_name: "Qt UI Engineering"\n'
                '  short_description: "Design and review native Qt interfaces"\n'
                '  default_prompt: "Improve this Qt interface."\n',
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("openai-metadata", codes)

    def test_widget_wrapper_requires_its_exact_canonical_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            wrapper = root / ".cursor" / "rules" / "qt-ui-engineering" / "09-icon-system.md"
            wrapper.write_text(
                CURSOR_RULE_HEADER
                + "# Valid Cursor rule\n\n"
                + "Read [the canonical guidance](../../../references/widget/meta.md).\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("canonical-widget-reference", codes)

    def test_widget_wrapper_cannot_duplicate_canonical_guidance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            wrapper = root / ".cursor" / "rules" / "qt-ui-engineering" / "09-icon-system.md"
            wrapper.write_text(
                CURSOR_RULE_HEADER
                + "# Valid Cursor rule\n\n"
                + "Read [the canonical guidance](../../../references/widget/icon-system.md).\n"
                + "\n".join("Duplicated guidance." for _ in range(8))
                + "\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("canonical-widget-reference", codes)

    def test_widget_wrapper_requires_exactly_one_canonical_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            wrapper = root / ".cursor" / "rules" / "qt-ui-engineering" / "09-icon-system.md"
            wrapper.write_text(
                CURSOR_RULE_HEADER
                + "# Valid Cursor rule\n\n"
                + "Read [the canonical guidance](../../../references/widget/icon-system.md).\n"
                + "See [another reference](../../../references/widget/meta.md).\n",
                encoding="utf-8",
            )

            codes = issue_codes(root)

        self.assertIn("canonical-widget-reference", codes)

    def test_canonical_widget_reference_cannot_have_cursor_frontmatter(self):
        for frontmatter_start in ("---\n", "--- \n"):
            with self.subTest(frontmatter_start=frontmatter_start), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_valid_skill(root)
                reference = root / "references" / "widget" / "meta.md"
                reference.parent.mkdir(parents=True, exist_ok=True)
                reference.write_text(
                    frontmatter_start
                    + "description: Widget guidance\n"
                    + "---\n"
                    + "# Canonical guidance\n",
                    encoding="utf-8",
                )

                codes = issue_codes(root)

            self.assertIn("canonical-widget-reference", codes)

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
