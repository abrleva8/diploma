from sqlite3 import IntegrityError

from PyQt6.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)

from database import material_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class AddUnitWindow(QAppWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить единицу измерения")

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def __get_layout(self):
        layout = QGridLayout()

        self.unit_label = QLabel("Введите единицу измерения")

        self.unit_input = QLineEdit("")
        self.unit_input.setPlaceholderText('Введите обозначение')
        self.unit_input.textChanged.connect(self.__input_add_new_unit_changed)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить единицу измерения")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.__add_button_clicked)

        layout.addWidget(self.unit_label, 0, 0)
        layout.addWidget(self.unit_input, 0, 1)
        layout.addWidget(self.add_button, 1, 0, 2, 0)

        return layout

    def __input_add_new_unit_changed(self):
        self.add_button.setEnabled(bool(self.unit_input.text()))

    def __add_button_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        try:
            math_operator_worker.insert_unit(self.unit_input.text())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Единица измерения с таким обозначением уже существует")
            return
        QMessageBox.information(self, "Успех", "Единица измерения успешно добавлена")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddUnitWindow()
    window.show()
    sys.exit(app.exec())
