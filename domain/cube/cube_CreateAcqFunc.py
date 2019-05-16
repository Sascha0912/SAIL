def cube_CreateAcqFunc(gpModel, d):
    # 1. Drag 2. Lift 3. Genomes for Area Calculation 4. Hyperparams and base
    acqFunction = lambda x: cube_AcquisitionFunc(predictGP(gpModel[0],x), predictGP(gpModel[1],x), x, d)
    return acqFunction
