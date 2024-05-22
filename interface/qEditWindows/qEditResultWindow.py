from sqlite3 import IntegrityError

from PyQt6.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)

from database import material_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class EditResultWindow(QAppWindow):
    def __init__(self, result_name: str, current_unit_denote: str):
        super().__init__()
        self.setWindowTitle("Изменить результат")
        self.result_name = result_name
        self.current_unit_denote = current_unit_denote

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.__init_unit_combobox()

    def __get_layout(self):
        layout = QGridLayout()

        self.curr_name_label = QLabel("Текущее название:")

        self.current_name_label = QLabel(self.result_name)

        self.new_name_label = QLabel("Новое название:")

        self.new_result_name_input = QLineEdit(self.result_name)
        self.new_result_name_input.textChanged.connect(self.__edit_button_enabled_check)

        self.curr_unit_denote_label = QLabel("Текущая ед. измерения:")

        self.current_unit_denote_label = QLabel(self.current_unit_denote)

        self.new_unit_denote_label = QLabel("Новая ед. измерения:")

        self.new_unit_denote_combobox = QComboBox()
        self.new_unit_denote_combobox.currentTextChanged.connect(self.__edit_button_enabled_check)

        self.edit_button = QPushButton(self)
        self.edit_button.setText("Изменить результат")
        self.edit_button.setEnabled(bool(self.new_result_name_input.text()) and
                                    bool(self.new_unit_denote_combobox.currentText()))
        self.edit_button.clicked.connect(self.__edit_button_clicked)

        layout.addWidget(self.curr_name_label, 0, 0)
        layout.addWidget(self.current_name_label, 0, 1)
        layout.addWidget(self.new_name_label, 1, 0)
        layout.addWidget(self.new_result_name_input, 1, 1)
        layout.addWidget(self.curr_unit_denote_label, 2, 0)
        layout.addWidget(self.current_unit_denote_label, 2, 1)
        layout.addWidget(self.new_unit_denote_label, 3, 0)
        layout.addWidget(self.new_unit_denote_combobox, 3, 1)
        layout.addWidget(self.edit_button, 4, 0, 2, 0)

        return layout

    def __init_unit_combobox(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        units = math_operator_worker.get_units()
        units = list(map(lambda x: x[0], units))
        self.new_unit_denote_combobox.clear()
        self.new_unit_denote_combobox.addItems(units)

    #
    def __edit_button_enabled_check(self):
        self.edit_button.setEnabled(bool(self.new_result_name_input.text()) and
                                    bool(self.new_unit_denote_combobox.currentText()))

    def __edit_button_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        try:
            math_operator_worker.edit_result(self.result_name, self.current_unit_denote,
                                             self.new_result_name_input.text(),
                                             self.new_unit_denote_combobox.currentText())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Результат с такими параметрами уже существует")
            return
        QMessageBox.information(self, "Успех", "Результат успешно изменен")


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = EditResultWindow('test', 'test')
    window.show()
    sys.exit(app.exec())
