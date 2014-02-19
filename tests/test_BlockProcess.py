import unittest
from ATMA.BlockProcess import BlockProcess
import numpy
import h5py

data_1 = numpy.random.random_integers(99,size=(0,0,0))
data_2 = numpy.random.random_integers(99,size=(100,100,100))
data_3 = numpy.random.random_integers(99,size=(101,107,113))
data_5 = numpy.random.random_integers(99,size=(100,100,0))
data_4 = numpy.random.random_integers(99,size=(100,1,100))

def func(data):
    return 2*data

class testcase:

    def test_1_real(self):

        data_in  = h5py.File("./data/vagus001.h5")["volume/data"][:,:,:,0]
        f_out = h5py.File("./tmp.h5", "w")
        data_out = f_out.create_dataset("volume/data", (data_in.shape), dtype=float, compression="lzf")

        B = BlockProcess()
        B.data_in = data_in
        B.data_out = data_out
        B.Process = func
        B.run()
        

if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
