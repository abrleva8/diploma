import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QWidget, QLayout, QLabel, QFormLayout, QDoubleSpinBox, QPushButton


class PredictTabWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.columns = None
        self.predict_feature = None
        self.__update_layout()

    def __get_layout(self) -> QLayout | None:
        if self.columns is None:
            return None

        layout = QFormLayout()

        for column in self.columns:
            column_lbl = QLabel(column)
            column_lbl.setObjectName(f'{column}_lbl')

            column_spin_box = QDoubleSpinBox()
            column_spin_box.setObjectName(f'{column}_spin_box')

            layout.addRow(column_lbl, column_spin_box)

        predict_btn = QPushButton('Рассчитать')
        predict_btn.setObjectName('predict_btn')
        layout.addRow(predict_btn)

        predict_lbl = QLabel(self.predict_feature)
        predict_lbl.setObjectName('predict_lbl')
        predict_value_lbl = QLabel()
        predict_value_lbl.setObjectName('predict_value_lbl')
        layout.addRow(predict_lbl, predict_value_lbl)

        predict_btn.clicked.connect(self.create_df_for_predict)

        return layout

    def set_columns(self, columns: list[str], predict_feature: str):
        self.columns = columns
        self.predict_feature = predict_feature
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

    def create_df_for_predict(self) -> pd.DataFrame | None:
        if self.columns is None:
            return None

        values_lst = []
        for column in self.columns:
            values_lst.append(float(self.findChild(QDoubleSpinBox,
                                                   f'{column}_spin_box').text().replace(',', '.')))

        df = pd.DataFrame(np.array(values_lst).reshape(1, -1), columns=self.columns)

        return df
