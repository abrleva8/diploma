import numpy as np
import pandas as pd
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QMdiArea, QMdiSubWindow

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# TODO: get real name
class PlottingWindow(QMainWindow):
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        super().__init__()
        self.df = df
        self.cols = cols
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        for col in self.cols:
            self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
            self._ax = self._canvas.figure.subplots()
            tmp = df[col].dropna()
            if tmp.shape[0] == 0:
                continue
            n, bins, patches = self._ax.hist(
                tmp
            )
            self._ax.set_xlabel(col)
            self._ax.set_ylabel("Количество")
            # self._ax.set_title(r"$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$")
            self._ax.set_title(f"Гистрограмма признака {col}")
            # self._ax.axis([40, 160, 0, 0.03])
            self._ax.grid(True)

            widget = QMainWindow()
            widget.setCentralWidget(self._canvas)
            widget.addToolBar(
               NavigationToolbar(self._canvas, self)
            )
            sub_window = QMdiSubWindow()
            sub_window.setWidget(widget)
            self.mdiArea.addSubWindow(sub_window)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    df = pd.DataFrame({'x': [2, 2, 3, 4, 5, 2, 7, 4, 2, 4],
                       'y': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]})
    window = PlottingWindow(df=df, cols=['x', 'y'])
    window.show()
    sys.exit(app.exec())
