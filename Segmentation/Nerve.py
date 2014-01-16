import vigra
import h5py
import numpy
from Filters import *

class Nerve (Filters):

    sigmaSmooth = 0.7
    thresMembra = 0.7
    sizeFilter = [0,1000]

    def __init__(self,dataIN):
        self.dataIN=dataIN


    def run(self):

        res = self.thresholdSegmentation(self.dataIN[:,:,:,0],self.sigmaSmooth,self.thresMembra)
        res = self.invertVolume2D(res,self.sizeFilter)

        self.seg=res



