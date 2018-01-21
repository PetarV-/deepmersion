import numpy as np
import sys

mst = {}

indices = np.empty(365)

with open(sys.argv[2], 'r') as f:
    for line in f:
        els = line.split()
        mst[els[0]] = els[1]

with open(sys.argv[1], 'r') as f:
    for line in f:
        els = line.split()
        if els[0] in mst:
            indices[int(mst[els[0]])] = els[1]
            print(mst[els[0]], '->', els[1])
    
np.save('mask.npy', indices)

