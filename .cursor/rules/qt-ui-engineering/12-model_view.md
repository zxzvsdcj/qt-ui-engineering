---
description: Qt Widget Model-View架构、表格列表大数据性能与交互规范
globs: ["**/*.py","**/*.cpp","**/*.h","**/*.ui","**/*.qrc"]
---
# 12 Model-View数据视图规范
适用边界：仅用于Qt Widget的表格、列表和树视图。
统一范式：【场景 → 推荐做法 → 不推荐/禁止 → 参考来源】

## 1. 控件选型与数据量级
场景：在少量配置项、数百条动态数据和数千条业务记录之间选择Item Widget或Model-View。

推荐做法：
1. 少量、静态、低频更新且不需要复用数据源时，可以使用QTableWidget或QListWidget。
2. 数百条以上动态数据、需要排序筛选、增量更新或多个视图共享数据时，优先QTableView/QListView配合自定义Model。
3. 上千条动态业务数据强制使用QTableView与QAbstractTableModel，树形数据使用QTreeView与QAbstractItemModel。
4. 在输出代码前说明预计数据量、更新频率、排序筛选需求和最终控件选择。

不推荐/禁止：
1. 禁止上千条动态数据直接使用QTableWidget或QListWidget。
2. 禁止为了“写起来快”循环创建数千个QTableWidgetItem或调用addItem。
3. 禁止在需求包含排序、筛选、分页或共享数据时仍把数据状态分散在Item对象中。

参考来源：[Qt Model/View Programming](https://doc.qt.io/qt-6/model-view-programming.html)、[QAbstractTableModel](https://doc.qt.io/qt-6/qabstracttablemodel.html)

## 2. Model数据职责与data回调
场景：实现QAbstractTableModel或QAbstractListModel并保持滚动、选择和刷新流畅。

推荐做法：
1. Model持有已准备好的内存数据或轻量索引；在后台完成IO、解析和重计算，再通过GUI线程更新Model。
2. `rowCount()`、`columnCount()`和`data()`只执行有界、可预测的内存读取。
3. `data()`按role返回最少必要内容；DisplayRole、DecorationRole、ToolTipRole和对齐角色保持语义明确。
4. `headerData()`提供稳定、可本地化的列标题。
5. 可编辑Model通过`setData()`修改底层数据并发送精确`dataChanged`。

不推荐/禁止：
1. 禁止在`data()`中读取文件、访问数据库、调用网络、解析大JSON或创建昂贵图像。
2. 禁止在每次DisplayRole请求时重新格式化与业务无关的大对象。
3. 禁止从工作线程直接调用Model更新接口；使用queued信号把结果交回GUI线程。
4. 禁止用异常吞噬隐藏无效index或损坏的数据结构。

参考来源：[QAbstractItemModel线程安全](https://doc.qt.io/qt-6/qabstractitemmodel.html)、Qt Model/View官方示例

## 3. flags与编辑边界
场景：只读表格、可编辑表单表格、拖放列表或带复选框的数据视图。

推荐做法：
1. 只读业务表格保留ItemIsEnabled和ItemIsSelectable。
2. 只有可编辑列增加ItemIsEditable；复选框列按数据语义增加ItemIsUserCheckable。
3. 拖放只在业务确有排序或归组需求时启用，并同时实现对应mime/drop接口。
4. 编辑失败返回False并保持原值，向界面提供明确校验反馈。

不推荐/禁止：
1. 禁止所有单元格无条件可编辑。
2. 禁止声明拖放flags却没有一致的数据移动实现。
3. 禁止把按钮、复杂表单和持续动画塞入每一行的indexWidget。

参考来源：[QAbstractItemModel flags](https://doc.qt.io/qt-6/qabstractitemmodel.html)、[QAbstractItemView](https://doc.qt.io/qt-6/qabstractitemview.html)

## 4. 数据更新与局部刷新
场景：后台数据持续到达、单行状态变化、批量追加或整个数据集切换。

推荐做法：
1. 单元格或连续范围变化时发射带准确index范围和roles的`dataChanged`。
2. 插入行使用`beginInsertRows`/`endInsertRows`；删除行使用对应begin/end接口。
3. 只有数据结构整体替换、旧index全部失效时才使用beginResetModel/endResetModel。
4. 高频更新合并为短批次，控制UI刷新频率，同时保留最新值和错误状态。
5. 远端或超大数据源使用`canFetchMore()`/`fetchMore()`或业务分页，避免一次创建全部显示对象。

不推荐/禁止：
1. 禁止每个数据点变化都reset整个Model。
2. 禁止修改底层列表后不发送Model通知。
3. 禁止循环逐行addItem作为批量导入策略。
4. 禁止后台线程同时读写Model内部容器。

参考来源：[QAbstractItemModel](https://doc.qt.io/qt-6/qabstractitemmodel.html)、Qt Fetch More示例

## 5. Delegate使用边界
场景：需要自定义单元格绘制、进度显示、状态徽标或专用编辑器。

推荐做法：
1. 默认使用QStyledItemDelegate，保留原生style、选中、焦点和禁用状态。
2. 在`paint()`中复用轻量对象、缓存稳定资源，并只绘制当前可见index。
3. 复杂编辑器按需在`createEditor()`创建，编辑结束立即提交和关闭。
4. 动画或高频状态使用视图级计时和受控viewport更新，不为每个单元格创建计时器。

不推荐/禁止：
1. 禁止在Delegate绘制路径执行IO、SVG重复解析或重度计算。
2. 禁止每次paint创建字体、渐变、图标缓存和大Pixmap。
3. 禁止用setIndexWidget为数千行常驻创建复杂Widget。
4. 禁止自定义绘制后丢失选中、焦点、禁用或高对比度状态。

参考来源：[QStyledItemDelegate](https://doc.qt.io/qt-6/qstyleditemdelegate.html)、Qt Spin Box Delegate示例

## 6. 视图性能设置
场景：数千行表格或大型树在滚动、排序、展开和刷新时出现卡顿。

推荐做法：
1. QTableView使用稳定的`verticalHeader().setDefaultSectionSize()`控制固定默认行高；避免每行内容自动测量。
2. QTreeView只有在全部行高一致时使用`setUniformRowHeights(True)`；该API不属于QTableView。
3. 关闭确实不需要的word wrap和逐单元格尺寸计算；为昂贵列提供合理默认宽度。
4. 使用viewport范围更新和精确Model通知，不无条件调用全视图repaint。
5. 性能结论通过目标数据量、滚动和更新频率测量，不以控件创建成功代替。

不推荐/禁止：
1. 禁止对QTableView调用不存在的setUniformRowHeights。
2. 禁止频繁使用ResizeToContents扫描数千行作为实时列宽策略。
3. 禁止每次数据变化都调用resizeRowsToContents或resizeColumnsToContents。
4. 禁止通过关闭选择、焦点或可访问性来换取表面性能。

参考来源：[QTableView](https://doc.qt.io/qt-6/qtableview.html)、[QTreeView](https://doc.qt.io/qt-6/qtreeview.html)

## 7. 表头交互与列状态
场景：高信息密度业务表格需要可读默认布局，并允许用户按工作流调整。

推荐做法：
1. 为关键列设置合理初始宽度；文本主列可Stretch，数值和状态列优先Interactive或固定最小宽度。
2. 使用QHeaderView的Interactive模式允许用户拖拽列宽；需要时允许移动列和显示/隐藏次要列。
3. 保存QHeaderView的saveState结果，并在列模型与版本兼容时restoreState。
4. 排序指示器与实际Model排序保持一致；无排序能力时不要展示可点击假象。
5. 提供“恢复默认列布局”操作，避免损坏状态永久困住用户。

不推荐/禁止：
1. 禁止把全部列设为Stretch导致数值列浪费空间、文本列不足。
2. 禁止启动时每次覆盖用户已保存的列宽。
3. 禁止恢复旧列状态失败后留下不可见关键列。

参考来源：[QHeaderView](https://doc.qt.io/qt-6/qheaderview.html)、[Spyder](https://github.com/spyder-ide/spyder)

## 8. 选择模式决策
场景：查看详情、批量操作、连续范围处理或清单勾选。

推荐做法：
1. 查看单条详情或单对象编辑：SingleSelection配合SelectRows。
2. 独立多项批处理：MultiSelection，或更符合桌面习惯的ExtendedSelection。
3. Shift连续范围任务：ContiguousSelection或ExtendedSelection，并提供清晰选中计数。
4. 长期业务选择状态使用数据字段或复选框Model角色，不依赖瞬时selection model。

不推荐/禁止：
1. 禁止无批处理功能却默认ExtendedSelection。
2. 禁止仅用颜色表达选中状态而没有焦点、行标识或辅助信息。
3. 禁止把瞬时选中行持久化为长期业务数据。

参考来源：[QAbstractItemView SelectionMode](https://doc.qt.io/qt-6/qabstractitemview.html)、Qt Selection Model文档

## 9. 反模式清单
场景：AI生成或评审大数据表格、列表和树代码。

推荐做法：
1. 输出前主动报告数据量级、更新方式、控件选择、刷新策略和用户选择模式。
2. 对性能建议附带可观测验证方法：目标行数、滚动、排序、增量更新和内存占用。

不推荐/禁止：
1. 数千行循环创建Item对象。
2. `data()`内执行IO或业务计算。
3. 任意更新都reset整个Model。
4. Delegate每次paint解析SVG或创建复杂Widget。
5. 实时ResizeToContents扫描全表。
6. 表头不可调整且没有状态恢复。

参考来源：Qt官方Model/View示例、[Spyder](https://github.com/spyder-ide/spyder)、[Cura](https://github.com/Ultimaker/Cura)的大数据工作流；不得引入Cura的非Widget界面实现
