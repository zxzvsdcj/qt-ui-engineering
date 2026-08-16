# Case: PySide6综合UI、UX、图标、主题与持久化

## Pressure scenario

写一个PySide6自用工具主窗口，可折叠左侧侧边导航，包含设置、文件、导出；支持亮暗黑切换；导航栏带有SVG图标；耗时任务提供加载状态反馈；软件重启自动记忆窗口大小、侧边栏展开/折叠状态。

## Baseline failure risks without this Skill

- 使用固定颜色或位图图标，切换主题后不可读。
- 在点击槽中同步执行耗时任务，主窗口冻结。
- 只保存业务配置，不保存窗口和侧边栏布局。
- 使用老旧QStyle SP系统图标代替业务SVG。

## Required behavior with this Skill

- 检测并保持`Python / Qt 6 / PySide6 / QWidget`技术栈。
- 使用主题自适应SVG图标；纯图标折叠态提供tooltip和可访问名称。
- 将耗时任务移入工作线程，通过信号提供加载、完成、失败和取消反馈。
- 使用版本化QSettings保存窗口geometry与侧边栏展开状态，首次启动有默认值。
- 附带简短【实现与UX说明】，解释导航、反馈和状态恢复边界。

## Pass conditions

- 使用SVG图标并支持主题自动变色。
- UI线程不阻塞，具备明确UX状态反馈。
- 包含窗口和侧边栏UI布局持久化逻辑。
- 不使用QStyle SP系统图标作为业务图标。
- 不引入任何非Widget界面实现。
