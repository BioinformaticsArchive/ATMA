import unittest
import ATMA.BlockProcess
import numpy

data_0=numpy.zeros((0,0,0))
data_1=numpy.zeros((100,100,100))
data_2=numpy.zeros((100,100,100))
data_3=numpy.zeros((10,1,3))
data_4=numpy.zeros((107,101,103))

class testcase:
    pass

if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
