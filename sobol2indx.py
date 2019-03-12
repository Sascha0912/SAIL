import sobol_seq
import numpy as np
def sobol2indx(sobSet, sobPoints, d, edges):
    sampleCoords = sobol_seq#...
    binIndx = np.nan(len(sobPoints), d.nDims)
    for iDim in range(0,d.nDims):
        binIndx[:,iDim] = np.digitize(sampleCoords[:,iDim], edges[iDim])
    
    mapLinIndx = np.ravel_multi_index(binIndx[:,0], binIndx[:,1], dims=d.featureRes, order='F')
    
    return mapLinIndx, binIndx