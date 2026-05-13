# Class 03: Jetson DLI - Image Classification 실습

## 1. DLI(Deeper Learning Institute) 환경 설정

### 1.1 Swap File 생성

```bash
# Swap file 생성 (4GB 권장)
sudo systemctl disable nvzramconfig
sudo fallocate -l 4G /mnt/4GB.swap
sudo chmod 600 /mnt/4GB.swap
sudo mkswap /mnt/4GB.swap
sudo swapon /mnt/4GB.swap

# fstab에 추가
echo '/mnt/4GB.swap swap swap defaults 0 0' | sudo tee -a /etc/fstab

# 재부팅
sudo reboot
```

### 1.2 Docker 실행

```bash
# 데이터 디렉토리 생성
mkdir -p ~/nvdli-data

# DLI Docker 컨테이너 실행
sudo docker run --runtime nvidia -it --rm --network host \
    --volume ~/nvdli-data:/nvdli-nano/data \
    --device /dev/video0 \
    nvcr.io/nvidia/dli/dli-nano-ai:v2.0.2-r32.7.1
```

### 1.3 JupyterLab 접근

```bash
# 브라우저에서 접근
# http://<Jetson_IP>:8888
# Password: dlinano
```

## 2. Image Classification 개요

### 2.1 분류 vs 회귀

```
Classification (분류):
- 입력: 이미지
- 출력: 이산적 클래스 레이블 (예: cat, dog)
- 예: MNIST 숫자 인식, CIFAR-10 이미지 분류

Regression (회귀):
- 입력: 이미지
- 출력: 연속적 수치 (예: 나이, 좌표)
- 예: Face Landmark Detection, Age Estimation
```

### 2.2 CNN (Convolutional Neural Network)

```python
# CNN 기본 구조
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        
        # Convolution layers
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(2, 2)
        
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(2, 2)
        
        # Fully Connected layers
        self.fc1 = nn.Linear(64 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, num_classes)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.pool1(self.relu(self.conv1(x)))
        x = self.pool2(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x
```

## 3. Jetson DLI Image Classification 실습

### 3.1 데이터셋 준비

```python
# 필요한 라이브러리 임포트
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms

# CIFAR-10 데이터셋 전처리
transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# 데이터 로드
trainset = torchvision.datasets.CIFAR10(
    root='./data', train=True, download=True, transform=transform
)
testset = torchvision.datasets.CIFAR10(
    root='./data', train=False, download=True, transform=transform
)

trainloader = DataLoader(trainset, batch_size=32, shuffle=True)
testloader = DataLoader(testset, batch_size=32, shuffle=False)

# 클래스 정의
classes = ('plane', 'car', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck')
```

### 3.2 모델 정의

```python
# CNN 모델 정의
class ClassificationCNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Conv Block 1
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        # Conv Block 2
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        
        # Conv Block 3
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)
        
        # FC layers
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

# 모델 생성 및 GPU 설정
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

model = ClassificationCNN().to(device)
print(model)
```

### 3.3 학습 실행

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

### 3.4 모델 평가

```python
# 테스트 정확도 계산
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

# 클래스별 정확도
class_correct = [0.] * 10
class_total = [0.] * 10

with torch.no_grad():
    for inputs, labels in testloader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 1)
        c = (predicted == labels).squeeze()
        
        for i in range(len(labels)):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1

for i in range(10):
    print(f'{classes[i]}: {100.*class_correct[i]/class_total[i]:.2f}%')
```

## 4. Transfer Learning

### 4.1 사전 학습된 모델 사용

```python
import torchvision.models as models

# ResNet18 로드
model = models.resnet18(pretrained=True)

# 마지막 레이어 수정
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 10)

model = model.to(device)
```

### 4.2 특징 추출기 고정

```python
# 특징 추출기 파라미터 고정
for param in model.parameters():
    param.requires_grad = False

# 마지막 레이어만 학습
model.fc = nn.Linear(num_ftrs, 10).to(device)
```

## 5. Thumbs Project 실습 (DLI)

### 5.1 데이터 수집

```python
# TASK 및 CATEGORIES 정의
TASK = 'thumbs'
CATEGORIES = ['thumbs_up', 'thumbs_down']
DATASETS = ['A', 'B']

# 데이터 변환
transforms.Compose([
    transforms.ColorJitter(0.2, 0.2, 0.2, 0.2),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

### 5.2 모델 학습

```python
# ResNet-18 사용
model = torchvision.models.resnet18(pretrained=True)
model.fc = nn.Linear(512, len(CATEGORIES))
model = model.to(device)

# 학습 실행
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# ... 학습 루프 ...
```

## 6. 실습 과제

1. CIFAR-10 데이터셋으로 CNN 모델을 학습시키세요.
2. Transfer Learning을 적용하여 성능을 비교하세요.
3. Thumbs Project를 수행하여 실시간 분류를 확인하세요.
4. 모델을 저장하고 추론을 테스트하세요.

## 7. 다음 실습 예고

다음 클래스에서는 Image Regression 실습을 진행합니다.