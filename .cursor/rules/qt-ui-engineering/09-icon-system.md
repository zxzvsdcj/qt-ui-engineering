---
description: Qt Widget SVG图标系统工程规范，图标选型、设计约束、主题变色实现方案
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# 09‑icon‑system.md SVG图标系统规范
统一范式：【场景 → 推荐做法 → 不推荐/禁止 → 参考来源】

## 1. UX基础设计原则
场景：按钮、工具栏、侧边导航、菜单、状态标识
推荐做法：
1. SVG矢量图标优先，避免位图PNG作为长期业务图标。
2. 图标语义清晰；优先使用「图标+文字」组合；纯图标按钮需要tooltip文字说明。
3. 统一尺寸规范：工具栏16px，侧边导航20~24px，弹窗标题图标24px。
4. 项目图标风格统一，不可同时混用线框图标与填充图标。
5. 明暗主题切换时，图标颜色跟随主题自动变更。
不推荐/禁止：
1. 使用QStyle.StandardPixmap系统内置老旧图标作为业务主图标；
2. 固定写死SVG填充色，无法适配明暗主题；
3. 不同界面随意使用多种尺寸、多种风格图标。

## 2. 图标来源决策树
1. 新项目首选：PyQt‑Fluent‑Widgets FluentIcon枚举；自动适配DPI、自动跟随主题变色。
2. 自主图标备选素材库：Fluent-System-Icons、IconPark、Material Icons。
3. 自定义图标制作约束（Figma / Inkscape导出SVG）：
   - viewBox="0 0 24 24"；
   - 移除硬编码fill、stroke色值；
   - 删除冗余图层、注释、无用metadata，精简path；
   - 避免大量滤镜、渐变，防止Qt渲染异常。

## 3. Qt Widget三种实现方案
### 方案A：FluentIcon（首选）
直接调用控件内置图标，无需外部SVG文件，自动主题适配。

### 方案B：原始SVG文件 + QSvgRenderer动态重绘着色
适用场景：自研图标、外部自定义SVG资源。
重要注意坑：原生 `QIcon("xxx.svg")` **无法动态修改颜色**，必须通过QSvgRenderer重绘生成变色图标。

### 方案C：qrc资源系统打包SVG
推荐将SVG纳入qrc资源文件，统一路径 `:/icons/xxx.svg`，规避打包后路径丢失问题。

## 4. 各场景图标UX细则
1. 侧边导航：展开显示图标+文字；折叠仅显示图标，hover显示Tooltip；
2. 工具栏hover提供视觉反馈；
3. 危险操作图标增加视觉警示；

## 5. 图标相关反模式
1. 直接加载SVG生成QIcon，期望运行时修改颜色；
2. 大量重复图标不纳入资源文件，使用本地外部相对路径；
3. 高DPI场景使用固定尺寸位图图标，出现模糊；

## 参考来源
PyQt‑Fluent‑Widgets、BallonsTranslator、Open‑Code IDE、Cura
