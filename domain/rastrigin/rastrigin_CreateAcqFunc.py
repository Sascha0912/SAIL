def ratrigin_CreateAcqFunc(gpModel, d):
    acqFunction = lambda x: rastrigin_AcquisitionFunc(predictGP(gpModel[0],x), predictGP(gpModel[1],x), x, d)
    return acqFunction