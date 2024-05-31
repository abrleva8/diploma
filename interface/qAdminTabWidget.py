from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from database import material_bd
from interface.qMaterialWidget import MaterialWidget
from interface.qResearchWidget import ResearchWidget
from interface.qUserWidget import UserWidget


class AdminWidgets(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.user_tab = UserWidget()
        self.materials_tab = MaterialWidget()
        self.research_tab = ResearchWidget()

        self.tabs.tabBarClicked.connect(self.__material_tab_clicked)

        # Add tabs
        self.tabs.addTab(self.user_tab, "Пользователи")
        self.tabs.addTab(self.materials_tab, "Материалы")
        self.tabs.addTab(self.research_tab, "Эксперименты")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def __material_tab_clicked(self, index):
        self.material_bd_worker = material_bd.MaterialDataBaseWorker()
        match index:
            case 0:
                self.user_tab.init_users_combo_box()
            case 1:
                self.materials_tab.init_combox()
            case 2:
                self.research_tab.get_researches()
