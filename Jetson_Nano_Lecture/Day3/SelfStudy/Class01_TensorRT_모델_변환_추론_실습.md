# Class 01: TensorRT 모델 변환 및 추론 실습

## 1. TensorRT 기초

### 1.1 TensorRT란?

TensorRT는 NVIDIA에서 개발한 고성능 딥러닝 추론 엔진입니다. 모델을 최적화하여 GPU에서 낮은 지연 시간과 높은 처리량을 달성합니다.

### 1.2 최적화 기법

```
TensorRT Optimization:
┌─────────────────────────────────────┐
│         Layer Fusion               │
│    (여러 레이어을 하나로 병합)      │
├─────────────────────────────────────┤
│         Precision Calibration      │
│    (FP32 → FP16 → INT8)            │
├─────────────────────────────────────┤
│         Kernel Auto-Tuning         │
│    (GPU 아키텍처별 최적 커널 선택)   │
├─────────────────────────────────────┤
│         Memory Optimization        │
│    (메모리 사용 최적화)             │
└─────────────────────────────────────┘
```

### 1.3 지원 프레임워크

- TensorFlow
- PyTorch
- ONNX
- Caffe
- Darknet

## 2. TensorRT 설치

### 2.1 JetPack에 포함된 TensorRT

```bash
# JetPack 버전 확인
cat /etc/nv_tegra_release

# TensorRT 버전 확인
dpkg -l | grep tensorrt
```

### 2.2 Python TensorRT 설치

```bash
# Python binding 설치
pip3 install pycuda

# TensorRT Python package (JetPack에 포함됨)
python3 -c "import tensorrt; print(tensorrt.__version__)"
```

### 2.3 TensorRT 샘플 확인

```bash
# TensorRT 샘플 디렉토리
ls /usr/src/tensorrt/samples/

# Python 샘플 확인
ls /usr/src/tensorrt/python/
```

## 3. PyTorch 모델에서 TensorRT로

### 3.1 PyTorch → ONNX → TensorRT 파이프라인

```python
import torch
import torch.nn as nn

# 간단한 모델 정의
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.fc = nn.Linear(32 * 8 * 8, 10)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# 모델 생성 및 저장
model = SimpleModel().eval()
torch.save(model.state_dict(), 'model.pth')

print("Model saved!")
print(model)
```

### 3.2 ONNX로 변환

```python
import torch.onnx

# 더미 입력 생성
dummy_input = torch.randn(1, 3, 32, 32)

# ONNX로 변환
torch.onnx.export(
    model,
    dummy_input,
    'model.onnx',
    export_params=True,
    opset_version=11,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)

print("ONNX model saved!")

# ONNX 모델 검증
import onnx
onnx_model = onnx.load('model.onnx')
onnx.checker.check_model(onnx_model)
print("ONNX model verified!")
```

### 3.3 TensorRT로 변환

```python
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np

# TensorRT 로거 설정
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

def build_engine(onnx_file_path):
    """ONNX 파일에서 TensorRT 엔진 빌드"""
    with trt.Builder(TRT_LOGGER) as builder, \
         builder.create_network(1) as network, \
         builder.create_builder_config() as config, \
         trt.OnnxParser(network, TRT_LOGGER) as parser:

        # 최대 배치 크기 설정
        builder.max_batch_size = 1

        # 워크스페이스 크기 설정 (1GB)
        config.max_workspace_size = 1 << 30

        # FP16 지원 (Jetson Nano에서 지원 시)
        if builder.platform_has_fast_fp16:
            config.set_flag(trt.BuilderFlag.FP16)

        # ONNX 파일 읽기
        with open(onnx_file_path, 'rb') as f:
            if not parser.parse(f.read()):
                print("ONNX parsing failed!")
                for error in range(parser.num_errors):
                    print(f"Error: {parser.get_error(error)}")
                return None

        # 엔진 빌드
        print("Building TensorRT engine...")
        return builder.build_serialized_network(network, config)

# 엔진 빌드 및 저장
engine = build_engine('model.onnx')

if engine:
    with open('model.trt', 'wb') as f:
        f.write(engine)
    print("TensorRT engine saved!")
else:
    print("Engine build failed!")
```

## 4. TensorRT 추론

### 4.1 엔진 로드 및 추론

```python
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import pycuda.driver as cuml

# TensorRT 로거
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

# 엔진 로드
with open('model.trt', 'rb') as f:
    engine_data = f.read()

# 런타임 생성
runtime = trt.Runtime(TRT_LOGGER)
engine = runtime.deserialize_cuda_engine(engine_data)

# 컨텍스트 생성
context = engine.create_execution_context()

# 입력/출력 allocator
inputs = []
outputs = []
bindings = []

for binding in engine.bindings:
    size = trt.volume(engine.get_binding_shape(binding)) * engine.max_batch_size
    dtype = trt.nptype(engine.get_binding_dtype(binding))

    # GPU 메모리 할당
    cuda_mem = cuda.mem_alloc(size * dtype().itemsize)
    bindings.append(int(cuda_mem))
    outputs.append(cuda_mem) if 'output' in binding.lower() else inputs.append(cuda_mem)

print(f"Input shape: {engine.get_binding_shape(0)}")
print(f"Output shape: {engine.get_binding_shape(1)}")

# 추론 함수
def infer(batch_input):
    # 입력 데이터를 GPU로 복사
    cuda.memcpy_htod(inputs[0], batch_input)

    # 추론 실행
    context.execute(batch_size=1, bindings=bindings)

    # 출력 데이터를 CPU로 복사
    output = np.empty(engine.get_binding_shape(1), dtype=np.float32)
    cuda.memcpy_dtoh(output, outputs[0])

    return output

# 테스트
batch_input = np.random.randn(1, 3, 32, 32).astype(np.float32)
output = infer(batch_input)
print(f"Output shape: {output.shape}")
print(f"Output sample: {output[0][:5]}")
```

### 4.2 TensorRT Python API简化

```python
import torch2trt

# PyTorch 모델에서 직접 TensorRT 변환
model = SimpleModel().eval().cuda()

# 더미 입력
x = torch.randn(1, 3, 32, 32).cuda()

# 변환
model_trt = torch2trt.convert(
    model,
    [x],
    fp16_mode=True,
    max_workspace_size=1 << 30
)

# 추론 테스트
output = model_trt(x)
print(f"TensorRT output: {output.shape}")

# 저장
torch.save(model_trt.state_dict(), 'model_trt.pth')
```

## 5. YOLOv5 TensorRT 변환

### 5.1 YOLOv5 설치 및 모델 로드

```bash
# YOLOv5 클론
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip3 install -r requirements.txt
```

### 5.2 YOLOv5 → ONNX

```python
import torch

# YOLOv5s 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = model.eval()

# 추론 위한 더미 입력
x = torch.randn(1, 3, 640, 640)

# ONNX로 변환
torch.onnx.export(
    model,
    x,
    'yolov5s.onnx',
    opset_version=11,
    input_names=['images'],
    output_names=['output'],
    dynamic_axes={'images': {0: 'batch'}}
)

print("YOLOv5 ONNX model saved!")
```

### 5.3 TensorRT 변환 (YOLOv5 전용)

```bash
# tensort 설치
pip3 install tensorrt

# Python으로 TensorRT 변환
python3 << 'EOF'
import tensorrt as trt
import pycuda.driver as cuda
import numpy as np

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

def build_yolov5_engine():
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(1)
    config = builder.create_builder_config()
    parser = trt.OnnxParser(network, TRT_LOGGER)

    with open('yolov5s.onnx', 'rb') as f:
        parser.parse(f.read())

    config.max_workspace_size = 1 << 30
    builder.max_batch_size = 1

    if builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)

    return builder.build_serialized_network(network, config)

engine = build_yolov5_engine()
with open('yolov5s.trt', 'wb') as f:
    f.write(engine)
print("YOLOv5 TensorRT model saved!")
EOF
```

### 5.4 YOLOv5 TensorRT 추론

```python
import tensorrt as trt
import cv2
import numpy as np
import pycuda.driver as cuda

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)

# 엔진 로드
with open('yolov5s.trt', 'rb') as f:
    engine_data = f.read()

runtime = trt.Runtime(TRT_LOGGER)
engine = runtime.deserialize_cuda_engine(engine_data)
context = engine.create_execution_context()

# 입력 크기
INPUT_H, INPUT_W = 640, 640

def preprocess_image(image):
    """이미지 전처리"""
    img = cv2.resize(image, (INPUT_W, INPUT_H))
    img = img.astype(np.float32) / 255.0
    img = img.transpose(2, 0, 1)
    img = np.expand_dims(img, axis=0)
    return img

def detect_image(image_path):
    """객체 탐지"""
    # 이미지 로드
    img = cv2.imread(image_path)
    orig_h, orig_w = img.shape[:2]

    # 전처리
    input_data = preprocess_image(img)

    # GPU 메모리 할당
    d_input = cuda.mem_alloc(input_data.nbytes)
    d_output = cuda.mem_alloc(1 * 85 * 25200 * 4)  # 예시 크기

    # 메모리 복사 및 추론
    cuda.memcpy_htod(d_input, input_data)
    context.execute_v2([int(d_input), int(d_output)])

    # 결과 복사
    output = np.empty((1, 85, 25200), dtype=np.float32)
    cuda.memcpy_dtoh(output, d_output)

    return output

# 테스트
output = detect_image('data/images/bus.jpg')
print(f"Output shape: {output.shape}")
```

## 6. TensorRT 최적화 기법

### 6.1 INT8 양자화

```python
# INT8 양자화 calibartor
class INT8Calibrator(trt.IInt8Calibrator):
    def __init__(self, data_loader):
        super().__init__()
        self.data_loader = data_loader
        self.input_shape = (1, 3, 640, 640)

    def get_batch(self, names):
        batch = next(self.data_loader)
        cuda.memcpy_htod(self.d_input, batch)
        return [int(self.d_input)]

    def get_batch_size(self):
        return self.input_shape[0]

    def read_calibration_cache(self):
        return None

    def write_calibration_cache(self, cache):
        pass

# INT8 엔진 빌드
config.set_flag(trt.BuilderFlag.INT8)
config.int8_calibrator = calibrator
```

### 6.2 FP16 최적화

```python
# FP16 활성화
config.set_flag(trt.BuilderFlag.FP16)

# Mixed precision (일부 레이어만 FP16)
config.set_layer_precision(layer, trt.float16)
```

### 6.3 Profiling

```python
# TensorRT Profiler 사용
profiler = trt.Profiler()
context.profiler = profiler

# 추론 실행
context.execute_v2(bindings)

# 결과 분석
print("Layer timings:")
for layer_name, time_ms in profiler.get_layer_time():
    print(f"{layer_name}: {time_ms:.2f}ms")
```

## 7. Jetson에서 TensorRT

### 7.1 Jetson Nano 최적화

```bash
# 성능 모드 설정
sudo nvpmodel -m 0
sudo jetson_clocks

# TensorRT 추론 테스트
cd /usr/src/tensorrt/bin
./trtexec --onnx=yolov5s.onnx --saveEngine=yolov5s.trt
```

### 7.2 Jetson TensorRT 실시간 추론

```python
import cv2
import tensorrt as trt
import numpy as np

# Jetson에서 웹캠 추론
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# TensorRT 엔진 로드
engine = load_engine('yolov5s.trt')
context = engine.create_execution_context()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 전처리
    input_data = preprocess(frame)

    # 추론
    output = infer(context, input_data)

    # 후처리 및 시각화
    results = postprocess(output)
    frame = draw_results(frame, results)

    cv2.imshow('TensorRT Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 8. 실습 과제

1. PyTorch 모델을 ONNX로 변환하세요.
2. ONNX 모델을 TensorRT 엔진으로 변환하세요.
3. YOLOv5 모델을 TensorRT로 변환하고 추론하세요.
4. Jetson Nano에서 TensorRT 추론 속도를 측정하세요.
5. FP16과 INT8 성능을 비교하세요.

## 9. 다음 실습 예고

다음 클래스에서는 Mediapipe 실습을 진행합니다.