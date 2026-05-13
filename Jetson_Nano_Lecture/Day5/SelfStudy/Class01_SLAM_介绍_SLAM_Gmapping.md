# Class 01: SLAM 소개 및 SLAM(Gmapping) 실습

## 1. SLAM (Simultaneous Localization and Mapping)

### 1.1 SLAM 개념

SLAM은 로봇이 알지 못하는 환경에서 지도를 만들면서 동시에 자신의 위치를 추정하는 문제입니다.

```
SLAM Process:
┌─────────────────────────────────────┐
│                                      │
│  ① Sensor Data                      │
│     (Lidar, Camera, IMU)            │
│         │                            │
│         ▼                            │
│  ② Frontend (Odometry, Loop Closing)│
│         │                            │
│         ▼                            │
│  ③ Backend (Pose Graph Optimization)│
│         │                            │
│         ▼                            │
│  ④ Map Generation                   │
│     (Occupancy Grid / Point Cloud)  │
│                                      │
└─────────────────────────────────────┘
```

### 1.2 SLAM 알고리즘 유형

| 알고리즘 | 유형 | 특징 |
|----------|------|------|
| Gmapping | 2D Laser SLAM | Rao-Blackwellized PF, 실시간 |
| Cartographer | 2D/3D Laser SLAM | 서브맵 기반, 고품질 |
| ORB-SLAM | Visual SLAM | 카메라 기반 |
| LOAM | 3D Laser SLAM | 실시간 3D |

### 1.3 Occupancy Grid Map

```
Occupancy Grid:
┌─────────────────────────────────────┐
│ 0.0  0.1  0.0  0.0  0.0            │
│ 0.0  0.8  0.8  0.1  0.0            │
│ 0.0  1.0  1.0  0.0  0.0  ← Wall   │
│ 0.0  0.0  0.0  0.0  0.0            │
│ 0.0  0.0  0.0  0.0  0.0            │
│                                      │
│ Gray: Unknown                       │
│ Black: Occupied (확률 高)          │
│ White: Free (확률 低)              │
└─────────────────────────────────────┘
```

## 2. Gmapping 설치

### 2.1 의존성 설치

```bash
# 의존성 패키지
sudo apt install ros-noetic-slam-gmapping
sudo apt install ros-noetic-navigation
sudo apt install ros-noetic-rosbase

# 추가 패키지
sudo apt install ros-noetic-joy
sudo apt install ros-noetic-teleop-twist-keyboard
```

### 2.2 패키지 확인

```bash
# 설치 확인
dpkg -l | grep slam-gmapping
rospack find slam_gmapping
```

## 3. Gmapping 실습

### 3.1 실행 요구사항

```bash
# 필수 토픽
/scan           # sensor_msgs/LaserScan
/tf             # 좌표계 변환
/odom           # nav_msgs/Odometry (선택, 없으면 fake)
```

### 3.2 Gmappinglaunch

```xml
<!-- launch/gmapping.launch -->
<launch>
  <!-- Gmapping 노드 -->
  <node name="gmapping" pkg="slam_gmapping" type="slam_gmapping" output="screen">
    <!-- 파라미터 -->
    <param name="scan_topic" value="/scan"/>
    <param name="odom_frame" value="odom"/>
    <param name="base_frame" value="base_link"/>
    <param name="map_frame" value="map"/>

    <!-- 맵 해상도 (m/cell) -->
    <param name="delta" value="0.05"/>

    <!-- 맵 크기 -->
    <param name="xmin" value="-10"/>
    <param name="ymin" value="-10"/>
    <param name="xmax" value="10"/>
    <param name="ymax" value="10"/>

    <!-- 입자 필터 파라미터 -->
    <param name="particles" value="30"/>
    <param name="iterations" value="5"/>

    <!--</param>
    <param name="srr" value="0.01"/>
    <param name="srt" value="0.02"/>
    <param name="str" value="0.01"/>
    <param name="stt" value="0.02"/>
  </node>
</launch>
```

### 3.3 전체 SLAMlaunch

```xml
<!-- launch/robot_slam.launch -->
<launch>
  <!-- Robot Description -->
  <param name="robot_description" command="cat $(find my_robot)/urdf/robot.urdf"/>

  <!-- Robot State Publisher -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>

  <!-- Joint State Publisher -->
  <node name="joint_state_publisher" pkg="joint_state_publisher" type="joint_state_publisher"/>

  <!-- Motor Driver -->
  <node name="motor_driver" pkg="my_robot" type="motor_driver.py" output="screen"/>

  <!-- Odometry -->
  <node name="odometry_publisher" pkg="my_robot" type="odometry_publisher.py" output="screen"/>

  <!-- Gmapping -->
  <node name="gmapping" pkg="slam_gmapping" type="slam_gmapping" output="screen">
    <param name="delta" value="0.05"/>
  </node>

  <!-- Teleop -->
  <node name="teleop" pkg="teleop_twist_keyboard" type="teleop_twist_keyboard.py" output="screen"/>

  <!-- RViz -->
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/slam.rviz"/>
</launch>
```

### 3.4 RViz 설정

```bash
# Displays 설정:
# - Map > Topic: /map
# - RobotModel > Robot Description: robot_description
# - TF > Frame: odom, base_link, laser_link
# - LaserScan > Topic: /scan
# - Odometry > Topic: /odom
```

## 4. 맵 저장

### 4.1 map_server

```bash
# 맵 저장 (SLAM 실행 중)
rosservice call /dynamic_map "{}"

# map_server로 저장
rosrun map_server map_saver -f my_map

# 결과:
# my_map.pgm (맵 이미지)
# my_map.yaml (메타데이터)
```

### 4.2 YAML 파일

```yaml
# my_map.yaml
image: my_map.pgm
resolution: 0.05
origin: [-10.0, -10.0, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
```

## 5. 실습 실행

### 5.1 전체 실행

```bash
roslaunch my_robot robot_slam.launch
```

### 5.2 수동 제어

```bash
# 키보드 조종
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
# ↑↓: 전진/후진
# ←→: 회전
```

### 5.3 맵 저장

```bash
# 맵 저장
rosservice call /gmapping/get_map "{}"

# 또는
rosrun map_server map_saver -f ~/map
```

## 6. 실습 과제

1. Gmapping을 설치하고 실행하세요.
2. 키보드로 로봇을 조종하며 맵을 만드세요.
3. 완성된 맵을 저장하세요.
4. RViz에서 맵 생성과정을 확인하세요.

## 7. 다음 실습 예고

다음 클래스에서는 SLAM(Gmapping) 실습을 계속합니다.