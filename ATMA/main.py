from GUI import *
import vigra
import GUI
import Training
from CLT import CLT
import Segmentation
import GapClosing
import h5py
import re
import numpy


class ATMA_GUI(QtGui.QWidget):

    def __init__(self):
        super(ATMA_GUI,self).__init__()
        self.initUI()

    def initUI(self):
        self.grid = QtGui.QGridLayout()

        #Buttons
        self._text(0, "Import / Export")
        self._button2(1, self._openFileR, "Raw",self._openFileP, "Pre")
        self.labRaw= self._label(2, self._none, "Raw Data" , "Path to hdf5 file")
        self.labPre= self._label(3, self._none, "Prediction" , "Path to hdf5 file")
        self.labOut= self._label(4, self._set_pathOut, "Output" , "Path to hdf5 file")

        self._text(6, "Select Range")
        self.labRange = self._label(7, self._set_range, "Range" , "[x0,x1,y0,y1,z0,z1]")
        self._button(8, self._viewPrediction, "View Sub Volume")

        self._text(10, "Axon Classification")
        self._label(11, self._set_sigmaSmooth, "Smoothing" , "Sigma [float]")
        self._label(12, self._set_thresMembra, "Thresholding" , "Level [float]")
        self._label(13, self._none, "Closing" , "Pixel [integer]")
        self._label(14, self._none, "Max. Distance" , "Pixel [integer]")
        self._label(15, self._none, "Min. Distance" , "Pixel [integer]")
        self._button2(16, self._runGapClosing, "Run Axon Classification",self._viewResults,"View Results")
        
        
        self._text(19, "Node of Ranvier Detection")
        self._button(20,self.runNodeDetection, "Train Classifier")
        self._button2(21, self._viewGaps, "View Gaps",self.zoom, "Zoom In/Out")

        self.NodeClasTrue= QtGui.QPushButton(self)
        self.NodeClasTrue.setText("True")
        self.NodeClasTrue.clicked.connect(self.clickTRUE)
        self.grid.addWidget(self.NodeClasTrue, 24, 3,1,5)
        
        self.NodeClasFalse= QtGui.QPushButton(self)
        self.NodeClasFalse.setText("False")
        self.NodeClasFalse.clicked.connect(self.clickFALSE)
        self.grid.addWidget(self.NodeClasFalse, 24, 8,1,5)



        self._text(23, "Batch Processing")
        self._button(24, self._runFull, "-- Run --")

        #Maya Widget
        self.M = MayaviQWidget()
        self.grid.addWidget(self.M, 0, 3,24,10)

        #Layout
        self.setGeometry(2300, 0, 1250, 850)
        self.setLayout(self.grid)
        self.setWindowTitle('ATMA')
        self.show()



    # Core Functions
    def runNodeDetection(self):
        self.CurrentNode=0
        self.view=0
        ND = Training.GapDetection()
        ND.gaps = h5py.File(self.path_out[0])[self.path_out[1]+"/gaps"]
        ND.raw = self.RawData
        ND.pred_volume = self.PredData
        ND.Range = self.Range
        ND.calcGapList()
        g = ND.gapL

        s=self.PredData.shape
        M=24
        self.O = ND.calcObjectMatrix(s,M)

        self.CurrentObject=0
        self.view=0
        self.zoom()

    def zoom(self):
        self.view+=1
        self._clear()
        r=self.Range

        if self.view%2!=0:
            #Show zoom in, subset with single gap
            data = self.O[self.CurrentObject]["Data"]
            x,y,z=numpy.array(data.shape)/2
            opac = 0.3

            p=self.O[self.CurrentObject]["Prediction"][0]
            if len(p)==1:
                C=[0,0,0]
            if len(p)==2:
                C=numpy.array([1,0,0])*p[0]+numpy.array([0,1,0])*p[1]

            GUI.DataVisualizer.points( x, y, z, 1, opac,C)

        else:
            #show zoom out: full dataset with all gaps
            L=self.Range
            data=self.RawData[L[0]:L[1],L[2]:L[3],L[4]:L[5]]

            # Do do:
            # multiple classes
            # 1: Done       (yellow,orange) To test only, later disappear
            # 2: Current    (blue)
            # 3: prediction (green, red)
            X,Y,Z,S,C=[],[],[],[],[]
            for o in self.O:
                x,y,z = o['Position']-numpy.array([r[0],r[2],r[4]])
                C=[0,0,0]


                # unlabeled candidates have double the size
                # Labeled are either red or green
                if o["Label"]==-1:
                    S=1
                    opac = 0.3
                else:
                    if o["Label"]==1:
                        C=[0,1,0]
                    if o["Label"]==0:
                        C=[1,0,0]
                    S=0.5
                    opac = 1


                # current object
                if o==self.O[self.CurrentObject]:
                    opac = 0.7
                    S=2
                else:
                    p=o["Prediction"][0]
                    if len(p)==1:
                        C=[0,0,0]
                    if len(p)==2:
                        C=numpy.array([1,0,0])*p[0]+numpy.array([0,1,0])*p[1]


                GUI.DataVisualizer.points( x, y, z, S, opac ,C)

        GUI.DataVisualizer.rawSlider( data )


    def calcProbabilities(self):
        # Compute Features
        L,F,=[],[]
        for o in self.O:
            l=o["Label"]
            f=o["Features"]
            if l != -1:
                L.append([l])
                F.append(f)

        # Train RF
        r = vigra.learning.RandomForest()
        Feat = numpy.array(F, dtype=numpy.float32)
        Lab = numpy.array(L, dtype=numpy.uint32)
        r.learnRF(Feat, Lab)

        
        # Predict on Data
        for o in self.O:
            f=numpy.array([o["Features"]],dtype=numpy.float32)
            pred=r.predictProbabilities(f)
            o["Prediction"]=pred





    def clickTRUE(self):
        o=self.O[self.CurrentObject]
        self.M.visualization.clear()
        self.view+=1

        o["Label"]=1
        self.calcProbabilities()

        #Show next
        self.CurrentObject+=1
        self.zoom()

    def clickFALSE(self):
        o=self.O[self.CurrentObject]
        self.M.visualization.clear()
        self.view+=1

        o["Label"]=0
        self.calcProbabilities()

        #Show next
        self.CurrentObject+=1
        self.zoom()
    
    def _runGapClosing(self):
        x0,x1,y0,y1,z0,z1=self.Range

        a=CLT()
        a.path_in= self.path_in
        a.path_out = self.path_out
        a.Sub_Volume = [[x0,x1],[y0,y1],[z0,z1]] 
        a.blockSize = [200,200,200]
        a.helo = 20
        a.sigmaSmooth = self.sigmaSmooth
        a.thresMembra = self.thresMembra
        a.sizeFilter = [20,1000]
        a.verbose = 1
        a.run()
        self.res=h5py.File(a.path_out[0])[a.path_out[1]+"/axons"][::]
        print "Done"

    def _runFull(self):
        a=CLT()
        a.path_in= self.path_in
        a.path_out = self.path_out
        a.blockSize = [200,200,200]
        a.helo = 30
        a.sigmaSmooth = self.sigmaSmooth
        a.thresMembra = self.thresMembra
        a.sizeFilter = [20,1000]
        a.verbose = 1
        a.run()
        self.res=h5py.File(a.path_out[0])[a.path_out[1]+"/axons"][::]



    # Widgets (ToDo: this should be in an separate class)
    def _button(self,x,func,title):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,0,1,3)

    def _button2(self,x,func,title,func2,title2):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,0,1,1)

        b2 = QtGui.QPushButton(title2,self)
        b2.clicked.connect(func2)
        self.grid.addWidget(b2,x,1,1,2)

    def _button3(self,x,func,title,func2,title2,func3,title3):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,0,1,1)

        b2 = QtGui.QPushButton(title2,self)
        b2.clicked.connect(func2)
        self.grid.addWidget(b2,x,1)

        b3 = QtGui.QPushButton(title3,self)
        b3.clicked.connect(func3)
        self.grid.addWidget(b3,x,2)

    def _label(self,x,func, title, startValue):
        q = QtGui.QLineEdit(self)
        q.setMaximumWidth(200)
        q.textChanged[str].connect(func)
        q.setPlaceholderText(startValue)


        l = QtGui.QLabel(self)
        l.setText(title)

        self.grid.addWidget(l,x,0)
        self.grid.addWidget(q,x,1,1,2)

        #if startValue has form of inatager or float, convert it
        try:
            startValue=float(startValue)
        except ValueError:
            pass

        func(startValue)

        return q

    def _text(self,x,title):
        l = QtGui.QLabel(self)
        l.setText("---"+title+"---")
        self.grid.addWidget(l,x,0,1,3)

    def _buttonLabel(self,x,func,title,startValue):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,0,1,1)



    
    # Other Functions
    def _none(self,text):pass

    def _set_pathOut(self,text):
        self.path_out=[text,'data']

    def _openFileP(self):
        self.path_in = ['', '']
        self.path_in[0] = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home/')
        self.path_in[1] = 'volume/data'
        #self.path_in = ['./data/vagus001.h5',"volume/data"]
        self.PredData=h5py.File(self.path_in[0])[self.path_in[1]]
        self.labPre.setText(self.path_in[0])

        #set initial range of full volume
        X,Y,Z,c = self.PredData.shape
        self.RANGE=[0,X,0,Y,0,Z]
        self.labRange.setText(str(self.RANGE))

    def _openFileR(self):
        self.path_raw= ['', '']
        self.path_raw[0] = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home/')
        self.path_raw[1] = 'volume/data'
        self.RawData=h5py.File(self.path_raw[0])[self.path_raw[1]]
        self.labRaw.setText(self.path_raw[0])

    def _set_range(self,text):
        L=re.findall('\d+', text)
        self.Range=[int(L[0]),int(L[1]),int(L[2]),int(L[3]),int(L[4]),int(L[5])]

    def _set_sigmaSmooth(self, text):
        try:
            self.sigmaSmooth=float(text)
        except ValueError:
            pass

    def _set_thresMembra(self, text):
        try:
            self.thresMembra=float(text)
        except ValueError:
            pass

    def _viewPrediction(self):
        L=self.Range
        data=self.RawData[L[0]:L[1],L[2]:L[3],L[4]:L[5]]
        self._clear()
        GUI.DataVisualizer.rawSlider( data )
    
    def _viewGaps(self):pass

    def _viewResults(self):
        GUI.DataVisualizer.segmentation( self.res )

    def test(self):pass

    def _clear(self):
        self.M.visualization.clear()

    def _demo(self):
        self.M.visualization.update_plot()

