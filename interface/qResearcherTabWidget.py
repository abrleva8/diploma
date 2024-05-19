from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton

from interface.qDataWidget import DataWidget
from interface.qMathModelResultWidget import MathModelResultWidget
from interface.qMathModelWidget import MathModelWidget, dataframe_generation_from_table
from math_model.data_frame_manager import DataFrameManager


class ResearcherTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)
        self.data_tab = DataWidget()
        self.math_model_tab = MathModelWidget()
        self.math_model_result = MathModelResultWidget()

        # Add tabs
        self.tabs.addTab(self.data_tab, "Выбор данных")
        self.tabs.addTab(self.math_model_tab, "Математическая модель")
        self.tabs.addTab(self.math_model_result, "Результаты")

        # Connect events
        self.child = self.data_tab.layout.parentWidget().findChild(QPushButton, 'confirm_data')
        self.child.clicked.connect(self.__apply_dataset)

        self.math_model_tab.apply_text_btn.clicked.connect(self.__apply_result)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def __apply_dataset(self):
        self.math_model_tab.set_table_widget(self.data_tab.table)
        self.math_model_tab.change_header(self.data_tab.table)
        header_labels = [self.data_tab.table.horizontalHeaderItem(i).text()
                         for i in range(self.data_tab.table.columnCount())]
        self.math_model_tab.df_manager = DataFrameManager(dataframe_generation_from_table(self.data_tab.table,
                                                                                          header_labels))
        self.data_tab.layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(False)

    def __apply_result(self):
        self.math_model_result.set_table_widget(self.math_model_tab.result)
        self.math_model_result.set_fisher_info(self.math_model_tab.fisher, self.math_model_tab.fisher_table)
        self.math_model_result.set_determinate_info(self.math_model_tab.r2)
        self.math_model_result.set_mse(self.math_model_tab.mse)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ResearcherTabWidget(parent=None)
    window.show()
    sys.exit(app.exec())
