"""Tests for the flux_densities module"""

from unittest import TestCase
from collections import namedtuple

from jrtools import flux_densities as fd


class TestFluxDensities(TestCase):
    """Test class for the flux_densities module"""

    @staticmethod
    def test_source_list():
        """Test get_sources"""
        source_list = fd.get_sources()
        assert len(source_list) == 20

    @staticmethod
    def test_get_jy():
        """Test get_jy"""
        flux = fd.get_jy('Cygnus A', 3.0)
        assert float('%.2f' % flux) == 668.55

    @staticmethod
    def test_coeffs():
        """Test get_source_coeffs"""
        result = fd.get_source_coeffs('Cygnus A')
        SourceCoeffs = namedtuple(
            'SourceCoeffs', 'name a0 a1 a2 a3 a4 a5 fit fmin fmax')
        expected_result = SourceCoeffs(name='Cygnus A', a0=3.3498, a1=-1.0022,
                                       a2=-0.225, a3=0.023, a4=0.043, a5=0.0,
                                       fit=1.9, fmin=0.05, fmax=12)
        assert result == expected_result
