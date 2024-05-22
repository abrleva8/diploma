from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLayout, QLabel, QCheckBox, QComboBox, \
    QPushButton

from interface.qAppWindows.qAppWindow import QAppWindow


class EDASettingsWindow(QAppWindow):
    eda_set_signal = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Настройки EDA")

        layout = self.__get_layout()

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.__center()

    def __center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __get_layout(self) -> QLayout:
        layout = QGridLayout()

        normal_distrub_lbl = QLabel("Нормальное распределение")
        self.normal_distrub_cbox = QCheckBox()
        self.normal_distrub_cmb_box = QComboBox()
        self.normal_distrub_cmb_box.addItem('Метод Шапиро-Уилка')
        self.normal_distrub_cmb_box.setEnabled(False)

        corr_analysis_lbl = QLabel("Корреляционный анализ")
        self.corr_analysis_cbox = QCheckBox()

        apply_btn = QPushButton("Применить")
        apply_btn.clicked.connect(self.__apply_btn_clicked)

        layout.addWidget(normal_distrub_lbl, 0, 0)
        layout.addWidget(self.normal_distrub_cbox, 0, 1)
        layout.addWidget(self.normal_distrub_cmb_box, 0, 2)

        layout.addWidget(corr_analysis_lbl, 1, 0)
        layout.addWidget(self.corr_analysis_cbox, 1, 1)

        layout.addWidget(apply_btn, 2, 0, 1, 3)

        return layout

    def __apply_btn_clicked(self):
        is_normal_check = self.normal_distrub_cbox.isChecked()
        check_method = self.normal_distrub_cmb_box.currentText()
        self.eda_set_signal.emit(is_normal_check, check_method)
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = EDASettingsWindow()
    window.show()
    sys.exit(app.exec())
