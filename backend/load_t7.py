# Load t7 files
# Required package: torchfile.
# $ pip install torchfile

import torchfile
import numpy as np
import pdb

# Make xrange compatible in both Python 2, 3
try:
    xrange
except NameError:
    xrange = range

keys = ['conv1', 'conv2', 'conv3', 'conv4', 'conv5', 'conv6',
        'conv7', 'conv8', 'conv8_2']

def load(o, param_list):
    """ Get torch7 weights into numpy array """
    try:
        num = len(o['modules'])
    except:
        num = 0

    for i in xrange(num):
        # 2D conv
        if o['modules'][i]._typename == 'nn.SpatialConvolution' or \
            o['modules'][i]._typename == 'cudnn.SpatialConvolution':
            temp = {'weights': o['modules'][i]['weight'].transpose((2,3,1,0)),
                    'biases': o['modules'][i]['bias']}
            param_list.append(temp)
        # 2D deconv
        elif o['modules'][i]._typename == 'nn.SpatialFullConvolution':
            temp = {'weights': o['modules'][i]['weight'].transpose((2,3,1,0)),
                    'biases': o['modules'][i]['bias']}
            param_list.append(temp)
        # 3D conv
        elif o['modules'][i]._typename == 'nn.VolumetricFullConvolution':
            temp = {'weights': o['modules'][i]['weight'].transpose((2,3,4,1,0)),
                    'biases': o['modules'][i]['bias']}
            param_list.append(temp)
        # batch norm
        elif o['modules'][i]._typename == 'nn.SpatialBatchNormalization' or \
            o['modules'][i]._typename == 'nn.VolumetricBatchNormalization':
            param_list[-1]['gamma'] = o['modules'][i]['weight']
            param_list[-1]['beta'] = o['modules'][i]['bias']
            param_list[-1]['mean'] = o['modules'][i]['running_mean']
            param_list[-1]['var'] = o['modules'][i]['running_var']

        if o['modules'][i]._typename == 'nn.ConcatTable'.encode('ASCII'):
            print("Final conv layers")

            print("Bias", o['modules'][i]['modules'][0]['bias'].shape)
            print("Weights", o['modules'][i]['modules'][0]['weight'].shape)

            print("Bias", o['modules'][i]['modules'][1]['bias'].shape)
            print("Weights", o['modules'][i]['modules'][1]['weight'].shape)

            np.array(o['modules'][i]['modules'][0]['bias']).tofile('conv81_bs.npy')
            np.array(o['modules'][i]['modules'][0]['weight']).tofile('conv81_ws.npy')

            np.array(o['modules'][i]['modules'][1]['bias']).tofile('conv82_bs.npy')
            np.array(o['modules'][i]['modules'][1]['weight']).tofile('conv82_ws.npy')

        load(o['modules'][i], param_list)


def show(o):
    """ Show nn information """
    nn = {}
    nn_keys = {}
    nn_info = {}
    num = len(o['modules']) if o['modules'] else 0
    mylist = get_mylist()

    for i in xrange(num):
        # Get _obj and keys from torchfile
        nn[i] = o['modules'][i]._obj
        nn_keys[i] = o['modules'][i]._obj.keys()

        # Get information from _obj
        # {layer i: {mylist keys: value}}
        nn_info[i] = {key: nn[i][key] for key in sorted(nn_keys[i]) if key in mylist}
        nn_info[i]['name'] = o['modules'][i]._typename
        bias_key = 'gradBias'.encode('ASCII')
        weight_key = 'gradWeight'.encode('ASCII')
        if bias_key in list(nn_keys[i]) or weight_key in list(nn_keys[i]):
            if nn_info[i]['name'].find('Convolution'.encode('ASCII')) != -1 or\
               nn_info[i]['name'].find('Batch'.encode('ASCII')) != -1:
                print(i, nn_info[i]['name'])
                print("Bias", nn[i][bias_key].shape)
                print("Weights", nn[i][weight_key].shape)
                if i == 0:
                    np.array(nn[i][weight_key]).tofile('conv1_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv1_bs.npy')
                elif i == 4:
                    np.array(nn[i][weight_key]).tofile('conv2_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv2_bs.npy')
                elif i == 8:
                    np.array(nn[i][weight_key]).tofile('conv3_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv3_bs.npy')
                elif i == 11:
                    np.array(nn[i][weight_key]).tofile('conv4_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv4_bs.npy')
                elif i == 14:
                    np.array(nn[i][weight_key]).tofile('conv5_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv5_bs.npy')
                elif i == 18:
                    np.array(nn[i][weight_key]).tofile('conv6_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv6_bs.npy')
                elif i == 21:
                    np.array(nn[i][weight_key]).tofile('conv7_ws.npy')
                    np.array(nn[i][bias_key]).tofile('conv7_bs.npy')
                elif i == 1:
                    np.array(nn[i][weight_key]).tofile('bn1_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn1_bs.npy')
                elif i == 5:
                    np.array(nn[i][weight_key]).tofile('bn2_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn2_bs.npy')
                elif i == 9:
                    np.array(nn[i][weight_key]).tofile('bn3_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn3_bs.npy')
                elif i == 12:
                    np.array(nn[i][weight_key]).tofile('bn4_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn4_bs.npy')
                elif i == 15:
                    np.array(nn[i][weight_key]).tofile('bn5_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn5_bs.npy')
                elif i == 19:
                    np.array(nn[i][weight_key]).tofile('bn6_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn6_bs.npy')
                elif i == 22:
                    np.array(nn[i][weight_key]).tofile('bn7_ws.npy')
                    np.array(nn[i][bias_key]).tofile('bn7_bs.npy')
        """
        for item in sorted(nn_info[i].keys()):
            print("  {}:{}".format(item, nn_info[i][item] if 'running' not in item \
                                                        else nn_info[i][item].shape))
        """


def get_mylist():
    """ Return manually selected information lists """
    return ['_type', 'nInputPlane', 'nOutputPlane', \
            'input_offset', 'groups', 'dH', 'dW', \
            'padH', 'padW', 'kH', 'kW', 'iSize', \
            'running_mean', 'running_var']


if __name__ == '__main__':
    # File loader
    t7_file = '../../soundnet_models_public/soundnet8_final.t7'
    o = torchfile.load(t7_file)

    # To show nn parameter
    show(o)

    # To store as npy file
    param_list = []
    load(o, param_list)
    print(param_list)
    """
    save_list = {}
    for i, k in enumerate(keys):
        save_list[k] = param_list[i]
    np.save('sound8', save_list)
    """
