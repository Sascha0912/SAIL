import numpy as np
import pyPGs

def paramsGP(nInputs):
    class P:
        def __init__(self):
            self.covfunc = pyGPs.cov.RBF
            self.hyp_cov = [np.zeros(nInputs,1),[0]] # unit vector in log space
            
            self.meanfunc = pyGPs.mean.Const
            self.hyp_mean = 0
            self.likfunc = 'Gauss' # Gauss
            self.hyp_lik = np.log(0.1)
            self.functionEvals = 100 # function evals to optimize hyperparams
     

    return P()
