#!/usr/bin/env python

import PyQt4
from ATMA.main import ATMA_GUI

def main():

    app = PyQt4.QtGui.QApplication.instance()
    ex = ATMA_GUI()
    app.exec_()

if __name__ == '__main__':

    main()
