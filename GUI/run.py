from qt_embedding import *
import ATMA


class ATMA_GUI(QtGui.QWidget):
    def __init__(self):
        super(ATMA_GUI,self).__init__()
        self.initUI()

    def initUI(self):

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(18)

        #Buttons
        self._button(0, 0, 1, 1, self.openFile, "Open File" )
        self._button(1, 0, 1, 1, self.clear,    "Clear"     )
        self._button(2, 0, 1, 1, self.demo,     "Demo"      )


        #Maya Widget
        self.M = MayaviQWidget(self)
        self.grid.addWidget(self.M, 0, 3,18,1)

        #Layout
        self.setGeometry(2300, 0, 1250, 650)
        self.setLayout(self.grid)
        self.setWindowTitle('ATMA')
        self.show()


    #Widgets
    def _button(self,x,y,w,t,func,title):
        b = QtGui.QPushButton(title,self)
        b.clicked.connect(func)
        self.grid.addWidget(b,x,y,w,t)


    #Functions
    def openFile(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file','/home/')

    def clear(self):
        self.M.visualization.clear()

    def demo(self):
        self.M.visualization.update_plot()

def main():
    app = QtGui.QApplication.instance()
    ex = ATMA_GUI()
    app.exec_()

if __name__ == '__main__':


    main()

