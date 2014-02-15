import numpy
import vigra


def thresholdSegmentation(data,smoothingLevel,thresholdLevel):

    # Apply gaussian smoothing
    if smoothingLevel==0:
        smo = numpy.copy(data)
    else:
        smo = vigra.gaussianSmoothing(data,smoothingLevel)

    # Apply thresholding
    res=smo>thresholdLevel

    return res


def invertVolume2D(data,sizeFilter=[2,1000]):

    res=numpy.zeros(data.shape)

    #invert each layer
    for z in range(res.shape[2]):
        layer  = vigra.Image( data[:,:,z] )
        layer  = vigra.analysis.labelImageWithBackground(1-layer)
        feat   = vigra.analysis.extractRegionFeatures(\
                vigra.Image(layer)\
                ,numpy.array(layer),[\
                'Count',\
                'Mean'\
                ])

        #Remove BG
        Valid1=feat["Mean"][numpy.argwhere(feat["Count"]>sizeFilter[0]).T[0]]
        Valid2=feat["Mean"][numpy.argwhere(feat["Count"]<sizeFilter[1]).T[0]]
        Valid=numpy.intersect1d(Valid1,Valid2)
        tmp=numpy.zeros(layer.shape)
        for c in Valid:
            if c==0:continue
            tmp_c=(layer==c)
            res[:,:,z][tmp_c]=1

    return res


def rayFeatures( data, rayLength ):
    S = data.shape
    L = rayLength
    DATA=numpy.zeros((S[0]+2*L,S[1]+2*L,S[2]+2*L))
    DATA[L:-L,L:-L,L:-L]=data

    res_tmp=numpy.zeros((S[0],S[1],S[2],8))

    for i in range(3,L):
        n=0
        for x in [-1,1]:
            for y in [-1,1]:
                for z in [-1,1]:
                    res_tmp[:,:,:,n]=numpy.maximum(res_tmp[:,:,:,n],DATA[L+i*x:-L+i*x,L+i*y:-L+i*y,L+i*z:-L+i*z])
                    n+=1
    median=numpy.median(res_tmp,axis=3)
    return median


def multiHessian( data, scales ): 
    for r in scales:

        hes=vigra.filters.hessianOfGaussianEigenvalues(vigra.Volume(data),r)
        hes=numpy.sort(numpy.abs(hes),axis=3)
        l1=hes[:,:,:,0]
        l2=hes[:,:,:,1]
        l3=hes[:,:,:,2]

        K = 1 - numpy.abs(l2-l3) / (l2-l3)
        tmp=-K*(2/3*l1-l2-l3)


        tmp=tmp*( (r)**2 )
        if r==scales[0]:
            res=tmp
        else:
            res = numpy.maximum( res, tmp )

    res[numpy.isnan(res)]=0
    return res

def waterSeg( data1, data2, th, dist ):
    data2 = vigra.Volume( data2 )
    M = data2>th
    O=vigra.filters.distanceTransform3D(vigra.Volume(M==1))
    O=O>dist
    S=2*M+O
    S=numpy.array(S,dtype=numpy.uint32)
    res=vigra.analysis.watersheds(data1 ,method = 'RegionGrowing',seeds=S)[0]==2
    return res



