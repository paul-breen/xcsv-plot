# xcsv-plot

xcsv-plot is a subpackage of [xcsv](https://github.com/paul-breen/xcsv).  It's main purpose is to provide a simple CLI for plotting extended CSV (XCSV) files.

## Install

The package can be installed from PyPI:

```bash
$ pip install xcsv-plot
```

## Using the package

XCSV data can be plotted directly, as the data table is a `pandas` table:

```python
content.data.plot(x='time (year) [a]', y='depth (m)')
```

and of course for more control over the plot, the data can be plotted using `matplotlib`, say.

But an XCSV file with an [ACDD-compliant](https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3) extended header section, and well-annotated column-headers, already provides much of the text needed to make an informative plot, so we can just plot the XCSV file directly from the command line.  This is the purpose of the `xcsv-plot` subpackage.  For example:

```bash
$ python3 -m xcsv.plot -x 0 -y 1 example.csv
```

Note here that we're calling `xcsv-plot` as a *module main*.  As a convenience, this invocation is wrapped as a console script when installing the package, hence the following invocation is equivalent:

```bash
$ xcsv_plot -x 0 -y 1 example.csv
```

In addition to using the CLI, the package can be used as a Python library.  The main class is `Plot` which provides methods to plot a given list of datasets (XCSV objects):

```python
import xcsv
import xcsv.plot as xp

filenames = ['example1.csv','example2.csv','example3.csv']
datasets = []

for filename in filenames:
    with xcsv.File(filename) as f:
        datasets.append(f.read())

plotter = xp.Plot()
plotter.plot_datasets(datasets, xidx=0, yidx=1)
```

## Command line usage

Calling the script with the `--help` option will show the following usage:

```bash
$ python3 -m xcsv.plot --help
usage: xcsv_plot [-h] [-x XIDX | -X XCOL] [-y YIDX | -Y YCOL]
                 [--x-label XLABEL] [--y-label YLABEL] [--invert-x-axis]
                 [--invert-y-axis] [--title TITLE] [--caption CAPTION]
                 [--label-key LABEL_KEY] [-s FIGSIZE FIGSIZE] [-b BG_IMG_PATH]
                 [-o OUT_FILE] [-P PLOT_OPTS] [-S] [-V]
                 in_file [in_file ...]

plot the given XCSV files

positional arguments:
  in_file               input XCSV file(s)

optional arguments:
  -h, --help            show this help message and exit
  -x XIDX, --x-idx XIDX
                        column index (zero-based) containing values for the
                        x-axis
  -X XCOL, --x-column XCOL
                        column label containing values for the x-axis
  -y YIDX, --y-idx YIDX
                        column index (zero-based) containing values for the
                        y-axis
  -Y YCOL, --y-column YCOL
                        column label containing values for the y-axis
  --x-label XLABEL      text to be used for the plot x-axis label
  --y-label YLABEL      text to be used for the plot y-axis label
  --invert-x-axis       invert the x-axis
  --invert-y-axis       invert the y-axis
  --title TITLE         text to be used for the plot title
  --caption CAPTION     text to be used for the plot caption
  --label-key LABEL_KEY
                        key of the header item in the extended header section
                        whose value will be used for the plot legend label
  -s FIGSIZE FIGSIZE, --figsize FIGSIZE FIGSIZE
                        size of the figure (width height)
  -b BG_IMG_PATH, --background-image BG_IMG_PATH
                        path to an image to show in the background of the plot
  -o OUT_FILE, --out-file OUT_FILE
                        output plot file
  -P PLOT_OPTS, --plot-options PLOT_OPTS
                        options for the plot, specified as a simple JSON
                        object
  -S, --scatter-plot    set plot options (see -P) to produce a scatter plot
  -V, --version         show program's version number and exit

Examples

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
```

