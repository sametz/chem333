from ipywidgets import interactive
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from nmrtools.nmrmath import first_order, nspinspec
from nmrtools.nmrplot import add_signals

layout = go.Layout(
    xaxis={'autorange': 'reversed'}
)


def interactive_dd(J1=3.0, J2=7.0, w=0.5):
    args = (J1, J2)
    x = np.linspace(85, 115, 8000)
    signal = (100.0, 1)
    couplings = [(J1, 1), (J2, 1)]
    spectrum = first_order(signal, couplings)
    y = add_signals(x, spectrum, w)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)


def interactive_ddd(J1=4.0, J2=10.0, J3=12.0):
    args = (J1, J2, J3)
    x = np.linspace(75, 125, 8000)
    signal = (100.0, 1)
    couplings = [(J1, 1), (J2, 1), (J3, 1)]
    spectrum = first_order(signal, couplings)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)


def interactive_dddd(J1=6.0, J2=6.0, J3=10.0, J4=16.0):
    args = (J1, J2, J3, J4)
    x = np.linspace(75, 125, 8000)
    signal = (100.0, 1)
    couplings = [(J1, 1), (J2, 1), (J3, 1), (J4, 1)]
    spectrum = first_order(signal, couplings)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)


def interactive_AB(v1=150.0, v2=50.0, J=10.0):
    x = np.linspace(25, 175, 8000)
    freqs = [v1, v2]
    Js = np.array(
        [[0.0, J],
         [J, 0.0]])
    spectrum = nspinspec(freqs, Js)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)


def interactive_ABX(va=110.0, vb=90.0, vx=200.0, Jax=5.0, Jbx=10.0, Jab=13.0):
    x = np.linspace(50, 235, 8000)
    freqs = [va, vb, vx]
    Js = np.array(
        [[0.0, Jab, Jax],
         [Jab, 0.0, Jbx],
         [Jax, Jbx, 0]])
    spectrum = nspinspec(freqs, Js)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)


def interactive_AAXX(va=110.0, vx=90.0,
                     Jaa=15.0, Jxx=15.0, Jax=7.0, Jax_prime=7.0):
    x = np.linspace(-10, 210, 8000)
    freqs = [va, va, vx, vx]
    Js = np.array(
        [[0.0, Jaa, Jax, Jax_prime],
         [Jaa, 0.0, Jax_prime, Jax],
         [Jax, Jax_prime, 0, Jxx],
         [Jax_prime, Jax, Jxx, 0]])
    spectrum = nspinspec(freqs, Js)
    y = add_signals(x, spectrum, 0.5)
    obj = go.Scatter(x=x, y=y)
    data = [obj]
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)
