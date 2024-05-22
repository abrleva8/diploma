from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from database import material_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class AddResultWindow(QAppWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление результата")

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self._center()

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.__init_unit_combobox()

    def __get_layout(self):
        layout = QGridLayout()

        self.result_label = QLabel("Введите результат")
        layout.addWidget(self.result_label, 0, 0)

        self.result_input = QLineEdit("")
        self.result_input.setPlaceholderText('Введите новый результат')
        self.result_input.textChanged.connect(self.__input_add_new_result_changed)
        layout.addWidget(self.result_input, 0, 1)

        self.unit_label = QLabel("Выберите единицу измерения")
        layout.addWidget(self.unit_label, 1, 0)

        self.unit_combobox = QComboBox(self)
        layout.addWidget(self.unit_combobox, 1, 1)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить результат")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.__add_button_clicked)
        layout.addWidget(self.add_button, 2, 0, 2, 0)

        return layout

    def _center(self):
        pass

    def __input_add_new_result_changed(self):
        self.add_button.setEnabled(bool(self.result_input.text() and self.unit_combobox.currentText()))

    def __init_unit_combobox(self):
        units = self.math_operator_worker.get_units()
        units = list(map(lambda x: x[0], units))
        self.unit_combobox.clear()
        self.unit_combobox.addItems(units)

    def __add_button_clicked(self):
        try:
            self.math_operator_worker.insert_result(self.result_input.text(), self.unit_combobox.currentText())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Результат с таким названием уже существует")
            return
        QMessageBox.information(self, "Успех", "Результат успешно добавлен")
