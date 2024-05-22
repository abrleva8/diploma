import sys

from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication

from interface.qLoginWindow import LoginWindow
import ctypes


if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('company.app.1')
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/logo.ico'))
    app.setStyle('Fusion')

    window = LoginWindow()
    window.show()

    app.exec()
