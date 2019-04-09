import pyGPs
import numpy as np
import GPy

def trainGP(input, output, d, **kwargs):
    for key, value in kwargs.items():
        if key=="functionEvals":
            functionEvals = value
            # print(functionEvals)

    input = input.values # to numpy array    
    output = output[:,np.newaxis] 

    print("input")
    print(input)
    print("output")
    print(output)
#     print("d")
#     print(d)
    if not isinstance(d, GPy.core.GP):
        m = GPy.core.GP(input, output, kernel=d.k, likelihood=d.lik, mean_function=d.meanfunc)
    else:
        m = GPy.core.GP._build_from_input_dict(d.dict)    
#     print("model")
#     print(m)
#     m = GPy.models.GPRegression(input,output,d.k)    
    # print("d.meanfunc")
    # print(d.meanfunc)   
#     model = pyGPs.GPR()
#     model.setPrior(mean=d.meanfunc, kernel=d.covfunc)
    # model.useLikelihood(d.likfunc) # Gauss ist bereits implizit durch GPR Modell gesetzt

#     print("input")
#     print(input.values)
#     print("output")
#     print(output.values)
    m.optimize(max_iters=100)    
    # model.getPosterior(input.values, output.values)
    # print("getPosterior")
    # print("input.values")
    # print(input.values)
    # print("output.values")
    # print(output.values)
    # model.optimize(input.values, output.values)
    # print("optimize")
    return m
