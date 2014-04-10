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


def ilp(costMatrix):

    #Invalid_Connections : -1
    if costMatrix.shape==(0,0):
        return []

    tmpMatrix = numpy.copy(costMatrix)
    binMatrix = numpy.zeros( tmpMatrix.shape,dtype=bool )


    dist_mat=numpy.copy(costMatrix)
    size_x   = dist_mat.shape[0]
    size_y   = dist_mat.shape[1]
    size_min = int(numpy.amin([size_x,size_y]))
    from gurobipy import Model, quicksum, GRB


    m=Model("mip1")
    COS,VAR={},{}

    for i in range(size_x):
        x_cos, x_var = [],[]
        for j in range(size_y):
            COS[i,j]=dist_mat[i,j]
            VAR[i,j]=m.addVar(vtype='B',name="["+str(i)+","+str(j)+"]")
    m.update()


    # Set objective
    m.setObjective( quicksum(\
            COS[x,y]*VAR[x,y]
            for x in range(size_x) \
            for y in range(size_y) \
            ),GRB.MINIMIZE)


    # Constrains HORIZONTAL
    for i in range(size_x):
        m.addConstr( quicksum\
                (VAR[i,y] for y in range(size_y)) <= 1)

    # Constrains VERTICAL
    for i in range(size_y):
        m.addConstr( quicksum\
                (VAR[x,i] for x in range(size_x)) <= 1)

    m.addConstr(quicksum(\
            VAR[x,y] for x in range(size_x) for y in range(size_y)) == int(size_min))

    m.setParam("OutputFlag",False)
    m.optimize()
    res=numpy.zeros(dist_mat.shape,dtype=bool)
    for i in range(size_x):
        for j in range(size_y):
            res[i,j]=VAR[i,j].x

    binMatrix[costMatrix==1]=0
    return binMatrix

