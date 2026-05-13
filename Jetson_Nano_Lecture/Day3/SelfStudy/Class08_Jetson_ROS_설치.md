# Class 08: Jetson ROS 설치 실습

## 1. Jetson ROS 상세 설치

### 1.1 JetPack 기반 ROS 설치

```bash
# Jetson 모델 확인
cat /proc/device-tree/model
# 또는
tegrastats

# Ubuntu 버전 확인
cat /etc/lsb-release
# DISTRIB_DESCRIPTION="Ubuntu 18.04.6 LTS"

# Jetson용 ROS 설치 (JetPack 4.6 - Ubuntu 18.04 기준)
sudo apt update
sudo apt install -y curl

# ROS 저장소 추가
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros-latest.list'

sudo apt update
sudo apt install -y ros-melodic-ros-base

# ROS 환경 설정
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 1.2 필수 패키지 설치

```bash
# Python 및 빌드 도구
sudo apt install -y \
    python3-pip \
    python3-rosdep \
    python3-catkin-tools \
    build-essential \
    git

# Jetson 하드웨어 패키지
sudo apt install -y \
    ros-melodic-raspicam-node \
    ros-melodic-image-transport-plugins \
    ros-melodic-vision-opencv

# 통신 패키지
sudo apt install -y \
    ros-melodic-ros-comm \
    ros-melodic-topic-tools
```

### 1.3 rosdep 설정

```bash
# rosdep 초기화
sudo rosdep init

# 의존성 설치
rosdep update

# 패키지 의존성 설치
rosdep install --from-paths ~/catkin_ws/src --ignore-src -r -y
```

## 2. CUDA 지원 ROS

### 2.1 cv_bridge 설치

```bash
# cv_bridge 설치
sudo apt install -y ros-melodic-cv-bridge

# 소스에서 설치 (CUDA 지원)
cd ~/catkin_ws/src
git clone https://github.com/ros-perception/vision_opencv.git
cd vision_opencv
git checkout melodic

# CMakeLists.txt 수정 (CUDA 활성화)
# find_package(CUDA REQUIRED)
# add_definitions(-DCUDA_ENABLED)

cd ~/catkin_ws
catkin_make
```

### 2.2 CUDA 확장 메시지

```python
# CUDA 지원 이미지 메시지 사용
from sensor_msgs.msg import Image
import cv_bridge
import cupy as cp

bridge = cv_bridge.CvBridge()

def gpu_process_image(msg):
    # CPU → GPU
    img = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
    gpu_img = cp.asarray(img)

    # GPU에서 처리
    gpu_result = gpu_img * 1.5  # 예: 밝기 조절

    # GPU → CPU
    result = cp.asnumpy(gpu_result)

    return bridge.cv2_to_imgmsg(result, encoding='bgr8')
```

## 3. Jetson 전용 ROS 패키지

### 3.1 NVIDIA ROS 패키지

```bash
# NVIDIA Isaac ROS Packages
# https://github.com/NVIDIA-ISAAC-ROS

# Isaac ROS 퍼셉션
cd ~/catkin_ws/src
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvargus_camera.git

# 의존성 설치
sudo apt install -y \
    libcuda \
    libcudnn

cd ~/catkin_ws
catkin_make
```

### 3.2 Jetson Stats

```bash
# jetson-stats 설치
pip3 install jetson-stats

# ROS 노드에서 사용
from jtop import jtop

with jtop() as jetson:
    print(f"CPU: {jetson.cpu['cpu']}")
    print(f"GPU: {jetson.gpu['util']}")
    print(f"RAM: {jetson.ram['use']/jetson.ram['tot']*100:.1f}%")
```

## 4. ROS 노드 작성 실습

### 4.1摄像头 노드

```python
#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class CameraPublisher:
    def __init__(self):
        rospy.init_node('camera_publisher')
        self.pub = rospy.Publisher('/usb_cam/image_raw', Image, queue_size=1)
        self.bridge = CvBridge()

        # 비디오 캡처 초기화
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            if ret:
                try:
                    msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                    msg.header.stamp = rospy.Time.now()
                    self.pub.publish(msg)
                except Exception as e:
                    rospy.logerr(e)

            rate.sleep()

        self.cap.release()

if __name__ == '__main__':
    try:
        CameraPublisher()
    except rospy.ROSInterruptException:
        pass
```

### 4.2 모터 제어 노드

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO

class MotorController:
    def __init__(self):
        rospy.init_node('motor_controller')
        self.sub = rospy.Cmd_vel('/cmd_vel', self.cmd_callback)

        # GPIO 초기화
        self.IN1 = 11
        self.IN2 = 13
        self.IN3 = 15
        self.IN4 = 16
        self.ENA = 12
        self.ENB = 18

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup([self.IN1, self.IN2, self.IN3, self.IN4, self.ENA, self.ENB], GPIO.OUT)
        self.pwm_left = GPIO.PWM(self.ENA, 1000)
        self.pwm_right = GPIO.PWM(self.ENB, 1000)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

        rospy.spin()

    def cmd_callback(self, msg):
        linear = msg.linear.x
        angular = msg.angular.z

        # Differential Drive 모델
        left_speed = (linear - angular) * 100
        right_speed = (linear + angular) * 100

        # 모터 제어
        if left_speed > 0:
            GPIO.output(self.IN1, True)
            GPIO.output(self.IN2, False)
        else:
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, True)

        if right_speed > 0:
            GPIO.output(self.IN3, True)
            GPIO.output(self.IN4, False)
        else:
            GPIO.output(self.IN3, False)
            GPIO.output(self.IN4, True)

        self.pwm_left.ChangeDutyCycle(abs(left_speed))
        self.pwm_right.ChangeDutyCycle(abs(right_speed))

    def on_shutdown(self):
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    node = MotorController()
```

## 5..launch 파일 작성

### 5.1 기본.launch

```xml
<launch>
  <!-- 노드 정의 -->
  <node name="camera_publisher" pkg="my_robot" type="camera_node.py" output="screen">
    <param name="camera_id" value="0"/>
    <param name="frame_rate" value="30"/>
  </node>

  <node name="motor_controller" pkg="my_robot" type="motor_node.py" output="screen">
    <param name="max_speed" value="1.0"/>
  </node>

  <!-- RViz 실행 -->
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/robot.rviz"/>
</launch>
```

### 5.2 카메라+모터.launch

```xml
<launch>
  <!-- USB 카메라 -->
  <node name="usb_cam" pkg="usb_cam" type="usb_cam_node" output="screen">
    <param name="video_device" value="/dev/video0"/>
    <param name="image_width" value="640"/>
    <param name="image_height" value="480"/>
    <param name="pixel_format" value="yuyv"/>
  </node>

  <!--_image_transport 변환 -->
  <node name="image_view" pkg="image_view" type="image_view">
    <remap from="image" to="/usb_cam/image_raw"/>
  </node>

  <!-- 모터 제어 -->
  <node name="teleop_key" pkg="teleop_twist_keyboard" type="teleop_twist_keyboard.py" output="screen"/>
</launch>
```

### 5.3 Gazebo 시뮬레이션.launch

```xml
<launch>
  <!-- Gazebo 시뮬레이터 -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name" value="$(find my_robot)/worlds/robot.world"/>
  </include>

  <!-- 로봇 모델 로드 -->
  <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model">
    <param name="robot_description" textfile="$(find my_robot)/urdf/robot.urdf"/>
    <param name="robot_name" value="my_robot"/>
  </node>

  <!-- ROS 제어 -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>
</launch>
```

## 6. NVCS/Isaac ROS 실습

### 6.1 Isaac ROS 설치

```bash
# Isaac ROS 필수 요구사항
# - JetPack 5.0 이상
# - ROS 2 Humble
# - CUDA 11.x

# Isaac ROS 설치 (Ubuntu 20.04 기준)
cd /opt/nvidia
sudo ./install_isaac_ros.sh

# 또는 개별 패키지 설치
cd ~/ros2_ws
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_nvargus_camera.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_image_pipeline.git
git clone https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam.git
```

### 6.2 Isaac 카메라 노드

```bash
# Isaac ROS 카메라 예시
ros2 run isaac_ros_nvargus_camera argus_camera_node

# 또는 launch 파일로 실행
ros2 launch isaac_ros_nvargus_camera isaac_nvargus_camera.launch.py
```

## 7. ROS 네트워크 설정

### 7.1 다중 기기 연결

```bash
# Master 설정 (로봇)
export ROS_MASTER_URI=http://192.168.1.100:11311
export ROS_HOSTNAME=192.168.1.100

# Remote 설정 (PC)
export ROS_MASTER_URI=http://192.168.1.100:11311
export ROS_HOSTNAME=192.168.1.50
```

### 7.2 네트워크 테스트

```bash
# Master에서
roscore

# Remote에서
rostopic list  # Master 토픽 확인
rosrun roscpp_tutorials listener  # Listener 시작

# Master에서
rosrun roscpp_tutorials talker  # Talker 시작
```

## 8. 통합 테스트

### 8.1 전체 시스템.launch

```xml
<launch>
  <!-- ROS 마스터는 별도 실행 -->

  <!-- 카메라 -->
  <node name="camera" pkg="my_robot" type="camera_node.py" output="screen"/>

  <!-- 모터 -->
  <node name="motors" pkg="my_robot" type="motor_node.py" output="screen"/>

  <!-- 인코더 -->
  <node name="encoders" pkg="my_robot" type="encoder_node.py" output="screen"/>

  <!-- 센서 -->
  <node name="sensors" pkg="my_robot" type="sensor_node.py" output="screen"/>

  <!-- 라이다 (있는 경우) -->
  <node name="laser" pkg="rplidar_ros" type="rplidarNode" output="screen"/>

  <!-- SLAM -->
  <node name="slam_toolbox" pkg="slam_toolbox" type="async_slam_launch.py" output="screen"/>

  <!-- RViz -->
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/nav.rviz"/>
</launch>
```

### 8.2 테스트 실행

```bash
# 1. roscore 실행
roscore

# 2. launch 파일 실행
roslaunch my_robot robot.launch

# 3. 토픽 확인
rostopic list
rostopic hz /camera/image_raw
rostopic echo /odom

# 4. rqt 실행
rqt
rqt_graph
```

## 9. 실습 과제

1. Jetson에 ROS를 설치하고 환경을 설정하세요.
2. USB 카메라에서 이미지를 publish하는 노드를 작성하세요.
3. cmd_vel을 구독하여 모터를 제어하는 노드를 작성하세요.
4. launch 파일을 작성하여 여러 노드를 한번에 실행하세요.
5. RViz에서 로봇 상태를 시각화하세요.

## 10. 마무리

이제까지 Jetson Nano에서 ROS를 설치하고 기본적인 로봇 제어 시스템을 구축했습니다. 더 많은 기능을 위해서는 다음을 학습하세요:

- Navigation Stack (SLAM, 경로 계획)
- MoveIt! ( motion planning)
- Gazeo 시뮬레이션
-Isaac ROS (고성능 AI)