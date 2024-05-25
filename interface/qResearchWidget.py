import pandas as pd
from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLayout

from database.material_bd import MaterialDataBaseWorker
from math_model.data_frame_manager import DataFrameManager


class ResearchWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = self.__get_material_layout()
        self.setLayout(self.layout)

        self.math_operator_worker = MaterialDataBaseWorker()
        self.__get_researches()

    def __get_material_layout(self) -> QLayout:
        layout = QHBoxLayout()

        layout_table = self.__table_layout()
        layout_buttons = self.__button_layout()

        layout.addLayout(layout_table)
        layout.addLayout(layout_buttons)

        return layout

    def __button_layout(self) -> QLayout:

        layout = QVBoxLayout()

        add_research_btn = QPushButton('Добавить эксперимент')
        edit_research_btn = QPushButton('Редактировать эксперимент')
        delete_research_btn = QPushButton('Удалить эксперимент')

        layout.addWidget(add_research_btn)
        layout.addWidget(edit_research_btn)
        layout.addWidget(delete_research_btn)

        return layout

    def __table_layout(self) -> QLayout:
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(self.table)

        return layout

    def __get_researches(self) -> None:
        data, keys = self.math_operator_worker.get_raw_researches()

        df = pd.DataFrame(data=data, columns=keys)

        data = DataFrameManager.get_research_df(df)

        data_units, columns = self.math_operator_worker.get_params_with_units()
        df_units = pd.DataFrame(data=data_units, columns=columns)
        self.df_manager = DataFrameManager(df_units)
        rename_dict = self.df_manager.rename_dict()

        self.table.setRowCount(data.shape[0])
        self.table.setColumnCount(data.shape[1])
        self.table.setHorizontalHeaderLabels([rename_dict.get(key.lower(), key) for key in data.columns])

        for i, row in data.iterrows():
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
