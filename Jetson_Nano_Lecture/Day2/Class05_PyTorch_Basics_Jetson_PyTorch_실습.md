# Class 05: PyTorch Basics 및 Jetson PyTorch 실습

## 1. PyTorch 개요

### 1.1 PyTorch 정의

PyTorch는 Meta AI(구 Facebook AI Research)에서 개발한 딥러닝 프레임워크입니다.

```
PyTorch 특징:
┌─────────────────────────────────────┐
│  - Python-first 설계               │
│  - 동적 계산 그래프 (Dynamic Graph)│
│  - 직관적인 코드                    │
│  - 자동 미분 (Autograd) 지원        │
│  - GPU 가속 지원                   │
└─────────────────────────────────────┘
```

### 1.2 TensorFlow vs PyTorch

| 구분 | TensorFlow | PyTorch |
|------|------------|---------|
| 그래프 | 정적/동적 | 동적 |
| 디버깅 | 어려움 | 용이 |
| 프로덕션 | 높음 | 중간 |
| 커뮤니티 | 방대 | 빠르게 성장 |

## 2. Jetson용 PyTorch 설치

### 2.1 PyTorch 설치

```bash
# JetPack version 확인
cat /etc/nv_tegra_release

# PyTorch 설치 (JP 4.6.1 기준)
python3 -m pip install --upgrade pip
python3 -m pip install numpy==1.26.1

# PyTorch wheel 다운로드 및 설치
wget https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
# (JP 4.6.1: torch-1.10.0-cp36-cp36m-linux_aarch64.whl)

pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
pip3 install torchvision
```

### 2.2 GPU 확인

```python
import torch

# CUDA 사용 가능 여부
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")

# cuDNN 버전
print(f"cuDNN version: {torch.backends.cudnn.version()}")
```

## 3. PyTorch 기초

### 3.1 Tensor 연산

```python
import torch
import numpy as np

# Tensor 생성
x = torch.randn(3, 3)  # 정규분포 랜덤
y = torch.zeros(3, 3)  # 영 행렬
z = torch.ones(3, 3)    # 일 행렬

# NumPy 변환
np_array = np.array([[1, 2], [3, 4]])
torch_tensor = torch.from_numpy(np_array)

# GPU로 이동
if torch.cuda.is_available():
    x_gpu = x.cuda()
    y_gpu = y.cuda()

# 연산
a = torch.randn(2, 3)
b = torch.randn(2, 3)
c = a + b  # 덧셈
d = torch.matmul(a, b.t())  # 행렬 곱셈
```

### 3.2 자동 미분 (Autograd)

```python
# requires_grad=True로.grad 활성화
x = torch.randn(3, requires_grad=True)
y = x * 2
z = y.mean()

# 역전파
z.backward()

# Gradient 확인
print(x.grad)
```

### 3.3 nn.Module

```python
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.relu = nn.ReLU()
        self.fc = nn.Linear(16*32*32, 10)
    
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

model = MyModel()
print(model)
```

### 3.4 DataLoader

```python
from torch.utils.data import Dataset, DataLoader

class CustomDataset(Dataset):
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

dataset = CustomDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for batch_data, batch_labels in loader:
    # 학습 코드
    pass
```

## 4. MNIST MLP/CNN 학습

### 4.1 MLP 모델

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# 데이터 로드
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=True, download=True, transform=transform),
    batch_size=64, shuffle=True
)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=False, transform=transform),
    batch_size=1000
)

# MLP 모델
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 10)
        self.dropout = nn.Dropout(0.2)
    
    def forward(self, x):
        x = x.view(-1, 784)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

model = MLP()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습
for epoch in range(5):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
    
    # 테스트
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in test_loader:
            output = model(data)
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
    
    print(f'Epoch {epoch+1}: Accuracy {100.*correct/total:.2f}%')
```

### 4.2 CNN 모델

```python
class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64*7*7, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# 모델 학습 (MLP와 동일한 방식)
```

## 5. Object Detection 파이프라인

### 5.1 PyTorch 모델 로드

```python
# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 모델 정보 확인
print(f"Classes: {model.names}")
print(f"Number of classes: {len(model.names)}")
```

### 5.2 추론 실행

```python
import cv2

# 이미지 추론
img = cv2.imread('test.jpg')
results = model(img)

# 결과 출력
print(results.xyxy[0])  # bounding boxes

# 시각화
results.show()

# 저장
results.save()
```

## 6. Jetson 최적화

### 6.1 FP16 양자화

```python
# FP16 변환
model = model.half()

# 추론
img = torch.randn(1, 3, 640, 640).half().cuda()
output = model(img)
```

### 6.2 TorchScript 변환

```python
# TorchScript로 변환
model.eval()
traced_model = torch.jit.trace(model, torch.randn(1, 3, 640, 640).cuda())
traced_model.save('yolov5s.pt')
```

## 7. 실습 과제

1. PyTorch를 Jetson에 설치하고 GPU를 확인하세요.
2. MNIST 데이터셋으로 MLP와 CNN 모델을 학습시키세요.
3. YOLOv5를 사용하여 이미지 추론을 실행하세요.
4. 모델을 TorchScript로 변환하세요.

## 8. 다음 실습 예고

다음 클래스에서는 Darknet과 YOLOv4 실습을 진행합니다.