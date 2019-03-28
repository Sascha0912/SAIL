import numpy as np
import numpy.matlib
import sys

def createMap(featureResolution, genomeLength, *args):
    class Map:
        def __init__(self):
            self.edges = []
            self.fitness = None
            self.genes = None
            
    edges = []
    map = Map()

    for i in range(0,len(featureResolution)):
        edges.insert(i, np.linspace(0,1,featureResolution[i]+1)) # check +1

    map.edges = edges

    blankMap = np.empty(featureResolution)
    blankMap[:] = np.nan
    map.fitness = blankMap
    # map.genes = np.matlib.repmat(blankMap, 1, genomeLength)
    map.genes = np.tile(blankMap, [1,1,genomeLength])
    print("map.genes")
    
    np.set_printoptions(threshold=sys.maxsize)
    print(map.genes)
    print(map.genes.shape)

    if args:
        for iValues in range(0,len(args[0])):
            exec('Map.'+args[0][iValues]+'=property(blankMap)')
    
    return map, edges