---
description: Qt Widget qrc资源、外部文件、SVG与QSS加载及PyInstaller发布规范
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# 14 资源管理与打包发布规范
适用边界：Qt Widget中的图片、SVG、QSS、字体和运行时外部资源。
统一范式：【场景 → 推荐做法 → 不推荐/禁止 → 参考来源】

## 1. 三种资源方案决策
场景：在qrc、外部资源目录和运行时动态加载SVG之间选择。

推荐做法：
1. qrc：用于随程序版本发布、不可缺失的图标、默认QSS、小型图片和固定模板；路径统一为`:/icons/name.svg`。
2. 外部资源目录：用于用户可替换主题、大型素材、插件资产和无需重新构建即可更新的内容。
3. 运行时动态SVG：用于主题着色、状态色或需要QSvgRenderer重绘的自定义图标；SVG源仍优先来自qrc或受控外部目录。
4. 一个资源定义唯一所有者；默认资源与用户覆盖层顺序写清楚。

不推荐/禁止：
1. 禁止把所有大型可变资源无条件编进qrc，导致更新和内存成本不透明。
2. 禁止把关键默认图标只放在开发机外部相对目录。
3. 禁止直接QIcon加载SVG后期待修改其内部fill实现主题变色。

参考来源：[Qt Resource System](https://doc.qt.io/qt-6/resources.html)、[QSvgRenderer](https://doc.qt.io/qt-6/qsvgrenderer.html)

## 2. qrc路径与编译
场景：PySide6或PyQt6项目把静态资源编译为Python资源模块。

推荐做法：
1. qrc使用稳定前缀与alias，例如`/icons`和`open.svg`；代码只引用`:/icons/open.svg`。
2. PySide6使用`pyside6-rcc resources.qrc -o resources_rc.py`。
3. PyQt6使用`pyrcc6 resources.qrc -o resources_rc.py`。
4. 应用入口或资源加载模块显式import生成的`resources_rc`，确保资源注册发生。
5. qrc与生成模块纳入构建流程；修改qrc后重新生成并进行缺失资源测试。

不推荐/禁止：
1. 禁止在代码中引用qrc源文件的磁盘位置代替`:/`路径。
2. 禁止忘记import生成资源模块，却只在开发目录碰巧找到同名文件。
3. 禁止手工编辑生成的resources_rc模块。
4. 禁止同一资源在多个qrc前缀下重复注册而没有目的。

参考来源：[Qt for Python资源教程](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/qrcfiles.html)、[Qt Resource System](https://doc.qt.io/qt-6/resources.html)

## 3. SVG图标与QSS加载
场景：主题切换、打包运行或资源缺失时加载SVG和样式表。

推荐做法：
1. 静态SVG通过qrc路径交给QIcon；主题着色SVG通过QSvgRenderer渲染到带正确device pixel ratio的QPixmap。
2. 默认QSS优先编入qrc；用户主题允许外部文件，并明确UTF-8编码。
3. 样式加载失败时记录实际资源标识，保留可用默认主题或显示明确错误。
4. QSS内部引用图片也使用可解析的qrc URL，并在打包产物中验证。
5. 对缓存图标按主题、尺寸和device pixel ratio建立键；主题切换时清理对应缓存。

不推荐/禁止：
1. 禁止捕获全部异常后返回空字符串，使资源缺失静默退化。
2. 禁止QSS依赖当前工作目录。
3. 禁止在每次Delegate绘制或hover事件重新解析SVG。
4. 禁止固定SVG fill导致明暗主题不可读。

参考来源：[QFile](https://doc.qt.io/qt-6/qfile.html)、[QIcon](https://doc.qt.io/qt-6/qicon.html)、[Qt Style Sheets](https://doc.qt.io/qt-6/stylesheet.html)

## 4. 开发与打包路径规范
场景：同一代码既从源码目录运行，也作为PyInstaller bundle运行。

推荐做法：
1. qrc资源直接使用`:/`标识，不参与文件系统拼接。
2. 外部资源基于资源加载模块的`__file__`定位，并使用pathlib组合路径。
3. PyInstaller通过保持相对目录结构的datas配置，让bundle中的`__file__`定位与源码一致。
4. 当前工作目录只代表用户运行位置，不作为应用资源根目录。
5. 用户选择的文件路径与应用内置资源路径分开建模。

不推荐/禁止：
1. 禁止硬编码盘符、用户目录、IDE工程目录或构建机绝对路径。
2. 禁止开发环境依赖cwd，打包环境改用另一套散落分支。
3. 禁止把`sys._MEIPASS`作为唯一资源根目录策略；当前PyInstaller优先支持基于`__file__`的定位。
4. 禁止把用户文档复制到只读的应用资源目录。

参考来源：[PyInstaller运行时信息](https://pyinstaller.org/en/stable/runtime-information.html)、Python pathlib文档

## 5. PyInstaller资源收集
场景：SVG、QSS、字体、外部模板或插件资源需要进入发布产物。

推荐做法：
1. qrc已编译进Python模块时，确保生成模块被import并由分析阶段收集。
2. 外部资源使用命令行`--add-data`或spec文件`datas`，目标目录保持源码相对结构。
3. 第三方包确有数据文件时，先检查项目已有spec和PyInstaller hook，再选择`collect_data_files`。
4. 构建后从干净目录启动产物，逐项验证图标、QSS、字体、文件对话框和主题切换。
5. 记录实际构建命令和资源清单，避免IDE本地文件掩盖缺失。

不推荐/禁止：
1. 禁止仅依据构建成功判断资源完整。
2. 禁止重复同时打包qrc源、生成模块和同一份外部资源而没有用途。
3. 禁止为了一个文件盲目收集整个开发目录。
4. 禁止让打包spec依赖开发机绝对路径。

参考来源：[PyInstaller添加数据文件](https://pyinstaller.org/en/stable/spec-files.html#adding-data-files)、[PyInstaller hooks](https://pyinstaller.org/en/stable/hooks.html)

## 6. 资源加载失败策略
场景：文件缺失、qrc未注册、SVG损坏或用户主题不可读。

推荐做法：
1. 关键默认资源缺失时快速失败并报告资源标识、加载模式和修复方向。
2. 可选用户主题失败时回退内置默认主题，同时向用户显示一次非模态错误。
3. 图标回退保持语义可识别，优先文字标签或内置qrc兜底，不使用无语义空白。
4. 自动测试同时覆盖qrc成功、外部成功、缺失失败和无cwd依赖。

不推荐/禁止：
1. 禁止静默返回空QIcon或空QSS并继续宣称加载成功。
2. 禁止缺失资源时回退到开发机路径。
3. 禁止连续弹出多个阻塞MessageBox报告同一批资源错误。

参考来源：Qt QFile错误处理、PyInstaller运行时文档

## 7. 反模式清单
场景：AI生成或审查资源加载、主题和发布代码。

推荐做法：
1. 输出资源所有权、qrc前缀、外部覆盖顺序、打包收集方式和失败路径。
2. 发布验证必须使用实际bundle，并记录关键资源是否可见。

不推荐/禁止：
1. 硬编码绝对资源路径。
2. 依赖当前工作目录加载QSS或SVG。
3. qrc生成模块未import。
4. 直接QIcon加载SVG却期待运行时变色。
5. PyInstaller构建成功但未运行资源冒烟测试。
6. 缺失资源异常被空catch吞掉。

参考来源：Qt官方资源文档、PyInstaller官方文档、[QGIS](https://github.com/QGIS/QGIS)、[Cura](https://github.com/Ultimaker/Cura)的资源与发布工程实践
