def cube_Domain():
    class Domain:
        def __init__(self):
            self.name = "cube"

            # Scripts
            self.preciseEvaluate   = "cube_PreciseEvaluate"
            self.categorize        = "cube_Categorize"
            self.createAcqFunction = "cube_CreateAcqFunc"
            self.validate          = "cube_ValidateChildren"

            # Alternative initialization
            self.loadInitialSamples  = False
            self.initialSampleSource = ""

            # Genotype to Phenotype Expression
            self.dof     = 10
            self.express = lambda x: cubeRaeY(x)
            self.base    = loadBaseCube(self.express, self.dof)

            # Feature Space
            self.featureRes    = [25, 25]
            self.nDims         = len(self.featureRes)
            self.featureMin    = [0.1, 0.5]
            self.featureMax    = [0.2, 0.6]
            self.featureLabels = ["Z", "X"] # [X label, Y label]

            # GP Models
            self.gpParams[0] = paramsGP(self.dof) # Drag
            self.gpParams[1] = paramsGP(self.dof) # Lift
            self.nVals       = 2 # number of values of interest

            # Acquisition function
            self.varCoef = 20 # variance weight
            self.muCoef  = 1  # mean weight

            # Domain Specific Map Values
            self.extraMapValues = ["cD","cL","confidence"]
            
    return Domain()
