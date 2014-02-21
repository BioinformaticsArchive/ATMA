import numpy
import vigra
from Segmentation.Filters import *

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


    def _calcFeatureList(self):

        s = self.gaps.shape
        M = 15

        F = []
        for g in self.gapL:


            V,f = [],[]
            x, y, z = g
            x0, x1 = max(0,x-M), min(s[0],x+M)
            y0, y1 = max(0,y-M), min(s[1],y+M)
            z0, z1 = max(0,z-M), min(s[2],z+M)

            tmp_volume = self.pred[x0:x1,y0:y1,z0:z1,:]

            for i in numpy.arange(4,13,2):
                V.append(rayFeatures(tmp_volume[:,:,:,0],i))

            for i in numpy.arange(0.5,6,0.5):
                V.append(vigra.gaussianSmoothing(tmp_volume[:,:,:,0],i))
                V.append(vigra.gaussianSmoothing(tmp_volume[:,:,:,1],i))
                V.append(vigra.gaussianSmoothing(tmp_volume[:,:,:,2],i))

            
            for v in V:
                s1, s2, s3 = v.shape
                c = v[s1/2,s2/2,s3/2]
                l = numpy.mean(v[s1/2,s2/2,:])
                d = numpy.mean(v[:,:,s3/2])
                f.append(c)
                f.append(l)
                f.append(d)


            F.append(f)


        self.Features = F



    def run(self):

        self._calcGapList()
        self._calcFeatureList()
        print len(self.Features),len(self.gapL)
