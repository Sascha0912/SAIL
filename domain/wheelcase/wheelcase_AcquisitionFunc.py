def wheelcase_AcquisitionFunc(drag,d):
    # print("Drag0: " + str(drag[0]))
    # print("Drag1: " + str(drag[1]))
    fitness = (drag[0] * d.muCoef) + (drag[1] * d.varCoef) # better fitness is higher fitness

    predValue = []
    predValue.insert(0,drag[0])
    predValue.insert(1,drag[1])

    return fitness, predValue