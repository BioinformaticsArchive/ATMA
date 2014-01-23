from nose.tools import *
import ATMA
import numpy

class Tokenizer_Test:

    def setup(self):
        d1=numpy.zeros((20,20,40))
        d1[1:3,1:3,1:3]=1
        d1[5:8,5:8,5:8]=1
        d1[15:18,15:18,15:18]=1
        d1[10:13,10:13,10:-10]=1
        self.t=ATMA.GapClosing.Tokenizer(d1)

        d2=numpy.zeros((20,20,20),dtype=numpy.uint8)
        d2[8:13,1,3:]=1

        d2[8:13,3:5,:]=1
        d2[8:13,3:5,10:12]=0

        d2[8:13,10:14,:]=1
        d2[8:13,10:14,8:12]=0
        d2[8:13,16:18,7:-7]=1
        self.t2=ATMA.GapClosing.Tokenizer(d2)
        self.d2=d2


    def test_empty(self):
        t=self.t
        assert len(t.TList)==0


    def test_basic(self):
        t=self.t
        t.minSize=0
        t.epHalo=1
        t.run()
        assert len(t.TList)==4
        assert len(t.TList)==len(t.EList)/2


    def test_advanced(self):
        t=self.t
        t.minSize=20
        t.epHalo=2
        t.run()
        assert len(t.TList)==3
        assert len(t.TList)==len(t.EList)/2


    def test_one_element(self):
        t=self.t
        t.minSize=20
        t.epHalo=4
        t.run()
        assert len(t.TList)==1
        assert len(t.TList)==len(t.EList)/2


    def test_one_element2(self):
        t=self.t
        t.minSize=4
        t.epHalo=6
        t.run()
        assert len(t.TList)==1
        assert len(t.TList)==len(t.EList)/2


    def test_large(self):
        self.t2.epHalo=1
        self.t2.run()
        for i in self.t2.EList:
            x,z,y=i.Position
            assert(self.d2[x,z,y]==1)
            self.d2[x,z,y]=2

        #Print results for debugging
        #print self.d2[10,:,:].T
