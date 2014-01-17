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
