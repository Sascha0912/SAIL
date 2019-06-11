import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

# import subprocess
import os

def wheelcase_FitnessFunc(pop):

    # TODO: adapt Fitnessfunction for wheelcase
    params = FFDParameters()
    stl_handler = StlHandler()
    params.read_parameters(filename='domain/wheelcase/ffd/ffd_config.prm') # Dummy config file
    # print(pop)

    # Generate config file for each sample
    for i in range(len(pop)):
        # Change displacements (weights) of each sample
        sample = pop.iloc[i] # get sample (1x36)
        # print("sample")
        # print(sample)
        mu_x = []
        mu_y = []
        mu_z = []
        x = sample.iloc[:12].to_numpy().reshape((6,2))
        mu_x.append(x[0:2])
        mu_x.append(x[2:4])
        mu_x.append(x[4:6])
        # print(mu_x)
        params.array_mu_x = mu_x

        y = sample.iloc[12:24].to_numpy().reshape((6,2))
        mu_y.append(y[0:2])
        mu_y.append(y[2:4])
        mu_y.append(y[4:6])
        # print(mu_y)
        params.array_mu_y = mu_y

        z = sample.iloc[24:36].to_numpy().reshape((6,2))
        mu_z.append(z[0:2])
        mu_z.append(z[2:4])
        mu_z.append(z[4:6])
        # print(mu_z)
        params.array_mu_z = mu_z
        # print(x[0:2])
        # mu_x.append([x[0:2]])
        # mu_x.append([x[2:4]])
        # mu_x.append([x[4:6]])
        # params.array_mu_x = mu_x
        # params.array_mu_y = sample.iloc[12:24].to_numpy().reshape((6,2))
        # params.array_mu_z = sample.iloc[24:36].to_numpy().reshape((6,2))
        # print("mu_x")
        # print(params.array_mu_x)
        params.write_parameters(filename='configs/ffd_config_'+str(i)+'.prm')

    # Create wheelcase stl based on each config file
    for j in range(len(pop)):
        mesh_points_base = stl_handler.parse(filename='domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned.stl') # Base stl
        params.read_parameters(filename='configs/ffd_config_'+str(j)+'.prm')
        free_form = FFD(params,mesh_points_base)
        free_form.perform() # Perform FFD
        new_mesh_points = free_form.modified_mesh_points # Save new mesh of wheelcase
        stl_handler.write(new_mesh_points, 'stls/wheelcase_'+str(j)+'.stl') # save it in stls folder

    # execute openFoam for each stl (combine with top and velo stls)
    for k in range(len(pop)):
        # TODO: verketten der Kommandos mit &
        copy_cmd = "cp /stls/wheelcase_"+str(k)+" domain/wheelcase/hpc1_velo_changed/constant/triSurface"
        rename_cmd = "mv domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_"+str(k)+" domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned"
        os.system(copy_cmd)
        os.system(rename_cmd)


    # params.read_parameters(filename='domain/cube/ffd/deform_goal.prm')

    # goal_genome = np.concatenate((params.array_mu_x.flatten(), params.array_mu_y.flatten(), params.array_mu_z.flatten()), axis=None)
    # fitness_arr = []
    #
    # for i in range(len(pop)):
    #     a = pop.iloc[i,:].values
    #     # print("a")
    #     # print(a)
    #     s = np.sum(abs(a-goal_genome))
    #     fitness_arr.append(s)
    #
    # # make all values negative (high fitness is bad fitness)
    # fitness_arr = np.negative(fitness_arr)
    df_fitness = pd.DataFrame()

    return df_fitness
