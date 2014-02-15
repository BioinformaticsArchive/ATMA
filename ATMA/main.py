from GUI import *
import GUI
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
        #self.grid.setSpacing(18)

        #Buttons
        self._button(0, self._openFile, "Open File")

        self.labPath  = self._label(1, self._none, "Path" , "Path")
        self.labRange = self._label(2, self._set_range, "Range" , "[x0,x1,y0,y1,z0,z1]")
        self._button(3, self._viewPrediction, "View Prediction")

        self._text(5, "Segmentation")
        self._label(6, self._set_sigmaSmooth, "Smoothing" , "Sigma [float]")
        self._label(7, self._set_thresMembra, "Thrasholding" , "Level [float]")
        self._label(8, self._set_thresMembra, "Closing" , "Pixel [intager]")
        self._button2(9, self._runSegmentation, "Preview",self._runSegmentation, "Parameter Estimation")

        self._text(11, "Gap Closing")
        #METHOD raider here !
        self._label(12, self._set_sigmaSmooth, "Max. Distance" , "Pixel [intager]")
        self._label(13, self._set_sigmaSmooth, "Min. Distance" , "Pixel [intager]")
        self._button2(14, self._runGapClosing, "Preview",self.test, "Train Classifier")


        self._text(16, "Node Detection")
        self._button3(17, self.test, "Preview",self.test, "Training",self.test, "Done")
        self._button(21, self._runSegmentation, "Run pipeline on subset"      )
        self._button(22, self._runSegmentation, "Run pipeline on full dataset"      )
        self._button(23, self._viewResults, "View Results" )

        #Maya Widget
        self.M = MayaviQWidget(self)
        self.grid.addWidget(self.M, 0, 3,24,1)

        #Layout
        self.setGeometry(2300, 0, 1250, 850)
        self.setLayout(self.grid)
        self.setWindowTitle('ATMA')
        self.show()




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
    def _openFile(self):

        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home/')
        #self.fname = "/Users/rwalecki/Dropbox/Projects/ATMA/tests/data/Volume001.h5"
        self.FullData = h5py.File(self.fname)["volume/data"]
        self.labPath.setText(self.fname)


        #set initaial range of full volume
        X,Y,Z,c = self.FullData.shape
        self.RANGE=[0,X,0,Y,0,Z]
        self.labRange.setText(str(self.RANGE))

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
        self.data=self.FullData[L[0]:L[1],L[2]:L[3],L[4]:L[5],0]

        self._clear()
        GUI.DataVisualizer.rawSlider( self.data)
    def _viewResults(self):
        GUI.DataVisualizer.segmentation( self.res )

    def test(self):pass

    def _clear(self):
        self.M.visualization.clear()

    def _demo(self):
        self.M.visualization.update_plot()

    def _runSegmentation(self):

        A=Segmentation.BioData.Nerve(self.data)
        A.sigmaSmooth = self.sigmaSmooth
        A.thresMembra = self.thresMembra
        A.sizeFilter = [20,1000]
        A.run()
        self.seg=A.seg

        self._clear()
        GUI.DataVisualizer.rawSlider( self.data)
        GUI.DataVisualizer.segmentation( self.seg)

    def _runGapClosing(self):

        # compute tokens end endpoints from the segmented data
        b=GapClosing.Tokenizer.Data2Token(self.seg)
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
        d=GapClosing.Tokenizer.Token2Data(TList,self.seg.shape)
        d.run()
        self.res=d.data

        GUI.DataVisualizer.rawSlider( self.data)
        GUI.DataVisualizer.segmentation( self.res )

    def _runNodeDetection(self):pass