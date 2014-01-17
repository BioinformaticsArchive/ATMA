import re
import numpy
from mayavi import mlab
from ColorTable import *





if __name__ == '__main__':
    Axon={}
    i=0
    with open("../../../res/ske.txt", "r") as f:
        while f.readline():
            i+=1
            print i
            #if i == 10000:break
            x = map(float, re.findall(r"[-+]?\d*\.\d+|\d+", f.readline()))
            if len(x)==0:continue
            [Z,ID,S,X,Y]=x[:5]
            if ID==0:continue
            try:
                Axon[ID].append(numpy.array([X,Y,Z,S]))
            except KeyError:
                Axon[ID]=[]
                Axon[ID].append(numpy.array([X,Y,Z,S]))


    n=0
    for A in Axon:
        X,Y,Z,S=[],[],[],[]
        for i in Axon[A]:
            X.append(i[0])
            Y.append(i[1])
            Z.append(i[2])
            S.append(i[3])

        n+=1
        if len(X)>1200:continue
        if len(X)<100:continue
        print n,len(Axon)
        col=int(A%numpy.uint(len(ColorTable)))
        r,g,b=ColorTable[col]

        Z,X,Y,S=zip(*sorted(zip(Z,Y,X,S)))

        z_tmp,y_tmp,x_tmp,s_tmp=[],[],[],[]
        z_res,y_res,x_res,s_res=[],[],[],[]
        i=0
        for z,s,x,y in zip(Z,S,X,Y):
            z_tmp.append(z)
            y_tmp.append(y)
            x_tmp.append(x)
            s_tmp.append(s)
            i+=1
            if i==10:
                i=0
                z_res.append(numpy.mean(z_tmp))
                y_res.append(numpy.mean(y_tmp))
                x_res.append(numpy.mean(x_tmp))
                s_res.append(numpy.mean(s_tmp))
                z_tmp,y_tmp,x_tmp,s_tmp=[],[],[],[]


        Z,Y,X,S=z_res,y_res,x_res,s_res
        if len(X)!=0:
            mlab.plot3d(X, Y, Z, tube_radius=(numpy.mean(S)/3.14)**(0.5), colormap='Spectral',color=(r,g,b))
    mlab.show()
