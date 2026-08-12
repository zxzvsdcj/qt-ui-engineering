# Local-Only Project Metadata Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove `.gitignore`, `findings.md`, `progress.md`, and `task_plan.md` from the public repository's current `main` tree while preserving their exact local contents and making public-clone validation independent of the local conversation record.

**Architecture:** Repository-local exclusions in `.git/info/exclude` replace the tracked `.gitignore` rules and keep all four files local-only. README and validator changes remove two public-clone dependencies, while focused regression tests prove those contracts before the files are untracked. Existing Git history is preserved and is not rewritten.

**Tech Stack:** Git, GitHub, Markdown, Python 3 standard-library `unittest`, PowerShell.

## Global Constraints

- Preserve the exact local contents of `.gitignore`, `findings.md`, `progress.md`, and `task_plan.md`.
- Remove those four paths only from the current tracked tree; do not rewrite Git history.
- Do not delete or recreate the GitHub repository and do not force-push.
- Store all local ignore rules only in `.git/info/exclude`.
- Keep `docs/Qt_UI_Skills_会话完整记录.md` local-only and ignored.
- Remove the `findings.md` link from both README files without changing other documentation content.
- Make `scripts/validate_skill.py` independent of the local conversation record.
- Add no dependency and modify no unrelated Skill behavior.

---

## File Map

- Modify `tests/test_skill_contract.py`: assert neither public README references `findings.md`.
- Modify `tests/test_validate_skill.py`: prove a complete public Skill fixture does not create or require the local conversation record.
- Modify `README.md`: remove the local research-record sentence.
- Modify `README.en.md`: remove the equivalent English sentence.
- Modify `scripts/validate_skill.py`: remove the local conversation record from `REQUIRED_FILES`.
- Modify locally, never commit: `.git/info/exclude`.
- Remove from Git index while preserving locally: `.gitignore`, `findings.md`, `progress.md`, `task_plan.md`.

### Task 1: Define public-document and public-clone contracts

**Files:**
- Modify: `tests/test_skill_contract.py`
- Modify: `tests/test_validate_skill.py`
- Test: `tests/test_skill_contract.py`
- Test: `tests/test_validate_skill.py`

**Interfaces:**
- Consumes: `README.md`, `README.en.md`, `REQUIRED_FILES`, `write_valid_skill`, and `validate_skill`.
- Produces: two regression assertions covering local-only metadata boundaries.

- [ ] **Step 1: Add the failing README assertions**

Append these assertions to `test_bilingual_readmes_are_complete_and_linked` after the existing local-conversation-record assertions:

```python
        self.assertNotIn("findings.md", chinese)
        self.assertNotIn("findings.md", english)
```

- [ ] **Step 2: Add the failing public-clone validation test**

Add this method to `ValidateSkillTests`:

```python
    def test_local_conversation_record_is_not_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_skill(root)
            local_record = root / "docs" / "Qt_UI_Skills_会话完整记录.md"

            issues = validate_skill(root)

            self.assertFalse(local_record.exists())

        self.assertEqual([], issues)
```

Before the validator change, `write_valid_skill` creates every entry in `REQUIRED_FILES`, so the `assertFalse` assertion proves the local record is still incorrectly considered public content.

- [ ] **Step 3: Run the two focused tests and verify their expected failures**

```text
python -B -m unittest tests.test_skill_contract.SkillContractTests.test_bilingual_readmes_are_complete_and_linked tests.test_validate_skill.ValidateSkillTests.test_local_conversation_record_is_not_required -v
```

Expected:

```text
test_bilingual_readmes_are_complete_and_linked ... FAIL
test_local_conversation_record_is_not_required ... FAIL
```

The first failure must report that `findings.md` is present. The second must report that the local record unexpectedly exists. Stop if either test fails for another reason.

- [ ] **Step 4: Commit the red contract tests**

```text
git add tests/test_skill_contract.py tests/test_validate_skill.py
git commit -m "test: define local-only metadata contracts"
```

### Task 2: Remove public references to local-only records

**Files:**
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `scripts/validate_skill.py`
- Test: `tests/test_skill_contract.py`
- Test: `tests/test_validate_skill.py`

**Interfaces:**
- Consumes: the failing contracts from Task 1.
- Produces: public documentation without a `findings.md` link and a validator whose `REQUIRED_FILES` excludes the local conversation record.

- [ ] **Step 1: Remove the local findings sentence from the Chinese README**

Delete only this line from `README.md`:

```markdown
详细的调研决策记录在 [findings.md](findings.md) 中。
```

- [ ] **Step 2: Remove the equivalent sentence from the English README**

Delete only this line from `README.en.md`:

```markdown
Detailed research decisions are recorded in [findings.md](findings.md).
```

- [ ] **Step 3: Remove the local conversation record from required public files**

Delete only this entry from `REQUIRED_FILES` in `scripts/validate_skill.py`:

```python
    "docs/Qt_UI_Skills_会话完整记录.md",
```

Do not change incomplete-marker scan behavior or any other required path.

- [ ] **Step 4: Run the focused tests and verify green**

```text
python -B -m unittest tests.test_skill_contract.SkillContractTests.test_bilingual_readmes_are_complete_and_linked tests.test_validate_skill.ValidateSkillTests.test_local_conversation_record_is_not_required -v
```

Expected: `Ran 2 tests` and `OK`.

- [ ] **Step 5: Verify README links and validator behavior**

```text
python -B scripts/validate_skill.py .
git diff --check
```

Expected: `OK: qt-ui-engineering skill is structurally valid` and no whitespace errors.

- [ ] **Step 6: Commit the public-clone fixes**

```text
git add README.md README.en.md scripts/validate_skill.py
git commit -m "fix: remove local-only public dependencies"
```

### Task 3: Preserve local files and remove them from the current Git tree

**Files:**
- Modify locally only: `.git/info/exclude`
- Preserve locally: `.gitignore`
- Preserve locally: `findings.md`
- Preserve locally: `progress.md`
- Preserve locally: `task_plan.md`
- Remove from Git index: `.gitignore`
- Remove from Git index: `findings.md`
- Remove from Git index: `progress.md`
- Remove from Git index: `task_plan.md`

**Interfaces:**
- Consumes: the four current tracked files and the existing three `.gitignore` rules.
- Produces: seven repository-local exclusion rules and a staged public-tree deletion without a filesystem deletion.

- [ ] **Step 1: Record the exact pre-operation hashes**

Run:

```powershell
$localOnly = @('.gitignore', 'findings.md', 'progress.md', 'task_plan.md')
$beforeHashes = @{}
foreach ($path in $localOnly) {
    $beforeHashes[$path] = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
}
$beforeHashes | ConvertTo-Json
```

Expected: four non-empty SHA-256 values. Keep this PowerShell session active through Step 5 or copy the JSON values for comparison.

- [ ] **Step 2: Add exact repository-local exclusion rules**

Append this block to `.git/info/exclude` using a surgical edit, preserving its existing comments:

```gitignore

# Local-only qt-ui-engineering workspace files
__pycache__/
*.py[cod]
docs/Qt_UI_Skills_会话完整记录.md
.gitignore
findings.md
progress.md
task_plan.md
```

- [ ] **Step 3: Verify every local exclusion before untracking**

```text
git check-ignore -v --no-index -- .gitignore findings.md progress.md task_plan.md docs/Qt_UI_Skills_会话完整记录.md scripts/__pycache__/module.pyc
```

Expected: six matching output lines sourced from `.git/info/exclude`. Do not untrack files if any path is missing.

- [ ] **Step 4: Remove only the four paths from the Git index**

```text
git rm --cached -- .gitignore findings.md progress.md task_plan.md
```

Expected: four `rm` messages. The command must not use filesystem deletion flags.

- [ ] **Step 5: Prove the local files are unchanged**

```powershell
$afterHashes = @{}
foreach ($path in $localOnly) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Local file was removed: $path"
    }
    $afterHashes[$path] = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
}
foreach ($path in $localOnly) {
    if ($beforeHashes[$path] -ne $afterHashes[$path]) {
        throw "Local file changed: $path"
    }
}
```

Expected: exit code 0 with no exception.

- [ ] **Step 6: Verify index and status behavior**

```text
git ls-files -- .gitignore findings.md progress.md task_plan.md
git status --short
```

Expected: `git ls-files` prints nothing. Status shows four staged deletions and does not show four untracked replacements.

- [ ] **Step 7: Commit the current-tree removal**

```text
git commit -m "chore: keep project metadata local only"
```

Expected: the commit records four file deletions. `.git/info/exclude` remains local and is not part of the commit.

### Task 4: Verify and publish

**Files:**
- Verify: `README.md`
- Verify: `README.en.md`
- Verify: `scripts/validate_skill.py`
- Verify locally: `.git/info/exclude` and the four local-only files.

**Interfaces:**
- Consumes: Tasks 1–3 commits and local exclusions.
- Produces: a tested `main` branch synchronized with the public repository.

- [ ] **Step 1: Run the complete test and structural validation suite**

```text
python -B -m unittest discover -s tests -v
python -B scripts/validate_skill.py .
git diff --check
```

Expected: all tests pass, the validator reports structural validity, and the whitespace check is silent.

- [ ] **Step 2: Verify the final local boundary**

Confirm all of these conditions in one read-only check:

```text
All four local-only files exist: yes
All four SHA-256 values match the pre-operation values: yes
git ls-files lists none of the four paths: yes
git status --short is empty: yes
.git/info/exclude matches all seven rules: yes
README.md contains findings.md: no
README.en.md contains findings.md: no
```

- [ ] **Step 3: Push normally without history rewriting**

```text
git push origin main
```

Expected: remote `main` advances normally. Do not use `--force` or `--force-with-lease`.

- [ ] **Step 4: Verify the public repository's current tree**

Using GitHub current-branch file queries, confirm that each path returns Not Found:

```text
.gitignore
findings.md
progress.md
task_plan.md
```

Also confirm:

```text
README.md exists and does not contain findings.md
README.en.md exists and does not contain findings.md
scripts/validate_skill.py does not require the local conversation record
Repository visibility is public
Local HEAD equals remote main
```

- [ ] **Step 5: Report the accepted history limitation**

State explicitly that the four paths were removed only from the current `main` tree and remain accessible through old commit history, matching the user's selected scheme 1.

## Self-Review Result

- Spec coverage: Tasks 1–4 cover local preservation, local exclusion, current-tree removal, README consistency, public-clone validation, tests, normal push, remote queries, and the accepted history limitation.
- Completeness scan: no deferred implementation instructions or unspecified error handling remain.
- Name consistency: all tasks use the exact four file paths and `test_local_conversation_record_is_not_required` consistently.
