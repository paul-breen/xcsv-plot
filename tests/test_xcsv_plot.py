import os

import pytest

import xcsv
import xcsv.plot as xp

base = os.path.dirname(__file__)

def test_version():
    assert xp.__version__ == '0.3.0'

@pytest.fixture
def short_test_datasets():
    in_files = [f'{base}/data/short-test-data-{n}.csv' for n in range(1, 4)]
    datasets = []

    for in_file in in_files:
        with xcsv.File(in_file) as f:
            datasets.append(f.read())

    return datasets

def test_get_plot_data_extent(short_test_datasets):
    p = xp.Plot()
    xcol, ycol = 'time (year) [a]', 'depth (m)'
    expected = [2010, 2012, 0.575, 6.725]
    actual = p.get_plot_data_extent(short_test_datasets, xcol, ycol)
    assert actual == expected

def test_get_plot_data_extent_no_xcol(short_test_datasets):
    p = xp.Plot()
    xcol, ycol = None, 'depth (m)'
    expected = [0, 2, 0.575, 6.725]
    actual = p.get_plot_data_extent(short_test_datasets, xcol, ycol)
    assert actual == expected

def test_plot_datasets(short_test_datasets):
    p = xp.Plot()

    # N.B.: Calling plot_datasets() is quite expensive as it generates a plot

    # The default is to take the first (zeroth) column for the y-axis
    p.plot_datasets(short_test_datasets, show=False)
    assert p.xcol == None
    assert p.ycol == 'time (year) [a]'

    p.plot_datasets(short_test_datasets, xidx=0, yidx=1, show=False)
    assert p.xcol == 'time (year) [a]'
    assert p.ycol == 'depth (m)'

    with pytest.raises(IndexError):
        p.plot_datasets(short_test_datasets, xidx=10, yidx=1, show=False)

    with pytest.raises(KeyError):
        p.plot_datasets(short_test_datasets, xcol='dummy', yidx=1, show=False)

