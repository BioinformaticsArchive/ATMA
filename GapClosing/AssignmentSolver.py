import numpy
import sys
from munkres import Munkres

def makeSquareWithNegValues(matrix):
    s = numpy.max(matrix.shape)
    res = -numpy.ones((s,s))
    res[:matrix.shape[0],:matrix.shape[1]]=matrix
    return res

def hun(costMatrix):

    # Check first, if costmatrix is not empty
    if costMatrix.shape==(0,0):
        return []

    # Create squared temporary matrix
    tmpMatrix = numpy.copy(costMatrix)
    tmpMatrix = makeSquareWithNegValues(tmpMatrix)
    sqCostMatrix = numpy.copy(tmpMatrix)
    sqCostMatrix[tmpMatrix==-1]=10e10

    # Solve ASP on the temporary matrix
    m=Munkres()
    i=m.compute(sqCostMatrix)


    # Create resultin matrix that contains ones at matching
    # objects and remove all excluded matches
    binMatrix = numpy.zeros( tmpMatrix.shape,dtype=bool )
    for x,y in i:
        if tmpMatrix[x,y]==-1:
            continue
        binMatrix[x,y]=True

    return binMatrix
