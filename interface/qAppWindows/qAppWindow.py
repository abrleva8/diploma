from PyQt6 import QtGui
from PyQt6.QtWidgets import QMainWindow

import resources


class QAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(':/logo.ico'))


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = QAppWindow()
    window.show()
    sys.exit(app.exec())
