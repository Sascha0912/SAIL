import numpy as np
import numpy.matlib
import pandas as pd
import sys
from pprint import pprint

def createMap(featureResolution, genomeLength, *args):
    class Map:
        def __init__(self):
            self.edges = []
            self.fitness = None
            self.genes = None
            
    edges = []
    map = Map()

    for i in range(0,len(featureResolution)):
        edges.insert(i, np.linspace(-2,2,featureResolution[i]+1)) # TODO: make generic!

    map.edges = edges

    blankMap = np.empty(featureResolution)
    blankMap[:] = np.nan
    map.fitness = blankMap
    map.genes = []
    # print("genomeLength " + str(genomeLength))
    
    # repmat
    # for i in range(0,genomeLength):
    #     map.genes.append(pd.DataFrame(data=blankMap))
    for i in range(0,genomeLength):
        map.genes.append(pd.DataFrame(data=blankMap).copy())

    # print(map.genes[0]._is_view)
    # print(map.genes[1]._is_view)

    # map.genes = np.tile(blankMap, [1,1,genomeLength])
    # print("map.genes")
    
    # Debugging
    # np.set_printoptions(threshold=sys.maxsize)
    # print(map.genes)
    # print(map.genes.shape)

    if args:
        # print("args")
        # print(args)
        for iValues in range(0,len(args[0])):
            exec('map.'+args[0][iValues]+'=blankMap.flatten("F")') # put already reshaped matrices for drag and confidence in map
        # pprint(vars(map))
    
    return map, edges