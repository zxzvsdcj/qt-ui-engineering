# 本地项目元数据排除设计规格

**日期：** 2026-08-12  
**状态：** 用户已批准方案 1  
**项目：** `qt-ui-engineering`

## 1. 目标

将以下四个工作过程文件从公开仓库当前 `main` 分支移除，同时完整保留在本地工作区，并防止后续提交再次将它们上传：

- `.gitignore`
- `findings.md`
- `progress.md`
- `task_plan.md`

本次不重写 Git 历史。这四个文件仍可在已有旧提交中查看，这是用户选择方案 1 后接受的边界。

## 2. 本地保留机制

四个文件继续保留在 `E:/cursor/qt-ui-engineering` 原位置，内容不修改。使用仓库本地且不会被提交的 `.git/info/exclude` 维护排除规则：

```gitignore
__pycache__/
*.py[cod]
docs/Qt_UI_Skills_会话完整记录.md
.gitignore
findings.md
progress.md
task_plan.md
```

前三条从当前 `.gitignore` 迁移，继续保护 Python 缓存和本地会话记录；后四条保证本次移除的文件不会再次出现在待提交列表中。

## 3. 远程移除方式

对四个文件执行仅取消 Git 跟踪的操作，不删除工作区文件。提交后，公开仓库 `main` 的当前文件树中不再包含它们。本次不删除远程仓库、不重建仓库、不强制推送，也不改变已有提交 SHA。

## 4. README 一致性

中英文 README 当前都包含指向 `findings.md` 的调研决策链接。文件从当前分支移除后，该链接会失效，因此必须同步调整：

- 中文版删除“详细的调研决策记录在 `findings.md` 中”一句。
- 英文版删除对应的 `Detailed research decisions...` 一句。
- 其余中英文内容、语言切换、命令、来源链接和技术说明不变。

公开文档不新增对本地四个文件的链接或文件名说明。

## 5. 实施范围

### 本地但不提交

- 修改 `.git/info/exclude`，写入七条精确规则。
- 保留 `.gitignore`、`findings.md`、`progress.md`、`task_plan.md` 原始内容。

### 提交到远程

- 从 Git 索引移除四个文件。
- 修改 `README.md` 和 `README.en.md`，删除失效的 `findings.md` 链接。
- 增加或调整契约测试，确保公开 README 不再引用 `findings.md`。

### 不在范围内

- 重写 Git 历史。
- 删除或重建 GitHub 仓库。
- 清除旧提交对象。
- 移除 `docs/superpowers`、测试、评测夹具或其他项目文件。

## 6. 验证标准

完成时必须同时满足：

1. 四个文件在本地文件系统中仍存在。
2. `git ls-files` 不再列出四个文件。
3. `git status --short` 不显示四个文件为未跟踪文件。
4. `.git/info/exclude` 能分别匹配四个文件、Python 缓存和本地会话记录。
5. `README.md` 与 `README.en.md` 不再包含 `findings.md`。
6. 中英文 README 的其他本地 Markdown 链接均有效。
7. 完整测试套件通过，Skill 结构校验通过，`git diff --check` 无错误。
8. 推送后，本地 `HEAD` 与远程 `main` 一致。
9. GitHub 当前 `main` 查询四个文件均返回 Not Found。
10. 旧提交历史保持不变且不宣称已彻底清除这些文件。

## 7. 风险与处理

- **旧历史仍可访问：** 这是方案 1 的明确取舍，在交付说明中再次标注。
- **本地文件误删：** 取消跟踪前记录四个文件的 SHA-256，操作后逐一核对存在性和哈希。
- **忽略规则丢失：** 在取消跟踪 `.gitignore` 前先将全部现有规则写入 `.git/info/exclude` 并验证匹配。
- **README 失效链接：** 在同一实现批次移除中英文 `findings.md` 引用，并运行链接校验。
- **后续克隆缺少 `.gitignore`：** 这是用户要求从远程移除 `.gitignore` 的直接结果；本地仓库仍由 `.git/info/exclude` 保护，新克隆不会继承这些本地排除规则。
