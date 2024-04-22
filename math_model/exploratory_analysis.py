import pandas as pd

from plotting.canvas import Canvas


def plot_hists(df: pd.DataFrame, cols: list[str]) -> Canvas:
    canvas = Canvas()
    canvas.axes.hist(df[cols[0]])
    return canvas
