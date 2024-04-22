import pandas as pd
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout, QPushButton

from interface.qModelSelectionWidget import ModelSelectionWidget
from interface.qPlottingWin import PlottingWindow


def dataframe_generation_from_table(table):
    number_of_rows = table.rowCount()
    number_of_columns = table.columnCount()

    tmp_df = pd.DataFrame(index=range(number_of_rows), columns=range(number_of_columns))

    for i in range(number_of_rows):
        for j in range(2, number_of_columns):
            tmp_df.iloc[i, j] = float(table.item(i, j).text())

    return tmp_df


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
        exploratory_layout = QHBoxLayout()

        self.exploratory_btn = QPushButton('EDA')
        self.exploratory_btn.clicked.connect(self.__exploratory_btn_clicked)

        table_layout.addWidget(self.table)

        exploratory_layout.addWidget(self.exploratory_btn)

        self.model_selection_widget = ModelSelectionWidget()
        self.model_selection_widget.eq_signal.connect(self.__get_eq)

        methods_layout.addWidget(self.model_selection_widget)
        methods_layout.addLayout(exploratory_layout)

        layout.addLayout(table_layout)
        layout.addLayout(methods_layout)

        return layout

    def __get_eq(self, eq: tuple[bool, list[str]]) -> None:
        self.eq = eq

    def __exploratory_btn_clicked(self):
        tmp_df = dataframe_generation_from_table(self.table)
        self.plotting_win = PlottingWindow(tmp_df, cols=tmp_df.columns)
        self.plotting_win.show()
