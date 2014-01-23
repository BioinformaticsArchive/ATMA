import numpy
import DataStructures
import AssignmentSolver

class Connector():
    """
    This class is used to find the metching endpoints of the axons.
    Therefore it uses the EndPoint datastructure from the tokenizer class.
    The User can set a method for:
        a) cost function
        b) assignment solver
    The result is a double list containing all endpointpartners:
        [[e1,e2],[e5,e8]...]
    """

    costMatrix = None
    method = "dist"     # cost function method
    solver = "hun"      # assignment solver method
    maxDist = 4         # maximal allowed distance of endoint partners for assignment problem
    maxOrie = 0.75      # maximal allowes orientation shift of endpoint partners

    def __init__(self,EList):

        # Split List in order to formulate Assignment problem
        self.EList_1 = [] # Axon starting points (jobs)
        self.EList_2 = [] # Axon ending points (workers)
        for e in EList:
            if e.Orientation[2]>0:
                self.EList_1.append(e)
            else:
                self.EList_2.append(e)


    def _calcCostMatrix(self):

        S1=len(self.EList_1)
        S2=len(self.EList_2)
        self.costMatrix=numpy.zeros((S1,S2))

        for (i,j),v in numpy.ndenumerate(self.costMatrix):
            ep1=self.EList_1[i]
            ep2=self.EList_2[j]
            v=self._costFunction(ep1,ep2,self.method)
            self.costMatrix[i,j]=v


    def _costFunction(self,ep1,ep2,method):

        # Endpoint Atribute (1)
        x1 = numpy.array(ep1.Position,dtype=numpy.float16)
        o1 = numpy.array(ep1.Orientation,dtype=numpy.float16)
        t1 = numpy.float16(ep1.Thickness)

        # Endpoint Atribute (2)
        x2 = numpy.array(ep2.Position,dtype=numpy.float16)
        o2 = numpy.array(ep2.Orientation,dtype=numpy.float16)
        t2 = numpy.float16(ep2.Thickness)

        # Pair Features
        c = (x1+x2)/2                           # centre
        d = numpy.linalg.norm(x1-x2)            # distance
        k1= (x1-c) / numpy.linalg.norm(x1-c)    # vector pointing to center (1)
        k2= (x2-c) / numpy.linalg.norm(x2-c)    # vector pointing to center (2)

        # Meassure if orientation of endpoints is alligned [0: <- -> , 1: -> <-]
        A=1-(2+numpy.dot(k1,o1)+numpy.dot(k2,o2))/4   #[0,1]

        if d>=self.maxDist:return -1
        if A<self.maxOrie:return -1

        if method == "dist":
            return d


    def _solveASP(self):

        self.EList_Matching=[]
        binMatrix=AssignmentSolver.hun(self.costMatrix)
        for x,y in numpy.argwhere(binMatrix):
            ep1=self.EList_1[x]
            ep2=self.EList_2[y]
            self.EList_Matching.append([ep1,ep2])


    def run(self):
        self._calcCostMatrix()
        self._solveASP()
        return self.EList_Matching
