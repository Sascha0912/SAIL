import numpy as np
import numpy.matlib

def createMap(featureResolution, genomeLength, *args):
    class Map:
        def __init__(self):
            self.edges = []
    edges = []
    map = Map()

    for i in range(0,len(featureResolution)):
        edges.insert(i, np.linspace(0,1,featureResolution[i]+1)) # check +1

    map.edges = edges

    blankMap = np.empty(featureResolution)
    blankMap[:] = np.nan
    map.fitness = blankMap
    map.genes = np.matlib.repmat(blankMap, 1, genomeLength)

    if args:
        for iValues in range(0,len(args[0])):
            exec('Map.'+args[0][iValues]+'=property(blankMap)')
    
    return map, edges