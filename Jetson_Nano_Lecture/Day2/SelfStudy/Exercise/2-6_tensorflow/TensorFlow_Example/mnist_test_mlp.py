import cv2
import numpy as np
import os 
import tensorflow as tf

# 1. CUDA를 사용하지 않도록 설정
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import matplotlib.pyplot as plt

from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical

'''
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)
'''

# 2. MNIST 데이터셋 로드 및 데이터셋 슬라이싱(Jetson Nano의 메모리 부족 이유) 
(t_train_images, t_train_labels), (t_test_images, t_test_labels) = mnist.load_data()
train_images = t_train_images[:20000]   # 60,000개 학습 이미지 데이터셋 중 20,000개 사용 
test_images = t_test_images[:3200]      # 10,000개 테스트 이미지 데이터셋 중 3,200개 사용 

print("원래 학습 데이터셋 이미지 수: %d" % (t_train_images.shape[0]))
print("원래 테스트 데이터셋 이미지 수: {}" .format(t_test_images.shape[0]))
print("")
print("학습 데이터셋 이미지 수: %d" % (train_images.shape[0]))
print("테스트 데이터셋 이미지 수: {}" .format(test_images.shape[0]))

# 3. 첫번째 데이터 이미지 확인 
#plt.imshow(train_images[0], cmap='Greys')
#plt.show()

# 4. 데이터셋 이미지 1차원 벡터화 및 정규화
train_images = train_images.reshape((train_images.shape[0], 784)).astype('float32') / 255
test_images = test_images.reshape((test_images.shape[0], 784)).astype('float32') / 255

# 5. 학습 및 테스트 레이블 데이터셋 원-핫 인코딩   
train_labels = t_train_labels[:20000]
test_labels = t_test_labels[:3200]
train_labels = to_categorical(train_labels, 10)
test_labels = to_categorical(test_labels, 10)


# 6. 모델 네트워크 구성 (MLP만 사용)
model = models.Sequential([
    layers.Dense(512, activation='relu', input_shape=(784,)),
    layers.Dense(256, activation='relu'),
    layers.Dense(10, activation='softmax')
])


# 7. 모델 컴파일
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# 8. 이미 학습이 되어 가중치 파일이 저장되어 있으면 가중치 파일 로드 
try:
    model.load_weights("mnist_mlp_weights.h5")
# 9. 학습되지 않아 가중치 파일이 없다면 학습진행. 
except:
    model.fit(train_images, train_labels, epochs=5, batch_size=1)
    model.save_weights("mnist_mlp_weights.h5")

# 10. 카메라 설정
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

while True:
# 11. 카메라 영상 이미지 read
    ret, frame = cap.read()
    if not ret:
        break

# 12. 이미지 흑백 변환 및 크기 조정
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
    (thresh, gray) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    resized = cv2.resize(gray, (28, 28))
# 13. 이미지 데이터 직렬화(Flattening) 및 정규화(Normalization) For MLP
    input_img = resized.reshape((1, 784)).astype('float32') / 255

# 14. 모델에 이미지 데이터를 입력하여 추론 
    prediction = model.predict(input_img)
# 15. 추론 결과 분류 
    digit = np.argmax(prediction)

# 16. 결과 표시
    cv2.putText(frame, str(digit), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('MNIST Digit Recognition', frame)
    #cv2.imshow('resized', resized)

# 17. ‘q’키가 눌려지면 while문 종료 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 18. Camera 캡쳐 종료 및 OpenCV 해제 
cap.release()
cv2.destroyAllWindows()


