from ipywidgets import interactive
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from nmrtools.nmrmath import first_order
from nmrtools.nmrplot import add_signals


def interactive_dd(J1=3.0, J2=7.0):
    args = (J1, J2)
    x = np.linspace(85, 115, 800)
    signal = (100.0, 1)
    couplings = [(J1, 1), (J2, 1)]
    spectrum = first_order(signal, couplings)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    iplot(data)


def interactive_ddd(J1=3.0, J2=7.0, J3=10.0):
    args = (J1, J2, J3)
    x = np.linspace(75, 125, 800)
    signal = (100.0, 1)
    couplings = [(J1, 1), (J2, 1), (J3, 1)]
    spectrum = first_order(signal, couplings)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    iplot(data)
