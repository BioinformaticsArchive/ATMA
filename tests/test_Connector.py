import unittest
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

        self.t=ATMA.GapClosing.Connector.GapFinder(EList)


    def test_empty(self):
        EList=[]
        t=ATMA.GapClosing.Connector.GapFinder(EList)
        t.run()
        assert t.GList==[]


    def test_calcCostMatrix(self):
        # check if costmarix does not exist
        assert self.t.costMatrix==None

        # run algorithm
        self.t._calcCostMatrix()

        # check if costmatrix exist
        assert self.t.costMatrix!=None
        #assert self.t.costMatrix.shape==(4,3)


    def test_basic(self):

        self.t.run()
        GList = self.t.GList

        assert GList[0].Ep1.Token.ID == 0 and GList[0].Ep2.Token.ID == 1
        assert GList[1].Ep1.Token.ID == 2 and GList[1].Ep2.Token.ID == 3
        assert GList[2].Ep1.Token.ID == 6 and GList[2].Ep2.Token.ID == 4


    def test_large(self):
        EList=[]
        for i in range(100):
            x1,x2,x3 = numpy.random.rand(1,3)[0]
            o1,o2,o3 = 2*numpy.random.rand(1,3)[0]-1

            newEndPoint = ATMA.GapClosing.DataStructures.EndPoint()
            newEndPoint.Position = [x1,x2,x3]
            newEndPoint.Orientation = [o1,o2,o3]

            EList.append( newEndPoint )

        t=ATMA.GapClosing.Connector.GapFinder(EList)
        t.run()
        A=len(t.GList)

        t.maxDist=0.2
        t.run()
        B=len(t.GList)

if __name__ == "__main__":
    import nose
    nose.run(defaultTest=__file__, env={'NOSE_NOCAPTURE' : 1})
