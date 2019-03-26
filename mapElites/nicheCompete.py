import numpy as np
from mapElites.getBestPerCell import getBestPerCell

def nicheCompete(newInds, fitness, map, d):
    bestIndex, bestBin = getBestPerCell(newInds, fitness, d, map.edges)
    mapLinIndx = np.ravel_multi_index((bestBin[:,0], bestBin[:,1]),dims=d.featureRes, order='F')

    # TODO: nan feature check

    # Compare to already existing samples
    fitness_bestIndex = (fitness[i] for i in bestIndex)
    mapfit_Index = (map.fitness[i] for i in mapLinIndx)
    improvement = ~(fitness_bestIndex >= mapfit_Index)
    print("improvement")
    print(improvement)