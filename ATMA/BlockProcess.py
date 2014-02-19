import numpy as np
import vigra
from scipy import ndimage
import time
import re
import h5py
from GapClosing.DataStructures import UnionFinder as UF

from multiprocessing import Process, Lock
import multiprocessing



class BlockProcess():

    helo       = 30
    Sub_Volume = 0
    IN         = 0
    OUT_RAW   = 0
    OUT_RESULT = 0
    Workers     = 8
    QTbar     = 0
    Sub_Volume = None
    verbose = 0

    def __init__(self):pass


    def _calcWorkingArray3d(self):
        self.BLOCKS=[]

        [[sx0,sx1],[sy0,sy1],[sz0,sz1]]=self.Sub_Volume
        S0,S1,S2=sx1-sx0,sy1-sy0,sz1-sz0
        n_blocks = [S0,S1,S2]/np.array(self.blockSize)
        bX,bY,bZ    = self.blockSize

        self.b,self.B,self.h=[],[],[]
        for z in range(n_blocks[2]+1):
            z0=max(0,z*bZ)
            z1=min((z+1)*bZ,S2)
            if z0==z1:continue
            hz1=min(z1+self.helo,S2)-z1
            hz0=max(z0-self.helo,0)-z0
            Z0=z0+hz0
            Z1=z1+hz1
            for x in range(n_blocks[0]+1):
                x0=max(0,x*bX)
                x1=min((x+1)*bX,S0)
                if x0==x1:continue
                hx1=min(x1+self.helo,S0)-x1
                hx0=max(x0-self.helo,0)-x0
                X0=x0+hx0
                X1=x1+hx1
                for y in range(n_blocks[1]+1):
                    y0=max(0,y*bY)
                    y1=min((y+1)*bY,S1)
                    if y0==y1:continue
                    hy1=min(y1+self.helo,S1)-y1
                    hy0=max(y0-self.helo,0)-y0
                    Y0=y0+hy0
                    Y1=y1+hy1

                    WD=np.array([x0+sx0,x1+sx0,y0+sy0,y1+sy0,z0+sz0,z1+sz0])
                    frame =np.array([hx0,hx1,hy0,hy1,hz0,hz1])
                    FD = WD + frame
                    FR = np.array([X0,X1,Y0,Y1,Z0,Z1])
                    WR = np.array([x0,x1,y0,y1,z0,z1])
                    self.BLOCKS.append((frame,FD,WD,FR,WR))

    def _ProcessBlock(self,data,i,R,r,h,UnionF,l):
        res=self.Process(data)

        #Prozess Sub-block
        tmp_res  =  np.array(res,dtype=np.uint32)
        B=((i+1)*(2**16))
        tmp_res[tmp_res!=0] += B


        #Write Results
        l.acquire()
        #Union = open(self.path_out+"_uni.txt",'a+')
        outF = h5py.File(self.path_out[0], "r+")
        outF.create_dataset(str(i), data=tmp_res)

        out=outF["volume/data"]

        S=tmp_res.shape
        tmp_old  = out[R[0]:R[1],R[2]:R[3],R[4]:R[5]]
        out[r[0]:r[1],r[2]:r[3],r[4]:r[5]]=tmp_res[-h[0]:S[0]-h[1],-h[2]:S[1]-h[3],-h[4]:S[2]-h[5]]
        outF.close()

        l.release()

    def _calcUnions(self):
        outF = h5py.File(self.path_out[0], "r+")
        self.Unions=[]

        v=2
        for i in range(len(self.BLOCKS)):

            h,D,d,R,r=self.BLOCKS[i]
            tmp_res = outF[str(i)][::v,::v,::v]
            tmp_old = outF["volume/data"][R[0]:R[1]:v,R[2]:R[3]:v,R[4]:R[5]:v]
            Picks=np.unique(tmp_old)

            for c in Picks:
                if c==0:continue
                bins = tmp_res[tmp_old==c]
                bins = bins[bins!=0]
                if len(bins)<self.helo*5:continue
                counts = np.bincount(bins)
                over=np.argmax(counts)
                self.Unions.append([over,c])

        outF.close()

        #Unionfinder
        a=UF(self.Unions)
        a.calcGroupIDs()
        self.G = a.GroupIDs

    def _AssignIDS(self,l,i):
        h,D,d,R,r=self.BLOCKS[i]

        l.acquire()
        outF = h5py.File(self.path_out[0], "r+")
        out=outF["volume/data"]
        tmp      = np.copy(out[ r[0]:r[1], r[2]:r[3], r[4]:r[5]])
        outF.close()
        l.release()

        for c in np.unique(tmp):
            try:
                id=self.G[c]
            except KeyError:
                id=c
            tmp[tmp==c]=id


        ske=[]
        for L in range(tmp.shape[2]):
            Layer=tmp[:,:,L]
            for c in np.unique(Layer):
                if c==0:continue
                tmpL=Layer==c
                S=np.sum(tmpL)
                X,Y = ndimage.measurements.center_of_mass(tmpL)
                X,Y,Z = [X,Y,L]+np.array([r[0],r[2],r[4]])
                ske.append([Z,c,S,X,Y])
        #ske=np.array(ske)
        l.acquire()
        f = open(self.path_out[0]+"_ske.txt", 'a')
        for Z,c,S,X,Y in ske:
                f.write(str(int(Z))+','+\
                        str(int(c))+','+\
                        str(S)+','+\
                        str(X)+','+\
                        str(Y)+','+\
                        '\n')


        outF = h5py.File(self.path_out[0], "r+")
        out=outF["volume/data"]
        out[ r[0]:r[1], r[2]:r[3], r[4]:r[5]]=tmp
        outF.close()
        f.close()
        l.release()

    def run(self):
        self.path_pre= h5py.File(self.path_in[0])[self.path_in[1]]
        lock = Lock()
        self.REMAP=[]

        #Set Range
        if np.any(self.Sub_Volume==None):
            S=self.path_pre.shape
            self.Sub_Volume=[[0,S[0]],[0,S[1]],[0,S[2]]]
        [[sx0,sx1],[sy0,sy1],[sz0,sz1]]=self.Sub_Volume
        S0,S1,S2=sx1-sx0,sy1-sy0,sz1-sz0



        #create block grid
        self._calcWorkingArray3d()



        #Initial Files
        UnionF = open(self.path_out[0]+"_uni.txt", 'w+')
        UnionF.close()

        outF = h5py.File(self.path_out[0], "w")
        outF.create_dataset(self.path_out[1], (S0,S1,S2), dtype=np.uint32)
        outF.close()

        f = open(self.path_out[0]+"_ske.txt", 'w')

        #Process Parallel
        for i in range(len(self.BLOCKS)):
            if self.verbose==1:
                print "Processing:",i+1,len(self.BLOCKS)
            if self.QTbar!=0:
                self.QTbar.setValue(70*(i+1)/len(self.BLOCKS))
            h,D,d,R,r=self.BLOCKS[i]
            data = self.path_pre[D[0]:D[1],D[2]:D[3],D[4]:D[5],:]
            Process(target=self._ProcessBlock, args=(data,i,R,r,h,UnionF,lock)).start()
            while len(multiprocessing.active_children())>=self.Workers:
                time.sleep(1)

        while len(multiprocessing.active_children())!=0:
            time.sleep(1)

        self._calcUnions()

        f.close()
        for i in range(len(self.BLOCKS)):
            if self.verbose==1:
                print "Saveing:",i+1,len(self.BLOCKS)
            if self.QTbar!=0:
                self.QTbar.setValue(70+(30*(i+1))/len(self.BLOCKS))

            Process(target=self._AssignIDS,args=(lock,i)).start()
            while len(multiprocessing.active_children())>=self.Workers:
            #while len(multiprocessing.active_children())>=1:
                time.sleep(1)

        while len(multiprocessing.active_children())!=0:
            time.sleep(1)

        self.res=h5py.File(self.path_out[0])[self.path_out[1]]