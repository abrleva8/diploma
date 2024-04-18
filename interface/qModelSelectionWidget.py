from PyQt6.QtWidgets import QWidget, QFormLayout, QGridLayout, QComboBox, QCheckBox, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QButtonGroup


def get_linear(size: int) -> str:
    if not size:
        size = 3
    li_res = [f' a{i + 1}*x{i + 1} ' for i in range(size)]
    return 'y = a0 + ' + '+'.join(li_res)


class ModelSelectionWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.__size = None
        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def set_size(self, size: int):
        self.__size = size

    def __get_layout(self):
        layout = QVBoxLayout()

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
        apply_btn = QPushButton('Применить')

        layout.addWidget(model_lbl)
        layout.addWidget(linear_rb)
        layout.addWidget(quad_rb)
        layout.addWidget(user_rb)
        layout.addWidget(self.result_txt_ed)
        layout.addWidget(apply_btn)

        return layout

    def __set_result_txt_ed(self, btn: QRadioButton) -> None:
        text = btn.text()
        match text:
            case 'Линейная':
                self.result_txt_ed.setText(get_linear(self.__size))
            case 'Квадратичная':
                self.result_txt_ed.setText('y = a*x^2 + b')
            case 'Пользовательская':
                self.result_txt_ed.setText('y = f(x)')
            case _:
                self.result_txt_ed.setText('')
