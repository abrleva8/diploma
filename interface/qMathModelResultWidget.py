import pandas as pd
from PyQt6.QtWidgets import QWidget, QLayout, QHBoxLayout, QTableWidget, QHeaderView, QAbstractItemView, QTableView, \
    QTableWidgetItem


class MathModelResultWidget(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        # self.mathModelWidget = mathModelWidget
        # self.mathModelWidget.connect(self.__set_result)

        self.table = QTableWidget(self)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def set_table_widget(self, df: pd.DataFrame):
        df = df.round(2)
        self.table.clear()
        headers = df.columns.values.tolist()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        for i, row in df.iterrows():
            # Добавление строки
            self.table.setRowCount(self.table.rowCount() + 1)

            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

    def __get_layout(self) -> QLayout:
        layout = QHBoxLayout()
        layout.addWidget(self.table)
        return layout


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MathModelResultWidget()
    window.show()
    sys.exit(app.exec())
