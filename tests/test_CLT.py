import unittest
import ATMA
from ATMA.CLT import CLT
import h5py
import numpy


class testcase:
    
    def test_CLT_basic(self):

        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/test.h5","data"]
        a.Sub_Volume = [[0,50],[0,50],[0,50]]
        a.blockSize = [25,25,25]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]

        #test if executing twice does not fail
        a.run()
        a.run()


    def test_CLT_basic(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/test.h5","data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        
        res = a.res[::]
        gaps = a.gaps[::]
        score = a.getScore()

        assert score>5 # mote than 5 start in the first 10 and end in the last 10 layer
        assert numpy.sum(gaps!=0)>10 # there should be at least 10 gaps 
        assert len(numpy.unique(res))<30 # no more than 30 axons
        assert len(numpy.unique(res))>15 # at least 15 axons

    def test_CLT_empty1(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/test.h5","data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = 2
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]
        score = a.getScore()

        # result is empty volume because th is to high
        assert score == 0
        assert numpy.all(res==0)

    def test_CLT_empty2(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/test.h5","data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [10e5,10e6]
        a.run()
        res = a.res[::]
        score = a.getScore()

        # result is empty volume because size filter is abnormal
        assert score == 0
        assert numpy.all(res==0)

    def test_CLT_empty3(self):
        a=CLT()
        a.path_in= ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/test.h5","data"]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = -1
        a.sizeFilter = [0,10e10]
        a.run()
        res = a.res[::]
        score = a.getScore()

        # result is empty volume because everything was one large component
        # (th<0), so the volume must be invalid
        assert score == 0
        assert numpy.all(res==0)

    def test_Block_basic(self):
        a=CLT()
        a.path_in = ["./data/vagus001.h5","volume/data"]
        a.path_out = ["/tmp/test.h5","data"]
        a.Sub_Volume = [[0,100], [0,100], [0,17]]
        a.blockSize = [50,50,50]
        a.helo = 10
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res[::]
        score = a.getScore()


        assert res.shape == (100,100,17)


if __name__ == "__main__":

    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
