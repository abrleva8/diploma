from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHBoxLayout, QTableView, QMessageBox, QPushButton, \
    QWidget

import pandas as pd
from PyQt6 import QtWidgets

from math_model import PandasModel, LinRegression
from plotting.canvas import Canvas


class ResearcherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.model = None
        self.setWindowTitle("Исследователь")

        menu = self.menuBar()
        file_menu = menu.addMenu("Файл")

        open_QAction = QAction("Открыть", self)
        open_QAction.triggered.connect(self.open_file_dialog)

        file_menu.addAction(open_QAction)

        layout = QHBoxLayout()
        self.table = QTableView()
        self.canvas = Canvas()
        self.button_train = QPushButton("Обучить")
        self.button_train.clicked.connect(self.train_data)

        layout.addWidget(self.table)
        layout.addWidget(self.button_train)
        layout.addWidget(self.canvas)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_file_dialog(self) -> None:
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        file_name, _ = QFileDialog.getOpenFileName(self, filter=file_filter)
        if file_name:
            self.read_data(file_name=file_name)
        else:
            QMessageBox.warning(self, 'Ошибка', 'Файл не выбран')

    def read_data(self, file_name) -> None:
        format = file_name.split('.')[-1]
        if format == 'xlsx':
            data = pd.read_excel(file_name)
        else:
            data = pd.read_csv(file_name)

        self.data = data
        self.model = PandasModel(data)
        self.table.setModel(self.model)

    def train_data(self) -> None:
        y_true, y_predict = LinRegression(self.data).train()
        self.canvas.plot(y_true, y_predict)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ResearcherWindow()
    window.show()
    sys.exit(app.exec())
