import numpy as np

def gPlot(*args):
    if len(args) == 1:
        input = args[0][args[0][:,2].argsort(),]   # (args[0],2)
        m = input[:,0]
        s2 = input[:,1]
        z = input[:,2]
    elif len(args) == 2:
        m = args[0][:,0].T
        s2 = args[0][:,1].T
        z = args[1]
    else
        m = args[0]
        s2 = args[1]
        z = args[2]

    f = [[m+2*np.sqrt(s2)], [np.flip(m-2*np.sqrt(s2),0)]]
