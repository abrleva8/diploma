from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog


class MathOperatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Специалист по математическому обеспечению")

    def open_file_dialog(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, filter="Video files (*.mp4 *.avi)")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MathOperatorWindow()
    window.show()
    sys.exit(app.exec())
