# TEST
import numpy as np
import math
import pandas as pd
def rastrigin_FitnessFunc(pop):
    def rastr(x):
        summ = 0
        summ += x[0]**2 - 10.0 * np.cos(2 * math.pi * x[0])
        summ += x[1]**2 - 10.0 * np.cos(2 * math.pi * x[1])
        return (20 + summ)/40

    genes = []
    print("pop")
    print(pop)
    for i in range(len(pop)):
        # genes.append(pop[i])
        genes.append(pop.iloc[i])
    df = pd.DataFrame(data=genes)
    # print(df)
    df_fitness = pd.DataFrame(data=rastr(df))
    df_fitness = df_fitness.transpose()

    return df_fitness
