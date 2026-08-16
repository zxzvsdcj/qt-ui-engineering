---
description: Qt Widget主窗口、QDockWidget、对话框、文件选择与通知选型规范
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# 11 主窗口、Dock与对话框规范
适用边界：仅用于Qt Widget窗口体系。
统一范式：【场景 → 推荐做法 → 不推荐/禁止 → 参考来源】

## 1. 通知与弹窗选型决策
场景：打开文件、提示状态、确认危险操作或编辑结构化表单。

推荐做法：
1. 选择本地文件或目录：使用QFileDialog，并传入当前主窗口作为parent。
2. 必须立即确认、拒绝或中止的短决策：使用QMessageBox，按钮角色表达行为语义。
3. 多字段输入、校验、预览或复杂帮助：使用自定义QDialog。
4. 普通成功、后台进度、自动恢复和轻量错误：优先StatusBar、页面内状态区或非模态通知。
5. 只有项目已经采用相应组件库时才使用InfoBar；不得为了一个通知自动添加依赖。

不推荐/禁止：
1. 禁止使用阻塞QMessageBox承担普通“保存成功”“正在加载”等轻量通知。
2. 禁止用自定义文件浏览器替代平台QFileDialog，除非业务明确需要额外预览或协议。
3. 禁止把不可逆操作放进无确认、无后果说明的普通按钮。

参考来源：[QFileDialog](https://doc.qt.io/qt-6/qfiledialog.html)、[QMessageBox](https://doc.qt.io/qt-6/qmessagebox.html)、[PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

## 2. 模态open/exec与非模态show
场景：决定对话框是否阻塞调用路径，以及对话框关闭后的对象生命周期。

推荐做法：
1. 用户必须完成当前决策才能继续同一工作流时，优先使用异步模态`open()`，连接`finished`、`accepted`或`rejected`处理结果，并持有对话框引用。
2. 只有既有同步调用路径确实依赖立即返回值时才使用`exec()`；保持任务短小，并明确它会建立嵌套事件循环。
3. 用户需要对照主窗口内容、并行查看多个窗口或持续使用工具面板时使用`show()`。
4. `open()`和`show()`返回后对象仍需存活：由主窗口持有引用，并设置明确parent和删除策略；关闭时清理引用。
5. 长操作始终移入工作线程；模态不等于允许阻塞UI线程。

不推荐/禁止：
1. 禁止为了读取一个返回值把所有提示都改成`exec()`；Qt 6官方不推荐把嵌套事件循环作为默认对话框流程。
2. 禁止在局部变量中创建对话框后立即`open()`或`show()`而不保留生命周期。
3. 禁止在模态对话框存续期间执行文件解析、网络请求或重计算。

参考来源：[QDialog](https://doc.qt.io/qt-6/qdialog.html)、[QObject对象树](https://doc.qt.io/qt-6/objecttrees.html)

## 3. 自定义QDialog UX
场景：设置、属性编辑、导出选项等结构化表单弹窗。

推荐做法：
1. 构造函数接收正确parent，使对话框层级、居中、任务栏和销毁行为跟随所属窗口。
2. 使用QDialogButtonBox的标准按钮和ButtonRole，让Windows、macOS、Linux采用对应按钮排布。
3. 将主操作设为默认按钮，但危险操作不得因误按Enter直接触发。
4. 保留ESC触发reject的标准行为；存在未保存编辑时，在reject路径进行一次明确确认。
5. 校验失败时保留用户输入，将焦点移动到首个错误字段，并显示具体错误原因。
6. 对话框内容允许随字体和翻译伸缩，使用布局与minimumSize，不锁死宽高。

不推荐/禁止：
1. 禁止手工按某一平台固定“确定/取消”左右顺序。
2. 禁止无parent创建本应属于主窗口的业务对话框。
3. 禁止校验失败后关闭窗口或清空全部输入。
4. 禁止移除ESC关闭，却不给等价的取消路径。

参考来源：[QDialogButtonBox](https://doc.qt.io/qt-6/qdialogbuttonbox.html)、[QDialog](https://doc.qt.io/qt-6/qdialog.html)

## 4. QDockWidget工程实践
场景：多面板桌面工具需要停靠、浮动、关闭和恢复工作区。

推荐做法：
1. 使用QMainWindow的dock区域管理QDockWidget；为每个Dock设置稳定且唯一的objectName。
2. 将minimumSize、sizeHint和业务布局约束设置在Dock内容Widget上。
3. 根据工作流配置allowedAreas、features和默认停靠区域；允许用户恢复到明确的默认布局。
4. 保存QMainWindow的saveState结果，并在所有Dock创建和命名完成后restoreState。
5. 在macOS验证浮动Dock和native handle相关拖拽限制；不要只依据Windows行为设计。

不推荐/禁止：
1. 禁止动态生成不稳定objectName后尝试恢复历史Dock布局。
2. 禁止把所有面板默认展开并压缩主工作区。
3. 禁止只保存几何位置而忽略Dock state。

参考来源：[QDockWidget](https://doc.qt.io/qt-6/qdockwidget.html)、[QMainWindow](https://doc.qt.io/qt-6/qmainwindow.html)

## 5. 无边框自定义窗口
场景：产品确有自定义标题栏、沉浸式工具框架或特殊硬件界面需求。

推荐做法：
1. 优先复用项目现有、经过目标平台验证的成熟封装。
2. 验证窗口拖拽、八方向缩放、最大化、系统菜单、多屏DPI、键盘访问和辅助功能。
3. 保留原生窗口作为可回退实现，平台能力不足时使用原生装饰。

不推荐/禁止：
1. 禁止仅实现鼠标拖动就宣称完成无边框窗口。
2. 禁止为视觉新颖牺牲系统窗口操作、可访问性和跨平台稳定性。
3. 禁止把单平台私有API无条件放进通用路径。

参考来源：Qt官方平台文档、[PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

## 6. 生命周期与内存管理
场景：同一设置窗口或业务弹窗被重复打开、关闭和重新创建。

推荐做法：
1. 模态短对话框可以按需创建并由parent管理。
2. 可重复打开的非模态窗口选择“单实例复用”或“关闭即销毁”中的一种，并写清所有权。
3. 单实例复用时，已存在则raise、activateWindow并同步最新数据。
4. 关闭即销毁时使用合适的delete-on-close策略，并在finished或destroyed信号中清理Python引用。

不推荐/禁止：
1. 禁止每次点击都创建一个永久隐藏的对话框实例。
2. 禁止parent缺失并依赖Python局部变量维持窗口。
3. 禁止同时存在多个修改同一份设置却没有冲突策略的窗口。

参考来源：[QObject](https://doc.qt.io/qt-6/qobject.html)、[QWidget属性](https://doc.qt.io/qt-6/qwidget.html)

## 7. 反模式清单
场景：AI生成或审查窗口、Dock、对话框代码。

推荐做法：
1. 明确通知是否必须阻断、是否需要返回值、是否允许用户对照主窗口、谁拥有窗口对象。
2. 对每个复杂弹窗附带简短【实现与UX说明】，解释选型和生命周期。

不推荐/禁止：
1. 普通完成通知连续弹出阻塞MessageBox。
2. 非模态窗口没有parent、没有持有引用、没有销毁策略。
3. 自定义按钮顺序覆盖平台惯例。
4. Dock没有稳定objectName却保存布局。
5. 对话框关闭后后台任务继续运行且无状态入口。
6. 从零手写无边框窗口并忽略多屏、缩放和系统菜单。

参考来源：[BallonsTranslator](https://github.com/dmMaze/BallonsTranslator)、[PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)、Qt官方Widget文档
