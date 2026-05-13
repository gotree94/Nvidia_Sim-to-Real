# Class 02: TensorFlow 소개 및 CUDA Enabled TensorFlow 실습

## 1. TensorFlow 개요

### 1.1 TensorFlow 정의

TensorFlow는 Google Brain 팀이 개발한 오픈소스 머신러닝 프레임워크입니다.

```
TensorFlow 구성 요소:
┌─────────────────────────────────────┐
│              Tensor                │
│  (다차원 배열, 데이터 표현 단위)    │
├─────────────────────────────────────┤
│              Operation             │
│  (덧셈, 곱셈, Convolution 등)      │
├─────────────────────────────────────┤
│              Graph                 │
│  (Tensor와 Operation의 계산 흐름)  │
└─────────────────────────────────────┘
```

### 1.2 TensorFlow 버전 역사

| 버전 | 특징 |
|------|------|
| TF 1.x | Graph 모드, 세션 사용 |
| TF 2.x | Eager Execution 기본, Keras 통합 |
| TF 2.7+ | Jetson 최적화 버전 제공 |

### 1.3 Tensor 주요 구성

```python
import tensorflow as tf

# Rank (차원)에 따른 Tensor
rank_0 = tf.constant(3)                           # 스칼라 (0D)
rank_1 = tf.constant([1, 2, 3])                  # 벡터 (1D)
rank_2 = tf.constant([[1, 2], [3, 4]])          # 행렬 (2D)
rank_3 = tf.constant([[[1,2],[3,4]],[[5,6],[7,8]]]) # 텐서 (3D)

# Variable (학습 가능한 파라미터)
var = tf.Variable(tf.random.normal([3, 3]))

# Constant (고정값)
const = tf.constant([[1.0, 2.0], [3.0, 4.0]])
```

## 2. TensorFlow 아키텍처

### 2.1 계층 구조

```
TensorFlow Architecture:
┌─────────────────────────────────────┐
│    High Level API (Keras, TF-Slim) │
├─────────────────────────────────────┤
│         Core Runtime                │
│    (Graph 실행, AutoDiff)            │
├─────────────────────────────────────┤
│         Backend Engines             │
│    (CPU, GPU, TPU)                  │
├─────────────────────────────────────┤
│         Low Level Operations        │
│    (Tensor, Kernel)                  │
└─────────────────────────────────────┘
```

### 2.2 Graph 모드 vs Eager 모드

```python
# TensorFlow 1.x (Graph 모드)
sess = tf.Session()
result = sess.run(op, feed_dict={x: input_data})

# TensorFlow 2.x (Eager Execution - 기본)
result = op(x)  # 즉시 실행
```

## 3. CUDA 지원 TensorFlow

### 3.1 Jetson용 TensorFlow 설치

```bash
# JetPack version 확인
cat /etc/nv_tegra_release

# TensorFlow 설치 (NVIDIA 제공 버전)
sudo apt-get update
sudo apt-get install -y python3-pip

# TensorFlow GPU 버전 설치 (JP 4.6.1 기준)
wget https://developer.download.nvidia.com/compute/redist/jp/v461/tensorflow/tensorflow-2.7.0+nv22.1-cp36-cp36m-linux_aarch64.whl
pip3 install tensorflow-2.7.0+nv22.1-cp36-cp36m-linux_aarch64.whl
pip3 install numpy==1.19.4
```

### 3.2 GPU 사용 확인

```python
import tensorflow as tf

# GPU 사용 가능 여부 확인
print("GPU 사용 가능:", tf.config.list_physical_devices('GPU'))

# CUDA 버전 확인
print("CUDA built:", tf.test.is_built_with_cuda())

# GPU 메모리 성장 설정
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
```

### 3.3 GPU 연산 확인

```python
# 장치 할당 로깅 활성화
tf.debugging.set_log_device_placement(True)

# 간단한 연산으로 GPU 사용 확인
a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[1.0, 1.0], [1.0, 1.0]])
result = a + b

print(result)
# 실행 시 GPU에서 수행되었다는 로그 출력 확인
```

### 3.4 장치 수동 할당

```python
# 특정 장치에 할당
with tf.device('/GPU:0'):
    a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    b = tf.constant([[1.0, 1.0], [1.0, 1.0]])
    c = tf.matmul(a, b)

# CPU로 강제 할당
with tf.device('/CPU:0'):
    result = a + b
```

## 4. Keras를 사용한 모델 구축

### 4.1 Sequential API

```python
from tensorflow.keras import layers, models

# Sequential 모델 생성
model = models.Sequential([
    layers.Dense(512, activation='relu', input_shape=(784,)),
    layers.Dense(256, activation='relu'),
    layers.Dense(10, activation='softmax')
])

model.summary()
```

### 4.2 Functional API

```python
# Functional API로 더 유연한 모델 구축
inputs = layers.Input(shape=(784,))
x = layers.Dense(512, activation='relu')(inputs)
x = layers.Dense(256, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)

model = models.Model(inputs=inputs, outputs=outputs)
```

### 4.3 모델 컴파일 및 학습

```python
# 모델 컴파일
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 학습 실행
history = model.fit(
    train_images, train_labels,
    epochs=10,
    batch_size=32,
    validation_data=(test_images, test_labels)
)
```

## 5. TensorFlow Lite

### 5.1 모델 변환

```python
# SavedModel로 저장
model.save('saved_model/my_model')

# TFLite로 변환
converter = tf.lite.TFLiteConverter.from_saved_model('saved_model/my_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]

tflite_model = converter.convert()

# 저장
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite 모델 변환 완료")
```

### 5.2 TFLite 추론

```python
import tensorflow.lite as tflite

# Interpreter 생성
interpreter = tflite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

# 입력/출력 텐서 정보
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 추론
input_data = np.array(train_images[0:1], dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])
print("예측 결과:", output_data)
```

## 6. TensorFlow 모델 저장 방식

### 6.1 SavedModel (권장)

```python
# 모델 저장
model.save('my_model')

# 모델 로드
loaded_model = tf.keras.models.load_model('my_model')
```

### 6.2 HDF5 (.h5)

```python
# 가중치만 저장
model.save_weights('weights.h5')

# 전체 모델 저장
model.save('model.h5')

# 가중치 로드
model.load_weights('weights.h5')
```

### 6.3 Checkpoints

```python
# 학습 중 저장
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    'weights_{epoch:02d}.h5',
    save_weights_only=True
)

model.fit(X, y, callbacks=[checkpoint_callback])
```

## 7. Jetson에서 TensorFlow 최적화

### 7.1 Mixed Precision

```python
from tensorflow.keras import mixed_precision

# Mixed Precision 활성화 (Volta 이상 GPU)
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_global_policy(policy)
```

### 7.2 메모리 최적화

```python
# 필요한 만큼의 메모리만 사용
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.set_logical_device_configuration(
        gpus[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=2048)]
    )
```

## 8. 실습 과제

1. Jetson Nano에 TensorFlow GPU 버전을 설치하세요.
2. GPU가 인식되는지 확인하세요.
3. Keras로 간단한 MLP 모델을 구축하세요.
4. TFLite로 모델을 변환하세요.

## 9. 다음 실습 예고

다음 클래스에서는 MNIST 데이터셋으로 MLP/CNN 학습 및 추론 실습을 진행합니다.