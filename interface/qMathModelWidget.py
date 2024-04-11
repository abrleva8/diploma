from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView


class MathModelWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.table = QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.layout = self.__get_math_model_layout()
        self.setLayout(self.layout)

    def set_table_widget(self, table: QTableWidget):
        num_rows = table.rowCount()
        num_cols = table.columnCount()

        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols)

        for row in range(num_rows):
            for col in range(num_cols):
                item = table.item(row, col)
                if item is not None:
                    self.table.setItem(row, col, item.clone())

        for col in range(num_cols):
            header_item = table.horizontalHeaderItem(col)
            if header_item is not None:
                self.table.setHorizontalHeaderItem(col, header_item.clone())

    def __get_math_model_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        return layout
