# Class 03: Mediapipe 얼굴 인식 실습

## 1. Face Mesh 개요

### 1.1 Face Mesh란?

MediaPipe Face Mesh는 얼굴의 468개 랜드마크를 실시간으로 추적하는 솔루션입니다. 안면 인식, 표정 분석, 얼굴 추적 등 다양한 응용에 사용됩니다.

### 1.2 랜드마크 구조

```
Face Mesh 468 Landmark:
┌─────────────────────────────────────┐
│          0-4: 얼굴 윤곽              │
│          5-9: 눈周围                │
│         10-15: 얼굴 윤곽            │
│         16-21: 눈 주변              │
│         22-36: 코                   │
│         37-48: 눈                   │
│        48-60: 입술 위              │
│        61-68: 입술 아래            │
│       362-377: 오른쪽 눈           │
│       233-466: 전체 윤곽           │
└─────────────────────────────────────┘
```

### 1.3 주요 랜드마크 그룹

| 그룹 | 인덱스 범위 | 설명 |
|------|------------|------|
|眉毛 | 107-160 | 양쪽 눈썹 |
|눈 | 33-246 | 양쪽 눈 |
|코 | 1-35 | 코 전체 |
|입 | 13-332 | 입술 전체 |
|얼굴 윤곽 | 10-338 | 전체 윤곽 |

## 2. Face Mesh 기본 실습

### 2.1 이미지에서 얼굴 인식

```python
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Face Mesh 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# 이미지 로드
image = cv2.imread('face.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 얼굴 랜드마크 추출
results = face_mesh.process(image_rgb)

# 결과 시각화
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        # 랜드마크 그리기
        for landmark in face_landmarks:
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 1, (0, 255, 0), -1)

cv2.imwrite('face_mesh_output.jpg', image)
```

### 2.2 실시간 웹캠 얼굴 추적

```python
import cv2
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

# 웹캠 열기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # MediaPipe 처리
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    # 랜드마크 시각화
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style()
            )

    cv2.imshow('Face Mesh', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 3. 얼굴 특징점 분석

### 3.1 얼굴 방향 추정

```python
import cv2
import mediapipe as mp
import numpy as np

def get_face_orientation(landmarks, image_shape):
    """얼굴 방향 추정"""
    h, w = image_shape[:2]

    # 코 끝점
    nose_tip = landmarks[4]
    nose_x, nose_y = int(nose_tip.x * w), int(nose_tip.y * h)

    # 눈 중심점
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    eye_center_x = int((left_eye.x + right_eye.x) * w / 2)
    eye_center_y = int((left_eye.y + right_eye.y) * h / 2)

    # 얼굴 방향 계산
    dx = nose_x - eye_center_x
    dy = nose_y - eye_center_y

    # 각도 계산 (도)
    angle = np.arctan2(dy, dx) * 180 / np.pi

    # 상태 반환
    if angle > 15:
        direction = "Right"
    elif angle < -15:
        direction = "Left"
    else:
        direction = "Center"

    return direction, angle

# 사용
results = face_mesh.process(frame_rgb)
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        direction, angle = get_face_orientation(face_landmarks.landmark, frame.shape)
        print(f"Face direction: {direction} ({angle:.1f}°)")
```

### 3.2 눈 상태 감지

```python
def get_eye_state(landmarks, image_shape):
    """눈 상태 감지 (열림/닫힘)"""
    h, w = image_shape[:2]

    # 왼쪽 눈 랜드마크
    left_eye_top = landmarks[159]
    left_eye_bottom = landmarks[145]
    left_eye_left = landmarks[130]
    left_eye_right = landmarks[133]

    # 눈 높이 계산
    left_eye_height = abs(left_eye_top.y - left_eye_bottom.y) * h
    left_eye_width = abs(left_eye_right.x - left_eye_left.x) * w

    # 눈 비율 (열림/닊힘)
    eye_ratio = left_eye_height / left_eye_width

    # 임계값 (실험적으로 조정 필요)
    if eye_ratio < 0.15:
        return "Closed"
    else:
        return "Open"

# 사용
if results.multi_face_landmarks:
    eye_state = get_eye_state(face_landmarks.landmark, frame.shape)
    print(f"Eye state: {eye_state}")
```

### 3.3 미소 감지

```python
def get_mouth_state(landmarks, image_shape):
    """입 상태 감지 (미소/일반)"""
    h, w = image_shape[:2]

    # 입술 랜드마크
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]
    mouth_left = landmarks[61]
    mouth_right = landmarks[291]

    # 입 открыт김
    mouth_height = abs(upper_lip.y - lower_lip.y) * h
    mouth_width = abs(mouth_right.x - mouth_left.x) * w

    # 미소 비율
    smile_ratio = mouth_height / mouth_width

    if smile_ratio > 0.25 and mouth_width > 0.1 * w:
        return "Smiling"
    elif mouth_height > 0.05 * h:
        return "Open"
    else:
        return "Neutral"

# 사용
mouth_state = get_mouth_state(face_landmarks.landmark, frame.shape)
print(f"Mouth state: {mouth_state}")
```

## 4. Face Mesh 활용 애플리케이션

### 4.1 얼굴랜드마크 추적 애플리케이션

```python
import cv2
import mediapipe as mp
import numpy as np

class FaceMeshApp:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # 얼굴 윤곽 그리기
                self.mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    self.mp_face_mesh.FACE_CONTOURS,
                    self.mp_drawing_styles.get_default_face_mesh_contours_style()
                )

                # 랜드마크 정보 표시
                self.draw_info(frame, face_landmarks)

        return frame

    def draw_info(self, frame, landmarks):
        h, w = frame.shape[:2]

        # 코 위치
        nose = landmarks[1]
        cv2.putText(frame, f"Nose: ({nose.x:.2f}, {eye.y:.2f})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 눈 중심
        left_eye = landmarks[33]
        right_eye = landmarks[263]
        eye_x = (left_eye.x + right_eye.x) / 2
        eye_y = (left_eye.y + right_eye.y) / 2
        cv2.putText(frame, f"Eye: ({eye_x:.2f}, {eye_y:.2f})",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    def run(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.process_frame(frame)

            cv2.imshow('Face Mesh App', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# 실행
app = FaceMeshApp()
app.run()
```

### 4.2 필터 효과 (얼굴 랜드마크 기반)

```python
def apply_face_filter(frame, landmarks):
    """얼굴에 필터 적용"""
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # 코 끝점
    nose = landmarks[1]
    nose_x, nose_y = int(nose.x * w), int(nose.y * h)

    # 눈 사이 거리
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    eye_distance = int(abs(left_eye.x - right_eye.x) * w)

    # 코에 원 그리기 ( filtre 효과)
    cv2.circle(overlay, (nose_x, nose_y), eye_distance // 2,
               (0, 255, 255), -1)

    # 투명도 적용
    return cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)
```

### 4.3 안경 가상 시도

```python
def apply_virtual_glasses(frame, landmarks):
    """가상 안경 적용"""
    h, w = frame.shape[:2]
    result = frame.copy()

    # 눈 위치
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    left_eye_x, left_eye_y = int(left_eye.x * w), int(left_eye.y * h)
    right_eye_x, right_eye_y = int(right_eye.x * w), int(right_eye.y * h)

    # 안경 너비
    glasses_width = int(abs(right_eye_x - left_eye_x) * 1.5)

    # 안경 그리기
    cv2.line(result,
             (left_eye_x - glasses_width//4, left_eye_y),
             (left_eye_x + glasses_width//4, left_eye_y),
             (0, 0, 0), 3)
    cv2.line(result,
             (right_eye_x - glasses_width//4, right_eye_y),
             (right_eye_x + glasses_width//4, right_eye_y),
             (0, 0, 0), 3)

    # 브릿지
    cv2.line(result,
             (left_eye_x + glasses_width//4, left_eye_y),
             (right_eye_x - glasses_width//4, right_eye_y),
             (0, 0, 0), 2)

    return result
```

## 5. Face Mesh 최적화

### 5.1 성능 최적화

```python
# 최적화된 Face Mesh 설정
face_mesh_optimized = mp_face_mesh.FaceMesh(
    static_image_mode=True,  # 이미지에서만 사용할 때
    max_num_faces=1,  # 한 번에 하나의 얼굴만
    refine_landmarks=False,  // 랜드마크 정교화 비활성화
    min_detection_confidence=0.7,  // 더 높은 신뢰도
    min_tracking_confidence=0.7
)
```

### 5.2 GPU 가속

```python
# GPU 사용 (Jetson에서)
face_mesh_gpu = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    running_mode=mp.solutions.mediapipe_python.RunningMode.GPU
)
```

## 6. 실습 과제

1. Face Mesh를 사용하여 이미지에서 얼굴 랜드마크를 추출하세요.
2. 실시간 웹캠에서 얼굴 방향을 추정하는 프로그램을 작성하세요.
3. 눈 상태(열림/닊힘)를 감지하는 기능을 구현하세요.
4. 가상 안경 필터를 적용하는 프로그램을 작성하세요.
5. Face Mesh 성능을 최적화하세요.

## 7. 다음 실습 예고

다음 클래스에서는 Mediapipe 손 제스처 인식 실습을 진행합니다.