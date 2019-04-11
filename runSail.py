from sail.sail import sail
from domain.rastrigin.rastrigin_Domain import rastrigin_Domain
# from domain.velo.velo_Domain import velo_Domain
from sail.defaultParamSet import defaultParamSet
import time
import pandas as pd
from sail.createPredictionMap import createPredictionMap
from visualization.viewMap import viewMap

# IN CASE OF ERRORS:
# 
# 1.) CHECK if Sobol Sequence is big enough (default is 10k) [IndexError: positional indexers are out-of-bounds]
# 

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

p.nInitialSamples = 20
p.nTotalSamples   = 40
p.nChildren       = 2**5
p.nGens           = 2**6 # Illumination Generations

p.data_mapEval    = False # produce intermediate prediction maps
p.data_mapEvalMod = 50    # how often? (in samples)

# Run SAIL
runTime = time.time() # tic
output = sail(p,d)
endTime = time.time()
print('Runtime: ' + str(endTime - runTime)) # toc

# Create new Prediction map from produced surrogate
# Adjust hyperparameters
p.nGens = 2*p.nGens
observations_df = pd.DataFrame(data=output.model[0].X.values.tolist())
print("observations_df")
print(observations_df.to_string())
predMap, percImproved = createPredictionMap(output.model, observations_df, p, d, featureRes=[25,25])
# print("viewMap")
viewMap(predMap[0], d)