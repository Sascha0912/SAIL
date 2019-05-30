from domain.cube.expression.loadBaseCube import loadBaseCube
from gaussianProcess.paramsGP import paramsGP

def cube_Domain():
    class Domain:
        def __init__(self):
            self.name = "cube"

            # Scripts
            self.preciseEvaluate   = "cube_PreciseEvaluate"
            self.categorize        = "cube_Categorize"
            self.createAcqFunction = "cube_CreateAcqFunc"
            self.validate          = "cube_ValidateChildren"

            self.objFun = "cube_FitnessFunc"

            # Alternative initialization
            self.loadInitialSamples  = False
            self.initialSampleSource = ""

            # Genotype to Phenotype Expression
            self.dof     = 36
            self.express = lambda x: cubeRaeY(x)
            self.base    = loadBaseCube(self.express, self.dof)
        #     print("base")
        #     print(self.base)

            # Feature Space
            self.featureRes    = [25, 25]
            self.nDims         = len(self.featureRes)
            self.featureMin    = [-2, -2]
            self.featureMax    = [2, 2]
            self.featureLabels = ["Z", "X"] # [X label, Y label]

            # GP Models
            self.gpParams = []
            self.gpParams.append(paramsGP(self.dof)) # Drag
            self.gpParams.append(paramsGP(self.dof)) # Lift
            self.nVals       = 2 # number of values of interest

            # Acquisition function
            self.varCoef = 20 # variance weight
            self.muCoef  = 1  # mean weight TODO: delete

            # Domain Specific Map Values
            self.extraMapValues = ["cD","confidence"]

    return Domain()
