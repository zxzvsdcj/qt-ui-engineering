---
description: Qt Widget窗口、Dock、Splitter、表格列与主题状态持久化规范
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# 13 UI状态持久化规范
适用边界：仅用于Qt Widget工具软件的界面状态，不承担业务数据库职责。
统一范式：【场景 → 推荐做法 → 不推荐/禁止 → 参考来源】

## 1. 应当持久化的UI状态
场景：用户重启工具后需要恢复稳定工作区和高频个性化调整。

推荐做法：
1. 主窗口保存`saveGeometry()`结果，恢复位置、大小和窗口状态。
2. QMainWindow保存`saveState(version)`结果，恢复QDockWidget与工具栏布局。
3. QSplitter保存各区域比例；QHeaderView保存列宽、顺序和隐藏状态。
4. 表格排序列、排序方向、明暗主题和侧边栏展开状态使用明确键值保存。
5. 为用户可自定义布局提供“恢复默认布局”。

不推荐/禁止：
1. 禁止只保存窗口宽高而忽略屏幕位置、Dock和Splitter。
2. 禁止对所有控件无差别序列化。
3. 禁止没有恢复默认布局的永久自定义状态。

参考来源：[QMainWindow](https://doc.qt.io/qt-6/qmainwindow.html)、[QWidget](https://doc.qt.io/qt-6/qwidget.html)、[QHeaderView](https://doc.qt.io/qt-6/qheaderview.html)

## 2. 不应持久化的瞬时状态
场景：临时查询、当前选中、一次性进度和瞬时错误提示。

推荐做法：
1. 临时选中条目、hover、焦点、实时搜索文本和加载动画在新会话使用安全默认值。
2. 只有产品明确要求“恢复上次工作”时，才单独设计业务会话恢复，并与UI布局配置分离。
3. 隐私或敏感输入不写入通用UI设置。

不推荐/禁止：
1. 禁止默认保存临时选中行和实时搜索词。
2. 禁止把尚未提交的表单内容伪装成UI布局状态。
3. 禁止把后台任务进度保存后在下次启动显示为仍在运行。

参考来源：[QSettings](https://doc.qt.io/qt-6/qsettings.html)、桌面应用会话恢复惯例

## 3. QSettings组织命名与封装
场景：Python或C++工具需要跨平台保存少量配置，并避免键名散落。

推荐做法：
1. 在应用启动时设置稳定的organizationName和applicationName，或构造QSettings时显式传入。
2. 将UI键集中封装在一个小型状态存储类，使用`ui/v1/window/geometry`等分层键。
3. 对布尔、整数、字符串和QByteArray恢复进行明确类型转换与缺失判断。
4. 将业务配置、账号数据和大对象放入适合的数据存储，不塞入QSettings。
5. 测试时使用独立组织名或临时设置范围，避免污染真实用户配置。

不推荐/禁止：
1. 禁止在各个Widget中散落重复字符串键。
2. 禁止大量业务数据、历史记录、表格数据或缓存写入QSettings。
3. 禁止依赖不同平台后端恰好采用相同物理文件位置。

参考来源：[QSettings](https://doc.qt.io/qt-6/qsettings.html)、[QCoreApplication组织属性](https://doc.qt.io/qt-6/qcoreapplication.html)

## 4. 配置版本兼容
场景：Dock名称、表格列、主题结构或默认布局随应用版本变化。

推荐做法：
1. UI状态键包含独立schema版本；QMainWindow的saveState/restoreState使用一致整数版本。
2. 只在能明确迁移时读取旧版本；否则保留其他设置并回退当前默认布局。
3. QDockWidget和QToolBar在各版本使用稳定且唯一的objectName。
4. 新增表格列时验证旧QHeaderView状态；关键列不可见或恢复失败时重置表头默认值。
5. 将“配置版本”与“应用发布版本”分开，只有结构改变时提升配置版本。

不推荐/禁止：
1. 禁止修改Dock的objectName却继续声称旧布局可恢复。
2. 禁止任何恢复失败都清空全部用户设置。
3. 禁止把发布版本字符串直接当作每次变化的设置前缀。

参考来源：[QMainWindow saveState](https://doc.qt.io/qt-6/qmainwindow.html)、[QSettings](https://doc.qt.io/qt-6/qsettings.html)

## 5. 保存与恢复时机
场景：避免频繁写盘，同时保证正常退出后工作区可恢复。

推荐做法：
1. 所有Dock、Splitter、工具栏和表头创建完成后再恢复UI状态。
2. 窗口关闭事件保存稳定状态；用户明确切换主题或提交列设置时可以同步保存对应小键值。
3. 拖拽Splitter或窗口resize期间只更新内存状态，不在每个像素变化时写QSettings。
4. 需要崩溃恢复时使用低频防抖快照，并与正常关闭保存区分。
5. 恢复完成后再连接会导致写回的高频信号，避免启动时覆盖旧值。

不推荐/禁止：
1. 禁止在resizeEvent、moveEvent和splitterMoved的每次回调直接sync。
2. 禁止在Dock创建前restoreState。
3. 禁止启动默认值先写盘再尝试读取历史值。

参考来源：[QSettings sync](https://doc.qt.io/qt-6/qsettings.html)、[QMainWindow](https://doc.qt.io/qt-6/qmainwindow.html)

## 6. 默认兜底与多屏恢复
场景：首次启动、配置损坏、屏幕减少或窗口停留在已断开的显示器。

推荐做法：
1. 每个读取操作都有可用默认值；restoreGeometry或restoreState返回失败时应用默认布局。
2. 恢复后检查窗口至少与一个可用screen有可见交集；否则移动到主屏可用区域。
3. 关键Dock、工具栏和表格列始终有恢复默认操作。
4. 配置损坏只重置受影响的UI状态组，不删除无关用户设置。

不推荐/禁止：
1. 禁止无默认配置导致首次启动零尺寸或关键面板不可见。
2. 禁止忽略restoreState返回值。
3. 禁止因为一个表头状态损坏清空主题、快捷键和其他独立设置。

参考来源：[QWidget restoreGeometry](https://doc.qt.io/qt-6/qwidget.html)、[QGuiApplication screens](https://doc.qt.io/qt-6/qguiapplication.html)

## 7. 反模式清单
场景：AI生成或审查工具软件的“记住布局”功能。

推荐做法：
1. 输出保存清单、不保存清单、键版本、保存时机、恢复失败路径和默认布局。
2. 分别验证首次启动、正常恢复、配置损坏、列结构变化和屏幕拓扑变化。

不推荐/禁止：
1. 大量业务数据存入QSettings。
2. 每次resize或拖拽都立即写盘。
3. Dock没有稳定objectName。
4. 没有配置版本和默认兜底。
5. 保存临时选择、实时搜索和瞬时任务状态。
6. 恢复失败后静默留下不可用窗口。

参考来源：[Spyder](https://github.com/spyder-ide/spyder)、[QGIS](https://github.com/QGIS/QGIS)、Qt官方状态保存文档
