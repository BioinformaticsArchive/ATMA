import unittest
from ATMA.BlockProcess0 import BlockProcess
import numpy
import h5py

def func(data):
    return data[:,:,:,0]>0.5

class testcase:

    def test_1_oneBlock(self):
    
        B = BlockProcess()
        B.path_in  = ["./data/vagus001.h5","volume/data"]
        B.path_out = ["/tmp/res.h5","volume/data"]
        B.blockSize = [100, 100, 50]
        B.helo = 50
        B.Process = func 
        B.Workers=6
        B.StoreAll=1
        B.run()
        res_Block = B.res[::]

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][::]
        res_Norm = func(data_in)

        assert numpy.mean(res_Block!=0) == numpy.mean(res_Norm!=0)

    def test_2_8Blocks(self):
    
        B = BlockProcess()
        B.path_in  = ["./data/vagus001.h5","volume/data"]
        B.path_out = ["/tmp/res1.h5","volume/data"]
        B.blockSize = [75, 75, 25]
        B.helo = 10
        B.Process = func 
        B.Workers=6
        B.StoreAll=1
        B.run()
        res_Block = B.res[::]

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][::]
        res_Norm = func(data_in)

        assert numpy.mean(res_Block!=0) == numpy.mean(res_Norm!=0)
        
    def test_3_0Helo(self):
    
        B = BlockProcess()
        B.path_in  = ["./data/vagus001.h5","volume/data"]
        B.path_out = ["/tmp/res2.h5","volume/data"]
        B.blockSize = [107, 59, 66]
        B.helo = 10
        B.Process = func 
        B.Workers=6
        B.StoreAll=1
        B.run()
        res_Block = B.res[::]

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][::]
        res_Norm = func(data_in)

        assert numpy.mean(res_Block!=0) == numpy.mean(res_Norm!=0)
        

if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
