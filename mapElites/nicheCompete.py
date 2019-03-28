import numpy as np
from mapElites.getBestPerCell import getBestPerCell
from pprint import pprint
import pandas as pd

def nicheCompete(newInds, fitness, map, d):
    # print("map[0].edges")
    # print(map[0].edges)
    # print("newInds")
    # print(newInds)
    # print("fitness")
    # print(fitness)

    # Hier checken, ob bestIndex und mapLinIndx korrekt sind
    # print("newInds")
    # print(newInds)
    # print("fitness")
    # print(fitness)
    # print("map[0].edges")
    # print(map[0].edges)
    # pprint(vars(map[0]))
    bestIndex, bestBin = getBestPerCell(newInds, fitness, d, map[0].edges) # in getBestPerCell liegt wahrscheinlich der Fehler
    # print("bestIndex")
    # print(bestIndex)
    # print("bestBin")
    # print(bestBin)
    # print(bestBin.iloc[:,0])
    # print("d.featureRes")
    # print(d.featureRes)
    mapLinIndx = np.ravel_multi_index((bestBin.iloc[:,0], bestBin.iloc[:,1]),dims=d.featureRes, order='C')
    # print("mapLinIndx")
    # print(mapLinIndx)

    # TODO: nan feature check

    # Compare to already existing samples
    improvement = []
    
    # print("mapLinIndx")
    # print(mapLinIndx)
    re_fitness = map[0].fitness.reshape((map[0].fitness.shape[0] * map[0].fitness.shape[1], 1))
    # print("re_fitness")
    # print(re_fitness)
    for i in zip(bestIndex,mapLinIndx):
        # print(i)
        if (np.isnan(fitness[i[0]])):
            improvement.append(False)
            continue
        if (fitness[i[0]] >= re_fitness[i[1]]):
            improvement.append(False)
        else:
            improvement.append(True)

    
    df_fitness = pd.DataFrame(data=fitness.transpose())
    # print("df_fitness")
    # print(df_fitness)
    improvement = ~np.greater_equal(df_fitness.iloc[0][bestIndex],re_fitness[mapLinIndx].transpose().ravel())
    # print("bestIndex")
    # print(bestIndex)
    # print("improvement")
    # print(improvement)
    replacement = [bestIndex[i] for i in range(len(bestIndex)) if improvement[improvement.index.values.tolist()[i]]]
    replaced    = mapLinIndx[improvement.tolist()]
    return replaced, replacement, mapLinIndx
    # fitness_bestIndex = (fitness[i] for i in bestIndex)
    # mapfit_Index = (map.fitness[i] for i in mapLinIndx)
    # improvement = ~(fitness_bestIndex >= mapfit_Index)
    # print("improvement")
    # print(improvement)