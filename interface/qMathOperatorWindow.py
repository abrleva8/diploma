from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
from interface.MathOperatorTabWidget import MathOperatorWidgets


class MathOperatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Специалист по математическому обеспечению")
        self.setFixedSize(500, 300)

        self.tab_widget = MathOperatorWidgets(self)
        self.setCentralWidget(self.tab_widget)

        self._center()

    def _center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MathOperatorWindow()
    window.show()
    sys.exit(app.exec())
