import numpy
from mayavi import mlab
from ColorTable import *


def segmentation(binData):

    #binData=binData%len(ColorTable)
    #faster but less colors
    binData = (binData!=0) + (binData%5)
    Components = numpy.unique(binData)
    l = len(Components)
    for i,c in enumerate(Components):
        print i+1,'/',len(Components)
        if c==0:continue

        col=int(c%len(ColorTable))
        r,g,b=ColorTable[col]

        tmp=numpy.array(binData==c,dtype=numpy.uint8)
        src = mlab.pipeline.scalar_field(tmp)
        mlab.pipeline.iso_surface(src,color=(r,g,b))



def rawSlider(rawData):

    bg=numpy.array(rawData,dtype=numpy.float32)
    S=numpy.array(bg.shape)/2
    src = mlab.pipeline.scalar_field(bg)
    for a in ["x_axes","y_axes","z_axes"]:
        for o in [S]:
            cut_plane = mlab.pipeline.scalar_cut_plane(src,
                                        plane_orientation=a,
                                        colormap='black-white')
            cut_plane.implicit_plane.origin = o
            cut_plane.implicit_plane.widget.enabled = True

def points(x,y,z):
    x=[x]
    y=[y]
    z=[z]
    s=[1]
    #x 
    #dd= sin(2 * t)*100
    #y = cos(t)*100
    #z = cos(2 * t)*50
    #s = 2 + sin(t)
    mlab.points3d(x, y, z, s, 
            transparent=True,
            opacity=0.2,
            color=(0,0,1),
            scale_factor=15
            )
