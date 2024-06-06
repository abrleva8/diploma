from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QAbstractItemView, QHBoxLayout, QLayout, QLabel, \
    QFormLayout, QDoubleSpinBox, QPushButton


class PredictTabWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.columns = None
        self.__update_layout()

    def __get_layout(self) -> QLayout:
        if self.columns is None:
            return None

        layout = QFormLayout()

        for column in self.columns:
            column_lbl = QLabel(column)
            column_spin_box = QDoubleSpinBox()

            layout.addRow(column_lbl, column_spin_box)

        calc_btn = QPushButton('Рассчитать')
        layout.addRow(calc_btn)

        return layout

    def set_columns(self, columns: list[str]):
        self.columns = columns
        # print(self.columns)
        self.__update_layout()

    def __update_layout(self):
        self.layout = self.__get_layout()
        if self.layout is None:
            return
        self.clear_layout()
        self.layout = self.__get_layout()
        self.setLayout(self.layout)
        self.updateGeometry()

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
