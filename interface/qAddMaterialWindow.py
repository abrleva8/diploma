from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox, QPushButton, \
    QMessageBox

from database import material_bd


class AddMaterialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить материал")

        layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self._center()

    def _get_layout(self):
        layout = QGridLayout()

        self.material_label = QLabel("Введите материал")
        layout.addWidget(self.material_label, 0, 0)

        self.material_input = QLineEdit("")
        self.material_input.setPlaceholderText('Введите новый материал')
        self.material_input.textChanged.connect(self.__input_add_new_material_changed)
        layout.addWidget(self.material_input, 0, 1)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить материал")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.__add_button_clicked)
        layout.addWidget(self.add_button, 1, 0, 2, 0)

        return layout

    def _center(self):
        pass

    def __input_add_new_material_changed(self):
        self.add_button.setEnabled(bool(self.material_input.text()))

    def __add_button_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        try:
            math_operator_worker.insert_material(self.material_input.text())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Материал с таким названием уже существует")
            return
        QMessageBox.information(self, "Успех", "Материал успешно добавлен")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddMaterialWindow()
    window.show()
    sys.exit(app.exec())
