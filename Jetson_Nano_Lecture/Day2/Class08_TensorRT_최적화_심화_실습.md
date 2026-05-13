# Class 08: TensorRT 최적화 및 심화 실습

## 1. TensorRT 개요

### 1.1 TensorRT 정의

TensorRT는 NVIDIA에서 개발한 딥러닝 추론 최적화 엔진입니다.

```
TensorRT 특징:
┌─────────────────────────────────────┐
│  - Layer Fusion (레이어 병합)       │
│  - Precision Calibration           │
│    (FP32 → FP16 → INT8)           │
│  - Kernel Auto-Tuning              │
│  - Memory Optimization             │
└─────────────────────────────────────┘
```

### 1.2 TensorRT vs cuDNN

| 구분 | cuDNN | TensorRT |
|------|-------|-----------|
| 목적 | 학습/추론 가속 | 추론 최적화 |
| 모델 변환 | 자동 | 수동 (필요) |
| 지원 정밀도 | FP32, FP16 | FP32, FP16, INT8 |
| 사용처 | TensorFlow, PyTorch 내부 | 최적화된 추론 |

## 2. TensorRT 변환

### 2.1 ONNX 모델 준비

```python
# YOLOv5를 ONNX로 변환
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.eval()

dummy_input = torch.randn(1, 3, 640, 640)

torch.onnx.export(
    model,
    dummy_input,
    'yolov5s.onnx',
    opset_version=13,
    input_names=['images'],
    output_names=['output']
)
```

### 2.2 trtexec 사용

```bash
# FP16 변환
/usr/src/tensorrt/bin/trtexec \
    --onnx=yolov5s.onnx \
    --saveEngine=yolov5s_fp16.engine \
    --workspace=4096 \
    --fp16

# INT8 변환 (Calibration 필요)
# /usr/src/tensorrt/bin/trtexec \
#     --onnx=yolov5s.onnx \
#     --saveEngine=yolov5s_int8.engine \
#     --workspace=4096 \
#     --int8
```

### 2.3 TensorRT Python API

```python
import tensorrt as trt

# TensorRT 로거
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

# 엔진 빌드
def build_engine(onnx_file):
    with trt.Builder(TRT_LOGGER) as builder, \
         builder.create_network(1) as network, \
         builder.create_builder_config() as config, \
         trt.OnnxParser(network, TRT_LOGGER) as parser:
        
        builder.max_batch_size = 1
        config.max_workspace_size = 1 << 30  # 1GB
        
        # FP16 활성화
        if builder.platform_has_fast_fp16:
            config.set_flag(trt.BuilderFlag.FP16)
        
        with open(onnx_file, 'rb') as f:
            parser.parse(f.read())
        
        return builder.build_serialized_network(network, config)

# 엔진 저장
engine = build_engine('yolov5s.onnx')
with open('yolov5s.trt', 'wb') as f:
    f.write(engine)
```

## 3. TensorRT 추론

### 3.1 엔진 로드 및 추론

```python
import tensorrt as trt
import pycuda.driver as cuda
import numpy as np

# 로더
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

with open('yolov5s.trt', 'rb') as f:
    engine_data = f.read()

runtime = trt.Runtime(TRT_LOGGER)
engine = runtime.deserialize_cuda_engine(engine_data)
context = engine.create_execution_context()

# 메모리 할당
input_size = engine.get_binding_shape(0)
output_size = engine.get_binding_shape(1)

d_input = cuda.mem_alloc(1 * input_size[1] * input_size[2] * input_size[3] * 4)
d_output = cuda.mem_alloc(1 * output_size[1] * 4)

bindings = [int(d_input), int(d_output)]

# 추론
def infer(image_data):
    # 입력 복사
    cuda.memcpy_htod(d_input, image_data)
    
    # 실행
    context.execute_v2(bindings)
    
    # 출력 읽기
    output = np.empty(output_size, dtype=np.float32)
    cuda.memcpy_dtoh(output, d_output)
    
    return output

# 테스트
input_data = np.random.randn(1, 3, 640, 640).astype(np.float32)
result = infer(input_data)
print(f"Output shape: {result.shape}")
```

## 4. 심화: 커스텀 YOLOv5 추론 앱

### 4.1 전체 추론 파이프라인

```python
import cv2
import torch
import tensorrt as trt
import numpy as np
from collections import OrderedDict, namedtuple

# 설정
CONF_THRES = 0.25
IOU_THRES = 0.45
IMG_SIZE = 640

# Class names (COCO)
CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light',
    # ... (80 classes)
]

# TensorRT 추론
def infer_trt(engine, image):
    # 전처리
    img = cv2.resize(image, (640, 640))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose(2, 0, 1)
    img = np.ascontiguousarray(img, dtype=np.float16) / 255.0
    img = torch.from_numpy(img).unsqueeze(0).cuda()
    
    # 추론 (기존 Python 구현 활용)
    # 또는 TensorRT bindings 사용
    return output

# 메인 실행
def main():
    # TensorRT 엔진 로드
    with open('yolov5s_fp16.engine', 'rb') as f:
        engine = trt.Runtime(TRT_LOGGER).deserialize_cuda_engine(f.read())
    
    context = engine.create_execution_context()
    
    # 카메라
    cap = cv2.VideoCapture(0)
    cap.set(640, 480)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 추론
        results = infer_trt(engine, frame)
        
        # 결과 시각화
        # ...
        
        cv2.imshow('YOLOv5 TensorRT', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
```

## 5. 성능 비교

### 5.1 FPS 측정

```python
import time
import cv2

def measure_fps(model, source, num_frames=100):
    cap = cv2.VideoCapture(source)
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
    return fps

# 테스트
print(f"PyTorch FPS: {measure_fps(yolov5s, 0)}")
print(f"TensorRT FPS: {measure_fps(yolov5s_trt, 0)}")
```

### 5.2 예상 결과

```
성능 비교 (Jetson Nano):
┌────────────────────┬────────┐
│ Model               │ FPS   │
├────────────────────┼────────┤
│ PyTorch YOLOv5s    │ ~5    │
│ TensorRT FP16      │ ~12   │
│ TensorRT INT8     │ ~18   │
└────────────────────┴────────┘
```

## 6. 실습 과제

1. YOLOv5 모델을 ONNX로 변환하세요.
2. TensorRT로 FP16 최적화된 모델을 생성하세요.
3. PyTorch와 TensorRT 성능을 비교하세요.
4. 실시간 웹캠 추론 애플리케이션을 작성하세요.

## 7. 마무리

이제까지 Jetson Nano에서 Deep Learning 실습을 완료했습니다.

```
요약:
- Day2: TensorFlow, PyTorch, Keras 기초
- Day2-3: DLI Image Classification
- Day2-4: DLI Image Regression
- Day2-5: PyTorch Basics
- Day2-6: Darknet/YOLOv4
- Day2-7: PyTorch YOLOv5
- Day2-8: TensorRT 최적화

배운 내용:
- 딥러닝 기초 (MLP, CNN)
- TensorFlow/PyTorch 활용
- Jetson에서 모델 학습 및 추론
- Darknet, YOLO 실습
- TensorRT 최적화
```