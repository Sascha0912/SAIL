from domain.rastrigin.rastrigin_AcquisitionFunc import rastrigin_AcquisitionFunc
from gaussianProcess.predictGP import predictGP

def rastrigin_CreateAcqFunc(gpModel, d):
    print("gpModel")
    print(gpModel)
    acqFunction = lambda x: rastrigin_AcquisitionFunc(predictGP(gpModel[0],x), d) # edited
    print("acqFunc")
    print(acqFunction)
    return acqFunction