def wheelcase_AcquisitionFunc(drag,d):
    fitness = (drag[0] * d.muCoef) - (drag[1] * d.varCoef) # better fitness is lower fitness

    predValue = []
    predValue.insert(0,drag[0])
    predValue.insert(1,drag[1])

    return fitness, predValue