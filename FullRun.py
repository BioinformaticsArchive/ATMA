import ATMA.CLT
a=ATMA.CLT()
a.path_in = ["/Data/suralis/pre.h5","volume/data"]
a.path_out = ["/tmp/res.h5","data"]
a.Sub_Volume = [[300,1200], [400,1100], [0,600]] #full dataset sub cube
a.blockSize = [500,500,500]
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


'''
import h5py
import vigra
import numpy

d=h5py.File(a.path_in[0])[a.path_in[1]][300:1200,400:1100,300]
vigra.impex.writeImage(d[:,:,0],"/tmp/pre.png")
vigra.impex.writeImage(vigra.Image(res[:,:,100]!=0),"/tmp/res.png")
'''
