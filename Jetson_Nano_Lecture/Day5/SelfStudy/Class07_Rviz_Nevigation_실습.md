# Class 07: Rviz와 Navigation 실습

## 1. Rviz Navigation 시각화

### 1.1 전체 시각화 설정

```
Rviz 디스플레이 설정:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│ Displays                               │
├───────────────────────────────────────│
│ [✓] Global Options                    │
│     Fixed Frame: map                  │
│     Background: Black                 │
│                                       │
│ [✓] RobotModel                        │
│     Robot Description: robot_desc    │
│                                       │
│ [✓] Map                               │
│     Topic: /map                       │
│     Color Scheme: map                 │
│                                       │
│ [✓] LaserScan                         │
│     Topic: /scan                      │
│     Size: 0.1                         │
│                                       │
│ [✓] Odometry                          │
│     Topic: /odom                      │
│     Covariance: 0.1                   │
│                                       │
│ [✓] Path                              │
│     Global: /move_base/.../plan       │
│     Local: /move_base/.../local_plan  │
│                                       │
│ [✓] Costmap 2D                        │
│     Global: /move_base/.../costmap   │
│     Local: /move_base/.../costmap    │
│                                       │
│ [✓] Pose                              │
│     Topic: /amcl_pose                 │
│     Covariance Scale: 1.0            │
│                                       │
│ [✓] Marker                            │
│     Topic: /move_base/current_goal    │
│                                       │
└───────────────────────────────────────
```

### 1.2 실행 중인 토픽 확인

```bash
# 모든 토픽 확인
rostopic list | grep -E "move_base|map|odom|costmap|plan"

# 특정 토픽 정보
rostopic info /move_base/global_costmap/costmap

# 토픽 값 확인
rostopic echo /move_base/global_costmap/costmap -n1
```

### 1.3 Costmap 시각화

```bash
# Costmap 레이어 확인
rostopic echo /move_base/global_costmap/costmap_updates

# Occupancy Grid 확인
rostopic type /move_base/global_costmap/costmap
rostopic hz /move_base/global_costmap/costmap
```

## 2. Navigation 문제 해결

### 2.1 일반적인 문제

| 문제 | 원인 | 해결책 |
|------|------|--------|
| 로봇이 움직이지 않음 | cmd_vel 미출력 | base controller 확인 |
| 목표에 도달 못함 | costmap/blocked | recovery behavior 확인 |
| localization 불안정 | 초기 위치 오류 | initial_pose 재설정 |
| 경로 불안정 |_planner 파라미터 | local planner 튜닝 |

### 2.2 디버깅 명령어

```bash
# 1. Costmap 확인
rqt_reconfigure
# Move Base > Local Costmap 확인

# 2. 경로 확인
rostopic echo /move_base/TrajectoryPlannerROS/local_plan -n1

# 3. 속도 확인
rostopic echo /cmd_vel -n1

# 4. 목표 상태 확인
rostopic echo /move_base/status -n1

# 5. TF 확인
rosrun tf tf_echo map base_link
```

### 2.3 비용 맵 재설정

```bash
# Clear costmap
rosservice call /move_base/clear_costmaps "{}"

# Global localization
rosservice call /global_localization "{}"

# Clear unknown space
rosservice call /move_base/clear_unknown_space "{}"
```

## 3. Rviz 도구 활용

### 3.1 도구 설명

```
Rviz Tools:
┌─────────────────────────────────────┐
│ Interact     │ 객체 선택/변경       │
├─────────────────────────────────────┤
│ Move Camera  │ 카메라 이동          │
├─────────────────────────────────────┤
│ Select       │ 요소 선택            │
├─────────────────────────────────────┤
│ 2D Pose Estimate │ 초기 위치 설정   │
├─────────────────────────────────────┤
│ 2D Nav Goal  │ 목표 위치 설정       │
├─────────────────────────────────────┤
│ Publish Point │ 포인트Publish      │
└─────────────────────────────────────┘
```

### 3.2 2D Pose Estimate

```bash
# 사용법: RViz에서 클릭 + 드래그
# 결과: /initial_pose 토픽 Publishing
# 효과: AMCL의 입자cloud 초기화
```

### 3.3 2D Nav Goal

```bash
# 사용법: RViz에서 클릭 + 드래그
# 결과: /move_base_simple/goal Publishing
# 효과: Move Base가 경로 계획 시작
```

## 4. 탐색 성능 최적화

### 4.1 Global Planner 튜닝

```yaml
# config/global_planner.yaml
NavfnROS:
  default_tolerance: 0.0
  planner_window_x: 0.0
  planner_window_y: 0.0
  use_dijkstra: true
  orientation_window_size: 1
```

### 4.2 Local Planner 튜닝

```yaml
# config/dwa_planner.yaml
DWAPlannerROS:
  # 속도 제한
  max_vel_x: 0.5
  min_vel_x: 0.0
  max_vel_trans: 0.5
  min_vel_trans: 0.0
  max_vel_theta: 1.0
  min_vel_theta: -1.0

  # 가속도 제한
  acc_lim_x: 1.0
  acc_lim_theta: 2.0

  # 목표 공차
  xy_goal_tolerance: 0.1
  yaw_goal_tolerance: 0.05

  # 경로 플러닝
  path_distance_bias: 32.0
  goal_distance_bias: 24.0
  occdist_scale: 0.01

  #振荡防止
  oscillation_reset_dist: 0.05
```

### 4.3 Costmap 튜닝

```yaml
# config/costmap_params.yaml
obstacle_layer:
  observation_sources: scan
  scan:
    data_type: LaserScan
    topic: /scan
    obstacle_range: 2.5
    raytrace_range: 3.0

inflation_layer:
  inflation_radius: 0.35
  cost_scaling_factor: 10.0
```

## 5. 실습 과제

1. RViz에서 Navigation의 모든 표시를 확인하세요.
2. Costmap이 어떻게 생성되는지 확인하세요.
3. 목표 설정 시 경로가 어떻게 변하는지 확인하세요.
4. Navigation 파라미터를 튜닝하여 성능을 개선하세요.

## 6. 다음 실습 예고

다음 클래스에서는 Move_Base 노드와 SendGoals에 대해 학습합니다.