# Class 05: 로봇에 Jetson Nano 조립 (1)

## 1. 조립 준비

### 1.1 필요한 부품

```
로봇 키트 구성품:
┌─────────────────────────────────────┐
│ 1. Jetson Nano 개발 키트           │
│ 2. 마운트 브래킷                    │
│ 3. Raspberry Pi 카메라              │
│ 4. USB 웹캠 (대안)                  │
│ 5. 이동용 배터리                    │
│ 6. 전원 케이블                      │
│ 7. 나사 및 볼트 세트               │
│ 8.散热器 ( heatsink)               │
│ 9.ファン (fan)                     │
│ 10. 브레드보드/ Perfboard           │
└─────────────────────────────────────┘
```

### 1.2 도구 준비

- 드라이버 세트 (Phillips, Hex)
- 스패너
- 플라이어
- 케이블 타이
- 본드
- multimeter
- 가위/커터

### 1.3 안전 주의사항

1. 정전기 방지 확인 (ESD strap 사용 권장)
2. 전원 연결 전 모든 연결 확인
3. 과전압/과전류 방지
4. 열 발생 주의

## 2. Jetson Nano 준비

### 2.1 부팅 SD 카드 준비

```bash
# Jetson Nano에 JetPack 설치
# 1. NVIDIA Jetson SDK Manager 다운로드
# 2. Jetson Nano를 Recovery 모드로 연결
# 3. JetPack 설치

# 대안: 사전 구축된 이미지 사용
# https://developer.nvidia.com/jetson-nano-sd-card-image
```

### 2.2 초기 설정

```bash
# 첫 부팅 후 설정
# 1. 사용자 생성
# 2. 네트워크 연결
# 3. 시스템 업데이트

sudo apt update
sudo apt upgrade -y
```

### 2.3 필수 패키지 설치

```bash
# 시스템 패키지
sudo apt install -y \
    build-essential \
    git \
    python3-pip \
    libopenjp2-7 \
    libtiff5 \
    libsm6 \
    libxext6 \
    libxrender-dev

# Python 패키지
pip3 install --upgrade pip
pip3 install numpy opencv-python torch torchvision
pip3 install jetson-stats
```

### 2.4 팬 설치

```python
# 팬 연결
# +: 5V (pin 4)
# -: GND (pin 6)
# 제어: GPIO (선택)

# 팬 속도 제어 스크립트
echo 5000 | sudo tee /sys/devices/pwm-fan/target_speed
```

### 2.5 방열판( heatsink) 설치

```thermal interface material (TIM)涂抹}
# 1. Jetson Nanochip 청소
# 2. 방열판 뒷면에 TIM 도포
# 3. 방열판 부착
# 4. 나사로 고정
```

## 3. 카메라 설치

### 3.1 Raspberry Pi Camera (CSI)

```bash
# CSI 카메라 활성화
sudo modprobe ov5647

# 또는 config.txt 수정
# /boot/config.txt에 추가:
# dtoverlay=ov5647

# 테스트
raspistill -o test.jpg

# OpenCV에서 사용
python3 << 'EOF'
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imwrite('camera_test.jpg', frame)
cap.release()
EOF
```

### 3.2 USB 웹캠

```bash
# USB 카메라 확인
ls /dev/video*

# v4l2-ctl로 확인
v4l2-ctl --list-devices

# OpenCV로 테스트
python3 << 'EOF'
import cv2
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = cap.read()
cv2.imwrite('webcam_test.jpg', frame)
cap.release()
print("Webcam test completed!")
EOF
```

### 3.3 카메라 마운트

```
카메라 배치:
┌─────────────────────────────────────┐
│              로봇 본체               │
│  ┌─────────────────────────────────┐│
│  │         Jetson Nano            ││
│  │   ┌─────────────────────────┐  ││
│  │   │      CSI/USB Camera    │  ││
│  │   │         ↑               │  ││
│  │   └─────────────────────────┘  ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

## 4. 전원 공급

### 4.1 전원 옵션

| 옵션 | 전압 | 용량 | 비고 |
|------|------|------|------|
| DC Barrel Jack | 5V 3A | 일반 | 권장 |
| USB-C | 5V 3A | 일반 | JetPack 4.4 이상 |
| 배터리 | 7.4V LiPo | 대용량 | regulator 필요 |
| PoE | 48V | - | PoE HAT 필요 |

### 4.2 배터리 연결

```python
# LiPo 배터리 → DC-DCConverter → Jetson Nano
# 7.4V LiPo → 5V 3A regulator

# Regulator 연결:
# BATTERY → [LM2596] → 5V → Jetson Nano

# 안전 고려:
# 1. 과전압 보호
# 2. 저전압 컷오프
# 3. 전원 filtering
```

### 4.3 전원 관리

```python
# 전원 버튼 GPIO 연결
# Pin 5 (GPIO 3) - Power button
# Pin 6 (GND) - Ground

# 전원 관리 스크립트
import RPi.GPIO as GPIO
import subprocess

POWER_BTN = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(POWER_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def shutdown(channel):
    subprocess.run(['sudo', 'shutdown', '-h', 'now'])

GPIO.add_event_detect(POWER_BTN, GPIO.FALLING, callback=shutdown, bouncetime=2000)
```

## 5. 마운트 브래킷 조립

### 5.1 브래킷 설계

```CAD
3D 프린트용 브래킷 (예시):
- Jetson Nano 크기: 100mm x 80mm
- 구멍 간격: 85mm x 75mm (M3 나사)
- thickness: 3mm
- Material: PLA/ABS
```

### 5.2 브래킷 설치

```assembly
1. 브래킷을 로봇 프레임에 배치
2. 구멍 위치 확인
3. M3 나사로 고정
4. Jetson Nano를 브래킷에 부착
5. 카메라 지지대 설치
```

### 5.3 케이블 관리

```bash
# 케이블 타이로 정리
# 1. 전원 케이블 고정
# 2. 카메라 케이블 정리
# 3. USB 케이블 정리

# 커넥터 보호
# - 더미 플러그 사용
# - 실리콘 씰링
```

## 6. 연결 케이블

### 6.1 연결 다이어그램

```
┌─────────────────────────────────────┐
│          연결 다이어그램             │
│                                     │
│   ┌─────────┐    ┌─────────┐        │
│   │Camera   │───▶│ Jetson  │        │
│   └─────────┘    │  Nano   │        │
│                  └────┬────┘        │
│   ┌─────────┐        │              │
│   │ Battery │───────┼──────────┐   │
│   └─────────┘        │          │   │
│                     ▼          ▼   │
│                  ┌──────┐    ┌────┐ │
│                  │ DC   │    │모터│ │
│                  │Reg   │    │드라이│ │
│                  └──────┘    └────┘ │
└─────────────────────────────────────┘
```

### 6.2 GPIO 연결

```python
# GPIO 사용 예시
# Pin 29: GPIO 5 (LED)
# Pin 31: GPIO 6 (Button)
# Pin 33: GPIO 13 (PWM FAN)
# Pin 35: GPIO 19 (UART TX)
# Pin 36: GPIO 16 (UART RX)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
```

## 7. 초기 테스트

### 7.1 부팅 테스트

```bash
# 전원 연결 후 부팅 확인
# 1. LED 점등
# 2. Fan 동작
# 3. HDMI 출력

# 시스템 로그 확인
dmesg | tail
journalctl -b
```

### 7.2 네트워크 테스트

```bash
# IP 주소 확인
hostname -I

# Ping 테스트
ping -c 4 8.8.8.8

# SSH 활성화
sudo systemctl enable ssh
sudo systemctl start ssh
```

### 7.3 카메라 테스트

```bash
# cheese (GUI 테스트)
cheese

# 또는命令行 테스트
gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM),width=1920,height=1080,framerate=30/1' ! nvvidconv ! xvimagesink
```

### 7.4 성능 테스트

```bash
# tegrastats로 시스템 상태 확인
tegrastats

# CPU/GPU 벤치마크
python3 << 'EOF'
import torch
print(f"CUDA: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
print(f"PyTorch: {torch.__version__}")
EOF
```

## 8. 실습 과제

1. Jetson Nano에 JetPack을 설치하세요.
2. 카메라를 연결하고 테스트하세요.
3. 팬과 방열판을 설치하세요.
4. 브래킷을 만들고 로봇에 부착하세요.
5. 전체 시스템을 테스트하세요.

## 9. 다음 실습 예고

다음 클래스에서는 로봇에 Jetson Nano를 조립하는 실습을 완료합니다.