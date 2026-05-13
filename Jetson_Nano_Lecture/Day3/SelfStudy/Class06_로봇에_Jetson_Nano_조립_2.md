# Class 06: 로봇에 Jetson Nano 조립 (2)

## 1. 모터 드라이버 연동

### 1.1 모터 드라이버 종류

```
모터 드라이버 옵션:
┌─────────────────────────────────────┐
│ 1. L298N (DC 모터)                  │
│    - 2채널, 2A/Ch                   │
│    - PWM 속도 조절                  │
├─────────────────────────────────────┤
│ 2. L293D (DC 모터)                  │
│    - 4채널, 0.6A/Ch                 │
│    - 저전력 프로젝트용              │
├─────────────────────────────────────┤
│ 3. DRV8833 (DC 모터)                │
│    - 2채널, 1.5A/Ch                 │
│    - 소형, 경량                     │
├─────────────────────────────────────┤
│ 4. BTS7960 (DC 모터)                 │
│    - 1채널, 43A                      │
│    - 고전력 프로젝트용              │
└─────────────────────────────────────┘
```

### 1.2 L298N 연결

```python
# L298N 모터 드라이버 연결
# ENA, ENB: PWM (속도 제어)
# IN1, IN2: 방향 제어 (왼쪽 모터)
# IN3, IN4: 방향 제어 (오른쪽 모터)

import RPi.GPIO as GPIO

# GPIO 설정
LEFT_ENA = 32  # Physical pin 32
LEFT_IN1 = 36  # Physical pin 36
LEFT_IN2 = 38  # Physical pin 38
RIGHT_ENB = 33
RIGHT_IN3 = 35
RIGHT_IN4 = 37

# 초기화
GPIO.setmode(GPIO.BOARD)
GPIO.setup([LEFT_ENA, LEFT_IN1, LEFT_IN2, RIGHT_ENB, RIGHT_IN3, RIGHT_IN4], GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_ENA, 1000)  # 1kHz PWM
right_pwm = GPIO.PWM(RIGHT_ENB, 1000)

left_pwm.start(0)
right_pwm.start(0)

def move_forward(speed):
    GPIO.output(LEFT_IN1, True)
    GPIO.output(LEFT_IN2, False)
    GPIO.output(RIGHT_IN3, True)
    GPIO.output(RIGHT_IN4, False)
    left_pwm.ChangeDutyCycle(speed)
    right_pwm.ChangeDutyCycle(speed)

def move_stop():
    left_pwm.ChangeDutyCycle(0)
    right_pwm.ChangeDutyCycle(0)
```

### 1.3 모터驱动 클래스

```python
class MotorController:
    def __init__(self):
        self.left_pwm = None
        self.right_pwm = None
        self.setup_motors()

    def setup_motors(self):
        GPIO.setmode(GPIO.BOARD)
        pins = [LEFT_ENA, LEFT_IN1, LEFT_IN2, RIGHT_ENB, RIGHT_IN3, RIGHT_IN4]
        GPIO.setup(pins, GPIO.OUT)

        self.left_pwm = GPIO.PWM(LEFT_ENA, 1000)
        self.right_pwm = GPIO.PWM(RIGHT_ENB, 1000)
        self.left_pwm.start(0)
        self.right_pwm.start(0)

    def set_motor(self, motor, speed):
        """모터 속도 설정 (-100 ~ 100)"""
        if motor == 'left':
            if speed > 0:
                GPIO.output(LEFT_IN1, True)
                GPIO.output(LEFT_IN2, False)
            else:
                GPIO.output(LEFT_IN1, False)
                GPIO.output(LEFT_IN2, True)
            self.left_pwm.ChangeDutyCycle(abs(speed))
        elif motor == 'right':
            if speed > 0:
                GPIO.output(RIGHT_IN3, True)
                GPIO.output(RIGHT_IN4, False)
            else:
                GPIO.output(RIGHT_IN3, False)
                GPIO.output(RIGHT_IN4, True)
            self.right_pwm.ChangeDutyCycle(abs(speed))

    def forward(self, speed):
        self.set_motor('left', speed)
        self.set_motor('right', speed)

    def backward(self, speed):
        self.set_motor('left', -speed)
        self.set_motor('right', -speed)

    def turn_left(self, speed):
        self.set_motor('left', -speed)
        self.set_motor('right', speed)

    def turn_right(self, speed):
        self.set_motor('left', speed)
        self.set_motor('right', -speed)

    def stop(self):
        self.set_motor('left', 0)
        self.set_motor('right', 0)

    def cleanup(self):
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()
```

## 2. 센서 연결

### 2.1 초음파 센서 (HC-SR04)

```python
import time
import RPi.GPIO as GPIO

class UltrasonicSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig = trig_pin
        self.echo = echo_pin
        GPIO.setup(trig_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start_time = time.time()
        while GPIO.input(self.echo) == 0:
            start_time = time.time()

        end_time = time.time()
        while GPIO.input(self.echo) == 1:
            end_time = time.time()

        distance = (end_time - start_time) * 34300 / 2
        return distance

# 사용
# us = UltrasonicSensor(trig=11, echo=13)
# dist = us.get_distance()
```

### 2.2 적외선 센서

```python
class IRSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN)

    def is_detected(self):
        return GPIO.input(self.pin) == 0

# 사용
# ir_left = IRSensor(pin=15)
# ir_right = IRSensor(pin=16)
# if ir_left.is_detected():
#     print("Line detected on left")
```

### 2.3 인코더 모터

```python
class Encoder:
    def __init__(self, pin):
        self.pin = pin
        self.count = 0
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=self.callback)

    def callback(self, channel):
        self.count += 1

    def get_count(self):
        return self.count

    def reset(self):
        self.count = 0
```

## 3. 통합 제어 시스템

### 3.1Robot 클래스

```python
class Robot:
    def __init__(self):
        self.motor = MotorController()
        self.camera = None
        self.sensors = {}

    def init_camera(self, camera_type='usb'):
        if camera_type == 'usb':
            import cv2
            self.camera = cv2.VideoCapture(0)
        elif camera_type == 'csi':
            # CSI 카메라 초기화
            pass

    def add_ultrasonic(self, name, trig, echo):
        self.sensors[name] = UltrasonicSensor(trig, echo)

    def add_ir_sensor(self, name, pin):
        self.sensors[name] = IRSensor(pin)

    def move(self, command, speed=50):
        commands = {
            'forward': self.motor.forward,
            'backward': self.motor.backward,
            'left': self.motor.turn_left,
            'right': self.motor.turn_right,
            'stop': self.motor.stop
        }
        if command in commands:
            if command == 'stop':
                commands[command]()
            else:
                commands[command](speed)

    def get_sensor_data(self):
        data = {}
        for name, sensor in self.sensors.items():
            if isinstance(sensor, UltrasonicSensor):
                data[name] = sensor.get_distance()
            elif isinstance(sensor, IRSensor):
                data[name] = sensor.is_detected()
        return data

    def get_image(self):
        if self.camera:
            ret, frame = self.camera.read()
            return frame if ret else None
        return None
```

### 3.2 자율주행 dasar

```python
class AutonomousController:
    def __init__(self, robot):
        self.robot = robot
        self.running = False

    def line_following(self):
        """라인 따라가기"""
        ir_left = self.robot.sensors.get('ir_left')
        ir_right = self.robot.sensors.get('ir_right')

        if not ir_left or not ir_right:
            return

        left_detected = ir_left.is_detected()
        right_detected = ir_right.is_detected()

        if left_detected and right_detected:
            self.robot.move('forward', 50)
        elif left_detected:
            self.robot.move('left', 50)
        elif right_detected:
            self.robot.move('right', 50)
        else:
            self.robot.move('stop')

    def obstacle_avoidance(self):
        """장애물 회피"""
        us = self.robot.sensors.get('front_ultrasonic')
        if not us:
            return

        distance = us.get_distance()

        if distance < 20:
            self.robot.move('stop')
            time.sleep(0.5)
            self.robot.move('backward', 50)
            time.sleep(0.5)
            self.robot.move('left', 50)
            time.sleep(0.5)
        else:
            self.robot.move('forward', 50)

    def run(self, mode='line_following'):
        self.running = True
        while self.running:
            if mode == 'line_following':
                self.line_following()
            elif mode == 'obstacle_avoidance':
                self.obstacle_avoidance()
            time.sleep(0.01)

    def stop(self):
        self.running = False
        self.robot.move('stop')
```

## 4. 무선 통신

### 4.1 WiFi 설정

```bash
# WiFi 연결
nmcli dev wifi connect "SSID" password "PASSWORD"

# 고정 IP 설정
sudo vim /etc/dhcpcd.conf
# interface wlan0
# static ip_address=192.168.1.100/24
# static routers=192.168.1.1
# static domain_name_servers=8.8.8.8
```

### 4.2 Bluetooth 설정

```bash
# Bluetooth 활성화
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Bluetoothctl로 페어링
bluetoothctl
scan on
pair XX:XX:XX:XX:XX:XX
connect XX:XX:XX:XX:XX:XX
```

### 4.3 SSH 원격 제어

```bash
# SSH 서버 활성화
sudo apt install openssh-server
sudo systemctl enable ssh

# 원격에서 접속
# ssh username@192.168.1.100
```

### 4.4 Web 서버 기반 제어

```python
# Flask 기반 웹 서버
from flask import Flask, render_template, request
import threading

app = Flask(__name__)
robot = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control')
def control():
    command = request.args.get('command')
    if robot:
        robot.move(command)
    return 'OK'

def start_web_server():
    app.run(host='0.0.0.0', port=5000)

# 스레드에서 웹 서버 실행
web_thread = threading.Thread(target=start_web_server)
web_thread.daemon = True
web_thread.start()
```

## 5. 전원 관리

### 5.1 전원 소비 모니터링

```bash
# tegrastats로 모니터링
tegrastats -l 1000

# Python에서 모니터링
import subprocess

def get_power_stats():
    result = subprocess.run(['tegrastats'], capture_output=True, text=True)
    return result.stdout
```

### 5.2 배터리 관리

```python
class BatteryManager:
    def __init__(self, voltage_pin):
        self.pin = voltage_pin
        self.voltage_ref = 3.3  # 레퍼런스 전압
        self.max_voltage = 12.6  # 3S LiPo 최대

    def get_voltage(self):
        # ADC를 사용한 전압 측정 코드
        raw = GPIO.input(self.pin)
        voltage = (raw / 1024) * self.voltage_ref * 2  # 분압기 비율
        return voltage

    def get_percentage(self):
        voltage = self.get_voltage()
        percentage = (voltage / self.max_voltage) * 100
        return min(100, max(0, percentage))

    def is_low_battery(self):
        return self.get_voltage() < 10.5  # Low voltage cutoff
```

### 5.3 자동关机

```python
import schedule
import time

def check_battery():
    battery = BatteryManager(voltage_pin=...)

    if battery.is_low_battery():
        # 경고
        print("Low battery! Returning to base...")

        # 정지
        robot.move('stop')

        #Shutdown
        subprocess.run(['sudo', 'shutdown', '-h', 'now'])

# 스케줄러로 주기적 확인
schedule.every(1).minutes.do(check_battery)
```

## 6. 최종 통합 테스트

### 6.1 시스템 테스트 체크리스트

```
체크리스트:
[x] Jetson Nano 부팅 정상
[x] 카메라 동작 확인
[x] 모터 드라이버 연결
[x] 센서 연결
[x] 네트워크 연결
[x] 전원 공급 안정적
[x] 케이블 정리 완료
[x] 방열판/팬 동작
```

### 6.2 자율주행 테스트

```python
# 테스트 스크립트
def run_integration_test():
    print("=== Integration Test ===")

    # 1. 로봇 초기화
    robot = Robot()
    print("[1/5] Robot initialized")

    # 2. 카메라 테스트
    robot.init_camera('usb')
    img = robot.get_image()
    assert img is not None
    print("[2/5] Camera OK")

    # 3. 모터 테스트
    robot.move('forward', 30)
    time.sleep(1)
    robot.move('stop')
    print("[3/5] Motors OK")

    # 4. 센서 테스트
    robot.add_ultrasonic('front', trig=11, echo=13)
    dist = robot.sensors['front'].get_distance()
    print(f"[4/5] Sensor OK: {dist}cm")

    # 5. 자율주행 테스트
    controller = AutonomousController(robot)
    print("[5/5] Starting autonomous mode...")
    controller.run(mode='obstacle_avoidance')

    print("=== Test Complete ===")

run_integration_test()
```

## 7. 실습 과제

1. 모터 드라이버를 연결하고 테스트하세요.
2. 초음파 센서와 적외선 센서를 연결하세요.
3. Robot 클래스를 완성하세요.
4. 자율주행 기본 동작을 구현하세요.
5. 통합 테스트를 실행하세요.

## 8. 다음 실습 예고

다음 클래스에서는 ROS(Robot Operating System) 소개 및 설치를 진행합니다.