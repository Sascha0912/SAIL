from domain.cube.cube_AcquisitionFunc import cube_AcquisitionFunc
from gaussianProcess.predictGP import predictGP

def cube_CreateAcqFunc(gpModel, d):
    # 1. Drag 2. Lift 3. Genomes for Area Calculation 4. Hyperparams and base
    acqFunction = lambda x: cube_AcquisitionFunc(predictGP(gpModel[0],x), d) # predictGP(gpModel[1],x)
    return acqFunction
