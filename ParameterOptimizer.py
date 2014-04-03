import ATMA.CLT
from random import shuffle

import numpy

BestScore=[0,0,0]
para=[]
for s in  numpy.arange(0.2,0.3,0.01):
    for t in  numpy.arange(0.1,0.4,0.01):
        para.append((s,t))

shuffle(para)
iteration = 0
for s,t in para:
    iteration+=1

    print
    print str(iteration)+". run:",s,t,

    a=ATMA.CLT()
    a.path_in = ["/Data/suralis/pre.h5","volume/data"]
    a.path_out = ["/tmp/testss.h5","data"]
    a.Sub_Volume = [[600,950], [300,1000], [400,575]]
    a.blockSize = [175,175,175]
    a.helo = 15 
    a.sigmaSmooth = s
    a.thresMembra = t
    a.sizeFilter = [20,1000]
    a.run()
    res = a.res[::]
    score = a.getScore()

    print "     score:", score
    if BestScore[2]<score:
        BestScore=[s,t,score]
    print "best score:", BestScore
