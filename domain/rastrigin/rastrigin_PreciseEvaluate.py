# import numpy as np
def rastrigin_PreciseEvaluate(observations, d):
    # shape = d.express(observations)
    # area  = np.squeeze()
    def feval(funcName,*args):
        return eval(funcName)(*args)
        
    # Get fitness of each individual
    fitness = feval(d.objFun, observations)

    # Get feature coordinates of each individual
    # behaviour = feval(d.getBc, observations)

    # Get miscellaneous values of each individual
    # miscVal = []
    # miscVal.append(np.random.rand(1,len(observations)))
    # miscVal.append(np.zeros((1,len(observations))))
       
    return fitness # TODO: check this return: is behaviour, fitness correct?