from PyQt6.QtWidgets import QApplication, QMainWindow


class MathOperatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Специалист по математическому обеспечению")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MathOperatorWindow()
    window.show()
    sys.exit(app.exec())
