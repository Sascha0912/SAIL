import numpy as np
import pandas as pd
import pyGPs

from sail.sobol2indx import sobol2indx
from sail.sobol_lib import i4_sobol_generate
from sail.initialSampling import initialSampling
from sail.createPredictionMap import createPredictionMap
from sail.getValidInds import getValidInds

from gaussianProcess.trainGP import trainGP

from domain.rastrigin.rastrigin_CreateAcqFunc import rastrigin_CreateAcqFunc
from domain.rastrigin.rastrigin_PreciseEvaluate import rastrigin_PreciseEvaluate

from mapElites.createMap import createMap
from mapElites.nicheCompete import nicheCompete
from mapElites.updateMap import updateMap
from mapElites.mapElites import mapElites


from pprint import pprint

def sail(p,d): # domain and params
    def feval(funcName,*args):
        return eval(funcName)(*args)
    # Produce initial samples
    if ~d.loadInitialSamples:
        # print("d")
        # pprint(vars(d))
        # print("p")
        # pprint(vars(p))
        # print("d")
        # print(d)
        # print("p.nInitlasmaples")
        # print(p.nInitialSamples)
        observation, value = initialSampling(d,p.nInitialSamples)
        # print("observation")
        # print(observation)
        # print("value")
        # print(value)
    else:
        np.load(d.initialSampleSource) # e.g. npz-File
        randomPick = np.random.permutation(observation.shape[0])[:p.initialSamples] # take only first "initialSamples" values
        observation = observation[randomPick,:] # get rows with indexes from randomPick
        value = value[randomPick,:] # same for value

    nSamples = observation.shape[0]

    # Acquisition loop
    trainingTime = []
    illumTime = []
    peTime = []
    predMap = []

    # print("value")
    # print(value)
    percImproved = pd.DataFrame()
    acqMapRecord = pd.DataFrame()
    confContribution = pd.DataFrame()

    while nSamples <= p.nTotalSamples:
        # Create surrogate and acquisition function
        # Surrogate models are created from all evaluated samples, and these
        # models are used to produce acquisition function.
        print('PE ' + str(nSamples) + ' | Training Surrogate Models')
        tstart = 0 # time calc
        gpModel = []
        # print("value")
        # print(value)
        # print("value.shape[1]: " + str(value.shape))
        # print("d.gpParams.shape: " + str(np.shape(d.gpParams)))
        for iModel in range(0,value.shape[1]): # must be parallelized
            # only retrain model parameters every 'p.trainingMod' iterations
            if (nSamples == p.nInitialSamples or np.remainder(nSamples, p.trainingMod * p.nAdditionalSamples)):
                gpModel.insert(iModel,trainGP(observation, value.loc[:,iModel], d.gpParams[iModel]))
                # pass
            else:
                gpModel.insert(iModel,trainGP(observation, value.loc[:,iModel], d.gpParams[iModel], functionEvals=0))
                # pass

        # Save found model parameters and update acquisition function
        for iModel in range(0,value.shape[1]):
            # d.gpParams[iModel].hyp = gpModel[iModel].hyp # See pyGPs hyp
            d.gpParams[iModel].hyp_cov = gpModel[iModel].covfunc
            d.gpParams[iModel].hyp_mean = gpModel[iModel].meanfunc
            d.gpParams[iModel].hyp_lik = gpModel[iModel].likfunc


        acqFunction = feval(d.createAcqFunction, gpModel, d)

        # Data Gathering (training Time)
        trainingTime = 0 # time calc

        # Create intermediate prediction map for analysis
        if ~np.remainder(nSamples, p.data_mapEvalMod) and p.data_mapEval:
            print('PE: ' + str(nSamples) + ' | Illuminating Prediction Map')
            predMap[nSamples], x = createPredictionMap(gpModel, observation, p, d, 'featureRes', p.data_predMapRes, 'nGens', 2*p.nGens)

        # 2. Illuminate Acquisition Map
        # A map is constructed using the evaluated samples which are evaluated
        # with the acquisition function and placed in the map as the initial
        # population. The observed samples are the seed population of the
        # 'acquisition map' which is then created by optimizing the acquisition
        # function with MAP-Elites.
        if nSamples == p.nTotalSamples:
            break # After final model is created no more infill is necessary
        print('PE: ' + str(nSamples) + ' | Illuminating Acquisition Map')
        tstart = 0

        # Evaluate observation set with acquisition function
        fitness, predValues = acqFunction(observation)

        # Place best samples in acquisition map
        obsMap = createMap(d.featureRes, d.dof, d.extraMapValues)
        replaced, replacement, x = nicheCompete(observation, fitness, obsMap, d)
        obsMap = updateMap(replaced, replacement, obsMap, fitness, observation, predValues, d.extraMapValues)

        # Illuminate with MAP-Elites
        acqMap, percImp, h = mapElites(acqFunction, obsMap, p, d)

        # Workaround for acqMap
        if (isinstance(acqMap,tuple)):
            if (isinstance(acqMap[0], tuple)):
                acqMap = acqMap[0][0]
            else:
                acqMap = acqMap[0]

        percImproved[nSamples] = percImp # ok
        # print("percImproved")
        # print(percImproved)

        # Data Gathering (illum Time)
        illumTime = 0 # time calc
        # print("acqMap")
        # pprint(vars(acqMap))
        acqMapRecord[nSamples] = acqMap
        # print("acqMap.confidence")
        # print(acqMap.confidence)
        # print("fitness_flattened")
        # print(fitness_flattened)
        # print("acqMap.fitness")
        # print(acqMap.fitness)
        fitness_flattened = acqMap.fitness.flatten('F')

        # DEBUG
        # for i in zip(acqMap.confidence, fitness_flattened):
        #     print(i)
        abs_fitness = [abs(val) for val in fitness_flattened]
        # print((acqMap.confidence * d.varCoef) / abs_fitness)
        confContribution.at[0,nSamples] = np.nanmedian( (acqMap.confidence * d.varCoef) / abs_fitness)
        # print("nanmedian") # works
        # print(np.nanmedian( (acqMap.confidence * d.varCoef) / abs_fitness))
        # print("confContribution")
        # print(confContribution)



        # 3. Select infill Samples
        # The next samples to be tested are chosen from the acquisition map: a
        # sobol sequence is used to evenly sample the map in the feature
        # dimensions. When evaluated solutions don't converge or the chosen bin
        # is empty the next bin in the sobol set is chosen.

        print('PE: ' + str(nSamples) + ' | Evaluating New Samples')
        tstart = 0

        # At first iteration initialize sobol sequence for sample selection
        if nSamples == p.nInitialSamples:
            sobSet = i4_sobol_generate(d.nDims,10000,1000).transpose()
            sobSet = pd.DataFrame(data=sobSet)
            sobSet = sobSet.sample(frac=1).reset_index(drop=True)
            sobPoint = 1

        # Choose new samples and evaluate them for new observations
        nMissing = p.nAdditionalSamples
        newValue = []
        newSample = []
        indPool = pd.DataFrame()
        while nMissing > 0:
            # Evenly sample solutions from acquisition map
            newSampleRange = list(range(sobPoint-1, sobPoint + p.nAdditionalSamples-1))
            # print("newSampleRange")
            # print(newSampleRange)
            x, binIndx = sobol2indx(sobSet, newSampleRange, d, acqMap.edges)
            # print("binIndxAfter")
            # print(binIndx)
            # print("acqMap.genes")
            # print(acqMap.genes)

            for iGenes in range(0,binIndx.shape[0]):
                indPool.at[iGenes,0] = acqMap.genes[0].iloc[binIndx.iloc[iGenes,0],binIndx.iloc[iGenes,1]]
                indPool.at[iGenes,1] = acqMap.genes[1].iloc[binIndx.iloc[iGenes,0],binIndx.iloc[iGenes,1]]

            # print("indPool")
            # print(indPool)
            # print("observation")
            # print(observation)

            # for iGenes in range(0,binIndx.shape[0]):
            #     indPool[iGenes,:] = acqMap.genes[binIndx.iloc[iGenes,0], binIndx.iloc[iGenes,1], :]








            # Remove repeats and nans (empty bins)
            # repeats in case of rastrigin: almost impossible?
            ds1 = set([tuple(line) for line in indPool.values])
            ds2 = set([tuple(line) for line in observation.values])
            indPool = pd.DataFrame(data=list(ds1.difference(ds2)))
            indPool.dropna(inplace=True) # ok
            # print("indPool after")
            # print(indPool)


            # indPool = np.setdiff1d(indPool,observation) # 'rows','stable' ?
            # indPool = indPool[:] # ~any(isnan(indPool),2)

            # Evaluate enough of these valid solutions to get your initial sample set
            peFunction = lambda x: feval(d.preciseEvaluate, x, d) # returns nan if not converged
            print("indPool")
            print(indPool)
            # TODO: reset_index of indPool to work
            print("peFunction")
            print(peFunction)
            print("nMissing")
            print(nMissing)

            foundSample, foundValue, nMissing = getValidInds(indPool, peFunction, nMissing)
            # print("foundSample")
            # print(foundSample)
            newSample = [[newSample], [foundSample]]
            newValue = [[newValue], [foundValue]]

            # Advance sobol sequence
            sobPoint = sobPoint + p.nAdditionalSamples + 1

        # Assign found values
        value = [value, newValue] # cat
        observation = [observation, newSample] # cat
        nSamples = observation.shape[0]

        if len(observation) != len(np.unique(observation, axis=0)):
            print('WARNING: duplicate samples in observation set.')

        peTime = 0 # TODO: time calc
        # End Acquisition loop

    # Save relevant Data
    output.p = p
    output.d = d
    output.model = gpModel
    output.trainTime = trainingTime
    output.illum = illumTime
    output.petime = peTime
    output.percImproved = percImproved
    output.predMap = predMap
    output.acqMap = acqMapRecord
    output.confContrib = confContribution
    output.unpack = '' # necessary?

    if p.data.outSave:
        pass
        # np.save() # sailRun.npz (example)
