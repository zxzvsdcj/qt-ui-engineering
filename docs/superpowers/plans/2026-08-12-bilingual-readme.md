# Bilingual README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the public GitHub repository render a complete Simplified Chinese `README.md` by default while preserving an equivalent English `README.en.md` with bidirectional language navigation.

**Architecture:** The two README files are hand-maintained Markdown documents with the same section order, commands, repository URL, technical identifiers, source links, evaluation matrix, and limitations. A focused contract test protects file presence, language navigation, Chinese default content, English preservation, and the public-repository wording.

**Tech Stack:** Markdown, Python 3 standard-library `unittest`, Git, GitHub.

## Global Constraints

- `README.md` is the Simplified Chinese default rendered by GitHub.
- `README.en.md` preserves the full English documentation.
- Both files use the exact language navigation specified in the approved design.
- Commands, paths, Skill name, Qt API names, source URLs, and repository URL remain untranslated and equivalent.
- The local conversation record remains ignored and is never linked from either README.
- No generator, dependency, or unrelated project file is added.

---

## File Map

- Create `README.en.md`: complete English project documentation and language navigation.
- Modify `README.md`: complete Simplified Chinese project documentation and language navigation.
- Modify `tests/test_skill_contract.py`: deterministic bilingual README contract checks.

### Task 1: Protect the bilingual README contract

**Files:**
- Modify: `tests/test_skill_contract.py`
- Test: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: repository-root `README.md` and `README.en.md` as UTF-8 Markdown.
- Produces: `SkillContractTests.test_bilingual_readmes_are_complete_and_linked`.

- [ ] **Step 1: Add the failing contract test**

Add this method to `SkillContractTests`:

```python
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
```

- [ ] **Step 2: Run the focused test and verify the missing English README failure**

Run:

```text
python -B -m unittest tests.test_skill_contract.SkillContractTests.test_bilingual_readmes_are_complete_and_linked -v
```

Expected: `ERROR` with `FileNotFoundError` for `README.en.md`.

- [ ] **Step 3: Commit the red test**

```text
git add tests/test_skill_contract.py
git commit -m "test: define bilingual README contract"
```

### Task 2: Publish equivalent Chinese and English README files

**Files:**
- Create: `README.en.md`
- Modify: `README.md`
- Test: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: the approved bilingual README design and the contract from Task 1.
- Produces: two UTF-8 GitHub Markdown entry documents linked to each other.

- [ ] **Step 1: Preserve the current English README**

Copy the complete current `README.md` content to `README.en.md`, then add this exact first line followed by one blank line:

```markdown
[简体中文](README.md) | **English**
```

Keep all current English sections, code blocks, source links, limitations, and public-repository wording unchanged.

- [ ] **Step 2: Replace the default README with the complete Chinese version**

Start `README.md` with:

```markdown
**简体中文** | [English](README.en.md)

# Qt UI 工程
```

Use these exact Chinese section headings in the same order as the English file:

```markdown
## 核心模型
## 支持矩阵
## 安装
## 使用
## 静态技术栈检测
## 设计产物
## 验证
## 项目结构
## 来源与综合方式
## 已知限制
```

Translate every explanatory paragraph, table label, list description, response-contract item, structure annotation, source annotation, and limitation into natural Simplified Chinese. Preserve the Mermaid diagram structure but translate only its human-readable node labels. Preserve these items byte-for-byte wherever they occur:

```text
qt-ui-engineering
SKILL.md
README.md
README.en.md
PyQt5
PyQt6
PySide2
PySide6
QWidget
Qt Quick/QML
Qt Quick Controls
Qt Designer
QSS
QPalette
QStyle
QProxyStyle
git clone https://github.com/zxzvsdcj/qt-ui-engineering.git .cursor/skills/qt-ui-engineering
python scripts/detect_qt_stack.py <target-project> --pretty
python -m unittest discover -s tests -v
python scripts/validate_skill.py .
```

Keep the two English invocation examples unchanged because they are copyable Agent prompts. Translate the surrounding explanation and the five response-contract labels as：`检测到的技术栈`、`设计意图`、`实现`、`审查`、`风险`。

The project-structure block must describe `docs/` as `已批准的设计与实施计划`, and the following paragraph must state that the original requirements record is retained only in the local workspace and excluded from version control, without naming or linking the file.

- [ ] **Step 3: Run the focused bilingual contract test**

Run:

```text
python -B -m unittest tests.test_skill_contract.SkillContractTests.test_bilingual_readmes_are_complete_and_linked -v
```

Expected: `Ran 1 test` and `OK`.

- [ ] **Step 4: Run structural link validation**

Run:

```text
python -B scripts/validate_skill.py .
```

Expected: `OK: qt-ui-engineering skill is structurally valid`.

- [ ] **Step 5: Review the two README files side by side**

Verify the following exact facts:

```text
README.md headings: 10 Chinese level-two headings
README.en.md headings: 10 English level-two headings
Evaluation fixtures listed in each file: 6
Language navigation present in each file: yes
Conversation-record filename present in either file: no
Private-repository wording present in either file: no
```

- [ ] **Step 6: Commit the bilingual documentation**

```text
git add README.md README.en.md
git commit -m "docs: add Chinese and English README files"
```

### Task 3: Verify and publish

**Files:**
- Verify: `README.md`
- Verify: `README.en.md`
- Verify: `tests/test_skill_contract.py`

**Interfaces:**
- Consumes: committed bilingual README documents and contract test.
- Produces: a clean, tested `main` branch synchronized with `origin/main`.

- [ ] **Step 1: Run the complete test suite**

```text
python -B -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 2: Run the Skill validator and whitespace check**

```text
python -B scripts/validate_skill.py .
git diff --check
```

Expected: validator reports the Skill is structurally valid and `git diff --check` prints no errors.

- [ ] **Step 3: Push the tested commits**

```text
git push origin main
```

Expected: remote `main` advances to the local `HEAD`.

- [ ] **Step 4: Verify the public GitHub result**

Confirm all of the following from the public repository:

```text
Repository visibility: public
Default branch: main
GitHub landing page title: Qt UI 工程
README.en.md is reachable through the English language link
docs/Qt_UI_Skills_会话完整记录.md returns Not Found
Local HEAD equals origin/main
Local git status is clean
```

## Self-Review Result

- Spec coverage: every approved file responsibility, navigation rule, consistency rule, implementation step, and verification criterion maps to Tasks 1–3.
- Completeness scan: no incomplete instructions or deferred implementation markers remain.
- Type and name consistency: both tests and documentation use `README.md`, `README.en.md`, and `test_bilingual_readmes_are_complete_and_linked` consistently.
