# Class 03: Jetson DLI Image Classification 실습

## 1. Image Classification 개요

### 1.1 정의

Image Classification은 이미지를预先 정의된 클래스로 분류하는 작업입니다. 입력된 이미지가 어떤 카테고리에 속하는지를 판단합니다.

### 1.2 분류 유형

- **Binary Classification**: 두 클래스 중 하나 선택
- **Multi-class Classification**: 여러 클래스 중 하나 선택
- **Multi-label Classification**: 여러 클래스 동시 할당

## 2. CNN(Convolutional Neural Network) 기초

### 2.1 CNN 구조

```
Input Image → Convolution → Pooling → Convolution → Pooling →
Flatten → Fully Connected → Output
```

### 2.2 주요 레이어

**Convolutional Layer:**
- 필터를 사용하여 특성 추출
- 파라미터: kernel size, stride, padding

**Pooling Layer:**
- 공간 크기 축소
- Max Pooling, Average Pooling

**Fully Connected Layer:**
- 모든 뉴런이 연결
- 분류 작업 수행

### 2.3 활성화 함수

```python
import torch.nn as nn

# ReLU (Rectified Linear Unit)
nn.ReLU()

# Sigmoid
nn.Sigmoid()

# Softmax (다중 클래스)
nn.Softmax(dim=1)
```

## 3. Jetson DLI 실습: Image Classification

### 3.1 실습 환경 준비

```python
# 필요한 라이브러리 임포트
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
```

### 3.2 데이터셋 준비

```python
# CIFAR-10 데이터셋 다운로드 및 전처리
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

trainset = torchvision.datasets.CIFAR10(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

testset = torchvision.datasets.CIFAR10(
    root='./data',
    train=False,
    download=True,
    transform=transform
)

trainloader = DataLoader(trainset, batch_size=32, shuffle=True)
testloader = DataLoader(testset, batch_size=32, shuffle=False)

# 클래스 정의
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')
```

### 3.3 CNN 모델 정의

```python
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)
        self.fc1 = nn.Linear(64 * 4 * 4, 512)
        self.fc2 = nn.Linear(512, 10)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 64 * 4 * 4)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

model = SimpleCNN()
print(model)
```

### 3.4 GPU 설정

```python
# GPU 사용 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

model = model.to(device)
```

### 3.5 학습 실행

```python
# 손실 함수 및 옵티마이저
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 학습 루프
num_epochs = 10

for epoch in range(num_epochs):
    running_loss = 0.0
    correct = 0
    total = 0

    for i, (inputs, labels) in enumerate(trainloader):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    print(f'Epoch [{epoch+1}/{num_epochs}], '
          f'Loss: {running_loss/len(trainloader):.4f}, '
          f'Accuracy: {100.*correct/total:.2f}%')

print('Training completed!')
```

### 3.6 모델 저장 및 로드

```python
# 모델 저장
torch.save(model.state_dict(), 'cifar10_cnn.pth')

# 모델 로드
model.load_state_dict(torch.load('cifar10_cnn.pth'))
model.eval()
```

## 4. 모델 평가

### 4.1 테스트 정확도 계산

```python
correct = 0
total = 0
model.eval()

with torch.no_grad():
    for inputs, labels in testloader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

print(f'Test Accuracy: {100.*correct/total:.2f}%')
```

### 4.2 분류 결과 시각화

```python
# 이미지 시각화 함수
def imshow(img):
    img = img / 2 + 0.5
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

# 테스트 배치 시각화
dataiter = iter(testloader)
images, labels = next(dataiter)
images, labels = images.to(device), labels.to(device)

outputs = model(images)
_, predicted = torch.max(outputs, 1)

imshow(torchvision.utils.make_grid(images.cpu()))
print('Predicted: ', ' '.join([classes[predicted[j]] for j in range(4)]))
print('Ground Truth: ', ' '.join([classes[labels[j]] for j in range(4)]))
```

### 4.3 클래스별 정확도

```python
class_correct = [0.] * 10
class_total = [0.] * 10

with torch.no_grad():
    for inputs, labels in testloader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1

for i in range(10):
    print(f'{classes[i]}: {100.*class_correct[i]/class_total[i]:.2f}%')
```

## 5. Transfer Learning

### 5.1 사전 학습된 모델 사용

```python
import torchvision.models as models

# 사전 학습된 ResNet 모델 로드
model = models.resnet18(pretrained=True)

# 마지막 레이어 수정
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 10)

model = model.to(device)
```

### 5.2 Frozen Feature Extractor

```python
# 특징 추출기 파라미터 고정
for param in model.parameters():
    param.requires_grad = False

# 마지막 레이어만 학습
model.fc = nn.Linear(num_ftrs, 10).to(device)
```

## 6. Jetson 최적화

### 6.1 모델 변환 (TensorRT)

```python
# Torchscript로 변환
model.eval()
scripted_model = torch.jit.trace(model, torch.randn(1, 3, 32, 32).to(device))
scripted_model.save('model_traced.pt')
```

### 6.2 추론 최적화

```python
# 배치 처리로 추론 속도 향상
batch_input = torch.randn(32, 3, 32, 32).to(device)
model.eval()
with torch.no_grad():
    output = model(batch_input)
```

## 7. 실습 과제

1. CIFAR-10 데이터셋으로 CNN 모델을 학습시키세요.
2. 학습된 모델의 정확도를 평가하세요.
3. Transfer Learning을 사용하여 ResNet 모델을 학습시켜보세요.
4. TensorRT로 모델을 최적화하세요.

## 8. 다음 실습 예고

다음 클래스에서는 Image Regression 실습을 진행합니다.