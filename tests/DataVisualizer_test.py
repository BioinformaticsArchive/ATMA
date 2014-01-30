from nose.tools import *
import ATMA
import numpy
from mayavi import mlab

class testcase:

    def test_empty(self):

        data=numpy.zeros((20,20,20))

        mlab.figure( bgcolor=(0,0,0), size=(1000,845) )
        ATMA.GUI.DataVisualizer.segmentation( data )
        mlab.close()

    def test_three_lines(self):

        data=numpy.zeros((200,200,160))
        data[50,50,:]=1
        data[150,150,:]=2
        data[50,150,:]=3

        mlab.figure( bgcolor=(0,0,0), size=(1000,845) )
        ATMA.GUI.DataVisualizer.segmentation( data )
        mlab.close()

    def test_rawData(self):

        raw=numpy.uint32(numpy.random.rand(200,200,200)*255)

        mlab.figure( bgcolor=(0,0,0), size=(1000,845) )
        ATMA.GUI.DataVisualizer.rawSlider( raw )
        mlab.close()


    def test_full(self):

        data=numpy.zeros((200,200,160))
        data[50:70,50:70,:]=1
        data[150:170,150:200,:]=2
        data[50:60,10:60,:]=3

        raw=numpy.uint32(numpy.random.rand(200,200,200)*255)

        mlab.figure( bgcolor=(0,0,0), size=(1000,845) )
        ATMA.GUI.DataVisualizer.segmentation( data )
        ATMA.GUI.DataVisualizer.rawSlider( raw )
        mlab.close(all=True)
