from PyQt6 import QtGui
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMenu

import interface
import resources


class QMainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))

        self.__create_actions()
        self.__create_menu_bar()
        self.__connect_actions()

        self.__center()

    def __center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = QMenu("Файл", self)
        menu_bar.addMenu(file_menu)
        file_menu.addAction(self.change_user_action)
        file_menu.addAction(self.exit_action)

    def __create_actions(self):
        self.change_user_action = QAction("Сменить пользователя", self)
        self.exit_action = QAction("Выход", self)

    def __connect_actions(self):
        self.change_user_action.triggered.connect(self.__change_user)
        self.exit_action.triggered.connect(self.close)

    def __change_user(self):
        self.close()
        self.window = interface.qLoginWindow.LoginWindow()
        self.window.show()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = QMainAppWindow()
    window.show()
    sys.exit(app.exec())
