# Class 02: Jetson DLI Docker 설치 및 Jupyter 사용 실습

## 1. Docker 기초

### 1.1 Docker란?

Docker는 컨테이너 기반의 가상화 플랫폼입니다. 개발 환경을 표준화하고 재현 가능하게 만들 수 있습니다.

### 1.2 Docker 핵심 개념

```
┌─────────────────────────────────────┐
│         Host Operating System      │
│  ┌───────────────────────────────┐ │
│  │         Docker Engine         │ │
│  │  ┌────────┐ ┌────────┐ ┌────┐  │ │
│  │  │Container│ │Container│ │Cnt │  │ │
│  │  │   1    │ │   2    │ │ 3  │  │ │
│  │  └────────┘ └────────┘ └────┘  │ │
│  │  ┌───────────────────────────┐ │ │
│  │  │      Images              │ │ │
│  │  └───────────────────────────┘ │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 2. Jetson에 Docker 설치

### 2.1 Docker 설치

```bash
# Docker 설치
sudo apt-get update
sudo apt-get install -y docker.io

# Docker 서비스 시작
sudo systemctl start docker
sudo systemctl enable docker

# 현재 사용자 docker 그룹에 추가
sudo usermod -aG docker $USER

# Docker 버전 확인
docker --version
```

### 2.2 Docker 기본 설정

```bash
# Docker 시작 확인
sudo systemctl status docker

# Docker 정보 확인
docker info

# Hello World 컨테이너 실행 (테스트)
sudo docker run hello-world
```

## 3. NVIDIA Docker 설치

### 3.1 NVIDIA Container Toolkit

Jetson에서 GPU를 Docker 컨테이너에서 사용하려면 NVIDIA Container Toolkit이 필요합니다.

```bash
# NVIDIA Docker 설치 (Jetson용)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# Docker 재시작
sudo systemctl restart docker
```

### 3.2 GPU 확인

```bash
# NVIDIA Docker가 정상 동작하는지 확인
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

## 4. Jetson DLI Docker 이미지

### 4.1 DLI Docker 이미지란?

NVIDIA DLI(Deeper Learning Institute)에서는 교육용 Docker 이미지를 제공합니다. 이 이미지는 Jetson용으로 최적화된 딥러닝 환경を含みます。

### 4.2 DLI 이미지 다운로드

```bash
# NVIDIA DLI Jupyter Docker 이미지 Pull
# (Jetson Nano의 경우 arm64 버전 사용)
docker pull nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1

# 이미지 목록 확인
docker images
```

### 4.3 컨테이너 실행

```bash
# Jupyter가 포함된 컨테이너 실행
docker run --name dli-nano -it --rm \
    -p 8888:8888 \
    --runtime nvidia \
    -v /home/$USER:/workspace \
    nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1

# 백그라운드 실행
docker run -d --name dli-nano \
    -p 8888:8888 \
    --runtime nvidia \
    -v /home/$USER:/workspace \
    nvcr.io/nvidia/dli/dli-nano-ai:v2.0.1
```

## 5. Jupyter Notebook 사용

### 5.1 Jupyter 접근

```bash
# 컨테이너 실행 확인
docker ps

# Jupyter 접근 URL 확인
docker logs dli-nano

# 브라우저에서 접근
# http://<Jetson_IP>:8888
```

### 5.2 Jupyter 환경 구성

```bash
# 컨테이너 내부 접속
docker exec -it dli-nano bash

# Python 환경 확인
python3 -c "import torch; print(torch.__version__)"
python3 -c "import tensorflow as tf; print(tf.__version__)"
python3 -c "import cv2; print(cv2.__version__)"
```

### 5.3 Jupyter 기본 사용법

**새 Notebook 생성:**
1. New → Python 3 클릭

**셀 실행:**
- Shift + Enter: 실행 후 다음 셀로 이동
- Ctrl + Enter: 현재 셀만 실행

**주석:**
- #: 한 줄 주석
- """ """: 여러 줄 주석

## 6. 실습: Jupyter에서 CUDA 확인

### 6.1 기본 환경 확인

Jupyter Notebook에서 다음 코드를 실행합니다:

```python
# CUDA 확인
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
print(f"Device count: {torch.cuda.device_count()}")
print(f"Device name: {torch.cuda.get_device_name(0)}")
```

### 6.2 TensorFlow CUDA 확인

```python
# TensorFlow에서 CUDA 확인
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")
print(f"GPU available: {tf.config.list_physical_devices('GPU')}")
```

### 6.3 OpenCV GPU 확인

```python
# OpenCV CUDA 지원 확인
import cv2
print(f"OpenCV version: {cv2.__version__}")
print(f"CUDA support: {cv2.cuda.getCudaEnabledDeviceCount()}")
```

## 7. Docker 관리

### 7.1 컨테이너 관리

```bash
# 실행 중인 컨테이너 확인
docker ps -a

# 컨테이너 시작
docker start dli-nano

# 컨테이너 중지
docker stop dli-nano

# 컨테이너 제거
docker rm dli-nano
```

### 7.2 이미지 관리

```bash
# 이미지 목록
docker images

# 이미지 제거
docker rmi <image_id>

# 사용하지 않는 이미지 정리
docker image prune -a
```

## 8. 실습 과제

1. Docker를 설치하고 hello-world 컨테이너를 실행하세요.
2. NVIDIA Docker를 설치하고 GPU 접근을 확인하세요.
3. DLI Docker 이미지를 다운로드하고 Jupyter를 실행하세요.
4. Jupyter에서 CUDA, TensorFlow, PyTorch 버전을 확인하세요.

## 9. 다음 실습 예고

다음 클래스에서는 Image Classification 실습을 진행합니다.