from nose.tools import *
import ATMA
import h5py
import numpy


class testcase:

    def setup(self):

        self.f=h5py.File("./tests/data/Volume001.h5")["volume/data"]


    def test_full(self):

        a=ATMA.Segmentation.BioData.Nerve(self.f)
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        seg = a.seg

        # check if there are components
        assert numpy.sum(seg==0)!=0
        assert numpy.sum(seg==1)!=0

        # compute tokens end endpoints from the segmented data
        b=ATMA.GapClosing.Tokenizer.Data2Token(seg)
        b.run()
        EList = b.EList
        TList = b.TList

        # Check if endpoints could be found
        assert len(EList)>10

        # metch endpoints and compute gaps
        c=ATMA.GapClosing.Connector.GapFinder(EList)
        c.run()
        GList = c.GList

        # from gaplist, compute token unions
        d=ATMA.GapClosing.Connector.TokenRemap( GList )
        d.run()

        # use tokens to reconstruct origin segmentation data
        d=ATMA.GapClosing.Tokenizer.Token2Data(TList,seg.shape)
        d.run()
        res=d.data

        '''
        from mayavi import mlab
        mlab.figure( bgcolor=(0,0,0), size=(1000,845) )
        ATMA.GUI.DataVisualizer.segmentation( res )
        ATMA.GUI.DataVisualizer.rawSlider( self.f[:,:,:,0] )
        mlab.show()
        '''

        assert len(numpy.unique(res))<30 # no more than 30 axons
        assert len(numpy.unique(res))>15 # at least 15 axons
        assert len(TList)>30             # more than 30 tokens
        assert len(EList)==2*len(TList)  # every token has two endings
        assert len(GList)>12             # more than 12 discontinuities


    def test_CLT_basic(self):
        a=ATMA.CLT()
        a.predictionData = self.f
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res

        assert len(numpy.unique(res))<30 # no more than 30 axons
        assert len(numpy.unique(res))>15 # at least 15 axons


    def test_CLT_empty1(self):
        a=ATMA.CLT()
        a.predictionData= self.f
        a.sigmaSmooth = 1
        a.thresMembra = 2
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res

        # result is empty volume because th is to high
        assert numpy.all(res==0)


    def test_CLT_empty2(self):
        a=ATMA.CLT()
        a.predictionData= self.f
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [10e5,10e6]
        a.run()
        res = a.res

        # result is empty volume because size filter is abnormal
        assert numpy.all(res==0)


    def test_CLT_empty3(self):
        a=ATMA.CLT()
        a.predictionData= self.f
        a.sigmaSmooth = 0.7
        a.thresMembra = -1
        a.sizeFilter = [0,10e10]
        a.run()
        res = a.res

        # result is empty volume because everything was one large component
        # (th<0), so the volume must be invalid
        assert numpy.all(res==0)


    def test_compareMethods(self):

        a=ATMA.Segmentation.BioData.Nerve(self.f)
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        seg = a.seg

        # check if there are components
        assert numpy.sum(seg==0)!=0
        assert numpy.sum(seg==1)!=0

        # compute tokens end endpoints from the segmented data
        b=ATMA.GapClosing.Tokenizer.Data2Token(seg)
        b.run()
        EList = b.EList
        TList = b.TList

        # Check if endpoints could be found
        assert len(EList)>10

        # metch endpoints and compute gaps
        c=ATMA.GapClosing.Connector.GapFinder(EList)
        c.run()
        GList = c.GList

        # from gaplist, compute token unions
        d=ATMA.GapClosing.Connector.TokenRemap( GList )
        d.run()

        # use tokens to reconstruct origin segmentation data
        d=ATMA.GapClosing.Tokenizer.Token2Data(TList,seg.shape)
        d.run()
        res1=d.data

        A=ATMA.CLT()
        A.predictionData= self.f
        A.sigmaSmooth = 0.7
        A.thresMembra = 0.7
        A.sizeFilter = [20,1000]
        A.run()
        res2 = A.res

        assert numpy.all( res1 == res2 )


