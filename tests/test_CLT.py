import unittest
import ATMA
from ATMA.CLT import CLT
import h5py
import numpy


class testcase:


    def test_CLT_basic(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/vagus000.h5","volume/data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]

        assert len(numpy.unique(res))<30 # no more than 30 axons
        assert len(numpy.unique(res))>15 # at least 15 axons

    def test_CLT_empty1(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/vagus001.h5","volume/data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.sigmaSmooth = 1
        a.thresMembra = 2
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]

        # result is empty volume because th is to high
        assert numpy.all(res==0)


    def test_CLT_empty2(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/vagus002.h5","volume/data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [10e5,10e6]
        a.run()
        res = a.res[::]

        # result is empty volume because size filter is abnormal
        assert numpy.all(res==0)


    def test_CLT_empty3(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/vagus003.h5","volume/data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.sigmaSmooth = 0.7
        a.thresMembra = -1
        a.sizeFilter = [0,10e10]
        a.run()
        res = a.res[::]

        # result is empty volume because everything was one large component
        # (th<0), so the volume must be invalid
        assert numpy.all(res==0)


    def test_Block_basic(self):

        a=CLT()
        a.path_in = ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/vagus004.h5","volume/data"]
        a.Sub_Volume = [[0,100], [0,100], [0,17]]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]
        assert res.shape == (100,100,17)


if __name__ == "__main__":

    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
