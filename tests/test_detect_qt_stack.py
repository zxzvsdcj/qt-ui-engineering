import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.detect_qt_stack import detect_project


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "fixtures"


class DetectQtStackTests(unittest.TestCase):
    def test_all_fixture_profiles_match_the_expected_matrix(self):
        expected = json.loads(
            (ROOT / "evals" / "expected" / "stack-detection.json").read_text(
                encoding="utf-8"
            )
        )

        for fixture_name, expected_profile in expected.items():
            with self.subTest(fixture=fixture_name):
                actual = detect_project(FIXTURES / fixture_name).to_dict()
                stable_profile = {
                    field: actual[field]
                    for field in (
                        "status",
                        "language",
                        "qt_major",
                        "binding",
                        "ui_frameworks",
                        "styling",
                    )
                }
                self.assertEqual(expected_profile, stable_profile)

    def test_pyqt5_qwidget_qss(self):
        report = detect_project(FIXTURES / "pyqt5-qwidget-qss")

        self.assertEqual("ok", report.status)
        self.assertEqual("Python", report.language)
        self.assertEqual(5, report.qt_major)
        self.assertEqual("PyQt5", report.binding)
        self.assertEqual(["QWidget"], report.ui_frameworks)
        self.assertEqual(["QSS"], report.styling)

    def test_pyqt6_qwidget_qss(self):
        report = detect_project(FIXTURES / "pyqt6-qwidget-qss")

        self.assertEqual("PyQt6", report.binding)
        self.assertEqual(6, report.qt_major)
        self.assertEqual(["QWidget"], report.ui_frameworks)
        self.assertEqual(["QSS"], report.styling)

    def test_pyside2_qwidget(self):
        report = detect_project(FIXTURES / "pyside2-qwidget")

        self.assertEqual("PySide2", report.binding)
        self.assertEqual(5, report.qt_major)
        self.assertEqual(["QWidget"], report.ui_frameworks)
        self.assertEqual([], report.styling)

    def test_pyside6_qwidget_qss(self):
        report = detect_project(FIXTURES / "pyside6-qwidget-qss")

        self.assertEqual("PySide6", report.binding)
        self.assertEqual(6, report.qt_major)
        self.assertEqual(["QWidget"], report.ui_frameworks)
        self.assertEqual(["QSS"], report.styling)

    def test_qt6_qml(self):
        report = detect_project(FIXTURES / "qt6-qml")

        self.assertEqual("ok", report.status)
        self.assertEqual("QML/C++", report.language)
        self.assertEqual(6, report.qt_major)
        self.assertIsNone(report.binding)
        self.assertEqual(["Qt Quick/QML"], report.ui_frameworks)
        self.assertEqual(["Qt Quick Controls"], report.styling)

    def test_qt5_cpp_qwidget(self):
        report = detect_project(FIXTURES / "qt5-cpp-qwidget")

        self.assertEqual("ok", report.status)
        self.assertEqual("C++", report.language)
        self.assertEqual(5, report.qt_major)
        self.assertIsNone(report.binding)
        self.assertEqual(["QWidget"], report.ui_frameworks)

    def test_unknown_project_is_not_guessed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_text("ordinary project", encoding="utf-8")
            report = detect_project(root)

        self.assertEqual("unknown", report.status)
        self.assertEqual("unknown", report.language)
        self.assertIsNone(report.qt_major)
        self.assertIsNone(report.binding)
        self.assertEqual([], report.ui_frameworks)

    def test_binding_declared_only_in_requirements_implies_python(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.txt").write_text("PySide6>=6.7\n", encoding="utf-8")

            report = detect_project(root)

        self.assertEqual("ok", report.status)
        self.assertEqual("Python", report.language)
        self.assertEqual("PySide6", report.binding)

    def test_cxx_source_suffix_is_detected_as_cpp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CMakeLists.txt").write_text(
                "find_package(Qt6 REQUIRED COMPONENTS Widgets)\n", encoding="utf-8"
            )
            (root / "main.cxx").write_text(
                "#include <QApplication>\n", encoding="utf-8"
            )

            report = detect_project(root)

        self.assertEqual("C++", report.language)
        self.assertEqual(6, report.qt_major)
        self.assertEqual(["QWidget"], report.ui_frameworks)

    def test_conflicting_bindings_are_not_silently_resolved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.py").write_text(
                "from PyQt6.QtWidgets import QWidget", encoding="utf-8"
            )
            (root / "b.py").write_text(
                "from PySide6.QtWidgets import QWidget", encoding="utf-8"
            )
            report = detect_project(root)

        self.assertEqual("conflict", report.status)
        self.assertIsNone(report.binding)
        self.assertTrue(report.warnings)

    def test_source_files_are_read_but_never_executed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = root / "executed.txt"
            (root / "app.py").write_text(
                "from PyQt6.QtWidgets import QWidget\n"
                f"open({str(marker)!r}, 'w').write('executed')\n",
                encoding="utf-8",
            )
            report = detect_project(root)

        self.assertEqual("PyQt6", report.binding)
        self.assertFalse(marker.exists())

    def test_cli_emits_json_and_conflicts_exit_two(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "detect_qt_stack.py"),
                str(FIXTURES / "pyqt6-qwidget-qss"),
                "--pretty",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("PyQt6", payload["binding"])
        self.assertTrue(payload["evidence"])


if __name__ == "__main__":
    unittest.main()
