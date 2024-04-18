from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton

from interface.qDataWidget import DataWidget
from interface.qMathModelWidget import MathModelWidget


class ResearcherTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)
        self.data_tab = DataWidget()
        self.math_model_tab = MathModelWidget()

        # Add tabs
        self.tabs.addTab(self.data_tab, "Выбор данных")
        self.tabs.addTab(self.math_model_tab, "Математическая модель")

        # Connect events
        self.child = self.data_tab.layout.parentWidget().findChild(QPushButton, 'confirm_data')
        self.child.clicked.connect(self.__apply_dataset)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def __apply_dataset(self):
        self.math_model_tab.set_table_widget(self.data_tab.table)
        self.math_model_tab.change_header(self.data_tab.table)
        self.data_tab.layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(False)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ResearcherTabWidget()
    window.show()
    sys.exit(app.exec())
