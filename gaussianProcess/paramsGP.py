import numpy as np
import pyGPs

def paramsGP(nInputs):
    class P:
        def __init__(self):
            # print(nInputs)
            self.covfunc = pyGPs.cov.RBF
            # vec = np.zeros((nInputs,1))
            # print(vec)
            self.hyp_cov = np.zeros((nInputs+1,1)) # unit vector in log space
            print(self.hyp_cov)
            self.meanfunc = pyGPs.mean.Const
            self.hyp_mean = 0
            self.likfunc = 'Gauss' # Gauss
            self.hyp_lik = np.log(0.1)
            self.functionEvals = 100 # function evals to optimize hyperparams


    return P()
