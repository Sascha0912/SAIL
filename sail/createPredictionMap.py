def createPredictionMap(gpModels, observation, p, d, varargin): # **kwargs
    # TODO: PARSING - see mapelites

    d.varCoef = 0 # no award for uncertainty

    # Construct functions
    acqFunction = feval(d.createAcqFunction, gpModels, d)

    # Seed map with precisely evaluated solutions
    fitness, predValues = acqFunction(observation)
    predMap = createMap(d.featureRes, d.dof, d.extraMapValues)
    replaced, replacement = nicheCompete(observation, fitness, predMap, d)
    predMap = updateMap(replaced, replacement, predMap, fitness, observation, predValues, d.extraMapValues)

    # Illuminate based on surrogate models
    predMap, percImproved = mapElites(acqFunction, predMap, p, d)

    return predMap, percImproved
