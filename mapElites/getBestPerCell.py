import numpy as np
import pandas as pd
from domain.rastrigin.rastrigin_Categorize import rastrigin_Categorize

def getBestPerCell(samples,fitness,d,edges):
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
    a = df_bin.append(fitness.iloc[0], ignore_index=True).transpose()
    sortedByFeatureAndFitness = a.sort_values(by=[0,1,2])

    indxSortOne = list(sortedByFeatureAndFitness.index.values)
    df_drop_dupl = sortedByFeatureAndFitness.drop_duplicates(subset=[0,1])
    indxSortTwo = list(df_drop_dupl.index.values)

    bestIndex = indxSortTwo
    bestBin = pd.DataFrame(data=df_bin[bestIndex])

    return bestIndex, bestBin