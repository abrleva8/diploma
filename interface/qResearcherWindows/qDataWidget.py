import pandas as pd
from PyQt6.QtWidgets import QWidget, QLayout, QGridLayout, QHBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QVBoxLayout, QTableWidgetItem, QTableWidget, QComboBox, QFormLayout, QLabel, QAbstractItemView, \
    QHeaderView

from database import material_bd
from math_model.data_frame_manager import DataFrameManager


# TODO: переписать через findChild
class DataTabWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = self.__get_user_layout()
        self.setLayout(self.layout)

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
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
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
            QMessageBox.warning(self, 'Ошибка', 'Файл не выбран')

        self.layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(True)

    def __get_full_dataset(self) -> None:
        result = self.result_cmb.currentText()
        type_material = self.type_cmb.currentText()
        keys, data = self.math_operator_worker.get_full_dataset(type_material, result)

        data_units, columns = self.math_operator_worker.get_params_with_units()
        df_units = pd.DataFrame(data=data_units, columns=columns)
        self.df_manager = DataFrameManager(df_units)
        rename_dict = self.df_manager.rename_dict()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels([rename_dict.get(key.lower(), key) for key in keys])

        for i, row in enumerate(data):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        self.layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(True)

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

    def __read_data(self, file_name: str) -> None:
        df = pd.read_csv(file_name)
        keys = df.columns
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(keys)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                val = df.iloc[i, j]
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
