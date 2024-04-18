from PyQt6.QtWidgets import QWidget, QFormLayout, QGridLayout, QComboBox, QCheckBox, QRadioButton, QVBoxLayout, \
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox, QButtonGroup


class ModelSelectionWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def __get_layout(self):
        layout = QVBoxLayout()

        model_btn_gp = QButtonGroup()

        model_lbl = QLabel('Модель: ')

        linear_rb = QRadioButton('Линейная')
        quad_rb = QRadioButton('Квадратичная')
        user_rb = QRadioButton('Пользовательская')
        model_btn_gp.addButton(linear_rb)
        model_btn_gp.addButton(quad_rb)
        model_btn_gp.addButton(user_rb)

        result_txt_ed = QLineEdit()
        result_txt_ed.setEnabled(False)
        apply_btn = QPushButton('Применить')

        layout.addWidget(model_lbl)
        layout.addWidget(linear_rb)
        layout.addWidget(quad_rb)
        layout.addWidget(user_rb)
        layout.addWidget(result_txt_ed)
        layout.addWidget(apply_btn)

        layout.setSpacing(0)

        return layout
