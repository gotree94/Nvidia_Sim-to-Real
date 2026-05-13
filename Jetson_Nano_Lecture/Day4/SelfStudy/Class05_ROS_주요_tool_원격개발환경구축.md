# Class 05: ROS 주요 tool 보기 및 원격 개발 환경 구축

## 1. ROS 주요 도구 실습

### 1.1 rqt_graph 실습

```bash
# rqt_graph 실행
rosrun rqt_graph rqt_graph

# 또는
rqt_graph
```

### 1.2 rqt_plot 실습

```bash
# 토픽 데이터 플롯
rqt_plot /odom/pose/pose/position/x:y:z

# 특정 주제 플롯
rqt_plot /scan/ranges[0]
```

### 1.3 rqt_console 실습

```bash
# 로그 메시지 확인
rqt_console
```

### 1.4 rqt_reconfigure 실습

```bash
# 동적 파라미터 설정
rosrun rqt_reconfigure rqt_reconfigure
```

### 1.5 rviz 주요 설정

```bash
# rviz 실행
rviz

# 주요 Displays 설정:
# - Fixed Frame: base_footprint
# - Grid: 표시
# - RobotModel: URDF 연동
# - TF: 좌표계 표시
# - LaserScan: 라이다 데이터
# - Map: SLAM 맵
# - Path: 경로 표시
# - Pose: 자세 표시
```

## 2. 원격 개발 환경 구축

### 2.1 네트워크 설정

```bash
# Master (로봇)에서
# ~/.bashrc에 추가
export ROS_MASTER_URI=http://192.168.1.100:11311
export ROS_HOSTNAME=192.168.1.100

# PC (원격)에서
# ~/.bashrc에 추가
export ROS_MASTER_URI=http://192.168.1.100:11311
export ROS_HOSTNAME=192.168.1.50
```

### 2.2 SSH 설정

```bash
# SSH 서버 설치 (로봇)
sudo apt install openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh

# PC에서 로봇에 접속
ssh username@192.168.1.100

# 키 기반 SSH 설정
ssh-keygen -t rsa
ssh-copy-id username@192.168.1.100
```

### 2.3 네트워크 연결 테스트

```bash
# Master에서
roscore

# 원격 PC에서
rostopic list
rostopic hz /scan

# 토픽 데이터 확인
rostopic echo /odom
```

### 2.4 패키지 동기화

```bash
# Rsync를 통한 패키지 동기화
rsync -avz --exclude='.git' --exclude='build' --exclude='devel' \
    ~/catkin_ws/src/ username@192.168.1.100:~/catkin_ws/src/

# Git을 통한 동기화 (권장)
# 원격에서 Git 서버 사용 (GitHub, GitLab)
git remote -v
git push origin main
```

## 3. 개발 환경 설정

### 3.1 VS Code 설정

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Build ROS",
      "type": "shell",
      "command": "cd ~/catkin_ws && catkin build",
      "group": "build",
      "problemMatcher": ["$catkin-gcc"]
    },
    {
      "label": "Source ROS",
      "type": "shell",
      "command": "source ~/catkin_ws/devel/setup.bash",
      "problemMatcher": []
    }
  ]
}
```

### 3.2 Development Container

```dockerfile
# Dockerfile
FROM osrf/ros:noetic-desktop-full

RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    vim \
    openssh-client

RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws

RUN pip3 install jupyter notebook

CMD ["/bin/bash"]
```

```bash
# Container 빌드 및 실행
docker build -t ros-dev .
docker run -it -p 6080:6080 -p 11311:11311 ros-dev
```

### 3.3 원격 디버깅

```python
# VS Code용launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "ROS: Launch",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/src/my_package/scripts/my_node.py",
      "console": "integratedTerminal",
      "env": {
        "ROS_MASTER_URI": "http://192.168.1.100:11311"
      }
    }
  ]
}
```

## 4. SSH 터널링

### 4.1 로컬 터널링

```bash
# 원격 ROS Master에 터널링
ssh -L 11311:localhost:11311 username@192.168.1.100
```

### 4.2 Gazebo 원격 실행

```bash
# Gazebo 클라이언트 원격 실행
# Master에서
roslaunch gazebo_ros empty_world.launch

# 원격 PC에서
export GAZEBO_MASTER_URI=http://192.168.1.100:11345
gzclient
```

## 5. 자동화 스크립트

### 5.1 연결 스크립트

```bash
#!/bin/bash
# connect_to_robot.sh

ROBOT_IP="192.168.1.100"
USERNAME="ubuntu"

echo "로봇에 SSH 연결..."
ssh ${USERNAME}@${ROBOT_IP}
```

### 5.2 동기화 스크립트

```bash
#!/bin/bash
# sync_workspace.sh

ROBOT_IP="192.168.1.100"
USERNAME="ubuntu"
LOCAL_WS="$HOME/catkin_ws"

echo "동기화 시작..."
rsync -avz --progress \
    --exclude='build' \
    --exclude='devel' \
    ${LOCAL_WS}/src/ \
    ${USERNAME}@${ROBOT_IP}:${LOCAL_WS}/src/

echo "동기화 완료!"
```

### 5.3 원격 빌드 스크립트

```bash
#!/bin/bash
# remote_build.sh

ROBOT_IP="192.168.1.100"
USERNAME="ubuntu"

ssh ${USERNAME}@${ROBOT_IP} << 'EOF'
    cd ~/catkin_ws
    source /opt/ros/noetic/setup.bash
    catkin build
EOF
```

## 6. 원격 개발 실제 구성

### 6.1 구성도

```
┌──────────────┐        ┌──────────────┐
│  Developer   │        │   Robot      │
│     PC       │◀──────▶│ (Jetson Nano)│
│              │  SSH   │              │
│  - VS Code   │        │ - ROS Master │
│  - Terminal  │        │ - Hardware   │
│  - RViz      │        │ - Sensors    │
└──────────────┘        └──────────────┘
```

### 6.2 워크플로우

```
1. PC에서 코드 개발
2. Git에 푸시
3. 로봇에서 풀
4. 빌드
5. 실행 및 테스트
6. RViz로 시각화 (PC 또는 로봇)
```

## 7. 실습 과제

1. SSH를 통해 로봇에 연결하세요.
2. 원격 PC에서 rviz를 실행하고机器人을 확인하세요.
3. 원격에서 토픽을Subscribe하여 데이터를 확인하세요.
4. 패키지 동기화 스크립트를 작성하세요.

## 8. 다음 실습 예고

다음 클래스에서는 원격 개발 환경 구축 실습을 계속합니다.