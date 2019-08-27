import numpy as np

def wheelcase_ValidateChildren(children, d):
    # All children are valid
    validInds = np.full(children.shape[0], True)
    return validInds