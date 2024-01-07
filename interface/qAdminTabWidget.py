
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QMessageBox

from database import material_bd
from interface.qMaterialWidget import MaterialWidget
from interface.qUserWidget import UserWidget


class AdminWidgets(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.user_tab = UserWidget()
        self.materials = MaterialWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.tabBarClicked.connect(self.__material_tab_clicked)

        # Add tabs
        self.tabs.addTab(self.user_tab, "Пользователи")
        self.tabs.addTab(self.materials, "Материалы")
        # self.tabs.addTab(self.tab3, "Отчёты")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def __material_tab_clicked(self, index):
        self.material_bd_worker = material_bd.MaterialDataBaseWorker()
        if index == 1:
            self.materials.init_combox()
