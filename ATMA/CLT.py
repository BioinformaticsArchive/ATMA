import Segmentation
import GapClosing
from BlockProcess import BlockProcess
import h5py
import numpy

class CLT():

    path_in = None
    path_out = None
    blockSize = None
    Sub_Volume = None
    blockSize  = [50,50,50]
    helo = 10
    Workers = 8
    verbose = 0
   
    #Vagus
    sigmaSmooth = 0.7
    thresMembra = 0.7
    minSize = 500
    sizeFilter = [20,1000]

    #Score
    Margin = 0.1


    def __init__(self):pass

    def _Process(self, data):
        a=Segmentation.BioData.Nerve(data[:,:,:,0])
        a.sigmaSmooth = self.sigmaSmooth
        a.thresMembra = self.thresMembra
        a.sizeFilter = self.sizeFilter
        a.run()
        seg = a.seg

        # compute tokens end endpoints from the segmented data
        b=GapClosing.Tokenizer.Data2Token(seg)
        b.minSize=self.minSize
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

        #Create Volume that contains all gaps
        Gaps = numpy.zeros(seg.shape)
        GapList = []
        for g in GList:

            #here pass the gap atributes in a better way
            xp1,yp1,zp1 = g.Ep1.Position
            xp2,yp2,zp2 = g.Ep2.Position
            xo1,yo1,zo1 = g.Ep1.Orientation
            xo2,yo2,zo2 = g.Ep2.Orientation
            t1 = g.Ep1.Thickness
            t2 = g.Ep2.Thickness
            #d = numpy.sum(((p1-p2)**2)**(0.5))
            x,y,z = g.Position
            Gaps[x,y,z]=1
            Attributes=[
            xp1,yp1,zp1,\
            xp2,yp2,zp2,\
            xo1,yo1,zo1,\
            xo2,yo2,zo2,\
            t1,t2]
            GapList.append(Attributes)

        return d.data, Gaps, GapList

    def getScore(self, method="linear"):
        if method=="linear":

            Z_0 = 0
            Z_1 = int(self.Margin * self.res.shape[2])
            Z_2 = int((1-self.Margin) * self.res.shape[2])
            Z_3 = int(self.res.shape[2])

            Candidates = numpy.unique(self.res[::2,::2,Z_0:Z_1:2])

            FullyTraced=[0]
            for z in range(Z_2,Z_3):
                l=self.res[::2,::2,z]
                Matches = numpy.intersect1d(Candidates,numpy.unique(l))
                FullyTraced = numpy.unique(numpy.append(Matches, FullyTraced))

            score = len(FullyTraced) - numpy.sum(FullyTraced==0)

        return score
    
    def run(self):
        self.predictionData = h5py.File(self.path_in[0])[self.path_in[1]]

        B = BlockProcess()
        B.path_in  = self.path_in
        B.path_out = self.path_out
        B.blockSize = self.blockSize
        B.Sub_Volume = self.Sub_Volume
        B.verbose = self.verbose
        B.helo = self.helo
        B.Process = self._Process 
        B.run()
        self.res = h5py.File(self.path_out[0])[self.path_out[1]+"/axons"]
        self.gaps = h5py.File(self.path_out[0])[self.path_out[1]+"/gaps"]
