import time
import cv2
import torch
import torch.backends.cudnn as cudnn
import numpy as np

model_path = "./yolov5s.pt"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
half = device.type != 'cpu'  # CUDA로 float16(half) 사용 
print('device:', device)

model = torch.load(model_path, map_location=device)
print('-' * 100)

# 모델 파일 딕셔너리 키 정보 출력 
print("model's keys:")
print(model.keys())
print('-' * 100)

# 모델 epoch 정보 출력 (['epoch'] 키의 값)
model_epoch = model["epoch"] 
print("model's epoch:")
print(model_epoch)
print('-' * 100)

# 모델 best_fitness 정보 출력 (['best_fitness'] 키의 값)
model_best_fitness = model["best_fitness"] 
print("model's best_fitness:")
print(model_best_fitness)
print('-' * 100)

# 모델 optimizer 정보 출력 (['optimizer'] 키의 값)
model_optimizer = model["optimizer"] 
print("model's optimizer:")
print(model_optimizer)
print('-' * 100)

# 모델 구성 출력 (['model'] 키의 값)
model_layer = model["model"].float()
if half:    
    model_layer.half() # to FP16
print("model's architecture:")
print(model_layer)
print('-' * 100)

# 모델의 Class names 출력  
model_class_name = model_layer.names 
print("model class names:")
print(model_class_name)
print('-' * 100)

# 모델의 가중치 출력  
model_weight = model_layer.state_dict() 
print("lenght of model's weight :", len(model_weight))
print('-' * 100)
print("model's weight :")
number = 0
for k, v in model_weight.items():
    number += 1
    print(f"{number} = {k}: {v.shape}")     # 모델 가중치 shape 출력
    #print(f"{v}")                          # 모델 가중치 값 출력


print('-' * 100)
# 더미 입력 (1 x 3 x 640 x 640)
dummy_input = torch.randn(1, 3, 640, 640)
dummy_input = dummy_input.to(device)
dummy_input = dummy_input.type_as(next(model_layer.parameters()))

# 추론
with torch.no_grad():
    output = model_layer(dummy_input)

# 출력 확인
print("Model input shape :", dummy_input.shape)
print("Model output shape:", output[0].shape)
#print("Output type :", type(output))
#print("Model output shape:", output[0].shape if isinstance(output, tuple) else output.shape)
