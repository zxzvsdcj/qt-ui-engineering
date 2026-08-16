---
description: Qt Widget Hi-DPI高分屏适配与Windows、macOS、Linux跨平台兼容规范
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# 10 Hi-DPI与跨平台兼容规范
适用边界：仅用于Qt Widget（Qt C++、PyQt5、PyQt6、PySide2、PySide6）。
统一范式：【场景 → 推荐做法 → 不推荐/禁止 → 参考来源】

## 1. Qt 6启动与缩放初始化
场景：PySide6或PyQt6应用入口需要在高分屏、多屏缩放环境下启动。

推荐做法：
1. 先确认Qt 6默认已经启用High-DPI缩放，不重复设置Qt 5时代的启用属性。
2. 确需统一小数缩放舍入策略时，在创建QApplication之前调用：

```python
try:
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtWidgets import QApplication
except ImportError:
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QGuiApplication
    from PyQt6.QtWidgets import QApplication

QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
)
app = QApplication([])
```

3. 将`QT_SCALE_FACTOR`、`QT_SCREEN_SCALE_FACTORS`和`QT_ENABLE_HIGHDPI_SCALING`视为诊断或自动化测试变量；必须在进程启动前设置，并在测试结束后移除。
4. Qt 5目标单独按对应绑定和Qt 5文档处理，不把Qt 5属性混入Qt 6入口。

不推荐/禁止：
1. 禁止在QApplication创建后修改缩放策略并假设能够追溯生效。
2. 禁止为了“更清晰”在产品启动代码中永久强制`QT_SCALE_FACTOR=2`。
3. 禁止把测试机器的DPI环境变量写入通用启动脚本。

参考来源：[Qt High DPI](https://doc.qt.io/qt-6/highdpi.html)、[QGuiApplication](https://doc.qt.io/qt-6/qguiapplication.html)

## 2. 逻辑像素、设备像素与字体
场景：布局在100%、125%、150%、200%缩放和混合DPI多屏之间保持可读、可操作。

推荐做法：
1. 将QWidget几何、布局边距和控件尺寸理解为逻辑像素；设备像素主要用于底层图像缓冲、截图和自绘资源。
2. 字体优先使用`setPointSize`或项目排版令牌，不使用固定PixelSize控制正文。
3. 自绘时读取`devicePixelRatioF()`，为像素缓冲设置正确的device pixel ratio。
4. 图标优先SVG；必须使用位图时提供高分辨率变体并验证device pixel ratio。
5. 根据字体metrics和原生style metrics决定输入框、按钮与行高，不只依据文字大小做算术放大。

不推荐/禁止：
1. 禁止把逻辑像素直接当成物理像素计算截图或离屏缓冲尺寸。
2. 禁止使用PixelSize锁定通用正文、菜单和表单字体。
3. 禁止仅在100%缩放下验收位图图标和自绘控件。

参考来源：[Qt High DPI概念](https://doc.qt.io/qt-6/highdpi.html)、[QScreen](https://doc.qt.io/qt-6/qscreen.html)

## 3. Windows、macOS、Linux行为差异
场景：同一Qt Widget工具在三个桌面平台运行，并包含标题栏、Dock、对话框或无边框窗口。

推荐做法：
1. Windows：验证Per-Monitor缩放、窗口跨屏移动、系统字体和原生文件对话框；不要假设所有显示器缩放一致。
2. macOS：优先保留原生标题栏和窗口按钮；使用QDialogButtonBox获得平台按钮顺序；验证QDockWidget浮动行为和系统菜单集成。
3. Linux：在目标桌面环境和窗口管理器验证窗口装饰、最小尺寸、置顶、焦点与无边框拖拽；将X11和Wayland差异记录为目标平台约束。
4. 三个平台都使用Qt布局、sizeHint、minimumSize和原生对话框能力承担适配。
5. 无边框窗口只有在产品需求明确且项目已有成熟封装时采用；保留缩放、拖拽、系统菜单、辅助功能与多屏边界处理。

不推荐/禁止：
1. 禁止假设无边框命中测试、阴影和系统按钮在三个平台行为一致。
2. 禁止通过平台坐标常量手工摆放窗口按钮。
3. 禁止把Windows标题栏补丁无条件应用到macOS或Linux。
4. 禁止将QDockWidget自身作为复杂尺寸约束的唯一承载者；约束应优先设置在其内容Widget。

参考来源：[Qt for Windows](https://doc.qt.io/qt-6/windows.html)、[Qt for macOS](https://doc.qt.io/qt-6/macos.html)、[Qt for Linux/X11](https://doc.qt.io/qt-6/linux.html)、[QDockWidget](https://doc.qt.io/qt-6/qdockwidget.html)

## 4. 可伸缩布局尺寸策略
场景：主窗口、面板、表单和工具栏需要覆盖不同屏幕和字体缩放。

推荐做法：
1. 主窗口提供合理的初始`resize`和`minimumSize`，让布局继续管理内部伸缩。
2. 仅在业务上确有上限时使用maximumSize；优先通过stretch、sizePolicy、QSplitter和可折叠面板表达空间分配。
3. 为长文本、翻译扩展、大字体和状态消息保留可增长方向。
4. 使用布局边距与间距令牌；把图标视觉尺寸和按钮可点击区域分开定义。

不推荐/禁止：
1. 禁止主窗口使用setFixedSize锁定工作区。
2. 禁止为修复一次溢出而给所有子控件添加固定宽高。
3. 禁止依赖最小化字体或裁剪文本维持布局。

参考来源：[QWidget大小约束](https://doc.qt.io/qt-6/qwidget.html)、[Qt Layout Management](https://doc.qt.io/qt-6/layout.html)

## 5. PyInstaller高DPI排查
场景：源码运行正常，PyInstaller打包后出现缩放异常、字体或图标模糊、资源缺失。

推荐做法：
1. 先比较源码与打包进程的Qt版本、平台插件、环境变量和启动顺序；不要先假设PyInstaller关闭了Qt 6缩放。
2. 检查自定义Windows manifest是否覆盖DPI awareness；只有项目明确需要时才维护自定义manifest。
3. 检查SVG、字体、QSS和高分辨率位图是否已收集；资源缺失可能表现为尺寸和布局退化。
4. 验证缩放策略调用发生在QApplication之前，且入口模块确实被打包执行。
5. 在至少两种系统缩放和一次跨屏移动中运行打包产物。

不推荐/禁止：
1. 禁止通过永久环境变量掩盖manifest、资源或启动顺序问题。
2. 禁止仅以编译成功证明打包产物的高DPI行为正确。
3. 禁止把模糊位图问题误判成Qt布局缩放失效。

参考来源：[PyInstaller运行时信息](https://pyinstaller.org/en/stable/runtime-information.html)、[Qt High DPI](https://doc.qt.io/qt-6/highdpi.html)

## 6. 反模式黑名单
场景：AI生成或评审跨平台Widget代码。

推荐做法：
1. 发现固定主窗口、PixelSize正文、绝对坐标、自绘DPI缓冲或产品内强制缩放变量时，标记具体平台后果并给出替代方案。
2. 跨平台输出附带已验证平台和待验证平台说明。

不推荐/禁止：
1. 固定主窗口尺寸并宣称“适配所有分辨率”。
2. 对所有显示器使用同一个缓存device pixel ratio。
3. 从零手写跨平台无边框窗口，却不处理系统菜单、缩放边缘和辅助功能。
4. 使用固定尺寸PNG承担需要主题变色和高DPI缩放的业务图标。
5. 将Cura的QML界面实现引入本规则；Cura只作为资源和发布问题参考。

参考来源：[PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)、[Cura](https://github.com/Ultimaker/Cura)、Qt官方平台文档
