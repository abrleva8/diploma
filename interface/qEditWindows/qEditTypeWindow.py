from sqlite3 import IntegrityError

from PyQt6.QtWidgets import (QWidget, QMainWindow, QGridLayout, QLabel, QApplication, QLineEdit, QPushButton,
                             QMessageBox)

from database import material_bd
from interface.qAppWindows.qAppWindow import QAppWindow


class EditTypeWindow(QAppWindow):
    def __init__(self, type_name: str):
        super().__init__()
        self.setWindowTitle("Изменить тип материала")

        self.type_name = type_name
        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def __get_layout(self):
        layout = QGridLayout()

        self.curr_type_lbl = QLabel("Текущее название:")

        self.current_type_lbl = QLabel(self.type_name)

        self.new_type_lbl = QLabel("Новое название:")

        self.new_type_input = QLineEdit()
        self.new_type_input.textChanged.connect(self.__new_type_changed)

        self.edit_button = QPushButton(self)
        self.edit_button.setText("Изменить тип материала")
        self.edit_button.setEnabled(False)
        self.edit_button.clicked.connect(self.__edit_btn_clicked)

        layout.addWidget(self.curr_type_lbl, 0, 0)
        layout.addWidget(self.current_type_lbl, 0, 1)
        layout.addWidget(self.new_type_lbl, 1, 0)
        layout.addWidget(self.new_type_input, 1, 1)
        layout.addWidget(self.edit_button, 2, 0, 2, 0)

        return layout

    def __new_type_changed(self):
        self.edit_button.setEnabled(bool(self.new_type_input.text()))

    def __edit_btn_clicked(self):
        math_operator_worker = material_bd.MaterialDataBaseWorker()
        try:
            math_operator_worker.edit_type(self.type_name, self.new_type_input.text())
        except IntegrityError as e:
            QMessageBox.critical(self, "Ошибка", "Тип материала с таким названием уже существует")
            return
        QMessageBox.information(self, "Успех", "Тип материала успешно изменен")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EditTypeWindow('test')
    window.show()
    sys.exit(app.exec())
