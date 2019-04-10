import numpy as np
from mapElites.getBestPerCell import getBestPerCell
from pprint import pprint
import pandas as pd

# newInds - Rastrigin: DataFrame 10x2
# fitness - Rastrigin: 2D List   10x1


def nicheCompete(newInds, fitness, map, d):

    # TODO: Test parameter "maximize" indicates whether to search for maximum fitness or not
    # should be added to domain parameters
    maximizeParam = False




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
    bestIndex, bestBin = getBestPerCell(newInds, fitness, d, map[0].edges, maximize=maximizeParam)
    # print("bestIndex")
    # print(bestIndex)
    # print("bestBin")
    # print(bestBin)
    # print(bestBin.iloc[:,0])
    # print("d.featureRes")
    # print(d.featureRes)
    bestBin = bestBin + (-1)
    # print("bestBinAfter")
    # print(bestBin.T.to_numpy())
    mapLinIndx = np.ravel_multi_index(bestBin.T.to_numpy(),dims=d.featureRes, order='C', mode='clip') # TODO: check here if C or F + mode clip causing incorrect solutions?
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



    # TODO: improvement is when smaller fitness value is found -> depends on param maximizeParam

    # if maximizeParam:
    #     for i in zip(bestIndex,mapLinIndx):
    #         # print(i)
    #         if (np.isnan(fitness[i[0]])):
    #             improvement.append(False)
    #             continue
    #         if (fitness[i[0]] >= re_fitness[i[1]]):
    #             improvement.append(False)
    #         else:
    #             improvement.append(True)
    # else:
    #     for i in zip(bestIndex,mapLinIndx):
    #         # print(i)
    #         if (np.isnan(fitness[i[0]])):
    #             improvement.append(False) # check this
    #             continue
    #         if (fitness[i[0]] >= re_fitness[i[1]]):
    #             improvement.append(True)
    #         else:
    #             improvement.append(False)

    
    df_fitness = pd.DataFrame(data=fitness.transpose())
    # print("df_fitness")
    # print(df_fitness)
    # TODO: vergleich prüfen
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