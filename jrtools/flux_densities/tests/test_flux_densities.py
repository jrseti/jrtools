import pytest

from jrtools import flux_densities as fd

def test_souurce_list():
    print("HELLO2\n")
    source_list = fd.get_sources()
    assert(len(source_list) == 20)


