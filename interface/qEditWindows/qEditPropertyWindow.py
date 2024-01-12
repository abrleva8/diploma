from sqlite3 import IntegrityError

from PyQt6.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)

from database import material_bd


class EditPropertyWindow(QMainWindow):
    def __init__(self, property_name: str, current_unit_denote: str):
        super().__init__()
        self.setWindowTitle("Изменить свойство")
        self.property_name = property_name
        self.current_unit_denote = current_unit_denote

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def __get_layout(self):
        layout = QGridLayout()

        self.curr_name_label = QLabel("Текущее название:")

        self.current_name_label = QLabel(self.property_name)

        self.new_name_label = QLabel("Новое название:")

        self.new_property_name_input = QLineEdit(self.property_name)
        self.new_property_name_input.textChanged.connect(self.__edit_button_enabled_check)

        self.curr_unit_denote_label = QLabel("Текущая ед. измерения:")

        self.current_unit_denote_label = QLabel(self.current_unit_denote)

        self.new_unit_denote_label = QLabel("Новая ед. измерения:")

        self.new_unit_denote_input = QLineEdit(self.current_unit_denote)
        self.new_unit_denote_input.textChanged.connect(self.__edit_button_enabled_check)

        self.edit_button = QPushButton(self)
        self.edit_button.setText("Изменить свойство")
        self.edit_button.setEnabled(bool(self.new_property_name_input.text()) and
                                    bool(self.new_unit_denote_input.text()))
        self.edit_button.clicked.connect(self.__edit_button_clicked)

        layout.addWidget(self.curr_name_label, 0, 0)
        layout.addWidget(self.current_name_label, 0, 1)
        layout.addWidget(self.new_name_label, 1, 0)
        layout.addWidget(self.new_property_name_input, 1, 1)
        layout.addWidget(self.curr_unit_denote_label, 2, 0)
        layout.addWidget(self.current_unit_denote_label, 2, 1)
        layout.addWidget(self.new_unit_denote_label, 3, 0)
        layout.addWidget(self.new_unit_denote_input, 3, 1)
        layout.addWidget(self.edit_button, 4, 0, 2, 0)

        return layout

    #
    def __edit_button_enabled_check(self):
        self.edit_button.setEnabled(bool(self.new_property_name_input.text()) and
                                    bool(self.new_unit_denote_input.text()))

    def __edit_button_clicked(self):
        # math_operator_worker = material_bd.MaterialDataBaseWorker()
        # try:
        #     math_operator_worker.edit_unit(self.unit_denote, self.new_unit_input.text())
        # except IntegrityError as e:
        #     QMessageBox.critical(self, "Ошибка", "Единица измерения с таким обозначением уже существует")
        #     return
        # QMessageBox.information(self, "Успех", "Единица измерения успешно изменена")
        pass


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EditPropertyWindow('test', 'test')
    window.show()
    sys.exit(app.exec())
