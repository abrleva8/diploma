from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu

import interface


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Администратор")
        self.setFixedSize(800, 400)

        self._create_actions()
        self._create_menu_bar()
        self._connect_actions()

        self.tab_widget = interface.qAdminTabWidget.AdminWidgets(self)
        self.setCentralWidget(self.tab_widget)

        self.__center()

    def __center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = QMenu("Файл", self)
        menu_bar.addMenu(file_menu)
        file_menu.addAction(self.change_user_action)
        file_menu.addAction(self.exit_action)

    def _create_actions(self):
        self.change_user_action = QAction("Сменить пользователя", self)
        self.exit_action = QAction("Выход", self)

    def _connect_actions(self):
        self.change_user_action.triggered.connect(self.__change_user)
        self.exit_action.triggered.connect(self.close)

    def __change_user(self):
        self.close()
        self.window = interface.qLoginWindow.LoginWindow()
        self.window.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
