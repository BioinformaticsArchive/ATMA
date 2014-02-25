from PyQt4 import QtCore, QtGui

class TrainingWidget(QtGui.QDialog):

    def __init__(self, parent=None):
        super(NodeDetection, self).__init__(parent)
        self.grid = QtGui.QGridLayout()

        self.a=[]
        for i in range(12):
            self.a.append(0)
        self.i=0
        
        self.k=3
        b={}
        self.w={}
        for X in range(self.k):
            for Y in range(self.k):
                x, y = 2*X, 2*Y

                b[x,y,1]= QtGui.QPushButton(self)
                b[x,y,2]= QtGui.QPushButton(self)

                b[x,y,1].setText("Node of Ranvier")
                b[x,y,2].setText("Non")

                self.connect(b[x,y,1], QtCore.SIGNAL("clicked()"), lambda arg=[x,y,1]: self.clicked(arg))
                self.connect(b[x,y,2], QtCore.SIGNAL("clicked()"), lambda arg=[x,y,2]: self.clicked(arg))

                self.w[x,y]= QtGui.QTextBrowser(self)
                self.w[x,y].append("This is a QTextBrowser!")

                self.grid.addWidget(b[x,y,1],1+x,0+y,1,1)
                self.grid.addWidget(b[x,y,2],1+x,1+y,1,1)
                self.grid.addWidget(self.w[x,y],0+x,0+y,1,2)

        next = QtGui.QPushButton(self)
        next.setText("Next Examples")
        self.connect(next, QtCore.SIGNAL("clicked()"), lambda arg='': self.clickNext(arg))
        self.grid.addWidget(next,self.k*self.k,0,1,2*self.k)

                        
        self.setGeometry(2300, 0, 1250, 850)
        self.setLayout(self.grid)

    def clicked(self,arg):
        print self.axons.shape
        [x,y,l] = arg
        x/=2
        y/=2
        id = self.k*x+y+self.i
        print id,l

    def clickNext(self,arg):
        for X in range(self.k):
            for Y in range(self.k):
                x, y = 2*X, 2*Y
                self.w[x,y].append(str(self.i))
                self.i+=1
