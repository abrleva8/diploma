import pandas as pd
from PyQt6.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLayout, QMessageBox

from database.material_bd import MaterialDataBaseWorker
from interface.qAddWindows.qAddResearchWindow import AddResearchWindow
from interface.qEditWindows.qEditResearchWindow import EditResearchWindow
from math_model.data_frame_manager import DataFrameManager


class ResearchWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = self.__get_material_layout()
        self.setLayout(self.layout)

        self.math_operator_worker = MaterialDataBaseWorker()
        self.get_researches()

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
        self.edit_research_btn = QPushButton('Редактировать эксперимент')
        self.delete_research_btn = QPushButton('Удалить эксперимент')

        self.edit_research_btn.setEnabled(False)
        self.delete_research_btn.setEnabled(False)

        add_research_btn.clicked.connect(self.__add_button_clicked)
        self.edit_research_btn.clicked.connect(self.__edit_button_clicked)
        self.delete_research_btn.clicked.connect(self.__delete_button_clicked)

        layout.addWidget(add_research_btn)
        layout.addWidget(self.edit_research_btn)
        layout.addWidget(self.delete_research_btn)

        return layout

    def __table_layout(self) -> QLayout:
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.selectionModel().selectionChanged.connect(self.__selection_changed)

        layout.addWidget(self.table)

        return layout

    def get_researches(self) -> None:
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

        for i, row in enumerate(data.iterrows()):
            for j, val in enumerate(row[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def __add_button_clicked(self):
        self.add_research_window = AddResearchWindow()
        self.add_research_window.show()

    def __edit_button_clicked(self):
        row = self.table.currentRow()
        research_number = int(self.table.item(row, 0).text())
        labels, values = [], []

        for c in range(self.table.columnCount()):
            it = self.table.horizontalHeaderItem(c)
            values.append(self.table.item(row, c).text())
            labels.append(str(c + 1) if it is None else it.text())

        labels = list(map(lambda x: x.split(':')[0], labels))
        result = dict(zip(labels, values))
        self.edit_research_window = EditResearchWindow(result, research_number)
        self.edit_research_window.show()

    def __delete_button_clicked(self):
        row = self.table.currentRow()
        research_number = int(self.table.item(row, 0).text())

        self.math_operator_worker.delete_research(research_number)

        QMessageBox.information(self, 'Успех', f'Эксперимент {research_number} успешно удален')

    def __selection_changed(self):
        is_enabled = len(self.table.selectedItems()) > 0

        self.edit_research_btn.setEnabled(is_enabled)
        self.delete_research_btn.setEnabled(is_enabled)
