import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.ticker import FormatStrFormatter

def viewMap(mapMatrix, d, **kwargs): # varagin == kwargs

    # if (isinstance(mapMatrix, tuple)):
    #     if (isinstance(mapMatrix[0], tuple)):
    #         mapMatrix = mapMatrix[0][0]
    #     else:
    #         mapMatrix = mapMatrix[0]
    # print("mapMatrix")
    # print(mapMatrix)
    print("mapMatrix.fitness")
    print(mapMatrix.fitness)
    mapRes = mapMatrix.fitness.shape
    edges = []

    fig = plt.figure()
    ax = plt.subplot(111)

    for i in range(0,len(mapRes)):
        edges.append(np.linspace(0,1,mapRes[i])) # ADJUSTSCALE
    
    # yOffset = [0.5, -0.0, 0]
    cax = ax.matshow(np.flipud(np.rot90(mapMatrix.fitness)))
    fitPlot = plt.gca()

    for key, value in kwargs.items():
        if value=='flip': # value or key ?
            imgHandle = plt.matshow(np.fliplr(np.rot90(np.rot90(mapMatrix))))
            fitPlot = plt.gca()

    xlab = plt.xlabel(d.featureLabels[0])
    ylab = plt.ylabel(d.featureLabels[1])

    # ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    # ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax.set_xticks(np.arange(mapRes[0]))
    ax.set_yticks(np.arange(mapRes[1]))

    ax.set_xticklabels( [str(round(float(label),2)) for label in np.linspace(0,1,num=mapRes[0])] ) 
    ax.set_yticklabels( [str(round(float(label),2)) for label in np.linspace(0,1,num=mapRes[1])] )

    # ...



    fig.colorbar(cax)
    figHandle = fitPlot
    imageHandle = cax
    plt.show()
    return figHandle, imageHandle
