import numpy as np

def getValidInds(indPool, testFunction, nDesired):
    inds = []
    vals = []
    nMissing = nDesired
    nAttempts = 0

    while nMissing > 0:
        # Get Next in Pool to test
        testStart = nAttempts+1
        testEnd = min(indPool.shape[0], nAttempts+nMissing)
        if testStart > testEnd:
            break
        nextInd = indPool[testStart:testEnd,:]

        # Test for validity
        result = testFunction(nextInd) # Must return a [nInds x nVals] matrix

        # Assign valid solutions
        # validInds = np.where()# any isnan TODO
        print("result")
        print(result)
        # isnan = ~np.isnan(result)
        # print("isnan")
        # print(isnan)

        vals = [[vals], [result[validInds,:]]]
        inds = [[inds], [nextInd[validInds,:]]]

        # Retry
        nMissing = nDesired - vals.shape[0]
        nAttempts = nAttempts + nextInd.shape[0]

    return inds, vals, nMissing, nAttempts
