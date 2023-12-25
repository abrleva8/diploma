from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QComboBox, QLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox

from database import admin_bd
from interface import qAddUserWindow


class UserWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = self.__get_user_layout()
        self.setLayout(self.layout)

        self.math_operator_worker = admin_bd.UserDataBaseWorker()
        self._init_users_combo_box()

    def _init_users_combo_box(self):
        list_of_logins = self.math_operator_worker.get_logins()
        list_of_logins = list(map(lambda x: x[0], list_of_logins))
        self.users_combo_box.clear()
        self.users_combo_box.addItems(list_of_logins)

    def __get_user_layout(self) -> QLayout:
        layout = QGridLayout()

        self.users_combo_box = QComboBox(self)
        self.user_cb_model = QStringListModel()
        self.users_combo_box.setModel(self.user_cb_model)
        self.users_combo_box.currentTextChanged.connect(self._users_combo_box_changed)
        layout.addWidget(self.users_combo_box, 0, 0)

        self.delete_button = QPushButton(self)
        self.delete_button.setText("Удалить пользователя")
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_button_clicked)
        layout.addWidget(self.delete_button, 0, 1)

        self.input_add_new_user = QLineEdit("")
        self.input_add_new_user.setPlaceholderText('Введите новый логин')
        self.input_add_new_user.textChanged.connect(self._input_add_new_user_changed)
        layout.addWidget(self.input_add_new_user, 1, 0)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить логин")
        self.add_button.setEnabled(False)
        layout.addWidget(self.add_button, 1, 1)
        self.add_button.clicked.connect(self._add_button_clicked)

        return layout

    def _users_combo_box_changed(self):
        text = self.users_combo_box.currentText()
        enabled = text not in ['admin', 'user'] and bool(text)
        self.delete_button.setEnabled(enabled)

    def _delete_button_clicked(self):
        self.math_operator_worker.delete_user(self.users_combo_box.currentText())
        QMessageBox.information(self, "Успех", "Пользователь был удален")
        self._init_users_combo_box()

    def _input_add_new_user_changed(self):
        self.add_button.setEnabled(bool(self.input_add_new_user.text()))

    def _add_button_clicked(self):
        self.admin = qAddUserWindow.AddWindow()
        self.admin.show()
