import torch
import torch.nn as nn

# takes a sequence of pitches described by location, speed, spin, and other descriptors
class PitchSequenceTransformer(nn.Module):
    def __init__(self, d_model, num_layers, dim_feedforward, nhead, dropout=0.1, features=9, num_classes=16, device='cpu'):
        super(PitchSequenceTransformer, self).__init__()
        self.d_model = d_model
        self.num_layers = num_layers
        self.dim_feedforward = dim_feedforward
        self.nhead = nhead

        self.feature_min = torch.tensor([-10.5433282251965, -5.18366373737265, 33.9, 32.4, 1.214, -0.002, -90.0, 0.1, 23.3], device=device)
        self.feature_max = torch.tensor([12.9529095060724, 14.8862417199696, 105.0, 96.9, 6539.259, 360.001, 269.4, 224889.3, 36.4], device=device)
        # self.embed = nn.Embedding(1024, d_model, device=device)

        transformer_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, dim_feedforward=dim_feedforward, dropout=dropout, batch_first=True, device=device)

        self.transformer = nn.TransformerEncoder(
            transformer_layer,
            num_layers=num_layers
        )
        # Output layer after pooling
        self.cls_token_emb = nn.Parameter(torch.zeros(1, 1, d_model), requires_grad=False)

        # Global average pooling on CLS token
        # self.pool = nn.AdaptiveAvgPool1d(16)
        self.fc = nn.Linear(d_model, num_classes)
        
    def normalize_features(self, features, feature_num=9):
        '''
        Feature: px, Max Value: 12.9529095060724, Min Value: -10.5433282251965
        Feature: pz, Max Value: 14.8862417199696, Min Value: -5.18366373737265
        Feature: start_speed, Max Value: 105.0, Min Value: 33.9
        Feature: end_speed, Max Value: 96.9, Min Value: 32.4
        Feature: spin_rate, Max Value: 6539.259, Min Value: 1.214
        Feature: spin_dir, Max Value: 360.001, Min Value: -0.002
        Feature: break_angle, Max Value: 269.4, Min Value: -90.0
        Feature: break_length, Max Value: 224889.3, Min Value: 0.1
        Feature: break_y, Max Value: 36.4, Min Value: 23.3
        '''
        normalized_features =  (features.long() - self.feature_min) / (self.feature_max - self.feature_min)
        normalized_features = torch.cuda.FloatTensor(normalized_features)
        return normalized_features
    def forward(self, inputs):
        x = self.normalize_features(inputs)
        # embed pitch description data to the size of d_model
        # do this for every pitch in sequence
        # replace one pitch with a mask token
        # use this for regular training
        # take final trained model and convert to strike out generator

        # should consider pitchers arsenal
        return x
