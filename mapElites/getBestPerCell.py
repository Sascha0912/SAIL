import numpy as np
import pandas as pd

def getBestPerCell(samples,fitness,d,edges):
    def feval(funcName,*args):
        return eval(funcName)(*args)
    # Get features of all samples
    feature = feval(d.categorize, samples, d)
    for iDim in range(0,d.nDims):
        bin[:][iDim] = np.digitize(feature[:][iDim], edges[iDim])
    
    df_bin = pd.DataFrame(data=bin)
    a = df_bin.append(fitness.iloc[0], ignore_index=True).transpose()
    sortedByFeatureAndFitness = a.sort_values(by=[0,1,2])

    indxSortOne = list(sortedByFeatureAndFitness.index.values)
    df_drop_dupl = sortedByFeatureAndFitness.drop_duplicates(subset=[0,1])
    indxSortTwo = list(df_drop_dupl.index.values)

    bestIndex = indxSortTwo
    bestBin = pd.DataFrame(data=df_bin[bestIndex])

    return bestIndex, bestBin