# Class 02: SLAM(Gmapping) 실습

## 1. Gmapping 상세 설정

### 1.1 주요 파라미터

```xml
<!-- Gmapping 파라미터 -->
<node name="gmapping" pkg="slam_gmapping" type="slam_gmapping">
  <!-- 스캔 토픽 -->
  <param name="scan_topic" value="/scan"/>

  <!-- 좌표계 -->
  <param name="odom_frame" value="odom"/>
  <param name="base_frame" value="base_link"/>
  <param name="map_frame" value="map"/>

  <!-- 맵 해상도 (m/cell) -->
  <param name="delta" value="0.05"/>

  <!-- 입자 수 (더 많으면 정밀하지만 느림) -->
  <param name="particles" value="30"/>

  <!-- 최대 범위 (m) -->
  <param name="maxUrange" value="3.0"/>

  <!-- 최소 스캔 거리 -->
  <param name="minUrange" value="0.2"/>

  <!-- 스캔 매칭 파라미터 -->
  <param name="llsamplerange" value="0.05"/>
  <param name="llsamplestep" value="0.05"/>
  <param name="lasamplerange" value="0.05"/>
  <param name="lasamplestep" value="0.05"/>

  <!--===
  <!-- 입자 필터 -->
  <param name="iterations" value="5"/>
  <param name="resampleThreshold" value="0.5"/>

  <!-- 초기 자세 -->
  <param name="xmin" value="-10.0"/>
  <param name="ymin" value="-10.0"/>
  <param name="xmax" value="10.0"/>
  <param name="ymax" value="10.0"/>

  <!-- 부트스트래핑 -->
  <param name="linearError" value="0.05"/>

  <!-- odomNoise -->
  <param name="srr" value="0.1"/>
  <param name="srt" value="0.1"/>
  <param name="str" value="0.1"/>
  <param name="stt" value="0.1"/>
</node>
```

### 1.2 파라미터 튜닝

```bash
# 동적 파라미터 설정
rosrun rqt_reconfigure rqt_reconfigure

# 또는命令行에서 설정
rosparam set /gmapping/particles 50
rosparam set /gmapping/maxUrange 5.0
```

## 2. 문제 해결

### 2.1 Localization 문제

```
증상: 로봇이 맵에서 잘못된 위치에 표시됨
해결:
1. Odometry 확인 (/odom)
2. base_frame 확인
3. TF 관계 확인 (rosrun tf tf_echo odom base_link)
```

### 2.2 맵 품질 문제

```
증상: 맵이 깨지거나 왜곡됨
해결:
1. 입자 수 증가 (particles)
2. 스캔 매칭 파라미터 조정
3. 이동 속도 감소
4. 스캔 주기 확인
```

### 2.3 Real-time 문제

```
증상: SLAM이跟不上 로봇 속도
해결:
1. maxUrange 감소
2. particles 감소
3. map 크기 감소
4.laser帧率提高
```

## 3. Gazebo 시뮬레이션

### 3.1 Gazebo 환경

```bash
# Gazebo 실행
roslaunch gazebo_ros empty_world.launch

# Turtlebot 예시
roslaunch turtlebot3_gazebo turtlebot3_world.launch
```

### 3.2 Gazebo SLAM

```xml
<!-- launch/gazebo_slam.launch -->
<launch>
  <!-- Gazebo -->
  <include file="$(find gazebo_ros)/launch/empty_world.launch"/>

  <!-- Turtlebot3 -->
  <include file="$(find turtlebot3_gazebo)/launch/robot.launch"/>

  <!-- SLAM -->
  <include file="$(find turtlebot3_slam)/launch/slam.launch"/>
</launch>
```

### 3.3 시뮬레이션 테스트

```bash
# 키보드 조종
roslaunch turtlebot3_teleop turtlebot3_keyboard.launch

# 또는
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

# 맵 저장
rosrun map_server map_saver -f ~/test_map
```

## 4. 맵 관리

### 4.1 맵 로드

```bash
# 맵 서버 실행
rosrun map_server map_server ~/test_map.yaml

# 또는 launch 파일
<node name="map_server" pkg="map_server" type="map_server" args="$(find my_robot)/maps/test_map.yaml"/>
```

### 4.2 맵 서비스

```bash
# dynamic_map 서비스
rosservice call /dynamic_map "{}"

# 메타데이터
rostopic echo /map_metadata
```

### 4.3 맵 변환

```bash
# PGM → PNG 변환
convert my_map.pgm my_map.png

# 맵 편집 (GIMP, ImageMagick)
```

## 5. 실습: 실제 환경 SLAM

### 5.1 환경 설정

```bash
# 라이다 연결 확인
ls /dev/ttyUSB0

# 권한 설정
sudo chmod 666 /dev/ttyUSB0
```

### 5.2 노드 실행

```bash
# 1. ROS Master
roscore

# 2. 라이다 드라이버
roslaunch rplidar_ros rplidar.launch

# 3. 모터 드라이버
roslaunch my_robot motor_driver.launch

# 4. Odometry
roslaunch my_robot odometry.launch

# 5. Gmapping
roslaunch my_robot slam_gmapping.launch

# 6. RViz
rviz -d $(find my_robot)/config/slam.rviz
```

### 5.3 SLAM 실행

```bash
# 키보드로 조종하며 맵 생성
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

# 맵 저장
rosrun map_server map_saver -f ~/my_map

# 저장 확인
ls ~/my_map.*
# my_map.pgm
# my_map.yaml
```

## 6. 실습 과제

1. Gmapping 파라미터를 조정하며 차이를 확인하세요.
2. Gazebo 시뮬레이션에서 SLAM을 실행하세요.
3. 실제 환경에서 맵을 생성하고 저장하세요.
4. 저장한 맵을 다시 로드하여Localization을 테스트하세요.

## 7. 다음 실습 예고

다음 클래스에서는 Navigation에 대해 학습합니다.