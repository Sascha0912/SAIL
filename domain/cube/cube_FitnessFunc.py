import numpy as np
import math
import pandas as pd

from pygem import FFDParameters, FFD, StlHandler

def cube_FitnessFunc(pop):#
    print("pop")
    print(pop)
    stl_handler = StlHandler()
    goal_mesh_points = stl_handler.parse('domain/cube/ffd/goal.stl')

    goal_df = pd.DataFrame(data=goal_mesh_points)

    for i in range(len(pop)):
        pass
