# Class 04: Navigation 해보기 실습

## 1. Navigation 실습 준비

### 1.1 사전 요구사항

```bash
# 필요한 패키지 실행 중인지 확인
roscore

# 라이다
roslaunch rplidar_ros rplidar.launch

# 모터 드라이버
roslaunch my_robot motor_driver.launch

# Odometry
roslaunch my_robot odometry.launch

# Robot State Publisher
roslaunch my_robot robot_state_publisher.launch
```

### 1.2 맵 로드

```bash
# 저장된 맵이 있는 경우
rosrun map_server map_server ~/my_map.yaml

# 또는 launch 파일에서
<node name="map_server" pkg="map_server" type="map_server" args="$(find my_robot)/maps/my_map.yaml"/>
```

## 2. Navigation 실행

### 2.1 전체 launch 파일

```xml
<!-- launch/navigation_robot.launch -->
<launch>
  <!-- Robot Description -->
  <param name="robot_description" command="cat $(find my_robot)/urdf/my_robot.urdf"/>

  <!-- Robot State Publisher -->
  <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>

  <!-- Map Server -->
  <node name="map_server" pkg="map_server" type="map_server" args="$(find my_robot)/maps/my_map.yaml"/>

  <!-- AMCL Localization -->
  <node name="amcl" pkg="amcl" type="amcl" output="screen">
    <param name="odom_model_type" value="diff"/>
    <param name="odom_alpha5" value="0.1"/>
    <param name="gui_init_pose_enabled" value="true"/>
    <param name="initial_pose_x" value="0.0"/>
    <param name="initial_pose_y" value="0.0"/>
    <param name="initial_pose_a" value="0.0"/>
  </node>

  <!-- Move Base -->
  <node name="move_base" pkg="move_base" type="move_base" output="screen">
    <rosparam file="$(find my_robot)/config/costmap_common_params.yaml" command="load" ns="global_costmap"/>
    <rosparam file="$(find my_robot)/config/costmap_common_params.yaml" command="load" ns="local_costmap"/>
    <rosparam file="$(find my_robot)/config/costmap_params.yaml" command="load"/>
    <rosparam file="$(find my_robot)/config/base_local_planner_params.yaml" command="load"/>
    <rosparam file="$(find my_robot)/config/base_global_planner_params.yaml" command="load"/>
  </node>
</launch>
```

### 2.2 실행

```bash
roslaunch my_robot navigation_robot.launch
```

## 3. RViz에서 Navigation

### 3.1 RViz 설정

```
Displays 설정:
- RobotModel: ✓
- Map: /map ✓
- LaserScan: /scan ✓
- Pose: /amcl_pose ✓ (AMCL 사용 시)
- PoseArray: /particlecloud (AMCL 사용 시)
- Path: /move_base/GlobalPlanner/plan
- Path: /move_base/TrajectoryPlannerROS/local_plan
- Marker: /move_base/NavfnROS/goal
```

### 3.2 초기 위치 설정

```bash
# 2D Pose Estimate 도구 사용
# RViz에서 클릭 후 드래그로 위치/방향 설정
# 또는命令行에서
rosservice call /initialpose "{pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}, header: {frame_id: 'map'}}"
```

### 3.3 목표 설정

```bash
# 2D Nav Goal 도구 사용
# 또는命令行에서
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped \
  "{header: {stamp: now, frame_id: 'map'}, \
    pose: {position: {x: 2.0, y: 0.0, z: 0.0}, \
           orientation: {x: 0.0, y: 0.0, z: 0.707, w: 0.707}}}"
```

## 4. Navigation 모니터링

### 4.1 토픽 확인

```bash
# 이동 중 확인
rostopic hz /move_base/global_costmap/rolled

# 경로 확인
rostopic echo /move_base/TrajectoryPlannerROS/local_plan

# 상태 확인
rostopic echo /move_base/status
```

### 4.2 rqt 확인

```bash
# 비용 맵 확인
rqt_plot /move_base/local_costmap/costmap/data[200:250]

# 속도 확인
rostopic echo /cmd_vel
```

### 4.3 문제 해결

```bash
# Goal에 도달하지 못할 때
# 1. Costmap 확인
rqt_plot /move_base/global_costmap/costmap/data

# 2. Localizer 재설정
rosservice call /global_localization "{}"

# 3. Clear costmap
rosservice call /move_base/clear_unknown_space "{}"
```

## 5. 다양한 목표 지정

### 5.1 코드에서 목표 지정

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped

def send_goal(x, y, theta):
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1)

    msg = PoseStamped()
    msg.header.stamp = rospy.Time.now()
    msg.header.frame_id = 'map'
    msg.pose.position.x = x
    msg.pose.position.y = y
    msg.pose.position.z = 0.0

    # Quaternion 변환
    import math
    msg.pose.orientation.z = math.sin(theta / 2)
    msg.pose.orientation.w = math.cos(theta / 2)

    rospy.sleep(1)
    pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('goal_sender')
    send_goal(2.0, 1.0, 0.0)
```

### 5.2 다중 목표

```python
# 순차적 목표 이동
goals = [
    (1.0, 0.0, 0.0),
    (2.0, 1.0, 1.57),
    (2.0, 2.0, 3.14),
]

for x, y, theta in goals:
    send_goal(x, y, theta)
    rospy.sleep(5)
```

## 6. 실습 과제

1. 저장된 맵을 사용하여 Navigation을 실행하세요.
2. RViz에서 초기 위치를 설정하고 목표까지 이동하세요.
3. 여러 목표점을 순차적으로 이동하는 코드를 작성하세요.
4. Navigation 중 발생하는 문제를 해결하세요.

## 7. 다음 실습 예고

다음 클래스에서는 Cartographer SLAM을 학습합니다.