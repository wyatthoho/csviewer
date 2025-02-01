from typing import Callable, Iterable, Optional, Tuple

import matplotlib.pyplot as plt


def initialize_figure(figsize: Tuple[float, float]) -> Tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=figsize, tight_layout=True)
    ax = plt.axes()
    return fig, ax


def get_plot_method(ax: plt.Axes, scale_x: str, scale_y: str) -> Callable:
    if scale_x == 'linear' and scale_y == 'linear':
        plot_method = ax.plot
    elif scale_x == 'log' and scale_y == 'linear':
        plot_method = ax.semilogx
    elif scale_x == 'linear' and scale_y == 'log':
        plot_method = ax.semilogy
    elif scale_x == 'log' and scale_y == 'log':
        plot_method = ax.loglog
    return plot_method


def make_a_plot(plot_method: Callable,
                values_x: Iterable[float],
                values_y: Iterable[float],
                label: Optional[str] = None) -> None:
    plot_method(values_x, values_y, label=label)


def set_axes(ax: plt.Axes,
             title: str,
             label_x: str, label_y: str,
             lim_x: Tuple[float, float], lim_y: Tuple[float, float],
             grid_visible: bool, legend_visible: bool) -> None:
    ax.set_title(title)
    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.set_xlim(lim_x)
    ax.set_ylim(lim_y)
    ax.grid(visible=grid_visible, axis='both')
    if legend_visible:
        ax.legend()
