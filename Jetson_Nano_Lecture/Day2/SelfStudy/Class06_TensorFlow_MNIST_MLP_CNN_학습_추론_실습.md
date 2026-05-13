# Class 06: TensorFlow MNIST MLP/CNN 학습 추론 실습

## 1. MNIST 데이터셋 소개

### 1.1 데이터셋 개요

MNIST는 필기체 숫자(0-9) 이미지 데이터셋입니다. 머신러닝의 "Hello World"로 널리 사용됩니다.

- **훈련 데이터**: 60,000개 이미지
- **테스트 데이터**: 10,000개 이미지
- **이미지 크기**: 28x28 픽셀
- **레이블**: 0-9 (10개 클래스)
- **포맷**: 그레이스케일 (1채널)

### 1.2 데이터 구조

```
MNIST Structure:
┌─────────────────┐
│ 28x28 Image     │
│ ┌─────────────┐ │
│ │ 5           │ │
│ │   ┌───┐     │ │
│ │   │3  │     │ │
│ │   └───┘     │ │
│ │     8       │ │
│ └─────────────┘ │
└─────────────────┘
→ Label: 5
```

## 2. TensorFlow에서 MNIST 로드

### 2.1 데이터 로드

```python
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# MNIST 데이터 로드
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# 데이터 정보 확인
print("Training data shape:", x_train.shape)
print("Training labels shape:", y_train.shape)
print("Test data shape:", x_test.shape)
print("Test labels shape:", y_test.shape)
print("Pixel value range:", x_train.min(), "-", x_train.max())
```

### 2.2 데이터 전처리

```python
# 정규화: 0-255 → 0-1
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# 데이터 shape 조정 (通道数 추가)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

print("Reshaped training data:", x_train.shape)
print("Reshaped test data:", x_test.shape)

# 레이블을 categorical로 변환
num_classes = 10
y_train_cat = keras.utils.to_categorical(y_train, num_classes)
y_test_cat = keras.utils.to_categorical(y_test, num_classes)

print("Categorical labels shape:", y_train_cat.shape)
```

### 2.3 데이터 시각화

```python
# 이미지 샘플 시각화
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.imshow(x_train[i].reshape(28, 28), cmap='gray')
    plt.title(f'Label: {y_train[i]}')
    plt.axis('off')
plt.tight_layout()
plt.show()
```

## 3. MLP (Multi-Layer Perceptron) 모델

### 3.1 모델 정의

```python
# MLP 모델 정의
def create_mlp_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(512, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation='softmax')
    ])
    return model

model_mlp = create_mlp_model()
model_mlp.summary()
```

### 3.2 모델 컴파일

```python
model_mlp.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
```

### 3.3 모델 학습

```python
# MLP 모델 학습
history_mlp = model_mlp.fit(
    x_train, y_train_cat,
    epochs=10,
    batch_size=128,
    validation_split=0.2,
    verbose=1
)
```

### 3.4 학습 결과 시각화

```python
# Loss 및 Accuracy 그래프
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Loss 그래프
axes[0].plot(history_mlp.history['loss'], label='Train Loss')
axes[0].plot(history_mlp.history['val_loss'], label='Val Loss')
axes[0].set_title('MLP Model Loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].legend()

# Accuracy 그래프
axes[1].plot(history_mlp.history['accuracy'], label='Train Acc')
axes[1].plot(history_mlp.history['val_accuracy'], label='Val Acc')
axes[1].set_title('MLP Model Accuracy')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].legend()

plt.tight_layout()
plt.show()
```

## 4. CNN (Convolutional Neural Network) 모델

### 4.1 모델 정의

```python
# CNN 모델 정의
def create_cnn_model():
    model = keras.Sequential([
        # Conv Block 1
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        
        # Conv Block 2
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        
        # Conv Block 3
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        
        # Dense layers
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation='softmax')
    ])
    return model

model_cnn = create_cnn_model()
model_cnn.summary()
```

### 4.2 모델 컴파일 및 학습

```python
model_cnn.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# CNN 모델 학습
history_cnn = model_cnn.fit(
    x_train, y_train_cat,
    epochs=10,
    batch_size=128,
    validation_split=0.2,
    verbose=1
)
```

### 4.3 CNN 학습 결과 비교

```python
# MLP vs CNN 성능 비교
print("=" * 50)
print("Model Performance Comparison")
print("=" * 50)
print(f"MLP Final Train Accuracy: {history_mlp.history['accuracy'][-1]:.4f}")
print(f"MLP Final Val Accuracy: {history_mlp.history['val_accuracy'][-1]:.4f}")
print(f"CNN Final Train Accuracy: {history_cnn.history['accuracy'][-1]:.4f}")
print(f"CNN Final Val Accuracy: {history_cnn.history['val_accuracy'][-1]:.4f}")
```

## 5. 모델 평가

### 5.1 테스트 데이터 평가

```python
# MLP 모델 평가
mlp_loss, mlp_acc = model_mlp.evaluate(x_test, y_test_cat, verbose=2)
print(f"\nMLP Test Loss: {mlp_loss:.4f}")
print(f"MLP Test Accuracy: {mlp_acc:.4f}")

# CNN 모델 평가
cnn_loss, cnn_acc = model_cnn.evaluate(x_test, y_test_cat, verbose=2)
print(f"\nCNN Test Loss: {cnn_loss:.4f}")
print(f"CNN Test Accuracy: {cnn_acc:.4f}")
```

### 5.2 예측 결과 시각화

```python
# CNN 모델 예측
predictions = model_cnn.predict(x_test)

# 예측 결과 시각화
plt.figure(figsize=(12, 8))
for i in range(15):
    plt.subplot(3, 5, i+1)
    plt.imshow(x_test[i].reshape(28, 28), cmap='gray')
    true_label = y_test[i]
    pred_label = np.argmax(predictions[i])
    color = 'green' if true_label == pred_label else 'red'
    plt.title(f'True: {true_label}, Pred: {pred_label}', color=color)
    plt.axis('off')
plt.tight_layout()
plt.show()
```

### 5.3 Confusion Matrix

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Confusion Matrix 계산
y_pred = np.argmax(predictions, axis=1)
cm = confusion_matrix(y_test, y_pred)

# 시각화
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('CNN Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
```

## 6. 모델 추론

### 6.1 단일 이미지 추론

```python
# 단일 이미지 추론
def predict_digit(model, image):
    image = image.reshape(1, 28, 28, 1)
    image = image.astype('float32') / 255.0
    prediction = model.predict(image)
    digit = np.argmax(prediction)
    confidence = prediction[0][digit]
    return digit, confidence

# 테스트 이미지 중 하나 선택
test_image = x_test[0]
digit, confidence = predict_digit(model_cnn, test_image)
print(f"Predicted Digit: {digit}")
print(f"Confidence: {confidence:.4f}")
plt.imshow(test_image.reshape(28, 28), cmap='gray')
plt.title(f'Prediction: {digit} ({confidence:.2%})')
plt.show()
```

### 6.2 외부 이미지 추론

```python
from PIL import Image

# 외부 이미지 로드 및 전처리
def load_and_preprocess_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.resize((28, 28))
    img_array = np.array(img)
    img_array = img_array.reshape(1, 28, 28, 1)
    img_array = img_array.astype('float32') / 255.0
    return img_array

# 추론 실행 (외부 이미지 파일이 있는 경우)
# img = load_and_preprocess_image('my_digit.png')
# pred = model_cnn.predict(img)
# print(f"Predicted: {np.argmax(pred)}")
```

## 7. 모델 저장 및 로드

### 7.1 SavedModel 형식

```python
# 모델 저장
model_cnn.save('mnist_cnn_model.h5')

# 모델 로드
loaded_model = keras.models.load_model('mnist_cnn_model.h5')

# 로드된 모델로 추론
predictions_loaded = loaded_model.predict(x_test)
print("Model loaded and predictions match:", np.allclose(predictions, predictions_loaded))
```

### 7.2 TensorFlow Lite 변환

```python
# TFLite 변환
converter = tf.lite.TFLiteConverter.from_keras_model(model_cnn)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_model = converter.convert()

# 저장
with open('mnist_cnn.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite model saved!")

# TFLite 모델 추론
interpreter = tf.lite.Interpreter(model_path='mnist_cnn.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']

# 단일 이미지 추론
interpreter.set_tensor(input_index, x_test[0:1])
interpreter.invoke()
tflite_pred = interpreter.get_tensor(output_index)
print(f"TFLite Prediction: {np.argmax(tflite_pred)}")
```

## 8. Jetson에서 최적화

### 8.1 GPU 메모리 관리

```python
# GPU 메모리 성장 설정
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)
```

### 8.2 배치 크기 최적화

```python
# Jetson Nano에 적합한 배치 크기
BATCH_SIZE = 64  # Jetson Nano에서는 32-64 권장

model_cnn.fit(
    x_train, y_train_cat,
    epochs=5,
    batch_size=BATCH_SIZE,
    validation_data=(x_test, y_test_cat)
)
```

## 9. 실습 과제

1. MNIST 데이터를 로드하고 전처리하세요.
2. MLP 모델을 구축하고 학습시키세요.
3. CNN 모델을 구축하고 학습시키세요.
4. 두 모델의 성능을 비교하세요.
5. TensorFlow Lite 모델로 변환하세요.

## 10. 다음 실습 예고

다음 클래스에서는 Darknet, PyTorch, TensorRT에 대한 소개와 Darknet 실습을 진행합니다.