# Class 07: Darknet, PyTorch, TensorRT 소개 및 Darknet 실습

## 1. Darknet 소개

### 1.1 Darknet이란?

Darknet은 Joseph Redmon이 개발한 오픈소스 딥러닝 프레임워크입니다. YOLO(You Only Look Once) 알고리즘의 원본 구현으로 유명합니다.

### 1.2 주요 특징

- **경량화**: C로 구현되어 빠른 실행
- **CUDA 지원**: GPU 가속 지원
- **Windows/Linux 지원**: 다양한 플랫폼 호환
- **YOLO Native**: YOLO 시리즈의 기본 프레임워크

### 1.3 Darknet 아키텍처

```
Darknet Architecture:
┌─────────────────────────────────────┐
│         Configuration              │
│    (cfg file - network structure) │
├─────────────────────────────────────┤
│           Darknet Library          │
│     (C implementation - layers)    │
├─────────────────────────────────────┤
│          Weights File              │
│        (pretrained weights)        │
└─────────────────────────────────────┘
```

## 2. PyTorch 소개

### 2.1 PyTorch란?

PyTorch는 Facebook에서 개발한 딥러닝 프레임워크입니다. 동적 계산 그래프와 직관적인 API로 연구자와 개발자에게 널리 사용됩니다.

### 2.2 주요 특징

- **Dynamic Computational Graph**: 즉시 실행 모드
- **Python-first**: Python과 자연스러운 통합
- **TorchScript**: 모델 직렬화
- **Distributed Training**: 분산 학습 지원
- **ONNX 지원**: 모델 변환 유연성

### 2.3 PyTorch vs TensorFlow

| 특성 | PyTorch | TensorFlow |
|------|---------|------------|
| 그래프 유형 | 동적 | 정적/동적 |
| 학습 난이도 | 낮음 | 중간 |
| 프로덕션 지원 | 높음 | 매우 높음 |
| 디버깅 | 용이 | 어려움 |
| 커뮤니티 | 빠르게 성장 | 방대함 |

## 3. TensorRT 소개

### 3.1 TensorRT란?

TensorRT는 NVIDIA에서 개발한 고성능 딥러닝 추론 엔진입니다. 모델을 최적화하여 GPU에서 빠른 추론을 가능하게 합니다.

### 3.2 최적화 기법

- **Layer Fusion**: 여러 레이어 병합
- **Precision Calibration**: FP32 → FP16/INT8 양자화
- **Kernel Auto-Tuning**: GPU별 커널 최적화
- **Memory Optimization**: 메모리 사용 최적화

### 3.3 TensorRT 워크플로우

```
Training → Model Export → TensorRT Optimization → Inference
                                     │
                                     ▼
                              ┌─────────────┐
                              │    .trt     │
                              │   model     │
                              └─────────────┘
```

## 4. Darknet 실습

### 4.1 Darknet 설치

```bash
# Darknet 클론
git clone https://github.com/AlexeyAB/darknet.git
cd darknet

# Makefile 수정 (GPU, CUDA 활성화)
# GPU=1
# CUDNN=1
# OPENCV=1

# 빌드
make -j$(nproc)

# 빌드 확인
./darknet version
```

### 4.2 사전 학습된 모델 다운로드

```bash
# YOLOv4 weights 다운로드
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

# YOLOv3 weights 다운로드
wget https://pjreddie.com/media/files/yolov3.weights

# tiny 버전 (빠른 추론)
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4-tiny.weights
```

### 4.3 이미지 추론

```bash
# YOLOv4로 이미지 추론
./darknet detector test \
    cfg/coco.data \
    cfg/yolov4.cfg \
    yolov4.weights \
    data/dog.jpg

# Confidence threshold 설정
./darknet detector test \
    cfg/coco.data \
    cfg/yolov4.cfg \
    yolov4.weights \
    -thresh 0.5 \
    data/dog.jpg
```

### 4.4 Darknet Python Binding

```python
import cv2
import numpy as np

# Darknet Python bindings
import darknet

# 네트워크 초기화
network, class_names, class_colors = darknet.load_network(
    b"cfg/yolov4.cfg",
    b"cfg/coco.data",
    b"yolov4.weights"
)

# 이미지 추론
image = cv2.imread('data/dog.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_resized = cv2.resize(image_rgb, (darknet.network_width(network), darknet.network_height(network)))

darknet_image = darknet.make_image(
    darknet.network_width(network),
    darknet.network_height(network),
    3
)

darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
detections = darknet.detect_image(network, class_names, darknet_image)

print("Detections:", detections)
```

### 4.5 커스텀 데이터셋 학습

```python
# 데이터셋 준비
# - images/: 이미지 파일
# - labels/: bounding box annotation (YOLO format)
#   class_id x_center y_center width height (normalized)

# Training command
# ./darknet detector train \
#     data/custom.data \
#     cfg/yolov4-custom.cfg \
#     yolov4.weights
```

## 5. YOLO 설정 파일 이해

### 5.1 yolov4.cfg 구조

```ini
[net]
# Testing
# batch=1
# subdivisions=1

# Training
batch=64
subdivisions=16
width=608
height=608
channels=3
momentum=0.949
decay=0.0005
angle=0
saturation = 1.5
exposure = 1.5
hue=.1

[convolutional]
batch_normalize=1
filters=32
size=3
stride=1
pad=1
activation=mish

[maxpool]
size=2
stride=2

[yolo]
mask = 0,1,2
anchors = 12,16, 19,36, 40,28, 36,75, 76,55, 72,146
classes=80
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1
```

### 5.2 데이터 설정 파일

```ini
# custom.data
classes= 80
train  = data/train.txt
valid  = data/valid.txt
names = data/coco.names
backup = backup/
```

## 6. Darknet 최적화

### 6.1 INT8 양자화

```bash
# Darknet에서 INT8 추론
./darknet detector test \
    cfg/coco.data \
    cfg/yolov4.cfg \
    yolov4.weights \
    -dont_show \
    -ext_output \
    data/dog.jpg
```

### 6.2 Jetson에서 Darknet

```bash
# Jetson Nano에서 Darknet 빌드
cd darknet
sed -i 's/GPU=0/GPU=1/' Makefile
sed -i 's/CUDNN=0/CUDNN=1/' Makefile
sed -i 's/OPENCV=0/OPENCV=1/' Makefile

# Jetson 특화 최적화
# ARM neon 활성화
make -j4
```

## 7. Darknet 실습 과제

### 7.1 기본 추론 실습

```python
# 실습 1: Darknet으로 이미지 추론
# 1. Darknet 설치
# 2. YOLOv4 weights 다운로드
# 3. 테스트 이미지 추론

# 실습 2: Python으로 추론
# 1. Python bindings 컴파일
# 2. 이미지 로드 및 전처리
# 3. 추론 및 결과 시각화
```

### 7.2 커스텀 학습 실습

```bash
# 실습 3: 커스텀 데이터 학습
# 1. 데이터셋 준비 (YOLO 포맷)
# 2. 설정 파일 생성
# 3. 모델 학습
# 4. 추론 테스트
```

## 8. TensorRT 최적화

### 8.1 Darknet에서 TensorRT로

```bash
# Darknet weights를 ONNX로 변환
# 1. Darknet → ONNX
# 2. ONNX → TensorRT

# onnx-tensorrt 설치 필요
pip3 install onnx onnxruntime
pip3 install tensorrt
```

### 8.2 PyTorch에서 TensorRT

```python
import torch
import tensorrt as trt

# PyTorch 모델을 TorchScript로 변환
model = MyModel().eval()
example_input = torch.randn(1, 3, 416, 416)
traced_model = torch.jit.trace(model, example_input)
traced_model.save('model.pt')

# TensorRT로 변환 (명령줄)
trtexec --onnx=model.onnx --saveEngine=model.trt
```

## 9. Jetson에서 Darknet/TensorRT

### 9.1 Jetson 최적화 스크립트

```bash
# Jetson Performance 설정
sudo nvpmodel -m 0
sudo jetson_clocks

# Darknet 추론 테스트
./darknet detector test \
    cfg/coco.data \
    cfg/yolov4-tiny.cfg \
    yolov4-tiny.weights \
    data/dog.jpg
```

### 9.2 프레임 레이트 측정

```bash
# FPS 측정
./darknet detector demo \
    cfg/coco.data \
    cfg/yolov4-tiny.cfg \
    yolov4-tiny.weights \
    -c 0 \
    -dont_show \
    -benchmark
```

## 10. 실습 과제

1. Darknet을 설치하고 YOLOv4 모델을 실행하세요.
2. Python으로 Darknet 추론을 수행하세요.
3. Darknet 모델의 추론 속도를 측정하세요.
4. Jetson Nano에서 Darknet을 빌드하고 실행하세요.

## 11. 다음 실습 예고

다음 클래스에서는 PyTorch YOLOv5 실습을 진행합니다.