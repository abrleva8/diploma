from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget

from interface.qDataWidget import DataWidget


class ResearcherWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)
        self.data_tab = DataWidget()

        # Add tabs
        self.tabs.addTab(self.data_tab, "Выбор данных")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ResearcherWidget()
    window.show()
    sys.exit(app.exec())
