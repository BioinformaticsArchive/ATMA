import unittest
from ATMA.GapClosing.DataStructures import UnionFinder

class testcase(unittest.TestCase):

    def test_UnionFinder_NoData(self):

        L0=None

        a=UnionFinder(L0)
        a.calcGroupIDs()

        assert a.GroupIDs == None


    def test_UnionFinder1(self):

        L1=[    [1,2],\
                [2,3],\
                [5,6],\
                [6,7],\
                [7,8]  ]

        a=UnionFinder(L1)
        a.calcGroupIDs()

        assert a.GroupIDs[7] == 5
        assert a.GroupIDs[1] == 1


    def test_UnionFinder2(self):

        L2=[    [1,1],\
                [2,2],\
                [2,1],\
                [3,8],\
                [5,6]  ]

        a=UnionFinder(L2)
        a.calcGroupIDs()

        assert a.GroupIDs[1],2
        assert a.GroupIDs[8],3
        assert a.GroupIDs[6],5


    def test_UnionFinder3(self):

        L3=[[1,1]]

        a=UnionFinder(L3)
        a.calcGroupIDs()

        assert a.GroupIDs[1],1


if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
