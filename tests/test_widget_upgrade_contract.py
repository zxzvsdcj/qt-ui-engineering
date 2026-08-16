import ast
import json
import re
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

    def read_snippet(self, name: str) -> str:
        path = ROOT / "snippets" / name
        self.assertTrue(path.is_file(), f"missing snippet: {name}")
        return path.read_text(encoding="utf-8")

    def assert_standard_cursor_header(self, name: str) -> None:
        content = self.read_rule(name)
        self.assertTrue(content.startswith("---\n"), name)
        frontmatter = content.split("---", 2)[1]
        self.assertIn("description:", frontmatter, name)
        for glob in STANDARD_GLOBS:
            self.assertIn(f'"{glob}"', frontmatter, name)

    def assert_directive_structure(self, name: str) -> None:
        content = self.read_rule(name)
        for fragment in ("场景", "推荐做法", "不推荐/禁止", "参考来源"):
            with self.subTest(name=name, fragment=fragment):
                self.assertIn(fragment, content)

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

    def test_hidpi_rule_covers_qt6_and_platform_boundaries(self):
        name = "10-hidpi_cross_platform.md"
        self.assert_standard_cursor_header(name)
        self.assert_directive_structure(name)
        content = self.read_rule(name)
        for fragment in (
            "逻辑像素",
            "设备像素",
            "PointSize",
            "Windows",
            "macOS",
            "Linux",
            "PyInstaller",
            "QT_SCALE_FACTOR",
            "PyQt-Fluent-Widgets",
            "Cura",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)
        self.assertNotIn("setFixedSize(", content)

    def test_window_dialog_rule_covers_selection_lifecycle_and_docks(self):
        name = "11-window_dialog.md"
        self.assert_standard_cursor_header(name)
        self.assert_directive_structure(name)
        content = self.read_rule(name)
        for fragment in (
            "QFileDialog",
            "QMessageBox",
            "QDialogButtonBox",
            "exec()",
            "show()",
            "ESC",
            "parent",
            "QDockWidget",
            "objectName",
            "BallonsTranslator",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)

    def test_model_view_rule_has_performance_contract(self):
        name = "12-model_view.md"
        self.assert_standard_cursor_header(name)
        self.assert_directive_structure(name)
        content = self.read_rule(name)
        for fragment in (
            "QTableView",
            "QAbstractTableModel",
            "data()",
            "beginInsertRows",
            "dataChanged",
            "QStyledItemDelegate",
            "QTreeView",
            "setUniformRowHeights",
            "Interactive",
            "ExtendedSelection",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)

    def test_state_rule_has_versioned_native_state_contract(self):
        name = "13-ui_state_persistence.md"
        self.assert_standard_cursor_header(name)
        self.assert_directive_structure(name)
        content = self.read_rule(name)
        for fragment in (
            "QSettings",
            "saveGeometry",
            "saveState",
            "QSplitter",
            "QHeaderView",
            "objectName",
            "版本",
            "默认",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)

    def test_resource_rule_has_qrc_and_packaging_contract(self):
        name = "14-resource_deploy.md"
        self.assert_standard_cursor_header(name)
        self.assert_directive_structure(name)
        content = self.read_rule(name)
        for fragment in (
            "qrc",
            ":/",
            "pyside6-rcc",
            "pyrcc6",
            "__file__",
            "PyInstaller",
            "--add-data",
            "SVG",
            "QSS",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)
        self.assertIsNone(re.search(r"[A-Za-z]:\\", content))

    def test_hidpi_and_dialog_snippets_are_parseable_and_safe(self):
        names = ("hidpi_init.py", "custom_dialog_template.py")
        for name in names:
            with self.subTest(name=name):
                content = self.read_snippet(name)
                ast.parse(content, filename=name)
                self.assertIn("PySide6", content)
                self.assertIn("PyQt6", content)
                self.assertNotIn("setFixedSize(", content)
                self.assertNotIn("QtQuick", content)

        hidpi = self.read_snippet("hidpi_init.py")
        self.assertIn("setHighDpiScaleFactorRoundingPolicy", hidpi)
        self.assertLess(
            hidpi.index("setHighDpiScaleFactorRoundingPolicy"),
            hidpi.index("QApplication(argv)"),
        )

        dialog = self.read_snippet("custom_dialog_template.py")
        self.assertIn("QDialogButtonBox", dialog)
        self.assertIn("StandardButton.Ok", dialog)
        self.assertIn("SettingsDialog(self)", dialog)
        self.assertIn("self._settings_dialog", dialog)
        self.assertIn("finished.connect", dialog)

    def test_data_state_and_resource_snippets_are_parseable(self):
        names = (
            "tableview_model_demo.py",
            "ui_persistence_helper.py",
            "resource_loader.py",
        )
        forbidden = (
            "QTableWidget",
            "QListWidget",
            "setUniformRowHeights",
            "setFixedSize(",
            "_MEIPASS",
            "QtQuick",
        )
        for name in names:
            with self.subTest(name=name):
                content = self.read_snippet(name)
                ast.parse(content, filename=name)
                self.assertIn("PySide6", content)
                self.assertIn("PyQt6", content)
                self.assertIsNone(re.search(r"[A-Za-z]:\\", content))
                for fragment in forbidden:
                    self.assertNotIn(fragment, content)

    def test_table_model_snippet_uses_model_view_and_header_state(self):
        content = self.read_snippet("tableview_model_demo.py")
        for fragment in (
            "QAbstractTableModel",
            "QTableView",
            "SelectionMode.SingleSelection",
            "SelectionBehavior.SelectRows",
            "ResizeMode.Interactive",
            "verticalHeader().setDefaultSectionSize",
            "horizontalHeader().saveState",
            "horizontalHeader().restoreState",
            "dataChanged",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, content)

    def test_persistence_and_resource_helpers_use_native_storage(self):
        state = self.read_snippet("ui_persistence_helper.py")
        for fragment in (
            "QSettings",
            "saveGeometry",
            "restoreGeometry",
            "saveState",
            "restoreState",
            "setObjectName",
            "closeEvent",
        ):
            with self.subTest(kind="state", fragment=fragment):
                self.assertIn(fragment, state)

        resources = self.read_snippet("resource_loader.py")
        for fragment in ("QFile", "__file__", 'startswith(\":/\")', "QIcon"):
            with self.subTest(kind="resource", fragment=fragment):
                self.assertIn(fragment, resources)

    def test_three_widget_upgrade_evals_match_requested_contracts(self):
        path = ROOT / "evals" / "evals.json"
        self.assertTrue(path.is_file(), "missing evals/evals.json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("qt-ui-engineering", payload["skill_name"])
        self.assertEqual(3, len(payload["evals"]))
        prompts = "\n".join(item["prompt"] for item in payload["evals"])
        for fragment in (
            "可折叠左侧侧边导航",
            "完整实现HiDPI适配",
            "展示数千条动态业务表格数据",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, prompts)
        for item in payload["evals"]:
            self.assertGreaterEqual(len(item["assertions"]), 3)

    def test_all_widget_upgrade_files_are_present(self):
        rule_names = (
            "0-meta.md",
            "08-ux-interaction.md",
            "09-icon-system.md",
            "10-hidpi_cross_platform.md",
            "11-window_dialog.md",
            "12-model_view.md",
            "13-ui_state_persistence.md",
            "14-resource_deploy.md",
        )
        snippet_names = (
            "hidpi_init.py",
            "custom_dialog_template.py",
            "tableview_model_demo.py",
            "ui_persistence_helper.py",
            "resource_loader.py",
        )
        eval_names = (
            "widget-comprehensive-persistence.md",
            "widget-hidpi-dialog-qrc.md",
            "widget-large-table-model-view.md",
        )
        required = (
            *(RULE_ROOT / name for name in rule_names),
            *(ROOT / "snippets" / name for name in snippet_names),
            *(ROOT / "evals" / "cases" / name for name in eval_names),
        )
        for path in required:
            with self.subTest(path=path):
                self.assertTrue(path.is_file())

    def test_root_skill_routes_widget_advanced_rules(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in (
            "10-hidpi_cross_platform.md",
            "11-window_dialog.md",
            "12-model_view.md",
            "13-ui_state_persistence.md",
            "14-resource_deploy.md",
        ):
            with self.subTest(name=name):
                self.assertIn(
                    f".cursor/rules/qt-ui-engineering/{name}", content
                )

    def test_existing_references_receive_only_targeted_addenda(self):
        spacing = (ROOT / "references" / "spacing-and-layout.md").read_text(
            encoding="utf-8"
        )
        qss = (ROOT / "references" / "adapters" / "qss.md").read_text(
            encoding="utf-8"
        )
        anti = (ROOT / "references" / "anti-ai-slop.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Hi-DPI Widget addendum", spacing)
        self.assertIn("Resource deployment addendum", qss)
        self.assertIn("Widget engineering anti-pattern index", anti)


if __name__ == "__main__":
    unittest.main()
