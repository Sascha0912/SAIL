import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

import math
import stl
from stl import mesh

# import subprocess
import os

def wheelcase_FitnessFunc(pop):

    def downscaleXandZ(value, max_orig, min_orig, max_goal, min_goal):
        return (value - min_orig)/(max_orig-min_orig)*(max_goal-min_goal)+min_goal

    # os.system('. /usr/local/stella/OpenFOAM/OpenFOAM-2.4.0/bin/tools/RunFunctions')
    fitness_values = []
    case_folder = 'domain/wheelcase/hpc1_velo_changed'
    home_dir = '/home/sascha/'
    # TODO: adapt Fitnessfunction for wheelcase
    params_left = FFDParameters()
    params_right = FFDParameters()

    # stl_handler_wheel = StlHandler()
    # stl_handler_velo = StlHandler()
    # stl_handler_top = StlHandler()
    stl_handler_all = StlHandler()

    params_left.read_parameters(filename='domain/wheelcase/ffd/ffd_config_left.prm') # Dummy config file
    params_right.read_parameters(filename='domain/wheelcase/ffd/ffd_config_right.prm')
    
    # pop.to_csv('domain/wheelcase/pop.csv',mode='a+',index=False,header=False)

    # WORKAROUND because of OpenFOAM error when faces of mesh intersect -> x and z deformation downscale

    # TODO: Teste ob hier die pop Werte schon skalierst sind
    # print("pop_before")
    # print(pop)

    # pop[0] = pop[0].apply(lambda x : downscaleXandZ(x,0,-2,0.2,-0.2))
    # pop[1] = pop[1].apply(lambda x : downscaleXandZ(x,0,-2,0.2,-0.2))
    # pop[4] = pop[4].apply(lambda x : downscaleXandZ(x,0,-2,0.2,-0.2))
    # pop[5] = pop[5].apply(lambda x : downscaleXandZ(x,0,-2,0.2,-0.2))
    pop.to_csv('domain/wheelcase/pop.csv',mode='a+',index=False,header=False)
    # print("pop")
    # print(pop)

    # Generate config file for each sample
    # print("len(pop)")
    # print(len(pop))
    for i in range(len(pop)):

        # Change displacements (weights) of each sample
        sample = pop.iloc[i] # get sample (1x6)

        # add penalty if abs(bottom ffd value ) < 1.5
        # and abs(top ffd value) < 0.2
        if (sample.iloc[2:4].to_numpy().reshape((1,2))[0,0] > -1.5 or sample.iloc[2:4].to_numpy().reshape((1,2))[0,1] > -0.2):
            fitness_values.append(-1)
        else:
            fitness_values.append(0)

        mu_x = []
        mu_x_right = []
        mu_y = []
        mu_y_right = []
        mu_z = []
        mu_z_right = []

        tmp_list = []

        x = sample.iloc[:2].to_numpy().reshape((1,2))

        # for 6 genomes
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_x.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([x[0,0],x[0,1]])
        mu_x.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_x.append(tmp_list.copy())
        del tmp_list[:]


        # for 18 genomes
        # tmp_list.append([0,0])
        # tmp_list.append([x[0,0],x[0,1]])
        # mu_x.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([0,0])
        # tmp_list.append([x[1,0],x[1,1]])
        # mu_x.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([0,0])
        # tmp_list.append([x[2,0],x[2,1]])
        # mu_x.append(tmp_list.copy())
        # del tmp_list[:]

        # for 36 genomes
        # mu_x.append(x[0:2])
        # mu_x.append(x[2:4])
        # mu_x.append(x[4:6])
        # print(mu_x)
        # print(mu_x)
        params_left.array_mu_x = mu_x

        # for right side: different coords
        # Reihenfolge
        # 2,3,0,1,6,7,4,5,10,11,8,9

        # for 36 genomes
        # tmp_list.append([x[1,0],x[1,1]])
        # tmp_list.append([x[0,0],x[0,1]])
        # mu_x_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([x[3,0],x[3,1]])
        # tmp_list.append([x[2,0],x[2,1]])
        # mu_x_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([x[5,0],x[5,1]])
        # tmp_list.append([x[4,0],x[4,1]])
        # mu_x_right.append(tmp_list.copy())
        # del tmp_list[:]

        # for 6 genomes
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_x_right.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([x[0,0],x[0,1]])
        tmp_list.append([0,0])
        mu_x_right.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_x_right.append(tmp_list.copy())
        del tmp_list[:]


        # for 18 genomes
        # tmp_list.append([x[0,0],x[0,1]])
        # tmp_list.append([0,0])
        # mu_x_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([x[1,0],x[1,1]])
        # tmp_list.append([0,0])
        # mu_x_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([x[2,0],x[2,1]])
        # tmp_list.append([0,0])
        # mu_x_right.append(tmp_list.copy())
        # del tmp_list[:]




        params_right.array_mu_x = mu_x_right


        y = sample.iloc[2:4].to_numpy().reshape((1,2))

        # for 36 genomes
        # mu_y.append(y[0:2])
        # mu_y.append(y[2:4])
        # mu_y.append(y[4:6])


        # for 6 genomes
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_y.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([y[0,0],y[0,1]])
        mu_y.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_y.append(tmp_list.copy())
        del tmp_list[:]


        # for 18 genomes
        # tmp_list.append([0,0])
        # tmp_list.append([y[0,0],y[0,1]])
        # mu_y.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([0,0])
        # tmp_list.append([y[1,0],y[1,1]])
        # mu_y.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([0,0])
        # tmp_list.append([y[2,0],y[2,1]])
        # mu_y.append(tmp_list.copy())
        # del tmp_list[:]

        params_left.array_mu_y = mu_y

        # for 6 genomes
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_y_right.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([-y[0,0],-y[0,1]])
        tmp_list.append([0,0])
        mu_y_right.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_y_right.append(tmp_list.copy())
        del tmp_list[:]

        # for 18 genomes
        # tmp_list.append([-y[0,0],-y[0,1]])
        # tmp_list.append([0,0])
        # mu_y_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([-y[1,0],-y[1,1]])
        # tmp_list.append([0,0])
        # mu_y_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([-y[2,0],-y[2,1]])
        # tmp_list.append([0,0])
        # mu_y_right.append(tmp_list.copy())
        # del tmp_list[:]

        params_right.array_mu_y = mu_y_right


        z = sample.iloc[4:6].to_numpy().reshape((1,2))
        # mu_z.append(z[0:2])
        # mu_z.append(z[2:4])
        # mu_z.append(z[4:6])


        # for 6 genomes
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_z.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([z[0,0],z[0,1]])
        mu_z.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_z.append(tmp_list.copy())
        del tmp_list[:]

        # for 18 genomes
        # tmp_list.append([0,0])
        # tmp_list.append([z[0,0],z[0,1]])
        # mu_z.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([0,0])
        # tmp_list.append([z[1,0],z[1,1]])
        # mu_z.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([0,0])
        # tmp_list.append([z[2,0],z[2,1]])
        # mu_z.append(tmp_list.copy())
        # del tmp_list[:]


        params_left.array_mu_z = mu_z

        # for 6 genomes
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_z_right.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([z[0,0],z[0,1]])
        tmp_list.append([0,0])
        mu_z_right.append(tmp_list.copy())
        del tmp_list[:]
        tmp_list.append([0,0])
        tmp_list.append([0,0])
        mu_z_right.append(tmp_list.copy())
        del tmp_list[:]

        # for 18 genomes
        # tmp_list.append([z[0,0],z[0,1]])
        # tmp_list.append([0,0])
        # mu_z_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([z[1,0],z[1,1]])
        # tmp_list.append([0,0])
        # mu_z_right.append(tmp_list.copy())
        # del tmp_list[:]
        # tmp_list.append([z[2,0],z[2,1]])
        # tmp_list.append([0,0])
        # mu_z_right.append(tmp_list.copy())
        # del tmp_list[:]

        params_right.array_mu_z = mu_z_right

        params_left.write_parameters(filename='configs/ffd_config_left_'+str(i)+'.prm')
        params_right.write_parameters(filename='configs/ffd_config_right_'+str(i)+'.prm')
    print("config files generated")
    # print("fitness values")
    # print(fitness_values)


    # Create wheelcase stl based on each config file
    for j in range(len(pop)):
        params_left.read_parameters(filename='configs/ffd_config_left_'+str(j)+'.prm')
        params_right.read_parameters(filename='configs/ffd_config_right_'+str(j)+'.prm')

        mesh_points_all = stl_handler_all.parse(filename='/home/sascha/SAIL/domain/wheelcase/ffd/combined_180.stl')

        free_form = FFD(params_left,mesh_points_all)
        free_form.perform() # Perform FFD
        new_mesh_points = free_form.modified_mesh_points # Save new mesh of wheelcase

        free_form = FFD(params_right,new_mesh_points)
        free_form.perform()
        mesh_points_final = free_form.modified_mesh_points

        stl_handler_all.write(mesh_points_final, 'stls/all_deformed_' + str(j) + '.stl')
    print("slts generated")

    # config and stls correct
    # execute openFoam for each stl (combine with top and velo stls)
    # long running loop (!)
    print("start openfoam")
    for k in range(len(pop)):

        copy_cmd = "cp stls/all_deformed_"+str(k)+".stl domain/wheelcase/hpc1_velo_changed/constant/triSurface"

        rename_cmd = "mv domain/wheelcase/hpc1_velo_changed/constant/triSurface/all_deformed_"+str(k)+".stl domain/wheelcase/hpc1_velo_changed/constant/triSurface/all_deformed.stl"

        print("cp: " + str(os.system(copy_cmd)))
        print("cp executed")

        print("renaming: " + str(os.system(rename_cmd)))
        print("renaming executed")
        os.chdir("/home/sascha/SAIL/domain/wheelcase/hpc1_velo_changed")
        os.system("./Allrun")

        data_force = np.loadtxt('/home/sascha/SAIL/domain/wheelcase/hpc1_velo_changed/postProcessing/forceCoeffs1/0/forceCoeffs.dat')
        df_force = pd.DataFrame(data=data_force)
        cD = df_force.iloc[:,2]
        cD.to_csv('drag'+str(k)+'.csv')
        # fitness is mean over the last 100 timesteps (inverted because lower cD (drag) is better)
        fitness = np.negative(cD.iloc[100:200].mean()) # OpenFOAM 200 timesteps -> controlDict
        print("FITNESS IS: " + str(fitness))
        fitness_values[k] += fitness

        remove_wheelcase_cmd = "rm /home/sascha/SAIL/domain/wheelcase/hpc1_velo_changed/constant/triSurface/all_deformed.stl"

        os.system("./Allclean")
        os.system(remove_wheelcase_cmd)
        os.chdir("/home/sascha/SAIL")
        print("wheelcase_turned.stl removed from hpc folder")

    print("end openfoam")
    # print("fitness values after")
    # print(fitness_values)

    remove_stls_cmd = "rm -r " + home_dir + "SAIL/stls/*"
    remove_configs_cmd = "rm -r " + home_dir + "SAIL/configs/*"
    os.system(remove_stls_cmd)
    os.system(remove_configs_cmd)

    # extract Fitness values (postProcessing folder)
    pd.DataFrame(data=fitness_values).to_csv('domain/wheelcase/fitness.csv',mode='a+',index=False,header=False)

    df_fitness = pd.DataFrame(data=fitness_values).transpose()

    return df_fitness