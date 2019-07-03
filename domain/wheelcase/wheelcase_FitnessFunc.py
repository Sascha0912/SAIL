import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

import math
import stl
from stl import mesh

# import subprocess
import os

def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz

def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)

def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies

# # Using an existing stl file:
# main_body = mesh.Mesh.from_file('ball_and_socket_simplified_-_main_body.stl')

# # rotate along Y
# main_body.rotate([0.0, 0.5, 0.0], math.radians(90))

# minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
# w1 = maxx - minx
# l1 = maxy - miny
# h1 = maxz - minz
# copies = copy_obj(main_body, (w1, l1, h1), 2, 2, 1)

# # I wanted to add another related STL to the final STL
# twist_lock = mesh.Mesh.from_file('ball_and_socket_simplified_-_twist_lock.stl')
# minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(twist_lock)
# w2 = maxx - minx
# l2 = maxy - miny
# h2 = maxz - minz
# translate(twist_lock, w1, w1 / 10., 3, 'x')
# copies2 = copy_obj(twist_lock, (w2, l2, h2), 2, 2, 1)
# combined = mesh.Mesh(numpy.concatenate([main_body.data, twist_lock.data] +
#                                     [copy.data for copy in copies] +
#                                     [copy.data for copy in copies2]))

# combined.save('combined.stl', mode=stl.Mode.ASCII)  # save as ASCII

def wheelcase_FitnessFunc(pop):
    # os.system('. /usr/local/stella/OpenFOAM/OpenFOAM-2.4.0/bin/tools/RunFunctions')
    fitness_values = []
    case_folder = 'domain/wheelcase/hpc1_velo_changed'
    home_dir = '/home/sobst2s/'
    # TODO: adapt Fitnessfunction for wheelcase
    params_left = FFDParameters()
    params_right = FFDParameters()
    stl_handler = StlHandler()
    params_left.read_parameters(filename='domain/wheelcase/ffd/ffd_config_left.prm') # Dummy config file
    params_right.read_parameters(filename='domain/wheelcase/ffd/ffd_config_right.prm')
    # print(pop)
    pop.to_csv('domain/wheelcase/pop.csv',mode='a+',index=False,header=False)


    # Generate config file for each sample
    for i in range(len(pop)):
        # Change displacements (weights) of each sample
        sample = pop.iloc[i] # get sample (1x36)
        # f = open("domain/wheelcase/debug.txt","a+")
        # f.write()
        # np.savetxt('domain/wheelcase/debug.txt',sample)
        # print("sample")
        # print(sample)
        mu_x = []
        mu_y = []
        mu_y_neg = []
        mu_z = []
        x = sample.iloc[:12].to_numpy().reshape((6,2))
        mu_x.append(x[0:2])
        mu_x.append(x[2:4])
        mu_x.append(x[4:6])
        # print(mu_x)
        params_left.array_mu_x = mu_x
        params_right.array_mu_x = mu_x

        y = sample.iloc[12:24].to_numpy().reshape((6,2))
        mu_y.append(y[0:2])
        mu_y.append(y[2:4])
        mu_y.append(y[4:6])
        mu_y_neg.append(-y[0:2])
        mu_y_neg.append(-y[2:4])
        mu_y_neg.append(-y[4:6])
        # print(mu_y)
        params_left.array_mu_y = mu_y
        params_right.array_mu_y = mu_y_neg

        z = sample.iloc[24:36].to_numpy().reshape((6,2))
        mu_z.append(z[0:2])
        mu_z.append(z[2:4])
        mu_z.append(z[4:6])
        # print(mu_z)
        params_left.array_mu_z = mu_z
        params_right.array_mu_z = mu_z
        # print(x[0:2])
        # mu_x.append([x[0:2]])
        # mu_x.append([x[2:4]])
        # mu_x.append([x[4:6]])
        # params.array_mu_x = mu_x
        # params.array_mu_y = sample.iloc[12:24].to_numpy().reshape((6,2))
        # params.array_mu_z = sample.iloc[24:36].to_numpy().reshape((6,2))
        # print("mu_x")
        # print(params.array_mu_x)
        params_left.write_parameters(filename='configs/ffd_config_left_'+str(i)+'.prm')
        params_right.write_parameters(filename='configs/ffd_config_right_'+str(i)+'.prm')
    print("config files generated")

    # Create wheelcase stl based on each config file
    for j in range(len(pop)):
        mesh_points_left = stl_handler.parse(filename='domain/wheelcase/ffd/wheelcase_turned_left.stl') # Base stl
        mesh_points_right = stl_handler.parse(filename='domain/wheelcase/ffd/wheelcase_turned_right.stl')
        params_left.read_parameters(filename='configs/ffd_config_left_'+str(j)+'.prm')
        params_right.read_parameters(filename='configs/ffd_config_right_'+str(j)+'.prm')

        free_form_left = FFD(params_left,mesh_points_left)
        free_form_left.perform() # Perform FFD

        free_form_right = FFD(params_right, mesh_points_right)
        free_form_right.perform()

        new_mesh_points_left = free_form_left.modified_mesh_points # Save new mesh of wheelcase
        stl_handler.write(new_mesh_points_left, 'stls/wheelcase_left_'+str(j)+'.stl') # save it in stls folder

        new_mesh_points_right = free_form_right.modified_mesh_points
        stl_handler.write(new_mesh_points_right, 'stls/wheelcase_right_'+str(j)+'.stl')

        # STLs zusammenfuegen - rechts und links
        left = mesh.Mesh.from_file('stls/wheelcase_left_'+str(j)+'.stl')
        right = mesh.Mesh.from_file('stls/wheelcase_right_'+str(j)+'.stl')

        # TODO: beide STLs zu einem zusammenfügen
        combined = mesh.Mesh(np.concatenate([left.data, right.data]))
        combined.save('stls/wheelcase_'+str(j)+'.stl', mode=stl.Mode.ASCII)
    print("slts generated")

    # config and stls correct
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
        # cd_cmd = "cd " + str(case_folder)
        blockMesh_cmd = "blockMesh -case " + home_dir + "SAIL/domain/wheelcase/hpc1_velo_changed"#-case " + str(case_folder)  + " -dict domain/wheelcase/hpc1_velo_changed/constant/polyMesh/blockMeshDict"
        # decompose_cmd = "runApplication decomposePar -case " + home_dir + "SAIL/domain/wheelcase/hpc1_velo_changed"
        snappy_cmd = "snappyHexMesh -case " + str(case_folder) + " -overwrite"
        # copy all the contents of 0.org to 0 folder (should exist at this point)
        copy_0org_cmd = "cp -a domain/wheelcase/hpc1_velo_changed/0.org/. domain/wheelcase/hpc1_velo_changed/0"
        # non parallel computation (TODO: look at Allrun for parallel run functions)
        openfoam_cmd = "patchSummary -case " + str(case_folder)
        potential_cmd = "potentialFoam -case " + str(case_folder)
        simple_cmd = "simpleFoam -case " + str(case_folder)

        # recParMesh_cmd = "runApplication reconstructParMesh -constant -case " + home_dir + "SAIL/domain/wheelcase/hpc1_velo_changed"
        # recPar_cmd = "runApplication reconstructPar -latestTime -case " + home_dir + "SAIL/domain/wheelcase/hpc1_velo_changed"
        # postprocess_cmd = ""
        # print(copy_cmd)
        os.system(copy_cmd)
        print("cp executed")
        # print(rename_cmd) # 105 - 165
        os.system(rename_cmd)
        print("renaming executed")
        # # testen ob case ausführbar ist
        # # os.system(source_of240_cmd)
        # print(openfoam_pre_cmd)
        os.system(openfoam_pre_cmd)
        print("surfaceFaetureExtract executed")
        
        # # print(cd_cmd)
        # # os.system(cd_cmd)
        # print(blockMesh_cmd)
        os.system(blockMesh_cmd)
        print("blockMesh executed")
        # exit()
        # # print(decompose_cmd)
        # # os.system(decompose_cmd)

        # print(snappy_cmd)
        os.system(snappy_cmd)
        print("snappy executed")
        

        # print(copy_0org_cmd)
        os.system(copy_0org_cmd)
        print("copying 0.org files to 0 folder")
        # print(openfoam_cmd)
        os.system(openfoam_cmd)
        print("patchSummary executed")
        # print(potential_cmd)
        os.system(potential_cmd)
        print("potentialFoam executed")
        # print(simple_cmd)
        os.system(simple_cmd)
        print("simpleFoam executed")

        # # print(recParMesh_cmd)
        # # os.system(recParMesh_cmd)
        # # print(recPar_cmd)
        # # os.system(recPar_cmd)
        # # Postprocessing - extraxt cD values
        data_force = np.loadtxt('domain/wheelcase/hpc1_velo_changed/postProcessing/forceCoeffs1/0/forceCoeffs.dat')
        df_force = pd.DataFrame(data=data_force)
        cD = df_force.iloc[:,2]
        # fitness is mean over the last 100 timesteps (inverted because lower cD (drag) is better)
        fitness = np.negative(cD.iloc[0:100].mean())
        print("FITNESS IS: " + str(fitness))
        fitness_values.append(fitness)
        # exit()

        # clean_cmd = "domain/wheelcase/hpc1_velo_changed/Allclean"
        clean_cmd1 = "rm -rf domain/wheelcase/hpc1_velo_changed/constant/extendedFeatureEdgeMesh"
        clean_cmd2 = "rm -f domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned.eMesh"
        clean_cmd3 = "rm -rf domain/wheelcase/hpc1_velo_changed/0"
        clean_cmd4 = "rm -r domain/wheelcase/hpc1_velo_changed/1* | rm -r domain/wheelcase/hpc1_velo_changed/2* | rm -r domain/wheelcase/hpc1_velo_changed/3* | rm -r domain/wheelcase/hpc1_velo_changed/4* | rm -r domain/wheelcase/hpc1_velo_changed/5* | rm -r domain/wheelcase/hpc1_velo_changed/6* | rm -r domain/wheelcase/hpc1_velo_changed/7* | rm -r domain/wheelcase/hpc1_velo_changed/8* | rm -r domain/wheelcase/hpc1_velo_changed/9* | rm -r domain/wheelcase/hpc1_velo_changed/postProcessing"
        # #TODO: delete polyMesh contents
        clean_cmd5 = "rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/faces | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/neighbour | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/owner | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/points | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/cellLevel | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/level0Edge | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/pointLevel | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/refinementHistory | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/surfaceIndex | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/faceZones | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/pointZones | rm -f domain/wheelcase/hpc1_velo_changed/constant/polyMesh/cellZones | rm -rf domain/wheelcase/hpc1_velo_changed/constant/polyMesh/sets"
        # # clean_cmd5 = "rm -v !('blockMeshDict')"
        # # clean_cmd4 = ". $WM_PROJECT_DIR/bin/tools/CleanFunctions"# & /home/sascha/Schreibtisch/SAIL/domain/wheelcase/hpc1_velo_changed/cleanCase"
        # # os.chdir('/home/sascha/Schreibtisch/SAIL/domain/wheelcase/hpc1_velo_changed')
        # # clean_cmd5 = "cleanCase"
        remove_wheelcase_cmd = "rm domain/wheelcase/hpc1_velo_changed/constant/triSurface/wheelcase_turned.stl"
        
        os.system(clean_cmd1)
        os.system(clean_cmd2)
        os.system(clean_cmd3)
        os.system(clean_cmd4)
        os.system(clean_cmd5)

        os.system(remove_wheelcase_cmd)
        print("wheelcase_turned.stl removed from hpc folder")

    print("end openfoam")

    remove_stls_cmd = "rm -r " + home_dir + "SAIL/stls/*"
    remove_configs_cmd = "rm -r " + home_dir + "SAIL/configs/*"
    os.system(remove_stls_cmd)
    os.system(remove_configs_cmd)
    
    # extract Fitness values (postProcessing folder)
    pd.DataFrame(data=fitness_values).to_csv('domain/wheelcase/fitness.csv',mode='a+',index=False,header=False)
    # for i in range(len(pop)):
        

    # np.savetxt('domain/wheelcase/debug.txt',fitness_values)
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
