# Class 08: PyTorch YOLOv5 실습

## 1. PyTorch YOLOv5 개요

### 1.1 YOLOv5 소개

YOLOv5는 Ultralytics에서 개발한 YOLO 시리즈의 최신 버전입니다. PyTorch 기반으로 구현되어 사용 편의성이 크게 향상되었습니다.

### 1.2 모델 변형

| 모델 | 파라미터 | mAP@0.5 | 추론 속도 |
|------|----------|---------|-----------|
| YOLOv5n | 1.9M | 28.0 | 1ms |
| YOLOv5s | 7.2M | 37.4 | 2ms |
| YOLOv5m | 21.2M | 45.4 | 4ms |
| YOLOv5l | 46.5M | 49.0 | 7ms |
| YOLOv5x | 86.7M | 51.9 | 12ms |

### 1.3 YOLOv5 특징

- **PyTorch Native**: 모든 기능이 PyTorch로 구현
- **AutoML**: 하이퍼파라미터 자동 최적화
- **Model Ensemble**: 다중 모델 결합
- **Export Options**: ONNX, TensorRT, CoreML 등 지원
- **Active Training**:Continuous 학습 지원

## 2. YOLOv5 설치

### 2.1 요구 사항

```bash
# 필수 패키지 설치
pip3 install torch torchvision torchaudio
pip3 install matplotlib pillow pandas seaborn
pip3 install opencv-python
pip3 install scipy
```

### 2.2 YOLOv5 클론

```bash
# YOLOv5 저장소 클론
git clone https://github.com/ultralytics/yolov5.git
cd yolov5

# 의존성 설치
pip3 install -r requirements.txt

# 설치 확인
python3 detect.py --source data/images/bus.jpg
```

### 2.3 Jetson에서 설치

```bash
# Jetson용 PyTorch 설치 (whl 파일 사용)
# https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-10/72048

# TensorFlow와 호환되는 버전 선택
pip3 install torch==1.10.0+cpu torchvision==0.11.0+cpu -f \
    https://download.pytorch.org/whl/torch_stable.html
```

## 3. 사전 학습된 모델 사용

### 3.1 모델 다운로드

```python
import torch

# YOLOv5s (small) 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 다른 크기 모델 로드
# yolov5n, yolov5m, yolov5l, yolov5x 도 가능

print(model)
```

### 3.2 이미지 추론

```python
import cv2
from PIL import Image

# 이미지 로드
img = Image.open('data/images/bus.jpg')

# 추론
results = model(img)

# 결과 출력
print(results.xyxy[0])  # bounding boxes
print(results.pandas().xyxy[0])  # DataFrame 형식
```

### 3.3 결과 시각화

```python
# 결과 표시
results.show()

# 이미지 저장
results.save()

# 바운딩 박스 정보
boxes = results.xyxy[0].cpu().numpy()
for box in boxes:
    x1, y1, x2, y2, conf, cls = box
    print(f"Class: {int(cls)}, Conf: {conf:.2f}, Box: [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")
```

### 3.4 비디오 추론

```python
# 비디오에서 추론
cap = cv2.VideoCapture('video.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 추론
    results = model(frame)

    # 결과 시각화
    cv2.imshow('YOLOv5', np.squeeze(results.render()))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 3.5 실시간 웹캠

```python
# 웹캠 실시간 추론
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Camera not available")
        break

    # 추론
    results = model(frame)

    # 결과 표시
    cv2.imshow('YOLOv5 Webcam', np.squeeze(results.render()))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
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
│       ├── image3.jpg
│       └── image4.jpg
└── labels/
    ├── train/
    │   ├── image1.txt
    │   └── image2.txt
    └── val/
        ├── image3.txt
        └── image4.txt
```

### 4.2 Annotation 형식

```txt
# label.txt (YOLO 포맷)
# class_id center_x center_y width height
# (모든 값은 이미지에 대해 정규화됨: 0~1)

0 0.5 0.5 0.3 0.4  # 클래스 0의 객체
1 0.3 0.7 0.2 0.2  # 클래스 1의 객체
```

### 4.3 데이터 설정 파일

```yaml
# data/custom.yaml
# dataset root directory
path: dataset
train: images/train
val: images/val

# number of classes
nc: 10

# class names
names:
  0: person
  1: car
  2: dog
  3: cat
  4: bicycle
  5: motorcycle
  6: airplane
  7: bus
  8: train
  9: truck
```

### 4.4 모델 학습

```python
# 명령줄에서 학습
# python3 train.py --data data/custom.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 50

# Python 코드에서 학습
import torch
from yolov5 import train

train.run(
    data='data/custom.yaml',
    cfg='models/yolov5s.yaml',
    weights='yolov5s.pt',
    epochs=50,
    batch_size=16,
    imgsz=640,
    device='0',  # GPU
    workers=8,
    project='runs/train',
    name='exp'
)
```

### 4.5 학습 모니터링

```bash
# TensorBoard로 학습 모니터링
tensorboard --logdir runs/train

# 학습 결과 확인
# runs/train/exp/weights/best.pt
# runs/train/exp/weights/last.pt
```

### 4.6 학습된 모델 평가

```python
# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/exp/weights/best.pt')

# 추론 테스트
results = model('test_image.jpg')
results.show()
results.save()
```

## 5. 모델 최적화

### 5.1 TorchScript 변환

```python
# TorchScript로 변환
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.eval()

example_input = torch.randn(1, 3, 640, 640)
traced_model = torch.jit.trace(model, example_input)
traced_model.save('yolov5s.pt')
```

### 5.2 ONNX 변환

```python
# ONNX로 변환
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.eval()

example_input = torch.randn(1, 3, 640, 640)
torch.onnx.export(
    model,
    example_input,
    'yolov5s.onnx',
    opset_version=11,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}}
)

print("ONNX 모델 저장 완료")
```

### 5.3 TensorRT 변환

```bash
# ONNX에서 TensorRT로 변환
python3 -c "
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

def build_engine(onnx_file):
    with trt.Builder(TRT_LOGGER) as builder, \
         builder.create_network(1) as network, \
         trt.OnnxParser(network, TRT_LOGGER) as parser:
        builder.max_batch_size = 1
        builder.max_workspace_size = 1 << 30
        with open(onnx_file, 'rb') as f:
            parser.parse(f.read())
        return builder.build_cuda_engine(network)

engine = build_engine('yolov5s.onnx')
with open('yolov5s.trt', 'wb') as f:
    f.write(engine.serialize())
print('TensorRT 모델 저장 완료')
"
```

## 6. Jetson에서 YOLOv5

### 6.1 Jetson용 모델 최적화

```python
# Jetson에서 FP16 최적화
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = model.half()  # FP16 변환

# 추론
img = torch.randn(1, 3, 640, 640).half()
output = model(img)
```

### 6.2 Jetson 추론 스크립트

```python
import torch
import cv2
import numpy as np
from PIL import Image

# Jetson에서 YOLOv5 추론
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', device=device)
model = model.half()  # FP16

# 이미지 추론
img = cv2.imread('test.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = model(img)

# 결과 표시
print(results.pandas().xyxy[0])
```

### 6.3 Triton Inference Server

```python
# Triton 서버 모델 설정 (config.pbtxt)
"""
name: "yolov5s"
platform: "tensorrt_plan"
max_batch_size: 8
input [
  {
    name: "input"
    shape: [1, 3, 640, 640]
    dtype: TYPE_FP16
  }
]
output [
  {
    name: "output"
    shape: [1, 25200, 85]
    dtype: TYPE_FP16
  }
]
"""
```

## 7. 실습: 객체 추적

### 7.1 DeepSORT 연동

```python
# YOLOv5 + DeepSORT로 객체 추적
# https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch

# 설치
git clone https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch.git

# 실행
python3 track.py --source 0 --yolo-weights yolov5s.pt
```

### 7.2 다중 객체 추적

```python
# Track 클래스 사용 예시
from deep_sort import DeepSort

deepsort = DeepSort(
    "deep_checkpoints/ckpt.t7",
    max_dist=0.3,
    max_iou_distance=0.7,
    max_age=30,
    n_init=3
)

# 각 프레임에서 추적
for frame in video_frames:
    detections = model(frame)
    outputs = deepsort.update(detections, frame)
```

## 8. Jetson 성능 최적화

### 8.1 성능 설정

```bash
# Jetson 클록 설정
sudo jetson_clocks

#.power 모드 설정
sudo nvpmodel -m 0  # Max Performance
sudo nvpmodel -m 1  # Economic Mode

# 부스트 활성화
echo 1 | sudo tee /sys/devices/70090000.gpu/power/control
```

### 8.2 프레임 레이트 측정

```python
import time

# FPS 측정
def measure_fps(model, video_source, num_frames=100):
    cap = cv2.VideoCapture(video_source)
    start_time = time.time()

    frame_count = 0
    while frame_count < num_frames:
        ret, frame = cap.read()
        if not ret:
            break

        _ = model(frame)
        frame_count += 1

    elapsed = time.time() - start_time
    fps = frame_count / elapsed

    cap.release()
    print(f"FPS: {fps:.2f}")
    return fps

fps = measure_fps(model, 'test.mp4')
```

### 8.3 배치 처리

```python
# 배치 처리로 효율성 향상
def batch_inference(model, images, batch_size=8):
    results = []
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]
        batch_results = model(batch)
        results.extend(batch_results)
    return results
```

## 9. 실습 과제

1. YOLOv5s 모델을 설치하고 테스트 이미지를 추론하세요.
2. 웹캠을 사용하여 실시간 객체 탐지를 수행하세요.
3. 커스텀 데이터셋으로 YOLOv5 모델을 학습시키세요.
4. 학습된 모델을 ONNX 및 TensorRT로 변환하세요.
5. Jetson Nano에서 추론 속도를 측정하고 최적화하세요.

## 10. 부록: YOLOv5 명령어 모음

```bash
# 추론
python3 detect.py --source data/images --weights yolov5s.pt

# 학습
python3 train.py --data data/coco.yaml --cfg yolov5s.yaml --weights yolov5s.pt --epochs 100

# 검증
python3 val.py --data data/coco.yaml --weights yolov5s.pt

# 모델 내보내기
python3 export.py --weights yolov5s.pt --include onnx tensorrt

# 배치 추론
python3 detect.py --source inference/images --weights yolov5s.pt --save-txt --save-conf
```