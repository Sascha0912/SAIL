import numpy as np
import pandas as pd

def getValidInds(indPool, testFunction, nDesired):
    def any(df): # any is nonzero - equivalent to MATLAB "any"
        for index, row in df.iterrows():
            if row[0]==True or row[0]==1:
                return True
            else:
                continue
        return False
    inds = []
    vals = []
    nMissing = nDesired
    nAttempts = 0

    # print(indPool)
    # print(testFunction)
    # print(nDesired)

    while nMissing > 0:
        # Get Next in Pool to test
        testStart = nAttempts+1
        # print("nAttempts: " + str(nAttempts))
        testEnd = min(indPool.shape[0], nAttempts+nMissing)
        # print("TestStart: " + str(testStart))
        # print("TestEnd: " + str(testEnd))
        if testStart > testEnd:
            break
        nextInd = indPool[testStart:testEnd,:]
        # nextInd hat immer gleiche Länge und Inhalt -> durchmischen?
        # print("nextInd")
        # print(nextInd)
        # Test for validity
        result = testFunction(nextInd) # Must return a [nInds x nVals] matrix

        # Assign valid solutions
        # validInds = np.where()# any isnan TODO
        # print("result")
        # print(result[:, np.newaxis])
        result_df = pd.DataFrame(data=result[:, np.newaxis])
        # print("result_df")
        # print(result_df)
        not_isnan = pd.DataFrame(data=~np.isnan(result_df))
        s = not_isnan.loc[:,0]
        validInds = s.to_numpy().nonzero() # liefert Indizes der validen Einträge
        # print(type(validInds))
        # any_value = any(not_isnan)
        # print("any_value")
        # print(any_value)
        # validInds = np.nonzero(~np.isnan(result))
        # print("isnan")
        # print(isnan)

        idx_list = validInds[0]
        # print(idx_list)

        vals_df = pd.DataFrame(data=vals)
        # print(vals_df)
        res_val_df = result_df.loc[idx_list]
        # print(res_val_df)
        vals_df = vals_df.append(res_val_df)

        # print(vals_df)

        # print(nextInd)
        nextInd_df = pd.DataFrame(data=nextInd)
        # print(nextInd_df)

        inds_df = pd.DataFrame(data=inds)
        nextInd_inds_df = nextInd_df.loc[idx_list]
        inds_df = inds_df.append(nextInd_inds_df)
        # print(inds_df)




        # vals = [[vals], [result[validInds,:]]] # vals_df
        # inds = [[inds], [nextInd[validInds,:]]]

        # Retry
        print(nDesired)                                     # nDesired bleibt bei 100 und ändert sich nicht   -> sollte aber stetig sinken von 100 auf 1 zb 100,99,99,98,97,...
        # print(vals_df.shape[0])                           # vals_df shape 0 sinkt 100,99,0,99,0,1,0000-....
        nMissing = nDesired - vals_df.shape[0]
        
        nAttempts = nAttempts + nextInd_df.shape[0]
        # print(nAttempts)

    return inds_df, vals_df, nMissing, nAttempts
