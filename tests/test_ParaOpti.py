import unittest
from ATMA.ParaOpti import Score 
from ATMA.CLT import CLT
import numpy
import h5py

#Create Data
class testcase:

    def stest_simple(self):

        a=CLT()
        a.path_in = ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/pores1.h5","data"]
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]

        
        s = Scorej()
        s.res = res
        assert p.scoreTracer() > 10

    def test_lowScore(self):

        a=CLT()
        a.path_in = ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/pores2.h5","data"]
        a.sigmaSmooth = 0.7
        a.thresMembra = 1
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]

        
        s = Score()
        s.res = res
        assert s.scoreTracer() == 0

    def test_large(self):
        pass


if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
