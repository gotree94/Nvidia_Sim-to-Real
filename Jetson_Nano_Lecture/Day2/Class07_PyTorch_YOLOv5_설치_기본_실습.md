# Class 07: PyTorch YOLOv5 설치 및 기본 실습

## 1. YOLOv5 개요

### 1.1 YOLOv5 정의

YOLOv5는 Ultralytics에서 개발한 PyTorch 기반의 YOLO 시리즈 최신 버전입니다.

```
YOLOv5 모델 변형:
┌─────────────────────────────────────┐
│  YOLOv5n  (nano)   - 1.9M params    │
│  YOLOv5s  (small)  - 7.2M params   │
│  YOLOv5m  (medium) - 21.2M params   │
│  YOLOv5l  (large)  - 46.5M params   │
│  YOLOv5x  (xlarge) - 86.7M params  │
└─────────────────────────────────────┘
```

### 1.2 YOLOv4 vs YOLOv5

| 구분 | YOLOv4 | YOLOv5 |
|------|---------|---------|
| 프레임워크 | Darknet | PyTorch |
| 속도 | 느림 | 빠름 |
| 사용성 | 어려움 | 쉬움 |
| 커뮤니티 | 제한적 | 활발 |

## 2. Jetson에 YOLOv5 설치

### 2.1 의존성 설치

```bash
# 기본 의존성
sudo apt-get update
sudo apt-get install -y libopenmpi-dev libopenblas-dev

# PyTorch 설치 (JP 4.6.1)
wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl \
    -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl

# TorchVision 설치
git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
cd torchvision
sudo python3 setup.py install
```

### 2.2 YOLOv5 클론

```bash
# 클론 및特定 커밋으로 이동
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
git reset --hard 9bcc32a

# requirements.txt 수정
# pillow==8.3.2 추가
pip3 install -r requirements.txt

# 환경변수 설정
echo "export OPENBLAS_CORETYPE=ARMV8" >> ~/.bashrc
source ~/.bashrc
```

### 2.3 사전 학습 모델 다운로드

```bash
# YOLOv5s 모델 다운로드
wget https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt
```

## 3. YOLOv5 추론

### 3.1 이미지 추론

```bash
# 기본 추론
python3 detect.py --weights yolov5s.pt --source data/images/bus.jpg

# 옵션 설명
# --weights: 모델 파일
# --source: 입력 소스 (0=웹캠, 이미지, 동영상, 디렉토리)
# --img: 입력 이미지 크기 (default: 640)
# --conf-thres: 신뢰도 임계값 (default: 0.25)
# --nosave: 결과 저장 안함
```

### 3.2 웹캠 추론

```bash
# 웹캠으로 실시간 추론
python3 detect.py --weights yolov5s.pt --source 0 --img 320 --nosave
```

### 3.3 Python 코드에서 추론

```python
import torch

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 추론
img = 'test.jpg'
results = model(img)

# 결과 접근
print(results.xyxy[0])  # bounding boxes
print(results.pandas().xyxy[0])  # DataFrame

# 시각화
results.show()
results.save()
```

## 4. 커스텀 데이터 학습

### 4.1 데이터셋 구조

```
dataset/
├── images/
│   ├── train/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   └── val/
│       └── ...
└── labels/
    ├── train/
    │   ├── image1.txt  # YOLO 포맷
    │   └── image2.txt
    └── val/
        └── ...
```

### 4.2 데이터 설정 파일

```yaml
# data/custom.yaml
path: dataset
train: images/train
val: images/val

nc: 10  # 클래스 수

names:
  0: person
  1: car
  # ... (클래스 이름)
```

### 4.3 학습 실행

```bash
# 학습
python3 train.py --data data/custom.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 50
```

## 5. ONNX 변환

### 5.1 ONNX로 변환

```python
import torch

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.eval()

# 더미 입력
dummy_input = torch.randn(1, 3, 640, 640)

# ONNX로 변환
torch.onnx.export(
    model,
    dummy_input,
    'yolov5s.onnx',
    opset_version=13,
    input_names=['images'],
    output_names=['output'],
    dynamic_axes={
        'images': {0: 'batch'},
        'output': {0: 'batch'}
    }
)

print("ONNX 변환 완료!")
```

### 5.2 ONNX 추론

```bash
# ONNX 모델로 추론
python3 detect.py --weights yolov5s.onnx --source 0 --nosave
```

## 6. 실습 과제

1. YOLOv5를 Jetson에 설치하세요.
2. 사전 학습 모델로 웹캠 추론을 실행하세요.
3. 커스텀 데이터셋으로 모델을 학습시키세요.
4. ONNX로 변환 후 추론을 비교하세요.

## 7. 다음 실습 예고

다음 클래스에서는 TensorRT 최적화와 심화 실습을 진행합니다.