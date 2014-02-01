from qt_embedding import *
import h5py


class ATMA_GUI(QtGui.QWidget):

    def __init__(self):
        super(ATMA_GUI,self).__init__()
        self.initUI()

    def initUI(self):

        self.grid = QtGui.QGridLayout()
        #self.grid.setSpacing(18)

        #Buttons
        self._buttonLabel(0, self._openFile, "Open File" , "Path [string]")
        self._buttonLabel(1, self.test, "Save File" , "Path [string]")
        self._label(2, self._set_sigmaSmooth, "Range" , "[x0,x1,y0,y1,z0,z1]")
        self._button(3, self._viewPrediction, "View Prediction")

        self._text(5, "Segmentation")
        self._label(6, self._set_sigmaSmooth, "Smoothing" , "Sigma [float]")
        self._label(7, self._set_thresMembra, "Thrasholding" , "Level [float]")
        self._label(8, self._set_thresMembra, "Closing" , "Pixel [intager]")
        self._button2(9, self.test, "Preview",self.test, "Parameter Estimation")

        self._text(11, "Gap Closing")
        #METHOD raider here !
        self._label(12, self._set_sigmaSmooth, "Max. Distance" , "Pixel [intager]")
        self._label(13, self._set_sigmaSmooth, "Min. Distance" , "Pixel [intager]")
        self._button2(14, self.test, "Preview",self.test, "Train Classifier")


        self._text(16, "Gap Closing")
        self._button3(17, self.test, "Preview",self.test, "Training",self.test, "Done")
        self._button(21, self._run, "Run pipeline on subset"      )
        self._button(22, self._run, "Run pipeline on full dataset"      )
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

    def _text(self,x,title):

        l = QtGui.QLabel(self)
        l.setText("---"+title+"---")
        self.grid.addWidget(l,x,0,1,3)



    def _buttonLabel(self,x,func,title,startValue):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,0,1,1)
        q = QtGui.QLineEdit(self)
        q.setMaximumWidth(200)
        q.textChanged[str].connect(func)
        q.setPlaceholderText(startValue)
        self.grid.addWidget(q,x,1,1,2)






    #Functions
    def _set_sigmaSmooth(self, text):self.sigmaSmooth=text
    def _set_thresMembra(self, text):self.thresMembra=text
    def _viewResults(self):ATMA.GUI.DataVisualizer.segmentation( self.res )
    def _viewPrediction(self):ATMA.GUI.DataVisualizer.rawSlider( self.pre )

    def test(self):pass

    def _openFile(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home/')
        self.predictionData = h5py.File(self.fname)["volume/data"]

    def _clear(self):
        self.M.visualization.clear()

    def _demo(self):
        self.M.visualization.update_plot()

    def _run(self):

        A=ATMA.CLT()
        A.sigmaSmooth = self.sigmaSmooth
        A.thresMembra = self.thresMembra

        #for debugging, remove in final version!
        A.predictionData = h5py.File("./tests/data/Volume001.h5")["volume/data"]
        A.sizeFilter = [20,1000]

        A.run()
        print "--Done--"

        self.res = A.res
        self.pre = A.predictionData[:,:,:,0]
