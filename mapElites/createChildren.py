import numpy as np
import pandas as pd

def createChildren(map, nChildren, p, d):
    # Remove empty bins from parent pool
    if (isinstance(map,tuple)):
        if (isinstance(map[0],tuple)):
            map = map[0][0]
        else:
            map = map[0]

    # print("map.genes") # map.genes enthält nur in den ersten beiden 25x25 maps genome. Die anderen sind alle mit nan gefüllt
    # print(map.genes)
    parentPool = pd.DataFrame(data=np.empty([len(map.genes[0].index) * len(map.genes[0].columns), len(map.genes)]))
    # print("parentPool")
    # print(parentPool)
    # print("map.genes")
    # print(map.genes[0].to_numpy())
    # Reshaping to columns
    reshaped_genes = [] # index 1 = first attribute, ...
    for i in range(0,len(map.genes)):
        # print(map. genes[i].shape)
        # tmp_to_numpy = map.genes[i].to_numpy()
        reshaped_genes.append(map.genes[i].to_numpy().reshape(( map.genes[i].shape[0] * map.genes[i].shape[1], 1 ), order='F'))

    # print("reshaped")
    # print(reshaped_genes)
    k = 0 # counter for reshaped array
    for i in range(0, len(map.genes[0].index) * len(map.genes[0].columns)): # each sample (25)
        for j in range(0, len(map.genes)): # each attribute (2)
            entry = reshaped_genes[j][i][0]
            # if (np.isnan(entry)): # only checks first attribute of sample if nan
            #     break
            parentPool.at[i, j] = entry
            # if j==len(map.genes)-1:
            #     k = k+1
    parentPool.dropna(inplace=True)
    parentPool.reset_index(drop=True, inplace=True)
    # print("parentPool")
    # print(parentPool)
    # print("nChildren: " + str(nChildren))

    # Choose parents and create mutation
    selected_parents = np.random.randint(len(parentPool.index), size=nChildren)
    # print("selected_parents")
    # print(selected_parents)
    parents = parentPool.iloc[selected_parents,:]
    parents.reset_index(drop=True, inplace=True)
    # print("parents")
    # print(parents)
    mutation = pd.DataFrame(data=np.random.normal(size=(nChildren,d.dof)) * p.mutSigma)
    # print("mutation")
    # print(mutation)
    children = parents.add(mutation)

    # ADJUSTSCALE
    
    children[0] = children[0].clip(upper=0.2,lower=-0.2)
    children[1] = children[1].clip(upper=0.2,lower=-0.2)

    children[2] = children[2].clip(upper=0,lower=-2)
    children[3] = children[3].clip(upper=0,lower=-2)

    children[4] = children[4].clip(upper=0.2,lower=-0.2)
    children[5] = children[5].clip(upper=0.2,lower=-0.2)
    

    # children[children<-2] = -2 # DOMAINCHANGE
    # children[children>0] = 0
    # print("children")
    # print(children)
    # children[children<0] = 0
    # children[children>4] = 4


    # print("children")
    # print(children)
    return children
