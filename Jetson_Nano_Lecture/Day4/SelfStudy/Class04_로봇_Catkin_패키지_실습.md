# Class 04: 로봇 Catkin 패키지 실습

## 1. 실습: 전체 로봇 패키지 구축

### 1.1 패키지 구조 생성

```bash
cd ~/catkin_ws/src

# 종합 로봇 패키지 생성
catkin_create_pkg my_robot_description \
    roscpp \
    rospy \
    std_msgs \
    geometry_msgs \
    nav_msgs \
    sensor_msgs \
    tf \
    tf2 \
    urdf \
    xacro \
    joint_state_publisher \
    robot_state_publisher

# 디렉토리 구조
cd my_robot_description
mkdir -p launch config urdf/xacro rviz
```

### 1.2 xacro 파일 작성

```xml
<!-- urdf/xacro/robot_base.xacro -->
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="mobile_robot">

  <!-- 상수 정의 -->
  <xacro:property name="PI" value="3.14159265359"/>
  <xacro:property name="base_mass" value="5.0"/>
  <xacro:property name="base_radius" value="0.15"/>
  <xacro:property name="base_height" value="0.1"/>
  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="wheel_width" value="0.03"/>
  <xacro:property name="wheel_mass" value="0.5"/>
  <xacro:property name="wheel_separation" value="0.2"/>
  <xacro:property name="laser_height" value="0.15"/>

  <!-- Base Link -->
  <link name="base_footprint">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.01 0.01 0.01"/>
      </geometry>
    </visual>
  </link>

  <link name="base_link">
    <inertial>
      <mass value="${base_mass}"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="${base_mass/12*(base_radius*base_radius*2)}" ixy="0" ixz="0"
                iyy="${base_mass/12*(3*base_radius*base_radius+base_height*base_height)}" iyz="0"
                izz="${base_mass/12*(3*base_radius*base_radius+base_height*base_height)}"/>
    </inertial>
    <visual>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="${base_radius}" length="${base_height}"/>
      </geometry>
      <material name="blue">
        <color rgba="0.2 0.2 0.8 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 ${base_height/2}" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="${base_radius}" length="${base_height}"/>
      </geometry>
    </collision>
  </link>

  <joint name="base_footprint_joint" type="fixed">
    <parent link="base_footprint"/>
    <child link="base_link"/>
    <origin xyz="0 0 ${base_height}" rpy="0 0 0"/>
  </joint>

  <!-- Wheel Macro -->
  <xacro:macro name="wheel" params="name x y">
    <link name="${name}">
      <inertial>
        <mass value="${wheel_mass}"/>
        <origin xyz="0 0 0" rpy="0 0 0"/>
        <inertia ixx="${wheel_mass/12*(3*wheel_radius*wheel_radius+wheel_width*wheel_width)}" ixy="0" ixz="0"
                  iyy="${wheel_mass/12*(3*wheel_radius*wheel_radius+wheel_width*wheel_width)}" iyz="0"
                  izz="${wheel_mass/2*wheel_radius*wheel_radius}"/>
      </inertial>
      <visual>
        <origin xyz="0 0 0" rpy="${PI/2} 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
        <material name="black">
          <color rgba="0.1 0.1 0.1 1.0"/>
        </material>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="${PI/2} 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>
    </link>

    <joint name="${name}_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${name}"/>
      <origin xyz="${x} ${y} ${-base_height/4}" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
      <dynamics damping="0.7" friction="0.5"/>
    </joint>
  </xacro:macro>

  <!-- Wheels -->
  <xacro:wheel name="front_left_wheel" x="${wheel_separation/2}" y="${wheel_separation/2}"/>
  <xacro:wheel name="front_right_wheel" x="${wheel_separation/2}" y="-${wheel_separation/2}"/>
  <xacro:wheel name="back_left_wheel" x="-${wheel_separation/2}" y="${wheel_separation/2}"/>
  <xacro:wheel name="back_right_wheel" x="-${wheel_separation/2}" y="-${wheel_separation/2}"/>

  <!-- Laser Scanner -->
  <link name="laser_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.05"/>
      </geometry>
      <material name="darkgrey">
        <color rgba="0.3 0.3 0.3 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <cylinder radius="0.03" length="0.05"/>
      </geometry>
    </collision>
  </link>

  <joint name="laser_joint" type="fixed">
    <parent link="base_link"/>
    <child link="laser_link"/>
    <origin xyz="0.12 0 ${base_height/2 + laser_height/2}" rpy="0 0 0"/>
  </joint>

  <!-- Camera -->
  <link name="camera_link">
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.05 0.08 0.03"/>
      </geometry>
      <material name="grey">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.05 0.08 0.03"/>
      </geometry>
    </collision>
  </link>

  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 ${base_height/2}" rpy="0 0 0"/>
  </joint>

</robot>
```

### 1.3 메인 xacro 파일

```xml
<!-- urdf/robot.urdf.xacro -->
<?xml version="1.0"?>
<robot name="mobile_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <xacro:include filename="$(find my_robot_description)/urdf/xacro/robot_base.xacro"/>

  <!-- gazebo 물리 속성 -->
  <xacro:macro name="gazebo_material" params="name color">
    <gazebo reference="${name}">
      <material>${color}</material>
      <mu1>0.2</mu1>
      <mu2>0.2</mu2>
    </gazebo>
  </xacro:macro>

  <xacro:gazebo_material name="base_link" value="Gazebo/Blue"/>
  <xacro:gazebo_material name="front_left_wheel" value="Gazebo/Black"/>
  <xacro:gazebo_material name="front_right_wheel" value="Gazebo/Black"/>
  <xacro:gazebo_material name="back_left_wheel" value="Gazebo/Black"/>
  <xacro:gazebo_material name="back_right_wheel" value="Gazebo/Black"/>
  <xacro:gazebo_material name="laser_link" value="Gazebo/Grey"/>
  <xacro:gazebo_material name="camera_link" value="Gazebo/DarkGrey"/>
</robot>
```

### 1.4 launch 파일

```xml
<!-- launch/display.launch -->
<launch>
  <arg name="model" default="$(find my_robot_description)/urdf/robot.urdf.xacro"/>

  <param name="robot_description" command="xacro $(arg model)"/>

  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher">
    <param name="publish_frequency" value="10"/>
  </node>

  <node name="joint_state_publisher" pkg="joint_state_publisher" type="joint_state_publisher"/>

  <node name="rviz" pkg="rviz" type="rviz" args="-d $(find my_robot_description)/rviz/robot.rviz"/>
</launch>
```

### 1.5 rviz 설정

```xml
<!-- rviz/robot.rviz -->
Panels:
  - Class: rviz/Displays
    Help Height: 78
    Name: Displays
    Splitter Ratio: 0.5
  - Class: rviz/Initial Camera Pose
    Name: Views
    Splitter Ratio: 0.5

Visualization Manager:
  Displays:
    - Alpha: 0.5
      Cell Size: 1
      Class: rviz/Grid
      Enabled: true
      Name: Grid
      Value: true

    - Class: rviz/RobotModel
      Enabled: true
      Name: RobotModel
      Robot Description: robot_description
      Value: true

    - Class: rviz/TF
      Enabled: true
      Frame Timeout: 15
      Frames:
        All Enabled: true
      Markers:
        All Enabled: true
      Names:
        All Enabled: true
      Value: true
      Visual Enabled: true

  Global Options:
    Background Color: 48; 48; 48
    Fixed Frame: base_footprint
    Frame Rate: 30

  Name: root
  Tools:
    - Class: rviz/Interact
      Hide Inactive Objects: true
    - Class: rviz/MoveCamera
    - Class: rviz/Select

  Value: true
  Views:
    Current:
      Class: rviz/Orbit
      Target Configuration:
        Target: 0 0 0
      Value: Orbit (rviz)
```

## 2. Gazebo 연동

### 2.1 Gazebo launch

```xml
<!-- launch/gazebo.launch -->
<launch>
  <arg name="world_name" default="$(find gazebo_ros)/launch/empty_world.launch"/>

  <!-- Gazebo 실행 -->
  <include file="$(arg world_name)"/>

  <!-- URDF 로드 -->
  <param name="robot_description" command="xacro $(find my_robot_description)/urdf/robot.urdf.xacro"/>

  <!-- Gazebo에서 로봇 스폰 -->
  <node name="spawn_urdf" pkg="gazebo_ros" type="spawn_model" args="-urdf -param robot_description -model mobile_robot -x 0 -y 0 -z 0.1"/>

  <!-- Robot State Publisher -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>
</launch>
```

### 2.2 Gazebo 컨트롤러

```xml
<!-- launch/control.launch -->
<launch>
  <!-- 컨트롤러 로드 -->
  <rosparam file="$(find my_robot_description)/config/robot_controllers.yaml" command="load"/>

  <!-- Effort Controllers -->
  <node name="spawner" pkg="controller_manager" type="spawner" args="--stopped effort_controllers joint_state_controller"/>

  <!-- Robot State Publisher -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" output="screen"/>
</launch>
```

### 2.3 컨트롤러 설정

```yaml
# config/robot_controllers.yaml
robot_state_publisher:
  type: robot_state_publisher/RobotStatePublisher

joint_state_controller:
  type: joint_state_controller/JointStateController
  publish_rate: 50

effort_controllers:
  type: effort_controllers/JointGroupVelocityController
  joints:
    - front_left_wheel_joint
    - front_right_wheel_joint
    - back_left_wheel_joint
    - back_right_wheel_joint
  command_interface: velocity
  pid: {p: 1.0, i: 0.0, d: 0.1}
```

## 3. 실습 실행

### 3.1 RViz 실행

```bash
cd ~/catkin_ws
source devel/setup.bash
roslaunch my_robot_description display.launch
```

### 3.2 Gazebo 실행

```bash
roslaunch my_robot_description gazebo.launch
roslaunch my_robot_description control.launch
```

### 3.3 토픽 테스트

```bash
# cmd_vel로 이동
rostopic pub /effort_controllers/command std_msgs/Float64MultiLayout "data: [0.5, 0.5, 0.5, 0.5]"

# Joint 상태 확인
rostopic echo /joint_states
```

## 4. 실습 과제

1. 작성한 URDF 파일을 Gazebo에서 실행하세요.
2. RViz에서 로봇 모델을 확인하세요.
3. Gazebo에서 물리 시뮬레이션을 확인하세요.
4. 컨트롤러를 사용하여 로봇을 이동시켜보세요.

## 5. 다음 실습 예고

다음 클래스에서는 ROS 주요 tool과 원격 개발 환경을 구축합니다.