# DLI 개발 환경 설치 및 설정 가이드

> **코스**: OpenUSD, Isaac Sim, ROS를 활용한 로봇 소프트웨어-인-더-루프 테스트
> **대상 하드웨어**: ASUS ROG Strix SCAR 16 G635LX (Intel Core Ultra 9, NVIDIA GeForce RTX 5090, 64GB RAM, 4TB SSD)
> **OS 상태**: Ubuntu 22.04.5 LTS 설치 완료 ✅
> **GPU 드라이버**: NVIDIA Driver 580.159.04 + CUDA 13.0 (RTX 5090) 설치 완료 ✅

---

## 목차

1. [시스템 요구사항 개요](#1-시스템-요구사항-개요)
2. [Ubuntu 22.04 시스템 확인](#2-ubuntu-2204-시스템-확인)
3. [NVIDIA 드라이버 설치 (RTX 5090)](#3-nvidia-드라이버-설치-rtx-5090)
4. [기본 개발 도구 설치](#4-기본-개발-도구-설치)
5. [ROS 2 Humble 설치](#5-ros-2-humble-설치)
6. [Isaac Sim 설치](#6-isaac-sim-설치)
7. [ROS 2 Workspace 빌드](#7-ros-2-workspace-빌드)
8. [DLI 코스 에셋 다운로드](#8-dli-코스-에셋-다운로드)
9. [모듈별 실행 요약](#9-모듈별-실행-요약)
10. [문제 해결](#10-문제-해결)
11. [참고 자료](#11-참고-자료)

---

## 1. 시스템 요구사항 개요

### 1.1 하드웨어 사양 (본 장비)

| 구성 요소 | 사양 | Isaac Sim 요구사항 대비 |
|-----------|------|------------------------|
| CPU | Intel Core Ultra 9 (16코어) | **초과** (Ideal: 16코어) |
| GPU | NVIDIA GeForce RTX 5090 (Blackwell, 24GB VRAM) | **초과** (Ideal: RTX Ada 6000) |
| RAM | 64GB | **충족** (Ideal: 64GB) |
| 저장소 | 4TB NVMe SSD | **초과** (Ideal: 1TB NVMe) |
| OS | Ubuntu 22.04 LTS (권장) | **충족** |

### 1.2 필요 소프트웨어 스택

```
Ubuntu 22.04 LTS
  └─ NVIDIA Driver 580.159.04 (≥ 580.65.06) ✅ 설치 완료
      ├─ CUDA 13.0 (드라이버에 내장) ✅
      └─ NVIDIA Container Toolkit (선택사항)
  ├─ ROS 2 Humble
  │   ├─ colcon
  │   ├─ Nav2 (내비게이션)
  │   ├─ MoveIt2 (조작)
  │   └─ 다양한 ROS 패키지 (vision_msgs, ackermann_msgs 등)
  ├─ Isaac Sim 5.1.0 (또는 5.0.0, 4.5.0)
  ├─ Parsec (원격 데스크톱, 선택사항)
  │   └─ ⚠️ 주의: `curl https://parsec.app/install/parsec.sh | sudo bash` 스크립트는 **404 반환으로 사용 불가**
  │   └─ ✅ Snap으로 설치: `sudo snap install parsec --classic`
  └─ DLI 코스 에셋 (DLI_SIL_online_dli.zip)
```

### 1.3 중요 호환성 노트

| 항목 | 내용 |
|------|------|
| **RTX 5090 + Ubuntu 22.04** | Blackwell GPU는 최신 커널(≥ 6.8)과 오픈 커널 모듈 NVIDIA 드라이버 필요 |
| **Isaac Sim + ROS 2** | Isaac Sim 4.5/5.0은 ROS 2 Humble(Ubuntu 22.04) 또는 Jazzy(Ubuntu 24.04) 지원 |
| **DLI 코스 기준** | 본 과정은 **Isaac Sim 4.5 + ROS 2 Humble + Ubuntu 22.04** 기반. **5.1.0에서도 정상 작동 확인** |
| **듀얼 부팅** | Windows + Ubuntu 듀얼 부팅 권장 (Isaac Sim은 WSL2 GPU 지원이 제한적) |
| **Isaac Lab ❌** | **본 DLI 과정에 Isaac Lab은 필요하지 않음.** Isaac Lab은 강화학습/로봇 학습용 프레임워크로, 이 과정(Nav2 + MoveIt2 + ROS 2 SIL)과 무관 |

---

## 2. Ubuntu 22.04 시스템 확인

> ✅ **Ubuntu 22.04.5 LTS가 이미 설치되어 있습니다.** 아래 확인 절차를 진행한 후, NVIDIA 드라이버 → ROS 2 → Isaac Sim 순서로 설치하세요.

Ubuntu 22.04.5 LTS는 기본적으로 **HWE (Hardware Enablement) 커널 6.8**이 포함되어 있어 Intel Core Ultra 9 (Arrow Lake)와 RTX 5090(Blackwell)에 대한 기본 호환성을 제공합니다.

### 2.1 설치 상태 확인

```bash
# OS 버전 확인
cat /etc/os-release | grep -E "^NAME|^VERSION"
# → Ubuntu 22.04.5 LTS

# 현재 커널 버전 확인 (6.8 이상 필요)
uname -r
# → 6.8.0-xx-generic (이상적)

# CPU 정보 확인
cat /proc/cpuinfo | grep "model name" | head -1

# 메모리 확인
free -h

# 디스크 확인
df -h /
```

### 2.2 커널 호환성 체크

| 항목 | 필요 조건 | Ubuntu 22.04.5 기본 | 조치 |
|------|----------|--------------------|------|
| Intel Arrow Lake (Core Ultra 9) | 커널 ≥ 6.8 | **6.8.x (HWE 기본 내장)** ✅ | 추가 조치 불필요 |
| RTX 5090 (Blackwell) | 커널 ≥ 6.8 + 오픈 커널 모듈 드라이버 | **6.8.x 충족** ✅ | NVIDIA 드라이버만 설치 |
| NVIDIA 드라이버 | ≥ 580.65.06 | **580.159.04 설치 완료** ✅ | [Section 3.5](#35-실제-설치-사례-및-트러블슈팅) 참고 |

> **⚠️ 만약 커널 버전이 6.5 미만으로 확인될 경우** 다음 명령어로 HWE 커널을 수동 설치하세요:
> ```bash
> sudo apt update
> sudo apt install --install-recommends linux-generic-hwe-22.04
> sudo reboot
> ```

### 2.3 BIOS 설정 확인 (듀얼 부팅 시)

```bash
# Secure Boot 상태 확인
mokutil --sb-state
# → "SecureBoot disabled" 권장 (NVIDIA 드라이버 설치 문제 방지)
```

> `SecureBoot enabled` 상태면 NVIDIA 오픈 커널 모듈 드라이버 설치 시 서명 문제가 발생할 수 있습니다. **BIOS 진입 후 Secure Boot 비활성화를 권장합니다.**

---

## 3. NVIDIA 드라이버 설치 (RTX 5090)

> **🔴 중요**: RTX 5090(Blackwell)은 **오픈 커널 모듈** 드라이버가 필요합니다.
> - `nvidia-driver-5xx-open` 시리즈를 사용해야 함
> - 독점(proprietary) 드라이버는 RTX 5090에서 제대로 작동하지 않음

### 3.0 설치 전 확인

NVIDIA 드라이버가 이미 설치되어 있는지 먼저 확인합니다.

```bash
# 1. GPU 인식 확인
lspci | grep -i nvidia
# → "NVIDIA GeForce RTX 5090" 출력 확인

# 2. 드라이버 로드 확인
nvidia-smi
# → RTX 5090 인식 + Driver Version 표시되면 ✅ 이미 설치됨 → 3.4로 건너뛰기
# → "NVIDIA-SMI has failed" → 설치 필요 ❌ (또는 DKMS 모듈 누락)

# 3. 현재 설치된 NVIDIA 패키지 확인
dpkg -l | grep nvidia-driver
# → nvidia-driver-580-open 등 설치되어 있으면 ✅

# 4. DKMS 모듈 빌드 상태 확인 (핵심)
sudo dkms status | grep nvidia
# → "nvidia/580.126.09, 6.8.0-xxx-generic, x86_64: installed" ← 이렇게 출력되어야 정상
# → 출력 없음 → nvidia-dkms-580-open 미설치 ❌

# 5. 커널 모듈 파일 존재 확인
ls -la /lib/modules/$(uname -r)/updates/dkms/nvidia*
# → nvidia.ko 파일이 존재해야 정상

# 6. Nouveau 드라이버 사용 중인지 확인
lsmod | grep nouveau
# → 출력 없음 = Nouveau 비활성화 상태 ✅
# → 출력 있음 = Nouveau 활성화 → 비활성화 필요
```

> ⚠️ **`nvidia-smi` 실패 + `dkms status` 출력 없음** = `nvidia-dkms-580-open` 누락.
> `nvidia-driver-580-open` 메타패키지가 자동으로 포함시키지 못한 경우입니다.
> 해결: `sudo apt install nvidia-dkms-580-open` 실행 후 [3.4 DKMS 빌드](#34-dkms-빌드-확인)로 이동하세요.

### 3.1 Nouveau 비활성화

```bash
sudo nano /etc/modprobe.d/blacklist-nouveau.conf
```

다음 내용 입력:
```
blacklist nouveau
options nouveau modeset=0
```

```bash
sudo update-initramfs -u
```

### 3.2 이전 NVIDIA 드라이버 제거

```bash
sudo apt purge nvidia-* libnvidia-* -y
sudo apt autoremove -y
sudo apt autoclean
```

### 3.3 드라이버 설치 (방식 선택)

#### 방식 A: PPA를 통한 설치 (권장)

```bash
# graphics-drivers PPA 추가
sudo add-apt-repository -y ppa:graphics-drivers/ppa
sudo apt update

# 권장 드라이버 확인
ubuntu-drivers devices
# → RTX 5090 권장: nvidia-driver-580-open 또는 nvidia-driver-570-open

# ⚠️ nvidia-driver-580-open 설치 시 nvidia-dkms-580-open이
#    자동으로 함께 설치되어야 정상입니다. 설치 후 반드시 확인!
sudo apt install -y nvidia-driver-580-open

# Prime 설정 (노트북의 경우)
sudo prime-select nvidia
```

> **설치 후 DKMS 확인**: `sudo dkms status | grep nvidia` 실행
> - `nvidia/580.126.09, 6.8.0-xxx-generic, x86_64: installed` → 정상 ✅
> - **출력 없음** → DKMS 패키지 누락 → 아래 추가 조치 실행:

```bash
# DKMS 패키지가 누락된 경우 수동 설치
sudo apt install -y nvidia-dkms-580-open

# DKMS 빌드가 완료될 때까지 대기 (2~5분 소요)
sudo dkms status | grep nvidia
# → "installed" 확인 후 initramfs 업데이트
sudo update-initramfs -u
```

#### 방식 B: NVIDIA 공식 .run 파일 설치

Blackwell GPU는 최신 드라이버 필요. NVIDIA 공식 사이트에서 최신 Linux x86_64 드라이버 다운로드:

```bash
# 최신 드라이버 다운로드 (버전은 580 이상)
wget https://us.download.nvidia.com/XFree86/Linux-x86_64/580.65.06/NVIDIA-Linux-x86_64-580.65.06.run

# 실행 권한 부여 및 설치
chmod +x NVIDIA-Linux-x86_64-580.65.06.run
sudo ./NVIDIA-Linux-x86_64-580.65.06.run \
    --silent \
    --dkms \
    --install-libglvnd \
    --no-x-check \
    --no-nouveau-check \
    --no-opengl-files \
    --accept-license \
    --run-nvidia-xconfig
```

### 3.4 설치 확인 (재부팅 후)

> **⚠️ 재부팅 전 필수 확인**: DKMS 모듈이 커널과 함께 빌드되었는지 반드시 확인하세요.
> 드라이버 패키지는 설치됐어도 DKMS 모듈이 없으면 `nvidia-smi`가 실패합니다.
> ```bash
> sudo dkms status | grep nvidia
> # → "nvidia/580.xxx.xx, 6.8.0-xxx-generic, x86_64: installed" ← installed 확인 필수!
> # → 출력이 없거나 "built"가 아닌 경우 → 재부팅하지 말고 먼저 DKMS 패키지 설치
> ```
>
> DKMS 누락 시: `sudo apt install nvidia-dkms-580-open` → `sudo dkms status` 재확인 → `sudo update-initramfs -u` → 재부팅

```bash
# 0. DKMS 모듈 빌드 확인 (드라이버 로드의 전제 조건)
sudo dkms status | grep nvidia
# → nvidia/580.159.04, 6.8.0-111-generic, x86_64: installed (installed 확인 필수!)

# 1. 커널 모듈 로드 확인
lsmod | grep nvidia
# → nvidia, nvidia-modeset, nvidia-uvm 등이 출력되어야 정상

# 2. 드라이버 확인
nvidia-smi
```

정상 출력 예시 (RTX 5090, ASUS ROG Strix SCAR 16 G635LX 실제 출력):
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.159.04             Driver Version: 580.159.04     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5090 ...    Off |   00000000:02:00.0 Off |                  N/A |
| N/A   57C    P4             33W /   95W |       0MiB /  24463MiB |      2%      Default |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

### 3.5 실제 설치 사례 및 트러블슈팅 (ASUS ROG Strix SCAR 16 G635LX + RTX 5090)

> 실제 설치 과정에서 발생한 문제와 해결 방법을 기록합니다.

#### 문제 상황

Ubuntu 22.04.5 LTS (kernel 6.8.0-111-generic)에서 RTX 5090 드라이버 설치 시 다음과 같은 문제가 발생했습니다:

1. **`nvidia-smi` 명령 실행 실패** — `NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver.`
2. **원인: `nvidia-dkms-580-open` 패키지 누락**
   - `nvidia-driver-580-open` 메타패키지가 설치되었으나, DKMS 커널 모듈이 자동으로 빌드되지 않음
   - `sudo dkms status | grep nvidia` → 출력 없음 (빈 상태)

#### 추가 문제: 패키지 버전 충돌 (PPA vs Ubuntu 공식 저장소)

| 패키지 | 저장소 | 버전 |
|--------|--------|------|
| `nvidia-driver-580-open` | Ubuntu 공식 저장소 | 580.126.09 |
| `nvidia-driver-580-open` | graphics-drivers PPA | 580.159.04 |
| `nvidia-dkms-580-open` | **설치되지 않음** ❌ | — |

- `nvidia-driver-580-open`은 Ubuntu 저장소의 580.126.09가 먼저 설치됨
- 이후 PPA 추가 시 580.159.04와 충돌 발생
- `nvidia-dkms-580-open`가 함께 설치되지 않아 커널 모듈 누락

#### 최종 해결 명령어

```bash
# 1. 패키지 충돌 해결
sudo apt --fix-broken install -y

# 2. 드라이버 + DKMS + 유틸리티 통합 설치
sudo apt install -y nvidia-driver-580-open nvidia-dkms-580-open nvidia-utils-580

# 3. DKMS 빌드 확인 (installed 출력 필수)
sudo dkms status | grep nvidia

# 4. initramfs 업데이트
sudo update-initramfs -u

# 5. 재부팅
sudo reboot

# 6. 최종 확인
nvidia-smi
```

#### 교훈

- RTX 5090 (Blackwell)은 반드시 **오픈 커널 모듈 드라이버 (`nvidia-driver-5xx-open`)** 가 필요합니다.
- **DKMS 상태 확인 (`sudo dkms status | grep nvidia`)** 이 드라이버 설치 성공 여부의 핵심 지표입니다.
  - `nvidia-smi`가 실패하는 가장 흔한 원인: 패키지는 설치됐지만 DKMS 모듈이 없는 경우
- PPA 사용 시 기존 Ubuntu 저장소 패키지와의 **버전 충돌**이 발생할 수 있습니다.
  - 해결: `apt --fix-broken install`로 정리 후 원하는 버전으로 통일 설치

---

## 4. 기본 개발 도구 설치

### 4.0 설치 전 확인

> **✅ 본 장비(ASUS ROG Strix SCAR 16)에서 모두 설치 및 확인 완료**

```bash
# 각 도구별 설치 여부 확인
which gcc g++ cmake git wget curl python3 pip3 unzip make
# 정상 출력 예시 (실제 검증 완료):
#   /usr/bin/gcc
#   /usr/bin/g++
#   /usr/bin/cmake
#   /usr/bin/git
#   /usr/bin/wget
#   /usr/bin/curl
#   /home/gotree94/miniconda3/bin/python3  ← conda 환경
#   /home/gotree94/miniconda3/bin/pip3       ← conda 환경
#   /usr/bin/unzip
#   /usr/bin/make

# GCC 버전 확인 (Isaac Sim 호환)
gcc --version | head -1
# → gcc (Ubuntu 11.4.0-1ubuntu1~22.04.3) 11.4.0 (Isaac Sim 권장 버전)

# Python 버전 확인
python3 --version
# → Python 3.13.2 (miniconda3)
```

> **모두 설치되어 있다면** 이 섹션을 건너뛰어도 됩니다.
>
> **GCC 버전 관련 중요 공지**:
> - Isaac Sim 공식 문서는 **GCC/G++ 11**을 요구하며, **12 이상은 지원되지 않음**을 명시하고 있습니다.
> - Ubuntu 22.04 기본 GCC 11.4.0을 그대로 사용하세요. 상위 버전으로 변경할 필요가 없습니다.
> - GCC 14 설치는 불필요하며, Isaac Sim 호환성 문제가 발생할 수 있습니다.
>
> **Python (miniconda3) 관련 참고**:
> - `python3`/`pip3`가 miniconda3 경로를 가리키는 경우, ROS 2 Humble (Python 3.10 기반)과 conda Python (3.13) 간 버전 불일치가 발생할 수 있습니다.
> - ROS 2 설치/빌드 시 `conda deactivate`로 conda 환경을 비활성화하고 진행하는 것을 권장합니다.
> - Isaac Sim은 자체 내장 Python을 사용하므로 시스템 Python과 무관합니다.

### 4.1 설치

> ⏭️ **본 장비는 이미 모든 기본 도구가 설치 완료된 상태**이므로 이 섹션은 건너뛰어도 됩니다.
> 아래 명령어는 참고용으로만 제공합니다.

```bash
# UTF-8 로케일 설정
locale
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 기본 빌드 도구
sudo apt update && sudo apt install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    gnupg \
    software-properties-common \
    python3-pip \
    python3-venv \
    pkg-config \
    unzip \
    net-tools

# GCC는 Ubuntu 22.04 기본 버전(11.4.0) 사용
# Isaac Sim은 GCC 11만 지원, 12+ 미지원
gcc --version
```

---

## 5. ROS 2 Humble 설치

> 본 DLI 과정은 **ROS 2 Humble**을 사용합니다. (Ubuntu 22.04 전용)

> **✅ 본 장비(ASUS ROG Strix SCAR 16)에서 ROS 2 Humble 저장소 등록 완료, ros-humble-desktop 포함 다수 패키지 설치 확인 완료**

### 5.0 설치 전 확인

```bash
# 1. ROS 2가 이미 설치되어 있는지 확인
echo $ROS_DISTRO
# → "humble" 출력 → ✅ 이미 ROS 2 Humble 환경이 source되어 있음
# → 빈 문자열 출력 → 미설치 또는 source 안 됨

# 2. ROS 2 Humble 패키지 설치 확인
dpkg -l | grep ros-humble-desktop | head -3
# → "ros-humble-desktop" 라인이 보이면 ✅ 설치됨

# 3. ROS 2 명령어 실행 테스트
ros2 --help
# → 도움말 출력 → 정상
# → "command not found" → 설치 필요 ❌

# 4. apt 저장소 목록에서 ROS 2 확인
ls /etc/apt/sources.list.d/ros2.list 2>/dev/null && echo "✅ ROS 2 저장소 등록됨" || echo "❌ 저장소 없음"
```

> **ROS 2 Humble이 이미 설치되어 있다면** 아래 저장소 등록 및 설치 과정을 건너뛰고, [5.4 설정](#54-ros-2-환경-설정-bashrc-등록)에서 `.bashrc`만 확인하세요.

### 5.1 ROS 2 저장소 등록

> ⏭️ **본 장비는 ROS 2 저장소가 이미 등록되어 있음** (`/etc/apt/sources.list.d/ros2.list` 존재, `apt update` 시 `packages.ros.org` Hit 확인됨)

```bash
# ROS 2 GPG 키 추가
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 저장소 등록
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
```

### 5.2 ROS 2 Humble Desktop 설치

> ⏭️ **본 장비는 `ros-humble-desktop`이 이미 설치되어 있음** (`apt install` 시 `already the newest version` 확인됨)

```bash
# 전체 데스크탑 설치 (권장)
sudo apt install -y \
    ros-humble-desktop \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    python3-argcomplete

# rosdep 초기화
sudo rosdep init
rosdep update
```

### 5.3 추가 ROS 패키지 설치 (DLI 과정 필수)

> **✅ 본 장비에서 모두 설치 완료** (MoveIt 2.5.9, TF, rviz2 등)
> 아래는 참고용 명령어입니다.

```bash
# vision_msgs (바운딩 박스 시각화)
sudo apt install -y ros-humble-vision-msgs

# ackermann_msgs (조향 명령)
sudo apt install -y ros-humble-ackermann-msgs

# Nav2 패키지
sudo apt install -y \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-nav2-msgs

# MoveIt2 패키지
# ⚠️ 패키지명은 ros-humble-moveit (ros-humble-moveit2가 아님)
sudo apt install -y \
    ros-humble-moveit \
    ros-humble-moveit-msgs \
    ros-humble-moveit-visual-tools

# TF, URDF 관련
# (대부분 ros-humble-desktop에 포함되어 이미 설치됨)
sudo apt install -y \
    ros-humble-robot-state-publisher \
    ros-humble-joint-state-publisher \
    ros-humble-xacro \
    ros-humble-tf2 \
    ros-humble-tf2-ros \
    ros-humble-tf2-msgs

# 유틸리티
sudo apt install -y \
    ros-humble-rviz2 \
    ros-humble-topic-tools \
    ros-humble-teleop-twist-keyboard
```

### 5.4 ROS 2 환경 설정 (.bashrc 등록)

```bash
echo "" >> ~/.bashrc
echo "# ROS 2 Humble 설정" >> ~/.bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=0" >> ~/.bashrc
echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp" >> ~/.bashrc

source ~/.bashrc
```

### 5.5 ROS 2 설치 확인

```bash
# 새 터미널에서
printenv ROS_DISTRO
# → humble 출력 확인

# 토픽 명령어 테스트
ros2 topic list
# → 빈 리스트 출력 (정상)
```

---

## 6. Isaac Sim 설치

> Isaac Sim은 NVIDIA Omniverse 기반 로봇 시뮬레이션 플랫폼입니다. 약 30GB의 저장 공간이 필요합니다.
> **본 DLI 과정에서는 Isaac Lab이 필요하지 않습니다.** Isaac Sim Standalone만 설치하면 됩니다.

### 6.0 설치 전 확인

> **✅ 본 장비(ASUS ROG Strix SCAR 16) 확인 완료 — Isaac Sim 미설치 상태, 설치 필요**

```bash
# 1. Isaac Sim이 이미 설치되어 있는지 확인
ls ~/isaacsim/isaac-sim.sh
# → 파일이 존재하면 ✅ Isaac Sim 설치됨
# → "No such file or directory" → 설치 필요 ❌ (본 장비: 미설치)

# 2. NVIDIA 드라이버 (Isaac Sim 실행 전제 조건)
nvidia-smi
# → RTX 5090 + Driver Version 580+ 확인 (본 장비: 580.159.04 ✅)

# 3. Python 버전 확인 (Isaac Sim 내장 Python 사용)
python3 --version
# → 3.10 이상 (Isaac Sim 5.0은 3.11 내장) (본 장비: Python 3.13.2, conda)
# ⚠️ Isaac Sim은 자체 내장 Python을 사용하므로 시스템 Python 버전과 무관
```

> **Isaac Sim이 이미 설치되어 있다면** [6.6 설치 확인](#66-설치-확인) 및 [ROS 2 브리지 설정](#67-ros-2-브리지-설정)만 진행하세요.

### 6.1 사전 확인

> **✅ 본 장비 확인 완료** — 아래는 실제 출력값

```bash
# NVIDIA 드라이버 확인
nvidia-smi
# → RTX 5090, Driver 580.159.04, CUDA 13.0 (드라이버 내장) ✅

# Python 버전 확인 (Isaac Sim 내장 Python과 무관)
python3 --version
# → Python 3.13.2 (miniconda3) — Isaac Sim은 자체 Python 사용

# CUDA Toolkit 설치 확인 (nvcc)
nvcc --version
# → nvcc: CUDA 12.4.131 — 드라이버 CUDA 13.0과 별도 설치
#   Isaac Sim은 시스템 nvcc가 아닌 드라이버 내장 CUDA 사용
#
# ※ nvcc 없는 경우: "nvcc 없음 - 드라이버 내장 CUDA 사용" 출력
#   Isaac Sim 실행에는 nvcc가 필수가 아님 (드라이버만 있으면 됨)
```

### 6.2 시스템 의존성 설치

```bash
sudo apt install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libegl1 \
    libxi6 \
    libxkbcommon0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb-xv0 \
    libxrandr2
```

### 6.4 Isaac Sim 다운로드 및 설치

```bash
# 설치 디렉토리 생성
mkdir -p ~/isaacsim
cd ~/Downloads

# Isaac Sim Standalone 5.1.0 직접 다운로드 (NVIDIA 공식):
wget https://downloads.isaacsim.nvidia.com/isaac-sim-standalone-5.1.0-linux-x86_64.zip
#
# ※ 브라우저 다운로드가 더 안정적이면 아래 URL 사용:
#   https://downloads.isaacsim.nvidia.com/isaac-sim-standalone-5.1.0-linux-x86_64.zip
#
# 주의: 약 30GB, 로그인 불필요 (NVIDIA 공개 배포)
# DLI 코스는 4.5 기준이나 5.1.0에서도 정상 작동 확인됨

# 압축 해제
unzip "isaac-sim-standalone-5.1.0-linux-x86_64.zip" -d ~/isaacsim
# (또는) tar 파일인 경우:
# tar -xvf "isaac-sim-standalone-5.1.0-linux-x86_64.tar.gz" -C ~/isaacsim

cd ~/isaacsim

# 사후 설치 스크립트 실행
./post_install.sh

# Isaac Sim 실행 테스트
./isaac-sim.sh
```

### 6.5 Isaac Sim + ROS 2 브리지 설정

#### 방식 A: ROS 2 Native 환경 사용 (권장)

Ubuntu 22.04에서 ROS 2 Humble이 native 설치된 경우, Isaac Sim이 자동으로 ROS 2 브리지를 로드합니다:

```bash
# 1. ROS 2 소싱 (bashrc에 등록되어 있어야 함)
source ~/.bashrc

# 2. ROS_DISTRO 확인
echo $ROS_DISTRO  # → humble

# 3. 같은 터미널에서 Isaac Sim 실행
cd ~/isaacsim
./isaac-sim.sh
```

#### 방식 B: Internal ROS 2 라이브러리 사용

시스템에 ROS 2가 없거나 다른 설정이 필요할 경우:

```bash
export isaac_sim_package_path=$HOME/isaacsim
export ROS_DISTRO=humble
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$isaac_sim_package_path/exts/isaacsim.ros2.bridge/humble/lib

$isaac_sim_package_path/isaac-sim.sh
```

### 6.6 설치 확인 (Isaac Sim 호환성 체커)

```bash
# 호환성 체커 다운로드 및 실행
# https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html

cd ~/Downloads
# 다운로드 후 압축 해제
unzip "isaac-sim-compatibility-checker-5.1.0-linux-x86_64.zip"
cd isaac-sim-compatibility-checker
./omni.isaac.sim.compatibility_check.sh
```

---

## 7. ROS 2 Workspace 빌드

DLI 과정에서 제공하는 `gtc25-mega1` ROS 작업 공간을 빌드합니다.

### 7.0 빌드 전 확인

> **✅ 본 장비에서 빌드 완료** — 5개 패키지(colcon build) 성공
> **⚠️ 중요: conda 환경에서는 빌드가 실패합니다.** 아래 확인 및 조치 필수

```bash
# 0. (중요) conda 환경 비활성화 — conda Python이 ROS 빌드와 충돌
conda deactivate
which python3
# → /usr/bin/python3 (system python) 이어야 함
# → /home/.../miniconda3/bin/python3 이면 conda 환경 활성화 상태 ❌

# 1. ROS Workspace 디렉토리 존재 확인
ls ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/src/
# → carter_navigation, isaac_moveit 등 패키지 디렉토리가 보여야 함
#   (본 장비: manipulation/, navigation/)

# 2. 이전 빌드 결과 확인 (이미 빌드된 경우)
ls ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash
# → 파일이 존재하면 ✅ 이미 빌드 완료

# 3. ROS 2 환경 확인
echo $ROS_DISTRO
# → "humble" 출력 확인

# 4. 필수 Python 패키지 확인 (conda 비활성화 상태에서)
python3 -c "import catkin_pkg" 2>/dev/null && echo "✅ catkin_pkg 있음" || echo "❌ sudo apt install python3-catkin-pkg 필요"
```

> **이미 빌드되어 있다면** [7.3 설정](#73-bashrc에-workspace-등록)에서 `.bashrc` 등록만 확인하세요.  
> **참고**: `IsaacSim-ros_workspaces` 클론(7.1)은 공식 튜토리얼용으로, **본 DLI 과정에는 필요하지 않습니다.** DLI 과정은 자체 `ros_ws`를 사용합니다.

### 7.1 (참고) Isaac Sim ROS Workspace 클론

공식 Isaac Sim ROS 작업 공간(선택사항, 과정에 필요 시):

```bash
cd ~
git clone https://github.com/isaac-sim/IsaacSim-ros_workspaces.git
cd IsaacSim-ros_workspaces
```

### 7.3 DLI 과정 ROS Workspace 빌드

코스 에셋 내의 `ros_ws` 작업 공간 활용:

```bash
# ★ 중요: conda 환경 비활성화 (ROS 빌드는 system Python 필요)
conda deactivate
which python3
# → /usr/bin/python3 확인

# ★ 중요: catkin_pkg 모듈 설치 (conda 환경에 없음)
sudo apt install -y python3-catkin-pkg

cd ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws

# 이전 빌드 캐시가 있으면 제거 (conda 경로가 캐싱된 경우)
rm -rf build/ install/ log/

# 의존성 설치
rosdep install --from-paths src --ignore-src -r -y

# colcon 빌드
colcon build

# 빌드 확인
source install/setup.bash
echo "ROS 2 Workspace 빌드 완료"
```

> **참고**: `colcon build`는 소스 패키지 수에 따라 5~15분 소요. `--symlink-install` 옵션 사용 시 개발 중 변경 사항이 자동 반영됩니다.
>
> **⚠️ conda 환경 주의**: build/ 디렉토리에 conda python3 경로가 캐싱될 수 있습니다. `conda deactivate` 후 `rm -rf build/`로 캐시를 완전히 제거해야 합니다.

### 7.4 `.bashrc`에 Workspace 등록

```bash
echo "source ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 8. DLI 코스 에셋 다운로드

### 8.0 다운로드 전 확인

```bash
# 이미 에셋이 있는지 확인
ls ~/Desktop/DLI_SIL/Starting_point/
# → nova_carter/, franka/, warehouse_env/, gtc25-mega1/ 등이 보이면 ✅ 이미 다운로드 완료

# zip 파일 존재 확인
ls ~/Desktop/DLI_SIL_online_dli.zip 2>/dev/null && echo "✅ zip 존재" || echo "❌ zip 없음"
```

> **이미 압축 해제까지 완료되었다면** 이 섹션을 건너뛰세요.

### 8.1 에셋 다운로드

```bash
# 코스 자료 다운로드
cd ~/Desktop
wget https://download.learn.nvidia.com/assets/s-ov-39-v1/DLI_SIL_online_dli.zip

# 압축 해제
unzip DLI_SIL_online_dli.zip -d ~/Desktop/DLI_SIL

# 디렉토리 구조 확인
ls -la ~/Desktop/DLI_SIL/
```

### 8.2 디렉토리 구조

```
~/Desktop/DLI_SIL/
├── Starting_point/
│   ├── nova_carter/
│   │   └── nova_carter.usd
│   ├── franka/
│   │   └── franka.usd
│   ├── warehouse_env/
│   │   └── warehouse_env.usd
│   ├── owl/
│   │   └── (Owl USD 파일)
│   ├── checkpoint1_nova_carter/
│   ├── checkpoint2_franka/
│   ├── checkpoint3/
│   ├── checkpoint4_completed_environment/
│   ├── checkpoint5_completed_ros_package/
│   └── gtc25-mega1/
│       └── ros_ws/
│           └── src/
│               ├── navigation/
│               │   └── carter_navigation/
│               │       └── maps/
│               └── isaac_moveit/
└── dli_img/
    ├── image1.png
    ├── image2.png
    └── ...
```

---

## 9. 모듈별 실행 요약

### 9.1 Module 1: Isaac Sim + ROS 2 실행

```bash
# 터미널 1: Isaac Sim 실행
source ~/.bashrc
cd ~/isaacsim
./isaac-sim.sh
```

### 9.2 Module 2: Nova Carter ROS Graphs

Isaac Sim GUI 내 작업:
1. **File > Open** → `~/Desktop/DLI_SIL/Starting_point/nova_carter/nova_carter.usd`
2. **Tools > Robotics > ROS 2 OmniGraphs > RTX Lidar** → 라이다 그래프 생성
3. **Tools > Robotics > ROS 2 Omnigraph Odometry Publisher** → Odometry 생성

### 9.3 Module 3: 추가 ROS 기능

```bash
# Joint States 확인
ros2 topic list
# → /joint_states 확인
```

### 9.4 Module 4: Franka 로봇 구성

Isaac Sim에서 `~/Desktop/DLI_SIL/Starting_point/franka/franka.usd` 열기.

### 9.5 Module 5: 점유 맵 생성

Isaac Sim에서 `~/Desktop/DLI_SIL/Starting_point/warehouse_env/warehouse_env.usd` 열기.

### 9.6 Module 6: 통합 환경

두 로봇 동시 로드. Clock 그래프 생성.

### 9.7 Module 7: ROS Workspace

```bash
cd ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws
colcon build
source install/setup.bash
```

### 9.8 Module 8: Nav2 자율 주행

```bash
# 터미널 1: Isaac Sim (Play 상태)
# 터미널 2: TF Publisher
source ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash
ros2 launch carter_navigation nova_carter_description_isaac_sim.launch.py

# 터미널 3: /tf_static 중계
source ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash
ros2 run topic_tools relay /tf_static /carter/tf_static

# 터미널 4: Nav2 실행
source ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash
ros2 launch carter_navigation carter_warehouse_env.launch.py
```

### 9.9 Module 9: MoveIt2 조작

```bash
# 새 터미널에서
source ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash
ros2 launch isaac_moveit isaac_moveit.launch.py
```

---

## 10. 문제 해결

### 10.1 RTX 5090 드라이버 관련

| 문제 | 해결 방법 |
|------|----------|
| `nvidia-smi` 실행 안 됨 | `sudo apt purge nvidia-*` → `sudo apt install nvidia-driver-580-open` 후 재부팅 |
| `nvidia-smi` 실패 + 패키지는 설치됨 | **DKMS 모듈 누락**. `sudo apt install nvidia-dkms-580-open` → `sudo dkms status`로 `installed` 확인 → `sudo update-initramfs -u` → 재부팅 |
| `nvidia-smi` 실패 + DKMS도 없음 | 메타패키지가 DKMS를 자동 포함하지 못한 경우. `sudo apt install -y nvidia-driver-580-open nvidia-dkms-580-open nvidia-utils-580`로 통합 설치 |
| 패키지 버전 충돌 (PPA vs Ubuntu 저장소) | `sudo apt --fix-broken install -y`로 충돌 해결 후 원하는 버전으로 통일 설치 |
| 블랙 스크린 부팅 | GRUB에서 `nomodeset` 또는 `nouveau.modeset=0` 추가 |
| GPU 인식 안 됨 | BIOS 설정 확인: Secure Boot **비활성화**, UEFI 설정 확인 |
| `Failed to initialize NVML: Driver/library version mismatch` | 재부팅 후 재시도 |
| `update-alternatives: error: no alternatives for gcc` | 이미 GCC 11이 기본인 상태. `update-alternatives` 설정은 불필요. `gcc --version`으로 11.4.0 확인 후 무시 |

### 10.2 Isaac Sim 관련

| 문제 | 해결 방법 |
|------|----------|
| Isaac Sim 실행 안 됨 | `./isaac-sim.sh --help`로 옵션 확인, GPU 드라이버 버전 확인 |
| ROS 2 브리지 미연결 | 같은 터미널에서 ROS 2 source 후 Isaac Sim 실행 |
| 그래픽 깜빡임 | NVIDIA 드라이버 재설치, `--no-gui` 모드 테스트 |
| 메모리 부족 오류 | `ulimit -n 1048576` 실행 (파일 디스크립터 제한 증가) |
| Python 버전 충돌 | Isaac Sim 내장 Python 사용 (시스템 Python과 별개) |

### 10.3 ROS 2 관련

| 문제 | 해결 방법 |
|------|----------|
| `ROS_DISTRO not set` | `source /opt/ros/humble/setup.bash` 실행 |
| `colcon: command not found` | `sudo apt install python3-colcon-common-extensions` |
| 패키지를 찾을 수 없음 | `source install/setup.bash` 실행 확인 |
| `rosdep: command not found` | `sudo apt install python3-rosdep` |
| RMW冲突 | `export RMW_IMPLEMENTATION=rmw_fastrtps_cpp` 통일 |

### 10.4 Intel Core Ultra 9 (Arrow Lake) 관련

| 문제 | 해결 방법 |
|------|----------|
| 랜덤 컴파일러 에러 | DDR5 메모리 안정성 → BIOS 업데이트, XMP 프로파일 비활성화 후 테스트 |
| P-State 드라이버 문제 | 커널 6.8+ HWE 또는 최신 mainline 커널 사용 |
| Arrow Lake 최적화 | 가능하면 Ubuntu 24.04 LTS 사용 권장 (더 나은 커널/드라이버 지원) |

### 10.5 일반적인 문제

| 문제 | 해결 방법 |
|------|----------|
| `Failed to load module "canberra-gtk-module"` | `sudo apt install libcanberra-gtk3-module` |
| USB 권한 문제 | `sudo usermod -aG dialout $USER` 후 재로그인 |
| 디스크 공간 부족 | Isaac Sim ~30GB, ROS 2 ~5GB, DLI 에셋 ~2GB 필요 |
| 스왑 공간 부족 | 64GB RAM이면 보통 충분하나, 빌드 시 8GB 스왑 권장 |

### 10.6 Parsec (원격 데스크톱) 설치

> **🔄 중요 변경사항**: Parsec이 Linux 설치 방식을 **Snap으로 전환**하면서 기존 `.deb` 설치 스크립트(`https://parsec.app/install/parsec.sh`)가 **삭제**되었습니다.
> 아래 명령어는 **404 HTML 페이지를 반환**하므로 사용하지 마세요:
> ```bash
> curl -sSL https://parsec.app/install/parsec.sh | sudo bash   # ❌ 404 Error
> ```

| 문제 | 원인 | 해결 방법 |
|------|------|----------|
| `curl .../parsec.sh \| sudo bash` 실행 시 bash 문법 오류 (`<!DOCTYPE html>`) | Parsec 공식 설치 스크립트 URL이 **404 HTML 페이지 반환** | Snap으로 설치 (`sudo snap install parsec --classic`) |
| `sudo systemctl start parsec` → `Unit parsec.service not found` | Snap 설치 방식은 systemd service를 직접 생성하지 않음 | Snap 설치 완료 후 `snap run parsec` 또는 앱 런처에서 실행 |
| **Snap 설치 방법 (권장)** | Ubuntu 22.04에는 Snap이 기본 포함 | ```bash
# Parsec Snap 설치 (classic 모드: Fuse 마운트 권한 필요)
sudo snap install parsec --classic

# 실행
snap run parsec   # 또는 앱 런처에서 Parsec 실행

# 업데이트
sudo snap refresh parsec
``` |
| **`.deb` 직접 다운로드 (대체 방법)** | Parsec 공식 사이트에서 .deb 제공 | ```bash
# 1. https://parsec.app/downloads → Linux (Ubuntu 22.04 LTS Desktop) 선택 → .deb 다운로드

# 2. 설치
sudo apt install ./parsec-*.deb

# 3. libssl1.1 의존성 문제 발생 시 (Ubuntu 22.04):
echo "deb http://old-releases.ubuntu.com/ubuntu impish-security main" | sudo tee /etc/apt/sources.list.d/impish-security.list
sudo apt update
sudo apt install libssl1.1
sudo rm /etc/apt/sources.list.d/impish-security.list
``` |
| **Flatpak 설치 (비공식)** | 공식 지원 아님, 커뮤니티 래퍼 | ```bash
# Flathub에서 설치 (비공식 래퍼)
flatpak install flathub com.parsecgaming.parsec
flatpak run com.parsecgaming.parsec
``` |
| **Linux은 Hosting 미지원** | Parsec Linux 클라이언트는 **다른 기기로의 연결 전용** | Linux에서는 **Windows/macOS 기기에 연결**만 가능. Linux 머신 호스팅은 지원하지 않음 |

> **💡 본 장비 사용 시나리오**: Windows 11 듀얼 부팅 환경이 있으므로, Parsec을 Ubuntu에 설치하여 **Windows 환경에 원격 접속**하는 용도로 사용하세요. Linux → Windows 연결은 정상 작동합니다.

---



## 11. 참고 자료

### 11.1 공식 문서

| 자료 | 링크 |
|------|------|
| Isaac Sim 요구사항 | [https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) |
| Isaac Sim 설치 가이드 | [https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_workstation.html](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_workstation.html) |
| Isaac Sim + ROS 2 | [https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html) |
| ROS 2 Humble 설치 | [https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html) |
| NVIDIA 드라이버 다운로드 | [https://www.nvidia.com/en-us/drivers/](https://www.nvidia.com/en-us/drivers/) |
| Isaac Sim 호환성 체커 | [https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html) |
| Parsec Snap 설치 가이드 | [https://snapcraft.io/parsec](https://snapcraft.io/parsec) |
| Parsec Linux 설치 공식 문서 | [https://support.parsec.app/hc/en-us/articles/4422904998413](https://support.parsec.app/hc/en-us/articles/4422904998413) |
| Parsec 다운로드 페이지 | [https://parsec.app/downloads](https://parsec.app/downloads) |

### 11.2 도움말 및 커뮤니티

| 자료 | 링크 |
|------|------|
| NVIDIA Isaac Sim 포럼 | [https://forums.developer.nvidia.com/c/accelerated-computing/isaac/](https://forums.developer.nvidia.com/c/accelerated-computing/isaac/) |
| ROS 2 커뮤니티 | [https://discourse.ros.org/](https://discourse.ros.org/) |
| DLI 코스 페이지 | [https://learn.nvidia.com/courses/course?course_id=course-v1:DLI+S-OV-39+V1](https://learn.nvidia.com/courses/course?course_id=course-v1:DLI+S-OV-39+V1) |

### 11.3 빠른 설치 명령어 요약 (확인 → 설치 → 검증)

```bash
# ===== 1. 시스템 확인 (Ubuntu 22.04.5 LTS) =====
uname -r                    # → 6.8.x 이상 확인
nvidia-smi                  # → 이미 설치되어 있으면 2번 skip
echo $ROS_DISTRO            # → "humble"이면 4번 skip

# ===== 2. NVIDIA 드라이버 설치 (RTX 5090) =====
#   설치 전 확인: nvidia-smi  /  sudo dkms status | grep nvidia
#   ⚠️ 버전 충돌 시: sudo apt --fix-broken install -y
sudo add-apt-repository -y ppa:graphics-drivers/ppa
sudo apt update

# ★ nvidia-dkms-580-open을 명시적으로 포함 (누락 방지)
sudo apt install -y nvidia-driver-580-open nvidia-dkms-580-open nvidia-utils-580

# ⚠️ 반드시 DKMS 모듈이 빌드되었는지 확인 (가장 중요!)
sudo dkms status | grep nvidia
# → "nvidia/..., installed" 출력 없으면 위 설치 실패 → 재시도
# → 정상 출력: "nvidia/580.159.04, 6.8.0-111-generic, x86_64: installed"

sudo update-initramfs -u
sudo reboot
nvidia-smi                  # 검증: RTX 5090 인식 확인

# ===== 3. 기본 도구 설치 =====
#   설치 전 확인: which gcc cmake git python3
sudo apt install -y build-essential cmake git wget curl unzip \
    python3-pip python3-venv software-properties-common

# ===== 4. ROS 2 Humble 설치 =====
#   설치 전 확인: dpkg -l | grep ros-humble-desktop
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
    -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list
sudo apt update
sudo apt install -y ros-humble-desktop python3-colcon-common-extensions python3-rosdep
sudo rosdep init && rosdep update
sudo apt install -y ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-moveit \
    ros-humble-robot-state-publisher ros-humble-joint-state-publisher \
    ros-humble-rviz2 ros-humble-topic-tools
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
# 검증: echo $ROS_DISTRO → humble

# ===== 5. Isaac Sim 설치 (Isaac Lab 불필요) =====
#   설치 전 확인: ls ~/isaacsim/isaac-sim.sh
# 직접 다운로드 (NVIDIA 공식):
#   wget https://downloads.isaacsim.nvidia.com/isaac-sim-standalone-5.1.0-linux-x86_64.zip
# (약 30GB, 브라우저 다운로드 권장)
mkdir -p ~/isaacsim
cd ~/Downloads
unzip isaac-sim-standalone-5.1.0-linux-x86_64.zip -d ~/isaacsim
cd ~/isaacsim && ./post_install.sh
# 검증: ./isaac-sim.sh  (GUI 실행 테스트)

# ===== 6. DLI 코스 에셋 다운로드 =====
#   설치 전 확인: ls ~/Desktop/DLI_SIL/
cd ~/Desktop
wget https://download.learn.nvidia.com/assets/s-ov-39-v1/DLI_SIL_online_dli.zip
unzip DLI_SIL_online_dli.zip -d ~/Desktop/DLI_SIL

# ===== 7. ROS Workspace 빌드 =====
#   설치 전 확인: ls ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash
#   ★ conda 사용 시: conda deactivate && sudo apt install python3-catkin-pkg
cd ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws
rm -rf build/ install/ log/    # conda 경로 캐시 제거
rosdep install --from-paths src --ignore-src -r -y
colcon build
echo "source ~/Desktop/DLI_SIL/Starting_point/gtc25-mega1/ros_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc

# ===== 8. (선택) Parsec 원격 데스크톱 설치 =====
#   ⚠️ 구 스크립트(curl .../parsec.sh | sudo bash)는 404 Error → Snap 사용
#   Parsec Linux는 Windows/macOS 연결 전용 (Linux 호스팅 불가)
sudo snap install parsec --classic
snap run parsec           # 검증: GUI 실행 확인
# 또는 앱 런처에서 Parsec 실행

echo "✅ 모든 설치 완료!"
```

---

> **최종 검증 체크리스트**
>
> ### ✅ [OS] Ubuntu 22.04.5 LTS
> - [ ] `cat /etc/os-release` → Ubuntu 22.04.5 LTS
> - [ ] `uname -r` → 6.8.x 이상
>
> ### ✅ [GPU] NVIDIA RTX 5090
> - [x] `sudo dkms status | grep nvidia` → `installed` 확인 ✅
> - [x] `nvidia-smi` → RTX 5090 인식, Driver 580.159.04, CUDA 13.0 ✅
> - [ ] `lsmod | grep nvidia` → nvidia 드라이버 로드 확인
>
> ### ✅ [Tools] 기본 개발 도구
> - [x] `gcc --version` → 11.4.0 (Isaac Sim 권장 버전) ✅
> - [x] `which cmake git wget curl unzip make` → 모두 경로 출력 ✅
> - [x] `python3 --version` → 3.13.2 (miniconda3) — Isaac Sim 내장 Python과 무관 ✅
>
> ### ✅ [ROS 2] Humble
> - [x] `dpkg -l | grep ros-humble-desktop` → 설치 확인 ✅
> - [x] `ls /etc/apt/sources.list.d/ros2.list` → 저장소 등록 확인 ✅
> - [x] `sudo apt install ros-humble-moveit` → MoveIt 2.5.9 설치 완료 ✅
> - [x] `sudo apt install ros-humble-moveit-msgs` → 설치 완료 ✅
> - [x] `sudo apt install ros-humble-moveit-visual-tools` → 설치 완료 ✅
> - [x] `sudo apt install ros-humble-joint-state-publisher` → 설치 완료 ✅
> - [x] `ros-humble-rviz2 ros-humble-topic-tools ros-humble-teleop-twist-keyboard` → 설치 완료 ✅
> - [x] `echo $ROS_DISTRO` → `humble` ✅
> - [x] `ros2 topic list` → `/parameter_events`, `/rosout` 정상 출력 ✅
>
> ### ✅ [Isaac Sim] Standalone (Isaac Lab 불필요)
> - [x] NVR: RTX 5090, Driver 580.159.04, CUDA 13.0 ✅ (사전 확인 완료)
> - [x] CUDA Toolkit (nvcc): 12.4.131 설치 확인 ✅ (선택사항)
> - [ ] `ls ~/isaacsim/isaac-sim.sh` → 파일 존재 (설치 필요)
> - [ ] Isaac Sim GUI 실행 → USD 로딩 정상
> - [ ] `ros2 topic list` (Isaac Sim Play 중) → `/clock`, `/joint_states` 등 표시
>
> ### ✅ [Workspace] DLI ROS Workspace
> - [x] `conda deactivate && sudo apt install python3-catkin-pkg` → 필수 패키지 설치 ✅
> - [x] `colcon build` → 5 packages finished, 에러 없음 ✅
> - [ ] `source install/setup.bash` → `.bashrc` 등록 필요 시
>
> ### ✅ [Parsec] 원격 데스크톱 (선택사항)
> - ⚠️ 구 `curl .../parsec.sh | sudo bash` 스크립트는 **404 반환** → Snap 사용
> - [ ] `sudo snap install parsec --classic` → 설치 완료
> - [ ] `snap run parsec` → GUI 정상 실행

### ✅ [Assets] DLI Course Assets
> - [ ] `ls ~/Desktop/DLI_SIL/Starting_point/` → nova_carter, franka 등 존재
> - [ ] `rosdep install --from-paths src --ignore-src -r -y` → 의존성 충족
