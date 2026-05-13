# Class 05: SLAM(Cartographer) 실습

## 1. Cartographer 개요

### 1.1 Cartographer란?

Cartographer는 Google이 개발한 Real-time SLAM 라이브러리입니다. 2D 및 3D SLAM을 지원합니다.

```
Cartographer 특징:
┌─────────────────────────────────────┐
│ - 서브맵(Submap) 기반 SLAM          │
│ - Loop Closure 최적화              │
│ -リアルタイムSLAM 가능              │
│ - 고품질 맵 생성                    │
│ - ROS 통합 지원                    │
└─────────────────────────────────────┘
```

### 1.2 Gmapping vs Cartographer

| 구분 | Gmapping | Cartographer |
|------|----------|--------------|
| 알고리즘 | Particle Filter | Pose Graph |
| 품질 | 중간 | 높음 |
| 속도 | 느림 | 빠름 |
| 메모리 | 많음 | 적음 |
| Loop closure | 약함 | 강함 |

## 2. Cartographer 설치

### 2.1 의존성 설치

```bash
# 의존성 패키지
sudo apt-get update
sudo apt-get install -y \
    ros-noetic-cartographer \
    ros-noetic-cartographer-ros \
    ros-noetic-cartographer-ros-msgs \
    ros-noetic-abseil-cpp

# 빌드 (소스 설치 시)
cd ~/catkin_ws/src
git clone https://github.com/cartographer-project/cartographer_ros.git
cd ..
catkin_make_isolated --install --use-ninja
```

### 2.2 패키지 확인

```bash
rospack find cartographer_ros
rospack find cartographer
```

## 3. Cartographer 설정

### 3.1 설정 파일 구조

```lua
-- cartographer.lua
include "map_builder.lua"
include "trajectory_builder.lua"

MAP_BUILDER {
  use_trajectory_builder_2d = true,
  submaps = {
    range_data_inserter = {
      hit_probability = 0.55,
      miss_probability = 0.49,
      insertion_probability = 0.55,
    },
  },
}

TRAJECTORY_BUILDER_2D {
  min_range = 0.2,
  max_range = 30.,
  missing_data_ray_length = 30.,
  voxels = {
    max_length = 0.05,
    max_range = 20.,
    min_density = 0.65,
  },
}
```

### 3.2-launch 파일

```xml
<!-- launch/cartographer.launch -->
<launch>
  <param name="robot_description"
    command="xacro $(find my_robot)/urdf/my_robot.urdf" />

  <!-- Cartographer Node -->
  <node name="cartographer" pkg="cartographer_ros"
        type="cartographer_node" output="screen"
        args="-configuration_directory $(find my_robot)/config \
              -configuration_basename cartographer.lua">

    <remap from="scan" to="/scan"/>
    <remap from="echoes" to="/echoes"/>
  </node>

  <!-- Occupancy Grid Node -->
  <node name="cartographer_occupancy_grid_node" pkg="cartographer_ros"
        type="cartographer_occupancy_grid_node" output="screen"
        args="-resolution 0.05"/>

  <!-- Robot State Publisher -->
  <node name="robot_state_publisher" pkg="robot_state_publisher"
        type="robot_state_publisher">
    <remap from="robot_description" to="robot_description"/>
  </node>
</launch>
```

### 3.3 설정 파일

```lua
-- config/cartographer.lua
MAP_BUILDER {
  use_trajectory_builder_2d = true,
  submaps = {
    num_range_data = 90,
    resolution = 0.05,
  },
  pose_graph = {
    fast_correlative_scan_matcher = {
      linear_search_window = 0.15,
      angular_search_window = 0.15,
      coarse_angle_resolution = 0.15,
    },
    optimization_problem = {
      hysteresis_threshold = 0.1,
      outlier_exclusion_percentage = 0.15,
    },
  },
}

TRAJECTORY_BUILDER_2D {
  min_range = 0.3,
  max_range = 20.,
  num_accumulated_range_data = 10,
  voxels = {
    max_length = 0.5,
    max_range = 20.,
    min_density = 0.5,
  },
  adaptive_voxel_filter = {
    max_length = 0.1,
    min_num_points = 100,
  },
}
```

## 4. Cartographer 실행

### 4.1 실행

```bash
roslaunch my_robot cartographer.launch
```

### 4.2 토픽 확인

```bash
# 토픽 확인
rostopic list | grep -E "cartographer|submap|scan_match"

#サブマップ 확인
rostopic echo /submap_list

# 트래젝토리 확인
rostopic echo /trajectory_node_list
```

### 4.3 RViz 설정

```
RViz Displays:
- Map: /map (Cartographer가 생성한 맵)
- Submap List: /submap_list
- LaserScan: /scan
- RobotModel: robot_description
- TF: map → odom → base_link
```

## 5. 맵 저장

### 5.1.pbstream 저장

```bash
#.pbstream 파일로 저장
rosservice call /write_state "{filename: '/home/user/map.pbstream'}"

# 또는 launch에서
<node name="cartographer" pkg="cartographer_ros"
      type="cartographer_node"
      args="-configuration_directory $(find my_robot)/config \
            -configuration_basename cartographer.lua \
            -save_state_filename /home/user/map.pbstream"/>
```

### 5.2 Occupancy Grid 변환

```bash
# pbstream → OccupancyGrid
rosrun cartographer_ros proto_to_pbstream \
    map.pbstream map.lua

# 또는 Cartographer의 occupancy_grid_node가 자동으로 생성
rostopic echo /map
```

## 6. 실습 과제

1. Cartographer를 설치하고 실행하세요.
2. 키보드로 로봇을 조종하며 맵을 생성하세요.
3. Gmapping과 Cartographer의 맵 품질을 비교하세요.
4. 저장한 맵을 다시 로드하여Navigation에 사용하세요.

## 7. 다음 실습 예고

다음 클래스에서는 Cartographer와 Rviz/Navigation 연동을 학습합니다.