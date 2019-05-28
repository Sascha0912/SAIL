# import pyGPs
import pandas as pd
import numpy as np

def predictGP(gpModel, input):
    # hyp = gpModel.hyp
    # print("input")
    # print(input)
    if (isinstance(input, pd.DataFrame)):
        input = input.to_numpy()
    elif isinstance(input, list):
        input = np.array(input)
    # print("input")
    # print(input)
    # print("gpModel")
    # print(gpModel)
    mean, var = gpModel.predict(input)
    return mean, var
