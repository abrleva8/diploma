from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox, QPushButton, \
    QMessageBox, QSpinBox, QDoubleSpinBox

from database import material_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class AddMaterialWindow(QAppWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить материал")

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.properties = None

        self.layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.__init_material_types_cmbox()

    def _get_layout(self):
        layout = QGridLayout()

        self.material_lbl = QLabel("Введите название")

        self.material_input = QLineEdit("")
        self.material_input.setPlaceholderText('Название материала')
        self.material_input.textChanged.connect(self.__input_add_new_material_changed)

        self.material_type_lbl = QLabel("Выберите тип")

        self.material_type_cmbox = QComboBox()

        self.apply_button = QPushButton()
        self.apply_button.setText("Добавить материал")
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.__add_button_clicked)

        layout.addWidget(self.material_lbl, 0, 0)
        layout.addWidget(self.material_input, 0, 1)
        layout.addWidget(self.material_type_lbl, 1, 0)
        layout.addWidget(self.material_type_cmbox, 1, 1)

        self.set_labels(layout)

        layout.addWidget(self.apply_button)

        return layout

    def __input_add_new_material_changed(self):
        self.apply_button.setEnabled(bool(self.material_input.text()))

    def __add_button_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()

        try:
            type_id = math_operator_worker.get_type_id_by_type_name(self.material_type_cmbox.currentText())[0][0]
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при получении id типа материала")
            return

        try:
            math_operator_worker.insert_material(self.material_input.text(), type_id)
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при добавлении материала")
            return

        material_id = math_operator_worker.get_id_material_by_material_name(self.material_input.text())[0][0]

        try:
            for proper in self.properties:
                proper_name = self.layout.parentWidget().findChild(QLabel, proper).text()
                proper_id = self.math_operator_worker.get_id_property_by_property_name(proper_name)[0][0]
                proper_value = self.layout.parentWidget().findChild(QDoubleSpinBox, f'{proper}_spinbox').value()
                self.math_operator_worker.insert_raw_material_property(material_id, proper_id, proper_value)
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при добавлении значений свойств")
            return

        QMessageBox.information(self, "Успех", "Материал успешно добавлен")

    def set_labels(self, layout: QGridLayout):
        if self.properties is None:
            self.properties, _ = self.math_operator_worker.get_properties(unit=True)

        for index, proper in enumerate(self.properties):
            q_label = QLabel(proper[0])
            q_label.setObjectName(proper[0])

            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{proper[0]}_spinbox')
            layout.addWidget(spin_box, index + 2, 1)

            unit_label = QLabel(proper[1])

            layout.addWidget(q_label, index + 2, 0)
            layout.addWidget(spin_box, index + 2, 1)
            layout.addWidget(unit_label, index + 2, 2)

    def __init_material_types_cmbox(self):
        material_types = self.math_operator_worker.get_material_types()
        material_types = list(map(lambda x: x[0], material_types))
        self.material_type_cmbox.clear()
        self.material_type_cmbox.addItems(material_types)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AddMaterialWindow()
    window.show()
    sys.exit(app.exec())
