import numpy as np

def updateMap(replaced, replacement, map, fitness, genes, values, extraMapValues):

    print("replaced")
    print(replaced)
    print("replacement")
    print(replacement)
    print("fitness")
    print(fitness)

    mapfit_re = map[0].fitness.reshape(map[0].fitness.shape[0] * map[0].fitness.shape[1], 1)
    mapfit_re[replaced] = fitness.iloc[0][replacement,np.newaxis]


    # Assign Fitness
    for i in zip(replaced,replacement):
        map.fitness[i[0]] = fitness[i[1]]

    # Assign Genomes
    r, c = np.shape(map.fitness)
    replacedI, replacedJ = np.unravel_index(np.hstack((r,c)), replaced)
    for iReplace in range(0,len(replaced)):
        map.genes[replacedI[iReplace], replacedJ[iReplace], :] = genes[replacement[iReplace]]

    # Assign Miscellaneaous Map values
    if extraMapValues: # not empty
        for iValues in range(0,len(extraMapValues)):
            for i in zip(replaced,replacement):
                exec('Map.'+extraMapValues[iValues]+'[i[0]] = values['+str(iValues)+'][i[1]]')
    
    return map