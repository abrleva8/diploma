from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import QWidget, QComboBox, QLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox

from database import admin_bd
from interface.qAddWindows.qAddUserWindow import AddUserWindow
from interface.qEditWindows.qEditUserWindow import EditUserWindow


class UserWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = self.__get_user_layout()
        self.setLayout(self.layout)

        self.math_operator_worker = admin_bd.UserDataBaseWorker()
        self.init_users_combo_box()

    def init_users_combo_box(self):
        list_of_logins = self.math_operator_worker.get_logins()
        list_of_logins = list(map(lambda x: x[0], list_of_logins))
        self.users_cmbox.clear()
        self.users_cmbox.addItems(list_of_logins)

    def __get_user_layout(self) -> QLayout:
        layout = QGridLayout()

        self.users_cmbox = QComboBox(self)
        self.user_cb_model = QStringListModel()
        self.users_cmbox.setModel(self.user_cb_model)
        self.users_cmbox.currentTextChanged.connect(self.__users_combo_box_changed)

        self.add_btn = QPushButton(self)
        self.add_btn.setText("Добавить пользователя")
        self.add_btn.clicked.connect(self._add_button_clicked)

        self.edit_btn = QPushButton(self)
        self.edit_btn.setText("Изменить данные")
        self.edit_btn.clicked.connect(self.__edit_button_clicked)

        self.delete_btn = QPushButton(self)
        self.delete_btn.setText("Удалить пользователя")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.__delete_button_clicked)

        layout.addWidget(self.users_cmbox, 0, 0)
        layout.addWidget(self.add_btn, 0, 1)
        layout.addWidget(self.edit_btn, 0, 2)
        layout.addWidget(self.delete_btn, 0, 3)

        return layout

    def __users_combo_box_changed(self):
        text = self.users_cmbox.currentText()
        enabled = text not in ['admin', 'user'] and bool(text)
        self.delete_btn.setEnabled(enabled)
        self.edit_btn.setEnabled(enabled)

    def __delete_button_clicked(self):
        self.math_operator_worker.delete_user(self.users_cmbox.currentText())
        QMessageBox.information(self, "Успех", "Пользователь был удален")
        self.init_users_combo_box()

    def _add_button_clicked(self):
        self.admin = AddUserWindow()
        self.admin.show()

    def __edit_button_clicked(self):
        self.edit_window = EditUserWindow(self.users_cmbox.currentText())
        self.edit_window.show()
