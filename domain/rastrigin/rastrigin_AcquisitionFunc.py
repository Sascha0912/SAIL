def rastrigin_AcquisitionFunc(drag,lift,deform,d):
    fitness = (drag[:,0] * d.muCoef) - (drag[:,1] * d.varCoef)
    predValue = []
    predValue.insert(0,drag[:,0])
    predValue.insert(1,drag[:,1])

    print("rastr_fitness")
    print(fitness)
    print("rastr_predvalue")
    print(predValue)


    return fitness, predValue