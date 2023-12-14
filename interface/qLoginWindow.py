from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLayout, QLabel, QWidget, QLineEdit, QPushButton


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")

        layout = self._get_layout()
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def _get_layout(self) -> QLayout:
        layout = QGridLayout()
        title = QLabel("Окно регистрации")
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
        pass
