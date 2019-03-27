def rastrigin_AcquisitionFunc(drag,d):
    # print("drag[0]")
    # print(drag[0])
    fitness = (drag[0] * d.muCoef) - (drag[1] * d.varCoef)
    # print("fitness")
    # print(fitness)
    predValue = []
    predValue.insert(0,drag[0])
    predValue.insert(1,drag[1])

    # print("rastr_fitness")
    # print(fitness)
    # print("rastr_predvalue")
    # print(predValue)


    return fitness, predValue