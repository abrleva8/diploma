from PyQt6.QtCore import QStringListModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QGridLayout, QComboBox, QLayout, QPushButton, \
    QLineEdit, QMessageBox

from database import admin_bd
from interface import qAddUserWindow
from interface.UserWidget import UserWidget


class MathOperatorWidgets(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.user_tab = UserWidget()
        self.materials = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.user_tab, "Пользователи")
        self.tabs.addTab(self.materials, "Материалы")
        self.tabs.addTab(self.tab3, "Отчёты")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
