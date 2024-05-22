from sqlite3 import IntegrityError

from PyQt6.QtWidgets import QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, \
    QMessageBox

from database import material_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class AddConditionWindow(QAppWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление условия")

        layout = self._get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self._center()

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self._init_unit_combobox()

    def _get_layout(self):
        layout = QGridLayout()

        self.property_label = QLabel("Введите условие")
        layout.addWidget(self.property_label, 0, 0)

        self.condition_input = QLineEdit("")
        self.condition_input.setPlaceholderText('Введите новое условие')
        self.condition_input.textChanged.connect(self.__input_add_new_condition_changed)
        layout.addWidget(self.condition_input, 0, 1)

        self.unit_label = QLabel("Выберите единицу измерения")
        layout.addWidget(self.unit_label, 1, 0)

        self.unit_combobox = QComboBox(self)
        layout.addWidget(self.unit_combobox, 1, 1)

        self.add_button = QPushButton(self)
        self.add_button.setText("Добавить условие")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._add_button_clicked)
        layout.addWidget(self.add_button, 2, 0, 2, 0)

        return layout

    def _center(self):
        pass

    def __input_add_new_condition_changed(self):
        self.add_button.setEnabled(bool(self.condition_input.text() and self.unit_combobox.currentText()))

    def _add_button_clicked(self):
        try:
            self.math_operator_worker.insert_condition(self.condition_input.text(), self.unit_combobox.currentText())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Условие с таким названием уже существует")
            return
        QMessageBox.information(self, "Успех", "Условие успешно добавлено")

    def _init_unit_combobox(self):
        units = self.math_operator_worker.get_units()
        units = list(map(lambda x: x[0], units))
        self.unit_combobox.clear()
        self.unit_combobox.addItems(units)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AddConditionWindow()
    window.show()
    sys.exit(app.exec())
