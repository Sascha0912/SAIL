import pyGPs
import numpy as np

def trainGP(input, output, d, **kwargs):
    for key, value in kwargs.items():
        if key=="functionEvals":
            functionEvals = value
            print(functionEvals)
	    
    model = pyGPs.GPR()
    model.setPrior(mean=d.meanfunc, kernel=d.covfunc)
    model.useLikelihood(d.likfunc)


    model.getPosterior(input, output)
    model.optimize(input, output)

    return model
