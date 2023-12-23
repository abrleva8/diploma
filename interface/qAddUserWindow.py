from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox, QPushButton, \
    QMessageBox

from database import admin_bd


class AddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить пользователя")

        layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self._center()

        self.math_operator_worker = admin_bd.DataBaseWorker()
        self._init_type_combobox()

    def _get_layout(self):
        layout = QGridLayout()

        self.user_label = QLabel("Введите логин")
        layout.addWidget(self.user_label, 0, 0)

        self.user_input = QLineEdit("")
        self.user_input.setPlaceholderText('Введите новый логин')
        self.user_input.textChanged.connect(self._input_add_new_user_changed)
        layout.addWidget(self.user_input, 0, 1)

        self.password_label = QLabel("Введите пароль")
        layout.addWidget(self.password_label, 1, 0)

        self.password_input = QLineEdit("")
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.textChanged.connect(self._input_add_new_user_changed)
        layout.addWidget(self.password_input, 1, 1)

        self.user_type_label = QLabel("Выберите тип пользователя")
        layout.addWidget(self.user_type_label, 2, 0)

        self.type_combobox = QComboBox(self)
        layout.addWidget(self.type_combobox, 2, 1)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить логин")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._add_button_clicked)
        layout.addWidget(self.add_button, 3, 0, 2, 0)

        return layout

    def _center(self):
        pass

    def _input_add_new_user_changed(self):
        self.add_button.setEnabled(bool(self.user_input.text() and self.password_input.text()
                                        and self.type_combobox.currentText()))

    def _add_button_clicked(self):
        try:
            self.math_operator_worker.insert_login(self.user_input.text(), self.password_input.text(),
                                                   self.type_combobox.currentText())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Пользователь с таким логином уже существует")
            return
        QMessageBox.information(self, "Успех", "Пользователь успешно добавлен")

    def _init_type_combobox(self):
        user_types = self.math_operator_worker.get_user_types()
        user_types = list(map(lambda x: x[0], user_types))
        self.type_combobox.clear()
        self.type_combobox.addItems(user_types)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddWindow()
    window.show()
    sys.exit(app.exec())
