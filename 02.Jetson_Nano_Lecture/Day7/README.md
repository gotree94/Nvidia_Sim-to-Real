# Day2


https://brev.nvidia.com/

## 1. Brev

* 1.1 brev.nvidia.com
   * 복잡한 설정 없이 NVIDIA GPU  서버를 편하게 사용할 수 있는 서비스
   * 로그인할때 allai12@allai.co.kr로(0519Kosa#) 로그인하고 -> 다른방법으로 -> 다름에 google 계정으로 선택하면 됨.

<img src="001.png" width="60%">

* 1.2 Launchables > My launchables 에서 ku 선택

<img src="004.png" width="60%">

* 1.3 Deploy Launchable > Go to Instance Page (우측 하단에 버튼이 있음)
  * Deploy Launchable로 문제 없이 Deploy가 잘 되면 상관 없지만, 잘 되지 않을 경우 꼭 질문할 것
  * 사용하고 싶은데 서버가 선점되었다면 다른 서버를 실행하기 위함.

<img src="004.png" width="60%">

* 1.4 Instance는 다음 항목 들로 한정 (금요일 제외)

<img src="003.png">

<img src="002.png">

* 1.5 화면 하단의 Using Secure Links > Share a Service
   * 8080 입력 후 Create

<img src="005.png">

* 1.6 Brev 시작
   * 사용자 이름: allai / 비밀번호: kosa 
   * 입력 후 START 버튼을 눌러 원격 데스크톱 시작

<img src="010.png">

---

## 2. Isaac Sim
   * NVIDIA Isaac Sim™은 NVIDIA Omniverse 기반의 로봇 시뮬레이션 Reference Application입니다.
      -	가상 물리 환경 기반 로봇 테스트 및 개발
      -	Omniverse Kit backend 기반 Extension 사용 가능
      -	정적 USD 파일에 ‘Runtime Interaction’ 부여
      -	Newton Physics, Warp, Cosmos 등 무궁무진한 업데이트 및 상호작용

* User Interface Reference
   * https://docs.isaacsim.omniverse.nvidia.com/5.1.0/gui/reference_user_interface.html
       •	Menu Bar
       •	Viewport
       •	Main Toolbar
       •	Browsers
       •	Stage
       •	Property Panel

* Menu Bar
       •	Create
       •	Window
       •	Tools
       •	Utilities
       •	Layout

* Navigation
   * https://docs.isaacsim.omniverse.nvidia.com/5.1.0/gui/reference_keyboard_shortcuts.html
       * 우 클릭 유지 - 카메라 회전
       * 휠 클릭 유지 - 카메라 이동
       * 휠 스크롤 - 확대/축소
       * Delete - 선택 삭제
       * Space - 애니메이션 시작/정지
       * 우 클릭 유지 + (W/A/S/D) - 앞/뒤/왼/오 이동

* Navigation
   * Toolbar를 눌러 직접 물체를 다양하게 (translation, rotation) 조종하거나 
   * W(translation)
   * E(rotation)
   * R(Scale) 을 눌러 조종 방식 변환해보기
   * 회전: 우클릭+드래그, 좌클릭+ALT,
   * 마우스 휠 클릭: 시점 이동
   * F: 선택한 물체로 시점 변경

* Tool Bar
   * Selection Modes
   * Mode(Global/Local)
   * Rotate(Global/Local)
   * Scale
   * Snap
   * Play/Stop

* Tabs
   * 실수로 무언가를 지웠다면
   * ctrl + 1 또는
   * Layouts > Default Layout 

## 실습1: Basic Tutorial

* STEP 1
   * 1. Ground Plane 추가 : Create > Physics > Ground Plane
   * 2. Light Source 추가 : Create > Lights > Distant Light
   * 3. Visual Cube 추가 : Create > Shape > Cube

* STEP 2
   * 큐브의 Translate, Rotate, Scale을 변경해보기

* STEP 3
   * Cube 항목을 우클릭하여 > Add > Physics > Rigid Body with Colliders Preset
   * 이후 실행 버튼을 눌러 Simulation 시작 
   * Rigidbody나 Collider만 있을 경우 각각 어떻게 될 지 생각해보기

* STEP 4 : 중력의 방향 수정해보기
   * Create > Physics > Physics Scene

* STEP 5
   * Create > Robots > Franka Emika Panda Arm 으로 Franka Panda 생성
   * Tools > Physics > Physics Inspector로 Joint 값 변경해보기

* STEP 6 : Assemble a Simple Robot
   * Ground Plane을 생성한 상태에서, World Prim 아래에 Xform을 생성 translate (0, 0, 1)
   * 생성한 Xform의 child에 Cube와 Cylinder를 생성(Shape)
   * Cube의 Scale(1, 2, 0.5)

* STEP 7: Assemble a Simple Robot
   * 동일한 방법으로 wheel_left, wheel_right Xform 생성 및 Translate, Orient 부여
   * wheel_left: Translate (1.5, 0, 1) Orient (90, 0, 0)
   * wheel_right: Translate( -1.5, 0, 1) Orient (90, 0, 0)
   * 생성한 xform 내부에 create > shape > cylinder
   * cylinder의 Property > Geometry > Axis 를 X로 설정 

* STEP 8 : Assemble a Simple Robot
   * 메쉬 복수 선택 > Add > Physics > Rigid Body with Colliders Preset

* STEP 9 : Assemble a Simple Robot
   * 이렇게 생성된 Collision Mesh 등 요소들은 위 눈 모양의 Show By Type 버튼을 통해 확인가능

* STEP 10 : Assemble a Simple Robot
   * Joint 추가해보기
   * 몸체 Cube와 Cylinder를 차례대로 선택 한 후 우클릭 > Create > Physics > Joint > Revolute Joint
   * 시뮬레이션을 시작하고, Xform을 선택한 후 마우스로 드래그하여 움직임 확인

* STEP 11 : Assemble a Simple Robot
   * Joint Drive 추가
   * Joint를 선택한 후, Property의 Add > Physics > Angular Drive

* STEP 12 : Assemble a Simple Robot
   * 다음과 같이 설정한 후, Play

---

## 3. Review
- Joint를 연결하려면 RigidBody 속성을 가지고 있어야 한다.
- 움직임을 위한 Articulation Root는 Root 프림에 설정하는 것을 권장
- Parent Prim에 RigidBody 속성을 적용하고, Child Prim에 RigidBody 속성을 중복으로 적용하는 것을 피해야 한다.

* STEP 1 : Collider
   * /Isaac/5.1/Isaac/Robots/NVIDIA/Jetbot에서 Jetbot.usd를 불러온 후, Collider를 확인해보자

* STEP 2 : Collider
   * /jetbot/chassis/geometry 아래 메쉬의 Approximation 방식을 바꿔가면서, Collision Mesh의 변화를 볼 수 있다.

   * 메쉬를 분리하고 Collision Mesh를 적용하여 정교함을 얻을 수 있지만, 성능과 속도의 trade-off 관계를 가진다

---

## 4. DLI 
   * Software-in-the-Loop Testing for Robots With OpenUSD, Isaac Sim, and ROS

   * https://docs.isaacsim.omniverse.nvidia.com/5.1.0/omnigraph/omnigraph_tutorial.html
   
   * https://learn.nvidia.com/courses/course-detail?course_id=course-v1:DLI+S-OV-39+V1

* Download : 6.0.0 : https://github.com/isaac-sim/IsaacSim/tree/develop


```
DModel      aaaa  ALab.zip      DLI_SIL_online_dli      JungleRuins             main_sponza      pkg_b_ivy       pkg_c_trees      roboot2.usd  test.usd
3DModel.zip  ALab  assemble.usd  DLI_SIL_online_dli.zip  JungleRuins_1_0_1b.zip  main_sponza.zip  pkg_b_ivy1.zip  pkg_c_trees.zip  robot.usd
ubuntu@e2e484f2865a:~/Downloads$ cd DLI_SIL_online_dli
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli$ ls
Checkpoint1_nova_carter  Checkpoint2_franka  Checkpoint3_occupancy_map  Checkpoint4_completed_environment  Checkpoint5_completed_ros_package  Starting_point
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli$ cd Starting_point/
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point$ ls
franka  gtc25-mega1  nova_carter  owl  warehouse_env
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point$ cd gtc25-mega1/
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1$ ls
install.sh  README.md  ros_ws
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1$ cat README.md 
# GTC25-MEGA1 Lab

This repository is part of the GTC MEGA 1 Lab, providing essential resources and instructions for setting up and building the project.

## Installation Instructions

To build and set up the project, follow these steps:

**Run the Installation Script**

Execute the provided installation script to set up the environment from the root folder:
```bash
bash ./install.sh
```

This script will:
- Initialize and update submodules.
- Install ROS 2 Humble, including setting up the locale and sources.
- Install the `nova_carter_description` package.
- Configure and build the ROS workspace.

ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1$ chmod +x install.sh 
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1$ 
```

* 설치시 에러가 나기 때문에 아래의 추가 설치 후 확인

```
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1$ ./install.sh
...
...
...
Installing ROS workspace...
Configuring and building ROS workspace...
/usr/bin/sudo: 175: rosdep: not found
./install.sh: line 75: rosdep: command not found
./install.sh: line 77: rosdep: command not found
./install.sh: line 78: colcon: command not found
./install.sh: line 79: install/setup.bash: No such file or directory
ROS Workspace installation complete.
ubuntu@e2e484f2865a:~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1$ 
```

```
sudo apt install python3-rosdep
sudo rosdep init
sudo rosdep update
sudo apt-get update && sudo apt-get install -y   ros-humble-topic-tools   ros-humble-navigation2   ros-humble-nav2-amcl   ros-humble-nav2-bringup   ros-humble-nav2-bt-navigator   ros-humble-nav2-costmap-2d   ros-humble-nav2-core   ros-humble-nav2-dwb-controller   ros-humble-nav2-lifecycle-manager   ros-humble-nav2-map-server   ros-humble-nav2-behaviors   ros-humble-nav2-planner   ros-humble-nav2-msgs   ros-humble-nav2-navfn-planner   ros-humble-nav2-rviz-plugins   ros-humble-nav2-behavior-tree   ros-humble-nav2-util   ros-humble-nav2-voxel-grid   ros-humble-nav2-controller   ros-humble-nav2-waypoint-follower   ros-humble-pointcloud-to-laserscan   ros-humble-joint-state-publisher-gui   ros-humble-xacro   ros-humble-moveit   ros-humble-topic-based-ros2-control   ros-humble-ros2-control   ros-humble-ros2-controllers   ros-humble-moveit-simple-controller-manager
sudo apt-get install -y python3-colcon-common-extensions
colcon build
source install/setup.bash
```

```

**문제 분석**

   * 1. rosdep, colcon 명령어 없음
   * 설치 스크립트에서 rosdep과 colcon이 설치되지 않은 상태에서 호출됨.

   * 2. ament_cmake not found
   * ROS 2 환경(source /opt/ros/humble/setup.bash)이 적용되지 않은 상태에서 colcon build 실행.

   * 3. APT sources.list 중복
   * NVIDIA 저장소가 sources.list에 두 번(:43과 :44) 등록됨.

**해결 방법**
   * Step 1: 중복 APT 저장소 정리

```
# 중복 라인 확인
grep -n "isaac" /etc/apt/sources.list

# 중복 제거 (첫 번째는 남기고 두 번째부터 삭제)
sudo sed -i '/isaac\.download\.nvidia\.com\/isaac-ros/{2,$d}' /etc/apt/sources.list

# 또는 파일을 열어서 직접 중복 라인 삭제
sudo nano /etc/apt/sources.list
```

   * Step 2: 빠진 패키지 설치

```
# rosdep 설치
sudo apt update
sudo apt install -y python3-rosdep python3-colcon-common-extensions

# rosdep 초기화
sudo rosdep init
rosdep update
```

   * Step 3: ROS 2 Humble 재확인 (ament_cmake 포함)

```
# ament_cmake가 실제로 설치되었는지 확인
dpkg -l | grep ament-cmake

# 없으면 재설치
sudo apt install --reinstall -y ros-humble-desktop
```

   * Step 4: 올바른 순서로 빌드

```
cd ~/Downloads/DLI_SIL_online_dli/Starting_point/gtc25-mega1/ros_ws

# ROS 환경 먼저 source (반드시 동일 쉘에서)
source /opt/ros/humble/setup.bash

# echo $AMENT_PREFIX_PATH 로 환경이 잡혔는지 확인
echo $AMENT_PREFIX_PATH  # 비어있지 않아야 정상

# rosdep으로 의존성 설치
rosdep install --from-paths src --ignore-src -r -y

# colcon build
colcon build

# workspace 환경 source
source install/setup.bash
✅ 권장: 전체 수정 설치 스크립트
기존 install.sh 대신 아래 내용으로 새로 만들어 실행:

#!/bin/bash
set -e  # 에러 발생 시 중단

# ============================================
# ROS 2 Humble 설치
# ============================================
sudo apt update -y && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install -y software-properties-common
sudo add-apt-repository -y universe
sudo apt update -y && sudo apt install -y curl

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update -y && sudo apt upgrade -y
sudo apt install -y ros-humble-desktop

# ============================================
# ROS 빌드 도구 설치
# ============================================
sudo apt install -y python3-rosdep python3-colcon-common-extensions

# ============================================
# NVIDIA Isaac ROS 저장소 등록
# ============================================
sudo apt install -y gnupg wget
wget -qO - https://isaac.download.nvidia.com/isaac-ros/repos.key | sudo apt-key add -

# 중복 방지: 이미 있으면 추가 안 함
if ! grep -q "isaac.download.nvidia.com/isaac-ros" /etc/apt/sources.list; then
  echo "deb https://isaac.download.nvidia.com/isaac-ros/release-3 $(lsb_release -cs) release-3.0" | sudo tee -a /etc/apt/sources.list
fi

sudo apt update -y

# ============================================
# nova_carter_description 설치
# ============================================
sudo apt install -y ros-humble-nova-carter-description

# ============================================
# ROS workspace 빌드
# ============================================
cd ros_ws

# ROS 환경 source
source /opt/ros/humble/setup.bash

# rosdep
sudo rosdep init || true  # 이미 init 되어있으면 skip
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# colcon build
colcon build

source install/setup.bash
echo "✅ ROS Workspace installation complete."
```

---

```Makefile
 # Install ROS workspace
 echo "Installing ROS workspace..."
 cd ros_ws
  
 # Configure and build ROS workspace
 echo "Configuring and building ROS workspace..."
 source /opt/ros/humble/setup.bash
 sudo rosdep init
 rosdep update
 
 rosdep install --from-paths src --ignore-src -r -y
 colcon build
 source install/setup.bash
 
 echo "ROS Workspace installation complete."
```

