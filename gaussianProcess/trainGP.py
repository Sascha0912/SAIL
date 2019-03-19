import pyGPs
import numpy as np

def trainGP(input, output, d, **kwargs):
    for key, value in kwargs.items():
        if key=="functionEvals":
            functionEvals = value
            # print(functionEvals)
    # print("d.meanfunc")
    # print(d.meanfunc)   
    model = pyGPs.GPR()
    model.setPrior(mean=d.meanfunc, kernel=d.covfunc)
    # model.useLikelihood(d.likfunc) # Gauss ist bereits implizit durch GPR Modell gesetzt

    print("input")
    print(input)
    print("output")
    print(output)
    model.getPosterior(input, output)
    model.optimize(input, output)

    return model
