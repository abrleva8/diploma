from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox, QPushButton, \
    QMessageBox, QSpinBox, QDoubleSpinBox

from database import material_bd


class EditMaterialWindow(QMainWindow):
    def __init__(self, curr_material_name: str):
        super().__init__()
        self.setWindowTitle(f"Изменение {curr_material_name}")

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.properties = None
        self.__curr_material_name = curr_material_name

        self.layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.__init_material_types_cmbox()
        self.__init_values()

    def _get_layout(self):
        layout = QGridLayout()

        self.material_lbl = QLabel("Введите новое название")

        self.material_input = QLineEdit("")
        self.material_input.setPlaceholderText('Новое название')
        self.material_input.textChanged.connect(self.__input_add_new_material_changed)

        self.material_type_lbl = QLabel("Выберите новый тип")

        self.material_type_cmbox = QComboBox()

        self.apply_button = QPushButton('Изменить материал')
        self.apply_button.setEnabled(False)

        self.apply_button.clicked.connect(self.__edit_button_clicked)

        layout.addWidget(self.material_lbl, 0, 0)
        layout.addWidget(self.material_input, 0, 1)
        layout.addWidget(self.material_type_lbl, 1, 0)
        layout.addWidget(self.material_type_cmbox, 1, 1)

        self.set_labels(layout)

        layout.addWidget(self.apply_button)

        return layout

    def __input_add_new_material_changed(self):
        self.apply_button.setEnabled(bool(self.material_input.text()))

    def __edit_button_clicked(self):
        try:
            self.math_operator_worker.edit_material(self.__curr_material_name, self.material_input.text(),
                                                    self.material_type_cmbox.currentText())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при изменении материала")
            return
        try:
            for proper in self.properties:
                proper_name = self.layout.parentWidget().findChild(QLabel, proper).text()
                proper_value = self.layout.parentWidget().findChild(QDoubleSpinBox, f'{proper}_spinbox').value()
                self.math_operator_worker.edit_raw_material_property(self.material_input.text(),
                                                                     proper_name, proper_value)
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при изменении значений свойств")
            return

        QMessageBox.information(self, "Успех", "Материал успешно изменен")

    def set_labels(self, layout: QGridLayout):
        if self.properties is None:
            self.properties = self.math_operator_worker.get_properties()
            self.properties = list(map(lambda x: x[0], self.properties))

        for index, proper in enumerate(self.properties):
            q_label = QLabel(proper)
            q_label.setObjectName(proper)

            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{proper}_spinbox')

            layout.addWidget(q_label, index + 2, 0)
            layout.addWidget(spin_box, index + 2, 1)

    def __init_values(self):
        type_name = self.math_operator_worker.get_type_id_by_material_name(self.__curr_material_name)[0][0]
        self.material_type_cmbox.setCurrentText(type_name)

        name_value_lst = self.math_operator_worker.get_name_and_value_by_material_name(self.__curr_material_name)
        self.set_properties(name_value_lst)

    def set_properties(self, name_value_lst: list[tuple[str, float]]):
        for index, (name, value) in enumerate(name_value_lst):
            self.layout.parentWidget().findChild(QLabel, name).setText(name)
            self.layout.parentWidget().findChild(QDoubleSpinBox, f'{name}_spinbox').setValue(value)

    def __init_material_types_cmbox(self):
        material_types = self.math_operator_worker.get_material_types()
        material_types = list(map(lambda x: x[0], material_types))
        self.material_type_cmbox.clear()
        self.material_type_cmbox.addItems(material_types)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EditMaterialWindow('Тест')
    window.show()
    sys.exit(app.exec())
