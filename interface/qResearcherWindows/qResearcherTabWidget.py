from PyQt6.QtCore import QObject, QMetaObject, pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton

from interface.qResearcherWindows.qDataWidget import DataTabWidget
from interface.qResearcherWindows.qMathModelResultWidget import MathModelResultWidget
from interface.qResearcherWindows.qMathModelWidget import MathModelWidget, dataframe_generation_from_table
from interface.qResearcherWindows.qPredictTabWidget import PredictTabWidget
from math_model.data_frame_manager import DataFrameManager


class ResearcherTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.child_predict_model_btn = None
        self.child_save_model_btn = None
        self.child_load_model_btn = None
        self.child_confirm_data_btn = None
        self.layout = QVBoxLayout(self)

        self.df_manager: DataFrameManager = None

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.data_tab = DataTabWidget()
        self.math_model_tab = MathModelWidget(self.df_manager)
        self.math_model_result = MathModelResultWidget()
        self.predict_tab = PredictTabWidget()

        # Add tabs
        self.tabs.addTab(self.data_tab, "Выбор данных")
        self.tabs.addTab(self.math_model_tab, "Математическая модель")
        self.tabs.addTab(self.math_model_result, "Результаты")
        self.tabs.addTab(self.predict_tab, "Предсказание")

        # Connect events
        # TODO: понять как избавиться от лишних связей
        self.child_confirm_data_btn = self.data_tab.layout.parentWidget().findChild(QPushButton, 'confirm_data')
        self.child_confirm_data_btn.clicked.connect(self.__apply_dataset)
        self.make_connects()

        # Add tabs to widget
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)

    def make_connects(self):
        self.child_load_model_btn = self.math_model_result.parentWidget().findChild(QPushButton, 'load_model_btn')
        self.child_save_model_btn = self.math_model_result.parentWidget().findChild(QPushButton, 'save_model_btn')
        self.child_predict_model_btn = self.predict_tab.parentWidget().findChild(QPushButton, 'predict_btn')

        self.child_load_model_btn.clicked.connect(self.__load_model)
        self.child_save_model_btn.clicked.connect(self.__save_model)

        if self.child_predict_model_btn is not None:
            self.child_predict_model_btn.clicked.connect(self.__predict_result)

        self.math_model_tab.apply_text_btn.clicked.connect(self.__apply_result)

    def __apply_dataset(self):
        self.math_model_tab.set_table_widget(self.data_tab.table)
        self.math_model_tab.change_header(self.data_tab.table)
        header_labels = [self.data_tab.table.horizontalHeaderItem(i).text()
                         for i in range(self.data_tab.table.columnCount())]
        self.df_manager = DataFrameManager(dataframe_generation_from_table(self.data_tab.table,
                                                                           header_labels))
        self.math_model_tab.df_manager = self.df_manager

        self.math_model_tab.save_df_btn.setEnabled(True)
        self.data_tab.layout.parentWidget().findChild(QPushButton, 'confirm_data').setEnabled(False)
        print(1)

    def __apply_result(self):
        self.math_model_result.set_table_widget(self.math_model_tab.model_info.pingouin_result)
        self.math_model_result.set_fisher_info(self.math_model_tab.model_info.fisher_result,
                                               self.math_model_tab.model_info.fisher_table)
        self.math_model_result.set_determinate_info(self.math_model_tab.model_info.r2)
        self.math_model_result.set_mse(self.math_model_tab.model_info.mse)
        self.predict_tab.set_columns(self.math_model_tab.pipeline[0].transformers[0][1].column_names.to_list())
        self.make_connects()

    def __save_model(self):
        self.math_model_result.save_model(self.math_model_tab.saver)

    def __load_model(self):
        model_loader = self.math_model_result.load_model(self.math_model_tab.saver)
        print(model_loader.pipeline[0].transformers[0][1].column_names.to_list())
        self.math_model_tab.model_info = model_loader.model_info
        self.math_model_tab.pipeline = model_loader.pipeline

        self.__apply_result()

    def __predict_result(self):
        df = self.predict_tab.create_df_for_predict()
        res = self.math_model_tab.pipeline.predict(df)
        print(res)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ResearcherTabWidget(parent=None)
    window.show()
    sys.exit(app.exec())
