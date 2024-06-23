from PyQt6.QtWidgets import QLayout, QGridLayout, QWidget, QLabel, QComboBox, QDoubleSpinBox, QPushButton, QMessageBox
from typing import List

from database.material_bd import MaterialDataBaseWorker
from interface.qAppWindows.qAppWindow import QAppWindow


class EditResearchWindow(QAppWindow):

    def __init__(self, labels: dict[str, str], research_number: int):
        super().__init__()

        self.__research_number = research_number
        self.__labels = labels

        self.setWindowTitle("Изменение эксперимента")

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
        self.apply_button.setText("Изменить эксперимент")
        # self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.__edit_button_clicked)

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
        self.raw_material_cmbox.setCurrentText(self.__labels.get('материал', None))

    def __set_conditions(self, layout: QGridLayout) -> int | None:
        if self.__conditions is None:
            self.__conditions = self.math_operator_worker.get_conditions(unit=True)

        index = -1

        for index, condition in enumerate(self.__conditions):
            condition_lbl = QLabel(condition[0])
            condition_lbl.setObjectName(condition[0])

            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{condition[0]}_spinbox')

            value = self.__labels.get(condition[0], None)
            if value is not None:
                spin_box.setValue(float(value))

            unit_lbl = QLabel(condition[1])

            layout.addWidget(condition_lbl, index + 2, 0)
            layout.addWidget(spin_box, index + 2, 1)
            layout.addWidget(unit_lbl, index + 2, 2)

        return index

    def __set_results(self, layout: QGridLayout, start_index: int):
        if self.__results is None:
            self.__results = self.math_operator_worker.get_results(unit=True)

        for index, result in enumerate(self.__results):
            result_lbl = QLabel(result[0])
            result_lbl.setObjectName(result[0])

            spin_box = QDoubleSpinBox()
            spin_box.setObjectName(f'{result[0]}_spinbox')

            value = self.__labels.get(result[0], None)
            if value is not None:
                spin_box.setValue(float(value))

            unit_lbl = QLabel(result[1])

            layout.addWidget(result_lbl, index + start_index, 0)
            layout.addWidget(spin_box, index + start_index, 1)
            layout.addWidget(unit_lbl, index + start_index, 2)

    def __edit_button_clicked(self):
        id_material = \
            self.math_operator_worker.get_id_material_by_material_name(self.__labels.get('материал', None))[0][0]

        condition_id_lst, old_values_lst, new_values_lst = [], [], []

        for condition in self.__conditions:
            condition_name = self.layout.parentWidget().findChild(QLabel, condition[0]).text()
            new_condition_value = self.layout.parentWidget().findChild(QDoubleSpinBox,
                                                                       f'{condition[0]}_spinbox').value()
            old_condition_value = self.__labels.get(condition[0], None)

            if old_condition_value is not None:
                old_condition_value = float(old_condition_value)

            condition_id = self.math_operator_worker.get_id_condition_by_condition_name(condition_name)[0][0]

            condition_id_lst.append(condition_id)
            new_values_lst.append(new_condition_value)
            old_values_lst.append(old_condition_value)

        old_index_lst = self.math_operator_worker.get_condition_set(condition_id_lst=condition_id_lst,
                                                                    values_lst=old_values_lst)

        new_index_lst = self.math_operator_worker.get_condition_set(condition_id_lst=condition_id_lst,
                                                                    values_lst=new_values_lst)

        old_id_condition_set = old_index_lst[0][0]
        new_id_condition_set = new_index_lst[0][0]

        id_research = int(self.__labels['номер_опыта'])

        result_id_lst: list[int] = []
        new_result_value_lst: list[float] = []

        for result in self.__results:
            result_name = self.layout.parentWidget().findChild(QLabel, result[0]).text()
            new_result_value = self.layout.parentWidget().findChild(QDoubleSpinBox, f'{result[0]}_spinbox').value()

            if new_result_value is not None:
                new_result_value = float(new_result_value)
            new_result_value_lst.append(new_result_value)

            result_id = self.math_operator_worker.get_result_id_by_result_name(result_name)[0][0]
            result_id_lst.append(result_id)

        id_values_dict = dict(zip(result_id_lst, new_result_value_lst))

        self.math_operator_worker.edit_research(id_values_dict=id_values_dict, new_condition_set=new_id_condition_set,
                                                id_raw_material=id_material, old_id_condition_set=old_id_condition_set,
                                                id_research=id_research)
        QMessageBox.information(self, 'Изменение', 'Данные эксперимента изменены')
        self.close()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = EditResearchWindow()
    window.show()
    sys.exit(app.exec())
