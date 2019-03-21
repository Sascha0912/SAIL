import numpy as np
import pandas as pd
import types

def getValidInds(indPool, testFunction, nDesired):
    def any(df): # any is nonzero - equivalent to MATLAB "any"
        for index, row in df.iterrows():
            if row[0]==True or row[0]==1:
                return True
            else:
                continue
        return False
    # inds = []
    inds = pd.DataFrame(columns=[0])
    # vals = []
    vals = pd.DataFrame(columns=[0,1])
    nMissing = nDesired
    nAttempts = 0
    # print("indPool")
    # print(indPool)
    # print("testFunction")
    # print(testFunction)
    # print("nDesired")
    # print(nDesired)
    # print("sge")


    # BIS HIER HIN GETESTET


    # print("check loop cond")
    while nMissing > 0:
        # Get Next in Pool to test
        testStart = nAttempts # testStart ist 1 höher als in matlab. problem?
        # 
        # print("testStart")
        # print(testStart)
        # print("nAttempts: " + str(nAttempts))
        testEnd = min(np.shape(indPool)[0], nAttempts+nMissing)-1 # testEnd sinkt in matlab durchgängig 10,10,9,9,8,8,8,7,7,...
        # print("testEnd")
        # print(testEnd)
        # print("TestStart: " + str(testStart))
        # print("TestEnd: " + str(testEnd))
        
        if testStart > testEnd:
            break
        # print("IndPool before")
        # print(indPool)
        indPool = pd.DataFrame(data=indPool)
        # print("IndPool dataframe")
        # print(indPool)
        nextInd = pd.DataFrame(data=indPool.loc[testStart:testEnd])
        # nextInd hat immer gleiche Länge und Inhalt -> durchmischen?
        # print("nextInd")
        # print(nextInd)
        # Test for validity
        # print("testFunction")
        # print(testFunction)
        result = testFunction(nextInd) # Must return a [nInds x nVals] matrix
        # print("result")
        # print(result)

        if isinstance(result, pd.DataFrame):
            # Fall 2: Evaluierung (PreciseEvaluate) -> result ist schon DataFrame
            pass
        else:
            # Fall 1: Validitätsprüfung
            # print("result")
            # print(result)
            result = pd.DataFrame(data=result[:,np.newaxis])
        # Assign valid solutions
        # validInds = np.where()# any isnan TODO
        # print("result")
        # print(result[:, np.newaxis])
        # result_df = pd.DataFrame(data=result[:, np.newaxis])
        # print("result_df")
        # print(result_df)
        not_isnan = pd.DataFrame(data=~np.isnan(result))
        s = not_isnan.loc[:,0]
        validInds = s.to_numpy().nonzero() # liefert Indizes der validen Einträge
        
        # validInds_test = find(any(logical_not(isnan(result)),2))
        # print(type(validInds))
        # any_value = any(not_isnan)
        # print("any_value")
        # print(any_value)
        # validInds = np.nonzero(~np.isnan(result))
        # print("isnan")
        # print(isnan)

        idx_list = validInds[0] # validInds
        # print("idx_list")
        # print(idx_list)
        validInds = pd.DataFrame(data=idx_list[:,np.newaxis])          #CHECKED validInds 100x1 int
        # print("validInds")                                            # CHECKED result 100x1 True
        # print(validInds)                                              # CHECKED nextInd 100x2 samples
        

        # print("result")
        # print(result)
        # print("validInds vlaue to list")
        [unpacked_validInds] = validInds.values.T.tolist()
        # print(unpacked_validInds)
        # print("result")
        # print(result)
        vals_result = result.loc[unpacked_validInds]

        vals_nextInd = nextInd.loc[unpacked_validInds]


        # print("vals_result")
        # print(vals_result)              #             |
                                        # vals_result V
        if vals.empty:
            vals = vals_result
        else:
            # vals = vals_result
            vals = vals.append(vals_result)
        # vals = np.concatenate((vals, np.take(result, validInds)), axis=1)
        if inds.empty:
            inds = vals_nextInd
        else:
            inds = inds.append(vals_nextInd)
            # inds = vals_nextInd
        # inds = np.concatenate((inds, np.take(nextInd, validInds)), axis=0)

        # print("vals")
        # print(vals)

        # print("inds")
        # print(inds)


        # vals_df = pd.DataFrame(data=vals_df)
        # print(vals_df)
        # res_val_df = result_df.loc[idx_list]
        # print(res_val_df)
        # vals_df = vals_df.append(res_val_df)

        # print(vals_df)

        # print(nextInd)
        # nextInd_df = pd.DataFrame(data=nextInd)
        # print(nextInd_df)

        # inds_df = pd.DataFrame(data=inds_df)
        # nextInd_inds_df = nextInd_df.loc[idx_list]
        # inds_df = inds_df.append(nextInd_inds_df)
        # print(inds_df)




        # vals = [[vals], [result[validInds,:]]] # vals_df
        # inds = [[inds], [nextInd[validInds,:]]]

        # Retry
        # print(nDesired)                                     # nDesired bleibt bei 100 und ändert sich nicht   -> sollte aber stetig sinken von 100 auf 1 zb 100,99,99,98,97,...
        # print(vals_df.shape[0])                           # vals_df shape 0 sinkt 100,99,0,99,0,1,0000-....
        nMissing = nDesired - vals.shape[0]
        # print("nMissing: " + str(nMissing))
        nAttempts = nAttempts + nextInd.shape[0] # nAttempts ist immer um 1 zu gross
        # print("nAttempts")
        # print(nAttempts)

    return inds, vals, nMissing, nAttempts
