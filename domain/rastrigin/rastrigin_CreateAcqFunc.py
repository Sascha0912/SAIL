def rastrigin_CreateAcqFunc(gpModel, d):
    print("gpModel")
    print(gpModel)
    acqFunction = lambda x: rastrigin_AcquisitionFunc(predictGP(gpModel[0],x), predictGP(gpModel[1],x), x, d)
    print("acqFunc")
    print(acqFunction)
    return acqFunction