import numpy as np
import pandas as pd
import seaborn as sns
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QMdiArea, QMessageBox, QMdiSubWindow, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from scipy.stats import norm
from scipy.stats import shapiro

from interface.qAppWindows.qAppWindow import QAppWindow


class NormalAnalystWindow(QAppWindow):

    is_normal_signal = pyqtSignal(bool)

    def __init__(self, df: pd.DataFrame):
        super().__init__()

        self.df = df

        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)

        self._canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self._canvas_2 = FigureCanvas(Figure(figsize=(5, 3)))
        self._ax_1 = self._canvas.figure.subplots()
        self._ax_2 = self._canvas_2.figure.subplots()

        X = df.iloc[:, 2:-1]
        df.to_csv("fragment.csv", sep=",", index=False)
        y = df[df.columns[-1]]

        if y.shape[0] == 0:
            QMessageBox.critical(self, "Ошибка", "Мало данных для анализа")

        mu, std = norm.fit(y)
        shapiro_result = shapiro(y)

        is_normal = shapiro_result.pvalue > 0.05
        self.is_normal_signal.emit(is_normal)

        n, bins, patches = self._ax_1.hist(
            y, density=True, bins=8
        )

        x_min, x_max = self._ax_1.get_xlim()
        x = np.linspace(x_min, x_max, 100)
        p = norm.pdf(x, mu, std)
        self._ax_1.plot(x, p, 'k', linewidth=2)

        self._ax_1.set_xlabel(y.name)
        self._ax_1.set_ylabel("Плотность")
        self._ax_1.set_title(f"Гистограмма признака {y.name}")

        # self._ax.format_coord = lambda x, y: 'the x-coordinate = ' + format(x, '1.4f') + ', ' + \
        #                                ' and the y-coordinate = ' + format(y, '1.4f')

        # self._ax_2.heatmap(X.corr())
        corr = X.corr()
        sns.heatmap(corr, ax=self._ax_2, annot=True)

        # corr.style.background_gradient(cmap='coolwarm', axis=self._ax_2)

        widget = QMainWindow()
        widget_2 = QMainWindow()
        widget.setCentralWidget(self._canvas)
        widget_2.setCentralWidget(self._canvas_2)
        widget.addToolBar(
            NavigationToolbar(self._canvas, self),
        )
        widget_2.addToolBar(
            NavigationToolbar(self._canvas_2, self),
        )
        sub_window = QMdiSubWindow()
        sub_window_2 = QMdiSubWindow()
        sub_window.setWidget(widget)
        sub_window_2.setWidget(widget_2)
        self.mdiArea.addSubWindow(sub_window)
        self.mdiArea.addSubWindow(sub_window_2)

        widget_info = QMainWindow()
        widget_info.setCentralWidget(
            QLabel(
                f"Статистика: {y.describe()}\n"
                f"Критерий Шапиро-Уилка: {shapiro_result}\n"
                f"Критерий {'пройден' if is_normal else 'не пройден'}"
            )
        )
        self.mdiArea.addSubWindow(widget_info)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = NormalAnalystWindow(pd.DataFrame(data=[
        [2, 2, 3, 4, 5, 2, 7, 4, 2, 4],
        [3, 4, 1, 4, 6, 2, 1, 4, 1, 5],
        [3, 4, 5, 4, 6, 2, 1, 3, 10, 4],
    ]))
    window.show()
    sys.exit(app.exec())
