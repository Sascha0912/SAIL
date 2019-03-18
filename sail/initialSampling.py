import numpy as np
from sobol_seq import i4_sobol_generate
# import chaospy as cp
# from sobol.sobol_seq import i4_sobol, i4_sobol_generate
from sail.getValidInds import getValidInds
from domain.rastrigin.rastrigin_ValidateChildren import rastrigin_ValidateChildren

def initialSampling(d, nInitialSamples):
    def feval(funcName,*args):
        return eval(funcName)(*args)




    # Produce initial solutions
    

    
    # Get collection of valid solutions
    nMissing = nInitialSamples
    inds = []
    sobPoint = 1

    num_take = (sobPoint+nMissing*2)-sobPoint
    sobSequence = i4_sobol_generate(d.dof,num_take,skip=1000)
    # print("sobseq")
    # print(sobSequence)



    while nMissing > 0:
        # how many sobol elements to take
        

        indPool = i4_sobol_generate(d.dof,num_take,skip=1000)
        sobPoint = 1 + sobPoint + nMissing*2
        # print("sobpoint")
        # print(sobPoint)
        validFunction = lambda genomes: feval(d.validate, genomes, d)
        # print("validFunction")
        # print(validFunction)
        # print("indPool")
        # print(indPool)
        # print("nMissing")
        # print(nMissing)
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
