from sqlite3 import IntegrityError

from PyQt6.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)

from database import material_bd


class AddTypeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить тип")

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def __get_layout(self):
        layout = QGridLayout()

        self.type_lbl = QLabel("Тип материала")

        self.type_input = QLineEdit("")
        self.type_input.setPlaceholderText('Введите тип')
        self.type_input.textChanged.connect(self.__input_add_new_unit_changed)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить тип материала")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.__add_button_clicked)

        layout.addWidget(self.type_lbl, 0, 0)
        layout.addWidget(self.type_input, 0, 1)
        layout.addWidget(self.add_button, 1, 0, 2, 0)

        return layout

    def __input_add_new_unit_changed(self):
        self.add_button.setEnabled(bool(self.type_input.text()))

    def __add_button_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        try:
            math_operator_worker.insert_type(self.type_input.text())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Тип материала с таким обозначением уже существует")
            return
        QMessageBox.information(self, "Успех", "Тип материала успешно добавлен")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddTypeWindow()
    window.show()
    sys.exit(app.exec())
