import vigra
import h5py
import numpy
import Filters

class Nerve():

    sigmaSmooth = 0.7
    thresMembra = 0.7
    sizeFilter = [0,1000]

    def __init__(self,dataIN):
        self.dataIN=dataIN


    def run(self):

        res = Filters.thresholdSegmentation(self.dataIN[:,:,:,0],self.sigmaSmooth,self.thresMembra)
        res = Filters.invertVolume2D(res,self.sizeFilter)

        self.seg=res



