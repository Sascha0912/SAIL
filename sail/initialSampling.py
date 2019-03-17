import numpy as np
import sobol_seq
from sail.getValidInds import getValidInds
from domain.rastrigin.rastrigin_Validate import rastrigin_Validate

def initialSampling(d, nInitialSamples):

    def feval(funcName,*args):
        return eval(funcName)(*args)

    # Produce initial solutions
    # sobSequence = sobol_seq #.i4_...

    # Get collection of valid solutions
    nMissing = nInitialSamples
    inds = []
    sobPoint = 1
    while nMissing > 0:
        # how many sobol elements to take
        num_take = (sobPoint+nMissing*2)-sobPoint

        indPool = sobol_seq.i4_sobol_generate(d.dof,num_take)
        sobPoint = 1 + sobPoint + nMissing*2
        validFunction = lambda genomes: feval(d.validate, genomes, d)
        validInds, x, nMissing = getValidInds(indPool, validFunction, nMissing)
        inds = [[inds], [validInds]]

    # Evaluate enough of these valid solutions to get your initial sample set
    testFunction = lambda x: feval(d.preciseEvaluate, x, d)
    sample, value, nMissing = getValidInds(inds, testFunction, nInitialSamples)

    # Recurse to make sure you get all the samples you need
    if nMissing > 0:
        sampleRemainder, valueRemainder = initialSampling(d, nMissing)
        sample = [[sample], [sampleRemainder]]
        value = [[value], [valueRemainder]]
    else:
        # Warnings of final sample set
        if sample.shape[0] != np.unique(sample, axis=0).shape[0]:
            print('WARNING: Duplicate samples in observation set!')
        if sample.shape[0] != nInitialSamples:
            print('WARNING: Observation set smaller than specified!')
