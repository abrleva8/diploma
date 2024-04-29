import numpy as np
import pandas as pd
from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QGridLayout, QLayout, QMainWindow, QMdiArea, QMessageBox, QMdiSubWindow, QLabel

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from scipy.stats import norm
from scipy.stats import shapiro


class NormalAnalystWindow(QMainWindow):

    is_normal_signal = pyqtSignal(bool)

    def __init__(self, series: pd.Series):
        super().__init__()

        self.series = series

        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self._ax = self._canvas.figure.subplots()

        series = series.dropna()
        if series.shape[0] == 0:
            QMessageBox.critical(self, "Ошибка", "Мало данных для анализа")

        mu, std = norm.fit(series)
        shapiro_result = shapiro(series)

        is_normal = shapiro_result.pvalue > 0.05
        self.is_normal_signal.emit(is_normal)

        n, bins, patches = self._ax.hist(
            series, density=True, bins=8
        )

        x_min, x_max = self._ax.get_xlim()
        x = np.linspace(x_min, x_max, 100)
        p = norm.pdf(x, mu, std)
        self._ax.plot(x, p, 'k', linewidth=2)

        self._ax.set_xlabel(series.name)
        self._ax.set_ylabel("Количество")
        self._ax.set_title(f"Гистограмма признака {series.name}")

        widget = QMainWindow()
        widget.setCentralWidget(self._canvas)
        widget.addToolBar(
            NavigationToolbar(self._canvas, self)
        )
        sub_window = QMdiSubWindow()
        sub_window.setWidget(widget)
        self.mdiArea.addSubWindow(sub_window)

        widget_info = QMainWindow()
        widget_info.setCentralWidget(
            QLabel(
                f"Статистика: {series.describe()}\n"
                f"Критерий Шапиро-Уилка: {shapiro_result}\n"
                f"Критерий {'пройден' if is_normal else 'не пройден'}"
            )
        )
        self.mdiArea.addSubWindow(widget_info)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = NormalAnalystWindow(pd.Series(name="x", data=[2, 2, 3, 4, 5, 2, 7, 4, 2, 4]))
    window.show()
    sys.exit(app.exec())
