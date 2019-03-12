from sail.sail import sail
from domain.rastrigin.rastrigin_Domain import rastrigin_Domain
# Algorithm hyperparameters
p = sail # load default hyperparameters

# Edit hyperparameters
p.nInitialSamples = 100
p.nTotalSamples   = 200
p.nChildren       = 2**5
p.nGens           = 2**6

p.data_mapEval = False # produce intermediate prediction maps
p.data_mapEvalMod = 50 # how often? (in samples)

# Domain
d = rastrigin_Domain()

# Run SAIL
runTime = 0 # tic
output = sail(p,d)
print('Runtime: ') # toc
