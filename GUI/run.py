from qt_embedding import *
import h5py
import numpy #can be removed
import ATMA


class ATMA_GUI(QtGui.QWidget):

    def __init__(self):
        super(ATMA_GUI,self).__init__()
        self.initUI()


    def initUI(self):

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(18)

        #Buttons
        self._button(0, 0, 1, 1, self._openFile,    "Open File"         )
        self._button(2, 0, 1, 1, self._clear,       "Clear"             )
        self._button(3, 0, 1, 1, self._demo,        "Demo"              )
        self._button(4, 0, 1, 1, self._viewResults, "View Results"      )
        self._button(5, 0, 1, 1, self._viewPrediction, "View Prediction")
        self._button(17,0, 1, 1, self._run, "Run"      )
        self._label(6, 0, 1, 1, self._set_sigmaSmooth, "Smoothing" , "0.7")
        self._label(8, 0, 1, 1, self._set_thresMembra, "Thrashold" , "0.7")

        #Maya Widget
        self.M = MayaviQWidget(self)
        self.grid.addWidget(self.M, 0, 1,18,2)

        #Layout
        self.setGeometry(2300, 0, 1250, 650)
        self.setLayout(self.grid)
        self.setWindowTitle('ATMA')
        self.show()


    #Widgets
    def _label(self,x,y,w,t,func, title, startValue):

        q = QtGui.QLineEdit(self)
        q.textChanged[str].connect(func)
        q.setPlaceholderText(startValue)


        l = QtGui.QLabel(self)
        l.setText(title)

        self.grid.addWidget(l,x,y,w,t)
        self.grid.addWidget(q,x+1,y,w,t)
        func(float(startValue))


    def _button(self,x,y,w,t,func,title):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,y,w,t)

    #Functions
    def _set_sigmaSmooth(self, text):self.sigmaSmooth=float(text)
    def _set_thresMembra(self, text):self.thresMembra=float(text)
    def _viewResults(self):ATMA.GUI.DataVisualizer.segmentation( self.res )
    def _viewPrediction(self):ATMA.GUI.DataVisualizer.rawSlider( self.pre )

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


def main():
    app = QtGui.QApplication.instance()
    ex = ATMA_GUI()
    app.exec_()


if __name__ == '__main__':


    main()

