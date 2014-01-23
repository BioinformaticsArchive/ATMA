import vigra
import numpy
from Structures import *
from scipy import ndimage
class Tokenizer():
    """
    This class is used to split a volume into its components (tokens) within bounding boxes.

    example:

        001001        1  01
        001011  --->  1  11
        001011        1  11

    Usage:

        d1 : volume containing binary data

        t=ATMA.GapClosing.Tokenizer(d1)
        t.minSize=0
        t.epHalo=1
        t.run()
        L, E = t.TList, t.EList

    """

    minSize = 0
    epHalo = 7
    TList = [] # list that contains all tokens in thair bounding box
    EList = [] # list that contains all endpoint belonging to tokens

    def __init__(self,data):
        self.data=data


    def _calc_TList(self):
        self.TList = []

        cc     = vigra.analysis.labelVolumeWithBackground(vigra.Volume(self.data))
        feat   = vigra.analysis.extractRegionFeatures(vigra.Volume(cc),cc,[\
                'Count',\
                'RegionCenter',\
                'Coord<Maximum>',\
                'Coord<Minimum>',\
                'Mean'\
                ])

        for Size,Max,Min,ID in zip(\
                feat['Count'],\
                feat['Coord<Maximum>'],\
                feat['Coord<Minimum>'],\
                numpy.uint32(feat['Mean'])):

            BBox=abs(Max-Min)+[1,1,1]

            if ID==0:continue

            # Size filter
            if Size<self.minSize:continue

            # Length filter (skip tokens that are to short in any Z-dimension)
            if BBox[2]<self.epHalo:continue

            # Compute token features
            tokenData=(cc[Min[0]:Max[0]+1,Min[1]:Max[1]+1,Min[2]:Max[2]+1]==ID)

            T=Token()
            T.ID=ID
            T.MIN=Min
            T.MAX=Max
            T.Data=tokenData
            T.SIZE=numpy.uint32(Size)

            Skelet=[]
            Thickness=[]
            for l in range(tokenData.shape[2]):
                Thickness.append(numpy.sum(tokenData[:,:,l]))
                X,Y=numpy.mean(numpy.argwhere(tokenData[:,:,l]),axis=0)
                layerCenter=Min+[X,Y,l]
                Skelet.append(layerCenter)

            Skelet=numpy.array(Skelet,dtype=numpy.float16)
            T.SKEL=Skelet
            T.THICK=Thickness
            self.TList.append(T)


    def _calc_EList(self):
        self.EList=[]

        #Loop over all tokens
        for t in self.TList:

            # Create starting end ending skeletons
            s1= t.SKEL[-self.epHalo:]
            s2= t.SKEL[:self.epHalo]

            # Compute endpoint center
            p1 = numpy.mean(s1,axis=0)
            p2 = numpy.mean(s2,axis=0)


            # Compute endpoint orientation
            o1=[]
            for k in range(len(s1)-1):
                o=s1[k+1]-s1[k]
                #print numpy.linalg.norm(o)
                o/=numpy.linalg.norm(o)
                o1.append(o)
            o1=numpy.mean(o1,axis=0)

            o2=[]
            for k in reversed(range(1,len(s2))):
                o=s2[k-1]-s2[k]
                o/=numpy.linalg.norm(o)
                o2.append(o)
            o2=numpy.mean(o2,axis=0)

            # Compute radius
            t1= t.THICK[-self.epHalo:]
            t1=numpy.sqrt(numpy.mean(t1)/numpy.pi)

            t2= t.THICK[:self.epHalo]
            t2=numpy.sqrt(numpy.mean(t2)/numpy.pi)


            epA=EndPoint()
            epA.Token       = t
            epA.Position    = p1
            epA.Thickness   = t1
            epA.Orientation = o1

            t.EndPointA=epA
            self.EList.append(epA)

            epB=EndPoint()
            epB.Token       = t
            epB.Position    = p2
            epB.Thickness   = t2
            epB.Orientation = o2

            t.EndPointB=epB
            self.EList.append(epB)


    def run(self):
        self._calc_TList()
        self._calc_EList()
