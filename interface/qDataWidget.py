import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QHBoxLayout, QPushButton, QTableView, QFileDialog, \
    QMessageBox, QVBoxLayout, QTableWidgetItem, QTableWidget, QComboBox, QFormLayout, QLabel, QAbstractItemView

from database import material_bd
from math_model import PandasModel


# TODO: переписать через findChild
class DataWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.my_layout = self.__get_user_layout()
        self.setLayout(self.my_layout)

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.__init_cmbs()

    def __init_cmbs(self):
        self.__init_result_cmb()
        self.__init_type_cmb()

    def __get_user_layout(self) -> QLayout:
        layout = QHBoxLayout()

        layout_buttons = self.__button_layout()
        layout_table = self.__table_layout()

        layout.addLayout(layout_buttons)
        layout.addLayout(layout_table)

        return layout

    # TODO: убрать self
    def __button_layout(self) -> QLayout:
        layout = QVBoxLayout()
        filter_layout = QFormLayout()

        raw_type_lbl = QLabel('Тип')
        self.type_cmb = QComboBox(self)
        result_lbl = QLabel('Результат')
        self.result_cmb = QComboBox(self)
        data_from_base_btn = QPushButton('Загрузить из базы')
        data_from_file_btn = QPushButton('Загрузить из файла')
        confirm_data_btn = QPushButton('Подтвердить выбор данных')
        confirm_data_btn.setObjectName('confirm_data')
        confirm_data_btn.setEnabled(False)

        data_from_base_btn.clicked.connect(self.__get_full_dataset)
        data_from_file_btn.clicked.connect(self.__open_file_dialog)
        confirm_data_btn.clicked.connect(self.__confirm_data)

        filter_layout.addRow(raw_type_lbl, self.type_cmb)
        filter_layout.addRow(result_lbl, self.result_cmb)

        layout.addLayout(filter_layout)
        layout.addWidget(data_from_base_btn)
        layout.addWidget(data_from_file_btn)
        layout.addWidget(confirm_data_btn)

        layout.setObjectName('layout_buttons')

        return layout

    def __table_layout(self) -> QLayout:
        layout = QGridLayout()

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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

    def __get_full_dataset(self) -> None:
        result = self.result_cmb.currentText()
        keys, data = self.math_operator_worker.get_full_dataset(result)

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels(keys)

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        self.my_layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(True)

    def __confirm_data(self):
        pass

    def __init_result_cmb(self) -> None:
        results = self.math_operator_worker.get_results()
        results = list(map(lambda x: x[0], results))
        self.result_cmb.clear()
        self.result_cmb.addItems(results)

    def __init_type_cmb(self):
        types = self.math_operator_worker.get_types()
        types = list(map(lambda x: x[0], types))
        types.append('Все')
        self.type_cmb.clear()
        self.type_cmb.addItems(types)

    def __read_data(self, file_name) -> pd.DataFrame | None:
        # format = file_name.split('.')[-1]
        # if format == 'xlsx':
        #     data = pd.read_excel(file_name)
        # else:
        #     data = pd.read_csv(file_name)
        #
        # self.data = data
        # self.model = PandasModel(data)
        # self.table.setModel(self.model)
        # # table_layout = self.layout().findChild(QLayout, 'layout_table')
        # # print(table_layout)
        # # print(type(table_layout))
        # # table = table_layout.findChild(QTableView, 'table_view')
        # # print(table)
        # # self.layout.wid
        # # table.setModel(PandasModel(data))
        # # table_layout.setModel(PandasModel(data))
        # x = 1
        pass
