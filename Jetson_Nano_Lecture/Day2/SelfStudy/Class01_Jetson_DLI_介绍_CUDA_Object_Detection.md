# Class 01: Jetson DLI 소개 및 CUDA, Object Detection 기초

## 1. Jetson DLI(Deeper Learning Institute) 소개

### 1.1 Jetson 플랫폼 개요

NVIDIA Jetson은 edge computing을 위한 임베디드 AI 플랫폼입니다. Jetson 시리즈에는 다양한 모델이 있습니다:

- **Jetson Nano**:entry-level, low power consumption
- **Jetson Xavier NX**: mid-range, excellent performance
- **Jetson AGX Xavier**: high-end, maximum performance
- **Jetson Orin**: latest generation, powerful AI computing

### 1.2 DLI(Deeper Learning Institute) 란?

DLI는 NVIDIA에서 운영하는 딥러닝 교육 프로그램입니다. Jetson DLI 실습을 통해 다음 내용을 학습합니다:

- Edge AI application development
- CUDA programming basics
- Neural network optimization
- Real-time inference

### 1.3 JetPack 개요

JetPack은 Jetson 플랫폼의 소프트웨어 스택입니다:

```
JetPack Components:
├── CUDA Toolkit - GPU programming
├── cuDNN - CUDA Deep Neural Network library
├── TensorRT - High-performance inference engine
├── OpenCV - Computer vision library
├── Docker - Container runtime
└── Jupyter - Interactive notebook
```

## 2. CUDA(Compute Unified Device Architecture) 기초

### 2.1 CUDA란?

CUDA는 NVIDIA GPU에서 병렬 컴퓨팅을 수행하기 위한 플랫폼이자 프로그래밍 모델입니다.

### 2.2 GPU 아키텍처 이해

```
GPU Architecture:
┌─────────────────────────────────────┐
│           Host (CPU)                │
│    - Main memory                    │
│    - System bus                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│           Device (GPU)              │
│  ┌─────────┐ ┌─────────┐ ┌────────┐│
│  │  SM 0   │ │  SM 1   │ │ SM N  ││
│  │ Thread  │ │ Thread  │ │Thread ││
│  │ Block   │ │ Block   │ │Block  ││
│  └─────────┘ └─────────┘ └────────┘│
│  ┌─────────────────────────────┐  │
│  │       Global Memory         │  │
│  └─────────────────────────────┘  │
└─────────────────────────────────────┘
```

### 2.3 CUDA 프로그래밍 기초

**Kernel 함수 정의:**
```c
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}
```

**Kernel 호출:**
```c
int blocks = (n + 255) / 256;
vectorAdd<<<blocks, 256>>>(d_a, d_b, d_c, n);
```

### 2.4 Jetson에서 CUDA 확인

```bash
# CUDA 버전 확인
nvcc --version

# GPU 정보 확인
nvidia-smi

# Jetson용 명령어
tegrastats
```

## 3. Object Detection 기초

### 3.1 Object Detection란?

Object Detection은 이미지에서 객체의 위치와 클래스를 식별하는 컴퓨터 비전 기술입니다.

### 3.2 주요 알고리즘

| 알고리즘 | 특징 | 속도 | 정확도 |
|---------|------|------|--------|
| YOLO | One-stage detection | 빠름 | 중간 |
| SSD | Single shot detection | 빠름 | 중간 |
| Faster R-CNN | Two-stage detection | 느림 | 높음 |
| RetinaNet | Focal loss 기반 | 중간 | 높음 |

### 3.3 Detection 파이프라인

```
Input Image → Preprocessing → Feature Extraction →
Region Proposal → Classification → Post-processing → Output
```

### 3.4 Jetson에서 Object Detection 실습 준비

```bash
# TensorRT로 사전 빌드된 모델 확인
ls /usr/src/tensorrt/samples/

# DeepStream 설치 확인
dpkg -l | grep deepstream
```

## 4. 실습 사전 준비

### 4.1 Jetson Nano 초기 설정

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# JetPack 버전 확인
cat /etc/nv_tegra_release

# CUDA 환경 변수 설정
export CUDA_HOME=/usr/local/cuda
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

### 4.2 필요 패키지 설치

```bash
# Python 패키지 설치
pip3 install numpy opencv-python torch torchvision

# jetson-stats로 시스템 모니터링
pip3 install jetson-stats
```

## 5. 확인 문제

1. Jetson Nano의 컴퓨팅 성능은 어떤 수준인가요?
2. CUDA와 cuDNN의 차이점은 무엇인가요?
3. One-stage detector와 Two-stage detector의 차이점을 설명하세요.
4. Jetson에서 GPU 사용량을 확인하는 명령어는?

## 6. 다음 실습 예고

다음 클래스에서는 Jetson DLI Docker 설치와 Jupyter 환경 설정 방법을 학습합니다.