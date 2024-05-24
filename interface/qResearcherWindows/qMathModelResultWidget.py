import numpy as np
import pandas as pd

from PyQt6.QtWidgets import QWidget, QLayout, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox


class MathModelResultWidget(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        self.table = QTableWidget(self)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def set_table_widget(self, df: pd.DataFrame):
        df = df.round(2)
        self.table.clear()
        self.table.setRowCount(0)
        headers = df.columns.values.tolist()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in df.iterrows():
            # Добавление строки
            self.table.setRowCount(self.table.rowCount() + 1)

            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))

    def set_fisher_info(self, fisher: float, fisher_table: float) -> None:

        fisher = round(fisher, 2)
        fisher_table = round(fisher_table, 2)

        self.fisher_lbl.setText(f'Значения критерия Фишера равно {fisher}')
        self.fisher_table_lbl.setText(f'Табличное значение критерия Фишера равно {fisher_table}')

        if fisher > fisher_table:
            self.fisher_result_lbl.setText('Критерий Фишера выполняется!')
            self.fisher_result_lbl.setStyleSheet('color: green;')
        else:
            self.fisher_result_lbl.setText('Критерий Фишера не выполняется!')
            self.fisher_result_lbl.setStyleSheet('color: red;')

    def set_determinate_info(self, r2: float, r2_table: float = 0.75) -> None:
        r2 = round(r2, 2)
        self.r2_lbl.setText(f'Значений критерия детерминированности равно {r2}')
        if r2 > r2_table:
            self.r2_lbl.setStyleSheet('color: green;')
        else:
            self.r2_lbl.setStyleSheet('color: red;')

    def set_mse(self, mse: np.float32) -> None:
        mse = round(float(mse), 2)
        self.mse_lbl.setText(f'Среднеквадратическая ошибка равна {mse}')

    def __get_layout(self) -> QLayout:
        layout = QHBoxLayout()

        table_layout = QGridLayout()
        info_layout = QVBoxLayout()

        self.save_model_btn = QPushButton('Сохранить')
        self.save_model_btn.setObjectName('save_model_btn')

        table_layout.addWidget(self.table, 0, 0)
        table_layout.addWidget(self.save_model_btn, 1, 0)

        self.fisher_lbl = QLabel()
        self.fisher_table_lbl = QLabel()
        self.fisher_result_lbl = QLabel()
        self.r2_lbl = QLabel()
        self.mse_lbl = QLabel()

        info_layout.addWidget(self.fisher_lbl)
        info_layout.addWidget(self.fisher_table_lbl)
        info_layout.addWidget(self.fisher_result_lbl)
        info_layout.addWidget(self.r2_lbl)
        info_layout.addWidget(self.mse_lbl)

        layout.addLayout(table_layout)
        layout.addLayout(info_layout)

        return layout

    def save_model(self, saver):
        filename = QFileDialog.getSaveFileName(self, 'Сохранение данных', filter='*.pkl')
        if not filename[0]:
            QMessageBox.warning(self, 'Сохранение данных', 'Вы не выбрали имя для сохранения')
            return
        saver.save(filename[0])
        QMessageBox.information(self, 'Сохранение данных', 'Модель успешно сохранена!')


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MathModelResultWidget()
    window.show()
    sys.exit(app.exec())
