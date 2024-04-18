from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout

from interface.qModelSelectionWidget import ModelSelectionWidget


class MathModelWidget(QWidget):
    size_sgn = pyqtSignal(int)

    def __init__(self):
        super(QWidget, self).__init__()
        # self.__size = None
        self.table = QTableWidget(self)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def set_table_widget(self, table: QTableWidget):
        num_rows = table.rowCount()
        num_cols = table.columnCount()

        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols)

        for row in range(num_rows):
            for col_number in range(num_cols):
                item = table.item(row, col_number)
                if item:
                    self.table.setItem(row, col_number, item.clone())

        for col_number in range(num_cols):
            header_item = table.horizontalHeaderItem(col_number)

            if header_item:
                self.table.setHorizontalHeaderItem(col_number, header_item.clone())

        self.model_selection_widget.set_size(num_cols - 3)

    def change_header(self, table: QTableWidget):
        num_cols = table.columnCount()

        for col_number in range(num_cols):
            header_item = table.horizontalHeaderItem(col_number)
            if col_number == num_cols - 1:
                header_item.setText(f'{header_item.text()}, y')
            elif col_number > 1:
                header_item.setText(f'{header_item.text()}, x{col_number - 1}')

            if header_item:
                self.table.setHorizontalHeaderItem(col_number, header_item.clone())

    def __get_layout(self):
        layout = QHBoxLayout()

        table_layout = QVBoxLayout()
        methods_layout = QVBoxLayout()

        table_layout.addWidget(self.table)

        self.model_selection_widget = ModelSelectionWidget()
        methods_layout.addWidget(self.model_selection_widget)

        layout.addLayout(table_layout)
        layout.addLayout(methods_layout)

        return layout
