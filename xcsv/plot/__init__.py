###############################################################################
# Project: Extended CSV common file format
# Purpose: Classes to plot data from an extended CSV file
# Author:  Paul M. Breen
# Date:    2022-05-13
###############################################################################

__version__ = '0.2.0'

import re

import matplotlib.pyplot as plt

import xcsv

class Plot(object):
    """
    Class for plotting extended CSV objects
    """

    DEFAULTS = {
        'title_key': 'title',
        'caption_key': 'citation',
        'label_key': 'id'
    }

    def __init__(self):
        """
        Constructor
        """

        self.fig = None
        self.axs = []
        self.datasets = []
        self.xcol = None
        self.ycol = None

    def get_plot_data_extent(self, datasets, xcol, ycol):
        """
        Get the extent over which the datasets range in data coordinates

        A list is returned with the shape [left, right, bottom, top].  This
        can be used for the extent kwarg to imshow().

        At least the ycol must be specified.  If xcol is None, then the
        indices of the data points are used for the x-axis coordinates.

        :param datasets: A list of XCSV objects containing the input datasets
        :type datasets: list
        :param xcol: The x-axis data column header label
        :type xcol: str
        :param ycol: The y-axis data column header label
        :type ycol: str
        :returns: The extent
        :rtype: list
        """

        if xcol is None:
            extent = [0, max([len(dataset.data) - 1 for dataset in datasets]), min([dataset.data[ycol].min() for dataset in datasets]), max([dataset.data[ycol].max() for dataset in datasets])]
        else:
            extent = [min([dataset.data[xcol].min() for dataset in datasets]), max([dataset.data[xcol].max() for dataset in datasets]), min([dataset.data[ycol].min() for dataset in datasets]), max([dataset.data[ycol].max() for dataset in datasets])]

        return extent

    def get_metadata_item_value(self, dataset, key, section='header'):
        """
        Get the value of the given key from the metadata dict of the given
        dataset, or the empty string if not found

        If the value is a list, then its elements are joined into a
        newline-separated string, as it would appear in the original file

        By default, the key is looked for in the 'header' section.  Set
        section='column_headers' to look in the 'column_headers' section
        instead.

        :param dataset: The dataset to query
        :type dataset: XCSV object
        :param key: The header item key
        :type key: str
        :param section: The metadata section.
        One of ['header','column_headers']
        :type section: str
        :returns: The value of the given key or the empty string if not found
        :rtype: str
        """

        try:
            value = dataset.metadata[section][key]

            if isinstance(value, list):
                value = '\n'.join(value)
        except KeyError:
            value = ''

        return value

    def setup_data_plot(self, fig, ax, xlabel=None, ylabel=None, caption=None, caption_x=0.1, caption_y=0.02, caption_wrap=True, subplots_adjust_bottom=0.15):
        """
        Setup the data plot

        This sets fixed annotations, such as the x- and y-axis labels.

        :param fig: The figure object
        :type fig: matplotlib.figure.Figure
        :param ax: The axis object
        :type ax: matplotlib.axes.Axes
        :param xlabel: The x-axis label text
        :type xlabel: str
        :param ylabel: The y-axis label text
        :type ylabel: str
        :param caption: The figure caption text
        :type caption: str
        :param caption_x: An offset for the caption text in the x-direction
        :type caption_x: float
        :param caption_y: An offset for the caption text in the y-direction
        :type caption_y: float
        :param caption_wrap: Wrap the caption text
        :type caption_wrap: bool
        :param subplots_adjust_bottom: Add space to hold the caption
        :type subplots_adjust_bottom: float
        """

        if caption:
            fig.text(caption_x, caption_y, caption, wrap=caption_wrap)
            fig.subplots_adjust(bottom=subplots_adjust_bottom)

        if xlabel:
            ax.set_xlabel(xlabel)

        if ylabel:
            ax.set_ylabel(ylabel)

    def plot_data(self, fig, ax, dataset, xcol, ycol, label=None, invert_xaxis=False, invert_yaxis=False, opts={}):
        """
        Plot the data for the given dataset

        * The xcol header label specifies the data series from the dataset's
        data table to be used for the x-axis.
        * The ycol header label specifies the data series from the dataset's
        data table to be used for the y-axis.

        :param fig: The figure object
        :type fig: matplotlib.figure.Figure
        :param ax: The axis object
        :type ax: matplotlib.axes.Axes
        :param dataset: The dataset to plot
        :type dataset: XCSV object
        :param xcol: The x-axis data column header label
        :type xcol: str
        :param ycol: The y-axis data column header label
        :type ycol: str
        :param label: A unique label to identify this data series in the plot
        legend.  This will most likely be a header item from the XCSV header
        :type label: str
        :param invert_xaxis: Invert the x-axis
        :type invert_xaxis: bool
        :param invert_yaxis: Invert the y-axis
        :type invert_yaxis: bool
        :param opts: Option kwargs to apply to all plots (e.g., color, marker)
        :type opts: dict
        """
  
        if xcol:
            ax.plot(dataset.data[xcol], dataset.data[ycol], label=label, **opts)
        else:
            ax.plot(dataset.data[ycol], label=label, **opts)

        if invert_xaxis:
            ax.invert_xaxis()

        if invert_yaxis:
            ax.invert_yaxis()

        if label:
            ax.legend()

    def plot_data_bg(self, fig, ax, img, img_extent, aspect='auto', alpha=0.5):
        """
        Plot the given image as a background for the data plot

        :param fig: The figure object
        :type fig: matplotlib.figure.Figure
        :param ax: The axis object
        :type ax: matplotlib.axes.Axes
        :param img: The image data
        :type img: array-like or PIL image
        :param img_extent: The image data extent as [left, right, bottom, top]
        :type img_extent: list
        :param aspect: The aspect ratio of the image
        :type aspect: str
        :param alpha: Controls the transparency of the image
        :type alpha: float
        """
 
        ax.imshow(img, extent=img_extent, aspect=aspect, alpha=alpha)

    def add_plot_bg(self, img_path=None, img=None, img_extent=None, axs_idx=0):
        """
        Add the image as a background for the data plot

        The image data can be provided directly in img.  Alternatively, a file
        can be specified in img_path that contains the image data.

        Whilst an img_extent can be specified (particularly useful if the image
        should only occupy a part of the data plot area), if it's left as None,
        then the function will discover the full extent of the plot area.  An
        advantage here is that if either of the axes have been inverted, then
        this will take this into account.

        :param img_path: Path to a file containing the image data
        :type img_path: str
        :param img: The image data
        :type img: array-like or PIL image
        :param img_extent: The image data extent as [left, right, bottom, top]
        :type img_extent: list
        :param axs_idx: The index of the axis object in the axs array
        :type axs_idx: int
        """

        if img is None:
            if img_path:
                img = plt.imread(img_path)

        if not img_extent:
            # This automatically takes care of inverted x or y axes
            img_extent = [*self.axs[axs_idx].get_xlim(), *self.axs[axs_idx].get_ylim()]

        if img is not None:
            self.plot_data_bg(self.fig, self.axs[axs_idx], img, img_extent)

    def setup_figure_and_axes(self, figsize=None):
        """
        Setup the figure and axes array

        If not called directly, then it is called by the plot_datasets()
        function.  If a specific figure size is required, then this function
        should be called directly, before calling any of the plotting
        functions (e.g., plot_datasets()).

        This stores the figure object in self.fig and the axes array in
        self.axs.

        :param figsize: The figure size tuple as (width, height)
        :type figsize: tuple
        """

        self.fig = plt.figure(figsize=figsize)
        self.axs.append(self.fig.add_subplot())

    def plot_datasets(self, datasets, fig=None, axs=None, axs_idx=0, xcol=None, ycol=None, xidx=None, yidx=0, xlabel=None, ylabel=None, title=None, title_wrap=True, caption=None, label_key=None, invert_xaxis=False, invert_yaxis=False, show=True, opts={}):
        """
        Plot the data for the given datasets

        Either the xcol and ycol column header labels, or the xidx and yidx
        column indices, can be specified.  These are mutually exclusive.  They
        identify the data series from the datasets' data tables to be used for
        the x- and y-axis data.

        If annotations such as the title and caption, and the label_key,
        are not specified, then they are taken from XCSV header items
        (see self.DEFAULTS for details).  If these keys are not present in
        the header, then an empty string is used instead, effectively leaving
        them blank.

        If show is set to False, then custom edits can be made to the plot
        (e.g. adding extra annotations) before displaying.  Also, if saving
        the plot to an output file instead of displaying, then set show=False.

        :param datasets: A list of XCSV objects containing the input datasets
        :type datasets: list
        :param fig: The figure object
        :type fig: matplotlib.figure.Figure
        :param axs: The axes array
        :type axs: matplotlib.axes.Axes
        :param axs_idx: The index of the axis object in the axs array
        :type axs_idx: int
        :param xcol: The x-axis data column header label
        :type xcol: str
        :param ycol: The y-axis data column header label
        :type ycol: str
        :param xidx: The x-axis data column index
        :type xidx: int
        :param yidx: The y-axis data column index
        :type yidx: int
        :param xlabel: The x-axis label text
        :type xlabel: str
        :param ylabel: The y-axis label text
        :type ylabel: str
        :param title: The figure title text
        :type title: str
        :param title_wrap: Wrap the title text
        :type title_wrap: bool
        :param caption: The figure caption text
        :type caption: str
        :param label_key: The key of a header item in the XCSV header to be
        used as a unique label to identify each data series in the plot legend
        :type label_key: str
        :param invert_xaxis: Invert the x-axis
        :type invert_xaxis: bool
        :param invert_yaxis: Invert the y-axis
        :type invert_yaxis: bool
        :param show: Show the plot
        :type show: bool
        :param opts: Option kwargs to apply to all plots (e.g., color, marker)
        :type opts: dict
        """
 
        if fig:
            self.fig = fig

        if axs:
            self.axs = axs

        if not self.fig or not self.axs:
            self.setup_figure_and_axes()

        self.datasets = datasets
        self.xcol = xcol
        self.ycol = ycol
        generate_colors = True

        if not title:
            title = self.get_metadata_item_value(datasets[0], self.DEFAULTS['title_key'])

        if not caption:
            caption = self.get_metadata_item_value(datasets[0], self.DEFAULTS['caption_key'])

        if not label_key:
            label_key = self.DEFAULTS['label_key']

        if not xcol:
            if xidx is not None:
                self.xcol = datasets[0].data.iloc[:, xidx].name

        if not ycol:
            self.ycol = datasets[0].data.iloc[:, yidx].name

        if not xlabel:
            xlabel = self.xcol

        if not ylabel:
            ylabel = self.ycol

        if 'color' in opts:
            generate_colors = False

        self.fig.suptitle(title, wrap=title_wrap)
        self.setup_data_plot(self.fig, self.axs[axs_idx], caption=caption, xlabel=xlabel, ylabel=ylabel)

        for i, dataset in enumerate(datasets):
            label = self.get_metadata_item_value(dataset, label_key)

            if generate_colors:
                opts.update({'color': f'C{i}'})

            self.plot_data(self.fig, self.axs[axs_idx], dataset, self.xcol, self.ycol, label=label, invert_xaxis=invert_xaxis, invert_yaxis=invert_yaxis, opts=opts)

        if show:
            plt.show()

    def show(self):
        """
        Display the figure

        Convenience function so caller can avoid having to import matplotlib.
        """

        plt.show()

    def savefig(self, filename):
        """
        Save the figure to the given output filename

        Convenience function so caller can avoid having to import matplotlib.
        """

        self.fig.savefig(filename)

