from PyQt6.QtWidgets import QApplication, QMainWindow


class ResearcherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Исследователь")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ResearcherWindow()
    window.show()
    sys.exit(app.exec())
