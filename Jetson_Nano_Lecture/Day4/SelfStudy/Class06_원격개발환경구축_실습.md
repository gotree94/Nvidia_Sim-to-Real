# Class 06: 원격 개발 환경 구축 실습

## 1. Jetson Nano 원격 환경 설정

### 1.1 네트워크 설정

```bash
# Jetson Nano에서
# 고정 IP 설정 (/etc/dhcpcd.conf)
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=8.8.8.8

# WiFi 설정
sudo nmcli device wifi connect "YourSSID" password "YourPassword"
```

### 1.2 ROS 환경 설정

```bash
# Jetson Nano에서
# ~/.bashrc에 추가
echo 'export ROS_MASTER_URI=http://localhost:11311' >> ~/.bashrc
echo 'export ROS_HOSTNAME=192.168.1.100' >> ~/.bashrc
source ~/.bashrc
```

### 1.3 PC 설정

```bash
# Developer PC에서
# ~/.bashrc에 추가
export ROS_MASTER_URI=http://192.168.1.100:11311
export ROS_HOSTNAME=192.168.1.50
source ~/.bashrc
```

## 2. Catkin 도구 설치

### 2.1 catkin_tools 설치

```bash
# Jetson Nano에서
sudo apt install python3-catkin-tools

# 사용법
catkin build              # 패키지 빌드
catkin clean             # 빌드 캐시 정리
catkin list              # 패키지 목록
catkin config            # 빌드 설정
```

### 2.2 빌드 최적화

```bash
# 병렬 빌드
catkin build -j4

# 특정 패키지만 빌드
catkin build <package_name>

# 빌드 로그 저장
catkin build -v > build.log 2>&1
```

## 3. 원격 실행 실습

### 3.1 원격 노드 실행

```bash
# PC에서
# ROS Master는 이미 로봇에서 실행 중이라고 가정

# 원격 노드 실행
rosrun <package> <node>

# 예시
rosrun roscpp_tutorials listener
```

### 3.2 원격 토픽 확인

```bash
# PC에서
rostopic list
rostopic hz /scan
rostopic echo /cmd_vel
```

### 3.3 원격 파라미터

```bash
# PC에서
rosparam get /robot_name
rosparam set /max_speed 1.0
```

## 4. RViz 원격 사용

### 4.1 rviz 실행

```bash
# PC의 RViz에서 로봇 데이터 표시
rviz

# 설정:
# - Fixed Frame: /odom 또는 /base_footprint
# - RobotModel 로드
# - TF 표시
```

### 4.2 이미지 전송 최적화

```bash
# 이미지 압축 (네트워크 대역폭 절약)
# image_transport 사용
rosrun image_transport republish compressed in:=/camera/image_raw out:=/camera/image_raw/compressed
```

## 5. 디버깅 도구

### 5.1 roswtf

```bash
# ROS 분석 도구
roswtf
roswtf --fix-plugins
```

### 5.2 roslaunch 디버깅

```bash
# 상세 출력
roslaunch --debug <package> <launch_file>

#_screen으로 모든 출력
roslaunch <package> <launch_file> screen:=true
```

### 5.3 네트워크 디버깅

```bash
# 연결 상태 확인
rosmaster

# XMLRPC 연결 테스트
rostopic pub /test std_msgs/String "data: 'test'" -v
```

## 6. praktische 개발 워크플로우

### 6.1 코드 개발

```python
# ~/catkin_ws/src/my_robot/src/motor_driver.py
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

class MotorDriver:
    def __init__(self):
        rospy.init_node('motor_driver')
        rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)
        # GPIO 초기화 코드

        rospy.spin()

    def cmd_callback(self, msg):
        # 속도 명령 처리
        linear = msg.linear.x
        angular = msg.angular.z

        # 모터 제어 코드
        rospy.loginfo(f"Speed: {linear}, Turn: {angular}")

if __name__ == '__main__':
    MotorDriver()
```

### 6.2 빌드 및 테스트

```bash
# 빌드
cd ~/catkin_ws
catkin build

# 실행
rosrun my_robot motor_driver.py

# 로그 확인
rqt_console
```

### 6.3 디버깅

```bash
# 노드 정보
rosnode list
rosnode info /motor_driver

# 토픽 확인
rostopic echo /cmd_vel
rostopic hz /cmd_vel
```

## 7. 개발 환경 자동화

### 7.1launch 스크립트

```bash
#!/bin/bash
# start_robot.sh

echo "ROS Master 시작..."
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

# 노드 실행
rosrun my_robot motor_driver.py &
rosrun my_robot sensor_reader.py &

echo "로봇 노드 실행 완료"
```

### 7.2一键 실행

```bash
# 원격에서一键 실행 스크립트 작성
ssh ubuntu@192.168.1.100 '~/catkin_ws/start_robot.sh'
```

## 8. 실습 과제

1. PC에서 Jetson Nano로 SSH 연결을 설정하세요.
2. 원격에서 ROS 노드를 실행하고 토픽을 확인하세요.
3. RViz를 사용하여 원격 로봇을 시각화하세요.
4. 개발 워크플로우를 자동화하는 스크립트를 작성하세요.

## 9. 다음 실습 예고

다음 클래스에서는 Rviz, Odometry, TF에 대해 학습합니다.