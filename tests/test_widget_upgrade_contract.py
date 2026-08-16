import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE_ROOT = ROOT / ".cursor" / "rules" / "qt-ui-engineering"
STANDARD_GLOBS = (
    "**/*.py",
    "**/*.cpp",
    "**/*.h",
    "**/*.ui",
    "**/*.qrc",
)


class WidgetUpgradeContractTests(unittest.TestCase):
    def read_rule(self, name: str) -> str:
        path = RULE_ROOT / name
        self.assertTrue(path.is_file(), f"missing Cursor rule: {name}")
        return path.read_text(encoding="utf-8")

    def assert_standard_cursor_header(self, name: str) -> None:
        content = self.read_rule(name)
        self.assertTrue(content.startswith("---\n"), name)
        frontmatter = content.split("---", 2)[1]
        self.assertIn("description:", frontmatter, name)
        for glob in STANDARD_GLOBS:
            self.assertIn(f'"{glob}"', frontmatter, name)

    def test_meta_ux_and_icon_baselines_exist(self):
        names = ("0-meta.md", "08-ux-interaction.md", "09-icon-system.md")
        for name in names:
            with self.subTest(name=name):
                self.assert_standard_cursor_header(name)

    def test_meta_declares_widget_scope_and_global_priorities(self):
        content = self.read_rule("0-meta.md")
        required = (
            "Qt Widget",
            "Hi‑DPI",
            "Model‑View",
            "UI布局状态",
            "资源",
            "setFixedSize",
            "QTableWidget/QListWidget",
            "绝对文件路径",
            "实现与UX说明",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)

    def test_ux_addendum_links_dialog_and_long_task_guidance(self):
        content = self.read_rule("08-ux-interaction.md")
        self.assertIn("11-window_dialog.md", content)
        self.assertIn("长任务", content)
        self.assertIn("取消", content)


if __name__ == "__main__":
    unittest.main()
