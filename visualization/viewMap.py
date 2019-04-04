import numpy as np
import matplotlib.pyplot as plt

def viewMap(mapMatrix, d, **kwargs): # varagin == kwargs

    # if (isinstance(mapMatrix, tuple)):
    #     if (isinstance(mapMatrix[0], tuple)):
    #         mapMatrix = mapMatrix[0][0]
    #     else:
    #         mapMatrix = mapMatrix[0]
    # print("mapMatrix")
    # print(mapMatrix)
    # print("mapMatrix.fitness")
    # print(mapMatrix.fitness)
    mapRes = mapMatrix.fitness.shape
    edges = []
    for i in range(0,len(mapRes)):
        edges.append(np.linspace(0,1,mapRes[i]+1))
    
    yOffset = [0.5, -0.0, 0]
    imgHandle = plt.matshow(np.flipud(np.rot90(mapMatrix.fitness)))
    fitPlot = plt.gca()

    for key, value in kwargs.items():
        if value=='flip': # value or key ?
            imgHandle = plt.matshow(np.fliplr(np.rot90(np.rot90(mapMatrix))))
            fitPlot = plt.gca()

    xlab = plt.xlabel(d.featureLabels[0])
    ylab = plt.ylabel(d.featureLabels[1])

    # ...

    plt.colorbar()
    figHandle = fitPlot
    imageHandle = imgHandle
    plt.show()
    return figHandle, imageHandle
