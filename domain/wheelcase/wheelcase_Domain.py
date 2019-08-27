from domain.wheelcase.expression.loadBaseWheelcase import loadBaseWheelcase
from gaussianProcess.paramsGP import paramsGP

def wheelcase_Domain():
    class Domain:
        def __init__(self):
            self.name = "wheelcase"

            # Scripts
            self.preciseEvaluate   = "wheelcase_PreciseEvaluate"
            self.categorize        = "wheelcase_Categorize"
            self.createAcqFunction = "wheelcase_CreateAcqFunc"
            self.validate          = "wheelcase_ValidateChildren"

            self.objFun = "wheelcase_FitnessFunc"

            # Alternative initialization
            self.loadInitialSamples  = False
            self.initialSampleSource = ""

            # Genotype to Phenotype Expression
            self.dof     = 6 # only outer side will be deformed 2*3*3 # only middle of one side will be deformed 2*3
            self.express = lambda x: wheelcaseRaeY(x)
            self.base    = loadBaseWheelcase(self.express, self.dof)

            # Feature Space
            self.featureRes    = [25, 25]
            self.nDims         = len(self.featureRes)
            self.featureMin    = [0, 0]
            self.featureMax    = [4, 0.2] # DOMAINCHANGE maximale Breite: 4 maximale h�he: 0.2
            self.featureLabels = ["velo width", "velo height"] # [X label, Y label]

            # GP Models
            self.gpParams = []
            self.gpParams.append(paramsGP(self.dof)) # Drag
            self.gpParams.append(paramsGP(self.dof)) # Lift
            self.nVals       = 2 # number of values of interest

            # Acquisition function
            self.varCoef = 2 # variance weight
            self.muCoef  = 1  # mean weight TODO: delete

            # Domain Specific Map Values
            self.extraMapValues = ["cD","confidence"]

    return Domain()
