# docs 目录本地保留设计规格

**日期：** 2026-08-12  
**状态：** 用户已批准  
**项目：** `qt-ui-engineering`

## 1. 目标

将整个 `docs/` 目录从公开仓库当前 `main` 文件树移除，同时完整保留在本地工作区，并防止目录中的现有文件和后续新增文件再次被提交。

本次沿用此前选择的方案 1：不重写 Git 历史。这意味着 `docs/` 中曾经提交过的文件仍可通过旧提交访问，但不再出现在 GitHub 当前项目文件列表中。

## 2. 当前目录边界

本地 `docs/` 当前包含七个文件：

- `docs/Qt_UI_Skills_会话完整记录.md`
- `docs/superpowers/plans/2026-08-12-bilingual-readme.md`
- `docs/superpowers/plans/2026-08-12-local-only-project-metadata.md`
- `docs/superpowers/plans/2026-08-12-qt-ui-engineering.md`
- `docs/superpowers/specs/2026-08-12-bilingual-readme-design.md`
- `docs/superpowers/specs/2026-08-12-local-only-project-metadata-design.md`
- `docs/superpowers/specs/2026-08-12-qt-ui-engineering-design.md`

本规格文件会成为第八个本地文件。实施计划随后会成为第九个本地文件。取消跟踪前必须以实际文件列表为准生成哈希清单，不能假定固定数量。

## 3. 本地排除机制

在不会被提交的 `.git/info/exclude` 中，将当前精确规则：

```gitignore
docs/Qt_UI_Skills_会话完整记录.md
```

替换为目录级规则：

```gitignore
docs/
```

目录级规则必须与现有本地规则共同保留：

```gitignore
__pycache__/
*.py[cod]
docs/
.gitignore
findings.md
progress.md
task_plan.md
```

该规则会覆盖 `docs/` 中的所有现有文件和后续新增文件。

## 4. 远程移除方式

使用仅取消 Git 索引跟踪的递归操作移除 `docs/`，不得删除本地目录或文件。提交后，公开仓库当前 `main` 文件树中不再包含 `docs/`。

本次操作明确禁止：

- 删除本地 `docs/`；
- 删除或重建 GitHub 仓库；
- 使用强制推送；
- 重写提交历史；
- 清除旧提交对象。

## 5. README 一致性

中英文 README 的项目结构代码块当前分别包含：

```text
docs/                      已批准的设计与实施计划
docs/                      approved design and implementation plan
```

目录从公开仓库移除后，这两行会描述不存在的公开内容，因此必须删除。README 中其他结构条目、语言切换、命令、来源和限制保持不变。

契约测试增加两项断言，确保 `README.md` 与 `README.en.md` 不包含 `docs/`。

## 6. 验证器与测试边界

`scripts/validate_skill.py` 当前不要求 `docs/` 中的任何文件，无需修改。

`tests/test_validate_skill.py` 中出现本地会话路径，是为了证明验证器不会创建或要求该文件；该测试是公开克隆安全契约的一部分，应保留。它不会创建仓库中的 `docs/` 目录。

## 7. 实施范围

### 仅本地修改

- 将 `.git/info/exclude` 的会话记录精确规则替换为 `docs/`。
- 保留 `docs/` 内所有文件及内容。

### 提交到远程

- 在中英文 README 中删除项目结构里的 `docs/` 条目。
- 增加 README 契约测试，防止再次公开描述 `docs/`。
- 从 Git 索引递归移除当前已跟踪的 `docs/` 文件。

### 不在范围内

- 修改 Skill 核心指导、适配器、检测器或验证器。
- 移除其他公开目录。
- 重写历史或彻底清除旧文件对象。

## 8. 安全操作顺序

1. 运行基线测试和 Skill 校验。
2. 添加 README 契约测试并观察它因现有 `docs/` 条目而失败。
3. 删除中英文 README 的两行目录描述，使契约测试通过。
4. 记录 `docs/` 内实际全部文件的相对路径、大小和 SHA-256。
5. 将 `.git/info/exclude` 更新为 `docs/`，并验证目录内文件均被本地规则命中。
6. 仅从 Git 索引递归移除 `docs/`。
7. 再次生成目录文件清单，逐项核对路径、大小和 SHA-256 完全一致。
8. 提交、完整验证并执行普通推送。
9. 通过 GitHub 当前分支查询确认 `docs` 返回 Not Found。

## 9. 验证标准

完成时必须同时满足：

1. 本地 `docs/` 目录存在。
2. 操作前后的文件路径集合、文件大小和 SHA-256 完全一致。
3. `git ls-files docs` 不返回任何路径。
4. `git status --short` 不把本地 `docs/` 显示为未跟踪内容。
5. `.git/info/exclude` 包含 `docs/`，且不再需要会话记录精确规则。
6. 中英文 README 均不包含 `docs/`。
7. 中英文 README 的其余相对链接均有效。
8. 完整测试套件通过，Skill 校验通过，`git diff --check` 无错误。
9. 推送后本地 `HEAD` 与远程 `main` 一致。
10. GitHub 当前 `main` 的 `docs` 路径返回 Not Found。
11. 旧提交中的 `docs/` 仍可访问，并在交付说明中明确这一方案 1 边界。

## 10. 风险与处理

- **本地目录误删：** 取消跟踪前后对实际目录树执行路径、大小和 SHA-256 三重核对。
- **后续文件误提交：** 使用目录级 `docs/` 规则覆盖未来新增文件。
- **README 描述失真：** 在同一实现批次删除中英文项目结构中的 `docs/` 条目。
- **全新克隆不含规划文档：** 这是用户要求隐藏 `docs/` 的直接结果，不影响 Skill 运行、测试和验证器。
- **旧历史仍可访问：** 这是沿用方案 1 的明确取舍，不宣称已彻底清除目录。
