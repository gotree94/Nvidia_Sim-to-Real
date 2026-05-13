# Class 04: Jetson DLI - Image Regression 실습

## 1. Image Regression 개요

### 1.1 정의

Image Regression은 이미지를 기반으로 연속적인 값을 예측하는 작업입니다.

```
Classification vs Regression:
┌─────────────────────────────────────┐
│  Classification                     │
│  Input → [Class A, Class B, Class C]│
│  출력: 이산적 레이블                 │
├─────────────────────────────────────┤
│  Regression                         │
│  Input → [값: 0.0 ~ 1.0]            │
│  출력: 연속적 값                    │
└─────────────────────────────────────┘
```

### 1.2 응용 분야

- Face Landmark Detection (얼굴 특징점 좌표)
- Age Estimation (나이 예측)
- Pose Estimation (자세 추정)
- Object Localization (객체 위치)

### 1.3 손실 함수

```python
# MSE (Mean Squared Error)
criterion = nn.MSELoss()
loss = criterion(predictions, targets)

# MAE (Mean Absolute Error)
criterion = nn.L1Loss()
loss = criterion(predictions, targets)

# Smooth L1 Loss
criterion = nn.SmoothL1Loss()
loss = criterion(predictions, targets)
```

## 2. Face Landmark Detection 실습

### 2.1 데이터셋 준비

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os

class FaceLandmarkDataset(Dataset):
    def __init__(self, image_dir, label_file, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.data = self._load_data(label_file)
    
    def _load_data(self, label_file):
        data = []
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                image_name = parts[0]
                landmarks = [float(x) for x in parts[1:]]
                data.append((image_name, landmarks))
        return data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        image_name, landmarks = self.data[idx]
        image = Image.open(os.path.join(self.image_dir, image_name)).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        landmarks = torch.tensor(landmarks, dtype=torch.float32)
        return image, landmarks

# 데이터 전처리
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])
```

### 2.2 회귀 모델 정의

```python
class LandmarkCNN(nn.Module):
    def __init__(self, num_landmarks=3):  # nose, left_eye, right_eye
        super().__init__()
        
        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        
        # Fully connected layers
        self.fc1 = nn.Linear(256 * 28 * 28, 512)
        self.fc2 = nn.Linear(512, num_landmarks * 2)  # x, y 좌표
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        
        x = x.view(x.size(0), -1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        
        return x
```

### 2.3 학습 실행

```python
# 모델 초기화
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = LandmarkCNN(num_landmarks=3).to(device)

# 손실 함수 및 옵티마이저
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습 루프
num_epochs = 20
batch_size = 16

for epoch in range(num_epochs):
    running_loss = 0.0
    
    for images, landmarks in train_loader:
        images = images.to(device)
        landmarks = landmarks.to(device)
        
        optimizer.zero_grad()
        outputs = model(images)
        
        # 출력 포맷 조정 (x, y 좌표 쌍)
        loss = criterion(outputs, landmarks)
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.6f}')

print('Training completed!')
```

## 3. 결과 시각화

### 3.1 예측 결과 시각화

```python
import matplotlib.pyplot as plt

def visualize_predictions(images, true_landmarks, pred_landmarks, num_samples=4):
    fig, axes = plt.subplots(1, num_samples, figsize=(15, 3))
    
    for i in range(num_samples):
        img = images[i].cpu().numpy().transpose(1, 2, 0)
        img = (img - img.min()) / (img.max() - img.min())
        
        axes[i].imshow(img)
        axes[i].axis('off')
        
        # 실제 landmark (녹색)
        for j in range(0, len(true_landmarks[i]), 2):
            x = int(true_landmarks[i][j].item() * 224)
            y = int(true_landmarks[i][j+1].item() * 224)
            axes[i].plot(x, y, 'go', markersize=5)
        
        # 예측 landmark (빨강)
        for j in range(0, len(pred_landmarks[i]), 2):
            x = int(pred_landmarks[i][j].item() * 224)
            y = int(pred_landmarks[i][j+1].item() * 224)
            axes[i].plot(x, y, 'ro', markersize=5)
    
    plt.tight_layout()
    plt.show()
```

## 4. Number Trace Project 실습

### 4.1 데이터 수집

```python
# TASK 및 CATEGORIES 설정
TASK = 'number'
CATEGORIES = ['1', '4']

# 데이터 수집 UI 활용
# - ClickableImageWidget 사용
# - 마우스로 클릭하여 좌표 수집
# - 각 숫자당 20~40장 수집
```

### 4.2 좌표 회귀 학습

```python
# 회귀 모델의 출력 차원
output_dim = 2 * len(CATEGORIES)  # 각 카테고리당 x, y 좌표

model = torchvision.models.resnet18(pretrained=True)
model.fc = nn.Linear(512, output_dim)

# 손실 함수 (MSE)
criterion = nn.MSELoss()

# 학습 실행
# ... (Classification과 유사한 학습 루프)
```

## 5. 모델 평가

### 5.1 평가 지표

```python
def evaluate_model(model, test_loader, device):
    model.eval()
    all_preds = []
    all_targets = []
    
    with torch.no_grad():
        for images, targets in test_loader:
            images = images.to(device)
            outputs = model(images)
            all_preds.extend(outputs.cpu().numpy())
            all_targets.extend(targets.numpy())
    
    # RMSE 계산
    predictions = np.array(all_preds)
    targets = np.array(all_targets)
    rmse = np.sqrt(np.mean((predictions - targets) ** 2))
    
    # MAE 계산
    mae = np.mean(np.abs(predictions - targets))
    
    print(f'RMSE: {rmse:.4f}')
    print(f'MAE: {mae:.4f}')
    
    return rmse, mae
```

## 6. Jetson 최적화

### 6.1 TorchScript 변환

```python
# 모델 변환
model.eval()
example_input = torch.randn(1, 3, 224, 224).to(device)
traced_model = torch.jit.trace(model, example_input)
traced_model.save('landmark_model_traced.pt')
```

### 6.2 INT8 양자화

```python
# TensorRT INT8 양자화 (Jetson에서)
# trtexec --onnx=model.onnx --saveEngine=model.trt --int8
```

## 7. 실습 과제

1. Face Landmark Detection 모델을 학습시키세요.
2. Number Trace Project를 수행하세요.
3. 예측 결과를 시각화하세요.
4. 모델을 TorchScript로 변환하세요.

## 8. 다음 실습 예고

다음 클래스에서는 PyTorch와 YOLOv5 실습을 진행합니다.