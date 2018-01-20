import numpy as np
import torch
import torch.nn as nn
from torch import bmm, cat, randn, zeros
from torch.autograd import Variable

LEN_WAVEFORM = 961920


class SoundNet(nn.Module):
    def __init__(self, input_shape):
        super(SoundNet, self).__init__()

        self.input_shape = input_shape

        self.conv1      = nn.Conv1d(1, 16, 64, stride=2, padding=32)
        #print("Conv1", self.conv1.weight.shape, self.conv1.bias.shape)
        self.batchnorm1 = nn.BatchNorm1d(16)
        #print("Bn1", self.batchnorm1.weight.shape, self.batchnorm1.bias.shape)
        self.relu1      = nn.ReLU(True)
        self.maxpool1   = nn.MaxPool1d(8, stride=8)

        self.conv2      = nn.Conv1d(16, 32, 32, stride=2, padding=16)
        #print("Conv2", self.conv2.weight.shape, self.conv2.bias.shape)
        self.batchnorm2 = nn.BatchNorm1d(32)
        #print("Bn2", self.batchnorm2.weight.shape, self.batchnorm2.bias.shape)
        self.relu2      = nn.ReLU(True)
        self.maxpool2   = nn.MaxPool1d(8, stride=8)

        self.conv3      = nn.Conv1d(32, 64, 16, stride=2, padding=8)
        #print("Conv3", self.conv3.weight.shape, self.conv3.bias.shape)
        self.batchnorm3 = nn.BatchNorm1d(64)
        #print("Bn3", self.batchnorm3.weight.shape, self.batchnorm3.bias.shape)
        self.relu3      = nn.ReLU(True)

        self.conv4      = nn.Conv1d(64, 128, 8, stride=2, padding=4)
        #print("Conv4", self.conv4.weight.shape, self.conv4.bias.shape)
        self.batchnorm4 = nn.BatchNorm1d(128)
        #print("Bn4", self.batchnorm4.weight.shape, self.batchnorm4.bias.shape)
        self.relu4      = nn.ReLU(True)

        self.conv5      = nn.Conv1d(128, 256, 4, stride=2, padding=2)
        #print("Conv5", self.conv5.weight.shape, self.conv5.bias.shape)
        self.batchnorm5 = nn.BatchNorm1d(256)
        #print("Bn5", self.batchnorm5.weight.shape, self.batchnorm5.bias.shape)
        self.relu5      = nn.ReLU(True)
        self.maxpool5   = nn.MaxPool1d(4, stride=4)

        self.conv6      = nn.Conv1d(256, 512, 4, stride=2, padding=2)
        #print("Conv6", self.conv6.weight.shape, self.conv6.bias.shape)
        self.batchnorm6 = nn.BatchNorm1d(512)
        #print("Bn6", self.batchnorm6.weight.shape, self.batchnorm6.bias.shape)
        self.relu6      = nn.ReLU(True)

        self.conv7      = nn.Conv1d(512, 1024, 4, stride=2, padding=2)
        #print("Conv7", self.conv7.weight.shape, self.conv7.bias.shape)
        self.batchnorm7 = nn.BatchNorm1d(1024)
        #print("Bn7", self.batchnorm7.weight.shape, self.batchnorm7.bias.shape)
        self.relu7      = nn.ReLU(True)

        self.conv8_objs = nn.Conv1d(1024, 1000, 8, stride=2)
        #print("Conv81", self.conv8_objs.weight.shape, self.conv8_objs.bias.shape)
        self.conv8_scns = nn.Conv1d(1024, 401,  8, stride=2)
        #print("Conv82", self.conv8_scns.weight.shape, self.conv8_scns.bias.shape)

    def forward(self, waveform):
        """
            Args:
                waveform (Variable): Raw 20s waveform to be partitioned into 4
                    chunks of equal size. Every chunk is then fed into the
                    network.

            Returns:
                dict: For each 5s chunk, a tuple of probabilities for objects
                    and scenes which will then be used to compute KL divergence
                    with probabilities from VGG and Places365.
        """
        # Partition input of 20s into 5s chunks
        wf1 = waveform.narrow(2, 0                    , LEN_WAVEFORM//4)
        wf2 = waveform.narrow(2, LEN_WAVEFORM // 4    , LEN_WAVEFORM//4)
        wf3 = waveform.narrow(2, LEN_WAVEFORM // 2    , LEN_WAVEFORM//4)
        wf4 = waveform.narrow(2, 3 * LEN_WAVEFORM // 4, LEN_WAVEFORM//4)

        if torch.cuda.is_available():
            wf1.cuda()
            wf2.cuda()
            wf3.cuda()
            wf4.cuda()

        result = { 'ps1' : None, 'ps2' : None, 'ps3' : None, 'ps4' : None }
        wfs = [wf1, wf2, wf3, wf4]
        for i in range(4):
            wf = wfs[i]

            out = self.conv1(wf)
            out = self.batchnorm1(out)
            out = self.relu1(out)
            out = self.maxpool1(out)

            out = self.conv2(out)
            out = self.batchnorm2(out)
            out = self.relu2(out)
            out = self.maxpool2(out)

            out = self.conv3(out)
            out = self.batchnorm3(out)
            out = self.relu3(out)

            out = self.conv4(out)
            out = self.batchnorm4(out)
            out = self.relu4(out)

            out = self.conv5(out)
            out = self.batchnorm5(out)
            out = self.relu5(out)
            out = self.maxpool5(out)

            out = self.conv6(out)
            out = self.batchnorm6(out)
            out = self.relu6(out)

            out = self.conv7(out)
            out = self.batchnorm7(out)
            out = self.relu7(out)

            p_objs = self.conv8_objs(out)
            p_scns = self.conv8_scns(out)

            result['ps' + str(i+1)] = (nn.Softmax(dim=1)(p_objs),
                                       nn.Softmax(dim=1)(p_scns))

        return result

    def load_weights(self):
        bn1_bs = np.fromfile('bn1_bs.npy', dtype=np.float32)
        self.batchnorm1.bias = torch.nn.Parameter(torch.from_numpy(bn1_bs))
        bn1_ws = np.fromfile('bn1_ws.npy', dtype=np.float32)
        self.batchnorm1.weight = torch.nn.Parameter(torch.from_numpy(bn1_ws))
        bn2_bs = np.fromfile('bn2_bs.npy', dtype=np.float32)
        self.batchnorm2.bias = torch.nn.Parameter(torch.from_numpy(bn2_bs))
        bn2_ws = np.fromfile('bn2_ws.npy', dtype=np.float32)
        self.batchnorm2.weight = torch.nn.Parameter(torch.from_numpy(bn2_ws))
        bn3_bs = np.fromfile('bn3_bs.npy', dtype=np.float32)
        self.batchnorm3.bias = torch.nn.Parameter(torch.from_numpy(bn3_bs))
        bn3_ws = np.fromfile('bn3_ws.npy', dtype=np.float32)
        self.batchnorm3.weight = torch.nn.Parameter(torch.from_numpy(bn3_ws))
        bn4_bs = np.fromfile('bn4_bs.npy', dtype=np.float32)
        self.batchnorm4.bias = torch.nn.Parameter(torch.from_numpy(bn4_bs))
        bn4_ws = np.fromfile('bn4_ws.npy', dtype=np.float32)
        self.batchnorm4.weight = torch.nn.Parameter(torch.from_numpy(bn4_ws))
        bn5_bs = np.fromfile('bn5_bs.npy', dtype=np.float32)
        self.batchnorm5.bias = torch.nn.Parameter(torch.from_numpy(bn5_bs))
        bn5_ws = np.fromfile('bn5_ws.npy', dtype=np.float32)
        self.batchnorm5.weight = torch.nn.Parameter(torch.from_numpy(bn5_ws))
        bn6_bs = np.fromfile('bn6_bs.npy', dtype=np.float32)
        self.batchnorm6.bias = torch.nn.Parameter(torch.from_numpy(bn6_bs))
        bn6_ws = np.fromfile('bn6_ws.npy', dtype=np.float32)
        self.batchnorm6.weight = torch.nn.Parameter(torch.from_numpy(bn6_ws))
        bn7_bs = np.fromfile('bn7_bs.npy', dtype=np.float32)
        self.batchnorm7.bias = torch.nn.Parameter(torch.from_numpy(bn7_bs))
        bn7_ws = np.fromfile('bn7_ws.npy', dtype=np.float32)
        self.batchnorm7.weight = torch.nn.Parameter(torch.from_numpy(bn7_ws))

        conv1_bs = np.fromfile('conv1_bs.npy', dtype=np.float32)
        self.conv1.bias = torch.nn.Parameter(torch.from_numpy(conv1_bs))
        conv1_ws = np.fromfile('conv1_ws.npy', dtype=np.float32)
        conv1_ws = np.reshape(conv1_ws, self.conv1.weight.shape)
        self.conv1.weight = torch.nn.Parameter(torch.from_numpy(conv1_ws))

        conv2_bs = np.fromfile('conv2_bs.npy', dtype=np.float32)
        self.conv2.bias = torch.nn.Parameter(torch.from_numpy(conv2_bs))
        conv2_ws = np.fromfile('conv2_ws.npy', dtype=np.float32)
        conv2_ws = np.reshape(conv2_ws, self.conv2.weight.shape)
        self.conv2.weight = torch.nn.Parameter(torch.from_numpy(conv2_ws))

        conv3_bs = np.fromfile('conv3_bs.npy', dtype=np.float32)
        self.conv3.bias = torch.nn.Parameter(torch.from_numpy(conv3_bs))
        conv3_ws = np.fromfile('conv3_ws.npy', dtype=np.float32)
        conv3_ws = np.reshape(conv3_ws, self.conv3.weight.shape)
        self.conv3.weight = torch.nn.Parameter(torch.from_numpy(conv3_ws))

        conv4_bs = np.fromfile('conv4_bs.npy', dtype=np.float32)
        self.conv4.bias = torch.nn.Parameter(torch.from_numpy(conv4_bs))
        conv4_ws = np.fromfile('conv4_ws.npy', dtype=np.float32)
        conv4_ws = np.reshape(conv4_ws, self.conv4.weight.shape)
        self.conv4.weight = torch.nn.Parameter(torch.from_numpy(conv4_ws))

        conv5_bs = np.fromfile('conv5_bs.npy', dtype=np.float32)
        self.conv5.bias = torch.nn.Parameter(torch.from_numpy(conv5_bs))
        conv5_ws = np.fromfile('conv5_ws.npy', dtype=np.float32)
        conv5_ws = np.reshape(conv5_ws, self.conv5.weight.shape)
        self.conv5.weight = torch.nn.Parameter(torch.from_numpy(conv5_ws))

        conv6_bs = np.fromfile('conv6_bs.npy', dtype=np.float32)
        self.conv6.bias = torch.nn.Parameter(torch.from_numpy(conv6_bs))
        conv6_ws = np.fromfile('conv6_ws.npy', dtype=np.float32)
        conv6_ws = np.reshape(conv6_ws, self.conv6.weight.shape)
        self.conv6.weight = torch.nn.Parameter(torch.from_numpy(conv6_ws))

        conv7_bs = np.fromfile('conv7_bs.npy', dtype=np.float32)
        self.conv7.bias = torch.nn.Parameter(torch.from_numpy(conv7_bs))
        conv7_ws = np.fromfile('conv7_ws.npy', dtype=np.float32)
        conv7_ws = np.reshape(conv7_ws, self.conv7.weight.shape)
        self.conv7.weight = torch.nn.Parameter(torch.from_numpy(conv7_ws))

        conv81_bs = np.fromfile('conv81_bs.npy', dtype=np.float32)
        self.conv8_objs.bias = torch.nn.Parameter(torch.from_numpy(conv81_bs))
        conv81_ws = np.fromfile('conv81_ws.npy', dtype=np.float32)
        conv81_ws = np.reshape(conv81_ws, self.conv8_objs.weight.shape)
        self.conv8_objs.weight = torch.nn.Parameter(torch.from_numpy(conv81_ws))

        conv82_bs = np.fromfile('conv82_bs.npy', dtype=np.float32)
        self.conv8_scns.bias = torch.nn.Parameter(torch.from_numpy(conv82_bs))
        conv82_ws = np.fromfile('conv82_ws.npy', dtype=np.float32)
        conv82_ws = np.reshape(conv82_ws, self.conv8_scns.weight.shape)
        self.conv8_scns.weight = torch.nn.Parameter(torch.from_numpy(conv82_ws))


if __name__ == '__main__':
    model = SoundNet(LEN_WAVEFORM // 4)
    model.load_weights()

    print(model)
    waveform = Variable(randn(32, 1, LEN_WAVEFORM))
    print(model.forward(waveform))

