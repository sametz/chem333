"""Functions used by notebooks for interactive NMR plots, using Holoviews/Panel.

When `panel.interact` passes args/kwargs to a function, all of the args/kwargs
will have a widget associated with it. In order to expose only the variables
that will be modified using widgets, wrapper functions that take only those
variables as arguments are required.

TODO: consider making all the non-wrapper functions private
"""

import holoviews as hv
import numpy as np
import panel as pn

# from nmrsim import SpinSystem
from nmrsim.discrete import AB
from nmrsim.firstorder import multiplet
from nmrsim.math import add_lorentzians
from nmrsim.qm import qm_spinsystem


def lineshape_from_peaklist(peaklist, w=0.5, points=800, limits=None):
    """Given a peaklist, Calculate the x (frequency) and y (intensity) for the
    corresponding lineshape.

    Parameters
    ----------
    peaklist : [(float, float)...]
        A list of (frequency, intensity) tuples
    w : float, optional (default = 0.5)
        Peak width at half height (Hz)
    points : int, optional (default = 800)
        The number of data points in the lineshape
    limits : (float, float), optional
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


def n_plus_one(J, n, v=100, i=1.0, w=0.5):
    """Given n and coupling constant J, return the lineshape for the corresponding
    n + 1 multiplet.

    Parameters
    ----------
    J: float
        the coupling constant in Hz
    n: int
        the number of neighboring nuclei (the 'n' in the 'n + 1' rule)
    v: float, optional (default = 100)
        the center of the multiplet (in Hz)
    i: float, optional (default = 1.0)
        The total of the individual peak's max intensities.
        Analogous to the integration of the signal when w = 0.5.
    w: float, optional (default = 0.5)
        The peak width at half-height (in Hz)

    Returns
    -------
    hv.Curve() object
        Formatted 'NMR-style' with labeled axes and the x-axis reversed

    """
    singlet = (v, i)  # center at 100 Hz; intensity 1
    couplings = [(J, n)]
    peaklist = multiplet(singlet, couplings)
    x, y = lineshape_from_peaklist(peaklist, w=w)
    return hv.Curve(zip(x, y)) \
        .options(axiswise=True, invert_xaxis=True) \
        .redim(y=hv.Dimension('intensity'), x=hv.Dimension('𝜈 (Hz)'))


def toggle_doublet(coupled=False):
    """Return a plot that simulates turning on/off a 10-Hz J coupling to a signal.

    Parameters
    ----------
    coupled : bool
        Whether to initialize with coupling on or not.

    Returns
    -------
    hv.Curve() object
    """
    n = 1 if coupled else 0
    return n_plus_one(10.0, n, w=0.5) \
        .options(xlim=(120, 80), ylim=(-0.1, 1.1))


def two_doublets(v1, v2, J, w=0.5, points=10000):
    """Return a plot for a first-order AX system.

    Parameters
    ----------
    v1, v2 : float
        The chemical shifts in Hz for the two signals
    J : float
        The coupling constant in Hz
    w: float, optional (default = 0.5)
        The peak width at half-height (in Hz)
    points : int, optional (default = 10000)
        The number of data points in the lineshape

    Returns
    -------
    hv.Curve() object
     """
    peak1 = (v1, 1)
    couplings = [(J, 1)]
    peak2 = (v2, 1)
    peaklist = multiplet(peak1, couplings) + multiplet(peak2, couplings)
    x, y = lineshape_from_peaklist(peaklist, w=w, points=points)
    return hv.Curve(zip(x, y)).options(axiswise=True, invert_xaxis=True,
                                       xlabel='𝜈',
                                       ylabel='intensity')


def singlet_to_triplet(n):
    """Return a plot showing transformation of s -> d -> t as n increases."""
    return n_plus_one(J=10.0, n=n, w=0.5).options(ylim=(-0.1, 1.1))


def simple_multiplet(n):
    """Return a plot for an n + 1 multiplet."""
    return n_plus_one(J=7.0, n=n, w=0.5).options(ylim=(-0.1, 1.1))


def n_coupling(*j_args, v=100.0, i=1.0,
               w=0.5, points=4000,
               limits=None):
    """Given parameters for a first-order multiplet, return a holoviews plot for it.

    Parameters
    ----------
    j_args: float
        One or more coupling constants, in Hz
    v: float, optional (default = 100.0 Hz)
        The frequency of the center of the multiplet, in Hz
    i: float, optional (default = 1.0)
        The intensity of the signal.
        When w = 0.5 Hz, i = the total of the peak heights,
        e.g. a doublet would default to two peaks with height 0.5.
    w: float, optional (default = 0.5 Hz)
    points: int, optional (default = 4000 datapoints)
    limits: (int or float, int or float), optional
        A tuple of minimum and maximum frequencies (Hz) for the plot.

    Returns
    -------
    hv.Curve() object
        Formatted 'NMR-style' with labeled axes and the x-axis reversed
    """
    couplings = [(j, 1) for j in j_args]
    peaklist = multiplet((v, i), couplings)

    # TODO: will n_coupling merit its own limit/points defaults, or just use lineshape_from_peaklist's?
    if not limits:
        limits = (v - 20, v + 20)
    x, y = lineshape_from_peaklist(peaklist,
                                   w=w,
                                   points=points,
                                   limits=limits)
    return hv.Curve(zip(x, y)) \
        .options(axiswise=True, invert_xaxis=True,
                 height=300, responsive=True
                 ) \
        .redim(y=hv.Dimension('intensity'), x=hv.Dimension('𝜈 (Hz)'))


def dd_interactive(J1, J2, w):
    return n_coupling(J1, J2, w=w)


def ddd_interactive(J1, J2, J3):
    return n_coupling(J1, J2, J3)


def dddd_interactive(J1, J2, J3, J4):
    return n_coupling(J1, J2, J3, J4)


dd_app = pn.interact(dd_interactive,
                     J1=(0.0, 10.0, 0.1, 3.0),
                     J2=(0.0, 10.0, 0.1, 7.0),
                     w=(0.0, 5.0, 0.1, 0.5)
                     )

ddd_app = pn.interact(ddd_interactive,
                      J1=(0.0, 15.0, 0.1, 4.0),
                      J2=(0.0, 15.0, 0.1, 10.0),
                      J3=(0.0, 15.0, 0.1, 12.0))

dddd_app = pn.interact(dddd_interactive,
                       J1=(0, 20, 0.1, 3.8),
                       J2=(0, 20, 0.1, 6.6),
                       J3=(0, 20, 0.1, 6.6),
                       J4=(0, 20, 0.1, 6.6))


def ab_wrapper(v1, v2, J):
    """A wrapper for nmrsim.discrete.AB so that chemical shift and J values are arguments."""
    vab = abs(v2 - v1)
    vcentr = (v1 + v2) / 2
    peaklist = AB(J, vab, vcentr)
    return peaklist


def ab_distortion(v1=100.0, v2=500.0):
    v1_arrow = hv.Arrow(v1, 0, '𝜈₁', '^')
    v2_arrow = hv.Arrow(v2, 0, '𝜈₂', '^')
    # sufficient datapoints to mitigate inaccurate intensities and "jittering"
    datapoints = max(int(abs(v2 - v1) * 100), 800)

    coupled = lineshape_from_peaklist(ab_wrapper(v1, v2, 10), points=datapoints)
    plot = hv.Curve(zip(*coupled)) * v1_arrow * v2_arrow
    return plot.options(axiswise=True, invert_xaxis=True,
                        xlabel='𝜈').redim(y=hv.Dimension('intensity', range=(-0.4, 1.2)))


def abx_wrapper(va=110.0, vb=90.0, vx=200.0, Jax=5.0, Jbx=10.0, Jab=13.0):
    # x = np.linspace(0, 235, 8000)
    freqs = [va, vb, vx]
    Js = np.array(
        [[0.0, Jab, Jax],
         [Jab, 0.0, Jbx],
         [Jax, Jbx, 0]])
    peaklist = qm_spinsystem(freqs, Js)
    # y = add_lorentzians(x, peaklist, 0.5)
    return peaklist


def abx(va, vb, vx, Jax, Jbx, Jab):
    peaklist = abx_wrapper(va, vb, vx, Jax, Jbx, Jab)
    vs = [va, vb, vx]
    vmax = max(vs)
    vmin = min(vs)
    # sufficient datapoints to mitigate inaccurate intensities and "jittering"
    datapoints = max(int(vmax - vmin) * 100, 800)
    xy = lineshape_from_peaklist(peaklist, points=datapoints)
    plot = hv.Curve(zip(*xy))
    return plot.options(axiswise=True, invert_xaxis=True,
                        xlabel='𝜈',
                        height=300, responsive=True
                        ).redim(y=hv.Dimension('intensity', range=(-0.4, 1.2)))


def interactive_aaxx(va=110.0, vx=90.0,
                     Jaa=15.0, Jxx=15.0, Jax=7.0, Jax_prime=7.0):
    datapoints = max(abs(int(va - vx)) * 100, 800)
    # x = np.linspace(min_, max_, 8000)
    freqs = [va, va, vx, vx]
    Js = np.array(
        [[0.0, Jaa, Jax, Jax_prime],
         [Jaa, 0.0, Jax_prime, Jax],
         [Jax, Jax_prime, 0, Jxx],
         [Jax_prime, Jax, Jxx, 0]])
    peaklist = qm_spinsystem(freqs, Js)
    xy = lineshape_from_peaklist(peaklist, points=datapoints)
    plot = hv.Curve(zip(*xy))
    return plot.options(axiswise=True, invert_xaxis=True,
                        xlabel='𝜈',
                        height=300, responsive=True
                        ).redim(y=hv.Dimension('intensity', range=(-0.4, 1.2)))


def para_benzene(va=50.0, vx=215.0):
    return interactive_aaxx(
        va=va, vx=vx,
        Jaa=2.0, Jxx=2, Jax=8.0, Jax_prime=0.0)


def anti_gauche(va=90.0, vx=110.0,
                Jaa=-13.0, Jxx=-13.0, Jax=5.5, Jax_prime=5.5):
    return interactive_aaxx(
        va=va, vx=vx,
        Jaa=Jaa, Jxx=Jxx, Jax=Jax, Jax_prime=Jax_prime)


def anti_gauche_wrapper(Jax=5.5, Jax_prime=5.5):
    return anti_gauche(va=50, vx=150, Jax=Jax, Jax_prime=Jax_prime)
