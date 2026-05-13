# Class 06: SLAM(Cartographer) 실습 및 Rviz와 Navigation

## 1. Cartographer 상세 실습

### 1.1パラメータ調整

```lua
-- config/cartographer_tuned.lua
MAP_BUILDER {
  use_trajectory_builder_2d = true,
  num_background_threads = 4,
  submaps = {
    num_range_data = 120,
    resolution = 0.05,
    hit_probability = 0.55,
    miss_probability = 0.49,
  },
  pose_graph = {
    fast_correlative_scan_matcher = {
      linear_search_window = 0.3,
      angular_search_window = math.rad(35),
      coarse_angle_resolution = math.rad(0.35),
    },
    ceres_solver_options = {
      use_nonmonotonic_steps = true,
      max_num_iterations = 50,
    },
  },
}

TRAJECTORY_BUILDER_2D {
  min_range = 0.2,
  max_range = 25.0,
  num_accumulated_range_data = 10,
  voxels = {
    max_length = 0.9,
    max_range = 20.0,
    min_density = 0.45,
  },
  adaptive_voxel_filter = {
    max_length = 0.15,
    min_num_points = 200,
    max_range = 15.0,
  },
  imu_tracker_options = {
    gravity_constant = 9.8,
  },
  scan_matcher_options = {
    delta_translation_weight = 1.0,
    delta_rotation_weight = 1.0,
  },
}
```

### 1.2 IMU 통합

```xml
<!-- Cartographer launch with IMU -->
<launch>
  <node name="cartographer" pkg="cartographer_ros"
        type="cartographer_node" output="screen"
        args="-configuration_directory $(find my_robot)/config \
              -configuration_basename cartographer_with_imu.lua">

    <remap from="scan" to="/scan"/>
    <remap from="imu" to="/imu/data"/>
  </node>
</launch>
```

### 1.3 Multi-robot SLAM

```xml
<!-- Multiple robots -->
<node name="cartographer_robot1" pkg="cartographer_ros"
      type="cartographer_node" output="screen"
      args="-configuration_directory $(find my_robot)/config \
            -configuration_basename cartographer_robot1.lua">
  <remap from="scan" to="/robot1/scan"/>
  <param name="robot_id" value="robot1"/>
</node>

<node name="cartographer_robot2" pkg="cartographer_ros"
      type="cartographer_node" output="screen"
      args="-configuration_directory $(find my_robot)/config \
            -configuration_basename cartographer_robot2.lua">
  <remap from="scan" to="/robot2/scan"/>
  <param name="robot_id" value="robot2"/>
</node>
```

## 2. Cartographer → Navigation

### 2.1 맵 변환

```bash
# OccupancyGrid로 변환
rostopic hz /map

# 저장된 pbstream에서 변환
rosrun cartographer_ros \
    map_converter \
    --map_filename=/home/user/map.pbstream \
    --output_filename=/home/user/map.yaml
```

### 2.2 Navigation 설정

```yaml
# config/navigation_costmap.yaml
global_costmap:
  global_costmap:
    robot_radius: 0.25
    inflation_radius: 0.3

local_costmap:
  local_costmap:
    robot_radius: 0.25
    inflation_radius: 0.3
    width: 4.0
    height: 4.0
    resolution: 0.05
```

### 2.3 전체 launch

```xml
<!-- launch/navigation_cartographer.launch -->
<launch>
  <!-- Cartographer로 생성된 맵 사용 -->
  <node name="map_server" pkg="map_server"
        type="map_server"
        args="$(find my_robot)/maps/cartographer_map.yaml"/>

  <!-- AMCL (Cartographer의 Pose 사용 시 생략 가능) -->
  <!-- 또는 Cartographer의 trajectory 제공 -->

  <!-- Move Base -->
  <node name="move_base" pkg="move_base" type="move_base" output="screen">
    <rosparam file="$(find my_robot)/config/costmap_params.yaml" command="load"/>
    <rosparam file="$(find my_robot)/config/base_local_planner_params.yaml" command="load"/>
  </node>
</launch>
```

## 3. Rviz와 Navigation 통합

### 3.1 Rviz 설정

```
Displays 설정:

1. Global Options
   - Fixed Frame: map

2. RobotModel
   - Robot Description: robot_description

3. Map
   - Topic: /map (Cartographer의 경우)
   - Color Scheme: map

4. LaserScan
   - Topic: /scan

5. Pose
   - Topic: /current_pose (Cartographer 제공 시)

6. Path
   - Global Plan: /move_base/NavfnROS/plan
   - Local Plan: /move_base/DWAPlannerROS/local_plan

7. Costmap
   - Global Costmap: /move_base/global_costmap/costmap
   - Local Costmap: /move_base/local_costmap/costmap
```

### 3.2 디버깅 표시

```bash
# Submap 시각화
rostopic echo /submap_visualization

# Trajectory 시각화
rostopic echo /trajectory

# Scan matching 결과
rostopic echo /scan_matcher_downsampled_scan
```

### 3.3 문제 해결

```bash
# 맵이 제대로 안 보이는 경우
# 1. Cartographer 상태 확인
rostopic echo /submap_list
rostopic echo /trajectory_node_list | head -20

# 2. TF 확인
rosrun tf tf_echo map odom

# 3. Laser 스캔 확인
rostopic hz /scan

# 4. RViz에서 다시 확인
# Tools > Reset을 클릭
```

## 4. 실습: Cartographer + Navigation

### 4.1 순서

```
1. Cartographer 실행 → SLAM 수행
2. 맵 저장 (pbstream)
3. Navigation으로 전환
4. 저장된 맵 로드
5. AMCL 또는 Cartographer Pose 사용
6. 목표 설정 → 이동
```

### 4.2 Cartographer → Navigation 전환

```bash
# 1. SLAM 중지 (Ctrl+C)
# 2. 맵 저장
rosservice call /write_state "{filename: '/home/user/my_map.pbstream'}"

# 3. Navigation 시작
roslaunch my_robot navigation_cartographer.launch

# 4. 초기 위치 설정
# RViz에서 2D Pose Estimate 사용

# 5. 목표 설정
# RViz에서 2D Nav Goal 사용
```

### 4.3 코드 예시

```python
#!/usr/bin/env python3
import rospy

def cartographer_to_navigation():
    """Cartographer SLAM → Navigation 전환"""
    rospy.init_node('slam_to_nav')

    # SLAM 중지 신호
    # (실제 구현은 파일에 따라 다름)

    # 맵 저장
    rospy.sleep(2)
    try:
        rospy.wait_for_service('/write_state', timeout=10)
        write_state = rospy.ServiceProxy('/write_state', WriteState)
        write_state(filename='/home/user/map.pbstream')
        rospy.loginfo("Map saved")
    except:
        rospy.logwarn("Failed to save map")

if __name__ == '__main__':
    cartographer_to_navigation()
```

## 5. 실습 과제

1. Cartographer로 맵을 생성하고 저장하세요.
2. 저장한 맵을 사용하여 Navigation을 실행하세요.
3. RViz에서 Cartographer와 Navigation을 동시에 확인하세요.
4. 실제 환경에서 Cartographer + Navigation을 테스트하세요.

## 6. 다음 실습 예고

다음 클래스에서는 Rviz와 Navigation 실습을 계속합니다.