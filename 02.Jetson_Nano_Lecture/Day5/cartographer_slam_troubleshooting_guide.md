# Cartographer (SLAM) 설치 및 문제 해결 가이드

> **대상 환경**: ROS Noetic (Ubuntu 20.04 Focal) / Jetson (ARM64/aarch64)
> **작성일**: 2026-05-18

---

## 목차

1. [사전 준비: Cartographer 개요](#1-사전-준비-cartographer-개요)
2. [전체 설치 과정 요약](#2-전체-설치-과정-요약)
3. [단계별 상세 가이드 및 문제 해결](#3-단계별-상세-가이드-및-문제-해결)
   - [3.1. 빌드 도구 설치](#31-빌드-도구-설치)
   - [3.2. 작업 공간 생성 및 소스 다운로드](#32-작업-공간-생성-및-소스-다운로드)
   - [3.3. rosdep 의존성 설치](#33-rosdep-의존성-설치)
   - [3.4. Abseil 수동 빌드](#34-abseil-수동-빌드)
   - [3.5. Cartographer 빌드](#35-cartographer-빌드)
   - [3.6. 환경 변수 설정](#36-환경-변수-설정)
   - [3.7. Launch 파일 및 Lua 설정](#37-launch-파일-및-lua-설정)
   - [3.8. 실행 및 지도 저장](#38-실행-및-지도-저장)
4. [자주 발생하는 오류와 해결 방법](#4-자주-발생하는-오류와-해결-방법)
5. [Jetson (ARM64) 특이사항](#5-jetson-arm64-특이사항)
6. [Gmapping vs Cartographer 비교](#6-gmapping-vs-cartographer-비교)
7. [참고 자료](#7-참고-자료)

---

## 1. 사전 준비: Cartographer 개요

**Cartographer**는 구글에서 개발한 실시간 SLAM(Simultaneous Localization and Mapping) 라이브러리입니다.

- 2D 및 3D 환경 지원
- LiDAR 및 카메라(비전) 센서 구성 지원
- **실시간**(real-time) 성능 제공
- 서브맵(submap) 기반의 그래프 최적화(graph optimization) 방식
- CSM(Correlative Scan Matching)과 IMU 융합을 통한 정밀한 매핑

### 지원 ROS 버전

| ROS 버전   | Ubuntu 버전       | 지원 상태 |
|------------|-------------------|-----------|
| Melodic    | Ubuntu 18.04 Bionic | 지원 |
| **Noetic** | **Ubuntu 20.04 Focal** | **권장** |
| Humble (ROS2) | Ubuntu 22.04 Jammy | 별도 가이드 참조 |

---

## 2. 전체 설치 과정 요약

```
[1] 빌드 도구 설치 (wstool, ninja, stow, rosdep)
          │
[2] 작업 공간 생성 (noncatkin_ws)
          │
[3] 소스 코드 다운로드 (wstool merge/update)
          │
[4] rosdep 의존성 설치 ★ 문제 발생 구간 ★
     ├─ libabsl-dev 이슈 → package.xml 수정
     └─ libqt5core5t64 이슈 → --skip-keys 사용
          │
[5] Abseil 수동 빌드 (install_abseil.sh)
          │
[6] Cartographer 빌드 (catkin_make_isolated --use-ninja)
          │
[7] 환경 변수 등록 (~/.bashrc)
          │
[8] Lua 설정 파일 및 Launch 파일 생성
          │
[9] 실행 및 지도 저장
```

---

## 3. 단계별 상세 가이드 및 문제 해결

### 3.1. 빌드 도구 설치

```bash
sudo apt-get update
sudo apt-get install -y python3-wstool python3-rosdep ninja-build stow
```

> **⚠️ 주의**: Ubuntu 20.04 (Focal) 이상에서는 `python-wstool`이 아닌 **`python3-wstool`** 을 사용해야 합니다.
> Python 2 기반 패키지(`python-wstool`)는 Ubuntu 20.04부터 기본 설치되지 않습니다.

| OS 버전 | 올바른 패키지명 |
|---------|----------------|
| Ubuntu 18.04 Bionic | `python-wstool python-rosdep` |
| **Ubuntu 20.04 Focal** | **`python3-wstool python3-rosdep`** |
| Ubuntu 22.04 Jammy | `python3-wstool python3-rosdep` |

#### 설치 확인

```bash
# 각 도구가 정상 설치되었는지 확인
wstool --version
ninja --version
stow --version
rosdep --version
```

---

### 3.2. 작업 공간 생성 및 소스 다운로드

```bash
# 작업 공간 생성
mkdir -p ~/noncatkin_ws
cd ~/noncatkin_ws

# wstool 초기화
wstool init src

# Cartographer 소스 코드 다운로드
wstool merge -t src \
  https://raw.githubusercontent.com/cartographer-project/cartographer_ros/master/cartographer_ros.rosinstall
wstool update -t src
```

#### 다운로드 결과 확인

명령 실행 후 `~/noncatkin_ws/src/` 디렉터리에는 다음 두 개의 저장소가 있어야 합니다:

| 디렉터리 | 저장소 | 설명 |
|----------|--------|------|
| `src/cartographer/` | cartographer-project/cartographer | 핵심 SLAM 라이브러리 (C++) |
| `src/cartographer_ros/` | cartographer-project/cartographer_ros | ROS 래퍼 패키지 |

```bash
# 확인
ls ~/noncatkin_ws/src/
# 출력 예시:
# cartographer  cartographer_ros
```

---

### 3.3. rosdep 의존성 설치 ⚠️ 가장 문제가 발생하는 구간

#### 3.3.1. 기본 명령 실행

```bash
# rosdep 초기화 (첫 실행 시에만 필요, 두 번째부터는 에러 무시)
sudo rosdep init
rosdep update

# 의존성 설치
rosdep install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} -y
```

> `${ROS_DISTRO}` 환경변수가 설정되어 있는지 반드시 확인하세요:
> ```bash
> echo $ROS_DISTRO   # 출력: noetic (또는 melodic 등)
> ```
> 설정되어 있지 않다면:
> ```bash
> source /opt/ros/noetic/setup.bash
> ```

#### 3.3.2. 오류 1: `libabsl-dev` not available

**증상**:
```
ERROR: the following packages/stacks could not have their rosdep keys
resolved to system dependencies:
cartographer: [libabsl-dev] defined as "not available" for OS version [focal]
```

**원인**:
Cartographer의 `package.xml` (46번 라인)에 `<depend>libabsl-dev</depend>`가 정의되어 있으나,
ROS Noetic (Ubuntu Focal)용 rosdep에 `libabsl-dev` 키가 등록되어 있지 않습니다.
Abseil 라이브러리는 Cartographer가 **특정 버전**을 요구하므로 시스템 패키지로 설치하면
ABI 충돌이 발생할 수 있어, 공식적으로는 **수동 빌드**를 권장합니다.

**해결 방법**: `package.xml`에서 `libabsl-dev` 항목을 주석 처리합니다.

```bash
# package.xml 파일 열기
nano ~/noncatkin_ws/src/cartographer/package.xml
```

46번째 라인 근처:
```xml
  <depend>libboost-iostreams-dev</depend>
  <depend>eigen</depend>
  <depend>libabsl-dev</depend>          <!-- ← 이 라인을 주석 처리 -->
  <depend>libcairo2-dev</depend>
```

다음과 같이 변경:
```xml
  <depend>libboost-iostreams-dev</depend>
  <depend>eigen</depend>
  <!-- <depend>libabsl-dev</depend> -->   <!-- 수동 빌드 예정이므로 주석 처리 -->
  <depend>libcairo2-dev</depend>
```

**또는 sed 명령어로 간단 처리**:
```bash
sed -i 's/<depend>libabsl-dev<\/depend>/<!-- <depend>libabsl-dev<\/depend> -->/' \
  ~/noncatkin_ws/src/cartographer/package.xml
```

#### 3.3.3. 오류 2: `libqt5core5t64` Unable to locate package

**증상**:
```
E: Unable to locate package libqt5core5t64
```

**원인**:
- `libqt5core5t64`는 Ubuntu 24.04 (Noble Numbat)에서 도입된 **64-bit time_t 전환** 패키지명입니다.
- Ubuntu 22.04 (Jammy)에서는 `libqt5core5a`가 올바른 패키지명입니다.
- rosdep이 Ubuntu 버전을 잘못 감지했거나, 해당 패키지가 ARM64 저장소에 없는 경우 발생합니다.

> **배경 지식**: Ubuntu 24.04부터 `time_t`를 32bit에서 64bit로 전환하면서
> 기존 라이브러리 패키지명에 `t64` 접미사가 추가되었습니다
> (예: `libqt5core5a` → `libqt5core5t64`, `libglib2.0-0` → `libglib2.0-0t64`).
> Jetson의 Ubuntu 버전에 따라 이 차이가 발생합니다.

**해결 방법**: `--skip-keys` 옵션으로 해당 의존성을 건너뜁니다.

```bash
# Qt5 관련 패키지를 건너뛰고 rosdep 실행
rosdep install --from-paths src --ignore-src \
  --rosdistro=${ROS_DISTRO} -y \
  --skip-keys=libqt5-core
```

> **참고**: Qt5 라이브러리는 Cartographer의 핵심 SLAM 알고리즘과 직접적인 관련이 없습니다.
> 주로 RViz 시각화나 일부 GUI 관련 의존성입니다. 이 키를 건너뛰어도 Cartographer 빌드에는
> 문제가 없습니다.

#### 3.3.4. rosdep 의존성 설치 완료 확인

의존성 설치가 성공하면 다음과 유사한 출력이 나타납니다:

```
# All required rosdeps installed successfully
```

또는 이미 설치된 경우:
```
#All required rosdeps installed successfully
```

---

### 3.4. Abseil 수동 빌드

Cartographer는 C++용 Abseil 라이브러리를 사용합니다. ROS에서 제공하는 `abseil-cpp` 패키지와
Cartographer가 요구하는 버전 간 **ABI 호환성 문제**가 있어, 공식 스크립트로 직접 빌드해야 합니다.

```bash
# noncatkin_ws 디렉터리에서 실행
cd ~/noncatkin_ws

# Abseil 빌드 스크립트 실행
src/cartographer/scripts/install_abseil.sh
```

#### Abseil 빌드 스크립트의 동작 방식

`install_abseil.sh` 스크립트는 내부적으로 다음을 수행합니다:

1. GitHub에서 Abseil 소스 코드를 `/usr/local/src/abseil-cpp/`에 클론
2. CMake로 빌드하여 `/usr/local/`에 설치 (정적 라이브러리)
3. Cartographer가 링크할 수 있도록 준비

#### ROS Abseil 패키지 제거

```bash
# 충돌 방지를 위해 ROS 버전의 abseil-cpp 제거
sudo apt-get remove ros-${ROS_DISTRO}-abseil-cpp
```

> **참고**: `ros-${ROS_DISTRO}-abseil-cpp`가 설치되어 있지 않은 경우
> "Package not installed" 메시지가 나와도 무시해도 됩니다.

#### Abseil 관련 참고 사항

| 항목 | 설명 |
|------|------|
| **왜 수동 빌드가 필요한가?** | Cartographer는 Abseil의 특정 내부 API를 사용합니다. ROS 패키지 버전과 Cartographer 빌드 간 ABI 불일치로 링크 오류 발생 |
| **ABI 문제 증상** | 빌드 시 undefined reference, 컴파일 오류, 런타임 세그멘테이션 폴트 |
| **ROS 버전 제거 이유** | `libabsl-dev` 시스템 패키지 또는 `ros-noetic-abseil-cpp`가 `/usr/lib/`에 설치되어 Cartographer가 잘못된 버전을 링크할 수 있음 |
| **Jetson ARM64 참고** | ARM64에서 Abseil 빌드 시 추가 플래그가 필요할 수 있습니다. 스크립트가 실패하면 `-DABSL_PLATFORM=arm` 또는 `-DCMAKE_CXX_FLAGS=-mno-outline-atomics` 플래그 추가 필요 |

---

### 3.5. Cartographer 빌드

```bash
# noncatkin_ws 디렉터리에서 실행
cd ~/noncatkin_ws

# Ninja 빌드 시스템으로 Cartographer 빌드
catkin_make_isolated --install --use-ninja
```

#### 빌드 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--install` | `install_isolated/` 디렉터리에 설치 |
| `--use-ninja` | Ninja 빌드 시스템 사용 (병렬 빌드로 속도 향상) |

#### `catkin_make_isolated` vs `catkin_make` 차이

| 특성 | `catkin_make_isolated` | `catkin_make` |
|------|------------------------|---------------|
| 빌드 방식 | 패키지별 격리 빌드 | 단일 CMake 프로젝트로 통합 빌드 |
| 장점 | 의존성 충돌 없음, 디버깅 용이 | 속도 빠름 |
| 단점 | 속도 느림 | 패키지 간 충돌 가능 |
| Cartographer | **필수** (비-catkin 패키지 포함) | 사용 불가 |

> **팁**: 빌드 시간이 오래 걸리므로 `-j` 옵션으로 병렬 작업 수를 조정할 수 있습니다.
> Jetson의 코어 수에 맞게 설정:
> ```bash
> catkin_make_isolated --install --use-ninja -j$(nproc)
> ```

#### 빌드 완료 확인

```bash
# 설치 디렉터리 확인
ls ~/noncatkin_ws/install_isolated/
# bin/  etc/  include/  lib/  lib/python3/dist-packages/  setup.bash  ...

# Cartographer 패키지 확인
roscd cartographer
pwd
# 출력: ~/noncatkin_ws/src/cartographer
```

> **참고**: `roscd` 명령이 동작하려면 먼저 환경 변수를 설정해야 합니다:
> ```bash
> source ~/noncatkin_ws/install_isolated/setup.bash
> ```

---

### 3.6. 환경 변수 설정

```bash
# ~/.bashrc에 Cartographer 워크스페이스 등록
echo 'source ~/noncatkin_ws/install_isolated/setup.bash' >> ~/.bashrc

# 또는 ROS 워크스페이스와 함께 등록 (이미 catkin_ws가 있는 경우)
echo 'source ~/noncatkin_ws/install_isolated/setup.bash' >> ~/.bashrc
echo 'source ~/catkin_ws/devel/setup.bash' >> ~/.bashrc

# 현재 셸에 적용
source ~/.bashrc
```

> **⚠️ 중요**: ROS 워크스페이스(`catkin_ws`)와 Cartographer 워크스페이스(`noncatkin_ws`)를
> **모두** source 해야 합니다. `.bashrc`에 등록할 때 순서는 일반적으로 Cartographer를 먼저,
> 그 다음에 catkin_ws를 등록합니다. (의존성 순서에 따라)

---

### 3.7. Launch 파일 및 Lua 설정

#### 3.7.1. Launch 파일: `lidar_slam_carto.launch`

**경로**: `~/catkin_ws/src/allbot/launch/lidar_slam_carto.launch`

```xml
<launch>
  <!-- YD-lidar X4 LiDAR -->
  <include file="$(find allbot)/launch/include/X4.launch" />

  <!-- Cartographer SLAM 노드 -->
  <node name="cartographer_node" pkg="cartographer_ros"
        type="cartographer_node"
        args="-configuration_directory $(find allbot)/launch/include
              -configuration_basename allbot_lidar.lua"
        output="screen">
    <remap from="scan" to="scan"/>
  </node>

  <!-- Occupancy Grid 변환 노드 (2D grid map 발행) -->
  <node name="cartographer_occupancy_grid_node" pkg="cartographer_ros"
        type="cartographer_occupancy_grid_node"
        args="-resolution 0.05" />

  <!-- Allbot URDF 로드 (로봇 모델) -->
  <include file="$(find allbot_urdf)/launch/urdf.launch" />

  <!-- Allbot 카메라 -->
  <include file="$(find jetson_csi_cam)/jetson_csi_cam.launch" />
</launch>
```

#### 3.7.2. Lua 설정 파일: `allbot_lidar.lua`

**경로**: `~/catkin_ws/src/allbot/launch/include/allbot_lidar.lua`

```lua
include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,

  map_frame = "map",
  tracking_frame = "base_link",     -- IMU 미사용 시 base_link 권장
  published_frame = "odom",
  odom_frame = "odom",

  provide_odom_frame = false,        -- Cartographer가 odom 프레임을 발행하지 않음
  publish_frame_projected_to_2d = true,

  use_odometry = true,               -- odom 토픽 사용
  use_nav_sat = false,
  use_landmarks = false,

  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,

  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,

  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 0.1,     -- 1.0에서 0.1로 변경 (오류 방지)
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

MAP_BUILDER.use_trajectory_builder_2d = true

TRAJECTORY_BUILDER_2D.min_range = 0.12
TRAJECTORY_BUILDER_2D.max_range = 10.0
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 3.
TRAJECTORY_BUILDER_2D.use_imu_data = false                -- IMU 미사용
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians = math.rad(0.1)

POSE_GRAPH.constraint_builder.min_score = 0.65
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7

-- POSE_GRAPH.optimize_every_n_nodes = 0  -- 실시간 성능 튜닝 시 필요하면 주석 해제

return options
```

> **⚠️ 중요 변경 사항**:
> 1. **`tracking_frame`**: 원본 가이드에서는 `"imu_link"`였으나, `use_imu_data = false`이므로
>    IMU 프레임이 TF 트리에 존재하지 않을 수 있습니다. `"base_link"`로 변경하는 것을 권장합니다.
>    (로봇의 URDF에 `imu_link`가 정의되어 있다면 `"imu_link"` 유지 가능)
> 2. **`odometry_sampling_ratio`**: `1.0`에서 `0.1`로 변경 (높은 값에서 오류 발생 가능)
> 3. **`use_imu_data = false`**: IMU 센서가 없거나 사용하지 않을 경우 필수 설정

#### 3.7.3. Lua 파라미터 상세 설명

| 파라미터 | 설정값 | 설명 |
|----------|--------|------|
| `map_frame` | `"map"` | 월드 좌표계 프레임 |
| `tracking_frame` | `"base_link"` | 센서가 장착된 로봇 본체 프레임 |
| `published_frame` | `"odom"` | Cartographer가 발행하는 프레임 |
| `provide_odom_frame` | `false` | odom→map 변환을 Cartographer가 제공하지 않음 (로봇의 odom 사용) |
| `use_odometry` | `true` | 엔코더 기반 odometry 사용 |
| `num_laser_scans` | `1` | 사용하는 LaserScan 토픽 수 |
| `TRAJECTORY_BUILDER_2D.min_range` | `0.12` | 최소 인식 거리 (12cm) |
| `TRAJECTORY_BUILDER_2D.max_range` | `10.0` | 최대 인식 거리 (10m) |
| `TRAJECTORY_BUILDER_2D.use_imu_data` | `false` | IMU 데이터 미사용 |
| `POSE_GRAPH.constraint_builder.min_score` | `0.65` | 루프 클로저 최소 점수 (낮을수록 적극적) |

---

### 3.8. 실행 및 지도 저장

#### 실행 순서

```bash
# 터미널 1: Host PC - roscore 실행
roscore

# 터미널 2: Host PC - 키보드 원격 제어
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

# 터미널 3: SSH로 Jetson 연결 - 로봇 구동
ssh user@jetson-ip
roslaunch allbot bringup.launch

# 터미널 4: SSH로 Jetson 연결 - Cartographer SLAM 실행
ssh user@jetson-ip
roslaunch allbot lidar_slam_carto.launch

# 터미널 5: Host PC - RViz 시각화
rviz
# File → Open Config → 이전에 저장한 slam.rviz 설정 파일 로드
```

#### 지도 저장

```bash
# SSH로 Jetson 연결 후
rosrun map_server map_saver -f ~/catkin_ws/src/allbot/maps/map
```

저장 확인:
- `~/catkin_ws/src/allbot/maps/map.pgm` (그레이스케일 지도 이미지)
- `~/catkin_ws/src/allbot/maps/map.yaml` (지도 메타데이터)

```yaml
# map.yaml 예시
image: map.pgm
resolution: 0.05
origin: [-10.0, -10.0, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
```

> **권장**: Gmapping 지도 파일을 백업해 두세요:
> ```bash
> mv ~/catkin_ws/src/allbot/maps/map.pgm ~/catkin_ws/src/allbot/maps/map_gmapping.pgm
> mv ~/catkin_ws/src/allbot/maps/map.yaml ~/catkin_ws/src/allbot/maps/map_gmapping.yaml
> ```

---

## 4. 자주 발생하는 오류와 해결 방법

### 4.1. `libabsl-dev` 오류

**증상**: `rosdep install` 중 `libabsl-dev`를 찾을 수 없음

**원인**: Cartographer의 `package.xml`에 정의된 `libabsl-dev`가 ROS Noetic rosdep에 없음

**해결**:
```bash
sed -i 's/<depend>libabsl-dev<\/depend>/<!-- <depend>libabsl-dev<\/depend> -->/' \
  ~/noncatkin_ws/src/cartographer/package.xml
rosdep install --from-paths src --ignore-src --rosdistro=${ROS_DISTRO} -y
```

### 4.2. `libqt5core5t64` 패키지 없음

**증상**: `E: Unable to locate package libqt5core5t64`

**원인**:
- Ubuntu 24.04 (Noble)의 새로운 패키지명이 Jetson 저장소에 없거나
- Ubuntu 22.04 (Jammy)에서 `t64` 패키지를 찾으려고 할 때

**해결**:
```bash
rosdep install --from-paths src --ignore-src \
  --rosdistro=${ROS_DISTRO} -y \
  --skip-keys=libqt5-core
```

### 4.3. `catkin_make_isolated` 명령 없음

**증상**: `catkin_make_isolated: command not found`

**원인**: `catkin_make_isolated`가 설치되지 않음

**해결**:
```bash
sudo apt-get install -y python3-catkin-tools
# 또는
sudo apt-get install -y ros-${ROS_DISTRO}-catkin
```

### 4.4. Abseil 빌드 실패 (Jetson ARM64)

**증상**: `install_abseil.sh` 실행 중 컴파일 오류

**해결**:
```bash
# 수동으로 Abseil 빌드 (ARM64 최적화 플래그 포함)
git clone https://github.com/abseil/abseil-cpp.git /tmp/abseil-cpp
cd /tmp/abseil-cpp
mkdir build && cd build
cmake -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
      -DCMAKE_CXX_FLAGS="-mno-outline-atomics" \
      -DCMAKE_INSTALL_PREFIX=/usr/local \
      ..
make -j$(nproc)
sudo make install
```

### 4.5. `rosdep init` 에러

**증상**: `sudo: rosdep: command not found`

**해결**:
```bash
sudo apt-get install -y python3-rosdep python3-rosinstall python3-rosinstall-generator
sudo rosdep init
rosdep update
```

### 4.6. TF 에러: `tracking_frame` not found

**증상**: Cartographer 실행 중 `"base_link" passed to lookupTransform argument target_frame does not exist`

**원인**: `tracking_frame`으로 지정한 프레임이 TF 트리에 없음

**해결**:
1. URDF에서 `imu_link` 프레임이 정의되어 있는지 확인
2. 또는 `tracking_frame`을 `"base_link"`로 변경
3. `rosrun tf tf_echo base_link map`으로 TF 트리 상태 확인

### 4.7. `odometry_sampling_ratio` 오류

**증상**: Cartographer 실행 중 odometry sampling ratio 관련 오류

**해결**: Lua 파일에서 `odometry_sampling_ratio = 0.1`로 설정 (1.0에서 변경)

### 4.8. 빌드 중 메모리 부족 (Jetson)

**증상**: 빌드 중 `Killed` 또는 `SIGKILL` 메시지

**해결**:
```bash
# 병렬 작업 수 제한
catkin_make_isolated --install --use-ninja -j2

# 또는 swap 공간 추가
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 5. Jetson (ARM64) 특이사항

### 5.1. 아키텍처 차이

| 항목 | 일반 PC (x86_64) | Jetson (ARM64/aarch64) |
|------|------------------|----------------------|
| 플랫폼 | amd64 | arm64 |
| 패키지 저장소 | 일반 Ubuntu 저장소 | Jetson 특화 저장소 (일부 패키지 상이) |
| 성능 | 높음 | 제한적 (전력 효율 중심) |
| CUDA 지원 | GPU에 따라 다름 | 내장 GPU (최적화 필요) |

### 5.2. 주요 고려 사항

1. **메모리 관리**
   - Jetson Nano: 4GB RAM → swap 필수
   - Jetson TX2: 8GB RAM
   - Jetson Xavier: 16GB/32GB RAM
   - 빌드 시 `-j$(nproc)` 대신 `-j2` 또는 `-j3` 권장

2. **ARM64 패키지 가용성**
   - 일부 ROS 패키지가 ARM64에서 누락될 수 있음
   - `libqt5core5t64` 오류가 ARM64에서 더 자주 발생

3. **Abseil 빌드**
   - ARM64에서 Abseil 컴파일 시 `-mno-outline-atomics` 플래그 필요할 수 있음
   - GCC 버전에 따라 다른 컴파일 플래그 필요

4. **CUDA 가속**
   - Cartographer는 기본적으로 CUDA를 사용하지 않음
   - Jetson GPU는 SLAM에 직접 사용되지 않음 (CPU 기반 연산)

### 5.3. 권장 빌드 설정

```bash
# build.sh (Jetson 최적화)
#!/bin/bash
export ROS_DISTRO=noetic
source /opt/ros/${ROS_DISTRO}/setup.bash

cd ~/noncatkin_ws

# 의존성 설치 (문제 해결 옵션 포함)
rosdep install --from-paths src --ignore-src \
  --rosdistro=${ROS_DISTRO} -y \
  --skip-keys=libqt5-core

# Abseil 빌드
src/cartographer/scripts/install_abseil.sh

# ROS Abseil 제거 (설치된 경우만)
sudo apt-get remove ros-${ROS_DISTRO}-abseil-cpp 2>/dev/null || true

# 빌드 (메모리 제한 고려)
catkin_make_isolated --install --use-ninja -j2
```

---

## 6. Gmapping vs Cartographer 비교

| 항목 | Gmapping | Cartographer |
|------|----------|--------------|
| **개발사** | OpenSlam (Brian Gerkey) | Google |
| **방식** | Particle Filter (RBPF) | Graph SLAM (Submap + SPA) |
| **실시간성** | 좋음 | 매우 좋음 |
| **대규모 맵** | 입자 수 증가로 느려짐 | 서브맵 기반으로 확장성 우수 |
| **루프 클로저** | 지원하지 않음 (단방향) | **지원** (백엔드 최적화) |
| **IMU 융합** | 제한적 | **우수** (IMU 데이터 적극 활용) |
| **3D 지원** | 불가능 | **가능** (3D LiDAR, 카메라) |
| **멀티 센서** | LaserScan 전용 | LaserScan, PointCloud, Odometry 등 |
| **설정 복잡도** | 낮음 | 높음 (Lua 파라미터 조정 필요) |
| **계산량** | 중간 | 높음 (특히 CSM 활성화 시) |
| **지도 정확도** | 기본적인 SLAM에 적합 | **더 정밀** (루프 클로저로 누적 오차 보정) |
| **빌드 난이도** | 쉬움 (apt install 가능) | **어려움** (소스 빌드, Abseil 이슈 등) |

### Cartographer의 장점

1. **루프 클로저(loop closure)** 지원 → 대규모 환경에서 누적 오차 보정
2. **서브맵 기반** → 계산 효율성 우수
3. **백엔드 그래프 최적화** → 전역 정합성 향상
4. **멀티 센서 융합** → LiDAR + IMU + Odometry 조합으로 정밀도 향상

### Cartographer의 단점

1. **설치 과정 복잡** → 소스 빌드 필요, Abseil ABI 이슈
2. **파라미터 튜닝 필요** → Lua 파일 수동 설정
3. **계산량 높음** → Jetson 같은 저성능 플랫폼에서 부담

---

## 7. 참고 자료

### 공식 문서

- [Cartographer ROS 공식 설치 가이드](https://github.com/cartographer-project/cartographer_ros/blob/master/docs/source/compilation.rst)
- [Cartographer 공식 문서](https://google-cartographer.readthedocs.io/)
- [Cartographer ROS Lua 설정 문서](https://github.com/cartographer-project/cartographer_ros/blob/master/docs/source/configuration.rst)

### 관련 GitHub 이슈

- [libabsl-dev not available #1726](https://github.com/cartographer-project/cartographer_ros/issues/1726)
- [Abseil ABI 문제](https://github.com/cartographer-project/cartographer_ros/issues?q=abseil)
- [libqt5core5t64 rosdistro 이슈](https://github.com/ros/rosdistro/issues/44826)

### ROS 관련

- [ROS Noetic 설치 가이드](http://wiki.ros.org/noetic/Installation)
- [catkin_make_isolated 문서](http://wiki.ros.org/catkin/commands/catkin_make_isolated)
- [rosdep 사용법](http://wiki.ros.org/rosdep)

---

## 부록: 문제 진단 체크리스트

설치 과정에서 문제가 발생했을 때 하나씩 확인해보세요:

```
□ ROS_DISTRO 환경변수가 설정되어 있는가? (echo $ROS_DISTRO)
□ apt 저장소가 최신인가? (sudo apt-get update)
□ python3-wstool, python3-rosdep이 설치되었는가?
□ ~/noncatkin_ws/src/cartographer/package.xml에서 libabsl-dev가 주석 처리되었는가?
□ rosdep install 시 --skip-keys=libqt5-core가 사용되었는가?
□ install_abseil.sh이 정상 실행되었는가? (권한, 경로 확인)
□ ros-${ROS_DISTRO}-abseil-cpp가 제거되었는가?
□ catkin_make_isolated가 정상 완료되었는가? (CMake 에러 확인)
□ install_isolated/setup.bash가 source 되었는가?
□ launch 파일에서 Lua 설정 파일 경로가 올바른가?
□ tracking_frame이 TF 트리에 존재하는가?
□ odometry_sampling_ratio가 0.1로 설정되었는가?
```

---

> **최종 요약**: Cartographer 설치는 크게 (1) 의존성 설치 중 libabsl-dev와 libqt5core5t64 문제 해결,
> (2) Abseil 수동 빌드, (3) catkin_make_isolated 빌드의 세 단계로 나눌 수 있습니다.
> 가장 문제가 되는 `rosdep install` 단계에서는 `package.xml` 수정과 `--skip-keys` 옵션으로
> 우회한 후, Abseil을 수동 빌드하여 정상 설치할 수 있습니다.
