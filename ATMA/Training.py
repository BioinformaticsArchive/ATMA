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
    

    def __init__(self):pass

    def _calcGapList(self,gaps):
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
        for z in range(gaps.shape[2]):
            pos=numpy.argwhere(gaps[:,:,z])
            if len(pos)!=0:
                for p in pos:
                    [x,y] = p
                    self.gapL.append([x,y,z])

                    # -1 means not labeled yet
                    self.Labels.append(-1)
        self.Labels = numpy.array(self.Labels)

    def _calcFeatureList(self):
        '''
        Computing the feature vector to each gap
        '''

        s = self.gaps.shape
        M = 15

        F = []
        for g in self.gapL:
            V,f = [],[]
            x, y, z = g
            x0, x1 = max(0,x-M), min(s[0],x+M)
            y0, y1 = max(0,y-M), min(s[1],y+M)
            z0, z1 = max(0,z-M), min(s[2],z+M)

            tmp_volume = self.pred_volume[x0:x1,y0:y1,z0:z1,:]

            for i in numpy.arange(4,13,2):
                V.append(rayFeatures(tmp_volume[:,:,:,0],i))

            for i in numpy.arange(0.5,6,0.5):
                V.append(vigra.gaussianSmoothing(tmp_volume[:,:,:,0],i))
                V.append(vigra.gaussianSmoothing(tmp_volume[:,:,:,1],i))
                V.append(vigra.gaussianSmoothing(tmp_volume[:,:,:,2],i))

            
            for v in V:
                s1, s2, s3 = v.shape
                c = v[s1/2,s2/2,s3/2]
                l = numpy.mean(v[s1/2,s2/2,:])
                d = numpy.mean(v[:,:,s3/2])
                f.append(c)
                f.append(l)
                f.append(d)

            f= numpy.array(f) 
            F.append(f)


        self.Features = F
        self.Features= numpy.array(self.Features, dtype=numpy.float32)

    def _runLabelTool(self):

        # training examples at once
        N=4

        first_nonlabeled=numpy.min(numpy.argwhere(self.Labels==-1))
        lab_current=range(first_nonlabeled,first_nonlabeled+N)

        # create labeling data for visualization
        M=40
        s=self.pred_volume.shape
        
        Examples=[]
        for g in lab_current:
            x, y, z = self.gapL[g]
            x0, x1 = max(0,x-M), min(s[0],x+M)
            y0, y1 = max(0,y-M), min(s[1],y+M)
            z0, z1 = max(0,z-M), min(s[2],z+M)
            tmp_volume = self.pred_volume[x0:x1,y0:y1,z0:z1,:]
            Examples.append([tmp_volume,g])

        print len(Examples)
        # HERE THE LABELTOOL! 
        # use the examples array (length = 4) for visualization
        # then, label this 4 examples and the resulting array has to be used
        # to update the self.Labels array
        
        #1 ranvier 
        #0 else 
        for i in lab_current:
            self.Labels[i]=i%2

        print lab_current, self.Labels
        
        
        self.Feat=[]
        self.Lab=[]
        for l in numpy.argwhere(numpy.array(self.Labels)==1).T[0]:
            self.Feat.append(self.Features[l])
            self.Lab.append([1])
        
        for l in numpy.argwhere(numpy.array(self.Labels)==0).T[0]:
            self.Feat.append(self.Features[l])
            self.Lab.append([0])
        
        self.Feat= numpy.array(self.Feat, dtype=numpy.float32)
        self.Lab= numpy.array(self.Lab, dtype=numpy.uint32)

    def _runTraining(self):
        r = vigra.learning.RandomForest()
        r.learnRF(self.Feat, self.Lab)

        #probability of being a node of ranvier
        self.pred_node= r.predictProbabilities(self.Features)[:,1]

    def _saveResults(self):
        Nodes=numpy.argwhere(self.pred_node>0.5).T[0]
        
        f = open("/tmp/oo.txt", 'w')
        f.write("X;\tY;\tZ;\tP;\n")
        for n in Nodes:
            X,Y,Z = self.gapL[n]
            P = self.pred_node[n]
            f.write(str(int(X))+';\t'+\
                    str(int(Y))+';\t'+\
                    str(int(Z))+';\t'+\
                    str(float(P))+';'+\
                    '\n')


    def run(self):
        #   self.Features contains all Features 
        #   self.Label contains all labels and cann be updated by 
        #   _runLabelTool

        #at startup
        self._calcGapList(self.gaps)
        self._calcFeatureList()

        #with a click, the labeltool should start
        #after labeling train the classifire
        for i in range(3):
            self._runLabelTool()
            self._runTraining()

        #run labeltool again on other nodes and see predictions
        #or stop labeling and run prediction on all gaps
        self._saveResults()
        




