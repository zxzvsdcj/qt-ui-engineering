# Tasks 1–3 Report: Portable structure, Widget references, and skill router

## Changed files

- `SKILL.md`: condensed into a cross-runtime router that preserves the supported Qt stack, no-unrequested-migration rule, Information-Density First, Anti-AI-Slop, the five-part response contract, all required adapters, and direct canonical Widget reference links without Cursor-rule paths.
- `agents/openai.yaml`: added the required Codex metadata verbatim.
- `.cursor/rules/qt-ui-engineering/*.md`: retained exactly eight thin compatibility entrypoints, each with standard frontmatter and one direct canonical-reference link.
- `references/widget/meta.md`, `ux-interaction.md`, `icon-system.md`, `hidpi-cross-platform.md`, `window-dialog.md`, `model-view.md`, `ui-state-persistence.md`, and `resource-deployment.md`: hold the canonical advanced Widget guidance.
- `tests/test_skill_contract.py` and `tests/test_widget_upgrade_contract.py`: retain the new portable-resource contract coverage; advanced guidance assertions now read canonical references while compatibility entrypoints are separately constrained to remain thin.

## Test command and result

```text
python -m unittest tests.test_skill_contract tests.test_widget_upgrade_contract -v
```

Result: 25 passed; 1 expected failure. The only failure is `test_behavior_evals_cover_triggering_conflicts_and_routing`, because `evals/behavior-evals.json` does not exist. That file is owned by Task 5 and was intentionally not created or modified.

## Previously observed RED evidence

The initial run had 41 failures: the portable Widget links were absent from `SKILL.md`, `agents/openai.yaml` was missing, the root router still referenced Cursor-rule paths, and the migrated compatibility entrypoints no longer contained the engineering prose that the legacy helper still read. The canonical reference files and thin compatibility entrypoints were already partially migrated in the worktree; this task completed their integration.

## Self-review

- Confirmed there are exactly eight Cursor compatibility files, each eight lines long and each linking only to its matching canonical Widget reference.
- Confirmed `SKILL.md` contains no `.cursor/rules/` path, preserves every required adapter link, and directly routes all eight Widget references.
- Ran `git diff --check`; no whitespace errors were reported.
- Did not modify the validator, eval content, READMEs, detector, or snippets.
