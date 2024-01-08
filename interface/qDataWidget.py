import pandas as pd
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QHBoxLayout, QPushButton, QTableView, QFileDialog, \
    QMessageBox, QVBoxLayout

from math_model import PandasModel


# TODO: переписать через findChild
class DataWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.my_layout = self.__get_user_layout()
        self.setLayout(self.my_layout)

    def __get_user_layout(self) -> QLayout:
        layout = QHBoxLayout()

        layout_buttons = self.__button_layout()
        layout_table = self.__table_layout()

        layout.addLayout(layout_buttons)
        layout.addLayout(layout_table)

        return layout

    def __button_layout(self) -> QLayout:
        layout = QVBoxLayout()

        data_from_base = QPushButton("Загрузить из базы")
        data_from_file = QPushButton("Загрузить из файла")

        data_from_file.clicked.connect(self.__open_file_dialog)

        layout.addWidget(data_from_base)
        layout.addWidget(data_from_file)

        layout.setObjectName('layout_buttons')

        return layout

    def __table_layout(self) -> QLayout:
        layout = QGridLayout()

        self.table = QTableView()
        self.table.setObjectName('table_view')

        layout.addWidget(self.table)
        layout.setObjectName('layout_table')

        return layout

    def __open_file_dialog(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        file_name, _ = QFileDialog.getOpenFileName(self, filter=file_filter)
        if file_name:
            self.__read_data(file_name=file_name)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Файл не выбран')

    def __read_data(self, file_name) -> pd.DataFrame:
        format = file_name.split('.')[-1]
        if format == 'xlsx':
            data = pd.read_excel(file_name)
        else:
            data = pd.read_csv(file_name)

        self.data = data
        self.model = PandasModel(data)
        self.table.setModel(self.model)
        # table_layout = self.layout().findChild(QLayout, 'layout_table')
        # print(table_layout)
        # print(type(table_layout))
        # table = table_layout.findChild(QTableView, 'table_view')
        # print(table)
        # self.layout.wid
        # table.setModel(PandasModel(data))
        # table_layout.setModel(PandasModel(data))
        x = 1
