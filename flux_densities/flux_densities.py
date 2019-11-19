#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Determine flux densities of sources based on Perley and Butler, 2016.
Using the method defined in Perley and Butler, 2016:
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

import webbrowser

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
        namedtuple: the 10 coefficientsfor this source, otherwise None if the
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

def create_html(coeffs, html_filename):
    """ Create an html page for displaying the data in a graph. """

    data = []
    source_name = coeffs[0]

    for freq in _frange(0.06, 50, 0.005):
        freq_flux = [float("%.4f"%freq),
                     float("%.7f"%(get_jy(source_name, float(freq))))]
        data.append(freq_flux)

    f_out = open(html_filename, "w")
    with open("index.template") as f_template:
        for line in f_template:
            if "$source" in line:
                line = line.replace("$source", source_name)
            if "$data" in line:
                line = line.replace("$data", str(data))
            f_out.write(line.replace("\n", ""))
    f_out.close()



def main():
    """Execute main function."""

    parser = argparse.ArgumentParser(description='Using techniques \
            described in Perley and Butler, 2016: \
            https://arxiv.org/pdf/1609.05940.pdf, calculate the flux densities \
            of various sources from 1 to 10GHz')

    parser.add_argument('-l', '--list', action='store_true',
                        help='List all available sources')
    parser.add_argument('-f', '--flux', nargs='*', metavar=('freq', 'source'),
                        help='Get the flux in Jy by specifying the frequency \
                              in MHz and the source name.')
    parser.add_argument('-c', '--chart', nargs='*', metavar='source_name',
                        help='Create an HTML chart of a source\'s flux vs \
                              frequency')
    parser.add_argument('-b', '--browser', action='store_true',
                        help='If HTML file is create, show in a browser.')

    if len(sys.argv) == 1:
        # display help message when no args are passed.
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.list is True:
        for source in get_sources():
            print(source)

    if args.flux is not None:
        freq_mhz = float(args.flux[0])
        source_name = " ".join(args.flux[1:])
        flux_jy = get_jy(source_name, freq_mhz/1000.0)
        print("Flux of %s @ %0.2f MHz is %0.2f Jy" %
              (source_name, freq_mhz, flux_jy))

    if args.chart is not None:
        source_name = " ".join(args.chart)
        coeffs = get_source_coeffs(source_name)
        html_filename = source_name.replace(" ", "_").lower() + "_flux.html"
        create_html(coeffs, html_filename)
        print(html_filename)
        if args.browser is True:
            webbrowser.open("file://%s/%s"%(os.getcwd(), html_filename), 1)

if __name__ == '__main__':
    main()
