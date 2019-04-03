from sail.sobol_lib import i4_sobol_generate
import numpy as np
import pandas as pd

def sobol2indx(sobSet, sobPoints, d, edges):
    # sobSet is DataFrame
    # sobPoints is list with indices
    # print("sobSet")
    # print(sobSet)
    sampleCoords = sobSet.iloc[sobPoints, :]
    # print("sampleCoords")
    # print(sampleCoords)

    nans = np.empty([len(sobPoints),d.nDims])
    nans[:] = np.nan

    binIndx = pd.DataFrame(data=nans)
    # binIndx = np.nan(len(sobPoints), d.nDims)
    # print("binIndx")
    # print(binIndx)
    # print("edges")
    # print(edges)
    for iDim in range(0,d.nDims):
        binIndx.at[:,iDim] = np.digitize(sampleCoords.iloc[:,iDim], edges[iDim])-1 # CHECK: -1 correct?
    
    # print("binIndx")
    # print(binIndx)
    mapLinIndx = np.ravel_multi_index((binIndx.iloc[:,0], binIndx.iloc[:,1]), dims=d.featureRes, order='F')
    
    return mapLinIndx, binIndx