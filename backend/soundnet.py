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
        self.batchnorm1 = nn.BatchNorm1d(16)
        self.relu1      = nn.ReLU(True)
        self.maxpool1   = nn.MaxPool1d(8, stride=8)

        self.conv2      = nn.Conv1d(16, 32, 32, stride=2, padding=16)
        self.batchnorm2 = nn.BatchNorm1d(32)
        self.relu2      = nn.ReLU(True)
        self.maxpool2   = nn.MaxPool1d(8, stride=8)

        self.conv3      = nn.Conv1d(32, 64, 16, stride=2, padding=8)
        self.batchnorm3 = nn.BatchNorm1d(64)
        self.relu3      = nn.ReLU(True)

        self.conv4      = nn.Conv1d(64, 128, 8, stride=2, padding=4)
        self.batchnorm4 = nn.BatchNorm1d(128)
        self.relu4      = nn.ReLU(True)

        self.conv5      = nn.Conv1d(128, 256, 4, stride=2, padding=2)
        self.batchnorm5 = nn.BatchNorm1d(256)
        self.relu5      = nn.ReLU(True)
        self.maxpool5   = nn.MaxPool1d(4, stride=4)

        self.conv6      = nn.Conv1d(256, 512, 4, stride=2, padding=2)
        self.batchnorm6 = nn.BatchNorm1d(512)
        self.relu6      = nn.ReLU(True)

        self.conv7      = nn.Conv1d(512, 1024, 4, stride=2, padding=2)
        self.batchnorm7 = nn.BatchNorm1d(1024)
        self.relu7      = nn.ReLU(True)

        self.conv8_objs = nn.Conv1d(1024, 1000, 8, stride=2)
        self.conv8_scns = nn.Conv1d(1024, 401,  8, stride=2)

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

            result['ps' + str(i+1)] = (nn.LogSoftmax(dim=1)(p_objs),
                                       nn.LogSoftmax(dim=1)(p_scns))

        return result


if __name__ == '__main__':
    model = SoundNet(LEN_WAVEFORM // 4)
    print(model)
    waveform = Variable(randn(1, 1, LEN_WAVEFORM))
    print(model.forward(waveform=waveform)['ps1'][0])
