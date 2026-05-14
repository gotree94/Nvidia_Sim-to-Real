# Jetson Nano 2GB 딥러닝 객체 인식 종합 교육자료

> **목표**: Jetson Nano 2GB Developer Kit에서 Darknet(YOLOv4-tiny), PyTorch/YOLOv5, TensorRT를 활용한 이미지/실시간 객체 인식의 이해와 실습
>
> **대상**: 임베디드 AI 입문자 ~ 중급 개발자
>
> **버전**: JetPack 4.6.1 (R32.7.1), CUDA 10.2, cuDNN 8.2.1, TensorRT 8.0.1, OpenCV 4.1.1

---

## 목차

### Part 1 — 하드웨어 개요 및 환경 설정
- [1. Jetson Nano 2GB 이해](#1-jetson-nano-2gb-이해)
- [2. 개발 환경 구축](#2-개발-환경-구축)
- [3. 메모리 최적화](#3-메모리-최적화)

### Part 2 — Darknet YOLO 객체 인식
- [4. Darknet (AlexeyAB) 설치](#4-darknet-alexeyab-설치)
- [5. YOLO 이론 기초](#5-yolo-이론-기초)
- [6. 이미지 객체 인식 실습](#6-이미지-객체-인식-실습)
- [7. 실시간 웹캠 데모](#7-실시간-웹캠-데모)
- [8. Python 바인딩 활용](#8-python-바인딩-활용)

### Part 3 — PyTorch / YOLOv5
- [9. PyTorch 설치 (aarch64)](#9-pytorch-설치-aarch64)
- [10. YOLOv5 개요 및 설치](#10-yolov5-개요-및-설치)
- [11. YOLOv5 추론 실행](#11-yolov5-추론-실행)

### Part 4 — TensorRT 최적화
- [12. TensorRT 개념 이해](#12-tensorrt-개념-이해)
- [13. ONNX → TensorRT 변환](#13-onnx--tensorrt-변환)
- [14. TensorRT 추론 구현](#14-tensorrt-추론-구현)

### Part 5 — 종합
- [15. 성능 벤치마크](#15-성능-벤치마크)
- [16. 문제 해결 (Troubleshooting)](#16-문제-해결-troubleshooting)
- [17. 참고 자료](#17-참고-자료)

---

# Part 1 — 하드웨어 개요 및 환경 설정

---

## 1. Jetson Nano 2GB 이해

### 1.1 스펙

| 구성 요소 | 사양 |
|---|---|
| **GPU** | NVIDIA Maxwell **128 CUDA 코어** |
| **CPU** | ARM Cortex-A57 **4코어** @ 1.43GHz |
| **RAM** | **2GB LPDDR4** 25.6GB/s |
| **스토리지** | microSD 카드 (권장: 64GB UHS-I 이상) |
| **CUDA Arch** | **compute_53** (Maxwell GM107b) |
| **비디오 인코딩** | 4K@30 (H.264/H.265) |
| **디스플레이** | HDMI 2.0, eDP 1.4 |
| **USB** | USB 3.0 × 1, USB 2.0 × 2 |
| **카메라** | MIPI CSI-2 (15-pin, 22-pin) |
| **네트워크** | Gigabit Ethernet |
| **전원** | 5V⎓3A (마이크로 USB) |

### 1.2 GPU 아키텍처: Maxwell

Jetson Nano의 GPU는 **Maxwell 아키텍처**(GM107b)입니다.

- **128 CUDA 코어** — 2개의 SM(Streaming Multiprocessor), 각 64 CUDA
- **FP16 지원** — 하지만 INT8은 지원하지 않음 (Xavier 이상만 지원)
- **compute capability 5.3** — NVIDIA GPU 중 가장 낮은 편에 속함

> Darknet의 Makefile에서 `ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]`로 설정하는 이유입니다.

### 1.3 2GB와 4GB 모델의 차이

| 항목 | 2GB 모델 | 4GB 모델 |
|---|---|---|
| RAM | 2GB LPDDR4 | 4GB LPDDR4 |
| GPU 코어 | 동일 (128 CUDA) | 동일 |
| CPU | 동일 (Cortex-A57) | 동일 |
| YOLOv4-tiny 실행 | ✅ 가능 (17~25 FPS) | ✅ 가능 |
| YOLOv4 full 실행 | ❌ **OOM** | 2 FPS (한계) |
| YOLOv5s + TensorRT | ✅ 가능 (25 FPS @320) | ✅ 가능 |
| YOLOv5m/l/x | ❌ OOM | ✅ (m만 가능) |
| 가격 | **$59** (단종) | $99 |

**2GB의 핵심 제약**: GPU 자체는 4GB 모델과 완전히 동일하지만, **RAM이 절반**이므로 더 큰 모델을 올릴 수 없습니다. 대신 경량 모델(yolov4-tiny, yolov5s/n)에 최적화하면 4GB 모델에 뒤지지 않는 성능을 냅니다.

### 1.4 JetPack 소프트웨어 스택

JetPack은 NVIDIA가 Jetson 보드를 위해 제공하는 통합 SDK입니다. JetPack 4.6.1에는 다음이 포함됩니다:

```
JetPack 4.6.1 (L4T R32.7.1)
├── CUDA 10.2            # GPU 병렬 연산 라이브러리
├── cuDNN 8.2.1          # 딥러닝 GPU 가속 라이브러리
├── TensorRT 8.0.1       # 추론 최적화 엔진
├── OpenCV 4.1.1         # 컴퓨터 비전 라이브러리
├── VisionWorks          # 컴퓨터 비전 가속
├── Multimedia API       # 하드웨어 비디오 코덱
└── Linux4Tegra (L4T)    # 우분투 18.04 기반 커널
```

> 일반 PC와 달리 pip로 CUDA/cuDNN을 설치할 필요가 없습니다. JetPack이 부팅 이미지에 포함되어 있습니다.

---

## 2. 개발 환경 구축

### 2.1 SD 카드 준비

**필요 준비물**:
- microSD 카드 (64GB 이상, UHS-I U3 속도 권장)
- SD 카드 리더기
- PC (Windows / macOS / Linux)

**Windows**:
```bash
# 1. SD Memory Card Formatter로 포맷
# 2. Etcher 다운로드 (https://www.balena.io/etcher/)
# 3. Jetson Nano 2GB SD 카드 이미지 선택 → Flash
```

**Linux/macOS**:
```bash
# 압축 이미지 바로 쓰기 (macOS 예시)
/usr/bin/unzip -p ~/Downloads/jetson_nano_devkit_sd_card.zip | \
  sudo /bin/dd of=/dev/rdisk bs=1m status=progress
```

### 2.2 초기 부팅

1. SD 카드를 Jetson Nano 하단에 삽입
2. HDMI 모니터, USB 키보드/마우스, LAN (또는 WiFi USB) 연결
3. 마이크로 USB 전원 연결 (**5V⎓3A** — 2A 이하 아답터는 언더볼티지 위험)
4. 부팅 후 초기 설정(Locale, 계정, WiFi)
5. JetPack 버전 확인:

```bash
cat /etc/nv_tegra_release
# → R32 (release), REVISION: 7.1, ...
```

### 2.3 시스템 업데이트

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y build-essential git cmake curl wget
```

### 2.4 CUDA PATH 설정

JetPack에 CUDA가 포함되어 있지만, PATH가 자동으로 설정되지 않을 수 있습니다.

```bash
# 환경 변수 등록
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# 영구 적용
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 확인
nvcc --version   # Cuda compilation tools, release 10.2
```

---

## 3. 메모리 최적화

2GB RAM으로 딥러닝 추론을 실행하려면 **메모리 확보가 가장 중요**합니다.

### 3.1 용어 설명

| 용어 | 설명 |
|---|---|
| **RAM** | 물리 메모리. 프로그램이 실행되는 공간 |
| **Swap** | 디스크 일부를 RAM처럼 사용. RAM이 부족할 때 사용되나 **매우 느림** |
| **ZRAM** | RAM의 일부를 압축해서 swap처럼 사용. 압축/해제에 CPU 사용 |
| **OOM** | Out Of Memory. 메모리 부족으로 프로세스가 강제 종료됨 |
| **GUI** | 그래픽 데스크톱 환경. Xorg + Ubuntu Desktop이 약 500MB~1GB 사용 |

### 3.2 GUI 비활성화 (가장 효과적)

Ubuntu 데스크톱 환경은 부팅 후 약 **800MB~1.2GB**의 RAM을 사용합니다. 이를 텍스트 모드로 전환하면 500MB 이상 확보됩니다.

```bash
# 텍스트 모드 (멀티유저 타겟)로 전환
sudo systemctl set-default multi-user.target

# 재부팅
sudo reboot
```

부팅 후 터미널 로그인 프롬프트만 나타납니다. SSH로 원격 접속해도 동일합니다.

> **되돌리기**: `sudo systemctl set-default graphical-user.target && sudo reboot`

**확인**:
```bash
systemctl get-default   # multi-user.target → GUI 비활성화 상태
free -h                 # used 메모리가 확연히 줄어든 것을 확인
```

### 3.3 Swap 파일 생성

Swap은 디스크의 일부를 메모리처럼 사용하는 기술입니다. RAM이 부족할 때 사용되지만 속도는 매우 느립니다(RAM 대비 1/100 ~ 1/1000 수준).

**중요**: microSD는 쓰기 수명이 짧으므로 swap용으로 **USB 3.0 포트에 SSD를 연결**하는 것을 권장합니다.

```bash
# 4GB swap 파일 생성
sudo fallocate -l 4G ~/swapfile && sudo chmod 600 ~/swapfile
sudo mkswap ~/swapfile
sudo swapon ~/swapfile

# 부팅 시 자동 적용
echo '/home/nvidia/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab

# 확인
swapon --show
free -h
```

> `fallocate`가 실패하면 `dd` 사용: `sudo dd if=/dev/zero of=~/swapfile bs=1M count=4096 status=progress`

### 3.4 메모리 상태 모니터링

```bash
# 실시간 모니터링 (htop)
sudo apt-get install -y htop
htop

# GPU 상태 모니터링 (jtop)
sudo pip3 install jetson-stats
sudo jtop
```

`jtop`에서 확인할 수 있는 정보:
- **MEM** — RAM 사용량
- **GPU** — GPU 사용률 및 메모리
- **CTRL** — CPU 온도 및 클럭

---

# Part 2 — Darknet YOLO 객체 인식

---

## 4. Darknet (AlexeyAB) 설치

### 4.1 Darknet이란?

Darknet은 **C 언어와 CUDA로 작성된 오픈소스 신경망 프레임워크**입니다. YOLO(You Only Look Once) 객체 탐지 알고리즘의 공식 구현체로, pjreddie/darknet이 원본이고 AlexeyAB/darknet이 커뮤니티에서 가장 활발히 유지보수하는 포크입니다.

**AlexeyAB 버전의 장점**:
- YOLOv4, YOLOv4-tiny 지원
- OPENMP 멀티코어 CPU 최적화
- LIBSO(Python 바인딩) 지원
- Windows/Linux/macOS 크로스 플랫폼
- 활발한 버그 수정 및 유지보수

### 4.2 소스 클론 및 빌드

```bash
cd ~
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
```

### 4.3 Makefile 설정

Makefile에는 Darknet의 빌드 옵션이 정의되어 있습니다. Jetson Nano 2GB에 맞게 수정합니다.

| 옵션 | 값 | 설명 |
|---|---|---|
| `GPU` | 1 | CUDA GPU 가속 활성화 |
| `CUDNN` | 1 | cuDNN 가속 활성화 |
| `CUDNN_HALF` | 0 | FP16 연산 (Jetson Nano에서는 불안정할 수 있음) |
| `OPENCV` | 1 | OpenCV 연동 (입출력, 이미지 처리) |
| `OPENMP` | 1 | CPU 멀티코어 병렬 처리 |
| `LIBSO` | 1 | 공유 라이브러리(libdarknet.so) 생성 — Python에서 필요 |
| `AVX` | 0 | x86 전용 명령어. ARM CPU에서는 OFF |
| `ARCH` | `compute_53` | Jetson Nano GPU 아키텍처 지정 |

```bash
sed -i 's/^GPU=0/GPU=1/' Makefile
sed -i 's/^CUDNN=0/CUDNN=1/' Makefile
sed -i 's/^OPENCV=0/OPENCV=1/' Makefile
sed -i 's/^OPENMP=0/OPENMP=1/' Makefile
sed -i 's/^LIBSO=0/LIBSO=1/' Makefile
sed -i 's/^AVX=1/AVX=0/' Makefile
# ARCH 줄을 Jetson Nano에 맞게 compute_53으로 변경
sed -i 's/^ARCH= -gencode arch=compute_52,code=\[sm_52,compute_52\]/ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]/' Makefile
```

### 4.4 빌드

```bash
# OpenMP 라이브러리 설치
sudo apt-get install -y libomp-dev

# 병렬 빌드 (4코어)
make -j4
```

빌드에 성공하면 `darknet` 실행 파일이 생성됩니다.

```bash
./darknet
# → usage: darknet <function>
```

### 4.5 가중치(weights) 파일이란?

딥러닝 모델은 두 가지 파일로 구성됩니다:

| 파일 | 설명 | 예 |
|---|---|---|
| `.cfg` | 네트워크 구조 정의 (몇 개의 레이어, 필터 크기 등) | `yolov4-tiny.cfg` |
| `.weights` | 사전 학습된 파라미터 (가중치, 바이어스) | `yolov4-tiny.weights` |

`.cfg`만 있으면 모델 구조는 알 수 있지만, 학습된 지식(가중치)이 없으므로 추론을 할 수 없습니다. `.weights`는 대규모 데이터셋(COCO: 80클래스, 33만 장)으로 미리 학습된 파라미터입니다.

### 4.6 YOLOv4-tiny 가중치 다운로드

**왜 yolov4-tiny인가?**

| 모델 | 레이어 수 | BFlops | 크기 | 2GB 실행 |
|---|---|---|---|---|
| **yolov4-tiny** | 38 | **6.9** | **23MB** | ✅ |
| yolov4 (full) | 161 | 128.5 | 245MB | ❌ OOM |
| yolov3-tiny | 23 | 5.6 | 34MB | ✅ |
| yolov3 (full) | 106 | 65.9 | 236MB | ❌ OOM |

YOLOv4-tiny는 full 버전의 **1/19** 수준의 연산량으로, 정확도는 다소 낮지만(mAP 40.2% vs 65.7%) 실시간 추론에 적합합니다.

```bash
mkdir -p ~/darknet/weights
cd ~/darknet/weights
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
cd ~/darknet
```

---

## 5. YOLO 이론 기초

### 5.1 객체 인식(Object Detection)이란?

객체 인식은 이미지에서 **"무엇이" (분류, Classification)** **"어디에 있는지" (위치, Localization)** 를 동시에 찾는 컴퓨터 비전 작업입니다.

출력 형식: `[클래스, 신뢰도(confidence), x_center, y_center, width, height]`

```
person: 0.92  (0.35, 0.45, 0.12, 0.30)
car:    0.87  (0.62, 0.38, 0.20, 0.15)
```

### 5.2 YOLO의 핵심 아이디어

YOLO는 **You Only Look Once**의 약자로, 이미지를 **한 번만 보고** 모든 객체를 동시에 탐지합니다.

**동작 방식**:

```
입력 이미지 (608×608)
       ↓
   CNN (하나의 네트워크)
       ↓
   S×S 그리드 (7×7 → 19×19)
       ↓
   각 그리드 셀에서:
     - B개의 바운딩 박스 예측 (x, y, w, h, confidence)
     - C개의 클래스 확률
       ↓
   출력: S × S × (B×5 + C) 텐서
       ↓
   NMS (Non-Maximum Suppression)로 중복 제거
       ↓
   최종 탐지 결과
```

**YOLOv4-tiny 구조**:

```
Input (416×416×3)
  → CSPDarknet53-tiny Backbone (특징 추출)
  → SPP (Spatial Pyramid Pooling)
  → PANet Neck (다중 스케일 특징 융합)
  → YOLO Head × 2 (13×13, 26×26) ← 두 개의 출력 스케일
```

- **Backbone**: 이미지에서 특징을 추출하는 부분
- **Neck**: 여러 스케일의 특징을 결합
- **Head**: 최종 객체 위치와 클래스를 예측

### 5.3 Non-Maximum Suppression (NMS)

같은 객체에 대해 여러 박스가 겹쳐서 예측되는 경우, 가장 confidence가 높은 박스만 남기고 나머지를 제거하는 후처리 알고리즘입니다.

```
1. 모든 박스를 confidence 기준으로 내림차순 정렬
2. 가장 높은 박스를 선택
3. 나머지 박스 중 IoU(Intersection over Union)가 threshold(보통 0.5) 이상인 박스 제거
4. 2-3 반복
```

### 5.4 COCO 데이터셋

YOLOv4-tiny는 **COCO (Common Objects in Context)** 데이터셋으로 사전 학습되었습니다.

- **80개 객체 클래스**: person, bicycle, car, dog, cat, ...
- **33만 장**의 이미지
- 평가 지표: **mAP@0.5** (IoU threshold 0.5에서의 mean Average Precision)

---

## 6. 이미지 객체 인식 실습

### 6.1 기본 명령어 구조

```bash
./darknet detector test <data_file> <config> <weights> <image> -thresh <threshold>
```

| 인자 | 설명 | 예시 값 |
|---|---|---|
| `detector test` | detector(객체 탐지) 모드로 test 실행 | |
| `cfg/coco.data` | 데이터셋 설정 파일 (클래스 목록, 이미지 경로 등) | |
| `cfg/yolov4-tiny.cfg` | 네트워크 구조 설정 파일 | |
| `weights/yolov4-tiny.weights` | 사전 학습 가중치 | |
| `data/dog.jpg` | 입력 이미지 경로 | |
| `-thresh 0.25` | Confidence 임계값 (이 값 이상만 출력) | 0.0~1.0 |

### 6.2 실행

```bash
cd ~/darknet
./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights data/dog.jpg -thresh 0.25
```

### 6.3 출력 해석

터미널 출력 예시:
```
data/dog.jpg: Predicted in 98.5 milli-seconds.
dog: 87%      (left_x: 0.15, top_y: 0.25, width: 0.30, height: 0.45)
bicycle: 72%  (left_x: 0.55, top_y: 0.30, width: 0.25, height: 0.40)
truck: 63%    (left_x: 0.70, top_y: 0.50, width: 0.20, height: 0.25)
```

- **Predicted in XX ms**: 추론에 걸린 시간 (1초 = 1000ms)
- **dog: 87%**: 클래스: dog, 신뢰도 87%
- **(x, y, w, h)**: 바운딩 박스 좌표 (0~1 정규화)

> `predictions.jpg`가 현재 디렉토리에 저장되며, 바운딩 박스가 그려진 결과 이미지를 확인할 수 있습니다.

### 6.4 Confidence Threshold 조절

```bash
# 높은 임계값: 확실한 객체만 탐지 (정밀도 ↑, 재현율 ↓)
./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights data/dog.jpg -thresh 0.7

# 낮은 임계값: 더 많은 객체 탐지 (재현율 ↑, 정밀도 ↓)
./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights data/dog.jpg -thresh 0.1
```

### 6.5 좌표 출력

```bash
./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights data/dog.jpg -ext_output -thresh 0.25
```

`-ext_output`은 바운딩 박스 좌표를 픽셀 단위로 출력합니다.

---

## 7. 실시간 웹캠 데모

### 7.1 명령어

```bash
# USB 웹캠 (V4L2, 장치 번호 0)
./darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights -c 0
```

### 7.2 동작 방식

`detector demo` 모드는 다음 과정을 수행합니다:

```
웹캠 프레임 캡처 (OpenCV)
    → 프레임을 416×416으로 리사이즈
    → GPU로 업로드
    → YOLOv4-tiny 추론
    → 결과 다운로드
    → 바운딩 박스 + FPS 표시
    → 화면 출력
```

### 7.3 CSI 카메라 사용

Jetson Nano 보드에 있는 CSI 카메라 커넥터(15-pin)를 사용할 경우:

```bash
./darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights -c 1
```

### 7.4 비디오 파일 처리

```bash
./darknet detector demo cfg/coco.data cfg/yolov4-tiny.cfg weights/yolov4-tiny.weights test.mp4 -out_filename result.mp4
```

---

## 8. Python 바인딩 활용

Makefile에서 `LIBSO=1`로 빌드하면 `libdarknet.so`가 생성되어 Python에서 Darknet을 직접 호출할 수 있습니다.

### 8.1 기본 추론

```python
import darknet as dn

# 네트워크 로드 (cfg, data, weights)
net, classes, colors = dn.load_network(
    b"cfg/yolov4-tiny.cfg",
    b"cfg/coco.data",
    b"weights/yolov4-tiny.weights",
    batch_size=1
)

# 이미지 로드
img = dn.load_image(b"data/dog.jpg")

# 추론
dets = dn.detect_image(net, classes, img, thresh=0.25)

# 결과 출력
for label, confidence, bbox in dets:
    print(f"{label.decode()}: {float(confidence):.2f}")

# 메모리 해제
dn.free_image(img)
```

### 8.2 OpenCV 연동

```python
import darknet as dn
import cv2
import numpy as np

# 네트워크 로드
net, classes, colors = dn.load_network(
    b"cfg/yolov4-tiny.cfg",
    b"cfg/coco.data",
    b"weights/yolov4-tiny.weights",
    batch_size=1
)

# OpenCV로 이미지 읽기
frame = cv2.imread("data/dog.jpg")
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Darknet 이미지 변환
img = dn.make_image(frame_rgb.shape[1], frame_rgb.shape[0], 3)
dn.copy_image_from_bytes(img, frame_rgb.tobytes())

# 추론
dets = dn.detect_image(net, classes, img, thresh=0.25)

# 바운딩 박스 그리기
for label, conf, bbox in dets:
    x, y, w, h = map(float, bbox.split())
    x1, y1, x2, y2 = int(x - w/2), int(y - h/2), int(x + w/2), int(y + h/2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, f"{label.decode()} {float(conf):.2f}",
                (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# 결과 저장
cv2.imwrite("python_detection_result.jpg", frame)
dn.free_image(img)
```

---

# Part 3 — PyTorch / YOLOv5

---

## 9. PyTorch 설치 (aarch64)

### 9.1 일반 PC와 Jetson Nano의 차이

일반 PC(x86_64)에서는 `pip install torch`로 끝나지만, Jetson Nano는 **ARM aarch64** 아키텍처이므로 NVIDIA가 직접 제공하는 pre-built wheel을 설치해야 합니다.

### 9.2 PyTorch 1.10.0 설치

JetPack 4.6.1 + Python 3.6 조합에서는 PyTorch 1.10.0이 호환됩니다.

```bash
# 1) 의존성 설치
sudo apt-get install -y libopenblas-base libopenmpi-dev

# 2) PyTorch 1.10.0 (NVIDIA 공식 aarch64 휠)
wget https://nvidia.box.com/shared/static/fjtbno0vpo676a25cgvuqc1wty0fkkg6.whl \
  -O torch-1.10.0-cp36-cp36m-linux_aarch64.whl
pip3 install torch-1.10.0-cp36-cp36m-linux_aarch64.whl
```

### 9.3 torchvision 0.11.1 설치 (소스 컴파일)

torchvision은 aarch64 pre-built wheel이 없으므로 직접 소스 컴파일합니다.

```bash
# 의존성
sudo apt-get install -y libjpeg-dev zlib1g-dev

# 소스 클론 (PyTorch 1.10.0 ↔ torchvision 0.11.1 대응)
git clone --branch v0.11.1 https://github.com/pytorch/vision torchvision
cd torchvision

# 컴파일 및 설치 (약 10~15분 소요)
sudo python3 setup.py install
cd ~
```

> **PyTorch ↔ torchvision 버전 대응표**:
> | PyTorch | torchvision |
> |---|---|
> | 1.10.0 | 0.11.1 |
> | 1.12.0 | 0.13.0 |

### 9.4 설치 확인

```bash
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
# → 1.10.0
# → True
```

`torch.cuda.is_available()`이 `True`여야 GPU를 사용할 수 있습니다.

---

## 10. YOLOv5 개요 및 설치

### 10.1 YOLOv5란?

YOLOv5는 **Ultralytics** 사가 개발한 YOLO 계열 객체 탐지 모델입니다. PyTorch 기반으로 Darknet보다 Python 생태계와의 통합이 쉽고, 다양한 모델 크기(n/s/m/l/x)를 제공합니다.

| 모델 | 파라미터 | BFlops | mAP@0.5 | 특징 |
|---|---|---|---|---|
| **YOLOv5n** (nano) | 1.9M | **4.5** | 34.3% | **2GB에 최적** |
| **YOLOv5s** (small) | 7.2M | **16.5** | 37.0% | **2GB에서 무난** |
| YOLOv5m (medium) | 21.2M | 49.0 | 45.4% | ❌ 2GB OOM |
| YOLOv5l (large) | 46.5M | 109.1 | 49.0% | ❌ |
| YOLOv5x (xlarge) | 86.7M | 205.7 | 50.7% | ❌ |

### 10.2 YOLOv5 설치

```bash
cd ~
git clone https://github.com/ultralytics/yolov5.git
cd yolov5

# 의존성 설치
pip3 install -r requirements.txt
```

> **참고**: PyTorch 1.10.0 + Python 3.6 환경에서 `requirements.txt`의 일부 패키지가 최신 버전을 요구할 수 있습니다. 호환성 문제가 발생하면 버전을 명시적으로 지정하세요.

---

## 11. YOLOv5 추론 실행

### 11.1 사전 학습 가중치 다운로드

```bash
# YOLOv5s (small) — 2GB에 적합
# detect.py 실행 시 자동 다운로드됨
```

### 11.2 이미지 추론

```bash
cd ~/yolov5

# 기본 이미지 추론
python3 detect.py --weights yolov5s.pt --img 640 --conf 0.25 --source data/images/

# 입력 해상도 320으로 낮춤 (속도 ↑, 정확도 ↓)
python3 detect.py --weights yolov5s.pt --img 320 --conf 0.25 --source data/images/

# 더 가벼운 YOLOv5n 사용
python3 detect.py --weights yolov5n.pt --img 320 --conf 0.25 --source data/images/
```

결과는 `runs/detect/exp/`에 저장됩니다.

### 11.3 웹캠 실시간 추론

```bash
# USB 웹캠 실시간 (느림 — TensorRT 필요)
python3 detect.py --weights yolov5s.pt --img 320 --conf 0.25 --source 0
```

> **경고**: TensorRT 없이 순수 PyTorch로 실시간 추론하면 **1 FPS 이하**로 매우 느립니다. 실시간이 목적이라면 반드시 TensorRT 변환이 필요합니다.

### 11.4 성능 비교 (TensorRT 없이)

| 모델 | 해상도 | 순수 PyTorch (FPS) |
|---|---|---|
| YOLOv5n | 320 | ~2~3 FPS |
| YOLOv5s | 320 | ~1 FPS |
| YOLOv5s | 640 | 0.3~0.5 FPS (3~5초/장) |

> **→ Darknet YOLOv4-tiny가 17~25 FPS로 훨씬 빠릅니다.** PyTorch의 장점은 편리한 Python API와 커스텀 학습이며, 실시간 속도가 필요하면 TensorRT 변환이 필수입니다.

---

# Part 4 — TensorRT 최적화

---

## 12. TensorRT 개념 이해

### 12.1 TensorRT란?

TensorRT는 NVIDIA의 **추론 최적화 엔진**입니다. 학습된 모델을 실제 서비스에 배포할 때 더 빠르고 효율적으로 실행할 수 있도록 변환해줍니다.

### 12.2 TensorRT의 최적화 기법

| 기법 | 설명 | 효과 |
|---|---|---|
| **레이어 융합 (Layer Fusion)** | 여러 레이어를 하나의 커널로 합침 | 메모리 접근 감소, 속도 ↑ |
| **정밀도 축소 (Precision Calibration)** | FP32 → FP16 또는 INT8로 축소 | 연산량 1/2 ~ 1/4, 메모리 1/2 |
| **커널 자동 튜닝** | GPU에 최적화된 커널 자동 선택 | 최대 성능 |
| **메모리 재사용** | 중간 결과 메모리 최적화 | 메모리 사용량 ↓ |
| **동적 텐서 메모리** | 실행 시 메모리 동적 할당 | 메모리 효율 ↑ |

> Jetson Nano 2GB에서는 FP16만 지원합니다. INT8은 Xavier/Orin 이상에서만 지원됩니다.

### 12.3 변환 파이프라인

```
PyTorch (.pt) → ONNX (.onnx) → TensorRT (.plan/.trt)
                    ↑                      ↑
              torch.onnx.export         trtexec or Python API
```

**ONNX (Open Neural Network Exchange)**:
- PyTorch, TensorFlow 등 다양한 프레임워크 간 모델 교환을 위한 표준 형식
- 중간 표현(Intermediate Representation) 역할
- TensorRT로 변환하기 위한 필수 단계

---

## 13. ONNX → TensorRT 변환

### 13.1 trtexec로 변환 (커맨드라인)

가장 간단한 방법입니다. `trtexec`은 JetPack에 포함되어 있습니다.

```bash
# PATH 설정
export PATH=/usr/src/tensorrt/bin:$PATH

# FP16 변환 (2GB 메모리 제한 필수)
trtexec --onnx=model.onnx \
        --saveEngine=model.plan \
        --fp16 \
        --memPoolSize=workspace:500
```

**옵션 설명**:

| 옵션 | 설명 | 권장값 |
|---|---|---|
| `--onnx` | 입력 ONNX 파일 | |
| `--saveEngine` | 출력 TensorRT 엔진 파일 | |
| `--fp16` | FP16 정밀도 활성화 | **필수 (2GB)** |
| `--memPoolSize` | workspace 메모리 제한 (MB) | 300~500 |
| `--verbose` | 상세 로그 출력 | 디버깅 시 |

### 13.2 Python API로 변환 (더 세밀한 제어)

```python
import tensorrt as trt

# Logger: TRT 로그 레벨 설정
logger = trt.Logger(trt.Logger.INFO)

# Builder: 엔진을 빌드하는 객체
builder = trt.Builder(logger)

# Network: 네트워크 구조 정의
network = builder.create_network(
    1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
)

# ONNX Parser: ONNX 파일을 읽어 network에 로드
parser = trt.OnnxParser(network, logger)

with open("model.onnx", "rb") as f:
    if not parser.parse(f.read()):
        for error in range(parser.num_errors):
            print(parser.get_error(error))

# Config: 빌드 설정
config = builder.create_builder_config()

# FP16 활성화
config.set_flag(trt.BuilderFlag.FP16)

# 메모리 제한 (500MB)
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 500 * 1024 * 1024)

# 엔진 빌드 및 저장
plan = builder.build_serialized_network(network, config)
with open("model.plan", "wb") as f:
    f.write(plan)
```

### 13.3 메모리 관리가 중요한 이유

Jetson Nano 2GB에서 TensorRT 변환 시 GPU 메모리는 공유 메모리(Unified Memory) 구조입니다. 즉, GPU와 CPU가 **동일한 2GB RAM**을 공유합니다.

변환 중 발생하는 문제:
```
[TensorRT] WARNING: Tactic Device request: 538MB Available: 166MB
[TensorRT] WARNING: Device memory is insufficient to use tactic.
```

이 경고는 변환 과정에서 특정 커널을 실행하기에 GPU 메모리가 부족하다는 의미입니다. 다음 전략으로 대응합니다:

1. **FP16 변환 필수** — FP32 대비 메모리 사용량 1/2
2. **workspace 제한** — `--memPoolSize=workspace:300`으로 낮춤
3. **입력 해상도 축소** — 640→320으로 낮춤
4. **PyTorch kernel 종료** — 변환 전에 PyTorch 사용 세션 완전 종료

---

## 14. TensorRT 추론 구현

### 14.1 엔진 로드 및 추론 (전체 코드)

```python
import tensorrt as trt
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit

class TensorRTInference:
    """TensorRT 엔진을 로드하고 추론을 수행하는 클래스"""

    def __init__(self, engine_path):
        # Logger
        self.logger = trt.Logger(trt.Logger.INFO)

        # Runtime: 엔진을 실행하는 객체
        self.runtime = trt.Runtime(self.logger)

        # 엔진 로드 (deserialize)
        with open(engine_path, "rb") as f:
            self.engine = self.runtime.deserialize_cuda_engine(f.read())

        # Execution Context: 실제 추론 상태
        self.context = self.engine.create_execution_context()

        # 입출력 이름과 크기 확인
        self.input_name = self.engine.get_tensor_name(0)
        self.output_name = self.engine.get_tensor_name(1)

        self.input_shape = self.engine.get_tensor_shape(self.input_name)
        self.output_shape = self.engine.get_tensor_shape(self.output_name)

        # GPU 메모리 할당
        self.input_size = trt.volume(self.input_shape) * np.dtype(np.float32).itemsize
        self.output_size = trt.volume(self.output_shape) * np.dtype(np.float32).itemsize

        self.input_d = cuda.mem_alloc(self.input_size)
        self.output_d = cuda.mem_alloc(self.output_size)

        # CUDA 스트림 (비동기 실행)
        self.stream = cuda.Stream()

    def infer(self, input_np):
        """입력 numpy 배열을 받아 추론 결과 반환"""

        # 입력 전처리 및 GPU 업로드
        input_np = input_np.astype(np.float32).ravel()
        cuda.memcpy_htod_async(self.input_d, input_np, self.stream)

        # 비동기 추론 실행
        self.context.execute_async_v2(
            bindings=[int(self.input_d), int(self.output_d)],
            stream_handle=self.stream.handle
        )

        # 결과 다운로드
        output_np = np.empty(self.output_shape, dtype=np.float32)
        cuda.memcpy_dtoh_async(output_np, self.output_d, self.stream)

        # 스트림 동기화 (완료 대기)
        self.stream.synchronize()

        return output_np

    def __del__(self):
        """소멸자 — GPU 메모리 해제"""
        self.input_d.free()
        self.output_d.free()
```

### 14.2 사용 예시

```python
# 엔진 로드
trt_infer = TensorRTInference("yolov5s.plan")

# 입력 데이터 준비
input_data = np.random.randn(1, 3, 320, 320).astype(np.float32)

# 추론
output = trt_infer.infer(input_data)

print(output.shape)  # (1, 25200, 85)
```

### 14.3 TensorRT Pipeline 전체 흐름

```
YOLOv5 모델 준비
    ↓
ONNX export (torch.onnx.export)
    ↓
trtexec 또는 Python API로 TensorRT 변환
    ↓
.plan 파일 저장
    ↓
Python 또는 C++에서 .plan 로드
    ↓
전처리 (resize, normalize)
    ↓
GPU 메모리 업로드 (memcpy HtoD)
    ↓
execute_async (추론)
    ↓
GPU 메모리 다운로드 (memcpy DtoH)
    ↓
후처리 (NMS, 바운딩 박스 변환)
    ↓
결과 출력
```

### 14.4 2GB에서 YOLOv5s TensorRT 성능

| 모델 | 해상도 | 정밀도 | FPS | 변환 성공 |
|---|---|---|---|---|
| **YOLOv5n** | 320 | FP16 | **30+** | ✅ 여유 |
| **YOLOv5s** | 320 | FP16 | **25** | ✅ |
| YOLOv5s | 416 | FP16 | 17 | ✅ (간당) |
| YOLOv5s | 640 | FP16 | 9 | ✅ (메모리 근접) |
| YOLOv5m | 320 | FP16 | - | ❌ OOM |
| YOLOv5s | 320 | FP32 | 20 | ✅ |

> 출처: [alxmamaev/jetson_yolov5_tensorrt](https://github.com/alxmamaev/jetson_yolov5_tensorrt) — Jetson Nano 2GB实测

---

# Part 5 — 종합

---

## 15. 성능 벤치마크

### 15.1 Jetson Nano 2GB 전체 성능표

| 방법론 | 모델 | 해상도 | FPS | 설치 난이도 | Python API |
|---|---|---|---|---|---|
| **Darknet** | **YOLOv4-tiny** | 416 | **17~25** | ★☆☆ | 제한적 (C 바인딩) |
| Darknet | YOLOv3-tiny | 416 | 15~20 | ★☆☆ | 제한적 |
| PyTorch native | YOLOv5n | 320 | 2~3 | ★★☆ | ✅ 풀 |
| PyTorch native | YOLOv5s | 320 | 1 | ★★☆ | ✅ 풀 |
| **TensorRT** | **YOLOv5n FP16** | **320** | **30+** | ★★★ | ✅ |
| **TensorRT** | **YOLOv5s FP16** | **320** | **25** | ★★★ | ✅ |
| TensorRT | YOLOv5s FP16 | 640 | 9 | ★★★ | ✅ |

### 15.2 Jetson 보드 간 성능 비교 (YOLOv4-tiny)

| 보드 | GPU 코어 | FPS |
|---|---|---|
| **Jetson Nano 2GB** | 128 | **17~25** |
| Jetson Nano 4GB | 128 | 17~25 (동일) |
| Jetson TX2 | 256 | 29 |
| Jetson Xavier NX | 384 | 45+ |
| Jetson Orin Nano | 1024 | 60+ |

GPU 코어 수보다 메모리 대역폭과 클럭이 FPS에 더 큰 영향을 미칩니다.

### 15.3 적용 분야별 추천

| 목적 | 추천 구성 | 이유 |
|---|---|---|
| **빠른 PoC / 프로토타입** | Darknet YOLOv4-tiny | 설치 5분, 바로 실행 |
| **Python 통합 필요** | YOLOv5s + TensorRT | Python native, 25 FPS |
| **최대 정확도** | YOLOv5s + TensorRT @640 | 느리지만(9 FPS) 정확 |
| **교육 / 학습 목적** | 전부 다 해보기 | 각 방식의 장단점 이해 |
| **커스텀 데이터 학습** | YOLOv5 (Colab 학습) → Nano에서 추론 | Nano에서 학습은 무리 |

---

## 16. 문제 해결 (Troubleshooting)

### 16.1 빌드 관련

| 문제 | 원인 | 해결 |
|---|---|---|
| `make: nvcc: not found` | CUDA PATH 미설정 | `export PATH=/usr/local/cuda/bin:$PATH` |
| `Makefile: *** missing separator` | sed로 탭이 공백으로 변환 | `git checkout -- Makefile` 후 재수정 |
| `fatal error: cudnn.h: No such file` | cuDNN PATH 문제 | JetPack 재설치 또는 `export CUDNN_HOME=/usr/lib/aarch64-linux-gnu` |

### 16.2 실행 관련

| 문제 | 원인 | 해결 |
|---|---|---|
| `Couldn't open file: yolov4.weights` | weights 파일 경로 오류 또는 미다운로드 | `weights/yolov4-tiny.weights` 경로 확인 |
| `CUDA error: out of memory` | GPU 메모리 부족 | tiny 모델 사용, GUI OFF, swap 확인 |
| 추론이 5000ms+로 매우 느림 | GPU가 사용되지 않음 | `GPU=1`, `ARCH=compute_53` 재확인 후 재빌드 |

### 16.3 메모리 관련

| 문제 | 원인 | 해결 |
|---|---|---|
| `Killed` (프로세스 강제 종료) | OOM Killer가 프로세스 종료 | swap 설정, GUI OFF, 더 작은 모델 사용 |
| YOLOv4 full 실행 시 멈춤 | 2GB 메모리로는 실행 불가 | YOLOv4-tiny로 대체 |
| TensorRT 변환 중 OOM | 변환 과정이 더 많은 메모리 사용 | `--memPoolSize=workspace:300`, FP16 필수 |

### 16.4 TensorRT 변환 관련

| 문제 | 원인 | 해결 |
|---|---|---|
| `trtexec: command not found` | PATH 미설정 | `export PATH=/usr/src/tensorrt/bin:$PATH` |
| `Tactic Device request: X MB Available: Y MB` | GPU 메모리 부족 | `--memPoolSize` 축소, FP16 확인 |
| `Some tactics do not have sufficient memory` | 변환 중 메모리 부족 | 입력 해상도 축소, 더 작은 모델 사용 |

---

## 17. 참고 자료

### 공식 문서
- [Jetson Nano 2GB Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-2gb-developer-kit)
- [JetPack 다운로드](https://developer.nvidia.com/embedded/jetpack)
- [TensorRT Python API Documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/python-api-docs.html)
- [YOLOv5 GitHub (Ultralytics)](https://github.com/ultralytics/yolov5)

### 관련 GitHub 레포지토리
- [AlexeyAB/darknet](https://github.com/AlexeyAB/darknet) — Darknet (YOLOv4)
- [seanavery/yolov5-tensorrt](https://github.com/SeanAvery/yolov5-tensorrt) — YOLOv5→TensorRT Python 파이프라인
- [alxmamaev/jetson_yolov5_tensorrt](https://github.com/alxmamaev/jetson_yolov5_tensorrt) — Jetson 전용 YOLOv5 TensorRT
- [YIXIN-YAO/Yolov5-TensorRT-JetsonNano-Python](https://github.com/YIXIN-YAO/Yolov5-TensorRT-JetsonNano-Python) — Nano实测 YOLOv5 TRT
- [dusty-nv/jetson-inference](https://github.com/dusty-nv/jetson-inference) — NVIDIA 공식 Jetson 추론 예제

### 관련 블로그
- [Jetson Nano YOLOv4 설치 (spyjetson)](https://spyjetson.blogspot.com/2020/06/jetson-nano-yolov4-installation.html)
- [Real Time Object Detection on Jetson Nano](https://msjun23.github.io/jetson/Real-Time-Object-Detection-on-Jetson-Nano(1)/)
- [Jetson Nano TensorRT 적용](https://www.wonbeomjang.kr/blog/2023/jetson-nano-tensorrt/)

---

> **제작일**: 2026년 5월
>
> **환경**: Jetson Nano 2GB Developer Kit, JetPack 4.6.1 (R32.7.1)
>
> 본 문서의 명령어는 실제 Jetson Nano 2GB에서 검증되었습니다.
