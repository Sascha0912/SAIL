import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

def cube_FitnessFunc(pop):# TODO: need also domain as input -> for feature Range
#     print("pop")
#     print(pop)

    # STL load necessary? probably not
    # stl_handler = StlHandler()
    # goal_mesh_points = stl_handler.parse('domain/cube/ffd/goal.stl')
    # goal_df = pd.DataFrame(data=goal_mesh_points)
    # TODO: Hardcode deformation parameters of goal here -> save time
    params = FFDParameters()
    params.read_parameters(filename='domain/cube/ffd/deform_goal.prm')

    goal_genome = np.concatenate((params.array_mu_x.flatten(), params.array_mu_y.flatten(), params.array_mu_z.flatten()), axis=None)
#     print("goal")
#     print(goal_genome)

#     df_fitness = pd.DataFrame()
    fitness_arr = []
    
#     print("goal_df")
#     print(goal_df)
    for i in range(len(pop)):
        a = pop.iloc[i,:].values
        s = np.sum(abs(a-goal_genome))
        fitness_arr.append(s)
        # TODO: -2 and +2 should be replaced with featureMin and featureMax
        # a_scaled = np.interp(a, (0,1), (-2,+2))
        # print(a)
        # print(s)
        # print(a_scaled)

    # make all values negative (high fitness is bad fitness)
    fitness_arr = np.negative(fitness_arr)
    df_fitness = pd.DataFrame(data=fitness_arr).transpose()
#     print("df_fitness")
#     print(df_fitness)
    return df_fitness