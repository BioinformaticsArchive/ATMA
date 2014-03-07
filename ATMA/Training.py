import numpy
import vigra
from Segmentation.Filters import *

class GapDetection():
    '''
    The node of Ranvier Classifier can be trained and used with this class.

    The segmentation process of ATMA creates a file that contains all axons 
    and all gaps with their unique ID.
    The axons are stored in [inner hdf5path]/axons
    the gaps are stored in [inner hdf5path]/gaps

    Both datasets are used for the node of Ranvier classifier training 
    '''

    gaps = None
    pred_volume = None # prediction volume data
    pred_node = None # prediction for node of ranvier 
    i=-1     # id of current example
    

    def __init__(self):pass

    def calcGapList(self):
        x0,x1,y0,y1,z0,z1=self.Range
        '''

        Computing the list that contains all gaps
        from a binary volume 

                [[x1,y1,z1],
                 [x2,y2,z2],
                 [x3,y3,z3],
                 ...
                ]

        '''
        
        self.gapL=[]
        self.Labels=[]
        for z in range(self.gaps.shape[2]):
            pos=numpy.argwhere(self.gaps[:,:,z])
            if len(pos)!=0:
                for p in pos:
                    [x,y] = p
                    self.gapL.append([x+x0,y+y0,z+z0])

                    # -1 means not labeled yet
                    self.Labels.append(-1)
        self.Labels = numpy.array(self.Labels)
    
    def calcObjectMatrix(self,s,M):

        #Features, Labels, Data
        O=[]
        for x,y,z in self.gapL:
            o={}
            F=[]

            x0, x1 = max(0,x-M), min(s[0],x+M)
            y0, y1 = max(0,y-M), min(s[1],y+M)
            z0, z1 = max(0,z-M), min(s[2],z+M)
           

            tmp_volume_pre = self.pred_volume[x0:x1,y0:y1,z0:z1,:]
            tmp_volume_raw = self.raw[x0:x1,y0:y1,z0:z1]

            tmp_Feature=[]
            #for i in numpy.arange(4,13,2):
                #tmp_Feature.append(rayFeatures(tmp_volume_pre[:,:,:,0],i))

            for i in numpy.arange(0.5,6,0.5):
                #tmp_Feature.append(vigra.gaussianSmoothing(tmp_volume_pre[:,:,:,0],i))
                tmp_Feature.append(vigra.gaussianSmoothing(tmp_volume_pre[:,:,:,1],i))
                #tmp_Feature.append(vigra.gaussianSmoothing(tmp_volume_pre[:,:,:,2],i))

            
            for v in tmp_Feature:
                s1, s2, s3 = v.shape
                c = v[s1/2,s2/2,s3/2]
                l = numpy.mean(v[s1/2,s2/2,:])
                d = numpy.mean(v[:,:,s3/2])
                F.append(c)
                F.append(l)
                F.append(d)

            o['Features']=F
            o['Position']=[x,y,z]
            o['Label']=-1
            o['Prediction']=[[0]]
            o['Data']=tmp_volume_raw

            O.append(o)
            #f=numpy.array(f) 
        #else:
            #return 0,0


        #return f,tmp_volume_raw
        return O
