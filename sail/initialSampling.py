import numpy as np
import pandas as pd
import random
from sobol_seq import i4_sobol_generate
# import chaospy as cp
# from sobol.sobol_seq import i4_sobol, i4_sobol_generate
from sail.getValidInds import getValidInds
from domain.rastrigin.rastrigin_ValidateChildren import rastrigin_ValidateChildren
from domain.rastrigin.rastrigin_PreciseEvaluate import rastrigin_PreciseEvaluate

def initialSampling(d, nInitialSamples):
    def feval(funcName,*args):
        return eval(funcName)(*args)




    # Produce initial solutions
    

    
    # Get collection of valid solutions
    nMissing = nInitialSamples
    inds = pd.DataFrame(columns=[0,1])
    sobPoint = 1


    skip = 1000
    
    # WORKAUROUND: generate 10000 samples
    # Performance durch die 10.000 schlecht TODO
    sobSequence = i4_sobol_generate(d.dof,10000) # generiere 10.000 samples
    sobSequence = sobSequence[skip:]
    random.shuffle(sobSequence)
    # print("sobseq")
    # print(sobSequence.shape)
    # print(sobSequence)



    while nMissing > 0:
        # how many sobol elements to take
        
        # num_take = (sobPoint+nMissing*2)-sobPoint
        indPool = sobSequence[sobPoint:(sobPoint+nMissing*2),:] # PROBLEM: immer die gleichen samples
        # print("indPool")
        # print(indPool.shape)
        # print(indPool)
        sobPoint = 1 + sobPoint + nMissing*2
        # print()
        # print("sobpoint")
        # print(sobPoint)
        validFunction = lambda genomes: feval(d.validate, genomes, d)
        # print("validFunction")
        # print(validFunction)
        # print("indPool")
        # print(indPool)
        # print("nMissing")
        # print(nMissing)
        validInds, x, nMissing, y = getValidInds(indPool, validFunction, nMissing)
        inds = inds.append(validInds)
        # inds = [[inds], [validInds]] # problem

    # Evaluate enough of these valid solutions to get your initial sample set
    testFunction = lambda x: feval(d.preciseEvaluate, x, d)
    sample, value, nMissing, y = getValidInds(inds, testFunction, nInitialSamples)

    # Recurse to make sure you get all the samples you need
    if nMissing > 0:
        sampleRemainder, valueRemainder = initialSampling(d, nMissing)
        sample = sample.append(sampleRemainder)
        value  = value.append(valueRemainder)
        # sample = [[sample], [sampleRemainder]]
        # value = [[value], [valueRemainder]]
    else:
        # Warnings of final sample set
        if sample.shape[0] != np.unique(sample, axis=0).shape[0]:
            print('WARNING: Duplicate samples in observation set!')
        if sample.shape[0] != nInitialSamples:
            print('WARNING: Observation set smaller than specified!')
    
    return sample, value
