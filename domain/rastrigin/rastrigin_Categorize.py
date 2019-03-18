def rastrigin_Categorize(samples, d):
    feature1 = []
    feature2 = []
    for i in range(0,len(samples,0)):
        feature1[i] = samples[i,0]
        feature2[i] = samples[i,1]
    
    feature = [feature1[:], feature2[:]]
    feature = (feature - d.featureMin) / (d.featureMax - d.featureMin)

    return feature
