from domain.rastrigin.rastrigin_CreateAcqFunc import rastrigin_CreateAcqFunc
from mapElites.createMap import createMap
from mapElites.nicheCompete import nicheCompete
from mapElites.updateMap import updateMap
from mapElites.mapElites import mapElites

def createPredictionMap(gpModels, observation, p, d, **kwargs):
    def scale(value):
        return (value - 0)/(1-0)*(d.featureMax[0] - d.featureMin[0]) + d.featureMin[0]
    def feval(funcName,*args):
        return eval(funcName)(*args)
    # TODO: PARSING - see mapelites
    for key, value in kwargs.items():
        if key=="nChildren":
            p.nChildren = value
        elif key=="nGens":
            p.nGens = value
        elif key=="featureRes":
            d.featureRes = value
    d.varCoef = 0 # no award for uncertainty
    scaled = observation.applymap(scale)   # ADJUSTSCALE

    
    # Construct functions
    acqFunction = feval(d.createAcqFunction, gpModels, d)
    # print("acqFunction")
    # print(acqFunction)
    # Seed map with precisely evaluated solutions
    fitness, predValues = acqFunction(scaled)
    # print("fitness")
    # print(fitness)
    # print("predValues")
    # print(predValues)
    predMap = createMap(d.featureRes, d.dof, d.featureMin, d.featureMax, d.extraMapValues)
    # print("predMap")
    # print(predMap)
    replaced, replacement, x = nicheCompete(scaled, fitness, predMap, d)
    # print("replaced")
    # print(replaced)
    # print("replacement")
    # print(replacement)
    predMap = updateMap(replaced, replacement, predMap, fitness, scaled, predValues, d.extraMapValues)
    # print("predMap")
    # print(predMap[0].fitness)

    # Illuminate based on surrogate models
    predMap, percImproved, h = mapElites(acqFunction, predMap, p, d)

    return predMap, percImproved
