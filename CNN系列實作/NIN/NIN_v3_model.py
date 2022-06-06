import torch
import torch.nn as nn

class NIN_v3(nn.Module):
    def __init__(self, pooling, num_classes):
        super(NIN_v3, self).__init__()

        pool2d = None
        if pooling == 'max':
            pool2d = nn.MaxPool2d((3, 3),(2, 2),(0, 0),ceil_mode=True)
        elif pooling == 'avg':
            pool2d = nn.AvgPool2d((3, 3),(2, 2),(0, 0),ceil_mode=True)

        self.features = nn.Sequential(
            nn.Conv2d(3,96,(11, 11),(4, 4)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(96,96,(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(96,96,(1, 1)),
	    nn.ReLU(inplace=True),
            pool2d,
	    nn.Conv2d(96,256,(5, 5),(1, 1),(2, 2)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(256,256,(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(256,256,(1, 1)),
	    nn.ReLU(inplace=True),
            pool2d,
	    nn.Conv2d(256,384,(3, 3),(1, 1),(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(384,384,(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(384,384,(1, 1)),
	    nn.ReLU(inplace=True),
            pool2d,
	    nn.Dropout(0.5),
	    nn.Conv2d(384,1024,(3, 3),(1, 1),(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(1024,1024,(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.Conv2d(1024,num_classes,(1, 1)),
	    nn.ReLU(inplace=True),
	    nn.AvgPool2d((6, 6),(1, 1),(0, 0),ceil_mode=True),
	    nn.Softmax(),
        nn.Flatten()
        )
        
    def forward(self,x):
        return self.features(x)
    
    # 模擬圖片輸入解析度
    def test_output_shape(self):
        test_img = torch.rand(size=(1, 3, 224, 224), dtype=torch.float32)
        for layer in self.features:
            test_img = layer(test_img)
            print(layer.__class__.__name__, 'output shape: \t', test_img.shape)

"""
nin_dict = {
'C': ['conv1', 'cccp1', 'cccp2', 'conv2', 'cccp3', 'cccp4', 'conv3', 'cccp5', 'cccp6', 'conv4-1024', 'cccp7-1024', 'cccp8-1024'], 
'R': ['relu0', 'relu1', 'relu2', 'relu3', 'relu5', 'relu6', 'relu7', 'relu8', 'relu9', 'relu10', 'relu11', 'relu12'],
'P': ['pool1', 'pool2', 'pool3', 'pool4'],
'D': ['drop'],
}


def SetupNIN(pooling):
    # Network In Network model 
    model = NIN(pooling)
    return model, nin_dict
"""


# 模擬圖片輸入解析度
#pooling = 'max'
#nin = NIN_v3(pooling=pooling, num_classes=5)
#nin.test_output_shape()

    
# 載入model框架，讀取權重檔.pth: https://github.com/ProGamerGov/pytorch-nin
#pooling = 'max'
#cnn, layerList = SetupNIN(pooling)
#cnn.load_state_dict(torch.load('nin_imagenet2.pth')) 
#print(cnn)

