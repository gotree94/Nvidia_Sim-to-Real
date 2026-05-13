# Class 03: ROS 주요 도구 및 로봇 Catkin 패키지

## 1. ROS 주요 도구

### 1.1 rqt_tools

```bash
# rqt 종합 도구
rqt

# 특정 도구 실행
rqt_graph           # 노드 그래프 시각화
rqt_plot            # 데이터 플롯
rqt_console         # 로그 콘솔
rqt_reconfigure     # 동적 파라미터
rqt_image_view      # 이미지 뷰어
rqt_bag             #bag 파일 뷰어
```

### 1.2 rviz

```bash
# RViz 실행
rviz
rviz -d my_config.rviz

# 설정에서 표시 가능한 것:
# - Robot Model
# - TF
# - LaserScan
# - PointCloud
# - Image
# - Map
# - Path
# - Pose
# - Odometry
```

### 1.3 Gazebo

```bash
# Gazebo 실행
gazebo
gzclient

# 빈 world 실행
roslaunch gazebo_ros empty_world.launch

# 특정 world 실행
roslaunch gazebo_ros playground.launch
```

### 1.4 명령줄 도구

```bash
# ROS Master
roscore                  # 마스터 실행
rosmaster               # 마스터 정보

# 패키지
rospack find <pkg>      # 패키지 경로
rospack list            # 패키지 목록
roscd <pkg>             # 패키지 디렉토리 이동
rosls <pkg>             # 패키지 파일 목록

# 노드
rosnode list            # 노드 목록
rosnode info <node>     # 노드 정보
rosnode kill <node>     # 노드 종료
rosnode ping <node>     # 노드 연결 테스트
rosnode machine         # 머신별 노드

# 토픽
rostopic list           # 토픽 목록
rostopic info <topic>  # 토픽 정보
rostopic type <topic>  # 토픽 타입
rostopic echo <topic>  # 토픽 메시지 출력
rostopic hz <topic>    # 토픽 주기
rostopic bw <topic>    # 토픽 대역폭
rostopic pub <topic>   # 토픽 Publishing

# 서비스
rosservice list        # 서비스 목록
rosservice info <srv>  # 서비스 정보
rosservice type <srv>  # 서비스 타입
rosservice call <srv>  # 서비스 호출

# 액션
rosaction list         # 액션 목록
rosaction info <action> # 액션 정보

# 파라미터
rosparam list          # 파라미터 목록
rosparam get <param>   # 파라미터 값 가져오기
rosparam set <param>   # 파라미터 값 설정
rosparam dump <file>   # 파라미터 저장
rosparam load <file>   # 파라미터 로드
rosparam delete <param> # 파라미터 삭제
```

### 1.5 rosbag

```bash
# Recording
rosbag record <topic1> <topic2>         # 특정 토픽 기록
rosbag record -a                        # 모든 토픽 기록
rosbag record -o <prefix>               # 출력 접두사

# Playback
rosbag play <bag_file>                  # 재생
rosbag play -r <rate>                  # 속도 조절
rosbag play -l                          # 루프 재생
rosbag play --clock                     # clockトピック送信

# Info
rosbag info <bag_file>                  # bag 정보
rosbag fix <old.bag> <new.bag>         # bag 수정
rosbag check <bag_file>                #bag 확인
```

## 2. tf (Transform)

### 2.1 tf 개념

tf는 좌표계 사이의 변환을 관리합니다. 로봇의 각 부분 간 위치 관계를 추적합니다.

```
좌표계 트리 예시:
┌─────────────────────────────────────┐
│             base_link               │
│        ┌────────┬────────┐         │
│        │        │        │         │
│    odom    laser_link   camera_link │
│                                  │
└─────────────────────────────────────┘
```

### 2.2 tf 사용

```python
import tf
import tf.transformations as transformations

# Listener 생성
listener = tf.TransformListener()

# 변환 조회
try:
    (trans, rot) = listener.lookupTransform('/base_link', '/laser_link', rospy.Time(0))
    print(f"Translation: {trans}")
    print(f"Rotation: {rot}")
except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    pass

# Broadcaster 생성
broadcaster = tf.TransformBroadcaster()

# 변환 보내기
broadcaster.sendTransform(
    (x, y, z),           # Translation
    (x, y, z, w),        # Rotation (quaternion)
    rospy.Time.now(),    # Timestamp
    child_frame,         # Child frame
    parent_frame         # Parent frame
)
```

### 2.3 tf2

```python
import tf2_ros
import geometry_msgs.msg

# tf2 Buffer 및 TransformListener
tf_buffer = tf2_ros.Buffer()
tf_listener = tf2_ros.TransformListener(tf_buffer)

# lookupTransform 사용
try:
    transform = tf_buffer.lookup_transform('base_link', 'laser_link', rospy.Time())
except tf2_ros.LookupException:
    pass
except tf2_ros.ConnectivityException:
    pass
except tf2_ros.ExtrapolationException:
    pass
```

## 3. URDF (Unified Robot Description Format)

### 3.1 URDF 기본 구조

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.16" radius="0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder length="0.16" radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Joints -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0.1 0.1 0" rpy="0 1.5707 0"/>
    <axis xyz="0 0 1"/>
  </joint>
</robot>
```

### 3.2 Joint 유형

| 유형 | 설명 | 사용 예시 |
|------|------|-----------|
| revolute | 회전 관절 (제한 각도) | 팔 관절 |
| continuous | 연속 회전 | 바퀴 |
| prismatic | 직선 이동 |Slider |
| fixed | 고정 | 프레임 |
| floating | 자유도 6 | 공중 드론 |
| planar | 평면 이동 | 이동 테이블 |

### 3.3 xacro 사용

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- 매개변수 -->
  <xacro:property name="PI" value="3.14159"/>
  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="base_mass" value="1.0"/>

  <!-- 매크로 -->
  <xacro:macro name="wheel_link" params="name">
    <link name="${name}">
      <visual>
        <geometry>
          <cylinder radius="${wheel_radius}" length="0.02"/>
        </geometry>
      </visual>
    </link>
  </xacro:macro>

  <!-- 사용 -->
  <xacro:wheel_link name="left_wheel"/>
  <xacro:wheel_link name="right_wheel"/>
</robot>
```

## 4. 로봇 Catkin 패키지 작성

### 4.1 패키지 생성

```bash
cd ~/catkin_ws/src

# 패키지 생성
catkin_create_pkg my_robot roscpp rospy std_msgs geometry_msgs nav_msgs sensor_msgs tf tf2 urdf joint_state_publisher robot_state_publisher

# 의존성 추가
rosdep install --from-paths . --ignore-src -r -y
```

### 4.2 패키지 구조

```bash
cd my_robot
mkdir -p launch config urdf scripts

# 확인
ls -la
```

### 4.3 URDF 작성

```xml
<!-- my_robot/urdf/my_robot.urdf -->
<?xml version="1.0"?>
<robot name="my_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Base Link -->
  <link name="base_footprint"/>
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.05" rpy="0 0 0"/>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
    </collision>
  </link>

  <joint name="base_footprint_joint" type="fixed">
    <parent link="base_footprint"/>
    <child link="base_link"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
  </joint>

  <!-- Wheels -->
  <link name="left_wheel">
    <visual>
      <origin xyz="0 0 0" rpy="1.5707 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0 0.1 -0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <link name="right_wheel">
    <visual>
      <origin xyz="0 0 0" rpy="1.5707 0 0"/>
      <geometry>
        <cylinder radius="0.05" length="0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0 -0.1 -0.05" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <!-- Laser Scanner -->
  <link name="laser_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" height="0.02"/>
      </geometry>
    </visual>
  </link>

  <joint name="laser_joint" type="fixed">
    <parent link="base_link"/>
    <child link="laser_link"/>
    <origin xyz="0.1 0 0.1" rpy="0 0 0"/>
  </joint>

</robot>
```

### 4.4 Launch 파일

```xml
<!-- my_robot/launch/robot.launch -->
<launch>
  <!-- 파라미터 로드 -->
  <param name="robot_description" command="cat $(find my_robot)/urdf/my_robot.urdf"/>

  <!-- Robot State Publisher -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher">
    <param name="publish_frequency" value="10.0"/>
  </node>

  <!-- Joint State Publisher -->
  <node name="joint_state_publisher" pkg="joint_state_publisher" type="joint_state_publisher"/>

  <!-- RViz -->
  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot)/config/robot.rviz"/>

  <!-- Gazebo 시뮬레이션 (선택) -->
  <!-- <include file="$(find gazebo_ros)/launch/empty_world.launch"/> -->
</launch>
```

## 5. 실습 과제

1. rqt_graph를 사용하여 노드 관계를 확인하세요.
2. URDF를 작성하여 간단한 로봇을 정의하세요.
3. xacro를 사용하여 URDF를 모듈화하세요.
4. Robot State Publisher를 사용하여 URDF를 시각화하세요.

## 6. 다음 실습 예고

다음 클래스에서는 로봇 Catkin 패키지 실습을 계속합니다.