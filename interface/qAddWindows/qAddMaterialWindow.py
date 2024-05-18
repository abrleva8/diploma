from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox, QPushButton, \
    QMessageBox, QSpinBox, QDoubleSpinBox

from database import material_bd


class AddMaterialWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить материал")

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.properties = None

        self.layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

    def _get_layout(self):
        layout = QGridLayout()

        self.material_lbl = QLabel("Введите название")

        self.material_input = QLineEdit("")
        self.material_input.setPlaceholderText('Название материала')
        self.material_input.textChanged.connect(self.__input_add_new_material_changed)

        self.material_type_lbl = QLabel("Введите тип")

        self.material_type_input = QLineEdit("")
        self.material_type_input.setPlaceholderText('Тип материала')
        self.material_type_input.textChanged.connect(self.__input_add_new_material_changed)

        self.apply_button = QPushButton()
        self.apply_button.setText("Добавить материал")
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.__add_button_clicked)

        layout.addWidget(self.material_lbl, 0, 0)
        layout.addWidget(self.material_input, 0, 1)
        layout.addWidget(self.material_type_lbl, 1, 0)
        layout.addWidget(self.material_type_input, 1, 1)

        self.set_labels(layout)

        layout.addWidget(self.apply_button)

        return layout

    def __input_add_new_material_changed(self):
        self.apply_button.setEnabled(bool(self.material_input.text()))

    def __add_button_clicked(self):
        # math_operator_worker = material_bd.MaterialDataBaseWorker()
        # try:
        #     math_operator_worker.insert_material(self.material_input.text())
        # except IntegrityError as e:
        #     QMessageBox.critical(self, "Ошибка", "Материал с таким названием уже существует")
        #     return
        # QMessageBox.information(self, "Успех", "Материал успешно добавлен")
        print(self.layout)

    def set_labels(self, layout: QGridLayout):
        if self.properties is None:
            self.properties = self.math_operator_worker.get_properties()
            self.properties = list(map(lambda x: x[0], self.properties))

        for index, proper in enumerate(self.properties):
            q_label = QLabel(proper)
            q_label.setObjectName(proper)
            layout.addWidget(q_label, index + 2, 0)
            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{proper}_spinbox')
            layout.addWidget(spin_box, index + 2, 1)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddMaterialWindow()
    window.show()
    sys.exit(app.exec())
