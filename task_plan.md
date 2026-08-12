# Qt UI Engineering Skill — Task Plan

## Goal

Implement the approved `qt-ui-engineering` Agent Skill directly in `E:/cursor/qt-ui-engineering`, validate it against six Qt stack fixtures, and publish each verified milestone to the private GitHub repository `zxzvsdcj/qt-ui-engineering`.

## Constraints

- Preserve the three-layer architecture: universal design, Qt UI framework adapters, and language/binding/version adapters.
- Do not add third-party runtime or test dependencies.
- Apply test-driven development to detector and validator scripts.
- Do not migrate or conflate Qt technology stacks.
- Keep `SKILL.md` below 500 lines and use progressive disclosure.
- Preserve the user-provided conversation record under `docs/`.
- Keep Git history incremental and push verified milestones.

## Phases

| Phase | Status | Exit condition |
|---|---|---|
| 1. Design and repository baseline | Complete | Approved specification and planning records are committed and pushed |
| 2. Research and implementation plan | Complete | Primary-source findings and a self-reviewed, task-level plan are saved |
| 3. Detection and validation tools | In progress | Failure-first tests pass using the Python standard library |
| 4. Skill core and universal references | Complete | `SKILL.md`, templates, and universal design guidance pass validation |
| 5. Qt adapters and examples | Complete | All required framework and stack adapters are complete and linked |
| 6. Six-stack evaluations | Complete | All fixture detections pass and rubric cases contain no placeholders |
| 7. Final verification and delivery | Pending | Full test suite, validator, link scan, source audit, and Git push succeed |

## Key decisions

- The remote repository is private by default to avoid publishing user-provided conversation content without explicit approval.
- The stack detector is advisory and static: it reads project text but never imports Qt packages or executes target code.
- Aesthetic evaluation remains rubric-based; deterministic validation does not claim to measure subjective visual quality.
- The repository itself is the Skill root, so `SKILL.md` is created at the project root rather than under `.cursor/skills/`.

## Errors and resolutions

| Error | Attempts | Resolution |
|---|---:|---|
| Public ChatGPT share returned no readable body | 1 | User supplied the complete conversation as a local Markdown file |
| Browser automation CLI unavailable | 1 | Stopped without installing dependencies; used the supplied local record |
| Initial Git inspection failed because the directory was not a repository | 1 | User explicitly requested repository initialization and remote creation |
