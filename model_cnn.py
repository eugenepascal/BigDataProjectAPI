from torch.autograd import Variable
import torchaudio
import torch
import torch.nn as nn
import numpy as np
from fastapi import UploadFile

valid_sentences = ['deux', 'non', 'oui', 'quatre', 'trois', 'un']

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        conv_layers = []

        # First Convolution Block with Relu and Batch Norm. Use Kaiming Initialization
        self.conv1 = nn.Conv2d(1, 8, kernel_size=(5, 5), stride=(2, 2), padding=(2, 2))
        self.relu1 = nn.ReLU()
        self.bn1 = nn.BatchNorm2d(8)
        nn.init.kaiming_normal_(self.conv1.weight, a=0.1)
        self.conv1.bias.data.zero_()
        conv_layers += [self.conv1, self.relu1, self.bn1]

        # Second Convolution Block
        self.conv2 = nn.Conv2d(8, 16, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.relu2 = nn.ReLU()
        self.bn2 = nn.BatchNorm2d(16)
        nn.init.kaiming_normal_(self.conv2.weight, a=0.1)
        self.conv2.bias.data.zero_()
        conv_layers += [self.conv2, self.relu2, self.bn2]

        # Second Convolution Block
        self.conv3 = nn.Conv2d(16, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.relu3 = nn.ReLU()
        self.bn3 = nn.BatchNorm2d(32)
        nn.init.kaiming_normal_(self.conv3.weight, a=0.1)
        self.conv3.bias.data.zero_()
        conv_layers += [self.conv3, self.relu3, self.bn3]

        # Second Convolution Block
        self.conv4 = nn.Conv2d(32, 64, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1))
        self.relu4 = nn.ReLU()
        self.bn4 = nn.BatchNorm2d(64)
        nn.init.kaiming_normal_(self.conv4.weight, a=0.1)
        self.conv4.bias.data.zero_()
        conv_layers += [self.conv4, self.relu4, self.bn4]

        # Linear Classifier
        self.ap = nn.AdaptiveAvgPool2d(output_size=1)
        self.lin = nn.Linear(in_features=64, out_features=len(valid_sentences))

        # Wrap the Convolutional Blocks
        self.conv = nn.Sequential(*conv_layers)

    def forward(self, x):
        x = self.conv(x)

        # Adaptive pool and flatten for input to linear layer
        x = self.ap(x)
        x = x.view(x.shape[0], -1)

        # Linear layer
        x = self.lin(x)

        # output = nn.functional.log_softmax(x, dim=1)

        return x

async def predict(file: UploadFile):
    # Load the audio file
    blob = await file.read()

    sound, sample_rate = torchaudio.load(io.BytesIO(blob))

    # Padding
    max_length = 48000  # You might need to adjust this value
    if sound.shape[1] < max_length:
        padding = torch.zeros(1, max_length - sound.shape[1])
        sound = torch.cat([sound, padding], dim=1)

    # MelSpectrogram
    specgram = torchaudio.transforms.MelSpectrogram(sample_rate, n_fft=1024, n_mels=64)(sound)
    specgram = torchaudio.transforms.AmplitudeToDB(top_db=80)(specgram)

    # Adding batch dimension
    specgram = specgram.unsqueeze(0)

    model = CNN()
    model.load_state_dict(torch.load('model_state_dict.pt'))
    model.eval()

    # Pass through the model
    outputs = model(specgram)
    _, predicted = torch.max(outputs.data, 1)
    return {"prediction": valid_sentences[predicted.item()]}
