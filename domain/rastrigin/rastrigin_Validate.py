import numpy as np

def rastrigin_Validate(genomes, d):
    validInds = np.full(genomes.shape[0], True)
