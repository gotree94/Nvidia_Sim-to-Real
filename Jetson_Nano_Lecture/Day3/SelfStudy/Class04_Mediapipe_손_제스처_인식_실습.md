# Class 04: Mediapipe 손 제스처 인식 실습

## 1. Hands 솔루션 개요

### 1.1 Hands란?

MediaPipe Hands는 손의 21개 랜드마크를 실시간으로 추적하고 손가락 개수, 제스처를 인식하는 솔루션입니다.

### 1.2 랜드마크 구조

```
Hand Landmarks (21 points):
┌─────────────────────────────────────┐
│ 0: 手首 (WRIST)                     │
│ 1-4: Thumb (엄지)                  │
│ 5-8: Index (검지)                   │
│ 9-12: Middle (중지)                 │
│ 13-16: Ring (약지)                  │
│ 17-20: Pinky (소지)                 │
└─────────────────────────────────────┘
```

### 1.3 랜드마크 인덱스

| 손가락 | TIP | PIP | MCP |
|--------|-----|-----|-----|
| Thumb | 4 | 3 | 1 |
| Index | 8 | 7 | 5 |
| Middle | 12 | 11 | 9 |
| Ring | 16 | 15 | 13 |
| Pinky | 20 | 19 | 17 |

## 2. Hands 기본 실습

### 2.1 손 랜드마크 추출

```python
import cv2
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

# 이미지 로드
image = cv2.imread('hand.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 손 랜드마크 추출
results = hands.process(image_rgb)

# 결과 시각화
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

cv2.imwrite('hand_output.jpg', image)
```

### 2.2 실시간 손 추적

```python
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 3. 손가락 개수 인식

### 3.1 손가락 펼침 감지

```python
def count_fingers(hand_landmarks):
    """펼친 손가락 개수 계산"""
    fingers = []

    # Thumb (엄지) - 측면에서 보기 때문에 별도 처리
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]
    if thumb_tip.x > thumb_ip.x:  # 오른손
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers (검지, 중지, 약지, 소지)
    finger_tips = [8, 12, 16, 20]  # TIP 인덱스
    finger_pips = [7, 11, 15, 19]  # PIP 인덱스

    for tip_idx, pip_idx in zip(finger_tips, finger_pips):
        tip = hand_landmarks.landmark[tip_idx]
        pip = hand_landmarks.landmark[pip_idx]
        if tip.y < pip.y:  # 펴진 상태 (y가 작을수록 위)
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

# 사용
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        finger_count = count_fingers(hand_landmarks)
        print(f"Finger count: {finger_count}")
```

### 3.2 손가락 개수 표시

```python
def count_and_draw_fingers(frame, hand_landmarks):
    """손가락 개수 계산 및 표시"""
    finger_count = count_fingers(hand_landmarks)

    h, w, c = frame.shape

    # 손 위치 찾기
    wrist = hand_landmarks.landmark[0]
    wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)

    # 손가락 개수 텍스트
    cv2.putText(
        frame,
        f"Fingers: {finger_count}",
        (wrist_x - 50, wrist_y - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    return frame, finger_count
```

## 4. 제스처 인식

### 4.1 기본 제스처 정의

```python
import math

# 제스처 정의
GESTURES = {
    "FIST": "주먹",
    "PALM": "바닥",
    "PEACE": "peace",
    "THUMBS_UP": "좋아요",
    "THUMBS_DOWN": "싫어요",
    "OK": "오케이",
    "ONE": "1",
    "TWO": "2",
    "THREE": "3",
    "FOUR": "4",
    "FIVE": "5"
}

def recognize_gesture(hand_landmarks):
    """제스처 인식"""
    # 랜드마크 추출
    finger_tips = [4, 8, 12, 16, 20]
    finger_bases = [2, 5, 9, 13, 17]

    fingers_extended = []
    for tip_idx, base_idx in zip(finger_tips, finger_bases):
        tip = hand_landmarks.landmark[tip_idx]
        base = hand_landmarks.landmark[base_idx]
        fingers_extended.append(tip.y < base.y)

    # 제스처 판단
    if not any(fingers_extended):
        return "FIST"
    elif all(fingers_extended):
        return "PALM"
    elif fingers_extended[1] and fingers_extended[2] and not fingers_extended[3] and not fingers_extended[4]:
        return "PEACE"
    elif fingers_extended[0] and not any(fingers_extended[1:]):
        return "THUMBS_UP"
    elif not fingers_extended[0] and not any(fingers_extended[1:]):
        return "THUMBS_DOWN"
    elif fingers_extended[0] and fingers_extended[1] and not any(fingers_extended[2:]):
        return "OK"
    else:
        count = sum(fingers_extended)
        return str(count)
```

### 4.2 제스처 인식 애플리케이션

```python
class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.gesture = "None"

    def process(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 랜드마크 그리기
                mp.solutions.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                # 제스처 인식
                self.gesture = recognize_gesture(hand_landmarks)

                # 텍스트 표시
                h, w = frame.shape[:2]
                wrist = hand_landmarks.landmark[0]
                wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)

                cv2.putText(
                    frame,
                    f"Gesture: {self.gesture}",
                    (wrist_x - 50, wrist_y - 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

        return frame

    def run(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.process(frame)

            cv2.imshow('Gesture Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# 실행
recognizer = GestureRecognizer()
recognizer.run()
```

## 5. 고급 제스처

### 5.1 손높이 추적

```python
def get_hand_height(hand_landmarks):
    """손높이 (손바닥 위치) 계산"""
    palm = hand_landmarks.landmark[9]
    return 1 - palm.y  # 화면 위쪽이 0, 아래쪽이 1

# 사용
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        height = get_hand_height(hand_landmarks)
        print(f"Hand height: {height:.2f}")
```

### 5.2 손 회전 감지

```python
def get_hand_rotation(hand_landmarks):
    """손 회전 각도 계산"""
    wrist = hand_landmarks.landmark[0]
    index_base = hand_landmarks.landmark[5]
    pinky_base = hand_landmarks.landmark[17]

    # 손바닥 중심에서 검지까지 벡터
    dx = index_base.x - wrist.x
    dy = index_base.y - wrist.y

    # 각도 계산
    angle = math.atan2(dy, dx) * 180 / math.pi
    return angle

# 사용
rotation = get_hand_rotation(hand_landmarks)
print(f"Hand rotation: {rotation:.1f}°")
```

### 5.3 손 동작 감지 (스왑)

```python
class GestureTracker:
    def __init__(self):
        self.prev_wrist = None
        self.gesture_history = []

    def update(self, hand_landmarks):
        """손 동작 추적"""
        wrist = hand_landmarks.landmark[0]

        if self.prev_wrist is not None:
            # 이동량 계산
            dx = wrist.x - self.prev_wrist.x
            dy = wrist.y - self.prev_wrist.y

            # 동작 판단
            if abs(dx) > 0.1:
                direction = "Right" if dx > 0 else "Left"
                return direction, (dx, dy)
            elif abs(dy) > 0.1:
                direction = "Down" if dy > 0 else "Up"
                return direction, (dx, dy)

        self.prev_wrist = wrist
        return "Stationary", (0, 0)

# 사용
tracker = GestureTracker()

if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        direction, delta = tracker.update(hand_landmarks)
        if direction != "Stationary":
            print(f"Gesture: {direction}, delta: {delta}")
```

## 6. 제스처 기반 애플리케이션

### 6.1 마우스 컨트롤

```python
import pyautogui

def hand_mouse_control(hand_landmarks, frame_shape):
    """손을 이용한 마우스 컨트롤"""
    h, w = frame_shape[:2]

    # 검지 손가락으로 마우스 이동
    index_tip = hand_landmarks.landmark[8]
    index_x = int(index_tip.x * w)
    index_y = int(index_tip.y * h)

    # 마우스 이동
    pyautogui.moveTo(index_x, index_y)

    # 엄지-검지 사이 거리로 클릭 감지
    thumb_tip = hand_landmarks.landmark[4]
    distance = ((index_tip.x - thumb_tip.x)**2 +
                (index_tip.y - thumb_tip.y)**2)**0.5

    if distance < 0.05:
        pyautogui.click()
        time.sleep(0.5)

    return frame
```

### 6.2 볼륨 컨트롤

```python
import subprocess

def volume_control(hand_landmarks, prev_height):
    """손높이로 볼륨 조절"""
    current_height = 1 - hand_landmarks[9].y  # palm center

    if prev_height is not None:
        delta = current_height - prev_height

        if delta > 0.05:
            subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', '5%+'])
            return "Volume Up"
        elif delta < -0.05:
            subprocess.run(['amixer', '-D', 'pulse', 'sset', 'Master', '5%-'])
            return "Volume Down"

    return current_height
```

## 7. Jetson에서 최적화

### 7.1 성능 최적화

```python
# 최적화된 Hands 설정
hands_optimized = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,  # 0: lite, 1: full
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
```

### 7.2 해상도 조정

```python
# 작은 해상도로 처리
small_frame = cv2.resize(frame, (320, 240))
results = hands.process(cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB))
```

## 8. 실습 과제

1. Hands를 사용하여 실시간 손 랜드마크를 추출하세요.
2. 펼쳐진 손가락 개수를 감지하는 프로그램을 작성하세요.
3. 기본 제스처(FIST, PALM, PEACE)를 인식하세요.
4. 손 동작(스왑)을 감지하여 볼륨을 조절하는 기능을 구현하세요.
5. Jetson에서 최적화하여 실시간 처리를하세요.

## 9. 다음 실습 예고

다음 클래스에서는 로봇에 Jetson Nano를 조립하는 실습을 진행합니다.