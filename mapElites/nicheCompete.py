import numpy as np
from mapElites.getBestPerCell import getBestPerCell
from pprint import pprint

def nicheCompete(newInds, fitness, map, d):
    # print("map[0].edges")
    # print(map[0].edges)
    # print("newInds")
    # print(newInds)
    # print("fitness")
    # print(fitness)

    # Hier checken, ob bestIndex und mapLinIndx korrekt sind
    print("newInds")
    print(newInds)
    print("fitness")
    print(fitness)
    print("map[0].edges")
    # print(map[0].edges)
    pprint(vars(map[0]))
    bestIndex, bestBin = getBestPerCell(newInds, fitness, d, map[0].edges) # in getBestPerCell liegt wahrscheinlich der Fehler
    print("bestIndex")
    print(bestIndex)
    print("bestBin")
    print(bestBin)
    
    mapLinIndx = np.ravel_multi_index((bestBin.iloc[:,0], bestBin.iloc[:,1]),dims=d.featureRes, order='F')

    # TODO: nan feature check

    # Compare to already existing samples
    improvement = []
    
    # print("mapLinIndx")
    # print(mapLinIndx)
    for i in zip(bestIndex,mapLinIndx):
        print(i)
        if (fitness[i[0]] >= map[0].fitness[i[1]]):
            improvement.append(False)
        else:
            improvement.append(True)

    # fitness_bestIndex = (fitness[i] for i in bestIndex)
    # mapfit_Index = (map.fitness[i] for i in mapLinIndx)
    # improvement = ~(fitness_bestIndex >= mapfit_Index)
    # print("improvement")
    # print(improvement)