from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox, QPushButton, \
    QMessageBox

from database import admin_bd, material_bd


class AddMaterialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить материал")

        layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self._center()

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self._init_unit_combobox()

    def _get_layout(self):
        layout = QGridLayout()

        self.material_label = QLabel("Введите материал")
        layout.addWidget(self.material_label, 0, 0)

        self.material_input = QLineEdit("")
        self.material_input.setPlaceholderText('Введите новый материал')
        self.material_input.textChanged.connect(self._input_add_new_material_changed)
        layout.addWidget(self.material_input, 0, 1)

        self.unit_label = QLabel("Выберите единицу измерения")
        layout.addWidget(self.unit_label, 1, 0)

        self.unit_combobox = QComboBox(self)
        # self.unit_input.setPlaceholderText('Введите единицу измерения')
        # self.unit_input.textChanged.connect(self._input_add_new_material_changed)
        layout.addWidget(self.unit_combobox, 1, 1)

        # self.user_type_label = QLabel("Выберите тип пользователя")
        # layout.addWidget(self.user_type_label, 2, 0)
        #
        # self.type_combobox = QComboBox(self)
        # layout.addWidget(self.type_combobox, 2, 1)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить материал")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._add_button_clicked)
        layout.addWidget(self.add_button, 2, 0, 2, 0)

        return layout

    def _center(self):
        pass

    def _input_add_new_material_changed(self):
        self.add_button.setEnabled(bool(self.material_input.text() and self.unit_combobox.currentText()))

    def _add_button_clicked(self):
        try:
            self.math_operator_worker.insert_material(self.material_input.text())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Материал с таким названием уже существует")
            return
        QMessageBox.information(self, "Успех", "Материал успешно добавлен")

    def _init_unit_combobox(self):
        units = self.math_operator_worker.get_units()
        units = list(map(lambda x: x[0], units))
        self.unit_combobox.clear()
        self.unit_combobox.addItems(units)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddMaterialWindow()
    window.show()
    sys.exit(app.exec())
