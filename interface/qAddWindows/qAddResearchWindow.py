from PyQt6.QtWidgets import QLayout, QGridLayout, QWidget, QLabel, QComboBox, QDoubleSpinBox, QPushButton, QMessageBox

from database.material_bd import MaterialDataBaseWorker
from interface.qAppWindows.qAppWindow import QAppWindow


class AddResearchWindow(QAppWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление эксперимента")

        self.__conditions = None
        self.__results = None
        self.math_operator_worker = MaterialDataBaseWorker()

        self.layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.__init_raw_material_cmbox()

    def __get_layout(self) -> QLayout:
        layout = QGridLayout()

        raw_material_lbl = QLabel('Сырье')
        self.raw_material_cmbox = QComboBox()
        condition_title_lbl = QLabel('Условия эксперимента')
        result_title_lbl = QLabel('Результаты эксперимента')

        self.apply_button = QPushButton()
        self.apply_button.setText("Добавить эксперимент")
        # self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.__add_button_clicked)

        layout.addWidget(raw_material_lbl, 0, 0)
        layout.addWidget(self.raw_material_cmbox, 0, 1)
        layout.addWidget(condition_title_lbl, 1, 0, 1, 2)

        index = self.__set_conditions(layout)

        layout.addWidget(result_title_lbl, index + 3, 0, 1, 2)

        self.__set_results(layout, index + 4)

        layout.addWidget(self.apply_button)

        return layout

    def __init_raw_material_cmbox(self) -> None:
        raw_materials = self.math_operator_worker.get_materials()
        raw_materials = list(map(lambda x: x[0], raw_materials))
        self.raw_material_cmbox.clear()
        self.raw_material_cmbox.addItems(raw_materials)

    def __set_conditions(self, layout: QGridLayout) -> int | None:
        if self.__conditions is None:
            self.__conditions = self.math_operator_worker.get_conditions(unit=True)

        index = -1

        for index, condition in enumerate(self.__conditions):
            condition_lbl = QLabel(condition[0])
            condition_lbl.setObjectName(condition[0])

            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{condition[0]}_spinbox')

            unit_lbl = QLabel(condition[1])

            layout.addWidget(condition_lbl, index + 2, 0)
            layout.addWidget(spin_box, index + 2, 1)
            layout.addWidget(unit_lbl, index + 2, 2)

        return index

    def __set_results(self, layout: QGridLayout, start_index: int):
        if self.__results is None:
            self.__results = self.math_operator_worker.get_results(unit=True)

        index = -1

        for index, result in enumerate(self.__results):
            result_lbl = QLabel(result[0])
            result_lbl.setObjectName(result[0])

            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{result[0]}_spinbox')

            unit_lbl = QLabel(result[1])

            layout.addWidget(result_lbl, index + start_index, 0)
            layout.addWidget(spin_box, index + start_index, 1)
            layout.addWidget(unit_lbl, index + start_index, 2)

    def __add_button_clicked(self):
        id_material = \
        self.math_operator_worker.get_id_material_by_material_name(self.raw_material_cmbox.currentText())[0][0]
        print(f'{id_material=}')

        condition_id_lst, values_lst = [], []

        for condition in self.__conditions:
            condition_name = self.layout.parentWidget().findChild(QLabel, condition[0]).text()
            condition_value = self.layout.parentWidget().findChild(QDoubleSpinBox, f'{condition[0]}_spinbox').value()

            condition_id = self.math_operator_worker.get_id_condition_by_condition_name(condition_name)[0][0]

            condition_id_lst.append(condition_id)
            values_lst.append(condition_value)

        index_lst = self.math_operator_worker.get_condition_set(condition_id_lst=condition_id_lst,
                                                                values_lst=values_lst)

        if len(index_lst) > 0:
            print('Есть совпадения')
        else:
            print('Нет совпадений')
            self.math_operator_worker.insert_condition_set(condition_id_lst, values_lst)
            index_lst = self.math_operator_worker.get_condition_set(condition_id_lst=condition_id_lst,
                                                                    values_lst=values_lst)

        id_condition_set = index_lst[0][0]
        print(f'{id_condition_set=}')

        id_research = self.math_operator_worker.get_current_id_research()[0][0] + 1

        for result in self.__results:
            result_name = self.layout.parentWidget().findChild(QLabel, result[0]).text()
            result_value = self.layout.parentWidget().findChild(QDoubleSpinBox, f'{result[0]}_spinbox').value()

            result_id = self.math_operator_worker.get_result_id_by_result_name(result_name)[0][0]

            print(f'{result_name=}, {result_value=}')

            self.math_operator_worker.insert_research(result_id, id_material,
                                                      id_condition_set, id_research, result_value)

            QMessageBox.information(self, "Успех", "Эксперимент добавлен")


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AddResearchWindow()
    window.show()
    sys.exit(app.exec())
