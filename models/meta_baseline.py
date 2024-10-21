"""
This file is borrowed with many thanks from [Few-Shot Meta-Baseline](https://github.com/yinboc/few-shot-meta-baseline),
by Yinbo Chen. It was copied on 2021-12-17. The license for this file can be found at ./few-shot-meta-baseline-LICENSE.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

import utils
from models.registry import make, register


@register("meta-baseline")
class MetaBaseline(nn.Module):

    def __init__(self, input_shape, encoder, encoder_args=None, method="cos", temp=10., temp_learnable=True):
        super().__init__()
        if encoder_args is None:
            encoder_args = {}
        self.encoder, _ = make(encoder, input_shape, **encoder_args)
        self.method = method
        # TODO: something seems not right about the code that converts method to metric.
        if method not in ("cos", "sqr"):
            raise RuntimeError(f'Invalid similarity method: "{method}"')

        if temp_learnable:
            self.temp = nn.Parameter(torch.tensor(temp))
        else:
            self.temp = temp

    def forward(self, x_shot, x_query):
        shot_shape = x_shot.shape[:-3]
        query_shape = x_query.shape[:-3]
        img_shape = x_shot.shape[-3:]

        x_shot = x_shot.view(-1, *img_shape)
        x_query = x_query.view(-1, *img_shape)
        x_tot = self.encoder(torch.cat([x_shot, x_query], dim=0))
        x_shot, x_query = x_tot[:len(x_shot)], x_tot[-len(x_query):]
        x_shot = x_shot.view(*shot_shape, -1)
        x_query = x_query.view(*query_shape, -1)

        if self.method == "cos":
            x_shot = x_shot.mean(dim=-2)
            x_shot = F.normalize(x_shot, dim=-1)
            x_query = F.normalize(x_query, dim=-1)
            metric = "dot"
        elif self.method == "sqr":
            x_shot = x_shot.mean(dim=-2)
            metric = "sqr"

        logits = utils.compute_logits(x_query, x_shot, metric=metric, temp=self.temp)
        return logits
