import pandas as pd
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout, \
    QPushButton, QGridLayout, QLabel

from interface.qEDASettingsWindow import EDASettingsWindow
from interface.qModelSelectionWidget import ModelSelectionWidget
from interface.qNormalAnalystWindow import NormalAnalystWindow
from interface.qPlottingWin import PlottingWindow


def dataframe_generation_from_table(table, columns: list[str] = None) -> pd.DataFrame:
    number_of_rows = table.rowCount()
    number_of_columns = table.columnCount()

    columns = columns if columns else [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]

    tmp_df = pd.DataFrame(index=range(number_of_rows), columns=columns)

    for i in range(number_of_rows):
        for j in range(2, number_of_columns):
            tmp_df.iloc[i, j] = float(table.item(i, j).text())

    for j in range(2, number_of_columns):
        tmp_df = tmp_df.astype({tmp_df.columns[j]: 'float32'})

    return tmp_df


class MathModelWidget(QWidget):
    size_sgn = pyqtSignal(int)

    def __init__(self):
        super(QWidget, self).__init__()
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
        analysis_layout = QGridLayout()

        eda_label = QLabel('Разведочный анализ')
        analysis_layout.addWidget(eda_label, 0, 0)

        settings_btn = QPushButton('Настройки')
        settings_btn.clicked.connect(self.__settings_btn_clicked)
        analysis_layout.addWidget(settings_btn, 1, 0)

        self.exploratory_btn = QPushButton('EDA')
        self.exploratory_btn.clicked.connect(self.__exploratory_btn_clicked)

        table_layout.addWidget(self.table)

        analysis_layout.addWidget(self.exploratory_btn, 2, 0)

        self.model_selection_widget = ModelSelectionWidget()
        self.model_selection_widget.eq_signal.connect(self.__get_eq)

        analysis_layout.addWidget(self.model_selection_widget, 3, 0)

        layout.addLayout(table_layout)
        layout.addLayout(analysis_layout)

        return layout

    def __get_eq(self, eq: tuple[bool, list[str]]) -> None:
        self.eq = eq

    # def __exploratory_btn_clicked(self):
    #     tmp_df = dataframe_generation_from_table(self.table)
    #     self.plotting_win = PlottingWindow(tmp_df, cols=tmp_df.columns)
    #     self.plotting_win.show()

    def __exploratory_btn_clicked(self):
        tmp_df = dataframe_generation_from_table(self.table)
        self.plotting_win = NormalAnalystWindow(tmp_df)
        self.plotting_win.show()

    def __settings_btn_clicked(self):
        self.__qEDASettingsWindow = EDASettingsWindow()
        self.__qEDASettingsWindow.show()
        self.__qEDASettingsWindow.eda_set_signal.connect(self.__eda_set_signal)

    def __eda_set_signal(self, is_normal_check, check_method):
        self.__is_normal_check = is_normal_check
        self.__check_method = check_method


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MathModelWidget()
    window.show()
    sys.exit(app.exec())
