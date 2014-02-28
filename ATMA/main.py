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
        self._text(0, "File Import / Export")
        self._button2(1, self._openFileR, "Raw",self._openFileP, "Pre")
        self.labRaw= self._label(2, self._none, "Raw Data" , "Path to hdf5 file")
        self.labPre= self._label(3, self._none, "Prediction" , "Path to hdf5 file")
        self.labOut= self._label(4, self._set_pathOut, "Output" , "Path to hdf5 file")

        self._text(6, "Set Sub-Volume")
        self.labRange = self._label(7, self._set_range, "Range" , "[x0,x1,y0,y1,z0,z1]")
        self._button(8, self._viewPrediction, "View Sub Volume")

        self._text(11, "Classification")
        self._label(12, self._set_sigmaSmooth, "Smoothing" , "Sigma [float]")
        self._label(13, self._set_thresMembra, "Thresholding" , "Level [float]")
        self._label(14, self._none, "Closing" , "Pixel [integer]")
        self._label(15, self._none, "Max. Distance" , "Pixel [integer]")
        self._label(16, self._none, "Min. Distance" , "Pixel [integer]")
        self._button(17, self._runGapClosing, "Run Axon Classification")
        
        
        self._text(20, "Node of Ranvier Detection")
        self.NDInit=0
        self.NodeClas= QtGui.QPushButton(self)
        self.NodeClas.setText("Train Classifier")
        self.NodeClas.clicked.connect(self.runNodeDetection)
        self.grid.addWidget(self.NodeClas, 21, 0,1,3)

        self.NodeClasTrue= QtGui.QPushButton(self)
        self.NodeClasTrue.setText("True")
        self.NodeClasTrue.clicked.connect(self.clickTRUE)
        self.grid.addWidget(self.NodeClasTrue, 24, 3,1,5)
        
        self.NodeClasFalse= QtGui.QPushButton(self)
        self.NodeClasFalse.setText("False")
        self.NodeClasFalse.clicked.connect(self.clickFALSE)
        self.grid.addWidget(self.NodeClasFalse, 24, 8,1,5)



        #self._button(23, self._viewResults, "View Results" )
        self._button(24, self._runFull, "Run Batch Processing")

        #Maya Widget
        self.M = MayaviQWidget()
        self.grid.addWidget(self.M, 0, 3,24,10)

        #Layout
        self.setGeometry(2300, 0, 1250, 850)
        self.setLayout(self.grid)
        self.setWindowTitle('ATMA')
        self.show()

    def runNodeDetection(self):
        self.Labels=[]
        self.Features=[]
        self.ND = Training.GapDetection()
        self.ND.gaps = h5py.File(self.path_out[0])[self.path_out[1]+"/gaps"]
        self.ND.raw= self.RawData
        self.ND.pred_volume = self.PredData
        self.ND.Range= self.Range
        self.ND.calcGapList()

        self.f,volume = self.ND.GetExamples()

        self.M.visualization.clear()
        GUI.DataVisualizer.rawSlider( volume )

    def clickTRUE(self):
        self.Labels.append([0])
        self.Features.append(self.f)
        self.f,volume = self.ND.GetExamples()

        self.M.visualization.clear()
        GUI.DataVisualizer.rawSlider( volume )
        print self.Labels
        print self.Features

        r = vigra.learning.RandomForest()
        Feat = numpy.array(self.Features, dtype=numpy.float32)
        Lab = numpy.array(self.Labels, dtype=numpy.uint32)
        r.learnRF(Feat, Lab)
        f = numpy.array([self.f], dtype=numpy.float32)
        pred=r.predictProbabilities(f)
        print pred
        #print Lab

    def clickFALSE(self):
        self.Labels.append([1])
        self.Features.append(self.f)
        self.f,volume = self.ND.GetExamples()

        self.M.visualization.clear()
        GUI.DataVisualizer.rawSlider( volume )
        print self.Labels
        print self.Features
        
        r = vigra.learning.RandomForest()
        Feat= numpy.array(self.Features, dtype=numpy.float32)
        Lab= numpy.array(self.Labels, dtype=numpy.uint32)
        r.learnRF(Feat, Lab)
        f = numpy.array([self.f], dtype=numpy.float32)
        pred=r.predictProbabilities(f)
        print pred
        #print Lab


    #Widgets
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



    #Functions

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

    def _viewResults(self):
        GUI.DataVisualizer.segmentation( self.res )

    def test(self):pass

    def _clear(self):
        self.M.visualization.clear()

    def _demo(self):
        self.M.visualization.update_plot()

    def _runGapClosing(self):
        x0,x1,y0,y1,z0,z1=self.Range

        a=CLT()
        a.path_in= self.path_in
        a.path_out = self.path_out
        a.Sub_Volume = [[x0,x1],[y0,y1],[z0,z1]] 
        a.blockSize = [200,200,200]
        a.helo = 30
        a.sigmaSmooth = self.sigmaSmooth
        a.thresMembra = self.thresMembra
        a.sizeFilter = [20,1000]
        a.verbose = 1
        a.run()
        self.res=h5py.File(a.path_out[0])[a.path_out[1]+"/axons"][::]

        self._viewPrediction() 
        GUI.DataVisualizer.segmentation( self.res )

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
