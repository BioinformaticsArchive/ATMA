import numpy

class GapDetection():

    gaps = None
    pred = None

    def __init__(self):pass

    def _calcGapList(self):
        
        self.gapL=[]
        self.labL=[]
        for z in range(self.gaps.shape[2]):
            pos=numpy.argwhere(self.gaps[:,:,z])
            if len(pos)!=0:
                for p in pos:
                    [x,y] = p
                    self.gapL.append([x,y,z])
                    self.labL.append(0)


    def run(self):
        self._calcGapList()
