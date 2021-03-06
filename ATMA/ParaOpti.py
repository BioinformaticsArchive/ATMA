from BlockProcess import BlockProcess

import numpy
import h5py

class Score():

    data = None
    Margin = 0.1

    def __init__(self):pass

    def scoreTracer(self):
        if self.res.shape==2:
            self.data = h5py.File(self.res[0])[self.res[1]]
        else:
            self.data = self.res


        Z_0 = 0
        Z_1 = int(self.Margin * self.data.shape[2])
        Z_2 = int((1-self.Margin) * self.data.shape[2])
        Z_3 = int(self.data.shape[2])

        Candidates = numpy.unique(self.data[::4,::4,Z_0:Z_1:4])

        FullyTraced=[0]
        for z in range(Z_2,Z_3):
            l=self.data[::4,::4,z]
            Matches = numpy.intersect1d(Candidates,numpy.unique(l))
            FullyTraced = numpy.unique(numpy.append(Matches, FullyTraced))


        return len(FullyTraced) - numpy.sum(FullyTraced==0)
