def rastrigin_Domain():
    class Domain:
        def __init__(self):
            self.name = 'rastrigin'

            # Scripts
            self.preciseEvaluate   = 'rastrigin_PreciseEvaluate'
            self.categorize        = 'rastrigin_Categorize'
            self.createAcqFunction = 'rastrigin_CreateAcqFunc'
            self.validate          = 'rastrigin_Validate'

            # Alternative initialization
            self.loadInitialSamples = False
            self.initialSampleSource = ''

            # Genotype to Phentotype Expression
            self.dof = 10
            self.express = lambda x: rastrRaeY(x)
            # self.base = loadBaseRastrigin(self.express, self.dof) # Creates base struct with drag, lift and geometry

            # Feature Space
            self.featureRes = [25, 25]
            self.nDims      = len(self.featureRes)
            self.featureMin = [-2, -1]
            self.featureMax = [2, 2]
            self.featureLabels = ['Z_{up}','X_{up}'] # [X label, Y label]

            # GP Models
            self.gpParams[0] = paramsGP(d.dof)
            self.gpParams[1] = paramsGP(d.dof)
            self.nVals = 2 # number of values of interest

            # Acquisition function
            self.varCoef = 20 # variance weight
            self.muCoef  = 1  # mean weight

            # Domain Specific Map Values
            self.extraMapValues = []

	    
    
    return Domain()

    

    

    
