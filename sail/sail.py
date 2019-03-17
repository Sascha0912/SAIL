import numpy as np
import pyGPs
import sobol_seq
from sail.initialSampling import initialSampling


def sail(p,d):
    # Produce initial samples
    if ~d.loadInitialSamples:
        observation, value = initialSampling(d,p.nInitialSamples)
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
    while nSamples <= p.nTotalSamples:
        # Create surrogate and acquisition function
        # Surrogate models are created from all evaluated samples, and these
        # models are used to produce acquisition function.
        print('PE ' + str(nSamples) + ' | Training Surrogate Models')
        tstart = 0 # time calc
        for iModel in range(0,value.shape[1]): # must be parallelized
            # only retrain model parameters every 'p.trainingMod' iterations
            if (nSamples == p.initialSamples or np.remainder(nSamples, p.trainingMod * p.nAdditionalSamples)):
                # gpModel
                pass
            else:
                # gpModel
                pass

        # Save found model parameters and update acquisition function
        for iModel in range(0,value.shape[1]):
            d.gpParams[iModel].hyp = gpModel[iModel].hyp # See pyGPs hyp

        acqFunction = feval(d.createAcqFunction, gpModel, d)

        # Data Gathering (training Time)
        trainingTime = 0 # time calc

        # Create intermediate prediction map for analysis
        if ~np.remainder(nSamples, p.data.mapEvalMod) and p.data.mapEval:
            print('PE: ' + str(nSamples) + ' | Illuminating Prediction Map')
            predMap[nSamples], x = createPredictionMap(gpModel, observation, p, d, 'featureRes', p.data.predMapRes, 'nGens', 2*p.nGens)

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
        replaced, replacement = nicheCompete(observation, fitness, obsMap, d)
        obsMap = updateMap(replaced, replacement, obsMap, fitness, observation, predValues, d.extraMapValues)

        # Illuminate with MAP-Elites
        acqMap, percImproved[:,nSamples] = mapElites(acqFunction, obsMap, p, d)

        # Data Gathering (illum Time)
        illumTime = 0 # time calc
        acqMapRecord[nSamples] = acqMap
        confContribution[nSamples] = np.nanmedian( (acqMap.confidence[:] * d.varCoef) / abs(acqMap.fitness[:]))

        # 3. Select infill Samples
        # The next samples to be tested are chosen from the acquisition map: a
        # sobol sequence is used to evenly sample the map in the feature
        # dimensions. When evaluated solutions don't converge or the chosen bin
        # is empty the next bin in the sobol set is chosen.

        print('PE: ' + str(nSamples) + ' | Evaluating New Samples')
        tstart = 0

        # At first iteration initialize sobol sequence for sample selection
        if nSamples == p.nInitialSamples:
            sobSet = sobol_seq #.i4_...
            sobPoint = 1

        # Choose new samples and evaluate them for new observations
        nMissing = p.nAdditionalSamples
        newValue = []
        newSample = []
        while nMissing > 0:
            # Evenly sample solutions from acquisition map
            newSampleRange = range(sobPoint, sobPoint + p.nAdditionalSamples)-1
            x, binIndx = sobol2indx(sobSet, newSampleRange, d, acqMap.edges)
            for iGenes in range(0,binIndx.shape[0]):
                indPool[iGenes,:] = acqMap.genes[binIndx[iGenes,0], binIndx[iGenes,1], :]
            # Remove repeats and nans (empty bins)
            indPool = np.setdiff1d(indPool,observation) # 'rows','stable' ?
            indPool = indPool[:] # ~any(isnan(indPool),2)

            # Evaluate enough of these valid solutions to get your initial sample set
            peFunction = lambda x: feval(d.preciseEvaluate, x, d) # returns nan if not converged
            foundSample, foundValue, nMissing = getValidInds(indPool, peFunction, nMissing)
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

        peTime = 0 # time calc
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
        np.save() # sailRun.npz (example)
