import numpy as np
from backend.soundnet import SoundNet, LEN_WAVEFORM
import os

nb_sounds = 10
nb_steps = 4 # 20s = 4 * 5s
obj_classes = 1000 # ImageNet
plc_classes = 401 # Enhanced Places365

out_objects = np.empty((1 << nb_sounds, 4, obj_classes))
out_places = np.empty((1 << nb_sounds, 4, plc_classes))

db_base = 'backend/db/'
featuriser = 'lua backend/featurise.lua '

# Construct the NN
model = SoundNet(LEN_WAVEFORM // 4)

for i in range(1, 1 << nb_sounds):
    # Generate bitstring
    bitstring = ''
    for j in range(nb_sounds):
        if i & (1 << j):
            bitstring += '1'
        else:
            bitstring += '0'

    print('Processing audio file', bitstring)
    
    # Pull out relevant mp3 file
    snd_name = db_base + bitstring + '.mp3 '
    # Lua-featurise it
    test_name = 'tmp.npy'
    lua_cmd = featuriser + snd_name + test_name
    os.system(lua_cmd)
    # Obtain the features
    X = np.load(test_name)
    # Feed the underlying features to the network
    Ys = model.forward(waveform=X)
    out_objects[i][0] = Ys['ps1'][0]
    out_places[i][0] = Ys['ps1'][1]
    out_objects[i][1] = Ys['ps2'][0]
    out_places[i][1] = Ys['ps2'][1]
    out_objects[i][2] = Ys['ps3'][0]
    out_places[i][2] = Ys['ps3'][1]
    out_objects[i][3] = Ys['ps4'][0]
    out_places[i][4] = Ys['ps4'][1]

np.save(db_base + 'objs_db.npy', out_objects)
np.save(db_base + 'plcs_db.npy', out_places)

