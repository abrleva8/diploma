import pandas as pd
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout, \
    QPushButton, QGridLayout, QLabel, QRadioButton, QLineEdit, QButtonGroup

from interface.qEDASettingsWindow import EDASettingsWindow
from interface.qNormalAnalystWindow import NormalAnalystWindow
from utils.eq_creator import get_linear, get_quad, get_new_x


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

    table_sgn = pyqtSignal(QTableWidget)

    def __init__(self):
        super(QWidget, self).__init__()
        self.model_size = None
        self.df_manager = None
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

        self.model_size = num_cols - 3

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

        self.model_btn_gp = QButtonGroup()
        self.model_btn_gp.setObjectName('model_btn_gp')

        model_lbl = QLabel('Модель: ')

        linear_rb = QRadioButton('Линейная')
        quad_rb = QRadioButton('Квадратичная')
        user_rb = QRadioButton('Пользовательская')
        self.model_btn_gp.addButton(linear_rb, 1)
        self.model_btn_gp.addButton(quad_rb, 2)
        self.model_btn_gp.addButton(user_rb, 3)
        self.model_btn_gp.buttonClicked.connect(self.__set_result_txt_ed)
        self.result_txt_ed = QLineEdit()
        self.result_txt_ed.setEnabled(False)
        self.apply_text_btn = QPushButton('Применить')
        self.apply_text_btn.clicked.connect(self.__apply_btn_clicked)

        analysis_layout.addWidget(model_lbl, 3, 0)
        analysis_layout.addWidget(linear_rb, 4, 0)
        analysis_layout.addWidget(quad_rb, 5, 0)
        analysis_layout.addWidget(user_rb, 6, 0)
        analysis_layout.addWidget(self.result_txt_ed, 7, 0)
        analysis_layout.addWidget(self.apply_text_btn, 8, 0)

        layout.addLayout(table_layout)
        layout.addLayout(analysis_layout)

        return layout

    def __get_eq(self, eq: tuple[bool, list[str]]) -> None:
        self.eq = eq

    def __exploratory_btn_clicked(self):
        self.plotting_win = NormalAnalystWindow(self.df_manager.df)
        self.plotting_win.show()

    def __settings_btn_clicked(self):
        self.__qEDASettingsWindow = EDASettingsWindow()
        self.__qEDASettingsWindow.show()
        self.__qEDASettingsWindow.eda_set_signal.connect(self.__eda_set_signal)

    def __eda_set_signal(self, is_normal_check, check_method):
        self.__is_normal_check = is_normal_check
        self.__check_method = check_method

    def __set_result_txt_ed(self, btn: QRadioButton) -> None:
        text = btn.text()
        match text:
            case 'Линейная':
                self.result_txt_ed.setEnabled(False)
                self.result_txt_ed.setText(get_linear(self.model_size, add_y=True))
            case 'Квадратичная':
                self.result_txt_ed.setEnabled(False)
                self.result_txt_ed.setText(get_quad(self.model_size, add_y=True))
            case 'Пользовательская':
                self.result_txt_ed.setEnabled(True)
                self.result_txt_ed.setText('y = ')
            case _:
                self.result_txt_ed.setText('')

    def __apply_btn_clicked(self):
        import pingouin as pg
        new_X = get_new_x(self.df_manager.df, self.result_txt_ed.text())
        self.result = pg.linear_regression(new_X, self.df_manager.df[self.df_manager.df.columns[-1]])

        # self.table_sgn.emit(result)
        # self.layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(False)

        return self.result


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MathModelWidget()
    window.show()
    sys.exit(app.exec())
