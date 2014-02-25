import unittest
import h5py
import numpy
import ATMA.Training

data_pre = h5py.File("./data/vagus001.h5")["volume/data"][::]
data_axon = h5py.File("./data/vagus001_res.h5")["data/axons"][::]
data_gap = h5py.File("./data/vagus001_res.h5")["data/gaps"][::]

class test_gapDetection:

    def test_simple(self):

        g = ATMA.Training.GapDetection()
        g.pred_volume = data_pre
        g.gaps = data_gap
        g.run()
        assert len(g.Features) == 16

if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
