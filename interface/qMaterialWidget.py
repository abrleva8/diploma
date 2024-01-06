from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, QMessageBox

from database import material_bd
from interface import qAddMaterialWindow, qAddPropertyWindow, qAddConditionWindow, qAddResultWindow


class MaterialWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.layout = self.__get_material_layout()
        self.setLayout(self.layout)

        self.math_operator_worker = material_bd.MaterialDataBaseWorker()
        self.init_combox()

    def init_combox(self):
        self.__init_materials_combo_box()
        self.__init_properties_combo_box()
        self.__init_conditions_combo_box()
        self.__init_result_combo_box()

    def __get_material_layout(self):
        layout = QGridLayout()

        self.material_label = QLabel("Материалы")
        layout.addWidget(self.material_label, 0, 0, 1, 2)

        self.material_combo_box = QComboBox(self)

        self.material_cb_model = QStringListModel()
        self.material_combo_box.setModel(self.material_cb_model)
        self.material_combo_box.currentTextChanged.connect(self.__material_combo_box_changed)
        layout.addWidget(self.material_combo_box, 1, 0)

        self.add_material_button = QPushButton(self)
        self.add_material_button.setText("Добавить материал")
        self.add_material_button.clicked.connect(self.__add_button_clicked)
        layout.addWidget(self.add_material_button, 1, 1)

        self.delete_material_button = QPushButton(self)
        self.delete_material_button.setText("Удалить материал")
        self.delete_material_button.setEnabled(False)
        self.delete_material_button.clicked.connect(self.__delete_button_clicked)
        layout.addWidget(self.delete_material_button, 1, 2)

        self.property_label = QLabel("Свойства")
        layout.addWidget(self.property_label, 2, 0, 1, 2)

        self.property_combo_box = QComboBox(self)
        self.property_cb_model = QStringListModel()
        self.property_combo_box.setModel(self.property_cb_model)
        self.property_combo_box.currentTextChanged.connect(self.__property_combo_box_changed)
        layout.addWidget(self.property_combo_box, 3, 0)

        self.add_property_button = QPushButton(self)
        self.add_property_button.setText("Добавить свойство")
        self.add_property_button.clicked.connect(self.__add_property_button_clicked)
        layout.addWidget(self.add_property_button, 3, 1)

        self.delete_property_button = QPushButton(self)
        self.delete_property_button.setText("Удалить свойство")
        self.delete_property_button.setEnabled(False)
        self.delete_property_button.clicked.connect(self.__delete_property_button_clicked)
        layout.addWidget(self.delete_property_button, 3, 2)

        self.condition_label = QLabel("Условия")
        layout.addWidget(self.condition_label, 4, 0, 1, 2)

        self.condition_combo_box = QComboBox(self)
        self.condition_cb_model = QStringListModel()
        self.condition_combo_box.setModel(self.condition_cb_model)
        self.condition_combo_box.currentTextChanged.connect(self.__condition_combo_box_changed)
        layout.addWidget(self.condition_combo_box, 5, 0)

        self.add_condition_button = QPushButton(self)
        self.add_condition_button.setText("Добавить условие")
        self.add_condition_button.clicked.connect(self.__add_condition_button_clicked)
        layout.addWidget(self.add_condition_button, 5, 1)

        self.delete_condition_button = QPushButton(self)
        self.delete_condition_button.setText("Удалить условие")
        self.delete_condition_button.setEnabled(False)
        self.delete_condition_button.clicked.connect(self.__delete_condition_button_clicked)
        layout.addWidget(self.delete_condition_button, 5, 2)

        self.result_label = QLabel("Результат")
        layout.addWidget(self.result_label, 6, 0, 1, 2)

        self.result_combo_box = QComboBox(self)
        self.result_cb_model = QStringListModel()
        self.result_combo_box.setModel(self.result_cb_model)
        self.result_combo_box.currentTextChanged.connect(self.__result_combo_box_changed)
        layout.addWidget(self.result_combo_box, 7, 0)

        self.add_result_button = QPushButton(self)
        self.add_result_button.setText("Добавить результат")
        self.add_result_button.clicked.connect(self.__add_result_button_clicked)
        layout.addWidget(self.add_result_button, 7, 1)

        self.delete_result_button = QPushButton(self)
        self.delete_result_button.setText("Удалить результат")
        self.delete_result_button.setEnabled(False)
        self.delete_result_button.clicked.connect(self.__delete_result_button_clicked)
        layout.addWidget(self.delete_result_button, 7, 2)

        return layout

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

    def __add_button_clicked(self):
        self.add_material_window = qAddMaterialWindow.AddMaterialWindow()
        self.add_material_window.show()

    def __material_combo_box_changed(self):
        self.delete_material_button.setEnabled(bool(self.material_combo_box.currentText()))

    def __property_combo_box_changed(self):
        self.delete_property_button.setEnabled(bool(self.property_combo_box.currentText()))

    def __condition_combo_box_changed(self):
        self.delete_condition_button.setEnabled(bool(self.condition_combo_box.currentText()))

    def __result_combo_box_changed(self):
        self.delete_result_button.setEnabled(bool(self.result_combo_box.currentText()))

    def __delete_button_clicked(self):
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

    def __add_property_button_clicked(self):
        self.add_property_window = qAddPropertyWindow.AddPropertyWindow()
        self.add_property_window.show()

    def __add_condition_button_clicked(self):
        self.add_condition_window = qAddConditionWindow.AddConditionWindow()
        self.add_condition_window.show()

    def __add_result_button_clicked(self):
        self.add_result_window = qAddResultWindow.AddResultWindow()
        self.add_result_window.show()
