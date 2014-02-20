import Segmentation
import GapClosing
from BlockProcess import BlockProcess
import h5py

class CLT():


    path_in = None
    path_out = None
    blockSize = None
    Sub_Volume = None
    helo = 10
    Workers = 8
   
    #Vagus
    sigmaSmooth = 0.7
    thresMembra = 0.7
    sizeFilter = [20,1000]


    def __init__(self):pass

    def _Process(self, data):

        # apply segmentation on prediction data
        a=Segmentation.BioData.Nerve(data[:,:,:,0])
        a.sigmaSmooth = self.sigmaSmooth
        a.thresMembra = self.thresMembra
        a.sizeFilter = self.sizeFilter
        a.run()
        seg = a.seg

        # compute tokens end endpoints from the segmented data
        b=GapClosing.Tokenizer.Data2Token(seg)
        b.run()
        EList = b.EList
        TList = b.TList

        # metch endpoints and compute gaps
        c=GapClosing.Connector.GapFinder(EList)
        c.run()
        GList = c.GList

        # from gaplist, compute token unions
        d=GapClosing.Connector.TokenRemap( GList )
        d.run()

        # use tokens to reconstruct origin segmentation data
        d=GapClosing.Tokenizer.Token2Data(TList,seg.shape)
        d.run()
        return d.data
    

    def run(self):
        self.predictionData = h5py.File(self.path_in[0])[self.path_in[1]]

        if self.Sub_Volume == None:
            self.res = self._Process(self.predictionData)
        else:
            B = BlockProcess()
            B.path_in  = self.path_in
            B.path_out = self.path_out
            B.blockSize = self.blockSize
            B.Sub_Volume = self.Sub_Volume
            B.helo = self.helo
            B.Process = self._Process 
            B.run()
            self.res = h5py.File(self.path_out[0])[self.path_out[1]]



