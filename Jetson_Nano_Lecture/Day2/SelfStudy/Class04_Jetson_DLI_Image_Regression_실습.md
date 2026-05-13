# Class 04: Jetson DLI Image Regression 실습

## 1. Image Regression 개요

### 1.1 정의

Image Regression은 이미지를 기반으로 연속적인 값을 예측하는 작업입니다. 분류가 이산적인 클래스 레이블을 출력하는 반면, 회귀는 연속적인数值를 출력합니다.

### 1.2 응용 분야

- **Age Estimation**: 이미지에서 인물 나이 예측
- **Pose Estimation**: 신체 관절 위치 좌표 예측
- **Face Landmark Detection**: 얼굴 특징점 좌표 예측
- **Object Localization**: 객체 중심 좌표 및 크기 예측
- **Image Quality Assessment**: 이미지 품질 점수 예측

### 1.3 분류 vs 회귀

```
Classification (분류):
  Input → [Class A, Class B, Class C]
  출력: 이산적 레이블

Regression (회귀):
  Input → [값: 0.0 ~ 1.0]
  출력: 연속적 값
```

## 2. 회귀 문제 분석

### 2.1 손실 함수

**MSE (Mean Squared Error):**
```python
criterion = nn.MSELoss()
loss = criterion(predictions, targets)
```

**MAE (Mean Absolute Error):**
```python
criterion = nn.L1Loss()
loss = criterion(predictions, targets)
```

**Smooth L1 Loss:**
```python
criterion = nn.SmoothL1Loss()
loss = criterion(predictions, targets)
```

### 2.2 평가 지표

- **RMSE** (Root Mean Squared Error): √MSE
- **MAE** (Mean Absolute Error): 평균 절대 오차
- **R² Score**: 결정 계수

## 3. 실습: Face Landmark Detection

### 3.1 데이터셋 준비

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os
```

### 3.2 커스텀 데이터셋 클래스

```python
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
```

### 3.3 데이터 전처리

```python
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])
```

### 3.4 CNN 기반 회귀 모델

```python
class LandmarkCNN(nn.Module):
    def __init__(self, num_landmarks=10):
        super(LandmarkCNN, self).__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.conv5 = nn.Conv2d(128, 256, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

        # Fully connected layers
        self.fc1 = nn.Linear(256 * 7 * 7, 512)
        self.fc2 = nn.Linear(512, num_landmarks * 2)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = self.pool(self.relu(self.conv4(x)))
        x = self.pool(self.relu(self.conv5(x)))

        x = x.view(x.size(0), -1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)

        return x
```

### 3.5 모델 초기화

```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

num_landmarks = 5  # 예: 눈, 코, 입 위치
model = LandmarkCNN(num_landmarks=num_landmarks)
model = model.to(device)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
```

### 3.6 학습 루프

```python
num_epochs = 50
batch_size = 16

# 데이터로더 생성 (실제 데이터 경로로 변경)
# train_dataset = FaceLandmarkDataset('path/to/images', 'path/to/labels.csv', transform)
# train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

for epoch in range(num_epochs):
    running_loss = 0.0

    for batch_idx, (images, landmarks) in enumerate(train_loader):
        images = images.to(device)
        landmarks = landmarks.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, landmarks)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.6f}')

print('Training completed!')
```

## 4. 실습: Age Estimation

### 4.1 데이터 준비

```python
# UTKFace 데이터셋 예시
# 각 이미지 파일명: [age]_[gender]_[race]_[datetime].jpg

class AgeDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        self.image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = os.path.join(self.image_dir, self.image_files[idx])
        image = Image.open(image_path).convert('RGB')

        # 파일명에서 나이 추출
        age = int(self.image_files[idx].split('_')[0])

        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(age, dtype=torch.float32)
```

### 4.2 VGG 기반 회귀 모델

```python
class AgeEstimator(nn.Module):
    def __init__(self):
        super(AgeEstimator, self).__init__()

        # VGG16 기반 특징 추출
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
        )

        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))

        self.regressor = nn.Sequential(
            nn.Linear(256 * 7 * 7, 4096),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(4096, 1024),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(1024, 1)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.regressor(x)
        return x
```

## 5. 결과 시각화

### 5.1 예측 결과 시각화

```python
import matplotlib.pyplot as plt

def visualize_predictions(images, true_landmarks, pred_landmarks, num_samples=4):
    fig, axes = plt.subplots(1, num_samples, figsize=(15, 3))

    for i in range(num_samples):
        img = images[i].cpu().numpy().transpose(1, 2, 0)
        img = (img - img.min()) / (img.max() - img.min())

        axes[i].imshow(img)
        axes[i].axis('off')

        # 실제 landmark 표시 (녹색)
        for j in range(0, len(true_landmarks[i]), 2):
            x = int(true_landmarks[i][j].item() * 224)
            y = int(true_landmarks[i][j+1].item() * 224)
            axes[i].plot(x, y, 'go', markersize=5)

        # 예측 landmark 표시 (빨강)
        for j in range(0, len(pred_landmarks[i]), 2):
            x = int(pred_landmarks[i][j].item() * 224)
            y = int(pred_landmarks[i][j+1].item() * 224)
            axes[i].plot(x, y, 'ro', markersize=5)

    plt.tight_layout()
    plt.show()
```

### 5.2 손실 그래프

```python
def plot_training_history(train_losses):
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses)
    plt.title('Training Loss over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.grid(True)
    plt.show()
```

## 6. 모델 평가

### 6.1 회귀 평가 지표

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

    # R² Score 계산
    ss_res = np.sum((targets - predictions) ** 2)
    ss_tot = np.sum((targets - np.mean(targets)) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    print(f'RMSE: {rmse:.4f}')
    print(f'MAE: {mae:.4f}')
    print(f'R² Score: {r2:.4f}')

    return rmse, mae, r2
```

## 7. Jetson 최적화

### 7.1 모델 변환

```python
# Torchscript 변환
model.eval()
example_input = torch.randn(1, 3, 224, 224).to(device)
traced_model = torch.jit.trace(model, example_input)
traced_model.save('age_estimator_traced.pt')
```

### 7.2 INT8 양자화

```python
# TensorRT INT8 양자화 (Jetson에서)
#trted_model = torch2trt(model, [example_input], fp16_mode=True)
```

## 8. 실습 과제

1. Face Landmark Detection 모델을 학습시키세요.
2. Age Estimation 모델을 학습시키고 RMSE를 계산하세요.
3. 예측 결과를 시각화하세요.
4. 모델을 Torchscript로 변환하세요.

## 9. 다음 실습 예고

다음 클래스에서는 TensorFlow 기초 및 CUDA 지원 TensorFlow 실습을 진행합니다.