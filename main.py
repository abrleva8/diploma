import sys

from PyQt6.QtWidgets import QApplication

from interface.qLoginWindow import LoginWindow


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = LoginWindow()
    window.show()

    app.exec()
