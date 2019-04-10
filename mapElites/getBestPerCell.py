import numpy as np
import pandas as pd
from domain.rastrigin.rastrigin_Categorize import rastrigin_Categorize

# param: maximize indicates whether to search for max. fitness or not (min search)
def getBestPerCell(samples,fitness,d,edges,maximize=True):
    def feval(funcName,*args):
        return eval(funcName)(*args)
    fitness = pd.DataFrame(data=fitness)
    # print("samples")
    # print(samples)
    # print("fitness")
    # print(fitness)
    # print("edges")
    # print(edges)
    # Get features of all samples
    feature = feval(d.categorize, samples, d)
    # print("feature")
    # print(feature)
    # print("feature")
    # print(feature)

    for iDim in range(0,d.nDims):
        if ("df_bin" in locals()):
            df_add = pd.DataFrame(data=np.digitize(feature.iloc[:,iDim], edges[iDim]))
            df_bin = pd.concat([df_bin,df_add], axis=1)
        else:
            df_bin = pd.DataFrame(data=np.digitize(feature.iloc[:,iDim], edges[iDim]))
        # bin[:][iDim] = np.digitize(feature.iloc[:,iDim], edges[iDim])
    # print("df_bin")
    # print(df_bin)
    # df_bin = pd.DataFrame(data=bin)
    fitness = pd.DataFrame(data=fitness)
    # print("fitness")
    # print(fitness)
    # a = df_bin.append(fitness.iloc[0], ignore_index=True)
    a = pd.concat([df_bin, fitness], axis=1)
    a.columns = range(a.shape[1])
    # print("a")
    # print(a)
    sortedByFeatureAndFitness = a.sort_values(by=[0,1,2])
    # print("sortedByFeatureAndFitness")
    # print(sortedByFeatureAndFitness)

    indxSortOne = list(sortedByFeatureAndFitness.index.values)
    # print("indxSortOne")
    # print(indxSortOne)

    # sortedByFeatureAndFitness.reset_index(drop=True, inplace=True)
    if (maximize):
        df_drop_dupl = sortedByFeatureAndFitness.drop_duplicates(subset=[0,1], keep='first')
    else:
        df_drop_dupl = sortedByFeatureAndFitness.drop_duplicates(subset=[0,1], keep='last')
    
    indxSortTwo = list(df_drop_dupl.index.values)

    # print("indxSortTwo")
    # print(indxSortTwo)

    bestIndex = indxSortTwo
    bestBin = pd.DataFrame(data=df_bin.iloc[bestIndex,:])
    # print("bestBin")
    # print(bestBin)

    return bestIndex, bestBin # works