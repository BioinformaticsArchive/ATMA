import ATMA.CLT
from scipy.optimize import minimize

import numpy
def sigmoid(X):
    '''Compute the sigmoid function '''
    X = numpy.array(X)

    den = 1.0 + numpy.e ** (-1.0 * X)
    d = 1.0 / den
       
    return d

global iteration
iteration = 0
def Run(X):
    global iteration
    iteration += 1
    '''Run the segmentation process'''
    #X=sigmoid(X)

    a=ATMA.CLT()
    a.path_in = ["/Data/suralis/pre.h5","volume/data"]
    a.path_out = ["/Data/test.h5","data"]
    #a.Sub_Volume = [[0,1200], [0,1200], [200,550]]
    a.blockSize = [175,175,175]
    a.helo = 15 
    a.sigmaSmooth = 1
    a.thresMembra = X[0]
    a.sizeFilter = [20,1500]
    a.run()
    res = a.res[::]
    score = a.getScore()
    print iteration,X,score
    return -score


#minimize(Run, [0], method='powell')

for x in numpy.arange(0.05,0.95,0.05):Run([x])
'''
BestScore=[0,0,0]
para=[]
for s in  numpy.arange(0.2,0.3,0.01):
    for t in  numpy.arange(0.1,0.4,0.01):
        para.append((s,t))

from random import shuffle
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

'''


"""all      | 100 | 350 """
