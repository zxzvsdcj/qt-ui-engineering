# Local-Only docs Directory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep the complete `docs/` directory unchanged in the local workspace while removing it from the current public `main` branch and preventing future files under `docs/` from being tracked accidentally.

**Architecture:** Treat `docs/` as local workspace material through the repository-local `.git/info/exclude` file. Remove the directory only from Git's index with `git rm --cached`, so no local file is deleted. Update the bilingual README contract before untracking, and verify preservation with an exact path, byte-size, and SHA-256 manifest captured before the index operation.

**Tech Stack:** Git, PowerShell, Python `unittest`, repository validation script

## Global Constraints

- Do not delete or move any local file under `docs/`.
- Do not rewrite Git history or force-push. Older commits will continue to expose historical `docs/` content.
- Do not add a tracked `.gitignore`; use only `.git/info/exclude` for local-only rules.
- Do not change `scripts/validate_skill.py`; it does not require `docs/` for the published skill contract.
- Make only the README, contract-test, local exclude, and index changes described below.
- Push with a normal fast-forward update to `origin/main` only after all verification passes.

---

## Task 1: Define the public README contract

**Files:**

- Modify: `tests/test_skill_contract.py`
- Test: `tests/test_skill_contract.py`

- [ ] **Step 1: Add failing assertions**

In `SkillContractTests.test_bilingual_readmes_are_complete_and_linked`, add these assertions beside the existing checks for local-only files:

```python
self.assertNotIn("docs/", chinese)
self.assertNotIn("docs/", english)
```

- [ ] **Step 2: Run the focused test and confirm the red state**

Run:

```powershell
python -B -m unittest tests.test_skill_contract.SkillContractTests.test_bilingual_readmes_are_complete_and_linked -v
```

Expected: `FAIL`, because both README files still list `docs/` in the project structure.

- [ ] **Step 3: Commit the contract test**

```powershell
git add tests/test_skill_contract.py
git commit -m "test: define local-only docs contract"
```

## Task 2: Remove the public README listing

**Files:**

- Modify: `README.md`
- Modify: `README.en.md`
- Test: `tests/test_skill_contract.py`

- [ ] **Step 1: Remove the Chinese project-tree entry**

Delete only this line from `README.md`:

```text
docs/                      已批准的设计与实施计划
```

- [ ] **Step 2: Remove the English project-tree entry**

Delete only this line from `README.en.md`:

```text
docs/                      approved design and implementation plan
```

- [ ] **Step 3: Run focused and repository validation**

Run:

```powershell
python -B -m unittest tests.test_skill_contract.SkillContractTests.test_bilingual_readmes_are_complete_and_linked -v
python -B scripts/validate_skill.py .
git diff --check
```

Expected: the focused test passes, the validator reports success, and `git diff --check` produces no output.

- [ ] **Step 4: Commit the README change**

```powershell
git add README.md README.en.md
git commit -m "docs: remove local-only docs listing"
```

## Task 3: Preserve the local directory and remove it from the index

**Files:**

- Modify locally: `.git/info/exclude`
- Remove from the Git index only: every tracked file under `docs/`
- Preserve locally: every file under `docs/`, including untracked files

- [ ] **Step 1: Capture the complete pre-operation manifest**

Run the following read-only command and retain its structured output in the execution record for comparison after the index change:

```powershell
$docsRoot = (Resolve-Path 'docs').Path
Get-ChildItem 'docs' -Recurse -File |
  ForEach-Object {
    [pscustomobject]@{
      Path = $_.FullName.Substring($docsRoot.Length + 1).Replace('\', '/')
      Size = $_.Length
      Sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    }
  } |
  Sort-Object Path |
  ConvertTo-Json -Depth 3
```

The manifest must cover both tracked and already-local-only files. Record the file count as well.

- [ ] **Step 2: Broaden the repository-local exclude rule**

In `.git/info/exclude`, replace only:

```text
docs/Qt_UI_Skills_会话完整记录.md
```

with:

```text
docs/
```

Keep the other local-only entries unchanged.

- [ ] **Step 3: Verify every local docs file is ignored**

Run:

```powershell
$unignored = @()
foreach ($file in Get-ChildItem 'docs' -Recurse -File) {
  git check-ignore -q --no-index -- $file.FullName
  if ($LASTEXITCODE -ne 0) { $unignored += $file.FullName }
}
if ($unignored.Count -gt 0) { throw "Unignored docs files: $($unignored -join ', ')" }
```

Expected: no exception.

- [ ] **Step 4: Remove docs only from Git's index**

Run:

```powershell
git rm --cached -r -- docs
```

Do not use a filesystem deletion command and do not omit `--cached`.

- [ ] **Step 5: Prove local preservation**

Re-run the manifest command from Step 1. Compare the before and after manifests exactly:

- identical file count;
- identical relative path set;
- identical byte size for every path;
- identical SHA-256 for every path.

Stop without committing if any difference exists.

- [ ] **Step 6: Verify the staged scope**

Run:

```powershell
git diff --cached --name-status
git ls-files -- docs
git status --short
```

Expected: the staged diff contains only deletions of formerly tracked `docs/` files; `git ls-files -- docs` is empty; local `docs/` files do not appear as untracked because `.git/info/exclude` covers the directory.

- [ ] **Step 7: Commit the index removal**

```powershell
git commit -m "chore: keep docs directory local only"
```

## Task 4: Verify and publish the current-main change

**Files:**

- Verify: complete repository
- Verify locally: `docs/`, `.git/info/exclude`
- Verify remotely: `origin/main`

- [ ] **Step 1: Run the full local verification suite**

Run:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/validate_skill.py .
git diff --check
git ls-files -- docs
git status --short --branch
```

Expected: all tests pass, validation succeeds, no whitespace errors are reported, `git ls-files -- docs` is empty, and the branch is clean ahead of `origin/main` only by the new commits.

- [ ] **Step 2: Reconfirm the local-only state**

Run:

```powershell
Test-Path 'docs'
Get-ChildItem 'docs' -Recurse -File | Select-Object FullName, Length
git check-ignore -v --no-index -- 'docs/Qt_UI_Skills_会话完整记录.md'
```

Expected: `docs/` exists, all expected files remain, and the ignore source is `.git/info/exclude` with the `docs/` rule. Reconfirm the final manifest still matches Task 3 Step 1.

- [ ] **Step 3: Push normally**

```powershell
git push origin main
```

Do not use `--force` or `--force-with-lease`.

- [ ] **Step 4: Verify the remote result**

Run:

```powershell
git fetch origin main
git rev-parse HEAD
git rev-parse origin/main
git ls-tree -r --name-only origin/main -- docs
git show origin/main:README.md | Select-String -SimpleMatch 'docs/'
git show origin/main:README.en.md | Select-String -SimpleMatch 'docs/'
```

Expected: local and remote commit IDs are identical; the remote tree and both remote README searches produce no `docs/` result.

Open the public repository and confirm that the current `main` page no longer displays a `docs` directory. Acknowledge in the delivery note that the directory remains available through older commits because history was intentionally not rewritten.
