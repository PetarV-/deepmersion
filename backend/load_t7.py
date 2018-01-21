import torchfile
import numpy as np


# Make xrange compatible in both Python 2, 3
try:
    xrange
except NameError:
    xrange = range


def save_layer_params(o):
    """ Show layers information """
    layer = {}
    layer_keys = {}
    num = len(o['modules']) if o['modules'] else 0

    for i in xrange(num):
        # Get _obj and keys from torchfile
        layer[i] = o['modules'][i]._obj
        layer_keys[i] = o['modules'][i]._obj.keys()

        # Get information from _obj
        layer_name = o['modules'][i]._typename
        bias_key = 'gradBias'.encode('ASCII')
        weight_key = 'gradWeight'.encode('ASCII')

        if layer_name.find('ConcatTable'.encode('ASCII')) != -1:
            print(i, "Final conv8 layers")

            # Layer conv_81 - objects
            print(o['modules'][i]['modules'][0]._typename)
            print("Bias", o['modules'][i]['modules'][0]['bias'].shape,\
                  "\tWeights", o['modules'][i]['modules'][0]['weight'].shape)

            # Layer conv_82 - places
            print(o['modules'][i]['modules'][1]._typename)
            print("Bias", o['modules'][i]['modules'][1]['bias'].shape,\
                  "\tWeights", o['modules'][i]['modules'][1]['weight'].shape)

            """
            np.array(o['modules'][i]['modules'][0]['bias']).
                tofile('conv81_bs.npy')
            np.array(o['modules'][i]['modules'][0]['weight']).
                tofile('conv81_ws.npy')

            np.array(o['modules'][i]['modules'][1]['bias']).
                tofile('conv82_bs.npy')
            np.array(o['modules'][i]['modules'][1]['weight']).
                tofile('conv82_ws.npy')
            """

        if bias_key in list(layer_keys[i]) or weight_key in list(layer_keys[i]):
            if layer_name.find('Convolution'.encode('ASCII')) != -1 or\
               layer_name.find('Batch'.encode('ASCII')) != -1:
                print(i, layer_name)
                print("Bias", layer[i][bias_key].shape,\
                      "\tWeights", layer[i][weight_key].shape)
                """
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


if __name__ == '__main__':
    t7_file = '../../soundnet_models_public/soundnet8_final.t7'
    o = torchfile.load(t7_file)
    save_layer_params(o)
