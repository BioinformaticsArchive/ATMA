import vigra
import h5py
import numpy
import vigra
import Filters

class Nerve():

    sigmaSmooth = 0.7
    thresMembra = 0.7
    sizeFilter = [0,1000]

    def __init__(self,dataIN):
        self.dataIN=dataIN


    def run(self):

        res = Filters.thresholdSegmentation(self.dataIN,self.sigmaSmooth,self.thresMembra)
        res = Filters.invertVolume2D(res,self.sizeFilter)

        self.seg=res

class Cortex():
    
    rayLength = 12
    scales = [3,5,7,9]
    sigmaSmooth = 1
    thMem = 0.3
    th1 = 0.55
    th2 = 12

    
    def __init__(self,dataIN):
        self.dataIN = vigra.Volume(dataIN)

    def run(self):

        res = Filters.rayFeatures( self.dataIN, self.rayLength)
        res = Filters.multiHessian( res, self.scales )

        mem = vigra.gaussianSmoothing( self.dataIN, self.sigmaSmooth)

        res = Filters.waterSeg( mem, res, self.th1, self.th2 )

        self.seg=res

