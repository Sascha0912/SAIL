import numpy as np
import pandas as pd

def wheelcase_DummyPreciseEvaluate(observations, d):
    # just return the sum of each element of one observation as fitness value
    df_fitness = pd.DataFrame(data=observations.sum(axis=1))
    # print("observations")
    # print(observations)
    # print("df_fitness")
    # print(df_fitness)
    return df_fitness
