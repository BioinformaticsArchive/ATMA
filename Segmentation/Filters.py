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
