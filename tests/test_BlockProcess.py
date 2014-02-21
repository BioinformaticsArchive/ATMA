import unittest
from ATMA.BlockProcess import BlockProcess
import numpy
import h5py

def func(data):
    res = data[:,:,:,0]>0.5
    gaps = numpy.zeros(res.shape)
    return res, gaps

class testcase:

    def test_1_simple(self):
    
        B = BlockProcess()
        B.path_in  = ["./data/vagus001.h5","volume/data"]
        B.path_out = ["/tmp/res.h5","data"]
        B.Process = func 
        B.run()
        res_Block = h5py.File("/tmp/res.h5")["data/axons"][::]

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][::]
        res_Norm = func(data_in)[0]

        assert numpy.mean(res_Block!=0) == numpy.mean(res_Norm!=0)

    def test_2_8Blocks(self):
    
        B = BlockProcess()
        B.path_in  = ["./data/vagus001.h5","volume/data"]
        B.path_out = ["/tmp/res1.h5","data"]
        B.blockSize = [75, 75, 25]
        B.helo = 10
        B.Process = func 
        B.Workers=6
        B.run()
        res_Block = h5py.File("/tmp/res1.h5")["data/axons"][::]

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][::]
        res_Norm = func(data_in)[0]

        assert numpy.mean(res_Block!=0) == numpy.mean(res_Norm!=0)
        
    def test_4_oneBlock(self):
    
        B = BlockProcess()
        B.path_in  = ["./data/vagus001.h5","volume/data"]
        B.path_out = ["/tmp/res3.h5","data"]
        B.blockSize = [150, 150, 80]
        B.Process = func 
        B.run()
        res_Block = h5py.File("/tmp/res3.h5")["data/axons"][::]

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][::]
        res_Norm = func(data_in)[0]

        assert numpy.mean(res_Block!=0) == numpy.mean(res_Norm!=0)


if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
