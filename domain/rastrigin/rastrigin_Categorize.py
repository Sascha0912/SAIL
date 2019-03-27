import numpy as np
import pandas as pd

def rastrigin_Categorize(samples, d):
    feature1 = []
    feature2 = []
    # print("samples")
    # print(samples)
    for i in range(0,np.shape(samples)[0]):
        feature1.insert(i, samples.iloc[i,0])
        feature2.insert(i, samples.iloc[i,1])
    
    # feature = [feature1[:], feature2[:]]
    feature1 = np.array(feature1)
    feature2 = np.array(feature2)
    feature1 = feature1[:,np.newaxis]
    feature2 = feature2[:,np.newaxis]
    # print("feature1[:]")
    # print(feature1[:])
    # print("feature2[:]")
    # print(feature2[:])
    # print("d.featureMin")
    # print(d.featureMin)
    # print("d.featureMax")
    # print(d.featureMax)
    feature = np.hstack((feature1[:], feature2[:]))
    df_feature = pd.DataFrame(data=feature)
    # print("df_feature")
    # print(df_feature)

    # df_feature.subtract(d.featureMin)


    df_feature = (df_feature - d.featureMin) / list(np.array(d.featureMax) - np.array(d.featureMin))

    # print("rastr_feature")
    # print(df_feature)
    return df_feature
