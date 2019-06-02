from domain.wheelcase.wheelcase_FitnessFunc import wheelcase_FitnessFunc

def wheelcase_PreciseEvaluate(observations, d):
    # observation:
    # print("observations")
    # print(observations)
    def feval(funcName,*args):
        return eval(funcName)(*args)

    fitness = feval(d.objFun, observations)
    fitness = fitness.T

    return fitness
