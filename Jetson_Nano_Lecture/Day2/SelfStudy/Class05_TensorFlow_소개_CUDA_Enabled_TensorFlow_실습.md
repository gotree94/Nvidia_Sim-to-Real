# Class 05: TensorFlow 소개 및 CUDA Enabled TensorFlow 실습

## 1. TensorFlow 개요

### 1.1 TensorFlow란?

TensorFlow는 Google에서 개발한 오픈소스 머신러닝 프레임워크입니다. 2015년에 공개되었으며, 딥러닝 연구와 프로덕션 환경에서 널리 사용됩니다.

### 1.2 주요 특징

- **Flexible Architecture**: 다양한 플랫폼 지원
- **Eager Execution**: 즉시 실행 모드
- **TensorBoard**: 시각화 도구
- **TensorFlow Lite**: 모바일/임베디드 지원
- **TensorFlow.js**: 브라우저 기반 실행
- **Distributed Training**: 분산 학습 지원

### 1.3 TensorFlow 버전

```bash
# Python에서 TensorFlow 버전 확인
import tensorflow as tf
print(tf.__version__)

# TensorFlow 2.x 주요 변경사항
# - Eager Execution이 기본 활성화
# - Keras가 공식 API로 통합
# - Session 제거
```

## 2. TensorFlow 아키텍처

### 2.1 계층 구조

```
┌─────────────────────────────────────────┐
│           High Level API               │
│    (Keras, TF-Slim, Estimator)         │
├─────────────────────────────────────────┤
│           Core Runtime                  │
│    (Graph execution, AutoDiff)          │
├─────────────────────────────────────────┤
│           Backend Engines              │
│    (CPU, GPU, TPU)                      │
├─────────────────────────────────────────┤
│           Low Level Operations         │
│    (Tensor operations, kernels)         │
└─────────────────────────────────────────┘
```

### 2.2 데이터플로우 그래프

```
TensorFlow Execution:
  
  Build Graph          Execute Graph
       │                    │
       ▼                    ▼
  ┌─────────┐         ┌─────────┐
  │  Node   │────────▶│ Tensor  │
  │  (Op)   │         │  Flow   │
  └─────────┘         └─────────┘
```

## 3. CUDA 지원 TensorFlow

### 3.1 GPU 지원 확인

```python
import tensorflow as tf

# GPU 사용 가능 여부 확인
print("GPU 사용 가능:", tf.config.list_physical_devices('GPU'))

# CUDA 版本 확인
print("CUDA 버전:", tf.config.list_physical_devices('GPU'))

# GPU 메모리 성장 설정
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU 메모리 성장 설정 완료")
    except RuntimeError as e:
        print(e)
```

### 3.2 GPU device 확인

```python
# TensorFlow가 사용하는 디바이스 확인
tf.debugging.set_log_device_placement(True)

# 간단한 연산으로 GPU 사용 확인
a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[1.0, 1.0], [1.0, 1.0]])
result = a + b
print(result)
```

### 3.3 GPU 메모리 관리

```python
# 방법 1: 필요한 만큼의 메모리만 사용
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.set_logical_device_configuration(
        gpus[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=1024)]
    )

# 방법 2: 단일 GPU 메모리 사용량 제한
tf.config.experimental.set_virtual_device_configuration(
    gpus[0],
    [tf.config.VirtualDeviceConfiguration(memory_limit=2048)]
)
```

## 4. TensorFlow 실습

### 4.1 기본 연산

```python
import tensorflow as tf
import numpy as np

# Tensor 생성
tensor = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
print("Tensor:", tensor)
print("Shape:", tensor.shape)
print("Dtype:", tensor.dtype)

# numpy 배열から tensor 생성
numpy_array = np.array([[1, 2, 3], [4, 5, 6]])
tensor_from_np = tf.constant(numpy_array, dtype=tf.float32)

# 난수 생성
random_tensor = tf.random.normal(shape=(3, 3), mean=0, stddev=1)
zeros_tensor = tf.zeros((3, 3))
ones_tensor = tf.ones((3, 3))
```

### 4.2 연산

```python
a = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)
b = tf.constant([[5, 6], [7, 8]], dtype=tf.float32)

# 기본 연산
print("a + b:", tf.add(a, b))
print("a - b:", tf.subtract(a, b))
print("a * b:", tf.multiply(a, b))
print("a / b:", tf.divide(a, b))

# 행렬 곱셈
result = tf.matmul(a, b)
print("Matrix multiplication:", result)
```

### 4.3 자동 미분

```python
# Gradient 계산
x = tf.Variable(3.0)

with tf.GradientTape() as tape:
    y = x ** 2

# dy/dx = 2x = 6
grad = tape.gradient(y, x)
print("Gradient:", grad.numpy())

# 다중 변수 Gradient
w = tf.Variable(tf.random.normal((3, 2)))
b = tf.Variable(tf.zeros(2))

with tf.GradientTape() as tape:
    y = tf.matmul(w, tf.constant([[1], [2], [3]], dtype=tf.float32)) + b
    loss = tf.reduce_mean(y ** 2)

grads = tape.gradient(loss, [w, b])
print("w gradient:", grads[0])
print("b gradient:", grads[1])
```

## 5. Keras를 사용한 모델 구축

### 5.1 Sequential API

```python
from tensorflow.keras import layers, models

# Sequential 모델 생성
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.summary()
```

### 5.2 Functional API

```python
# Functional API로 더 유연한 모델 구축
inputs = layers.Input(shape=(28, 28, 1))
x = layers.Conv2D(32, (3, 3), activation='relu')(inputs)
x = layers.MaxPooling2D((2, 2))(x)
x = layers.Conv2D(64, (3, 3), activation='relu')(x)
x = layers.Flatten()(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = models.Model(inputs=inputs, outputs=outputs)
model.summary()
```

### 5.3 서브클래싱

```python
class MyModel(models.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.conv1 = layers.Conv2D(32, (3, 3), activation='relu')
        self.pool = layers.MaxPooling2D((2, 2))
        self.conv2 = layers.Conv2D(64, (3, 3), activation='relu')
        self.flatten = layers.Flatten()
        self.dense1 = layers.Dense(64, activation='relu')
        self.dense2 = layers.Dense(10, activation='softmax')

    def call(self, x):
        x = self.pool(self.conv1(x))
        x = self.pool(self.conv2(x))
        x = self.flatten(x)
        x = self.dense1(x)
        return self.dense2(x)

model = MyModel()
```

## 6. 데이터 로드 및 전처리

### 6.1 tf.data.Dataset

```python
# Dataset from tensor
x = tf.random.normal((1000, 28, 28, 1))
y = tf.random.randint(0, 10, (1000,))

dataset = tf.data.Dataset.from_tensor_slices((x, y))
dataset = dataset.shuffle(1000)
dataset = dataset.batch(32)

# Dataset 전처리 파이프라인
dataset = dataset.map(lambda x, y: (x / 255.0, y))
dataset = dataset.prefetch(tf.data.AUTOTUNE)
```

### 6.2 이미지 전처리

```python
# ImageDataGenerator (Legacy)
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# flow_from_directory 사용
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    'train_directory',
    target_size=(150, 150),
    batch_size=32,
    class_mode='binary'
)
```

## 7. GPU에서 학습

### 7.1 모델 컴파일

```python
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
```

### 7.2 모델 학습

```python
# GPU를 사용한 학습
history = model.fit(
    train_dataset,
    epochs=10,
    validation_data=val_dataset,
    callbacks=[
        tf.keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True),
        tf.keras.callbacks.EarlyStopping(patience=3),
        tf.keras.callbacks.TensorBoard(log_dir='./logs')
    ]
)
```

### 7.3 GPU 활용 모니터링

```python
# GPU 메모리 사용량 확인
import gc

# Keras/backend 세션 초기화
tf.keras.backend.clear_session()

# Mixed precision ( Volta 이상 GPU )
from tensorflow.keras import mixed_precision
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)
```

## 8. TensorFlow Lite 변환

### 8.1 SavedModel로 변환

```python
model.save('saved_model/my_model')
loaded_model = tf.keras.models.load_model('saved_model/my_model')
```

### 8.2 TFLite 변환

```python
converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# 양자화
converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite 모델 변환 완료")
```

## 9. Jetson에서 TensorFlow

### 9.1 Jetson용 TensorFlow 설치

```bash
# JetPack과 호환되는 TensorFlow 설치
pip3 install tensorflow

# TensorFlow-gpu (CUDA 지원)
pip3 install tensorflow-gpu
```

### 9.2 Jetson에서 GPU 확인

```python
# Jetson-specific 확인
import tensorflow as tf
print("Built with CUDA:", tf.test.is_built_with_cuda())
print("GPU available:", tf.config.list_physical_devices('GPU'))

# TF-TRT (TensorRT) 최적화
from tensorflow.python.compiler.tensorrt import trt_convert as trt
```

## 10. 실습 과제

1. TensorFlow에서 GPU가 정상적으로 인식되는지 확인하세요.
2. Keras Sequential API로 간단한 모델을 구축하세요.
3. tf.data.Dataset을 사용하여 데이터 파이프라인을 구축하세요.
4. TensorFlow Lite 모델로 변환하세요.

## 11. 다음 실습 예고

다음 클래스에서는 TensorFlow로 MNIST 데이터를 사용한 MLP와 CNN 학습 추론 실습을 진행합니다.