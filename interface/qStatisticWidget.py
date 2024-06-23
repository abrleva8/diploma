from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel, QLayout, QDoubleSpinBox, QPushButton, QMessageBox


class StatisticWidget(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        self.layout = self.__get_layout()
        self.setLayout(self.layout)

    def __get_layout(self) -> QLayout:
        try:
            with open('confidence.txt', 'r') as f:
                confidence_value = float(f.readline())
        except:
            confidence_value = 0.05

        layout = QFormLayout()

        confidence_lbl = QLabel('Уровень значимости')
        self.confidence_spbox = QDoubleSpinBox()
        self.confidence_spbox.setRange(0.001, 0.1)
        self.confidence_spbox.setSingleStep(0.001)
        self.confidence_spbox.setDecimals(3)
        self.confidence_spbox.setValue(confidence_value)

        self.apply_btn = QPushButton('Применить')
        self.apply_btn.clicked.connect(self.__apply_btn_clicked)

        layout.addRow(confidence_lbl, self.confidence_spbox)
        layout.addRow(self.apply_btn)

        return layout

    def __apply_btn_clicked(self):
        with open('confidence.txt', 'w') as f:
            spbox_value = self.confidence_spbox.value()
            f.write(str(spbox_value))

        QMessageBox.information(self, 'Успех', 'Уровень значимости записан')
