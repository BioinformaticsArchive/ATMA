import unittest
import h5py
import numpy
import vigra
from ATMA.Segmentation.BioData import Nerve
from ATMA.Segmentation.BioData import Cortex

vagus_data = h5py.File("./data/vagus001.h5")["volume/data"][:,:,:,0]
cortex_data = h5py.File("./data/cortex001.h5")["volume/data"][100:200,100:200,:40,0]

class testNerve(unittest.TestCase):

    def test_basic(self):
        n = Nerve( vagus_data )

        n.sigmaSmooth = 1
        n.thresMembra = 0.5
        n.sizeFilter = [20,1000]
        n.run()
        res = n.seg


        layer = res[:,:,50]
        assert( numpy.max(layer) == 1 )
        assert( numpy.min(layer) == 0 )

        components = vigra.analysis.labelImageWithBackground(vigra.Image(layer))
        assert( len(components) > 5 )

    def test_empty(self):
        n = Nerve( vagus_data )

        n.sigmaSmooth = 1
        n.thresMembra = 1
        n.sizeFilter = [20,1000]
        n.run()
        res = n.seg


        layer = res[:,:,50]
        assert( numpy.max(layer) == 0 )
        assert( numpy.min(layer) == 0 )

    def test_full(self):
        n = Nerve( vagus_data )


        n.sigmaSmooth = 0.7
        n.thresMembra = 0.7
        n.sizeFilter = [20,2000]
        n.run()
        res = n.seg

        layer = res[:,:,50]
        assert( numpy.max(layer) == 1 )
        assert( numpy.min(layer) == 0 )

        n.sigmaSmooth = 0.7
        n.thresMembra = -1
        n.sizeFilter = [20,2000]
        n.run()
        res = n.seg

        layer = res[:,:,50]
        assert( numpy.max(layer) == 0 )
        assert( numpy.min(layer) == 0 )


        n.sigmaSmooth = 0.7
        n.thresMembra = 2
        n.sizeFilter = [20,10e10]
        n.run()
        res = n.seg

        layer = res[:,:,50]
        assert( numpy.max(layer) == 1 )
        assert( numpy.min(layer) == 1 )


class testCortex(unittest.TestCase):

    def test_basic(self):
        n = Cortex( cortex_data )

        n.run()
        res = n.seg
        assert( numpy.max(res) == 1 )
        assert( numpy.min(res) == 0 )

    def test_empty(self):
        n = Cortex(numpy.zeros((100,100,100)))
        n.run()
        res = n.seg
        assert( numpy.max(res) == 0 )
        assert( numpy.min(res) == 0 )

if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
