import ATMA.CLT
a=ATMA.CLT()
a.path_in = ["/Data/suralis/pre.h5","volume/data"]
a.path_out = ["/tmp/res6.h5","data"]
a.Sub_Volume = [[300,1200], [400,1100], [0,600]] #full dataset sub cube
a.blockSize = [300,300,600]
#a.blockSize = [900,700,600]
#a.Sub_Volume = [[600,700], [600,700], [0,100]] #testset
#a.blockSize = [75,75,75]
a.workers = 8
a.helo = 10
a.sigmaSmooth = 0
a.thresMembra = 0.3
a.sizeFilter = [20,1000]
a.verbose = 1
a.run()
res = a.res[::]

import vigra
score = a.getScore()

print "     score:", score

import h5py
import vigra
import numpy

#attribute=h5py.File('/tmp/res4.h5')['data/attributes'][::]
#for a in attribute:
    #print a
'''
d=h5py.File(a.path_in[0])[a.path_in[1]][300:1200,400:1100,300]
vigra.impex.writeImage(d[:,:,0],"/tmp/pre.png")
vigra.impex.writeImage(vigra.Image(res[:,:,100]!=0),"/tmp/res.png")
'''


