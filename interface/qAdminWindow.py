import interface

from interface.qMainAppWindow import QMainAppWindow


class AdminWindow(QMainAppWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Администратор")
        self.setFixedSize(800, 400)

        self.tab_widget = interface.qAdminTabWidget.AdminWidgets(self)
        self.setCentralWidget(self.tab_widget)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AdminWindow()
    window.show()
    sys.exit(app.exec())
