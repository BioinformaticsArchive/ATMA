from nose.tools import *
import ATMA
import h5py
import numpy
import vigra


class Nerve_Test:

    def setup(self):

        f=h5py.File("./tests/data/Volume001.h5")["volume/data"]
        self.n=ATMA.Segmentation.Nerve(f)


    def test_basic(self):

        self.n.sigmaSmooth = 1
        self.n.thresMembra = 0.5
        self.n.sizeFilter = [20,1000]
        self.n.run()
        res = self.n.seg


        layer = res[:,:,50]
        assert( numpy.max(layer) == 1 )
        assert( numpy.min(layer) == 0 )

        components = vigra.analysis.labelImageWithBackground(vigra.Image(layer))
        assert( len(components) > 5 )


    def test_empty(self):

        self.n.sigmaSmooth = 1
        self.n.thresMembra = 1
        self.n.sizeFilter = [20,1000]
        self.n.run()
        res = self.n.seg


        layer = res[:,:,50]
        assert( numpy.max(layer) == 0 )
        assert( numpy.min(layer) == 0 )


    def test_full(self):

        self.n.sigmaSmooth = 1
        self.n.thresMembra = -1
        self.n.sizeFilter = [20,10e10]
        self.n.run()
        res = self.n.seg


        layer = res[:,:,50]
        assert( numpy.max(layer) == 1 )
        assert( numpy.min(layer) == 1 )
