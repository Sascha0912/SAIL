import numpy as np

def rastrigin_ValidateChildren(children, d):
    validInds = np.full(children.shape[0], True)

    return validInds