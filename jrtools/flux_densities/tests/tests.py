from unittest import TestCase

from jrtools import flux_densities as fd

class TestFluxDensities(TestCase):

    def test_souurce_list(self):
        source_list = fd.get_sources()
        assert(len(source_list) == 20)


