from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from interface.qAdminTabWidget import AdminWidgets


class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Администратор")
        self.setFixedSize(700, 300)

        self.tab_widget = AdminWidgets(self)
        self.setCentralWidget(self.tab_widget)

        self.__center()

    def __center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
