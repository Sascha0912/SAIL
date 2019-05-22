from pygem import FFDParameters, FFD, StlHandler

# Function takes a list of sets of meshpoints and assigns a fitness values
def cube_PreciseEvaluate(observations, d):
    # observation:
    def feval(funcName,*args):
        return eval(funcName)(*args)

    fitness = feval(d.objFun, observations)
    fitness = fitness.T
    
    return fitness
