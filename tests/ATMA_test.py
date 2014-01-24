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


        # use tokens to reconstruct origin segmentation data
        d=ATMA.GapClosing.Tokenizer.Token2Data(TList,seg.shape)
        d.run()
        res=d.data!=0

        # Check if most of the tokens could be reconstruct
        # (except of the small ones )
        assert numpy.sum(res!=seg)/float(numpy.sum(res==seg))<0.01

