# from pygem import FFDParameters, FFD, StlHandler
from domain.cube.cube_FitnessFunc import cube_FitnessFunc

def cube_PreciseEvaluate(observations, d):
    # observation:
    # print("observations")
    # print(observations)
    def feval(funcName,*args):
        return eval(funcName)(*args)

    fitness = feval(d.objFun, observations)
    fitness = fitness.T
    
    return fitness
