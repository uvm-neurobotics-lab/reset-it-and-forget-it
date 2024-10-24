"""
VGG style models, imported from PyTorch.
"""
import torch
import torch.nn as nn
import torchvision.models.vgg as torchvgg

from models.registry import register


class VGGEncoder(nn.Module):

    def __init__(self, vgg):
        super().__init__()
        self.features = vgg.features
        self.avgpool = vgg.avgpool

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        return x


@register('vgg16')
def vgg16(pretrained=False, progress=True, **kwargs):
    """
    VGG-16 model from Torchvision.

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet-1K.
        progress (bool): If True, displays a progress bar of the download to stderr.
        **kwargs: parameters passed to the ``torchvision.models.vgg.VGG`` base class. Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/vgg.py>`_ for more details about this class.
    """
    return torchvgg.vgg16(pretrained=pretrained, progress=progress, **kwargs)


@register('vgg16_bn')
def vgg16_bn(pretrained=False, progress=True, **kwargs):
    """
    VGG-16-BN model from Torchvision.

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet-1K.
        progress (bool): If True, displays a progress bar of the download to stderr.
        **kwargs: parameters passed to the ``torchvision.models.vgg.VGG`` base class. Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/vgg.py>`_ for more details about this class.
    """
    return torchvgg.vgg16_bn(pretrained=pretrained, progress=progress, **kwargs)


@register('vgg16_encoder')
def vgg16_encoder(pretrained=False, progress=True, **kwargs):
    """
    VGG-16 model from Torchvision, but only the encoder part (before the linear classifier).

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet-1K.
        progress (bool): If True, displays a progress bar of the download to stderr.
        **kwargs: parameters passed to the ``torchvision.models.vgg.VGG`` base class. Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/vgg.py>`_ for more details about this class.
    """
    vgg = torchvgg.vgg16(pretrained=pretrained, progress=progress, **kwargs)
    return VGGEncoder(vgg)


@register('vgg16_bn_encoder')
def vgg16_bn_encoder(pretrained=False, progress=True, **kwargs):
    """
    VGG-16-BN model from Torchvision, but only the encoder part (before the linear classifier).

    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet-1K.
        progress (bool): If True, displays a progress bar of the download to stderr.
        **kwargs: parameters passed to the ``torchvision.models.vgg.VGG`` base class. Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/vgg.py>`_ for more details about this class.
    """
    vgg = torchvgg.vgg16_bn(pretrained=pretrained, progress=progress, **kwargs)
    return VGGEncoder(vgg)
