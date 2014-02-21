import unittest
from ATMA.ParaOpti import ParaOpti
from ATMA.CLT import CLT
import numpy
import h5py

#Create Data
class testcase:

    def test_simple(self):

        a=CLT()
        a.path_in = ["./data/vagus001.h5","volume/data"]
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]

        
        p = ParaOpti()
        p.res = res
        assert p.scoreVagus() > 10

    def test_lowScore(self):

        a=CLT()
        a.path_in = ["./data/vagus001.h5","volume/data"]
        a.sigmaSmooth = 0.7
        a.thresMembra = 1
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]

        
        p = ParaOpti()
        p.res = res
        assert p.scoreVagus() == 0


if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
