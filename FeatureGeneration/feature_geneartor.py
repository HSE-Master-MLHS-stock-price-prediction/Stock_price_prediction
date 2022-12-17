import numpy as np
import torch 
from torch import nn

class VAEModel(nn.Module):
    
    def __init__(self, window_size):
        super(VAEModel, self).__init__()
        self.window_size = window_size
        self.encoder = nn.Sequential(nn.Linear(self.window_size, 128), 
                                    nn.ReLU(), 
                                    nn.Linear(128, 64), 
                                    nn.ReLU())
        self.decoder = nn.Sequential(nn.Linear(64, 128), 
                                    nn.ReLU(), 
                                    nn.Linear(128, self.window_size))
    
    def forward(self, x):
        return self.decoder(self.encoder(x))
    
    def get_embedding(self, x):
        with torch.no_grad():
            return self.encoder(x)
        
class FeaturesGenerator:
    
    def __init__(self):
        
        self.encoder_model = torch.load('Linear_VAE.pytorch')
        for p in self.encoder_model.parameters():
            p.requires_grad = False
        
    def get_ecnoder_decoder_result(self, x):
        input_tens = torch.Tensor([list(x)])
        return self.encoder_model(input_tens)[0].detach().numpy()
    
    def get_encoder_decoder_embedding(self, x):
        input_tens = torch.Tensor([list(x)])
        return self.encoder_model.get_embedding(input_tens)[0].detach().numpy()