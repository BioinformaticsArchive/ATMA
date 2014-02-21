from ATMA.CLT import CLT
from ATMA.ParaOpti import ParaOpti

a=CLT()
a.path_in = ["/Data/vagus/data/pre.h5","volume/data"]
a.path_out = ["/Data/vagus/res_test.h5","data"]
#a.Sub_Volume = [[0,3750], [0,3750], [0,1000]]
a.Sub_Volume = [[2000,2200], [2000,2200], [0,100]]
#a.blockSize = [250,250,100]
a.blockSize = [100,100,50]
a.helo = 20
a.sigmaSmooth = 0.7
a.thresMembra = 0.7
a.sizeFilter = [20,1000]
a.verbose = 0
a.Workers = 8
a.run()
res = a.res
gap = a.gaps

import numpy
gapL=[]
labL=[]
for z in range(gap.shape[2]):
    pos=numpy.argwhere(gap[:,:,z])
    if len(pos)!=0:
        for p in pos:
            [x,y] = p
            gapL.append([x,y,z])
            labL.append(0)


#   To do!
#   Calc Features for all!

current = range(9)
for i in current:
    x,y,z = gapL[i]
    print x,y,z, labL[i]

#run label tool




#p = ParaOpti()
#p.res = ["/Data/vagus/res_test.h5","volume/data"]
#print p.scoreVagus()
