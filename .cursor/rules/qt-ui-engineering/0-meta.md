---
description: Qt-UI-Engineering 全局元规则，Widget桌面UI工程总规范
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# Qt-UI-Engineering Meta 全局规范
正式定位：Qt-UI-Engineering 是 Qt Widget 界面工程规范，包含 UI 视觉、UX 交互、性能、跨平台、数据视图、资源打包整套实践。
适用范围：Qt Widget（Qt C++ / PyQt5 / PyQt6 / PySide2 / PySide6）
适用场景：个人自用桌面工具软件。
边界约束：QML/Qt Quick不在本规则覆盖范围，禁止将 Widget 规则套用至 QML 代码。

## 全局优先原则
1. UX交互逻辑优先级高于纯视觉美化；布局架构优先级高于QSS样式。
2. 现代界面优先使用SVG矢量图标，尽量避免PNG位图作为业务图标；按钮、工具栏、侧边导航、菜单生成时必须考虑图标配置。
3. 重视Hi‑DPI高分屏适配，优先相对尺寸，减少硬编码固定像素。
4. 数据量大的表格/列表优先采用Model‑View架构，规避QTableWidget性能缺陷。
5. 工具软件关键UI布局状态支持持久化存储。
6. UI主线程禁止阻塞；耗时任务移入工作线程并提供用户状态反馈。
7. 发布阶段妥善管理SVG、QSS、图片等资源，防止打包后资源丢失。

## 全局禁止项
❌ 禁止将Qt老旧内置系统图标(QStyle.StandardPixmap SP_*)作为业务主图标；
❌ 禁止主窗口直接使用setFixedSize写死固定尺寸；
❌ 上千条动态数据直接选用QTableWidget/QListWidget；
❌ 开发与打包场景混用绝对文件路径；
❌ 在UI回调函数（信号槽、Model::data、Delegate绘制）执行IO、重度计算；
❌ 大量业务数据存入QSettings配置。

## AI输出约束
1. 生成复杂UI代码时附带简短【实现与UX说明】。
2. 包含表格视图时主动评估数据量级，推荐对应控件方案。
3. 跨平台界面代码标注系统差异化注意事项。
4. 区分模态/非模态弹窗适用场景，不滥用阻塞式弹窗。
