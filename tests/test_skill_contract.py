import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
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
