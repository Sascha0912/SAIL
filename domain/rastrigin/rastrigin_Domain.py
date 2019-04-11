from gaussianProcess.paramsGP import paramsGP
import numpy as np

def rastrigin_Domain():
    class Domain:
        def __init__(self):
            self.name = 'rastrigin'

            # Functions
            self.objFun = 'rastrigin_FitnessFunc'
            self.getBc  = 'rastrigin_GetBehaviour'
            self.breedPop = 'rastrigin_Variation'
            self.randInd = 'rastrigin_RandInd'

            # MAP-Elites settings
            self.nInitial = 2**6
            self.batchSize = 2**6
            self.nEvals = 2**10

            self.mapDims_res = [25, 25]
            self.mapDims_label = ['x-coord','y-coord']
            self.mapDims_min = [-2, -1]
            self.mapDims_max = [2, 2]
            self.mapDims_misc = ['otherVal1', 'otherVal2']

            # Genome
            self.sampleInd_genome = np.empty((2,1))
            self.sampleInd_genome[:] = np.nan

            # Recombine parameters
            self.recombine_range = [-2, 2]
            self.recombine_mutSigma = [[1/8], [1/10]]
            self.recombine_parents = 1

            # SAIL additions
            self.loadInitialSamples = False
            self.dof = 2
            self.validate = 'rastrigin_ValidateChildren'

            self.preciseEvaluate = 'rastrigin_PreciseEvaluate'
            self.createAcqFunction = 'rastrigin_CreateAcqFunc'

            self.gpParams = []
            self.gpParams.append(paramsGP(self.dof)) # X
            self.gpParams.append(paramsGP(self.dof)) # Y

            # Acquisition function
            self.varCoef = 20 # variance weight # TODO: testweise ändern
            self.muCoef = 1 # mean weight

            self.featureRes = [25, 25]
            # self.extraMapValues = []

            self.categorize = 'rastrigin_Categorize'

            self.featureMin = [0, 0] # ADJUSTSCALE 
            self.featureMax = [1, 1]   # currently, only the first values are used -> delete second items from list

            self.nDims = len(self.featureRes)

            self.featureLabels = ['X', 'Y']
            self.extraMapValues = ['dragForce','confidence']
            
    return Domain()
