#!/usr/bin/env python

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
    ex.path_in = ['/Data/vagus/data/pre.h5','volume/data']
    ex.PredData=h5py.File(ex.path_in[0])[ex.path_in[1]]
    ex.path_raw = ['/Data/vagus/data/raw.h5','volume/data']
    ex.RawData=h5py.File(ex.path_raw[0])[ex.path_raw[1]]
    ex.path_out = ["/tmp/ttt.h5","data"]
    ex.Range = [2200,2400,1000,1200,100,200]
    ex.sigmaSmooth=0.1
    ex.thresMembra=0.57
    #ex._viewPrediction()
    ex._runGapClosing()
    #ex._viewResults()
    app.exec_()


if __name__ == '__main__':

    main()
    #demo()
