import pyGPs

def predictGP(gpModel, input):
    # hyp = gpModel.hyp
    input = input.to_numpy()
    # print("input")
    # print(input)
    # print("gpModel")
    # print(gpModel)
    mean, var = gpModel.predict(input)
    return mean, var
