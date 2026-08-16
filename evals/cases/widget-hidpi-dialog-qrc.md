# Case: PySide6 Hi-DPI、对话框与qrc资源

## Pressure scenario

使用PySide6开发工具窗口，提供打开文件按钮，弹出标准文件选择框；支持打开自定义表单弹窗；完整实现HiDPI适配；不写死主窗口固定像素尺寸；资源使用qrc方式管理。

## Baseline failure risks without this Skill

- 在QApplication创建之后设置DPI策略，或强制产品缩放环境变量。
- 主窗口使用固定尺寸，字体或平台变化后内容溢出。
- QFileDialog和自定义QDialog没有parent，窗口层级异常。
- 源码使用磁盘相对路径，打包后SVG和QSS丢失。

## Required behavior with this Skill

- 说明Qt 6默认High-DPI行为；需要的舍入策略在QApplication之前设置。
- 主窗口使用resize、minimumSize和布局伸缩，不使用固定尺寸锁定。
- QFileDialog和自定义QDialog都绑定当前主窗口parent。
- 使用QDialogButtonBox、默认按钮和标准ESC reject行为。
- 静态资源通过`:/`路径访问，并显式导入编译后的资源模块。

## Pass conditions

- 应用启动在QApplication之前执行必要的DPI初始化。
- 对话框正确设置父对象。
- 不存在主窗口固定尺寸锁定。
- 使用规范qrc资源路径。
- 不把诊断缩放环境变量永久写入产品入口。
