# Class 02: Mediapipe 소개 및 실습

## 1. Mediapipe란?

### 1.1 개요

MediaPipe는 Google에서 개발한 프레임워크로, 실시간 미디어 처리 파이프라인을 위한高效적인 솔루션입니다. 얼굴 인식, 손 추적, 포즈 추정을 포함한 다양한 컴퓨터 비전 작업을 지원합니다.

### 1.2 주요 특징

- **Cross-platform**: Android, iOS, Web, Linux, Jetson 지원
- **Real-time**: 실시간 처리 최적화
- **Lightweight**: 경량화되어 임베디드 시스템에 적합
- **Modular**: 모듈식 구조로 필요한 솔루션만 선택 가능
- **GPU Acceleration**: GPU 가속 지원

### 1.3 지원 솔루션

```
MediaPipe Solutions:
┌─────────────────────────────────────┐
│           Face Mesh                  │
│   468개 얼굴 랜드마크 추적            │
├─────────────────────────────────────┤
│           Hands                     │
│   손 형태 및 제스처 인식              │
├─────────────────────────────────────┤
│           Pose                      │
│  全身 포즈 추정 (33개 랜드마크)       │
├─────────────────────────────────────┤
│           Objectron                  │
│   3D 객체 탐지 및 추적               │
├─────────────────────────────────────┤
│           Selfie Segmentation       │
│   실시간 배경 분리                   │
└─────────────────────────────────────┘
```

## 2. Jetson에 Mediapipe 설치

### 2.1 Python 의존성 설치

```bash
# 기본 의존성
pip3 install opencv-python
pip3 install pillow
pip3 install numpy

# Mediapipe 설치
pip3 install mediapipe
```

### 2.2 Jetson 특화 설치

```bash
# JetPack 확인
cat /etc/nv_tegra_release

# Python 버전 확인
python3 --version

# ARM64용 Mediapipe 설치
pip3 install mediapipe --extra-index-url https://pypi.nvidia.com

#或者是直接从源码安装
# git clone https://github.com/google/mediapipe.git
# cd mediapipe
# bazel build --copt=-DMESA_EGL_NO_X11-headless //mediapipe/python:mediapipe
```

### 2.3 설치 확인

```bash
# Mediapipe 버전 확인
python3 -c "import mediapipe; print(mediapipe.__version__)"

# GPU 지원 확인
python3 -c "
import mediapipe as mp
print('MediaPipe version:', mp.__version__)
print('GPU available:', hasattr(mp, 'gpu'))
"
```

## 3. MediaPipe 기본 사용

### 3.1 이미지 처리 파이프라인

```python
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 솔루션 초기화
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# 이미지 파일 로드
image = cv2.imread('test.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# MediaPipe로 처리
with mp_holistic.Holistic(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True
) as holistic:
    results = holistic.process(image)

# 결과 시각화
annotated_image = image.copy()
if results.face_landmarks:
    mp_drawing.draw_landmarks(
        annotated_image,
        results.face_landmarks,
        mp_holistic.FACE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
    )

# 이미지 저장
annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
cv2.imwrite('output.jpg', annotated_image)
```

### 3.2 비디오 처리

```python
import cv2
import mediapipe as mp

# 비디오 캡처
cap = cv2.VideoCapture('video.mp4')

# MediaPipe Hands 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # MediaPipe 처리
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # 결과 시각화
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow('MediaPipe', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 3.3 웹캠 실시간 처리

```python
import cv2
import mediapipe as mp

# 웹캠 열기
cap = cv2.VideoCapture(0)

# MediaPipe Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("웹캠을 열 수 없습니다.")
        break

    # MediaPipe 처리
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # 포즈 랜드마크 그리기
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow('MediaPipe Pose', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 4. MediaPipe 솔루션 상세

### 4.1 Face Detection

```python
import mediapipe as mp

# Face Detection 초기화
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(
    model_selection=0,  # 0: short-range, 1: long-range
    min_detection_confidence=0.5
)

# 처리
results = face_detection.process(frame_rgb)

# 결과 사용
if results.detections:
    for detection in results.detections:
        # 신뢰도
        confidence = detection.score[0]
        # 바운딩 박스
        bbox = detection.location_data.relative_bounding_box
```

### 4.2 Face Mesh

```python
import mediapipe as mp

# Face Mesh 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 랜드마크 인덱스
LEFT_EYE = 33
RIGHT_EYE = 263
NOSE_TIP = 1

# 처리
results = face_mesh.process(frame_rgb)

if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        # 특정 랜드마크 접근
        nose = face_landmarks.landmark[NOSE_TIP]
        print(f"Nose: ({nose.x}, {nose.y})")
```

### 4.3 Hands

```python
import mediapipe as mp

# Hands 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 랜드마크 인덱스
WRIST = 0
THUMB_TIP = 4
INDEX_TIP = 8

# 처리
results = hands.process(frame_rgb)

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        # 랜드마크 접근
        thumb_tip = hand_landmarks.landmark[THUMB_TIP]
        print(f"Thumb tip: ({thumb_tip.x}, {thumb_tip.y}, {thumb_tip.z})")
```

### 4.4 Pose

```python
import mediapipe as mp

# Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 중요 랜드마크 인덱스
NOSE = 0
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_HIP = 23
RIGHT_HIP = 24

# 처리
results = pose.process(frame_rgb)

if results.pose_landmarks:
    left_shoulder = results.pose_landmarks.landmark[LEFT_SHOULDER]
    print(f"Left shoulder: ({left_shoulder.x}, {left_shoulder.y})")
```

## 5. MediaPipe 시각화 유틸리티

### 5.1 커스텀 그리기 함수

```python
import cv2
import mediapipe as mp
import numpy as np

def draw_landmarks(image, landmarks, connections=None):
    """커스텀 랜드마크 그리기"""
    h, w, c = image.shape

    for landmark in landmarks:
        x, y = int(landmark.x * w), int(landmark.y * h)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    if connections:
        for connection in connections:
            start = landmarks[connection[0]]
            end = landmarks[connection[1]]
            start_x, start_y = int(start.x * w), int(start.y * h)
            end_x, end_y = int(end.x * w), int(end.y * h)
            cv2.line(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

    return image
```

### 5.2 랜드마크 위치 계산

```python
def calculate_distance(p1, p2):
    """두 랜드마크 간 거리 계산"""
    return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def calculate_angle(p1, p2, p3):
    """세 점 간 각도 계산 (도)"""
    p1 = np.array([p1.x, p1.y])
    p2 = np.array([p2.x, p2.y])
    p3 = np.array([p3.x, p3.y])

    v1 = p1 - p2
    v2 = p3 - p2

    angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    return np.degrees(angle)
```

### 5.3 성능 측정

```python
import time
import cv2

class FPSCounter:
    """FPS 측정 클래스"""
    def __init__(self):
        self.start_time = None
        self.frame_count = 0
        self.fps = 0

    def start(self):
        self.start_time = time.time()
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        elapsed = time.time() - self.start_time
        self.fps = self.frame_count / elapsed
        return self.fps

    def draw(self, frame):
        cv2.putText(
            frame,
            f"FPS: {self.fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )
        return frame
```

## 6. MediaPipe + ROS 연동

### 6.1 이미지 토픽 구독

```python
import rospy
from sensor_msgs.msg import Image
import mediapipe as mp
import cv2
import numpy as np

def image_callback(msg):
    # ROS Image를 OpenCV로 변환
    np_arr = np.frombuffer(msg.data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # MediaPipe 처리
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # 처리 결과 사용
    # ...

rospy.init_node('mediapipe_node')
rospy.Subscriber('/camera/image_raw', Image, image_callback)
rospy.spin()
```

## 7. 실습 과제

1. Mediapipe를 Jetson Nano에 설치하세요.
2. 웹캠에서 실시간 핸드 트래킹을 실행하세요.
3. 포즈 추정 결과를 화면에 표시하세요.
4. FPS를 측정하고 최적화하세요.
5. ROS 토픽과 연동하세요.

## 8. 다음 실습 예고

다음 클래스에서는 Mediapipe 얼굴 인식 실습을 진행합니다.