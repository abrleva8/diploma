from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow

from interface.qResearcherTabWidget import ResearcherTabWidget


class ResearcherWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Исследователь")

        self.tab_widget = ResearcherTabWidget(self)
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
    window = ResearcherWindow()
    window.show()
    sys.exit(app.exec())
