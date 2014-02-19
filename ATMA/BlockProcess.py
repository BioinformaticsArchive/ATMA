import numpy
import vigra
import time
import h5py

from multiprocessing import Process, Lock
import multiprocessing


class BlockProcess():

    data_in = None
    data_out = None
    Process = None

    def __init__(self):pass

    def run(self):
        print numpy.mean(self.data_in)
        print numpy.mean(self.Process(self.data_in))

