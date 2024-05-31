from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QComboBox, \
    QPushButton, QMessageBox

from database import admin_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class EditUserWindow(QAppWindow):
    def __init__(self, login: str):
        super().__init__()
        self.login = login
        self.setWindowTitle(f"Изменить пользователя {self.login}")

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.math_operator_worker = admin_bd.UserDataBaseWorker()
        self._init_type_combobox()

    def __get_layout(self):
        layout = QGridLayout()

        self.user_label = QLabel("Введите логин")

        self.user_input = QLineEdit("")
        self.user_input.setPlaceholderText('Введите новый логин')
        self.user_input.textChanged.connect(self.__input_add_new_user_changed)

        self.password_label = QLabel("Введите пароль")

        self.password_input = QLineEdit("")
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.textChanged.connect(self.__input_add_new_user_changed)

        self.user_type_label = QLabel("Выберите тип пользователя")

        self.type_combobox = QComboBox(self)

        self.edit_btn = QPushButton(self)
        self.edit_btn.setText("Изменить данные")
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.__edit_btn_clicked)

        layout.addWidget(self.user_label, 0, 0)
        layout.addWidget(self.user_input, 0, 1)
        layout.addWidget(self.password_label, 1, 0)
        layout.addWidget(self.password_input, 1, 1)
        layout.addWidget(self.user_type_label, 2, 0)
        layout.addWidget(self.type_combobox, 2, 1)
        layout.addWidget(self.edit_btn, 3, 0, 2, 0)

        return layout

    def __input_add_new_user_changed(self):
        self.edit_btn.setEnabled(bool(self.user_input.text() and self.password_input.text()
                                      and self.type_combobox.currentText()))

    def __edit_btn_clicked(self):
        try:
            self.math_operator_worker.update_user(self.login, self.user_input.text(), self.password_input.text(),
                                                  self.type_combobox.currentText())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при изменении пользователя")
            return
        QMessageBox.information(self, "Успех", "Пользователь успешно изменен")

    def _init_type_combobox(self):
        user_types = self.math_operator_worker.get_user_types()
        user_types = list(map(lambda x: x[0], user_types))
        self.type_combobox.clear()
        self.type_combobox.addItems(user_types)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = EditUserWindow('admin')
    window.show()
    sys.exit(app.exec())
