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


    def test_CLT(self):
        a=ATMA.CLT()
        a.h5File = self.f
        a.sigmaSmooth = 0.7
        a.thresMembra = 0.7
        a.sizeFilter = [20,1000]
        a.run()
        res = a.res

        assert len(numpy.unique(res))<30 # no more than 30 axons
        assert len(numpy.unique(res))>15 # at least 15 axons


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
        A.h5File = self.f
        A.sigmaSmooth = 0.7
        A.thresMembra = 0.7
        A.sizeFilter = [20,1000]
        A.run()
        res2 = A.res

        assert numpy.all( res1 == res2 )


