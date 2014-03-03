#!/usr/bin/env python
import os
home = os.path.dirname(os.path.realpath(__file__))

import PyQt4
from ATMA.main import ATMA_GUI

def main():

    app = PyQt4.QtGui.QApplication.instance()
    ex = ATMA_GUI()
    app.exec_()

def demo():
    
    app = PyQt4.QtGui.QApplication.instance()
    ex = ATMA_GUI()
    import h5py
    ex.path_in = [home+'/data/vagus002PRE.h5','volume/data']
    ex.PredData=h5py.File(ex.path_in[0])[ex.path_in[1]]
    ex.path_raw = [home+'/data/vagus002RAW.h5','volume/data']
    ex.RawData=h5py.File(ex.path_raw[0])[ex.path_raw[1]]
    ex.path_out = ["/tmp/ttt.h5","data"]
    ex.Range = [0,200,0,200,0,100]
    ex.sigmaSmooth=0.7
    ex.thresMembra=0.4
    ex._viewPrediction()
    ex._runGapClosing()
    app.exec_()


if __name__ == '__main__':

    main()
    #demo()
