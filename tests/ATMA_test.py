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

        #layer = seg[:,:,50]
        #vigra.impex.writeImage(vigra.Image(layer),"/tmp/ooo.png")
        #vigra.impex.writeImage(vigra.Image(self.f[:,:,50,0]),"/tmp/oo1.png")

        b=ATMA.GapClosing.Tokenizer.Data2Token(seg)
        b.run()
        EList = b.EList

        # Check if token endpoints could be found
        assert len(EList)>10

        c=ATMA.GapClosing.Connector.GapFinder(EList)
        c.run()
        GList = c.run()


        ATMA.GapClosing.Tokenizer.Token2Data(GList,2)
        #for e in EList:
            #print e.Token.ID, e.Partner.Token.ID


