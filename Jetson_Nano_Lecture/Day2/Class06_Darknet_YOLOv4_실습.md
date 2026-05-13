# Class 06: Darknet 및 YOLOv4 실습

## 1. Darknet 소개

### 1.1 Darknet 정의

Darknet은 Joseph Redmon이 개발한 YOLO 모델의 기반이 되는 오픈소스 프레임워크입니다.

```
Darknet 특징:
┌─────────────────────────────────────┐
│  - C/CUDA로 구현 (경량화)          │
│  - YOLO 시리즈의 원본 구현        │
│  - 임베디드 시스템 지원            │
│  - 빠른 실행 속도                  │
└─────────────────────────────────────┘
```

### 1.2 YOLO 버전 역사

| 버전 | 개발자 | 특징 |
|------|--------|------|
| YOLOv1 | Redmon | 최초 |
| YOLOv2 (YOLO9000) | Redmon |anchor box 도입 |
| YOLOv3 | Redmon | 다중 스케일 |
| YOLOv4 | Bochkovskiy |Bag of Freebies |
| YOLOv5 | Ultralytics | PyTorch 기반 |

## 2. Darknet 설치

### 2.1 소스코드 클론

```bash
# Darknet 소스코드 다운로드
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
```

### 2.2 Makefile 설정

```makefile
# Makefile 수정
GPU=1
CUDNN=1
CUDNN_HALF=0  # Jetson Nano에서는 0 권장
OPENCV=1
```

### 2.3 빌드

```bash
make -j$(nproc)
```

### 2.4 가중치 다운로드

```bash
# YOLOv4 가중치 다운로드
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

# YOLOv4-tiny (경량화 버전)
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4-tiny.weights
```

## 3. Darknet 사용법

### 3.1 이미지 추론

```bash
# 이미지 객체 탐지
./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights data/dog.jpg

# 신뢰도 임계값 설정
./darknet detector test cfg/coco.data cfg/yolov4.cfg yolov4.weights -thresh 0.5 data/dog.jpg
```

### 3.2 웹캠 추론

```bash
# 웹캠 실시간 탐지
./darknet detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights -c 0
```

### 3.3 동영상 추론

```bash
# 동영상 파일 탐지
./darknet detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights video.mp4

# 결과 저장
./darknet detector demo cfg/coco.data cfg/yolov4.cfg yolov4.weights video.mp4 -out_filename output.mp4
```

## 4. YOLOv4 모델 구조

### 4.1cfg 파일 이해

```ini
# yolov4.cfg (핵심 섹션)

[net]
# Training/Evaluation 설정
batch=64
subdivisions=8
width=608
height=608
channels=3
momentum=0.949
decay=0.0005

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
random=1
```

### 4.2 주요 파라미터 설명

| 파라미터 | 설명 |
|----------|------|
| batch | GPU로 한 번에 처리하는 이미지 수 |
| subdivisions | batch를 여러 번으로 분할 (메모리 절약) |
| width/height | 입력 이미지 크기 |
| classes | 탐지할 클래스 수 |
| anchors | 앵커 박스 크기 |

## 5. Jetson Nano 최적화

### 5.1 입력 크기 조정

```ini
# yolov4.cfg 수정
[net]
width=416
height=416
```

### 5.2 YOLOv4-tiny 사용

```bash
# YOLOv4-tiny로 더 빠른 추론
./darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights -c 0
```

### 5.3 성능 비교

```
테스트 결과:
- YOLOv4: ~2 FPS (Jetson Nano)
- YOLOv4-tiny: ~12 FPS (Jetson Nano)
```

## 6. 커스텀 데이터 학습

### 6.1 데이터셋 준비

```
dataset/
├── images/
│   ├── train/
│   └── val/
└── labels/  (YOLO 포맷)
    ├── train/
    └── val/
```

### 6.2.data 파일 설정

```ini
# custom.data
classes= 2
train  = data/train.txt
valid  = data/valid.txt
names = data/custom.names
backup = backup/
```

### 6.3 학습 실행

```bash
./darknet detector train data/custom.data cfg/yolov4-custom.cfg yolov4.weights
```

## 7. 실습 과제

1. Darknet을 Jetson Nano에 설치하세요.
2. YOLOv4와 YOLOv4-tiny 성능을 비교하세요.
3. 커스텀 데이터로 모델을 학습시키세요.
4. 입력 이미지 크기를 변경하여 속도 차이를 확인하세요.

## 8. 다음 실습 예고

다음 클래스에서는 PyTorch YOLOv5 실습을 진행합니다.