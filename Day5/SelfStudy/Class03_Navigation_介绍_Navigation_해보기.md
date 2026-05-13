# Class 03: Navigation 소개 및 Navigation 해보기

## 1. ROS Navigation Stack

### 1.1 Navigation 개요

ROS Navigation Stack은 2D 로봇의 자율 이동을 위한 완전한 시스템입니다.

```
Navigation Stack:
┌─────────────────────────────────────┐
│           User Input               │
│      (Goal, RViz, API)             │
├─────────────────────────────────────┤
│           Move Base                │
│    ┌───────────┬───────────┐        │
│    │  Global   │  Local    │        │
│    │  Planner  │  Planner  │        │
│    └───────────┴───────────┘        │
├─────────────────────────────────────┤
│          Costmap 2D                 │
│    ┌───────────┬───────────┐        │
│    │  Global   │  Local    │        │
│    │  Costmap  │  Costmap  │        │
│    └───────────┴───────────┘        │
├─────────────────────────────────────┤
│          Recovery Behaviors        │
├─────────────────────────────────────┤
│          Robot Driver              │
│     (Base Controller)              │
└─────────────────────────────────────┘
```

### 1.2 구성 요소

| 구성요소 | 설명 |
|----------|------|
| move_base | 네비게이션 메인 노드 |
| global_planner | 전역 경로 계획 |
| local_planner | 지역 충돌 회피 |
| costmap_2d | 비용 맵 관리 |
| map_server | 맵 제공 |
| amcl | Localization |
| robot_state_publisher | URDF 기반 TF |

### 1.3 필요 입력

```
Navigation Input:
┌─────────────────────────────────────┐
│ /map              - 정적 맵         │
│ /scan             - 레이저 스캔    │
│ /odom             - Odometry       │
│ /tf               - 좌표계 변환    │
│ /initial_pose     - 시작 위치      │
│ /move_base_simple/goal - 목표 위치 │
└─────────────────────────────────────┘
```

## 2. Navigation 설치

### 2.1 패키지 설치

```bash
# 기본 Navigation
sudo apt install ros-noetic-navigation
sudo apt install ros-noetic-map-server
sudo apt install ros-noetic-amcl

# Navigation 튜닝 도구
sudo apt install ros-noetic-navigation-stage
```

### 2.2 의존성 확인

```bash
rospack find navigation
rospack find costmap_2d
rospack find move_base
```

## 3. Navigation 설정

### 3.1 전체launch

```xml
<!-- launch/navigation.launch -->
<launch>
  <!-- Map Server -->
  <node name="map_server" pkg="map_server" type="map_server" args="$(find my_robot)/maps/my_map.yaml"/>

  <!-- AMCL (Localization) -->
  <node name="amcl" pkg="amcl" type="amcl" output="screen">
    <param name="initial_pose_x" value="0.0"/>
    <param name="initial_pose_y" value="0.0"/>
    <param name="initial_pose_a" value="0.0"/>
  </node>

  <!-- Move Base -->
  <node name="move_base" pkg="move_base" type="move_base" output="screen">
    <rosparam file="$(find my_robot)/config/costmap_params.yaml" command="load"/>
    <rosparam file="$(find my_robot)/config/base_local_planner_params.yaml" command="load"/>
    <rosparam file="$(find my_robot)/config/base_global_planner_params.yaml" command="load"/>
    <rosparam file="$(find my_robot)/config/dwa_local_planner_params.yaml" command="load"/>
  </node>
</launch>
```

### 3.2 Costmap 파라미터

```yaml
# config/costmap_params.yaml
obstacle_layer:
  enabled: true
  obstacle_range: 2.5
  raytrace_range: 3.0
  footprint_padding: 0.03

static_layer:
  enabled: true
  map_topic: /map

inflation_layer:
  enabled: true
  cost_scaling_factor: 10.0
  inflation_radius: 0.5

global_costmap:
  global_frame: /map
  robot_base_frame: /base_link
  update_frequency: 1.0
  publish_frequency: 1.0
  width: 20.0
  height: 20.0
  resolution: 0.05

local_costmap:
  global_frame: /odom
  robot_base_frame: /base_link
  update_frequency: 5.0
  publish_frequency: 5.0
  width: 6.0
  height: 6.0
  resolution: 0.05
```

### 3.3 Local Planner 파라미터

```yaml
# config/base_local_planner_params.yaml
TrajectoryPlannerROS:
  max_vel_x: 0.5
  min_vel_x: 0.1
  max_vel_theta: 1.0
  min_vel_theta: -1.0
  min_in_place_vel_theta: 0.5

  acc_lim_x: 1.0
  acc_lim_y: 0.0
  acc_lim_theta: 1.0

  holonomic_robot: false
```

### 3.4 Global Planner 파라미터

```yaml
# config/base_global_planner_params.yaml
NavfnROS:
  default_tolerance: 0.1
  planner_window_x: 0.0
  planner_window_y: 0.0
```

## 4. Navigation 실행

### 4.1 전체 실행

```bash
# launch 파일 사용
roslaunch my_robot navigation.launch
```

### 4.2 RViz 설정

```
RViz Displays:
- RobotModel: robot_description
- Map: /map
- Local Costmap: /move_base/local_costmap/costmap
- Global Costmap: /move_base/global_costmap/costmap
- Global Plan: /move_base/NavfnROS/plan
- Local Plan: /move_base/TrajectoryPlannerROS/local_plan
- Pose: /amcl_pose
```

### 4.3 목표 설정

```bash
#命令行에서 목표 전송
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped '{header: {stamp: now, frame_id: "map"}, pose: {position: {x: 2.0, y: 0.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}'
```

### 4.4 RViz에서 설정

```bash
# RViz에서:
# 1. "2D Nav Goal" 도구 선택
# 2. 맵에서 목표 위치 클릭
# 3. 드래그하여 방향 설정
```

## 5. Recovery Behavior

### 5.1 기본 복구 동작

```yaml
# recovery_behaviors 파라미터
recovery_behaviors:
  - name: 'oscillation_cleaner'
    type: 'clear_costmap_recovery/ClearCostmapRecovery'
  - name: 'backup_smoother'
    type: 'move_slow_and_clear/MoveSlowAndClear'
  - name: 'conservative_reset'
    type: 'clear_costmap_recovery/ClearCostmapRecovery'
```

### 5.2 수동 복구

```bash
# 모든 costmap 초기화
rosservice call /move_base/clear_unknown_space "{}"

# localization 재시작
rosservice call /global_localization "{}"
```

## 6. 실습 과제

1. Navigation 패키지를 설치하고 설정하세요.
2. 맵을 로드하여 RViz에서 확인하세요.
3. RViz에서 목표 위치를 설정하고 로봇을 이동시켜보세요.
4. Recovery 동작이 정상적으로 작동하는지 확인하세요.

## 7. 다음 실습 예고

다음 클래스에서는 Navigation 실습을 계속합니다.