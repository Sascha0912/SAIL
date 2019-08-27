import numpy as np
import pandas as pd

from sail.getValidInds import getValidInds

from visualization.viewMap import viewMap

from mapElites.createChildren import createChildren
from mapElites.nicheCompete import nicheCompete
from mapElites.updateMap import updateMap

from domain.rastrigin.rastrigin_ValidateChildren import rastrigin_ValidateChildren
from domain.cube.cube_ValidateChildren import cube_ValidateChildren
from domain.wheelcase.wheelcase_ValidateChildren import wheelcase_ValidateChildren

def mapElites(fitnessFunction, map, p, d):
    # print("map")
    # print(map[0])
    def feval(funcName,*args):
        return eval(funcName)(*args)
    # View initial map
    h = []
    if p.display_illu:
        h1, h2 = viewMap(map.fitness, d, map.edges)
        h.append(h1)
        h.append(h2)

    # MAP-Elites
    iGen = 1
    percImproved = []
    while iGen <= p.nGens:
        # Create and evaluate children
        # Create children which satisfy geometrix constraints for validity
        nMissing = p.nChildren
        children = pd.DataFrame()

        while nMissing > 0:
            indPool = createChildren(map, nMissing, p, d)
            validFunction = lambda genomes: feval(d.validate, genomes, d)
            validChildren, x, nMissing, y = getValidInds(indPool, validFunction, nMissing)
            children = children.append(validChildren)

        # print("children")
        # print(children)
        # print("fitness")
        # print(fitness)
        fitness, values = fitnessFunction(children)

        # Add Children to map
        # print("children")
        # print(children)
        # print("fitness")
        # print(fitness)
        # print("map")
        # print(map)
        # print("d")
        # print(d)
        replaced, replacement, x = nicheCompete(children, fitness, map, d)
        map = updateMap(replaced, replacement, map, fitness, children, values, d.extraMapValues)

        # Improvement stats
        percImproved.insert(iGen, len(replaced)/p.nChildren)

        # View illumination progress
        if p.display_illu and ~np.remainder(iGen, p.display_illuMod):
            pass # TODO: view + draw

        iGen = iGen+1
        if ~np.remainder(iGen,2**5):
            print("Illumination Generation: " + str(iGen) + " - Improved: " + str(percImproved[-1]*100) + "%")


    if percImproved[-1] > 0.05:
        print("Warning: MAP-Elites finished while still making improvements ( >5% / generation)")

    return map, percImproved, h
