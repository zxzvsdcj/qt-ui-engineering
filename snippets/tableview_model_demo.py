"""数千行QTableView + QAbstractTableModel最小可运行示例。"""

from __future__ import annotations

import sys
from collections.abc import Sequence

try:
    from PySide6.QtCore import QAbstractTableModel, QModelIndex, QObject, QSettings, Qt
    from PySide6.QtGui import QCloseEvent
    from PySide6.QtWidgets import (
        QApplication,
        QAbstractItemView,
        QHeaderView,
        QMainWindow,
        QTableView,
    )

    BINDING = "PySide6"
except ImportError:
    from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QObject, QSettings, Qt
    from PyQt6.QtGui import QCloseEvent
    from PyQt6.QtWidgets import (
        QApplication,
        QAbstractItemView,
        QHeaderView,
        QMainWindow,
        QTableView,
    )

    BINDING = "PyQt6"


Row = tuple[str, str, float]


class BusinessTableModel(QAbstractTableModel):
    HEADERS = ("订单号", "状态", "金额")

    def __init__(
        self, rows: Sequence[Row], parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self._rows = list(rows)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.HEADERS)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        value = self._rows[index.row()][index.column()]
        return f"{value:,.2f}" if index.column() == 2 else value

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return section + 1

    def sort(
        self,
        column: int,
        order: Qt.SortOrder = Qt.SortOrder.AscendingOrder,
    ) -> None:
        reverse = order == Qt.SortOrder.DescendingOrder
        self.layoutAboutToBeChanged.emit()
        self._rows.sort(key=lambda row: row[column], reverse=reverse)
        self.layoutChanged.emit()

    def replace_rows(self, rows: Sequence[Row]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def update_row(self, row: int, values: Row) -> None:
        if not 0 <= row < len(self._rows):
            raise IndexError(f"row out of range: {row}")
        self._rows[row] = values
        self.dataChanged.emit(
            self.index(row, 0),
            self.index(row, self.columnCount() - 1),
            [Qt.ItemDataRole.DisplayRole],
        )


def make_demo_rows(count: int = 5000) -> list[Row]:
    states = ("待处理", "处理中", "已完成")
    return [
        (f"ORD-{index:05d}", states[index % len(states)], index * 12.75)
        for index in range(1, count + 1)
    ]


class MainWindow(QMainWindow):
    HEADER_STATE_KEY = "table/header-state"

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Model-View大数据示例（{BINDING}）")
        self.resize(960, 640)
        self.setMinimumSize(640, 420)

        self.settings = QSettings("QtUiEngineering", "TableViewModelDemo")
        self.model = BusinessTableModel(make_demo_rows(), self)
        self.table = QTableView(self)
        self.table.setModel(self.model)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setDefaultSectionSize(26)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionsMovable(True)
        header.setStretchLastSection(True)

        saved_state = self.settings.value(self.HEADER_STATE_KEY)
        if saved_state is not None:
            self.table.horizontalHeader().restoreState(saved_state)

        self.setCentralWidget(self.table)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings.setValue(
            self.HEADER_STATE_KEY, self.table.horizontalHeader().saveState()
        )
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
