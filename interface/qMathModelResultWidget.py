import pandas as pd

from PyQt6.QtWidgets import QWidget, QLayout, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QLabel


class MathModelResultWidget(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        self.table = QTableWidget(self)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.fisher_lbl = QLabel()
        self.fisher_table_lbl = QLabel()
        self.fisher_result_lbl = QLabel()

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

    def set_fisher_info(self, fisher: float, fisher_table: float) -> None:

        fisher = round(fisher, 2)
        fisher_table = round(fisher_table, 2)

        self.fisher_lbl.setText(f'Значения критерия Фишера равно = {fisher}')
        self.fisher_table_lbl.setText(f'Табличное значение критерия Фишера равно = {fisher_table}')

        if fisher > fisher_table:
            self.fisher_result_lbl.setText('Критерий Фишера выполняется!')
            self.fisher_result_lbl.setStyleSheet('color: green;')
        else:
            self.fisher_result_lbl.setText('Критерий Фишера не выполняется!')
            self.fisher_result_lbl.setStyleSheet('color: red;')

    def __get_layout(self) -> QLayout:
        layout = QHBoxLayout()

        table_layout = QGridLayout()
        info_layout = QVBoxLayout()

        table_layout.addWidget(self.table, 0, 0)

        info_layout.addWidget(self.fisher_lbl)
        info_layout.addWidget(self.fisher_table_lbl)
        info_layout.addWidget(self.fisher_result_lbl)

        layout.addLayout(table_layout)
        layout.addLayout(info_layout)

        return layout


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MathModelResultWidget()
    window.show()
    sys.exit(app.exec())
