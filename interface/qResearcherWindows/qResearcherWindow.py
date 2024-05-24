from interface.qAppWindows.qMainAppWindow import QMainAppWindow
from interface.qResearcherWindows.qResearcherTabWidget import ResearcherTabWidget


class ResearcherWindow(QMainAppWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Исследователь")

        self.tab_widget = ResearcherTabWidget(self)
        self.setCentralWidget(self.tab_widget)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ResearcherWindow()
    window.show()
    sys.exit(app.exec())
