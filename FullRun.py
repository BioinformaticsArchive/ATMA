import ATMA.CLT
a=ATMA.CLT()
a.path_in = ["/Data/suralis/pre.h5","volume/data"]
a.path_out = ["/tmp/res2.h5","data"]
a.Sub_Volume = [[600,950], [300,1000], [400,575]]
a.blockSize = [175,175,175]
a.workers = 8
a.helo = 15 
a.sigmaSmooth = 0.23
a.thresMembra = 0.27
a.sizeFilter = [20,3000]
a.verbose = 1
a.run()
res = a.res[::]
score = a.getScore()

print "     score:", score
