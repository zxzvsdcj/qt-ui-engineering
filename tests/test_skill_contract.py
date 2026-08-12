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

    def test_six_evaluation_cases_exist(self):
        cases = sorted((ROOT / "evals" / "cases").glob("*.md"))

        self.assertEqual(6, len(cases))


if __name__ == "__main__":
    unittest.main()
