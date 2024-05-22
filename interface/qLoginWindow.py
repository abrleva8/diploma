from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLayout, QLabel, QWidget, QLineEdit, QPushButton, QApplication, \
    QMessageBox


from database import admin_bd
from interface.qAdminWindow import AdminWindow
from interface.qAppWindows.qAppWindow import QAppWindow
from interface.qResearcherWindow import ResearcherWindow


class LoginWindow(QAppWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")

        layout = self._get_layout()
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        self.resize(300, 150)

    def _get_layout(self) -> QLayout:
        layout = QGridLayout()
        title = QLabel("Окно авторизации")
        layout.addWidget(title, 0, 1, 1, 2, Qt.AlignmentFlag.AlignCenter)

        label_login = QLabel("Логин")
        layout.addWidget(label_login, 1, 0)

        self.input_login = QLineEdit("")
        self.input_login.setPlaceholderText('Введите непустой логин')
        self.input_login.textChanged.connect(self._input_text_changed)
        layout.addWidget(self.input_login, 1, 1, 1, 3)

        label_password = QLabel("Пароль")
        layout.addWidget(label_password, 2, 0)

        self.input_password = QLineEdit("")
        self.input_password.setPlaceholderText('Введите пароль')
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password, 2, 1, 1, 3)

        self.ok_button = QPushButton("OK")
        self.ok_button.setEnabled(False)
        self.ok_button.clicked.connect(self._ok_clicked)
        layout.addWidget(self.ok_button, 3, 1, 1, 2)

        return layout

    def _input_text_changed(self, string) -> None:
        self.ok_button.setEnabled(bool(string))

    def _ok_clicked(self) -> None:
        login = self.input_login.text()
        password = self.input_password.text()
        database_worker = admin_bd.UserDataBaseWorker()
        id_user_type = database_worker.check_user(login, password)

        if not id_user_type:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")
            return

        id_user_type = id_user_type[0][0]

        match id_user_type:
            case 1:
                self.main_window = ResearcherWindow()
                self.main_window.show()
                self.close()
            case 2:
                self.main_window = AdminWindow()
                self.main_window.show()
                self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
