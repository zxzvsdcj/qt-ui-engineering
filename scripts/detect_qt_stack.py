#!/usr/bin/env python3
"""Statically detect Qt technology evidence without executing project code."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
TEXT_SUFFIXES = {
    ".cmake",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hh",
    ".hpp",
    ".pri",
    ".pro",
    ".py",
    ".qml",
    ".qss",
    ".toml",
    ".txt",
    ".ui",
}
SPECIAL_FILENAMES = {"CMakeLists.txt", "setup.cfg"}
BINDING_TO_QT_MAJOR = {"PyQt5": 5, "PyQt6": 6, "PySide2": 5, "PySide6": 6}
BINDING_PATTERN = re.compile(r"\b(PyQt5|PyQt6|PySide2|PySide6)\b")
QT_MAJOR_PATTERN = re.compile(r"\bQt([56])(?:::|\b)")
QWIDGET_PATTERN = re.compile(
    r"\b(?:QtWidgets|QApplication|QWidget|QMainWindow|QDialog|QTableView|"
    r"QTreeView|QListView|QSplitter|QDockWidget|QToolBar|QStatusBar)\b"
)
MODEL_VIEW_PATTERN = re.compile(
    r"\b(?:QAbstractItemModel|QAbstractTableModel|QAbstractListModel|"
    r"QTableView|QTreeView|QListView)\b"
)
PLATFORM_PATTERNS = {
    "Windows": re.compile(r"\b(?:Q_OS_WIN|WIN32)\b"),
    "macOS": re.compile(r"\b(?:Q_OS_MACOS|Q_OS_MAC|APPLE)\b"),
    "Linux/Unix": re.compile(r"\b(?:Q_OS_LINUX|UNIX)\b"),
}


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


def _is_candidate(path: Path) -> bool:
    return path.name in SPECIAL_FILENAMES or path.suffix.lower() in TEXT_SUFFIXES


def _iter_project_files(root: Path):
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRECTORIES for part in path.relative_to(root).parts):
            continue
        if _is_candidate(path):
            yield path


def _add_evidence(
    collected: set[Evidence], kind: str, value: str, path: Path, root: Path, line: int
) -> None:
    collected.add(
        Evidence(
            kind=kind,
            value=value,
            path=path.relative_to(root).as_posix(),
            line=line,
        )
    )


def _language_label(languages: set[str]) -> str:
    if not languages:
        return "unknown"
    if languages == {"QML", "C++"}:
        return "QML/C++"
    if languages == {"QML", "Python"}:
        return "Python/QML"
    if languages == {"Python", "C++"}:
        return "Python/C++"
    if len(languages) == 1:
        return next(iter(languages))
    return "/".join(sorted(languages))


def detect_project(root: Path) -> DetectionReport:
    """Inspect project text and return an evidence-backed Qt stack profile."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")

    evidence: set[Evidence] = set()
    warnings: list[str] = []
    bindings: set[str] = set()
    qt_majors: set[int] = set()
    languages: set[str] = set()
    frameworks: set[str] = set()
    styling: set[str] = set()
    architecture: set[str] = set()
    target_platforms: set[str] = set()

    for path in _iter_project_files(root):
        suffix = path.suffix.lower()
        if suffix == ".py":
            languages.add("Python")
        elif suffix in {".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp"}:
            languages.add("C++")
        elif suffix == ".qml":
            languages.add("QML")
            frameworks.add("Qt Quick/QML")
            _add_evidence(evidence, "ui-framework", "Qt Quick/QML", path, root, 1)
        elif suffix == ".qss":
            styling.add("QSS")
            _add_evidence(evidence, "styling", "QSS", path, root, 1)

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            warnings.append(f"Could not read {path.relative_to(root).as_posix()}: {error}")
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in BINDING_PATTERN.finditer(line):
                binding = match.group(1)
                bindings.add(binding)
                languages.add("Python")
                qt_majors.add(BINDING_TO_QT_MAJOR[binding])
                _add_evidence(evidence, "binding", binding, path, root, line_number)

            for match in QT_MAJOR_PATTERN.finditer(line):
                major = int(match.group(1))
                qt_majors.add(major)
                _add_evidence(evidence, "qt-major", str(major), path, root, line_number)

            if QWIDGET_PATTERN.search(line):
                frameworks.add("QWidget")
                _add_evidence(evidence, "ui-framework", "QWidget", path, root, line_number)

            if "QtQuick" in line or "QuickControls2" in line:
                frameworks.add("Qt Quick/QML")
                _add_evidence(
                    evidence, "ui-framework", "Qt Quick/QML", path, root, line_number
                )

            if "QtQuick.Controls" in line or "QuickControls2" in line:
                styling.add("Qt Quick Controls")
                _add_evidence(
                    evidence, "styling", "Qt Quick Controls", path, root, line_number
                )

            if "setStyleSheet" in line:
                styling.add("QSS")
                _add_evidence(evidence, "styling", "QSS", path, root, line_number)

            if MODEL_VIEW_PATTERN.search(line):
                architecture.add("Model/View")
                _add_evidence(
                    evidence, "architecture", "Model/View", path, root, line_number
                )

            for platform, pattern in PLATFORM_PATTERNS.items():
                if pattern.search(line):
                    target_platforms.add(platform)
                    _add_evidence(
                        evidence, "target-platform", platform, path, root, line_number
                    )

        if suffix == ".ui":
            styling.add("Qt Designer")
            _add_evidence(evidence, "styling", "Qt Designer", path, root, 1)

    conflict = False
    if len(bindings) > 1:
        conflict = True
        warnings.append("Conflicting Python Qt bindings: " + ", ".join(sorted(bindings)))
    if len(qt_majors) > 1:
        conflict = True
        warnings.append(
            "Conflicting Qt major versions: " + ", ".join(map(str, sorted(qt_majors)))
        )

    binding = next(iter(bindings)) if len(bindings) == 1 else None
    qt_major = next(iter(qt_majors)) if len(qt_majors) == 1 else None
    has_qt_evidence = bool(bindings or qt_majors or frameworks or styling)
    status = "conflict" if conflict else ("ok" if has_qt_evidence else "unknown")

    return DetectionReport(
        status=status,
        language=_language_label(languages),
        qt_major=qt_major,
        binding=binding,
        ui_frameworks=sorted(frameworks),
        styling=sorted(styling),
        architecture=sorted(architecture),
        target_platforms=sorted(target_platforms),
        evidence=sorted(evidence, key=lambda item: (item.path, item.line, item.kind, item.value)),
        warnings=warnings,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Statically detect Qt stack evidence in a project directory."
    )
    parser.add_argument("project", type=Path, help="Project directory to inspect")
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        report = detect_project(args.project)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    print(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=True,
        )
    )
    return 2 if report.status == "conflict" else 0


if __name__ == "__main__":
    raise SystemExit(main())
