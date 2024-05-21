from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QFormLayout, QGridLayout, QComboBox, QCheckBox, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QButtonGroup, QMessageBox

import utils.eq_creator
from utils.eq_creator import get_linear, get_quad, get_new_x


class ModelSelectionWidget(QWidget):

    eq_signal = pyqtSignal(tuple)

    def __init__(self):
        super(QWidget, self).__init__()
        self.__size = None
        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def set_size(self, size: int):
        self.__size = size

    def __get_layout(self):
        layout = QGridLayout()

        self.model_btn_gp = QButtonGroup()
        self.model_btn_gp.setObjectName('model_btn_gp')

        model_lbl = QLabel('Модель: ')

        linear_rb = QRadioButton('Линейная')
        quad_rb = QRadioButton('Квадратичная')
        user_rb = QRadioButton('Пользовательская')
        self.model_btn_gp.addButton(linear_rb, 1)
        self.model_btn_gp.addButton(quad_rb, 2)
        self.model_btn_gp.addButton(user_rb, 3)
        self.model_btn_gp.buttonClicked.connect(self.__set_result_txt_ed)
        self.result_txt_ed = QLineEdit()
        self.result_txt_ed.setEnabled(False)
        apply_text_btn = QPushButton('Применить')
        apply_text_btn.clicked.connect(self.__apply_btn_clicked)

        layout.addWidget(model_lbl, 0, 0)
        layout.addWidget(linear_rb, 1, 0)
        layout.addWidget(quad_rb, 2, 0)
        layout.addWidget(user_rb, 3, 0)
        layout.addWidget(self.result_txt_ed, 4, 0)
        layout.addWidget(apply_text_btn, 5, 0)

        return layout

    # TODO: add exception if pars_eq doesn't work
    def __apply_btn_clicked(self):
        eq = utils.eq_creator.pars_eq(self.result_txt_ed.text())
        self.eq_signal.emit(eq)
