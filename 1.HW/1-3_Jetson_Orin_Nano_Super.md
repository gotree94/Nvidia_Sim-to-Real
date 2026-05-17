# NVIDIA Jetson Orin Nano Super Developer Kit

> **목차**
> 1. [개요](#1-개요)
> 2. ["Super" 업그레이드란?](#2-super-업그레이드란)
> 3. [하드웨어 상세 사양](#3-하드웨어-상세-사양)
> 4. [CPU 및 GPU 상세](#4-cpu-및-gpu-상세)
> 5. [메모리 및 스토리지](#5-메모리-및-스토리지)
> 6. [인터페이스 및 I/O](#6-인터페이스-및-io)
> 7. [개발자 키트 구성품](#7-개발자-키트-구성품)
> 8. [Orin Nano 모듈 비교 (4GB vs 8GB)](#8-orin-nano-모듈-비교-4gb-vs-8gb)
> 9. [초기화 및 셋업 방법](#9-초기화-및-셋업-방법)
> 10. [MAXN SUPER 모드 활성화](#10-maxn-super-모드-활성화)
> 11. [Force Recovery Mode 진입 방법](#11-force-recovery-mode-진입-방법)
> 12. [참고 자료](#12-참고-자료)

---

## 1. 개요

**Jetson Orin Nano Super Developer Kit**은 2024년 12월 NVIDIA가 발표한 엔트리 레벨 Gen AI 엣지 컴퓨팅 플랫폼이다. 기존 Jetson Orin Nano Developer Kit에 **소프트웨어 업데이트만으로** 1.7배의 AI 성능 향상을 제공한다. Ampere 아키텍처 GPU와 6코어 ARM CPU를 탑재하여 비전 트랜스포머, LLM, VLM 등 최신 생성형 AI 모델을 엣지에서 실행할 수 있다.

- **출시일**: 2024년 12월 (Super 업그레이드 발표)
- **SoC**: NVIDIA Orin (T234의 저전력 변형)
- **GPU**: NVIDIA Ampere 아키텍처, 1024 CUDA 코어, 32 Tensor 코어
- **CPU**: 6-core ARM Cortex-A78AE v8.2 64-bit
- **메모리**: 8GB 128-bit LPDDR5
- **AI 성능**: **67 INT8 TOPS** (Super 모드, 기존 40 TOPS 대비 1.7배↑)
- **메모리 대역폭**: **102 GB/s** (Super 모드, 기존 68 GB/s 대비 1.5배↑)
- **가격**: $249

---

## 2. "Super" 업그레이드란?

**Super**는 하드웨어 변경 없이 **소프트웨어/펌웨어 업데이트만으로** 성능이 향상된 것을 의미한다.

| 항목 | 일반 Orin Nano (JetPack 5.x) | Orin Nano Super (JetPack 6.x + Super) | 향상 |
|------|------------------------------|----------------------------------------|------|
| AI 성능 | 40 INT8 TOPS | **67 INT8 TOPS** | **1.7배 ↑** |
| GPU 클럭 | 625 MHz | ~1,020 MHz (추정) | 증가 |
| 메모리 대역폭 | 68 GB/s | **102 GB/s** | **1.5배 ↑** |
| CPU 클럭 | 1.5 GHz | **1.7 GHz** | ↑ |
| 전력 모드 | 7W / 15W | 7W / 15W / **25W (MAXN SUPER)** | 새 모드 |
| JetPack | 5.x | **6.x** | 필수 |
| 가격 | $249 (동일) | $249 (동일) | - |

> **즉, Jetson Orin Nano Developer Kit을 이미 가지고 있다면 JetPack 6.x를 설치하고 MAXN SUPER 모드를 활성화하는 것만으로 Super 성능을 얻을 수 있다.**

---

## 3. 하드웨어 상세 사양

### 종합 사양표

| 항목 | 사양 |
|------|------|
| **AI Performance** | 67 INT8 TOPS (Sparse) / 33 INT8 TOPS (Dense) |
| **GPU** | NVIDIA Ampere 아키텍처 |
| CUDA 코어 | 1,024개 |
| Tensor 코어 | 32개 (3세대) |
| GPU 최대 클럭 | 625 MHz (일반) ~ 약 1,020 MHz (Super) |
| **CPU** | 6-core Arm Cortex-A78AE v8.2 64-bit |
| CPU 클러스터 | 4-core 클러스터 (256KB L2/core + 2MB L3) + 2-core 클러스터 (256KB L2/core + 2MB L3) |
| 시스템 캐시 | 4MB (L3, 전체 클러스터 공유) |
| CPU 최대 클럭 | 1.5 GHz (일반) / **1.7 GHz (Super)** |
| **메모리** | 8GB 128-bit LPDDR5 |
| 메모리 대역폭 | 68 GB/s (일반) / **102 GB/s (Super)** |
| 메모리 클럭 | 2133 MHz → 3200 MHz (Super) |
| **스토리지** | microSD 슬롯 + 외부 NVMe SSD (M.2 Key M) |
| 전력 | 7W ~ 25W (MAXN SUPER 시) |
| 폼팩터 (모듈) | 69.6mm × 45mm, 260-pin SO-DIMM |
| 폼팩터 (키트) | 103mm × 90.5mm × 34.77mm |
| 온도 범위 | -25°C ~ 90°C (Tjunction) |

---

## 4. CPU 및 GPU 상세

### GPU: NVIDIA Ampere

| 항목 | 사양 |
|------|------|
| 아키텍처 | Ampere GA10B |
| CUDA 코어 | 1,024개 | 
| Tensor 코어 | 32개 (3세대) |
| Max 클럭 | 625 MHz (일반) → ~1,020 MHz (Super) |
| FP32 성능 | 약 2 TFLOPS (Super) |
| INT8 성능 | 67 TOPS (Sparse) / 33 TOPS (Dense) |
| API | CUDA 10, OpenGL 4.6, OpenGL ES 3.2, Vulkan 1.1 |
| 특징 | Lossless compression, Tile Caching |

> **Orin Nano 4GB 모듈**의 GPU는 절반인 **512 CUDA 코어 + 16 Tensor 코어**로 구성된다.

### CPU: ARM Cortex-A78AE

| 항목 | 사양 |
|------|------|
| 코어 | 8GB 모델: **6코어** / 4GB 모델: **6코어** (동일) |
| 아키텍처 | ARM v8.2 (64-bit) HMP |
| 클러스터 구성 | 4-core + 2-core (2개 클러스터) |
| L1 Cache | 128KB I-cache + 256KB D-cache per core (추정) |
| L2 Cache | 256KB per core |
| L3 Cache | 2MB per cluster (총 4MB) + 4MB 시스템 캐시 |
| Max 클럭 | 1.5 GHz (일반) → **1.7 GHz (Super)** |
| 특징 | Automotive Grade, Safety 기능 지원 |

---

## 5. 메모리 및 스토리지

### 메모리 (LPDDR5)

| 항목 | 일반 모드 | Super 모드 |
|------|----------|-----------|
| 용량 | 8GB | 8GB |
| 유형 | 128-bit LPDDR5 | 128-bit LPDDR5 |
| 주파수 | 2133 MHz | ~3200 MHz |
| 대역폭 | 68 GB/s | **102 GB/s** |
| ECC | 소프트웨어 지원 | 소프트웨어 지원 |

### 스토리지 옵션

| 옵션 | 인터페이스 | 속도 | 비고 |
|------|-----------|------|------|
| **microSD 카드** (기본) | SDMMC | UHS-1 | 기본 부트 미디어, 64GB 이상 권장 |
| **NVMe SSD (M.2 2280)** | PCIe 3.0 ×4 | ~3.5 GB/s | 권장, 10배 빠름 |
| **NVMe SSD (M.2 2230)** | PCIe 3.0 ×2 | ~1.8 GB/s | 소형 폼팩터 |
| **USB 드라이브** | USB 3.2 Gen2 | ~1 GB/s | 부팅 가능 |

> **NVMe SSD 권장**: microSD 대비 약 10배 빠른 I/O 성능으로 AI 워크로드에 큰 이점.

---

## 6. 인터페이스 및 I/O

### 개발자 키트 포트 구성

| 번호 | 포트 | 사양 |
|------|------|------|
| 1 | **microSD 카드 슬롯** | 기본 스토리지 (모듈 하단) |
| 2 | **40-pin 확장 헤더** | GPIO, UART, SPI, I2S, I2C |
| 3 | **전원 LED** | 녹색 LED |
| 4 | **USB-C 포트** | USB 3.2, Host/Device/Recovery 모드 (디스플레이 출력 불가) |
| 5 | **Gigabit Ethernet** | RJ45 |
| 6 | **USB 3.2 Gen2 Type-A (×4)** | 10 Gbps, 듀얼 스택 (각 스택 3A 제한) |
| 7 | **DisplayPort 출력** | DP 1.2 (+MST), **HDMI 미지원** (DP→HDMI 어댑터 필요) |
| 8 | **DC 전원 잭** | 5.5mm × 2.5mm, 9~20V 입력 (19V 어댑터 포함) |
| 9 | **MIPI CSI 카메라 커넥터 (×2)** | 22-pin, 0.5mm 피치, 2-lane/4-lane |
| 10 | **M.2 Key-M 슬롯 (2280)** | PCIe 3.0 ×4 (NVMe SSD) |
| 11 | **M.2 Key-M 슬롯 (2230)** | PCIe 3.0 ×2 (NVMe SSD) |
| 12 | **M.2 Key-E 슬롯 (2230)** | WiFi/BT (기본 장착됨) |

### 40-pin 확장 헤더 (J12)

| 핀 | 기능 | 핀 | 기능 |
|----|------|----|------|
| 1 | +3.3V | 2 | +5V |
| 3 | I2C1_SDA | 4 | +5V |
| 5 | I2C1_SCL | 6 | GND |
| 7 | GPIO13 | 8 | UART1_TXD |
| 9 | GND | 10 | UART1_RXD |
| 11 | UART1_RTS | 12 | GPIO8 |
| 13 | SPI1_SCK | 14 | GND |
| 15 | SPI1_MOSI | 16 | SPI1_MISO |
| 17 | SPI1_CS0 | 18 | SPI1_CS1 |
| 19 | SPI0_MOSI | 20 | GND |
| 21 | SPI0_MISO | 22 | SPI0_SCK |
| 23 | SPI0_CS0 | 24 | SPI0_CS1 |
| 25 | GND | 26 | GPIO18 |
| 27 | GPIO17 | 28 | GPIO16 |
| 29 | GPIO15 | 30 | GND |
| 31 | GPIO14 | 32 | GPIO12 |
| 33 | GPIO11 | 34 | GPIO10 |
| 35 | GPIO9 | 36 | GPIO7 |
| 37 | GPIO6 | 38 | GPIO5 |
| 39 | GPIO4 | 40 | GPIO3 |

### 비디오 코덱

| 항목 | 사양 |
|------|------|
| **비디오 디코드** | 1× 4K60 (H.265), 2× 4K30 (H.265), 5× 1080p60, 11× 1080p30 |
| **비디오 인코드** | 1080p30 (1-2 CPU 코어 사용, 하드웨어 인코더 제한적) |

---

## 7. 개발자 키트 구성품

| 구성품 | 설명 |
|--------|------|
| **Jetson Orin Nano 8GB 모듈** | Ampere GPU + 6-core CPU + 8GB LPDDR5 (방열판 포함) |
| **참조 캐리어 보드** | P3768-0000 |
| **DC 전원 공급기** | 19V 출력 |
| **무선 네트워크 카드** | M.2 Key-E 802.11ac/a/b/g/n (WiFi 5), Bluetooth |
| **빠른 시작 가이드** | 종이 매뉴얼 |

---

## 8. Orin Nano 모듈 비교 (4GB vs 8GB)

| 항목 | Orin Nano 4GB (P3767-0004) | Orin Nano 8GB (P3767-0003/0005) |
|------|---------------------------|--------------------------------|
| **GPU** | 512 CUDA + 16 Tensor 코어 | **1,024 CUDA + 32 Tensor 코어** |
| **CPU** | 6-core A78AE (동일) | 6-core A78AE (동일) |
| **메모리** | 4GB 64-bit LPDDR5 | **8GB 128-bit LPDDR5** |
| 메모리 대역폭 | 34 GB/s (일반) / 51 GB/s (Super) | 68 GB/s (일반) / **102 GB/s (Super)** |
| AI 성능 | 20 TOPS (일반) / 33 TOPS (Super) | 40 TOPS (일반) / **67 TOPS (Super)** |
| 전력 | 7W / 10W / 15W | 7W / 15W / **25W (MAXN SUPER)** |
| 파트 넘버 | P3767-0004 (4GB) | P3767-0003 (8GB), P3767-0005 (8GB v2) |

> **개발자 키트는 8GB 모듈(P3767-0005)과 함께 판매됨.**

---

## 9. 초기화 및 셋업 방법

Orin Nano Super는 두 가지 주요 설정 방법이 있다. **SDK Manager 방식이 가장 권장**된다 (펌웨어 + JetPack 한 번에, NVMe SSD 지원).

### 방법 1: SDK Manager 사용 (권장, Linux Host PC 필요)

#### 사전 요구사항

| 항목 | 요구사항 |
|------|---------|
| **Host PC** | x86_64, Ubuntu 22.04 또는 20.04 (Native 설치, VM/WSL 비권장) |
| **Host PC 저장공간** | 최소 25GB |
| **USB 케이블** | USB-C to USB-A/C |
| **스토리지** | microSD 64GB+ 또는 NVMe SSD 256GB+ (권장) |
| **점퍼 와이어** | Force Recovery 모드 진입용 |

#### Step 1: SDK Manager 설치 (Host PC)

```bash
# Ubuntu 22.04
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install sdkmanager

# 실행
sdkmanager
```

#### Step 2: NVMe SSD 장착 (선택, 권장)

1. Jetson Orin Nano Developer Kit을 뒤집기
2. 캐리어 보드 하단의 **M.2 Key-M (2280)** 슬롯에 NVMe SSD 삽입
3. 제공된 나사로 고정
4. 방열판이 있다면 함께 부착

#### Step 3: Force Recovery Mode 진입

1. 전원 OFF
2. USB-C 케이블로 Host PC와 연결
3. **모듈 아래 12-pin 헤더(J14)** 의 `FC REC`(핀 9)와 `GND`(핀 10)를 점퍼로 쇼트
4. DC 전원 연결 → 자동 부팅 → Recovery Mode 진입
5. Host PC에서 확인:

```bash
lsusb | grep -i nvidia
# 출력: Bus XXX Device XXX: ID 0955:7523 NVIDIA Corp. APX
```

#### Step 4: SDK Manager 플래싱

1. SDK Manager 실행 → NVIDIA 계정 로그인
2. **Step 01**:
   - Product Category: **Jetson**
   - Target Hardware: **Jetson Orin Nano Developer Kit** (8GB)
   - 필요시 "Host Machine" 체크 해제
   - Continue
3. **Step 02**:
   - JetPack 6.2 (또는 최신) 선택
   - **Jetson OS** 체크 (Jetson SDK Components는 나중에 설치 가능)
   - 라이선스 동의 → Continue
4. **Step 03**:
   - sudo 비밀번호 입력
   - 다운로드 및 이미지 생성 (수분 소요)
5. **플래싱 프롬프트**:
   - OEM Configuration: **Runtime** (첫 부팅 시 설정) 또는 **Pre-config**
   - Storage Device: **NVMe** 또는 **SD Card** 선택
   - **Flash** 클릭
   - 약 10~20분 소요 (NVMe가 SD 카드보다 빠름)

#### Step 5: 초기 부팅 및 설정

1. 플래싱 완료 후 **점퍼 제거**
2. 전원 코드 분리 후 재연결 (Power Cycle)
3. HDMI/DP 모니터, 키보드, 마우스 연결
4. 부팅 후 초기 설정:
   - EULA 동의
   - 언어 / 키보드 / 시간대 선택
   - WiFi 연결
   - 사용자 계정 생성
   - 로그인
5. SDK Manager로 돌아가서 Jetson SDK Components 설치 진행 (선택사항)

#### Step 6: Super 모드 활성화

초기 설정 완료 후 **MAXN SUPER 모드**를 활성화한다 (10장 참조).

---

### 방법 2: SD 카드 이미지 직접 기록 (Host PC 불필요)

Windows/Mac만 있어도 가능한 방법. 단, 펌웨어가 36.0 미만일 경우 추가 절차 필요.

#### Step 1: 펌웨어 버전 확인 (첫 부팅 시)

초기 상태의 Orin Nano는 UEFI 펌웨어 버전을 확인해야 한다:

- 터미널에서 확인: UEFI 부팅 화면에서 버전 확인
- 또는 JetPack 5.1.3으로 먼저 부팅 후 `sudo apt-get install nvidia-l4t-jetson-orin-nano-qspi-updater` 실행

#### Step 2: SD 카드 이미지 다운로드 및 기록

1. [NVIDIA JetPack SDK 페이지](https://developer.nvidia.com/embedded/jetpack)에서 최신 SD 카드 이미지 다운로드
2. [balenaEtcher](https://www.balena.io/etcher)로 SD 카드에 이미지 기록
3. SD 카드를 모듈 하단 슬롯에 삽입

#### Step 3: 펌웨어 업데이트 (필요 시)

QSPI 펌웨어가 최신이 아닌 경우 아래 순서로 업데이트:

**펌웨어 업데이트 플로우 (펌웨어 < 36.0인 경우):**
```
1. JetPack 5.1.3 SD 카드로 부팅
2. 초기 설정 완료
3. 재부팅 → 펌웨어 5.0으로 자동 업데이트
4. 터미널: sudo apt-get install nvidia-l4t-jetson-orin-nano-qspi-updater
5. 재부팅 → QSPI 업데이트 (펌웨어 36.4.0)
6. JetPack 6.x SD 카드로 교체 후 부팅
7. 재부팅 → 펌웨어 36.4.3으로 업데이트 (Super 준비 완료)
```

#### Step 4: 초기 설정

SD 카드 부팅 후 방법 1의 Step 5와 동일한 초기 설정 진행

---

## 10. MAXN SUPER 모드 활성화

Super 성능을 활성화하려면 JetPack 6.x 설치 후 MAXN SUPER 전력 모드로 전환해야 한다.

### nvpmodel로 확인 및 전환

```bash
# 현재 전력 모드 확인
sudo nvpmodel -q

# 사용 가능한 모든 모드 확인
sudo nvpmodel -p --verbose

# MAXN SUPER 모드로 전환 (모드 번호는 버전에 따라 다를 수 있음)
sudo nvpmodel -m MAXN_SUPER
# 또는
sudo nvpmodel -m 8  # 번호는 펌웨어에 따라 상이

# MAXN (일반) 모드로 전환
sudo nvpmodel -m MAXN

# 25W 모드
sudo nvpmodel -m 5

# 15W 모드
sudo nvpmodel -m 1

# 7W 모드
sudo nvpmodel -m 2
```

### 성능 확인

```bash
# GPU/CPU 클럭, 온도, 전력 모니터링
sudo tegrastats

# AI 성능 벤치마크 (jetson-inference 예제)
cd ~/jetson-inference/build/aarch64/bin
./imagenet.py --network=resnet-18 /dev/video0

# 메모리 대역폭 확인
sudo cat /sys/kernel/debug/bpmp/debug/clk/emc/rate
# Super 모드에서 3200000000 (3.2 GHz) 확인 가능
```

### 부팅 시 자동 적용

```bash
# MAXN SUPER를 기본 모드로 설정
sudo nvpmodel -m MAXN_SUPER
sudo nvpmodel -q  # 확인

# jetson_clocks로 최대 성능 고정 (선택사항)
sudo jetson_clocks
```

---

## 11. Force Recovery Mode 진입 방법

```
1. 전원 OFF (DC 전원 분리)
2. USB-C 케이블로 Host PC 연결
3. 모듈 아래 12-pin 버튼 헤더(J14) 찾기
4. FC REC 핀(pin 9)과 GND 핀(pin 10) 점퍼로 쇼트
5. DC 전원 연결 → 자동 전원 ON → Recovery Mode 진입
6. Host PC에서 lsusb 확인 (0955:7523 NVIDIA Corp. APX)
7. 플래싱 완료 후 점퍼 제거
```

### 12-pin 버튼 헤더 (J14) 핀맵

| 핀 | 신호 | 설명 |
|----|------|------|
| 1 | VDD_5V | 전원 LED + (Anode) |
| 2 | VDD_5V | 전원 LED - (Cathode) |
| 3 | UART2_RXD | 시리얼 콘솔 수신 |
| 4 | UART2_TXD | 시리얼 콘솔 송신 |
| 5 | LATCH_SET | Auto-Power-On 비활성화 (5-6 쇼트) |
| 6 | LATCH_SET_BTN | Auto-Power-On 비활성화 |
| 7 | GND | 접지 |
| 8 | RESET | 리셋 버튼 (7-8 쇼트) |
| 9 | GND | 접지 |
| 10 | **FC_REC** | **Force Recovery** (9-10 쇼트) |
| 11 | GND | 접지 |
| 12 | POWER_BTN | 전원 버튼 (11-12 쇼트) |

---

## 12. 참고 자료

- [NVIDIA Jetson Orin Nano Super Developer Kit 공식 페이지](https://nvidia.com/en-gb/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit)
- [Jetson Orin Nano Developer Kit Getting Started Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)
- [Jetson Orin Nano Developer Kit User Guide](https://developer.nvidia.com/embedded/learn/jetson-orin-nano-devkit-user-guide/index.html)
- [Jetson Orin Nano Series Datasheet (PDF)](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/5380/Jetson_Orin_Nano_Series_DS-11105-001_v1.1.pdf)
- [Orin Nano Super Datasheet (PDF)](https://digi-electronics.oss-us-west-1.aliyuncs.com/pdf/31567/JETSONORINNANOSUPERDEVKIT-datasheet.pdf)
- [NVIDIA JetPack SDK](https://developer.nvidia.com/embedded/jetpack)
- [SDK Manager Documentation](https://docs.nvidia.com/sdk-manager/)
- [Jetson AI Lab - Initial Setup Guide](https://www.jetson-ai-lab.com/tutorials/initial-setup-jetson-orin-nano/)
- [Jetson AI Lab - SDK Manager Setup Guide](https://www.jetson-ai-lab.com/tutorials/initial-setup-sdk-manager/)
- [NVIDIA Jetson Linux Developer Guide](https://docs.nvidia.com/jetson/l4t/)
