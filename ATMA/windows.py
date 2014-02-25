#from PyQt4 import QtCore, QtGui
from GUI import *
import Training

class Labeling(QtGui.QDialog):
    Ginitial = 0

    def __init__(self, parent=None):
        super(Labeling, self).__init__(parent)
        self.grid = QtGui.QGridLayout()
        


        self.a=[]
        for i in range(12):
            self.a.append(0)
        self.i=0
        
        self.k=3
        b={}
        self.Maya={}
        for X in range(self.k):
            for Y in range(self.k):
                x, y = 2*X, 2*Y

                b[x,y,1]= QtGui.QPushButton(self)
                b[x,y,2]= QtGui.QPushButton(self)

                b[x,y,1].setText("Node of Ranvier")
                b[x,y,2].setText("Non")

                self.connect(b[x,y,1], QtCore.SIGNAL("clicked()"), lambda arg=[x,y,1]: self.clicked(arg))
                self.connect(b[x,y,2], QtCore.SIGNAL("clicked()"), lambda arg=[x,y,2]: self.clicked(arg))

                #self.w[x,y]= QtGui.QTextBrowser(self)
                self.Maya[x,y] = MayaviQWidget(self)
                #self.w[x,y].append("This is a QTextBrowser!")

                self.grid.addWidget(b[x,y,1],1+x,0+y,1,1)
                self.grid.addWidget(b[x,y,2],1+x,1+y,1,1)
                self.grid.addWidget(self.Maya[x,y],0+x,0+y,1,2)

        next = QtGui.QPushButton(self)
        next.setText("Next Examples")
        self.connect(next, QtCore.SIGNAL("clicked()"), lambda arg='': self.clickNext(arg))
        self.grid.addWidget(next,self.k*self.k,0,1,2*self.k)

                        
        self.setGeometry(2300, 0, 1250, 850)
        self.setLayout(self.grid)


    def clicked(self,arg):
        
        [x,y,l] = arg
        x/=2
        y/=2
        id = self.k*x+y+self.i
        print id,l

    def clickNext(self,arg):
        if self.Ginitial==0:
            self.Ginitial = 1
            print "initial"

            self.Labels=[]
            self.Features=[]
            self.g = Training.GapDetection()
            self.g.pred_volume = self.pre 
            self.g.gaps = self.gaps

            self.g.calcGapList()
        F,E = self.g.GetExamples()
        for V in E:
            print V.shape
        print len(F)
        self.Maya[2,2].visualization.update_plot()



        print self.axons.shape
        print self.pre.shape
        x0,x1,y0,y1,z0,z1 = self.Range
        print x0,y0,z0

        for X in range(self.k):
            for Y in range(self.k):
                x, y = 2*X, 2*Y
                #self.w[x,y].append(str(self.i))
                #self.i+=1
