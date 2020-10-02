import torch.optim as optim

from medzoo.models.COVIDNet.COVIDNet import CovidNet, CNN
from medzoo.models.DenseVoxelNet.DenseVoxelNet import DenseVoxelNet
from medzoo.models.Densenet3D.Densenet3D import DualPathDenseNet, DualSingleDenseNet, SinglePathDenseNet
from medzoo.models.HighResNet3D.HighResNet3D import HighResNet3D
from medzoo.models.HyperDensenet.HyperDensenet import HyperDenseNet, HyperDenseNet_2Mod
from medzoo.models.ResNet3DMedNet.ResNet3DMedNet import generate_resnet3d
from medzoo.models.ResNet3D_VAE.ResNet3D_VAE import ResNet3dVAE
from medzoo.models.SkipDenseNet3D.SkipDenseNet3D import SkipDenseNet3D
from medzoo.models.Unet2D.Unet2D import Unet
from medzoo.models.Unet3D.Unet3D import UNet3D
from medzoo.models.Vnet.Vnet import VNet, VNetLight
from medzoo.utils.logger import Logger


def create_model(args):
    """

    Args:
        args:

    Returns:

    """
    model_list = ['UNET3D', 'DENSENET1', "UNET2D", 'DENSENET2', 'DENSENET3', 'HYPERDENSENET', "SKIPDENSENET3D",
                  "DENSEVOXELNET", 'VNET', 'VNET2', "RESNET3DVAE", "RESNETMED3D", "COVIDNET1", "COVIDNET2", "CNN",
                  "HIGHRESNET"]

    LOG = Logger(name='model_builder').get_logger()
    model_name = args.model
    assert model_name in model_list
    optimizer_name = args.opt
    lr = args.lr
    in_channels = args.inChannels
    num_classes = args.classes
    weight_decay = 0.0000000001
    LOG.info(f'Building Model . . . . . . . . {model_name}')

    if model_name == 'VNET2':
        model = VNetLight(in_channels=in_channels, elu=False, classes=num_classes)
    elif model_name == 'VNET':
        model = VNet(in_channels=in_channels, elu=False, classes=num_classes)
    elif model_name == 'UNET3D':
        model = UNet3D(in_channels=in_channels, n_classes=num_classes, base_n_filter=8)
    elif model_name == 'DENSENET1':
        model = SinglePathDenseNet(in_channels=in_channels, classes=num_classes)
    elif model_name == 'DENSENET2':
        model = DualPathDenseNet(in_channels=in_channels, classes=num_classes)
    elif model_name == 'DENSENET3':
        model = DualSingleDenseNet(in_channels=in_channels, drop_rate=0.1, classes=num_classes)
    elif model_name == "UNET2D":
        model = Unet(in_channels, num_classes)
    elif model_name == "RESNET3DVAE":
        model = ResNet3dVAE(in_channels=in_channels, classes=num_classes, dim=args.dim)
    elif model_name == "SKIPDENSENET3D":
        model = SkipDenseNet3D(growth_rate=16, num_init_features=32, drop_rate=0.1, classes=num_classes)
    elif model_name == "COVIDNET1":
        model = CovidNet('small', num_classes)
    elif model_name == "COVIDNET2":
        model = CovidNet('large', num_classes)
    elif model_name == "CNN":
        model = CNN(num_classes, 'resnet18')
    elif model_name == "HYPERDENSENET":
        if in_channels == 2:
            model = HyperDenseNet_2Mod(classes=num_classes)
        elif in_channels == 3:
            model = HyperDenseNet(classes=num_classes)
        else:
            raise NotImplementedError
    elif model_name == "DENSEVOXELNET":
        model = DenseVoxelNet(in_channels=in_channels, classes=num_classes)
    elif model_name == "HIGHRESNET":
        model = HighResNet3D(in_channels=in_channels, classes=num_classes)
    elif model_name == "RESNETMED3D":
        depth = 18
        model = generate_resnet3d(in_channels=in_channels, classes=num_classes, model_depth=depth)

    LOG.info(f'{model_name} Number of params: {sum([p.data.nelement() for p in model.parameters()])}')

    if optimizer_name == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=lr, momentum=0.5, weight_decay=weight_decay)
    elif optimizer_name == 'adam':
        optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    elif optimizer_name == 'rmsprop':
        optimizer = optim.RMSprop(model.parameters(), lr=lr, weight_decay=weight_decay)

    return model, optimizer
