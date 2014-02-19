import Segmentation
import GapClosing

class CLT():
    def __init__(self):pass
    def run(self):

        # apply segmentation on prediction data
        a=Segmentation.BioData.Nerve(self.predictionData)
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
        self.res = d.data
