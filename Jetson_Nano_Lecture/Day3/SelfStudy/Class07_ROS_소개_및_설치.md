# Class 07: ROS 소개 및 설치

## 1. ROS(Robot Operating System) 개요

### 1.1 ROS란?

ROS는 로보틱스를 위한 메타 운영체제입니다. 하드웨어 추상화, 장치 드라이버, 라이브러리, 시각화 도구, 메시지 전달, 패키지 관리 등 로봇 소프트웨어 개발에 필요한 기능을 제공합니다.

### 1.2 ROS的历史

```
ROS 버전:
┌─────────────────────────────────────┐
│ ROS 1 (Legacy)                      │
│ - ROS Groovy (2010)                 │
│ - ROS Hydro (2013)                 │
│ - ROS Indigo (2014)                 │
│ - ROS Kinetic (2016)               │
│ - ROS Melodic (2018)               │
│ - ROS Noetic (2020)                │
├─────────────────────────────────────┤
│ ROS 2 (新一代)                      │
│ - ROS 2 Ardent (2017)              │
│ - ROS 2 Bouncy (2018)              │
│ - ROS 2 Crystal (2019)            │
│ - ROS 2 Dashing (2019)             │
│ - ROS 2 Foxy (2020)                │
│ - ROS 2 Galactic (2021)            │
│ - ROS 2 Humble (2022) - LTS        │
└─────────────────────────────────────┘
```

### 1.3 ROS 특징

- **메시지 기반 통신**: 토픽, 서비스, 액션
- **분산 처리**: 다중 노드 실행
- **패키지 시스템**: 재사용성
- **도구 지원**: RViz, rqt, Gazebo
- **커뮤니티**: 방대한 생태계

## 2. ROS 아키텍처

### 2.1 노드와 토픽

```
ROS Computation Graph:
┌─────────────────────────────────────┐
│                                       │
│  ┌───────────┐   /cmd_vel   ┌───────┐│
│  │  Teleop  │ ──────────▶ │ turtle ││
│  │  Node   │              │  bot  ││
│  └───────────┘              └───────┘│
│        │                            │
│        │ /scan          /odom       │
│        ▼                            ▼
│  ┌───────────┐              ┌───────┐│
│  │  Laser   │              │ Nav   ││
│  │ Scanner  │              │ Stack ││
│  └───────────┘              └───────┘│
│                                       │
└─────────────────────────────────────┘
```

### 2.2 메시지 유형

```msg
# 표준 메시지 예시
geometry_msgs/Twist.msg
---
geometry_msgs/Vector3 linear
geometry_msgs/Vector3 angular

sensor_msgs/LaserScan.msg
---
Header header
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities
```

### 2.3 ROS 파일 시스템

```
ROS Package Structure:
┌─────────────────────────────────────┐
│ my_robot_package/                   │
│ ├── CMakeLists.txt                  │
│ ├── package.xml                     │
│ ├── src/                            │
│ │   └── my_node.cpp                 │
│ ├── launch/                         │
│ │   └── robot.launch                │
│ ├── msg/                            │
│ │   └── MyMessage.msg               │
│ ├── srv/                            │
│ │   └── MyService.srv               │
│ └── scripts/                        │
│     └── my_script.py                │
└─────────────────────────────────────┘
```

## 3. Jetson에 ROS 설치

### 3.1 ROS Melodic 설치 (Ubuntu 18.04)

```bash
# sources.list 설정
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# 키 추가
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B882B7EA7BA27222D6B832

# 패키지 업데이트
sudo apt update

# ROS 설치
sudo apt install ros-melodic-ros-base
sudo apt install ros-melodic-ros-base-dbg

# rosdep 초기화
sudo rosdep init
rosdep update

# 환경 설정
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 3.2 ROS Noetic 설치 (Ubuntu 20.04)

```bash
# sources.list 설정
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# 키 추가
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B882B7EA7BA27222D6B832

# 패키지 업데이트
sudo apt update

# ROS Noetic 설치
sudo apt install ros-noetic-ros-base

# 환경 설정
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 3.3 패키지 설치

```bash
# 필수 패키지
sudo apt install python3-rosdep python3-rosinstall python3-roslaunch

# 추가 패키지
sudo apt install \
    ros-melodic-ros-comm \
    ros-melodic-roslint \
    ros-melodic-rviz \
    ros-melodic-gazebo-ros-pkg \
    ros-melodic-navigation

#_catkin_tools 설치
sudo apt install python3-catkin-tools
```

## 4. ROS 기본 사용

### 4.1工作空间 설정

```bash
# catkin 작업 공간 생성
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin init

# 환경 설정
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 4.2 패키지 생성

```bash
cd ~/catkin_ws/src
catkin_create_pkg my_robot_pkg std_msgs rospy roscpp

# 빌드
cd ~/catkin_ws
catkin build
```

### 4.3 노드 실행

```bash
# ROS 마스터 실행
roscore

# 다른 터미널에서 노드 실행
rosrun my_robot_pkg my_node.py

# 토픽 목록 확인
rostopic list

# 토픽 정보
rostopic info /chatter

# 토픽 메시지 확인
rostopic echo /chatter
```

### 4.4-launch 파일

```xml
<!-- robot.launch -->
<launch>
  <param name="robot_name" value="my_robot" />

  <!-- 노드 실행 -->
  <node name="motor_driver" pkg="my_robot_pkg" type="motor_driver" output="screen"/>

  <!-- 파라미터 로드 -->
  <rosparam file="$(find my_robot_pkg)/config/params.yaml" command="load"/>

  <!-- launch 파일 중첩 -->
  <include file="$(find other_pkg)/other.launch"/>
</launch>
```

## 5. ROS 기본 예제

### 5.1 Publisher 노드

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10Hz

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
```

### 5.2 Subscriber 노드

```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " I heard %s", data.data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
```

### 5.3 Publisher/Subscriber_launch

```xml
<launch>
  <node name="talker" pkg="beginner_tutorials" type="talker.py" output="screen"/>
  <node name="listener" pkg="beginner_tutorials" type="listener.py" output="screen"/>
</launch>
```

## 6. ROS 도구

### 6.1 rqt_graph

```bash
# 노드 그래프 시각화
rqt_graph
# 또는
rosrun rqt_graph rqt_graph
```

### 6.2 RViz

```bash
# 3D 시각화 도구
rviz
# 또는
rosrun rviz rviz
```

### 6.3 Gazebo

```bash
# 시뮬레이터
roslaunch gazebo_ros empty_world.launch
# 또는
gazebo
```

### 6.4 명령줄 도구

```bash
# 패키지 관련
rospack find <package>
rospack list
roscd <package>

# 노드 관련
rosnode list
rosnode info <node>
rosnode kill <node>

# 토픽 관련
rostopic list
rostopic hz <topic>
rostopic type <topic>

# 서비스 관련
rosservice list
rosservice call <service>
```

## 7. ROS + Jetson 통합

### 7.1 Jetson용 ROS 노드

```python
# Jetson 하드웨어 접근
import rospy
import Jetson.GPIO as GPIO

class MotorNode:
    def __init__(self):
        rospy.init_node('motor_driver')
        self.sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_callback)

        # GPIO 초기화
        # ... 모터 드라이버 설정

    def cmd_callback(self, msg):
        # 속도 명령 처리
        linear = msg.linear.x
        angular = msg.angular.z
        # 모터 제어 로직

    def run(self):
        rospy.spin()
```

### 7.2 카메라 토픽

```python
import rospy
from sensor_msgs.msg import Image
import cv2

class CameraNode:
    def __init__(self):
        rospy.init_node('camera_publisher')
        self.pub = rospy.Publisher('/camera/image', Image, queue_size=10)
        self.cap = cv2.VideoCapture(0)

    def run(self):
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if ret:
                # OpenCV → ROS Image 변환
                msg = Image()
                msg.header.stamp = rospy.Time.now()
                # ... 이미지 데이터 설정
                self.pub.publish(msg)
            rate.sleep()

if __name__ == '__main__':
    node = CameraNode()
    node.run()
```

## 8. 실습 과제

1. Jetson에 ROS를 설치하세요.
2. catkin 작업 공간을 생성하세요.
3. 간단한 Publisher/Subscriber를 작성하세요.
4. rqt_graph로 노드 관계를 확인하세요.
5. ROS와 하드웨어를 연동하는 예제를 작성하세요.

## 9. 다음 실습 예고

다음 클래스에서는 Jetson ROS 설치를 완료하고 실습을 진행합니다.