import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

def wheelcase_FitnessFunc(pop):

    # TODO: adapt Fitnessfunction for wheelcase
    params = FFDParameters()
    # params.read_parameters(filename='domain/cube/ffd/deform_goal.prm')

    # goal_genome = np.concatenate((params.array_mu_x.flatten(), params.array_mu_y.flatten(), params.array_mu_z.flatten()), axis=None)
    fitness_arr = []

    for i in range(len(pop)):
        a = pop.iloc[i,:].values
        # print("a")
        # print(a)
        s = np.sum(abs(a-goal_genome))
        fitness_arr.append(s)

    # make all values negative (high fitness is bad fitness)
    fitness_arr = np.negative(fitness_arr)
    df_fitness = pd.DataFrame(data=fitness_arr).transpose()

    return df_fitness
