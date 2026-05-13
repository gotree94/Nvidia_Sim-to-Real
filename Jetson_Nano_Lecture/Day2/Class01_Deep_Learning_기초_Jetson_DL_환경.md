# Class 01: Deep Learning 기초 및 Jetson DL 환경

## 1. 컴퓨터 구성 부품 개요

### 1.1 하드웨어 기본 구조

```
컴퓨터 구조:
┌─────────────────────────────────────┐
│           CPU (Central Processing Unit)         │
│    ┌──────────────┐ ┌──────────────┐           │
│    │   Encoder    │ │     ALU      │           │
│    │ (명령어 해독) │ │ (산술/논리)   │           │
│    └──────────────┘ └──────────────┘           │
├─────────────────────────────────────┤
│              Memory (RAM)                         │
├─────────────────────────────────────┤
│              Storage (HDD/SSD)                    │
└─────────────────────────────────────┘
```

### 1.2 CPU와 GPU 비교

| 구분 | CPU | GPU |
|------|-----|-----|
| 처리 방식 | 직렬 순차 처리 | 병렬 처리 (SIMD) |
| 핵심 구성 | ALU + Decoder | 다수의 코어 (Tensor Core) |
| 최적화 | 범용 연산 | 대규모 행렬 연산 |
| 사용처 | 시스템 제어, 로직 | 그래픽, 딥러닝 |

### 1.3 딥러닝과 GPU

```
Deep Learning 연산:
┌─────────────────────────────────────┐
│     Neural Network Forward/Backward        │
│                                             │
│    Input (X) → Hidden Layers → Output (Y)   │
│         ↓              ↓              ↓     │
│      행렬 곱셈 (Matrix Multiplication)       │
│                                             │
│    GPU는 이러한 연산에 최적화됨              │
└─────────────────────────────────────┘
```

## 2. 인공신경망 (Artificial Neural Network)

### 2.1 Perceptron (感知機)

Perceptron은 사람의 뇌 신경세포(neuron)의 동작을 흉내 낸 수학적 모델입니다.

```python
# Perceptron 기본 구조
class Perceptron:
    def __init__(self, input_size):
        # 가중치 초기화
        self.weights = np.random.randn(input_size)
        self.bias = 0
    
    def forward(self, x):
        # 입력값과 가중치의 선형 결합
        z = np.dot(x, self.weights) + self.bias
        # 활성화 함수 (Step function)
        return 1 if z > 0 else 0
    
    def train(self, X, y, epochs):
        for epoch in range(epochs):
            for xi, yi in zip(X, y):
                # 예측
                pred = self.forward(xi)
                # 오차 계산
                error = yi - pred
                # 가중치 업데이트 (학습)
                self.weights += error * xi * 0.1
                self.bias += error * 0.1
```

### 2.2 MLP (Multi-Layer Perceptron)

```python
# MLP 구조
class MLP:
    def __init__(self, layer_sizes):
        self.weights = []
        self.biases = []
        
        # 각 레이어의 가중치 초기화
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
            b = np.zeros(layer_sizes[i+1])
            self.weights.append(w)
            self.biases.append(b)
    
    def forward(self, X):
        self.activations = [X]
        
        for w, b in zip(self.weights, self.biases):
            # 행렬 곱셈 + Bias
            z = np.dot(self.activations[-1], w) + b
            # ReLU 활성화 함수
            a = np.maximum(0, z)
            self.activations.append(a)
        
        return self.activations[-1]
```

## 3. 딥러닝 프레임워크 개요

### 3.1 CUDA (Compute Unified Device Architecture)

```bash
# CUDA 버전 확인
nvcc --version

# GPU 정보 확인
nvidia-smi

# Jetson용 명령어
tegrastats
```

### 3.2 cuDNN (CUDA Deep Neural Network Library)

```
cuDNN 위치:
┌─────────────────────────────────────┐
│    TensorFlow / PyTorch             │
├─────────────────────────────────────┤
│         cuDNN (딥러닝 가속 라이브러리)│
├─────────────────────────────────────┤
│              CUDA                   │
├─────────────────────────────────────┤
│            GPU Hardware             │
└─────────────────────────────────────┘
```

### 3.3 TensorRT

```python
# TensorRT vs cuDNN 비교
"""
cuDNN:
- 목적: 딥러닝 연산 가속 (학습 & 추론)
- 사용: TensorFlow, PyTorch 내부에서 자동 호출

TensorRT:
- 목적: 추론 최적화 (실시간 성능 향상)
- 사용: 학습된 모델을 .trt로 변환 후 실행
- 특징: FP32 → FP16 → INT8 양자화 지원
"""
```

## 4. Jetson Nano Deep Learning 환경

### 4.1 JetPack 구성

```bash
# JetPack 버전 확인
cat /etc/nv_tegra_release

# CUDA 환경 변수 설정
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

### 4.2 Python 패키지 설치

```bash
# 필수 패키지
pip3 install numpy opencv-python
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip3 install tensorflow==2.7.0+nv

# Jetson-stats (시스템 모니터링)
pip3 install jetson-stats

# 모니터링 실행
jtop
```

## 5. 딥러닝 학습流程

### 5.1 순전파 (Forward Propagation)

```python
def forward_propagation(X, Y_true, model):
    """
    1. 입력 데이터 X를 모델에 통과시킴
    2. 모델 예측값 Y_pred 계산
    3. 손실함수로 오차 계산
    """
    # 예측
    Y_pred = model.forward(X)
    
    # 손실 계산 (Cross-Entropy)
    loss = -np.sum(Y_true * np.log(Y_pred + 1e-8))
    
    return Y_pred, loss
```

### 5.2 역전파 (Backward Propagation)

```python
def backward_propagation(X, Y_true, model, learning_rate=0.01):
    """
    1. 출력층에서 입력층 방향으로 오차 전파
    2. 각 레이어의 가중치에 대한 Gradient 계산
    3. Optimizer로 가중치 업데이트
    """
    # 출력층 Gradient 계산
    output_grad = Y_pred - Y_true
    
    # 역전파
    for i in range(len(model.weights) - 1, -1, -1):
        # Gradient 계산
        grad_w = np.dot(model.activations[i].T, output_grad)
        grad_b = np.sum(output_grad, axis=0)
        
        # 가중치 업데이트
        model.weights[i] -= learning_rate * grad_w
        model.biases[i] -= learning_rate * grad_b
        
        # 다음 레이어로 Gradient 전파
        if i > 0:
            output_grad = np.dot(output_grad, model.weights[i].T)
            output_grad *= (model.activations[i] > 0)  # ReLU derivative
```

### 5.3 학습 반복 (Epoch)

```python
def train(X_train, y_train, model, epochs=100, batch_size=32):
    for epoch in range(epochs):
        # Mini-batch 학습
        for i in range(0, len(X_train), batch_size):
            X_batch = X_train[i:i+batch_size]
            y_batch = y_train[i:i+batch_size]
            
            # 순전파
            y_pred, loss = forward_propagation(X_batch, y_batch, model)
            
            # 역전파
            backward_propagation(X_batch, y_batch, model)
        
        # 검증
        if epoch % 10 == 0:
            val_pred = model.forward(X_val)
            val_acc = accuracy(y_val, val_pred)
            print(f"Epoch {epoch}: Loss={loss:.4f}, Val Acc={val_acc:.4f}")
```

## 6. 실습 과제

1. Jetson Nano에 JetPack이 설치되어 있는지 확인하세요.
2. CUDA 및 cuDNN 버전을 확인하세요.
3. Python에서 PyTorch가 GPU를 인식하는지 확인하세요.
4. 간단한 Perceptron 모델을 구현하고 학습시켜보세요.

## 7. 다음 실습 예고

다음 클래스에서는 TensorFlow 기초와 CUDA 지원 TensorFlow 실습을 진행합니다.