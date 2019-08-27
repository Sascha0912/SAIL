from domain.wheelcase.wheelcase_AcquisitionFunc import wheelcase_AcquisitionFunc
from gaussianProcess.predictGP import predictGP

def wheelcase_CreateAcqFunc(gpModel, d):
    # 1. Drag 2. Lift 3. Genomes for Area Calculation 4. Hyperparams and base
    acqFunction = lambda x: wheelcase_AcquisitionFunc(predictGP(gpModel[0],x), d) # predictGP(gpModel[1],x)
    return acqFunction