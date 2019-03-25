from sail.sail import sail
from domain.rastrigin.rastrigin_Domain import rastrigin_Domain
# from domain.velo.velo_Domain import velo_Domain
from sail.defaultParamSet import defaultParamSet

# class P:
#     def __init__(self):
        # Edit hyperparameters
        

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
# d = velo_Domain()
p = defaultParamSet()

p.nInitialSamples = 10
p.nTotalSamples   = 200
p.nChildren       = 2**5
p.nGens           = 2**6

p.data_mapEval    = False # produce intermediate prediction maps
p.data_mapEvalMod = 50    # how often? (in samples)

# Run SAIL
runTime = 0 # tic
output = sail(p,d)
print('Runtime: ') # toc