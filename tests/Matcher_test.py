from nose.tools import *
import ATMA
import numpy

class testcase:

    def setup(self):
        TList=[]
        for i in range(7):
            newToken=ATMA.GapClosing.DataStructures.Token()
            TList.append( newToken )

        for t in range(len(TList)):
            TList[t].ID=t

        EList=[]
        for i in range(7):
            newEndPoint=ATMA.GapClosing.DataStructures.EndPoint()
            newEndPoint.Thickness=i
            newEndPoint.Token=TList[i]
            EList.append( newEndPoint )

        EList[0].Position, EList[0].Orientation, = [0,0,0], [0,0, 1]
        EList[1].Position, EList[1].Orientation, = [0,0,3], [0,0,-1]
        EList[2].Position, EList[2].Orientation, = [0,1,1], [0,0, 1]
        EList[3].Position, EList[3].Orientation, = [0,1,4], [0,0,-1]
        EList[4].Position, EList[4].Orientation, = [0,3,2], [0,0,-1]
        EList[5].Position, EList[5].Orientation, = [0,4,4], [0,0, 1]
        EList[6].Position, EList[6].Orientation, = [0,6,0], [0,0, 1]

        self.t=ATMA.GapClosing.Matcher(EList)


    def test_empty(self):
        EList=[]
        t=ATMA.GapClosing.Matcher(EList)
        t.run()
        assert t.EList_Matching==[]


    def test_calcCostMatrix(self):
        # check if costmarix does not exist
        assert self.t.costMatrix==None

        # run algorithm
        self.t._calcCostMatrix()

        # check if costmatrix exist
        assert self.t.costMatrix!=None
        #assert self.t.costMatrix.shape==(4,3)


    def test_solveASP(self):

         # run algorithm
        self.t._calcCostMatrix()
        self.t._solveASP()

        # check if matching list has proper length and elements are different
        assert len(self.t.EList_Matching)!=0
        for e1,e2 in self.t.EList_Matching:
            assert e1!=e2


    def test_basic(self):
        self.t.run()
        res = self.t.EList_Matching

        assert res[0][0].Token.ID == 0 and res[0][1].Token.ID == 1
        assert res[1][0].Token.ID == 2 and res[1][1].Token.ID == 3
        assert res[2][0].Token.ID == 6 and res[2][1].Token.ID == 4


    def test_large(self):
        EList=[]
        for i in range(100):
            x1,x2,x3 = numpy.random.rand(1,3)[0]
            o1,o2,o3 = 2*numpy.random.rand(1,3)[0]-1

            newEndPoint = ATMA.GapClosing.DataStructures.EndPoint()
            newEndPoint.Position = [x1,x2,x3]
            newEndPoint.Orientation = [o1,o2,o3]

            EList.append( newEndPoint )

        t=ATMA.GapClosing.Matcher(EList)
        #t.maxDist=0.5
        t.run()
        A=len(t.EList_Matching)

        t.maxDist=0.2
        t.run()
        B=len(t.EList_Matching)

        assert A>B
