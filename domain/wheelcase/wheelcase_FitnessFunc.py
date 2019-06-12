import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

# import subprocess
import os

def wheelcase_FitnessFunc(pop):
    fitness_values = []
    case_folder = 'domain/wheelcase/hpc1_velo_changed'
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
    print("config files generated")
    # Create wheelcase stl based on each config file
    for j in range(len(pop)):
        mesh_points_base = stl_handler.parse(filename='domain/wheelcase/ffd/wheelcase_turned.stl') # Base stl
        params.read_parameters(filename='configs/ffd_config_'+str(j)+'.prm')
        free_form = FFD(params,mesh_points_base)
        free_form.perform() # Perform FFD
        new_mesh_points = free_form.modified_mesh_points # Save new mesh of wheelcase
        stl_handler.write(new_mesh_points, 'stls/wheelcase_'+str(j)+'.stl') # save it in stls folder
    print("slts generated")
    # execute openFoam for each stl (combine with top and velo stls)
    # long running loop (!)
    print("start openfoam")
    for k in range(len(pop)):
        # TODO: verketten der Kommandos mit &
        copy_cmd = "cp stls/wheelcase_"+str(k)+".stl domain/wheelcase/hpc1_velo_changed/constant/triSurface"
        rename_cmd = "mv domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_"+str(k)+".stl domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned.stl"
        # source_of240_cmd = "of240" # check if this alias exist
        # source_of240_cmd = "source ~/OpenFOAM/OpenFOAM-2.4.0/etc/bashrc WM_NCOMPPROCS=6"
        openfoam_pre_cmd = "surfaceFeatureExtract -case " + str(case_folder)
        cd_cmd = "cd " + str(case_folder)
        blockMesh_cmd = "blockMesh -case /home/sascha/Schreibtisch/SAIL/domain/wheelcase/hpc1_velo_changed"#-case " + str(case_folder)  + " -dict domain/wheelcase/hpc1_velo_changed/constant/polyMesh/blockMeshDict"
        snappy_cmd = "snappyHexMesh -case " + str(case_folder) + " -overwrite"
        # copy all the contents of 0.org to 0 folder (should exist at this point)
        copy_0org_cmd = "cp -a domain/wheelcase/hpc1_velo_changed/0.org/. domain/wheelcase/hpc1_velo_changed/0"
        # non parallel computation (TODO: look at Allrun for parallel run functions)
        openfoam_cmd = "patchSummary -case " + str(case_folder)
        potential_cmd = "potentialFoam -case " + str(case_folder)
        simple_cmd = "simpleFoam -case " + str(case_folder)
        # postprocess_cmd = ""
        print(copy_cmd)
        os.system(copy_cmd)
        print(rename_cmd)
        os.system(rename_cmd)
        # os.system(source_of240_cmd)
        print(openfoam_pre_cmd)
        os.system(openfoam_pre_cmd)
        # print(cd_cmd)
        # os.system(cd_cmd)
        print(blockMesh_cmd)
        os.system(blockMesh_cmd)
        print(snappy_cmd)
        os.system(snappy_cmd)

        print(copy_0org_cmd)
        os.system(copy_0org_cmd)
        print(openfoam_cmd)
        os.system(openfoam_cmd)
        print(potential_cmd)
        os.system(potential_cmd)
        print(simple_cmd)
        os.system(simple_cmd)
        # Postprocessing - extraxt cD values
        data_force = np.loadtxt('domain/wheelcase/hpc1_velo_changed/postProcessing/forceCoeffs1/0/forceCoeffs.dat')
        df_force = pd.DataFrame(data=data_force)
        cD = df_force.iloc[:,2]
        # fitness is mean over the last 100 timesteps (inverted because lower cD (drag) is better)
        fitness = np.negative(cD.iloc[900:1000].mean())
        fitness_values.append(fitness)


        # clean_cmd = "domain/wheelcase/hpc1_velo_changed/Allclean"
        clean_cmd1 = "\\rm -rf domain/wheelcase/hpc1_velo_changed/constant/extendedFeatureEdgeMesh"
        clean_cmd2 = "\\rm -f domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned.eMesh"
        clean_cmd3 = "rm -rf domain/wheelcase/hpc1_velo_changed/0"
        clean_cmd4 = "rm -r 0* & rm -r 1* & rm -r 2* & rm -r 3* &rm -r 4* & rm -r 5* & rm -r 6* & rm -r 7* & rm -r 8* & rm -r 9* & rm -r postProcessing"
        #TODO: delete polyMesh contents
        # clean_cmd4 = ". $WM_PROJECT_DIR/bin/tools/CleanFunctions"# & /home/sascha/Schreibtisch/SAIL/domain/wheelcase/hpc1_velo_changed/cleanCase"
        # os.chdir('/home/sascha/Schreibtisch/SAIL/domain/wheelcase/hpc1_velo_changed')
        # clean_cmd5 = "cleanCase"
        remove_wheelcase_cmd = "rm domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned.stl"
        os.system(clean_cmd1)
        os.system(clean_cmd2)
        os.system(clean_cmd3)
        os.system(clean_cmd4)
        os.system(remove_wheelcase_cmd)
    print("end openfoam")
        # extract Fitness values (postProcessing folder)


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
    df_fitness = pd.DataFrame(data=fitness_values).transpose()

    return df_fitness
