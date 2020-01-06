#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Using the method defined in Perley and Butler, 2016:
https://arxiv.org/pdf/1609.05940.pdf calculate the flux densities of various
sources from 1 to 10GHz and optionally produce a graph that is automatically
displayed in a browser.

Author: Jon Richards, jrseti@gmail.com

Example:

    Provide usage examples here


"""

import os
import sys

import argparse
from collections import namedtuple
from math import log
import time

import quick_chart as qc

# log(S) = a0 + a1 log(νG) + a2[log(νG)]2 + a3[log(νG)]3 + · · ·

_COEFF_TABLE = [
    ('J0133-3629', 1.0440, -0.6620, -0.225, 0.0, 0.0, 0.0, 267.0, 0.20, 4),
    ('3C48', 1.3253, -0.7553, -0.1914, 0.0498, 0.0, 0.0, 3.1, 0.05, 50),
    ('Fornax A', 2.2180, -0.661, 0.0, 0.0, 0.0, 0.0, 17.0, 0.20, 0.5),
    ('3C123', 1.8017, -0.7884, -0.1035, -0.0248, 0.009, 0.0, 1.9, 0.05, 50),
    ('J0444-2809', 0.9710, -0.8940, -0.118, 0.0, 0.0, 0.0, 3.3, 0.20, 2.0),
    ('3C138', 1.0088, -0.4981, -0.155, -0.0100, 0.0220, 0.0, 1.5, 0.20, 50),
    ('Pictor A', 1.9380, -0.7470, -0.074, 0.0, 0.0, 0.0, 8.1, 0.20, 4.0),
    ('Taurus A', 2.9516, -0.217, -0.047, -0.067, 0.0, 0.0, 1.9, 0.05, 4.0),
    ('3C147', 1.4516, -0.6961, -0.201, 0.064, -0.046, 0.029, 2.2, 0.05, 50),
    ('3C196', 1.2872, -0.8530, -0.153, -0.0200, 0.0201, 0.0, 1.6, 0.05, 50),
    ('Hydra A', 1.7795, -0.9176, -0.084, -0.0139, 0.03, 0.0, 3.5, 0.05, 12),
    ('Virgo A', 2.4466, -0.8116, -0.048, 0.0, 0.0, 0.0, 2.0, 0.05, 3),
    ('3C286', 1.2481, -0.4507, -0.1798, 0.0357, 0.0, 0.0, 1.9, 0.05, 50),
    ('3C295', 1.4701, -0.7658, -0.278, -0.0347, 0.0399, 0.0, 1.6, 0.05, 50),
    ('Hercules A', 1.8298, -1.0247, -0.0951, 0.0, 0.0, 0.0, 2.3, 0.20, 12),
    ('3C353', 1.8627, -0.6938, -0.100, -0.0320, 0.0, 0.0, 2.2, 0.20, 4),
    ('3C380', 1.2320, -0.7910, 0.095, 0.0980, -0.18, -0.16, 2.9, 0.05, 50),
    ('Cygnus A', 3.3498, -1.0022, -0.225, 0.023, 0.043, 0.0, 1.9, 0.05, 12),
    ('3C444', 1.1064, -1.0050, -0.075, -0.0770, 0.0, 0.0, 5.7, 0.20, 12),
    ('Cassiopeia A', 3.3584, -0.7518, -0.035, -0.071, 0., 0.0, 2.1, 0.2, 4)
    ]

def get_sources():
    """ Retrieve the list of available sources.

    Returns:
        list: Names of the available sources.

    """
    sources = []
    for coeffs in _COEFF_TABLE:
        sources.append(coeffs[0])

    return sources

def get_source_coeffs(source_name):
    """Retrieve the coefficients for a source

    Args:
        source_name (String): The name of a source, nust be a source defined
            int tlist of sources.

    Returns:
        namedtuple: the 10 coefficients for this source, otherwise None if the
        source_name is invalid (not in the list).

    """
    SourceCoeffs = namedtuple('SourceCoeffs', 'name a0 a1 a2 a3 a4 a5 fit fmin fmax')

    for coeffs in _COEFF_TABLE:
        if coeffs[0].lower() == source_name.lower():
            return SourceCoeffs(coeffs[0], coeffs[1], coeffs[2],
                                coeffs[3], coeffs[4], coeffs[5],
                                coeffs[6], coeffs[7], coeffs[8], coeffs[9])

    return None

def get_jy(source, freq_ghz):

    """Calculate the flux for a source at a given frequency.

    Args:
        source (string): Source name as in the _COEFF_TABLE.
        freq_ghz (float): The frequncy in GHz.

    Returns:
        float: Flux density of this source at the provided frequency,
            otherwise none if the source_name is invalid.

    """

    coeffs = get_source_coeffs(source)

    if coeffs is None:
        return None

    # log(S) = a0 + a1 log(νG) + a2[log(νG)]2 + a3[log(νG)]3 + · · ·
    jy_pre = (coeffs.a0 +
              coeffs.a1 * log(freq_ghz, 10) +
              coeffs.a2 * pow(log(freq_ghz, 10), 2.0) +
              coeffs.a3 * pow(log(freq_ghz, 10), 3.0) +
              coeffs.a4 * pow(log(freq_ghz, 10), 4.0) +
              coeffs.a5 * pow(log(freq_ghz, 10), 5.0))

    return pow(10.0, jy_pre)

def _frange(start, stop, step):
    """ Generator that is a version of xrange that allows specifying a step.

    Args:
        start (float): The start position.
        stop (float): The position at which to end.
        Step (float): The incrementation.

    Returns:
        float: the value at each setp.

    """

    value = start
    while value <= stop:
        yield value
        value += step

def create_chart(sources, minx, maxx, y_axis_linear=False):
    """ Create a chart of the sources frequency vs Jy.

    Args:
        sources (list): a list the sources to include in the chart.
        minx (float): the X axis minimum. In GHz.
        maxx (float): the X axis maximum. In GHz.
        y_axis_linear (bool): if True the Y axis will be linear.
            Defaults to False (logarithmic).

    Returns:
        (Chart): the newly created Charts instance.
    
    """

    data = [];
    for source in sources:
        source_data = []
        for freq in _frange(minx, maxx, 0.01):
            freq_flux = [float("%.4f"%freq),
                         float("%.7f"%(get_jy(source, float(freq))))]
            source_data.append(freq_flux)
        data.append((source, source_data))

    chart = qc.Chart()
    if len(sources) == 1:
        chart.set_title(sources[0])
    else:
        chart.set_title('Multiple Sources')
    chart.set_subtitle('Based on Perley and Butler, 2016: https://arxiv.org/pdf/1609.05940.pdf')
    chart.set_xaxis('logarithmic', 'Frequency in GHz')
    if y_axis_linear is True:
        chart.set_yaxis('linear', 'Jy')
    else:
        chart.set_yaxis('logarithmic', 'Jy')

    if len(sources) == 1:
        chart.set_tooltip({
                'crosshairs' : 'true',
                'shared' : 'true',
                'headerFormat' : '{point.x:.3f} GHz<br>',
                'pointFormat' : '{point.y:.1f} Jy<br>',
            })
    else:
        chart.set_tooltip({
                'crosshairs' : 'true',
                'shared' : 'true',
                'headerFormat' : '<b>[Multiple Sources] {point.key:.2f}</b> GHz: <br>',
                'pointFormat' : '<b>{series.name}:</b> {point.y:.1f} Jy<br>',
            })

    chart.set_width(800)
    chart.set_height(500)
    marker = {'marker': {'symbol': 'circle', 'radius': 0}}

    for source_data in data:
        series = qc.Series(source_data[0], source_data[1], marker)
        chart.add_series(series)

    return chart

def main():
    """Execute main function."""

    parser = argparse.ArgumentParser(description='Using techniques \
            described in Perley and Butler, 2016: \
            https://arxiv.org/pdf/1609.05940.pdf, calculate the flux densities \
            of various sources from 1 to 10GHz')

    parser.add_argument('source', nargs='*',
                        help='Name of a source. If the --chart option is \
                        specified this can be a comma separated list of \
                        source, enclosed in quotes.')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all available sources')
    parser.add_argument('-f', '--flux', type=float,
                        help='get the flux in Jy for a frequency specified in MHz.')
    parser.add_argument('-c', '--chart', action='store_true',
                        help='create an HTML chart of a source\'s flux vs frequency. \
                              Specify a source of "all" to chart all sources')
    parser.add_argument('-linear', '--linear', action='store_true',
                        help='if creating a chart the Y axis is to be drawn linear. \
                              Default is logarithmic.')
    parser.add_argument('-minf', '--minf', type=float, default=1.0,
                        help='min frequency in GHz. Defaults to 1GHz')
    parser.add_argument('-maxf', '--maxf', type=float, default=20.0,
                        help='max frequency in GHz. Defaults to 20GHz')
    parser.add_argument('-html', '--html', type=str, default=None,
                        help='if creating a chart this is the name of the html \
                              file to create. Defaults to using a system \
                              dependent temportary file that is deleted after \
                              displying in a browser.')
    parser.add_argument('-b', '--browser', action='store_true',
                        help='if HTML file is created, show in a browser.')
    parser.add_argument('-tb', '--typebrowser', type=str, default=None,
                        help='specify the browser type to display the chart. \
                             Useful for testing in various browser types. \
                             Valid types: chrome, safari, firefox.')

    # display help message when no args are passed.
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Construct the source name. args.source will be a list and
    # the true list of sources is constructed.
    sources = " ".join(args.source).split(',')

    # If the the first source is "all", use all available sources.
    if sources[0].upper() == 'ALL':
        sources = get_sources()

    # If the source is not defined, check the source name is valid.
    # Exit if the name is not valid. Print out all valid source names.
    sources_lowercase = [source.lower() for source in get_sources()]
    for source in sources:
        if source.lower() not in sources_lowercase:
            print("Error: %s is not a valid source name. Valid names are:"%source)
            for source in get_sources():
                print(source)
            sys.exit(0)

    # Optionally list all the sources then exit.
    if args.list is True:
        for source in get_sources():
            print(source)
        sys.exit(0)

    # Optionally calculate the flux at frequency, then exit.
    if args.flux is not None:
        for source in sources:
            freq_mhz = args.flux
            flux_jy = get_jy(source, freq_mhz/1000.0)
            print("Flux of %s @ %0.2f MHz is %0.2f Jy" %
                (source, freq_mhz, flux_jy))
        sys.exit(0)

    if args.chart is None:
        return

    # Create a chart of the one source specified by the user.
    #html_filename = source_name.replace(" ", "_").lower() + "_flux.html"
    """
    html_filename = args.html
    if html_filename is None:
        temporary_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w')
        html_filename = temporary_file.name
    """
    chart = create_chart(sources, args.minf, args.maxf, args.linear)
    page = qc.Page('Chart Test', 'Flux Densities')
    page.add_chart(chart)
    page.display_in_browser(args.html, args.typebrowser)
    """
    print('HTML file is %s'%html_filename)
    if args.browser is True:
        if args.html is None:
            webbrowser.get(args.typebrowser).open("file://%s"%html_filename, 1)
            #webbrowser.open("file://%s"%html_filename, 1)
            print('Sleeping 5 seconds to allow browser to render the chart...')
            time.sleep(5)
            os.unlink(html_filename)
            print('%s deleted. Bye!'%html_filename)
        else:
            webbrowser.open("file:%s"%os.path.join(os.getcwd(), html_filename), 1)
            print('HTML file fullpath: %s, Bye!'%os.path.join(os.getcwd(), html_filename))
    """

if __name__ == '__main__':
    main()
