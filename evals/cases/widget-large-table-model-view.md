# Case: PySide6大数据表格Model-View

## Pressure scenario

基于PySide6实现窗口，展示数千条动态业务表格数据，支持单选；优化渲染性能；表头宽度允许拖拽调整，布局状态重启保留。

## Baseline failure risks without this Skill

- 循环创建数千个Item对象，启动和更新卡顿。
- 在Model data回调中读取文件、解析数据或执行耗时格式化。
- 每次单行更新都reset整个Model。
- 表头固定且用户调整无法保存。

## Required behavior with this Skill

- 选用QTableView与自定义QAbstractTableModel，并说明数千条数据的选型依据。
- data回调只读取准备好的内存数据；后台结果通过GUI线程更新Model。
- 单行或连续范围使用dataChanged，批量结构变化使用对应begin/end通知。
- 使用SingleSelection和SelectRows。
- QHeaderView采用Interactive列宽并保存、恢复header state。
- QTableView使用固定默认行高，不调用只属于QTreeView的统一行高API。

## Pass conditions

- 使用QTableView和自定义Model，不使用Item式表格控件。
- data回调不存在IO或重度计算。
- 具备精确局部刷新策略。
- 具备单选、可拖拽表头和表头状态持久化代码。
- 不引入任何非Widget界面实现。
