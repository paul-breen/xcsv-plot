###############################################################################
# Project: Extended CSV common file format
# Purpose: Classes to plot data from an extended CSV file
# Author:  Paul M. Breen
# Date:    2022-05-13
###############################################################################

import argparse
import json

import xcsv
import xcsv.plot as xp

def get_datasets(filenames):
    """
    Read the XCSV datasets from the given list of files

    :param filenams: The list of filenames to be read in
    :type filenames: list
    :returns: The contents of the given files as XCSV objects
    :rtype: list
    """

    datasets = []

    for filename in filenames:
        with xcsv.File(filename) as f:
            datasets.append(f.read())

    return datasets

def parse_cmdln():
    """
    Parse the command line

    :returns: An object containing the command line arguments and options
    :rtype: argparse.Namespace
    """

    epilog = """Examples

Given an XCSV file with an ACDD-compliant extended header section, and a single column (at column 0) of data values:

# id: 1
# title: The title
depth (m)
0.575
1.125
2.225

Then the following invocation will plot the only column on the y-axis, with the x-axis the indices of the data points:

python3 -m xcsv.plot input.csv

If the file also contains a suitable variable for the x-axis:

# id: 1
# title: The title
time (year) [a],depth (m)
2012,0.575
2011,1.125
2010,2.225

then the columns to be used for the x- and y-axes can be specified thus:

python3 -m xcsv.plot -x 0 -y 1 input.csv
"""

    parser = argparse.ArgumentParser(description='plot the given XCSV files', epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter, prog='xcsv_plot')

    parser.add_argument('in_file', help='input XCSV file(s)', nargs='+')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x', '--x-idx', help='column index (zero-based) containing values for the x-axis', dest='xidx', default=None, type=int)
    group.add_argument('-X', '--x-column', help='column label containing values for the x-axis', dest='xcol', default=None, type=str)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-y', '--y-idx', help='column index (zero-based) containing values for the y-axis', dest='yidx', default=0, type=int)
    group.add_argument('-Y', '--y-column', help='column label containing values for the y-axis', dest='ycol', default=None, type=str)
 
    parser.add_argument('--x-label', help='text to be used for the plot x-axis label', dest='xlabel', default=None, type=str)
    parser.add_argument('--y-label', help='text to be used for the plot y-axis label', dest='ylabel', default=None, type=str)

    parser.add_argument('--invert-x-axis', help='invert the x-axis', dest='invert_xaxis', action='store_true', default=False)
    parser.add_argument('--invert-y-axis', help='invert the y-axis', dest='invert_yaxis', action='store_true', default=False)

    parser.add_argument('--title', help='text to be used for the plot title', dest='title', default=None, type=str)
    parser.add_argument('--caption', help='text to be used for the plot caption', dest='caption', default=None, type=str)
    parser.add_argument('--label-key', help='key of the header item in the extended header section whose value will be used for the plot legend label', dest='label_key', default=None, type=str)

    parser.add_argument('-s', '--figsize', help='size of the figure (width height)', dest='figsize', nargs=2, default=None, type=int)
    parser.add_argument('-b', '--background-image', help='path to an image to show in the background of the plot', dest='bg_img_path', default=None, type=str)

    parser.add_argument('-o', '--out-file', help='output plot file')

    parser.add_argument('-P', '--plot-options', help="options for the plot, specified as a simple JSON object", dest='plot_opts', default={}, type=json.loads)
    parser.add_argument('-S', '--scatter-plot', help="set plot options (see -P) to produce a scatter plot", dest='plot_opts', action='store_const', const={'marker': '.', 'ls': ''})

    parser.add_argument('-V', '--version', action='version', version=f"%(prog)s {xp.__version__}")

    args = parser.parse_args()

    return args

def main():
    """
    Main function
    """

    args = parse_cmdln()
    datasets = get_datasets(args.in_file)
    plotter = xp.Plot()

    if args.figsize:
        plotter.setup_figure_and_axes(figsize=args.figsize)

    plotter.plot_datasets(datasets, xidx=args.xidx, yidx=args.yidx, xcol=args.xcol, ycol=args.ycol, xlabel=args.xlabel, ylabel=args.ylabel, title=args.title, caption=args.caption, label_key=args.label_key, invert_xaxis=args.invert_xaxis, invert_yaxis=args.invert_yaxis, show=False, opts=args.plot_opts)

    if args.bg_img_path:
        plotter.add_plot_bg(img_path=args.bg_img_path)

    if args.out_file:
        plotter.savefig(args.out_file)
    else:
        plotter.show()

if __name__ == '__main__':
    main()

