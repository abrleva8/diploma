import pandas as pd
import pingouin as pg

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QAbstractItemView, QHeaderView, QHBoxLayout, \
    QPushButton, QGridLayout, QLabel, QRadioButton, QLineEdit, QButtonGroup, QFileDialog, QMessageBox
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from interface.qEDASettingsWindow import EDASettingsWindow
from interface.qNormalAnalystWindow import NormalAnalystWindow
from math_model.data_frame_manager import DataFrameManager
from utils.eq_creator import get_linear, get_quad, get_new_x


def dataframe_generation_from_table(table, columns: list[str] = None) -> pd.DataFrame:
    number_of_rows = table.rowCount()
    number_of_columns = table.columnCount()

    columns = columns if columns else [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]

    tmp_df = pd.DataFrame(index=range(number_of_rows), columns=columns)

    for i in range(number_of_rows):

        for j in range(2):
            tmp_df.iloc[i, j] = table.item(i, j).text()

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
        self.df_manager: DataFrameManager = None
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
        self.__set_btn_enabled()

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

        self.save_df_btn = QPushButton('Сохранить')
        self.save_df_btn.setEnabled(False)
        self.save_df_btn.clicked.connect(self.__save_df_btn_clicked)

        eda_label = QLabel('Разведочный анализ')

        settings_btn = QPushButton('Настройки')
        settings_btn.clicked.connect(self.__settings_btn_clicked)

        self.exploratory_btn = QPushButton('EDA')
        self.exploratory_btn.clicked.connect(self.__exploratory_btn_clicked)

        self.model_btn_gp = QButtonGroup()
        self.model_btn_gp.setObjectName('model_btn_gp')

        model_lbl = QLabel('Модель: ')

        self.linear_rb = QRadioButton('Линейная')
        self.quad_rb = QRadioButton('Квадратичная')
        self.user_rb = QRadioButton('Пользовательская')

        self.linear_rb.setEnabled(False)
        self.quad_rb.setEnabled(False)
        self.user_rb.setEnabled(False)

        self.model_btn_gp.addButton(self.linear_rb, 1)
        self.model_btn_gp.addButton(self.quad_rb, 2)
        self.model_btn_gp.addButton(self.user_rb, 3)
        self.model_btn_gp.buttonClicked.connect(self.__set_result_txt_ed)

        self.result_txt_ed = QLineEdit()
        self.result_txt_ed.setEnabled(False)
        self.apply_text_btn = QPushButton('Применить')
        self.apply_text_btn.setEnabled(False)
        self.apply_text_btn.clicked.connect(self.__apply_btn_clicked)

        table_layout.addWidget(self.table)
        table_layout.addWidget(self.save_df_btn)

        analysis_layout.addWidget(eda_label, 0, 0)
        analysis_layout.addWidget(settings_btn, 1, 0)
        analysis_layout.addWidget(self.exploratory_btn, 2, 0)
        analysis_layout.addWidget(model_lbl, 3, 0)
        analysis_layout.addWidget(self.linear_rb, 4, 0)
        analysis_layout.addWidget(self.quad_rb, 5, 0)
        analysis_layout.addWidget(self.user_rb, 6, 0)
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

    def __set_btn_enabled(self) -> None:
        self.linear_rb.setEnabled(True)
        self.quad_rb.setEnabled(True)
        self.user_rb.setEnabled(True)
        self.apply_text_btn.setEnabled(True)

    def __save_df_btn_clicked(self):
        filename = QFileDialog.getSaveFileName(self, 'Сохранение данных', filter='*.csv')
        if not filename[0]:
            QMessageBox.warning(self, 'Сохранение данных', 'Вы не выбрали имя для сохранения')
            return
        self.df_manager.save_df(filename[0])
        QMessageBox.information(self, 'Сохранение данных', 'Данные успешно сохранены')

    def __apply_btn_clicked(self):

        new_X = get_new_x(self.df_manager.df, self.result_txt_ed.text())
        y = self.df_manager.get_y()
        self.result = pg.linear_regression(new_X, y)

        # TODO: create a class for the next code lines
        lr = LinearRegression()
        lr.fit(new_X, y)
        y_pred = lr.predict(new_X)

        pearson_corr = stats.pearsonr(y, y_pred)
        corr = pearson_corr.statistic

        f1 = len(lr.coef_)
        f2 = len(y) - f1 - 1

        dfn = min(f1, f2)
        dfd = max(f1, f2)

        self.fisher = corr ** 2 / (1 - corr ** 2) * (dfn / dfd)
        self.fisher_table = stats.f.ppf(q=0.95, dfn=dfn, dfd=dfd)
        self.r2 = lr.score(new_X, y)
        self.mse = mean_squared_error(y, y_pred)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MathModelWidget()
    window.show()
    sys.exit(app.exec())
