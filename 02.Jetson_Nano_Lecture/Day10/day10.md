# Day 10 — Sim-to-Real with NVIDIA Isaac (SO-101 Workshop)

> Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac
> Task: **Centrifuge Vial Pick-and-Place** — 원심분리 바이알을 집어서 랙에 옮기는 작업

---

## 목차

1. [개요](#1-개요)
2. [사전 준비 (Windows + WSL2)](#2-사전-준비-windows--wsl2)
3. [Brev CLI로 클라우드 GPU 인스턴스 실행](#3-brev-cli로-클라우드-gpu-인스턴스-실행)
4. [컨테이너 환경 설정](#4-컨테이너-환경-설정)
5. [모델 파일 다운로드](#5-모델-파일-다운로드)
6. [워크숍 실행 (2개 터미널)](#6-워크숍-실행-2개-터미널)
7. [전체 파이프라인 요약](#7-전체-파이프라인-요약)
8. [Sim-to-Real 개념 정리](#8-sim-to-real-개념-정리)
9. [문제 해결](#9-문제-해결)
10. [로컬 vs 클라우드 전략](#10-로컬-vs-클라우드-전략)

---

## 1. 개요

### 1.1 What Is Sim-to-Real?

Sim-to-Real이란 **시뮬레이션 환경 내에서 policy를 학습**하여 실제 하드웨어에 배포하는 것.

> 최종 목표: 시뮬레이션에서 학습했지만, **실제에서도 잘 동작**하는 policy를 만드는 것

### 1.2 Sim-to-Real Gap ( Reality Gap )

시뮬레이션과 현실 사이의 차이로, 극복해야 할 주요 격차:

| Gap 유형 | 설명 |
|---|---|
| **Sensing Gap** | 시뮬레이터의 센서와 실제 센서 간 차이 (노이즈, 조명, 해상도) |
| **Actuation Gap** | 시뮬레이션 모터와 실제 모터 응답 특성 차이 |
| **Physics Gap** | 마찰, 질량, 유체 등 물리 엔진의 한계 |
| **Modeling Gap** | 로봇/환경 모델링 자체의 부정확성 |

참고 자료:
- [The Reality Gap in Robotics: Challenges, Solutions, and Best Practices](https://www.researchgate.net/publication/338445481_The_Reality_Gap_in_Robotics)
- [Visualizing the Reality Gap — Getting Started With Isaac Lab](https://isaac-sim.github.io/IsaacLab)

### 1.3 Why Simulation Matters

| 항목 | 설명 |
|---|---|
| **Time** | 시간적 이점 확보 (병렬 시뮬레이션, 가속 시간) |
| **Cost** | 실제 로봇 테스트보다 우수한 비용 효율성 |
| **Safety** | 실제 로봇 작업이 위험할 수 있는 시나리오 안전하게 테스트 |
| **Diversity** | 다양한 Domain Randomization(DR)을 자유롭게 수행 가능 |

### 1.4 How It Works (이번 Hands-on)

**Isaac GR00T-N1.6 VLA (Vision-Language-Action) 모델** 사용:

```
자연어 입력: "Pick up the vial and place it on the rack"
         ↓
Joint feedback + Camera observation → Policy 입력
         ↓
Motor position → 로봇 동작 수행
```

---

## 2. 사전 준비 (Windows + WSL2)

> 이 워크숍은 **클라우드 GPU 인스턴스(RTX Pro 6000)** 를 사용합니다.
> Windows 사용자는 WSL2 환경에서 Brev CLI로 접속합니다.

### 2.1 WSL2 설치

**PowerShell(관리자 권한)** 실행:

```powershell
wsl --install
```

재부팅 후 Ubuntu 실행 → 사용자 이름/비밀번호 생성.

WSL2 버전 확인:

```powershell
wsl -l -v
```

```
PS C:\Users\Administrator> wsl -l -v
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

### 2.2 Ubuntu 업데이트

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.3 Brev CLI 설치

```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"
```

PATH 등록:

```bash
echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc
source ~/.bashrc
```

설치 확인:

```bash
brev --version
```

> ⚠️ `Command not found` 시:
> ```bash
> sudo cp /root/.local/bin/brev /usr/local/bin/brev
> ```

---

## 3. Brev CLI로 클라우드 GPU 인스턴스 실행

> 이번 과정은 **RTX Pro 6000 (Blackwell, 96GB VRAM)** 인스턴스를 사용합니다.

### 3.1 Brev 로그인

```bash
brev login
```

브라우저에서 OAuth 로그인 진행.

### 3.2 인스턴스 생성

```bash
brev create
```

또는 특정 인스턴스 타입 지정:

```bash
brev create --type rtx-pro-6000
```

### 3.3 인스턴스 목록 확인

```bash
brev ls
```

### 3.4 SSH 접속

```bash
brev open <instance-name>
```

### 3.5 인스턴스 내 필수 확인 사항

SSH로 접속한 후:

```bash
# NVIDIA Container Toolkit 설치 확인
nvidia-ctk --version

# Docker 소켓 권한 설정 (selkies 환경)
sudo chmod 666 /var/run/docker.sock

# shadeform 디렉토리 권한
sudo chmod -R 777 /home/shadeform
```

---

## 4. 컨테이너 환경 설정

> 클라우드 인스턴스 SSH 터미널에서 실행

### 4.1 저장소 클론

```bash
mkdir -p ~/sim2real
cd ~/sim2real
git clone https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop.git
cd Sim-to-Real-SO-101-Workshop
```

### 4.2 의존성 설치

```bash
sudo apt-get update && sudo apt-get install -y git-lfs

# selkies 환경에서는 docker.io도 설치
sudo apt-get install -y docker.io

git lfs install
git lfs pull
```

### 4.3 Teleop & Simulation 컨테이너 빌드

```bash
docker build -t teleop-docker -f docker/sim/Dockerfile .
```

> 빌드 시간: 수십 분 소요 (Isaac Sim, Isaac Lab, LeRobot 등 포함)

### 4.4 Real Robot & Inference Server 컨테이너 빌드

**Blackwell GPU (RTX Pro 6000)**:

```bash
./docker/real/build.sh blackwell
```

**Ada GPU (RTX 4090 등)**:

```bash
./docker/real/build.sh ada
```

> ⚠️ 이 빌드는 teleop 컨테이너보다 **훨씬 오래 걸림** (GR00T, flash-attention 등 포함)

---

## 5. 모델 파일 다운로드

### 5.1 Hugging Face 로그인

```bash
pip install -U "huggingface_hub[cli]"
huggingface-cli login
```

**read token** 입력 필요 → [Hugging Face Tokens](https://huggingface.co/settings/tokens) 에서 생성

> GR00T N1.6 모델 페이지: [nvidia/GR00T-N1.6-3B](https://huggingface.co/nvidia/GR00T-N1.6-3B)

### 5.2 사전 학습된 Fine-tuned 모델 다운로드

```bash
cd ~/sim2real/Sim-to-Real-SO-101-Workshop
mkdir -p models
```

**4개 모델 다운로드:**

```bash
# 1. Simulation-only teleop
huggingface-cli download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left

# 2. Sim + Real co-training
huggingface-cli download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real

# 3. Augmented dataset model
huggingface-cli download aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02 \
  --local-dir ./models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02

# 4. Cosmos-augmented model
huggingface-cli download aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70 \
  --local-dir ./models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
```

---

## 6. 워크숍 실행 (2개 터미널)

> 클라우드 인스턴스에서 **2개의 SSH 터미널** 또는 **tmux/screen**으로 분할 실행

### 6.1 터미널 1 — Inference Server (GR00T 모델 서빙)

```bash
# X11 권한
xhost +

# Real Robot 컨테이너 실행
sudo docker run -it --rm --name real-robot --network host --privileged \
    --device nvidia.com/gpu=all \
    -e DISPLAY \
    -v /dev:/dev \
    -v /run/udev:/run/udev:ro \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
    -v $PWD/models:/workspace/models \
    -v $PWD/docker/env:/root/env \
    -v $PWD/docker/real/scripts:/Isaac-GR00T/gr00t/eval/real_robot/SO100 \
    real-robot \
    /bin/bash
```

컨테이너 내부에서 추론 서버 실행:

```bash
export MODEL=aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left/checkpoint-10000

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
```

> 서버가 실행된 상태로 유지되어야 함 — **terminal 1은 계속 켜둠**

### 6.2 터미널 2 — Teleop & Simulation

```bash
xhost +

# Teleop 컨테이너 실행
sudo docker run --name teleop -it --privileged --device nvidia.com/gpu=all -e "ACCEPT_EULA=Y" --rm --network=host \
   -e "PRIVACY_CONSENT=Y" \
   -e DISPLAY \
   -v /dev:/dev \
   -v /run/udev:/run/udev:ro \
   -v $HOME/.Xauthority:/root/.Xauthority \
   -v ~/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
   -v ~/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
   -v ~/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
   -v ~/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
   -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
   -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
   -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
   -v ~/docker/isaac-sim/documents:/root/Documents:rw \
   -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
   -v $PWD/docker/env:/root/env \
   -v $PWD:/workspace/Sim-to-Real-SO-101-Workshop \
   teleop-docker:latest
```

컨테이너 내부에서 평가 실행:

```bash
lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --headless \
    --rerun
```

### 6.3 실행 구조 요약

```
Terminal 1 (real-robot 컨테이너)           Terminal 2 (teleop 컨테이너)
┌─────────────────────────────┐           ┌──────────────────────────────┐
│                             │           │                              │
│  run_gr00t_server.py        │◄────gRPC──►  lerobot_eval                │
│  (GR00T N1.6 모델 추론)      │           │  (Isaac Sim 시뮬레이션)      │
│                             │           │                              │
│  Port: 기본 gRPC 포트       │           │  Observation → gRPC 요청     │
│  Return: motor position     │──────────►  Action ← 응답                │
└─────────────────────────────┘           └──────────────────────────────┘
```

---

## 7. 전체 파이프라인 요약

```
1. Brev 인스턴스 실행 (RTX Pro 6000)
         ↓
2. 저장소 클론 + 컨테이너 빌드
         ↓
3. Hugging Face 모델 다운로드 (4개)
         ↓
4. Terminal 1: Inference Server 실행
         ↓
5. Terminal 2: Simulation + Evaluation 실행
         ↓
6. 결과 확인 (rerun 시각화)
```

---

## 8. Sim-to-Real 개념 정리

### 8.1 Domain Randomization (DR)

시뮬레이션 환경의 다양한 요소(조명, 질감, 색상, 물리 파라미터 등)를 **무작위화**하여 현실과의 격차를 줄이는 기법.

### 8.2 GR00T N1.6 VLA Model

- **Vision-Language-Action** 모델
- 자연어 명령 → 로봇 행동으로 직접 매핑
- 1.6B / 3B 파라미터 모델 제공
- 사전 학습된 Foundation Model을 특정 태스크에 **post-training**(미세 조정)

### 8.3 이번 과정의 4가지 Sim-to-Real 전략

| 전략 | 설명 | 무거운 연산 |
|---|---|---|
| **Strategy 1:** Domain Randomization (시뮬레이션 데이터만 학습) | DR 적용 + Teleop 데이터 수집 → GR00T fine-tuning | GR00T 학습 (클라우드) |
| **Strategy 2:** Co-Training with Real Data | 시뮬레이션 + 실제 데이터 함께 학습 | GR00T 학습 (클라우드) |
| **Strategy 3:** Augment with Cosmos | Cosmos World Model로 데이터 증강 | Cosmos 추론 (클라우드) |
| **Strategy 4:** SAGE + GapONet | Actuation Gap 측정 및 보정 | 비교적 가벼움 |

---

## 9. 문제 해결

| 증상 | 해결 방법 |
|---|---|
| `nvidia-ctk: command not found` | `sudo apt install -y nvidia-container-toolkit` |
| `docker: permission denied` | `sudo chmod 666 /var/run/docker.sock` |
| `Permission denied: /home/shadeform` | `sudo chmod -R 777 /home/shadeform` |
| `CUDA out of memory` | 배치 사이즈 축소, 불필요한 프로세스 종료 |
| `git-lfs: command not found` | `sudo apt install -y git-lfs` |
| Docker build 실패 | `docker system prune -a` 로 캐시 정리 후 재시도 |
| Hugging Face 인증 실패 | `huggingface-cli login` 으로 토큰 재설정 |
| Inference server 연결 안 됨 | Terminal 1 서버 포트가 Terminal 2에서 접근 가능한지 확인 |
| X11 display 오류 | `xhost +` 실행 확인, DISPLAY 환경변수 확인 |
| `lerobot_eval: command not found` | teleop 컨테이너가 정상 빌드되었는지 확인 |

---

## 10. 로컬 vs 클라우드 전략

### 10.1 전체 파이프라인 기준 판단

| 구성 요소 | VRAM 요구 | 로컬 (5090 24GB) | 클라우드 (RTX Pro 6000 96GB) |
|---|---|---|---|
| Isaac Sim 기본 실행 | ~16GB | ✅ 가능 | ✅ |
| Domain Randomization | ~16-20GB | ✅ 가능 | ✅ |
| GR00T Inference (학습된 모델 실행) | ~8-10GB | ✅ 가능 | ✅ |
| GR00T Fine-tuning (학습) | ~31GB+ | ❌ 불가 | ✅ |
| Cosmos Predict2-2B 추론 | ~26-33GB | ❌ 불가 | ✅ |
| Real Robot Inference | ~10GB | ✅ 가능 | ✅ |

### 10.2 권장 Workflow (하이브리드)

```
[로컬 5090 24GB]                     [클라우드 RTX Pro 6000]
─────────────────                    ────────────────────────

Isaac Sim 기본 실습 ──────────►  GR00T Fine-tuning
                                    Cosmos Augmentation
      ◄──────────────────────  체크포인트 / 증강 데이터 다운로드

Fine-tuned 모델 Inference
Sim / Real Evaluation
```

### 10.3 SSD Swap은 도움이 될까?

**SSD Swap은 GPU VRAM 부족을 해결하지 못합니다.** GPU 연산은 VRAM에 올라간 데이터로만 동작하며, SSD Swap은 시스템 RAM(64GB) 초과 시에만 보조 역할을 합니다.

단, **CPU Offloading** 기법(DeepSpeed ZeRO-3 + CPU offload)을 사용하면 VRAM 부담을 시스템 RAM으로 전가할 수 있습니다. 이때 시스템 RAM이 부족하면 SSD Swap이 보조 역할을 합니다.

```
GPU VRAM (24GB) ← 부족 → CPU Offload → System RAM (64GB) ← 초과 → SSD Swap
     ✗ 불가                    가능                    마지막 보루
```

---

## 참고 자료

| 자료 | 링크 |
|---|---|
| Workshop 저장소 | https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop |
| NVIDIA 공식 문서 | https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/ |
| GR00T N1.6 모델 | https://huggingface.co/nvidia/GR00T-N1.6-3B |
| GR00T 저장소 | https://github.com/NVIDIA/Isaac-GR00T |
| Cosmos 문서 | https://docs.nvidia.com/cosmos/ |
| Isaac Sim 요구사양 | https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html |

---

*최종 업데이트: 2026-05-26*
