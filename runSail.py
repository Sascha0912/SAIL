from sail.sail import sail
from domain.rastrigin.rastrigin_Domain import rastrigin_Domain

class P:
    def __init__(self):
        # Edit hyperparameters
        self.nInitialSamples = 100
        self.nTotalSamples   = 200
        self.nChildren       = 2**5
        self.nGens           = 2**6

        self.data_mapEval    = False # produce intermediate prediction maps
        self.data_mapEvalMod = 50 # how often? (in samples)

# Algorithm hyperparameters
# p = sail # load default hyperparameters

# Edit hyperparameters
# p.nInitialSamples = 100
# p.nTotalSamples   = 200
# p.nChildren       = 2**5
# p.nGens           = 2**6
#
# p.data_mapEval = False # produce intermediate prediction maps
# p.data_mapEvalMod = 50 # how often? (in samples)

# Domain
d = rastrigin_Domain()
p = P()
# Run SAIL
runTime = 0 # tic
output = sail(p,d)
print('Runtime: ') # toc
