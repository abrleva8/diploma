from sqlite3 import IntegrityError

from PyQt6.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QComboBox,
                             QPushButton, QMessageBox)

from database import material_bd


class EditUnitWindow(QMainWindow):
    def __init__(self, unit_denote: str):
        super().__init__()
        self.setWindowTitle("Изменить единицу измерения")

        self.unit_denote = unit_denote
        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def __get_layout(self):
        layout = QGridLayout()

        self.curr_denote_label = QLabel("Текущее обозначение:")

        self.current_unit_label = QLabel(self.unit_denote)

        self.new_denote_label = QLabel("Новое обозначение:")

        self.new_unit_input = QLineEdit()
        self.new_unit_input.textChanged.connect(self.__new_unit_changed)

        self.edit_button = QPushButton(self)
        self.edit_button.setText("Изменить единицу измерения")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.__edit_button_clicked)

        layout.addWidget(self.curr_denote_label, 0, 0)
        layout.addWidget(self.current_unit_label, 0, 1)
        layout.addWidget(self.new_denote_label, 1, 0)
        layout.addWidget(self.new_unit_input, 1, 1)
        layout.addWidget(self.edit_button, 2, 0, 2, 0)

        return layout

    def __new_unit_changed(self):
        self.edit_button.setEnabled(bool(self.new_unit_input.text()))

    def __edit_button_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        try:
            math_operator_worker.edit_unit(self.unit_denote, self.new_unit_input.text())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Единица измерения с таким обозначением уже существует")
            return
        QMessageBox.information(self, "Успех", "Единица измерения успешно изменена")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EditUnitWindow('test')
    window.show()
    sys.exit(app.exec())
