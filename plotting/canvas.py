import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class Canvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)

    def plot(self, y_true, y_predict):
        self.axes.clear()
        self.axes.set_title('График предсказаний и ошибок!')
        self.axes.scatter(y_true, y_predict, c='crimson')

        p1 = max(y_predict.max(), np.array(y_true).max())
        p2 = min(y_predict.min(), np.array(y_true).min())
        self.axes.plot([p1, p2], [p1, p2], 'b-')

        self.axes.set_xlabel('Истинные значения', fontsize=15)
        self.axes.set_ylabel('Предсказания', fontsize=15)
        self.draw()
