import numpy as np
from backend.soundnet import SoundNet, LEN_WAVEFORM
import torch
from torch.autograd import Variable
import os

nb_sounds = 10
nb_steps = 4 # 20s = 4 * 5s
obj_classes = 1000 # ImageNet
plc_classes = 401 # Enhanced Places365

fname = 'backend/db/1111111111.mp3 '
featuriser = 'lua backend/featurise.lua '

# Construct the NN
model = SoundNet(LEN_WAVEFORM // 4)

if torch.cuda.is_available():
    model.cuda()

# Avoid code duplication
def unpack_cuda(variable):
    return np.squeeze((variable.data).cpu().numpy())

test_name = 'tmp.npy'
lua_cmd = featuriser + fname + test_name
os.system(lua_cmd)
# Obtain the features
X = np.load(test_name)
X = X[:,:,:LEN_WAVEFORM,:].astype('float32')
X = Variable(torch.from_numpy(X.reshape(1, 1, LEN_WAVEFORM))).cuda()
# Feed the underlying features to the network
Ys = model.forward(waveform=X)
np.save('obj0.npy', unpack_cuda(Ys['ps1'][0]))
np.save('obj1.npy', unpack_cuda(Ys['ps2'][0]))
np.save('obj2.npy', unpack_cuda(Ys['ps3'][0]))
np.save('obj3.npy', unpack_cuda(Ys['ps4'][0]))

