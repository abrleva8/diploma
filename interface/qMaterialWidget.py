from PyQt6 import QtCore
from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QMessageBox

from database import material_bd
from interface.qAddWindows import qAddResultWindow, qAddPropertyWindow, qAddMaterialWindow, qAddConditionWindow, \
    qAddUnitWindow, qAddTypeWindow
from interface.qEditWindows import qEditUnitWindow, qEditPropertyWindow, qEditResultWindow, qEditTypeWindow, \
    qEditMaterialWindow


class MaterialWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = self.__get_material_layout()
        self.setLayout(self.layout)

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.init_combox()

    def init_combox(self):
        self.__init_material_types_cmbox()
        self.__init_materials_combo_box()
        self.__init_properties_combo_box()
        self.__init_conditions_combo_box()
        self.__init_result_combo_box()
        self.__init_unit_combobox()

    def __get_material_layout(self):
        layout = QGridLayout()

        self.material_type_label = QLabel("Тип")

        self.material_type_cmbox = QComboBox(self)

        self.material_type_cb_model = QStringListModel()
        self.material_type_cmbox.setModel(self.material_type_cb_model)
        self.material_type_cmbox.currentTextChanged.connect(self.__material_type_cmbox_changed)

        self.add_type_btn = QPushButton(self)
        self.add_type_btn.setText("Добавить тип")
        self.add_type_btn.clicked.connect(self.__add_type_btn_clicked)

        self.edit_type_btn = QPushButton(self)
        self.edit_type_btn.setText("Изменить тип")
        self.edit_type_btn.setEnabled(True)
        self.edit_type_btn.clicked.connect(self.__edit_type_btn_clicked)

        self.delete_type_btn = QPushButton(self)
        self.delete_type_btn.setText("Удалить тип")
        self.delete_type_btn.setEnabled(True)
        self.delete_type_btn.clicked.connect(self.__delete_type_btn_clicked)

        self.material_label = QLabel("Материалы")

        self.material_combo_box = QComboBox(self)

        self.material_cb_model = QStringListModel()
        self.material_combo_box.setModel(self.material_cb_model)
        self.material_combo_box.currentTextChanged.connect(self.__material_combo_box_changed)

        self.add_material_button = QPushButton(self)
        self.add_material_button.setText("Добавить материал")
        self.add_material_button.clicked.connect(self.__add_material_button_clicked)

        self.edit_material_button = QPushButton(self)
        self.edit_material_button.setText("Изменить материал")
        self.edit_material_button.clicked.connect(self.__edit_material_button_clicked)

        self.delete_material_button = QPushButton(self)
        self.delete_material_button.setText("Удалить материал")
        self.delete_material_button.setEnabled(False)
        self.delete_material_button.clicked.connect(self.__delete_material_button_clicked)

        self.property_label = QLabel("Свойства")

        self.property_combo_box = QComboBox(self)
        self.property_cb_model = QStringListModel()
        self.property_combo_box.setModel(self.property_cb_model)
        self.property_combo_box.currentTextChanged.connect(self.__property_combo_box_changed)

        self.add_property_button = QPushButton(self)
        self.add_property_button.setText("Добавить свойство")
        self.add_property_button.clicked.connect(self.__add_property_button_clicked)

        self.edit_property_button = QPushButton(self)
        self.edit_property_button.setText("Изменить свойство")
        self.edit_property_button.setEnabled(False)
        self.edit_property_button.clicked.connect(self.__edit_property_button_clicked)

        self.delete_property_button = QPushButton(self)
        self.delete_property_button.setText("Удалить свойство")
        self.delete_property_button.setEnabled(False)
        self.delete_property_button.clicked.connect(self.__delete_property_button_clicked)

        self.unit_label = QLabel("Единицы измерения")

        self.unit_combo_box = QComboBox(self)
        self.unit_cb_model = QStringListModel()
        self.unit_combo_box.setModel(self.unit_cb_model)
        self.unit_combo_box.currentTextChanged.connect(self.__unit_combo_box_changed)

        self.add_unit_button = QPushButton(self)
        self.add_unit_button.setText("Добавить ед. измерения")
        self.add_unit_button.clicked.connect(self.__add_unit_button_clicked)

        self.edit_unit_button = QPushButton(self)
        self.edit_unit_button.setText("Изменить ед. измерения")
        self.edit_unit_button.setEnabled(False)
        self.edit_unit_button.clicked.connect(self.__edit_unit_button_clicked)

        self.delete_unit_button = QPushButton(self)
        self.delete_unit_button.setText("Удалить ед. измерения")
        self.delete_unit_button.setEnabled(False)
        self.delete_unit_button.clicked.connect(self.__delete_unit_button_clicked)

        self.condition_label = QLabel("Условия")

        self.condition_combo_box = QComboBox(self)
        self.condition_cb_model = QStringListModel()
        self.condition_combo_box.setModel(self.condition_cb_model)
        self.condition_combo_box.currentTextChanged.connect(self.__condition_combo_box_changed)

        self.add_condition_button = QPushButton(self)
        self.add_condition_button.setText("Добавить условие")
        self.add_condition_button.clicked.connect(self.__add_condition_button_clicked)

        self.edit_condition_button = QPushButton(self)
        self.edit_condition_button.setText("Изменить условие")
        self.edit_condition_button.setEnabled(False)
        self.edit_condition_button.clicked.connect(self.__edit_condition_button_clicked)

        self.delete_condition_button = QPushButton(self)
        self.delete_condition_button.setText("Удалить условие")
        self.delete_condition_button.setEnabled(False)
        self.delete_condition_button.clicked.connect(self.__delete_condition_button_clicked)

        self.result_label = QLabel("Результат")

        self.result_combo_box = QComboBox(self)
        self.result_cb_model = QStringListModel()
        self.result_combo_box.setModel(self.result_cb_model)
        self.result_combo_box.currentTextChanged.connect(self.__result_combo_box_changed)

        self.add_result_button = QPushButton(self)
        self.add_result_button.setText("Добавить результат")
        self.add_result_button.clicked.connect(self.__add_result_button_clicked)

        self.edit_result_button = QPushButton(self)
        self.edit_result_button.setText("Изменить результат")
        self.edit_result_button.setEnabled(False)
        self.edit_result_button.clicked.connect(self.__edit_result_button_clicked)

        self.delete_result_button = QPushButton(self)
        self.delete_result_button.setText("Удалить результат")
        self.delete_result_button.setEnabled(False)
        self.delete_result_button.clicked.connect(self.__delete_result_button_clicked)

        layout.addWidget(self.material_type_label, 0, 0, 1, 2)
        layout.addWidget(self.material_type_cmbox, 1, 0)
        layout.addWidget(self.add_type_btn, 1, 1)
        layout.addWidget(self.edit_type_btn, 1, 2)
        layout.addWidget(self.delete_type_btn, 1, 3)
        layout.addWidget(self.material_label, 2, 0, 1, 2)
        layout.addWidget(self.material_combo_box, 3, 0)
        layout.addWidget(self.add_material_button, 3, 1)
        layout.addWidget(self.edit_material_button, 3, 2)
        layout.addWidget(self.delete_material_button, 3, 3)
        layout.addWidget(self.property_label, 4, 0, 1, 2)
        layout.addWidget(self.property_combo_box, 5, 0)
        layout.addWidget(self.add_property_button, 5, 1)
        layout.addWidget(self.edit_property_button, 5, 2)
        layout.addWidget(self.delete_property_button, 5, 3)
        layout.addWidget(self.unit_label, 6, 0, 1, 2)
        layout.addWidget(self.unit_combo_box, 7, 0)
        layout.addWidget(self.add_unit_button, 7, 1)
        layout.addWidget(self.edit_unit_button, 7, 2)
        layout.addWidget(self.delete_unit_button, 7, 3)
        layout.addWidget(self.condition_label, 8, 0, 1, 2)
        layout.addWidget(self.condition_combo_box, 9, 0)
        layout.addWidget(self.add_condition_button, 9, 1)
        layout.addWidget(self.edit_condition_button, 9, 2)
        layout.addWidget(self.delete_condition_button, 9, 3)
        layout.addWidget(self.result_label, 10, 0, 1, 2)
        layout.addWidget(self.result_combo_box, 11, 0)
        layout.addWidget(self.add_result_button, 11, 1)
        layout.addWidget(self.edit_result_button, 11, 2)
        layout.addWidget(self.delete_result_button, 11, 3)

        return layout

    def __init_material_types_cmbox(self):
        material_types = self.math_operator_worker.get_material_types()
        material_types = list(map(lambda x: x[0], material_types))
        self.material_type_cmbox.clear()
        self.material_type_cmbox.addItems(material_types)

    def __init_materials_combo_box(self):
        materials = self.math_operator_worker.get_materials()
        materials = list(map(lambda x: x[0], materials))
        self.material_combo_box.clear()
        self.material_combo_box.addItems(materials)

    def __init_properties_combo_box(self):
        properties = self.math_operator_worker.get_properties()
        properties = list(map(lambda x: x[0], properties))
        self.property_combo_box.clear()
        self.property_combo_box.addItems(properties)

    def __init_conditions_combo_box(self):
        conditions = self.math_operator_worker.get_conditions()
        conditions = list(map(lambda x: x[0], conditions))
        self.condition_combo_box.clear()
        self.condition_combo_box.addItems(conditions)

    def __init_result_combo_box(self):
        results = self.math_operator_worker.get_results()
        results = list(map(lambda x: x[0], results))
        self.result_combo_box.clear()
        self.result_combo_box.addItems(results)

    def __init_unit_combobox(self):
        units = self.math_operator_worker.get_units()
        units = list(map(lambda x: x[0], units))
        self.unit_combo_box.clear()
        self.unit_combo_box.addItems(units)

    def __material_type_cmbox_changed(self):
        pass

    def __material_combo_box_changed(self):
        has_text = bool(self.material_combo_box.currentText())
        self.delete_material_button.setEnabled(has_text)

    def __property_combo_box_changed(self):
        has_text = bool(self.property_combo_box.currentText())
        self.delete_property_button.setEnabled(has_text)
        self.edit_property_button.setEnabled(has_text)

    def __condition_combo_box_changed(self):
        has_text = bool(self.condition_combo_box.currentText())
        self.delete_condition_button.setEnabled(has_text)
        # self.edit_condition_button.setEnabled(has_text)

    def __result_combo_box_changed(self):
        has_text = bool(self.result_combo_box.currentText())
        self.delete_result_button.setEnabled(has_text)
        self.edit_result_button.setEnabled(has_text)

    def __unit_combo_box_changed(self):
        has_text = bool(self.unit_combo_box.currentText())
        self.delete_unit_button.setEnabled(has_text)
        self.edit_unit_button.setEnabled(has_text)

    # TODO: add question
    def __delete_type_btn_clicked(self):
        type_name = self.material_type_cmbox.currentText()
        self.math_operator_worker.delete_type(type_name)
        QMessageBox.information(self, "Успех", f"Тип {type_name} был удален")
        self.__init_material_types_cmbox()

    def __delete_material_button_clicked(self):
        self.math_operator_worker.delete_material(self.material_combo_box.currentText())
        QMessageBox.information(self, "Успех", "Материал был удален")
        self.__init_materials_combo_box()

    def __delete_property_button_clicked(self):
        self.math_operator_worker.delete_property(self.property_combo_box.currentText())
        QMessageBox.information(self, "Успех", "Свойство было удалено")
        self.__init_properties_combo_box()

    def __delete_condition_button_clicked(self):
        self.math_operator_worker.delete_condition(self.condition_combo_box.currentText())
        QMessageBox.information(self, "Успех", "Условие было удалено")
        self.__init_conditions_combo_box()

    def __delete_result_button_clicked(self):
        self.math_operator_worker.delete_result(self.result_combo_box.currentText())
        QMessageBox.information(self, "Успех", "Результат был удален")
        self.__init_result_combo_box()

    def __delete_unit_button_clicked(self):
        self.math_operator_worker.delete_unit(self.unit_combo_box.currentText())
        QMessageBox.information(self, "Успех", "Единица измерения была удалена")
        self.__init_unit_combobox()

    def __add_type_btn_clicked(self):
        self.add_type_window = qAddTypeWindow.AddTypeWindow()
        self.add_type_window.show()

    def __add_material_button_clicked(self):
        self.add_material_window = qAddMaterialWindow.AddMaterialWindow()
        self.add_material_window.show()

    def __add_property_button_clicked(self):
        self.add_property_window = qAddPropertyWindow.AddPropertyWindow()
        self.add_property_window.show()

    @QtCore.pyqtSlot()
    def __add_condition_button_clicked(self):
        self.add_condition_window = qAddConditionWindow.AddConditionWindow()
        self.add_condition_window.show()

    def __add_result_button_clicked(self):
        self.add_result_window = qAddResultWindow.AddResultWindow()
        self.add_result_window.show()

    def __add_unit_button_clicked(self):
        self.add_unit_window = qAddUnitWindow.AddUnitWindow()
        self.add_unit_window.show()

    def __edit_type_btn_clicked(self):
        current_type = self.material_type_cmbox.currentText()
        self.edit_type_window = qEditTypeWindow.EditTypeWindow(current_type)
        self.edit_type_window.show()

    def __edit_material_button_clicked(self):
        self.edit_material_window = qEditMaterialWindow.EditMaterialWindow(self.material_combo_box.currentText())
        self.edit_material_window.show()

    def __edit_property_button_clicked(self):
        current_unit = self.math_operator_worker.get_unit_by_property_name(self.property_combo_box.currentText())[0][0]
        self.edit_property_window = qEditPropertyWindow.EditPropertyWindow(self.property_combo_box.currentText(),
                                                                           current_unit)
        self.edit_property_window.show()

    def __edit_condition_button_clicked(self):
        pass

    def __edit_result_button_clicked(self):
        current_result = self.result_combo_box.currentText()
        current_unit_name = self.math_operator_worker.get_unit_by_result_name(current_result)[0][0]
        self.edit_window = qEditResultWindow.EditResultWindow(current_result, current_unit_name)
        self.edit_window.show()

    def __edit_unit_button_clicked(self):
        self.edit_unit_window = qEditUnitWindow.EditUnitWindow(self.unit_combo_box.currentText())
        self.edit_unit_window.show()
