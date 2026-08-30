import unittest
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_skill_has_portable_codex_metadata(self):
        path = ROOT / "agents" / "openai.yaml"

        self.assertTrue(path.is_file())
        content = path.read_text(encoding="utf-8")
        self.assertIn('display_name: "Qt UI Engineering"', content)
        self.assertIn('short_description: "Design and review native Qt interfaces"', content)
        self.assertIn("$qt-ui-engineering", content)

    def test_skill_declares_discoverable_trigger_metadata(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: qt-ui-engineering", content)
        self.assertIn("description: Use when", content)

    def test_skill_routes_all_required_stack_adapters(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        required_links = [
            "references/adapters/qwidget.md",
            "references/adapters/qt-quick-qml.md",
            "references/adapters/pyqt5.md",
            "references/adapters/pyqt6.md",
            "references/adapters/pyside2.md",
            "references/adapters/pyside6.md",
            "references/adapters/qt5-cpp.md",
            "references/adapters/qt6-cpp.md",
        ]

        for link in required_links:
            with self.subTest(link=link):
                self.assertIn(link, content)

    def test_skill_routes_portable_widget_references_without_cursor_paths(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        required_links = [
            "references/widget/meta.md",
            "references/widget/ux-interaction.md",
            "references/widget/icon-system.md",
            "references/widget/hidpi-cross-platform.md",
            "references/widget/window-dialog.md",
            "references/widget/model-view.md",
            "references/widget/ui-state-persistence.md",
            "references/widget/resource-deployment.md",
        ]

        for link in required_links:
            with self.subTest(link=link):
                self.assertIn(link, content)
        self.assertNotIn(".cursor/rules/", content)

    def test_skill_routes_universal_references_by_concern(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        expected_routes = {
            "design-philosophy.md": "product intent",
            "information-density.md": "information density",
            "visual-system.md": "visual system",
            "typography.md": "typography",
            "color-system.md": "color system",
            "spacing-and-layout.md": "spacing or layout",
            "interaction-and-feedback.md": "interaction or feedback",
            "desktop-ux.md": "desktop UX",
            "accessibility.md": "accessibility",
            "anti-ai-slop.md": "anti-AI-slop",
            "ui-review-checklist.md": "UI review",
        }

        for reference, concern in expected_routes.items():
            with self.subTest(reference=reference):
                self.assertIn(f"references/{reference}", content)
                self.assertIn(concern, content)
                self.assertRegex(
                    content,
                    rf"{re.escape(concern)}.*{re.escape(f'references/{reference}')}",
                )

    def test_skill_routes_templates_and_snippets_by_matching_concern(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        expected_routes = {
            "templates/design-tokens.md": "design tokens",
            "templates/ui-design-brief.md": "design brief",
            "templates/ui-review.md": "review artifact",
            "snippets/hidpi_init.py": "Hi-DPI initialization",
            "snippets/custom_dialog_template.py": "custom dialog",
            "snippets/tableview_model_demo.py": "large data table",
            "snippets/ui_persistence_helper.py": "UI state persistence",
            "snippets/resource_loader.py": "resource loading",
        }

        for reference, concern in expected_routes.items():
            with self.subTest(reference=reference):
                self.assertIn(reference, content)
                self.assertIn(concern, content)
                self.assertRegex(
                    content, rf"{re.escape(concern)}.*{re.escape(reference)}"
                )
        self.assertIn("PySide6 or PyQt6 QWidget", content)

    def test_skill_routes_each_widget_reference_by_concern(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        expected_routes = {
            "references/widget/meta.md": "Widget architecture",
            "references/widget/ux-interaction.md": "Widget interaction",
            "references/widget/icon-system.md": "Widget icon",
            "references/widget/hidpi-cross-platform.md": "Widget Hi-DPI",
            "references/widget/window-dialog.md": "Widget window or dialog",
            "references/widget/model-view.md": "Widget model-view",
            "references/widget/ui-state-persistence.md": "Widget state persistence",
            "references/widget/resource-deployment.md": "Widget resource deployment",
        }

        for reference, concern in expected_routes.items():
            with self.subTest(reference=reference):
                self.assertIn(reference, content)
                self.assertIn(concern, content)
                self.assertRegex(
                    content, rf"{re.escape(concern)}.*{re.escape(reference)}"
                )
        self.assertIn("Do not load all Widget references", content)

    def test_behavior_evals_cover_triggering_conflicts_and_routing(self):
        path = ROOT / "evals" / "behavior-evals.json"

        self.assertTrue(path.is_file())
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases = payload["evals"]
        ids = [case["id"] for case in cases]
        categories = {case["category"] for case in cases}
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            {
                "positive-trigger",
                "negative-trigger",
                "stack-conflict",
                "reference-routing",
            },
            categories,
        )
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["prompt"])
                self.assertTrue(case["expected_behavior"])
                self.assertTrue(case["forbidden_behavior"])

    def test_skill_contains_non_negotiable_design_policies(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("Information-Density First", content)
        self.assertIn("Anti-AI-Slop", content)
        self.assertIn("Do not migrate", content)
        self.assertIn("Detected stack", content)
        self.assertIn("Risks", content)

    def test_nine_evaluation_cases_exist(self):
        cases = sorted((ROOT / "evals" / "cases").glob("*.md"))

        self.assertEqual(9, len(cases))

    def test_bilingual_readmes_are_complete_and_linked(self):
        chinese = (ROOT / "README.md").read_text(encoding="utf-8")
        english = (ROOT / "README.en.md").read_text(encoding="utf-8")

        self.assertTrue(chinese.startswith("**简体中文** | [English](README.en.md)"))
        self.assertTrue(english.startswith("[简体中文](README.md) | **English**"))
        self.assertIn("# Qt UI 工程", chinese)
        self.assertIn("# Qt UI Engineering", english)

        chinese_headings = [
            "## 核心模型",
            "## 支持矩阵",
            "## 安装",
            "## 使用",
            "## 静态技术栈检测",
            "## 设计产物",
            "## 验证",
            "## 项目结构",
            "## 来源与综合方式",
            "## 已知限制",
        ]
        english_headings = [
            "## Core model",
            "## Supported matrix",
            "## Install",
            "## Use",
            "## Static stack detection",
            "## Design artifacts",
            "## Validate",
            "## Project structure",
            "## Sources and synthesis",
            "## Limitations",
        ]

        for heading in chinese_headings:
            with self.subTest(language="zh-CN", heading=heading):
                self.assertIn(heading, chinese)
        for heading in english_headings:
            with self.subTest(language="en", heading=heading):
                self.assertIn(heading, english)

        shared_fragments = [
            "git clone https://github.com/zxzvsdcj/qt-ui-engineering.git",
            "python scripts/detect_qt_stack.py <target-project> --pretty",
            "python -m unittest discover -s tests -v",
            "python scripts/validate_skill.py .",
            "PyQt5",
            "PyQt6",
            "PySide2",
            "PySide6",
            "Qt 5",
            "Qt 6",
        ]
        for fragment in shared_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, chinese)
                self.assertIn(fragment, english)

        self.assertNotIn("private GitHub repository", english)
        self.assertNotIn("Qt_UI_Skills_会话完整记录.md", chinese)
        self.assertNotIn("Qt_UI_Skills_会话完整记录.md", english)
        self.assertNotIn("findings.md", chinese)
        self.assertNotIn("findings.md", english)
        self.assertNotIn("docs/", chinese)
        self.assertNotIn("docs/", english)


if __name__ == "__main__":
    unittest.main()
