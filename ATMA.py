#!/usr/bin/env python

import PyQt4
import GUI.main

def main():

    app = PyQt4.QtGui.QApplication.instance()
    ex = GUI.main.ATMA_GUI()
    app.exec_()

if __name__ == '__main__':

    main()
