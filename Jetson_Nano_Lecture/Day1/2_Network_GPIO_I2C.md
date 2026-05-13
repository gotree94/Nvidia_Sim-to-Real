# 2일차: Linux Network, Jetpack Library, GPIO, I2C

<img src="59.png" width="40%">


---

## Linux Network

### 주요 명령어

#### ip 명령어

- 네트워크 인터페이스 설정 및 관리
- 라우팅 테이블 관리
- 네트워크 장치 관리

```bash
# 모든 네트워크 인터페이스 정보 표시
ip addr show

# 네트워크 인터페이스 상태 표시
ip link show

# 인터페이스 비활성화/활성화
sudo ip link set eth0 down
sudo ip link set eth0 up

# 라우팅 테이블 표시
ip route show
```

#### ifconfig 명령어

- 네트워크 인터페이스 설정 및 관리 (구식 명령어)
- 네트워크 상태 확인

```bash
# 모든 인터페이스 정보
ifconfig

# 특정 인터페이스 정보
ifconfig eth0

# 인터페이스 비활성화/활성화
sudo ifconfig eth0 down
sudo ifconfig eth0 up
```

#### wget 명령어

- 웹에서 파일 다운로드 (HTTP, HTTPS, FTP 지원)
- 배치 다운로드 및 재시도 기능

```bash
# 파일 다운로드
wget https://example.com/file.txt

# 특정 이름으로 저장
wget -O output.txt https://example.com/file.txt

# 속도 제한
wget --limit-rate=0.5k https://example.com/file.txt
```

#### curl 명령어

- 웹 API와의 상호작용에 최적화
- 다양한 프로토콜 지원

```bash
# 파일 다운로드
curl -O https://example.com/file.txt

# 특정 이름으로 저장
curl -o output.txt https://example.com/file.txt

# 파일로 저장
curl https://example.com > output.txt

# 속도 제한
curl --limit-rate 500B -o output.txt https://example.com/file.txt
```

> **wget vs curl**: wget은 더 엄격하게 속도 제한, curl은 버퍼를 사용해 순간적으로 더 빠를 수 있음

#### ssh (Secure Shell)

- 네트워크를 통해 안전하게 원격 시스템에 접속
- 암호화된 연결로 데이터 기밀성 및 무결성 보장

```bash
# 원격 접속
ssh nvidia@172.30.1.5

# 파일 전송 (scp)
scp text.txt nvidia@172.30.1.5:~

# 서버에서 파일 다운로드
scp nvidia@172.30.1.5:~/test1.txt C:\Users\allai\Desktop\
```

#### Visual Studio Code SSH 연결

1. **Jetson Nano (Host)**:
   ```bash
   sudo apt-get install openssh-server
   ```

2. **Client (VSCode)**:
   - Extensions에서 "Remote-SSH" 설치
   - `Ctrl+Shift+P` → "Remote-SSH: Add New SSH Host"
   - `ssh nvidia@<IP주소>` 입력
   - 저장 위치: 기본값 선택
   - 연결 후 폴더 열기

---

## Jetpack Library

### Jetpack이란?

- Jetson용 AI 핵심 S/W 라이브러리
- 구성요소:
  - **CUDA**: GPU 가속을 위한 컴퓨팅 플랫폼
  - **TensorRT**: 딥러닝 추론 최적화 라이브러리
  - **cuDNN**: CUDA 기반 딥 뉴럴 네트워크 라이브러리
  - **OpenCV**: 컴퓨터 비전 라이브러리
  - **VPI**: Vision Programming Interface

### Jetpack Library 설치

#### SDK Manager 사용 (Dev Kit)

#### Linux Repository 사용 (Commercial Board - 예: JCB100)

```bash
# apt 업데이트
sudo apt update

# nvidia-jetpack 설치
sudo apt install nvidia-jetpack

# python3-pip 설치
sudo apt-get install python3-pip

# jetson-stats 설치
sudo -H pip3 install -U jetson-stats

# 재부팅
sudo reboot
```

#### 설치 확인

```bash
# jetson_release 도구 사용
jetson_release

# OpenCV 버전 확인
pkg-config --modversion opencv4
```

### CUDA Enabled OpenCV

```bash
# NVIDIA 제공 OpenCV 설치
# 또는 소스 코드에서 빌드

# CMake 옵션 예시
cmake -D WITH_CUDA=ON \
      -D WITH_CUDNN=ON \
      -D CUDA_FAST_MATH=ON \
      -D OPENCV_DNN_CUDA=ON \
      ...
```

### TensorFlow 설치

```bash
# JetPack version에 따른 CUDA Enabled TensorFlow
sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v512 tensorflow==2.12.0+nv23.06
```

### PyTorch 설치

```bash
export TORCH_INSTALL=https://developer.download.nvidia.com/compute/redist/jp/v511/pytorch/torch-2.0.0+nv23.05-cp38-cp38-linux_aarch64.whl

python3 -m pip install --upgrade pip
python3 -m pip install numpy==1.26.1
python3 -m pip install --no-cache $TORCH_INSTALL
```

### Jetson-stats

- 시스템 상태 모니터링 도구
- 포함 도구: `jtop`, `jetson_release`, `jetson_config`, `jetson_swap`

```bash
# 설치
sudo apt-get install python3-pip
sudo -H pip3 install -U jetson-stats

# 사용
jtop
jetson_release
```

#### jtop 화면 설명

| 번호 | 설명 |
|---|---|
| 1 | 시스템 요약 (CPU, GPU, 메모리, 디스크 사용량) |
| 2 | GPU 사용 현황 |
| 3 | CPU 사용 현황 |
| 4 | 메모리 사용 현황 |
| 5 | 엔진 상태 (하드웨어 가속 엔진) |
| 6 | 관리 화면 (전력, 클럭 최적화) |
| 7 | 정보 화면 (하드웨어/소프트웨어 정보) |

### Jetson 시스템 온도 확인

```bash
# 온도 확인 (값/1000 = 온도)
cat /sys/class/thermal/thermal_zone0/temp
# 예: 46000 → 46도
```

---

## GPIO (General Purpose Input Output)

### GPIO란?

- MCU의 일반적인 입력과 출력을 처리하는 외부 인터페이스
- 다양한 센서, LED, 버튼 등과 상호작용 가능

### Jetson.GPIO

- Jetson Nano 개발 보드에는 Raspberry Pi의 40pin 헤더와 유사한 40pin GPIO 헤더 포함
- Python 라이브러리로 디지털 입출력 제어 가능
- GitHub: https://github.com/NVIDIA/jetson-gpio

### LED 제어 실습 (sysfs GPIO)

#### 연결

- GPIO 번호: 32번 Pin (GPIO168)
- GND: 6번 Pin

#### 명령어

```bash
# Super User 모드
sudo su

# GPIO Export
echo 168 > /sys/class/gpio/export

# Direction 설정
echo out > /sys/class/gpio/gpio168/direction

# LED ON
echo 1 > /sys/class/gpio/gpio168/value

# LED OFF
echo 0 > /sys/class/gpio/gpio168/value
```

### Python으로 LED 제어 (Jetson.GPIO 라이브러리)

#### 주요 함수

| 함수 | 설명 |
|---|---|
| `GPIO.setmode(GPIO.BOARD)` | 40핀 헤더 번호 기준 |
| `GPIO.setmode(GPIO.BCM)` | Broadcom SoC GPIO 번호 기준 |
| `GPIO.setup(channel, GPIO.OUT)` | GPIO 핀을 입력/출력으로 설정 |
| `GPIO.output(channel, state)` | 출력값 제어 (HIGH/LOW) |

#### 예제 코드

```python
import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

try:
    while True:
        GPIO.output(11, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(11, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
```

---

## I2C (Inter-Integrated Circuit)

### I2C란?

- 동기식 직렬 통신 버스
- Master/Slave 방식
- 2개의 Pin (SDA, SCL)으로 구성
- 다양한 센서(온도, 압력, 가속도 등) 연결 가능

### I2C 원리

- **SDA (Serial Data Line)**: 데이터 전송
- **SCL (Serial Clock Line)**: 클럭 신호
- 각 센서는 고유한 주소를 가짐

### Jetson Nano I2C 장치 파일

- `/dev/i2c-0`, `/dev/i2c-1` 등

### i2cdetect 명령어

```bash
# I2C 버스 스캔
sudo i2cdetect -y -r 0
```

---

## I2C 실습 - LCD (LCD 1602 I2C)

### 연결

| LCD | Jetson Nano |
|---|---|
| VCC | 5V (2번) |
| GND | GND (6번) |
| SDA | GPIO 02 (3번) |
| SCL | GPIO 03 (5번) |

### LCD I2C 주소 확인

```bash
sudo i2cdetect -y -r 0
# 일반적으로 0x27
```

### Python으로 LCD 제어

```python
import RPi_I2C_driver
from time import *

lcd = RPi_I2C_driver.lcd(0x27)

# 문자 출력
lcd.print("Hello World!")

# 특정 위치에 출력
lcd.setCursor(0, 1)
lcd.print("Line 2")

# 화면 지우기
lcd.lcd_clear()
```

---

## I2C 실습 - IMU (MPU6050-GY25)

### 연결

| MPU6050 | Jetson Nano |
|---|---|
| VCC | 3.3V 또는 5V |
| GND | GND |
| SDA | SDA (3번) |
| SCL | SCL (5번) |

### I2C 주소 확인

```bash
sudo i2cdetect -y -r 0
# 일반적으로 0x68
```

### Python으로 IMU 데이터 읽기

```python
import smbus
import time

bus = smbus.SMBus(0)
Device_Address = 0x68

# 레지스터 설정
PWR_MGMT_1 = 0x6B
bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

# 가속도 읽기
ACCEL_XOUT_H = 0x3B
acc_x = bus.read_byte_data(Device_Address, ACCEL_XOUT_H)
acc_y = bus.read_byte_data(Device_Address, ACCEL_XOUT_H + 2)
acc_z = bus.read_byte_data(Device_Address, ACCEL_XOUT_H + 4)

# 자이로 읽기
GYRO_XOUT_H = 0x43
gyro_x = bus.read_byte_data(Device_Address, GYRO_XOUT_H)
```

### 온도 데이터 읽기

```python
TEMP_OUT0 = 0x41
temp = bus.read_byte_data(Device_Address, TEMP_OUT0)
actual_temp = (temp / 340) + 36.53
```

---

## PWM FAN 제어

### fan-ctl 설치

```bash
git clone https://github.com/jetsonworld/jetson-fan-ctl.git
cd jetson-fan-ctl
sudo sh install.sh
```

### 설정 파일 수정

```json
{
    "FAN_OFF_TEMP": 40,
    "FAN_MAX_TEMP": 60,
    "UPDATE_INTERVAL": 2,
    "MAX_PERF": 1
}
```

- **FAN_OFF_TEMP**: 이 온도°C보다 낮으면 팬 끄기
- **FAN_MAX_TEMP**: 이 온도°C 이상이면 팬 최대 속도
- **UPDATE_INTERVAL**: 온도 체크 주기 (초)
- **MAX_PERF**: 1 = 최대 성능 모드, 0 = 전력 절약

### 서비스 재시작

```bash
sudo service automagic-fan restart
sudo service automagic-fan status
```

---

## 주의사항

> **중요**: Jetson Nano는 NVIDIA의 커스텀 커널과 부트로더 기반.  
> `sudo apt upgrade` 명령어는 사용 금지 (커널 및 부팅 구성요소 손상 위험)

---

## 참고 자료

```
#!/usr/bin/env python

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import smbus
import time
import math

# MPU6050 Registers
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

bus = smbus.SMBus(0)
Device_Address = 0x68

# 자이로 및 가속도 스케일
ACCEL_SCALE_MODIFIER_16G = 2048.0  # 16G 범위에서 16-bit 값의 스케일
GYRO_SCALE_MODIFIER_250DEG = 131.0  # 250도/초 범위

# Complementary Filter 변수
pitch = 0
roll = 0
yaw = 0
last_time = time.time()

def MPU_Init():
    # 슬레이브 rate 설정 (.sample rate = 8kHz / (1 + SMPLRT_DIV))
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    # power management - PLL with X gyro
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    # gyro 설정 - 250도/초
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 0)
    
    # 가속도 설정 - 16G
    bus.write_byte_data(Device_Address, ACCEL_CONFIG, 0x18)  # 0x18 = 16G
    
    # interrupt enable
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

def read_imu_data():
    """가속도 및 자이로 데이터 읽기"""
    # 가속도 읽기 (Raw 값)
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)
    
    # 자이로 읽기 (Raw 값)
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)
    
    return acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z

def calculate_angles(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, dt):
    """Complementary Filter를 사용하여 각도 계산"""
    global pitch, roll, yaw
    
    # 가속도에서 각도 계산 (atar2 사용)
    # roll = atan2(acc_y, acc_z)
    # pitch = atan2(-acc_x, sqrt(acc_y^2 + acc_z^2))
    acc_roll = math.atan2(acc_y, acc_z) * (180 / math.pi)
    acc_pitch = math.atan2(-acc_x, math.sqrt(acc_y**2 + acc_z**2)) * (180 / math.pi)
    
    # 자이로 각도 (각속도 * dt)
    gyro_roll = gyro_x / GYRO_SCALE_MODIFIER_250DEG * dt
    gyro_pitch = gyro_y / GYRO_SCALE_MODIFIER_250DEG * dt
    gyro_yaw = gyro_z / GYRO_SCALE_MODIFIER_250DEG * dt
    
    # Complementary Filter (가속도 0.98, 자이로 0.02)
    alpha = 0.98
    roll = alpha * (roll + gyro_roll) + (1 - alpha) * acc_roll
    pitch = alpha * (pitch + gyro_pitch) + (1 - alpha) * acc_pitch
    yaw += gyro_yaw
    
    return pitch, roll, yaw

def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def draw(pitch, roll, yaw):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)
    
    # Yaw 모드에 따라 회전
    glRotatef(yaw, 0.0, 1.0, 0.0)      # Yaw (Y축)
    glRotatef(pitch, 1.0, 0.0, 0.0)   # Pitch (X축)
    glRotatef(-roll, 0.0, 0.0, 1.0)   # Roll (Z축)
    
    # 큐브 그리기
    glBegin(GL_QUADS)
    
    # 위쪽 (녹색)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)
    
    # 아래쪽 (주황)
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)
    
    # 앞쪽 (빨강)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    
    # 뒤쪽 (노랑)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)
    
    # 왼쪽 (파랑)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    
    # 오른쪽 (보라)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    
    glEnd()

def main():
    global pitch, roll, yaw
    
    MPU_Init()
    time.sleep(0.5)  # 초기화 후 대기
    
    # 초기 각도 설정
    acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = read_imu_data()
    pitch = math.atan2(-acc_x, math.sqrt(acc_y**2 + acc_z**2)) * (180 / math.pi)
    roll = math.atan2(acc_y, acc_z) * (180 / math.pi)
    
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((640, 480), video_flags)
    pygame.display.set_caption("IMU Visualization - Press 'r' to reset, 'z' to toggle yaw")
    resize(640, 480)
    init()
    
    last_time = time.time()
    frames = 0
    
    yaw_mode = True
    
    while True:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            break
        if event.type == KEYDOWN and event.key == K_r:
            # 리셋
            pitch, roll, yaw = 0, 0, 0
            acc_x, acc_y, acc_z, _, _, _ = read_imu_data()
            pitch = math.atan2(-acc_x, math.sqrt(acc_y**2 + acc_z**2)) * (180 / math.pi)
            roll = math.atan2(acc_y, acc_z) * (180 / math.pi)
        if event.type == KEYDOWN and event.key == K_z:
            yaw_mode = not yaw_mode
        
        # 시간 계산
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # IMU 데이터 읽기 및 각도 계산
        acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z = read_imu_data()
        
        if yaw_mode:
            pitch, roll, yaw = calculate_angles(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, dt)
        
        # 화면 그리기
        draw(pitch, roll, yaw)
        pygame.display.flip()
        
        # 터미널에 데이터 출력
        print(f"Pitch: {pitch:6.1f}  Roll: {roll:6.1f}  Yaw: {yaw:6.1f}", end='\r')
        
        frames += 1
        time.sleep(0.01)  # I2CCommunication 딜레이
        
        # FPS 표시 (5초마다)
        if frames % 500 == 0:
            elapsed = time.time() - current_time
            if elapsed > 0:
                print(f"\nFPS: {500 / (time.time() - current_time + 0.001):.1f}")
    
    print("\n종료")

if __name__ == '__main__':
    main()
```

- [Jetson.GPIO GitHub](https://github.com/NVIDIA/jetson-gpio)
- [I2C LCD Driver](https://github.com/eleparts/RPi_I2C_LCD_driver)
- [MPU6050 Datasheet](https://invensense.tdk.com/products/mpu6050/)
- [jetson-fan-ctl](https://github.com/jetsonworld/jetson-fan-ctl)
