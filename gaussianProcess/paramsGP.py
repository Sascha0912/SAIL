import numpy as np
import pyGPs
import GPy

def paramsGP(nInputs):
    class P:
        def __init__(self):
            self.k        = GPy.kern.RBF(input_dim=nInputs, variance=1, lengthscale=0.5)
            self.lik      = GPy.likelihoods.Gaussian()
            # mf = GPy.core.Mapping(1,1)
            # mf.f = np.log(0.1)
            # mf = 
            self.meanfunc = GPy.mappings.Constant(2,1)
            self.dict = None
            
        #     m = GPy.models.GPRegression(X,Y,k)

            # print(nInputs)
        #     self.covfunc = pyGPs.cov.RBF(log_ell=-1., log_sigma=0.)
        #     # vec = np.zeros((nInputs,1))
        #     # print(vec)
        #     self.hyp_cov = np.zeros((nInputs+1,1)) # unit vector in log space
        #     # print(self.hyp_cov)
        #     self.meanfunc = pyGPs.mean.Linear( D=2 ) + pyGPs.mean.Const() # nur const mit mean 0
        #     self.hyp_mean = 0
        #     # self.likfunc = 'Gauss' # Gauss bereits implizit durch GPR Modell
        #     self.hyp_lik = np.log(0.1)
        #     self.functionEvals = 100 # function evals to optimize hyperparams

            # Zusatz k-nearest neighbour für Längenskala 


    return P()
