import torch
import torch.nn as nn
from torchvision import models
from collections import OrderedDict

model_path = 'resnet50_berry_add_1.pth'
state_dict = torch.load(model_path, map_location=torch.device('cuda'))
print(state_dict)
# 读取模型

new_state_dict = OrderedDict()
# for k, v in state_dict.items():
#     if 'model.' in k:
#         new_key = k.replace('model.', '')
#     else:
#         new_key = k
#     new_state_dict[new_key] = v

# torch.save(new_state_dict, "resnet50_berry_add_1.pth")




