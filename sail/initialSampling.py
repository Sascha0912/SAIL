import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
# from sobol_seq import i4_sobol_generate
from sail.sobol_lib import i4_sobol_generate
from pprint import pprint
# import matlab.engine
# import chaospy as cp
# from sobol.sobol_seq import i4_sobol, i4_sobol_generate
from sail.getValidInds import getValidInds



from domain.rastrigin.rastrigin_ValidateChildren import rastrigin_ValidateChildren
from domain.rastrigin.rastrigin_PreciseEvaluate import rastrigin_PreciseEvaluate

from domain.cube.cube_ValidateChildren import cube_ValidateChildren
from domain.cube.cube_PreciseEvaluate import cube_PreciseEvaluate

def initialSampling(d, nInitialSamples): # CHECKED d, nInitialSamples

    # SOBOL settings (adjust also in sail)
    skip     = 1000
    seq_size = 20000

    def feval(funcName,*args):
        return eval(funcName)(*args)
    def scale(value):
        return (value - 0)/(1-0)*(d.featureMax[0] - d.featureMin[0]) + d.featureMin[0]


    
    # print("d")
    # pprint(vars(d))
    # print("nInitialSamples")
    # print(nInitialSamples)


    # Produce initial solutions
    

    
    # Get collection of valid solutions
    nMissing = nInitialSamples # CHECKED nMissing
    # print("nMissing")
    # print(nMissing)
    inds = pd.DataFrame(columns=[0,1])
    sobPoint = 1
    
    # WORKAUROUND: generate 10000 samples
    # Performance durch die 10.000 schlecht TODO
    # sobSequence = i4_sobol_generate(d.dof,10000) # generiere 10.000 samples
    sobSequence = i4_sobol_generate(d.dof,seq_size,skip).transpose() # dient nur dem initialen Sampling
    sobSequence = pd.DataFrame(data=sobSequence)
    sobSequence = sobSequence.sample(frac=1).reset_index(drop=True)

    # TODO: ADDED: Scaling
    sobSequence = sobSequence.applymap(scale)
    
    # print(sobSequence)
    # random.shuffle(sobSequence)
    # print("sobSequence")
    # print(sobSequence.shape)
    # print(sobSequence)
    # sobSequence = eng.generate_sobol(d.dof,skip)
    # print(sobSequence)
    # sobSequence = sobSequence[skip:]
    # random.shuffle(sobSequence)
    # print("sobseq")
    # print(sobSequence.shape)
    # print(sobSequence)



    while nMissing > 0:
        # how many sobol elements to take
        
        # num_take = (sobPoint+nMissing*2)-sobPoint
        indPool = sobSequence.loc[sobPoint-1:(sobPoint+nMissing*2),:] # indPool ok, aber samples sind pro iteration nicht unterschiedlich, wie in matlab
        # print("indPool")
        # print(indPool)
        # print("indPool")
        # print(indPool.shape)
        # print(indPool)
        sobPoint = 1 + sobPoint + nMissing*2 # sobPoint OK
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
        # print("validInds")
        # print(validInds)
        # print("nMissing")
        # print(nMissing)
        inds = inds.append(validInds)
        # inds = [[inds], [validInds]] # problem

    # Evaluate enough of these valid solutions to get your initial sample set
    testFunction = lambda x: feval(d.preciseEvaluate, x, d)
    sample, value, nMissing, y = getValidInds(inds, testFunction, nInitialSamples)
    # print(value)

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
    
    # print("value")
    # print(value)
    return sample, value