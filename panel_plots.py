import holoviews as hv
import numpy as np

from nmrsim.firstorder import multiplet
from nmrsim.math import add_lorentzians


def lineshape_from_peaklist(peaklist, w=0.5, points=800, limits=None):
    """Given a peaklist, Calculate the x (frequency) and y (intensity) for the
    corresponding lineshape.

    Parameters
    ----------
    peaklist : [(float, float)...]
        A list of (frequency, intensity) tuples
    w : float
        Peak width at half height (Hz)
    points : int
        The number of data points in the lineshape
    limits : (float, float)
        The frequency (left/right) limits for the lineshape

    Returns
    -------
    ([float...], [float...])
        The lists of x coordinates (frequency) and corresponding y coordinates (intensity) for the lineshape.
    """
    peaklist.sort()
    if limits:
        try:
            l_limit, r_limit = limits
            l_limit = float(l_limit)
            r_limit = float(r_limit)
        except Exception as e:
            print(e)
            print('limits must be a tuple of two numbers')
            raise
        if l_limit > r_limit:
            l_limit, r_limit = r_limit, l_limit
    else:
        l_limit = peaklist[0][0] - 50
        r_limit = peaklist[-1][0] + 50
    x = np.linspace(l_limit, r_limit, points)
    y = add_lorentzians(x, peaklist, w)
    return x, y


def dd(J1, J2, v=100.0, i=1.0):
    peaklist = multiplet((v, i), [(J1, 1), (J2, 1)])
    x, y = lineshape_from_peaklist(peaklist,
                                   points=4000,
                                   limits=(v - 20, v + 20))
    return hv.Curve(zip(x, y))\
        .options(axiswise=True, invert_xaxis=True)\
        .redim(y=hv.Dimension('intensity'), x=hv.Dimension('𝜈 (Hz)'))


def dd_interactive(J1, J2):
    return dd(J1, J2)


def ddd(J1, J2, J3, v=100.0, i=1.0):
    peaklist = multiplet((v, i), [(J1, 1), (J2, 1), (J3, 1)])
    x, y = lineshape_from_peaklist(peaklist, limits=(v - 20, v + 20))
    return hv.Curve(zip(x, y)) \
        .options(axiswise=True, invert_xaxis=True) \
        .redim(y=hv.Dimension('intensity'), x=hv.Dimension('𝜈 (Hz)'))


def ddd_interactive(J1, J2, J3):
    return ddd(J1, J2, J3)
