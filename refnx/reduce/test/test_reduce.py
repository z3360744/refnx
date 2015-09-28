import unittest
import refnx.reduce.platypusnexus as pn
import numpy as np
import os
from refnx.reduce.reduce import reduce_stitch_files, ReducePlatypus
from numpy.testing import (assert_almost_equal, assert_, assert_equal,
                           assert_array_less)


class TestPlatypusNexus(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(__file__)
        self.path = path

        return 0

    def test_smoke(self):
        # a quick smoke test to check that the reduction can occur
        a = reduce_stitch_files([708, 709, 710], [711, 711, 711],
                                rebin_percent=2)
        a.save('test1.dat')

    def test_event_reduction(self):
        # check that eventmode reduction can occur, and that there are the
        # correct number of datasets produced.
        a = ReducePlatypus('PLP0011641.nx.hdf', 'PLP0011613.nx.hdf',
                           rebin_percent=2, eventmode=[0, 900, 1800],
                           integrate=0)
        assert_equal(a.ydata.shape[0], 2)


if __name__ == '__main__':
    unittest.main()