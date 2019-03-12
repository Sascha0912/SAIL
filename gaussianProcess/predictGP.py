import pyGPs
def predictGP(gpModel, input):
    # hyp = gpModel.hyp
    ym, ys2, fm, fs2, lp = gpModel.predict(input)
    return ym, ys2
