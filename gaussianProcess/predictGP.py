import pyGPs

def predictGP(gpModel, input):
    # hyp = gpModel.hyp
    input = input.to_numpy()
    print("input")
    print(input)
    print("gpModel")
    print(gpModel)
    ym, ys2, fm, fs2, lp = gpModel.predict(input)
    return ym, ys2
