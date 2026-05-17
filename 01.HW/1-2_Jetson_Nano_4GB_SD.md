# NVIDIA Jetson Nano 4GB (Developer Kit, no eMMC)

> **목차**
> 1. [개요](#1-개요)
> 2. [파트 넘버와 보드 리비전](#2-파트-넘버와-보드-리비전)
> 3. [하드웨어 상세 사양](#3-하드웨어-상세-사양)
> 4. [CPU 및 GPU 상세](#4-cpu-및-gpu-상세)
> 5. [메모리 및 스토리지](#5-메모리-및-스토리지)
> 6. [인터페이스 및 I/O](#6-인터페이스-및-io)
> 7. [캐리어 보드 레이아웃](#7-캐리어-보드-레이아웃)
> 8. [eMMC 모델과의 차이점](#8-emmc-모델과의-차이점)
> 9. [초기화 및 셋업 방법](#9-초기화-및-셋업-방법)
> 10. [Force Recovery Mode 진입 방법](#10-force-recovery-mode-진입-방법)
> 11. [참고 자료](#11-참고-자료)

---

## 1. 개요

**Jetson Nano 4GB Developer Kit** (비 eMMC 버전)은 NVIDIA의 Maxwell 아키텍처 기반 엔트리 레벨 AI 컴퓨팅 모듈이다. 2019년 3월에 출시되었으며, microSD 카드를 주 저장장치 및 부트 미디어로 사용한다. 5W~10W의 초저전력으로 AI 추론이 가능하여 학습자, 메이커, 프로토타이핑에 최적화되어 있다.

- **SoC**: NVIDIA Tegra X1 (T210)
- **GPU**: 128-core Maxwell
- **CPU**: Quad-core ARM Cortex-A57
- **메모리**: 4GB LPDDR4
- **스토리지**: microSD 카드 (별도 구매) ← **내장 eMMC 없음**
- **부트 미디어**: QSPI-NOR + microSD 카드
- **AI 성능**: 472 GFLOPS (FP16)
- **출시 가격**: $99 (Developer Kit)

---

## 2. 파트 넘버와 보드 리비전

| 구분 | 파트 넘버 | 설명 |
|------|----------|------|
| **Jetson Nano 4GB 모듈** | P3448-0000 | SD 카드 기반 (eMMC 없음) |
| **Jetson Nano 4GB 모듈 (eMMC)** | P3448-0002 | 16GB eMMC 내장 (양산형) |
| **Jetson Nano 2GB 모듈** | P3448-0003 | 2GB RAM, SD 카드 기반 |
| **캐리어 보드 A02** | P3449-0000 A02 | 초기 리비전 (CSI 1개) |
| **캐리어 보드 B01** | P3449-0000 B01 | 후기 리비전 (CSI 2개, PoE 지원) |

> **현재 보유 모델**: Jetson Nano 4GB (P3448-0000) — 모듈에 eMMC가 없으며 microSD 카드로 부팅

### 보드 리비전 식별 방법

캐리어 보드의 보드 가장자리 또는 모듈 아래 PCB에 리비전이 인쇄되어 있다:
- **A02**: 초기 모델, 카메라 커넥터 1개, J40 버튼 헤더가 카메라 헤더 근처
- **B01**: 개선 모델, 카메라 커넥터 2개, J50 버튼 헤더가 보드 가장자리 (모듈 아래)

---

## 3. 하드웨어 상세 사양

### 종합 사양표

| 항목 | 사양 |
|------|------|
| **GPU** | NVIDIA Maxwell 아키텍처, 128 CUDA 코어 |
| GPU 최대 클럭 | 921 MHz |
| **CPU** | Quad-core ARM Cortex-A57 MPCore |
| CPU 최대 클럭 | 1.43 GHz |
| DL Accelerator | 없음 |
| Vision Accelerator | 없음 |
| **메모리** | 4GB 64-bit LPDDR4, 1600 MHz |
| 메모리 대역폭 | 25.6 GB/s |
| **스토리지** | microSD 카드 (별도 구매, 32GB UHS-1 이상 권장) |
| AI 성능 | 472 GFLOPS (FP16) |
| 전력 | 5W ~ 10W |
| 폼팩터 (모듈) | 69.6mm × 45mm, 260-pin SO-DIMM |
| 폼팩터 (개발자 키트) | 100mm × 80mm × 29mm |
| 무게 | 약 140g (모듈 + 방열판 + 캐리어 보드) |
| 온도 범위 | -25°C ~ 80°C (Tjunction) |

---

## 4. CPU 및 GPU 상세

### GPU: NVIDIA Maxwell

| 항목 | 사양 |
|------|------|
| 아키텍처 | Maxwell GM20B |
| CUDA 코어 | 128개 (1 Streaming Multiprocessor) |
| 최대 클럭 | 921 MHz |
| 성능 | 0.5 TFLOPS (FP16), 0.25 TFLOPS (FP32) |
| API | CUDA, OpenGL 4.6, OpenGL ES 3.2, Vulkan 1.0 |

### CPU: ARM Cortex-A57

| 항목 | 사양 |
|------|------|
| 코어 | Quad-core ARM Cortex-A57 |
| 아키텍처 | ARMv8-A (64-bit) |
| 최대 클럭 | 1.43 GHz |
| L1 Cache | 48KB I-cache + 32KB D-cache per core |
| L2 Cache | 2MB (공유) |

---

## 5. 메모리 및 스토리지

### 메모리 (LPDDR4)

| 항목 | 사양 |
|------|------|
| 용량 | 4GB |
| 버스 | 64-bit (1채널) |
| 유형 | LPDDR4 @ 1600 MHz |
| 대역폭 | 25.6 GB/s |

### 스토리지

| 항목 | 사양 |
|------|------|
| 주 저장장치 | **microSD 카드** (eMMC 없음) |
| 최소 용량 | 32GB UHS-1 권장 |
| QSPI-NOR | 부트로더 저장용 (내장, 약 32MB) |
| 부트 시퀀스 | QSPI-NOR → microSD 카드 |

### 권장 microSD 카드 사양

- **용량**: 32GB ~ 256GB
- **속도 등급**: UHS-1 U3 이상 (A1/A2 권장)
- **권장 브랜드**: Samsung EVO Plus, SanDisk Extreme Pro
- **주의**: 128GB 이상 카드는 일부 호환성 문제가 있을 수 있음

---

## 6. 인터페이스 및 I/O

### 개발자 키트 인터페이스

| 인터페이스 | 사양 |
|-----------|------|
| **USB** | 4× USB 3.0 Type-A (5 Gbps), 1× USB 2.0 Micro-B (Device/Recovery) |
| **디스플레이** | 1× HDMI 2.0, 1× DisplayPort 1.2 |
| **네트워크** | 1× Gigabit Ethernet (RJ45) |
| **무선** | M.2 Key E 슬롯 (WiFi/BT 카드 별도 구매) |
| **카메라** | 2× 15-pin MIPI CSI-2 (2-lane) — B01 기준 |
| **확장** | 40-pin 헤더 (GPIO, I2C, I2S, SPI, UART, PWM) |
| **기타** | 12-pin 오토메이션 헤더, 4-pin 팬 헤더, PoE 헤더 (B01) |
| **스토리지 확장** | M.2 Key E (PCIe ×1, USB 2.0, UART, I2S, I2C) |

### 40-pin 확장 헤더 (J6) 핀맵

| 핀 | 기능 | 핀 | 기능 |
|----|------|----|------|
| 1 | +3.3V | 2 | +5V |
| 3 | I2C0_SDA | 4 | +5V |
| 5 | I2C0_SCL | 6 | GND |
| 7 | GPIO216 (J4) | 8 | UART1_TXD |
| 9 | GND | 10 | UART1_RXD |
| 11 | UART1_RTS | 12 | I2S0_FS |
| 13 | SPI1_SCK | 14 | GND |
| 15 | SPI1_MOSI | 16 | SPI1_MISO |
| 17 | SPI1_CS0 | 18 | SPI1_CS1 |
| 19 | SPI0_MOSI | 20 | GND |
| 21 | SPI0_MISO | 22 | SPI0_SCK |
| 23 | SPI0_CS0 | 24 | SPI0_CS1 |
| 25 | GND | 26 | SPI0_CS2 |
| 27 | I2S0_SDIN | 28 | I2S0_LRCK |
| 29 | I2S0_BCLK | 30 | GND |
| 31 | I2S0_SDOUT | 32 | GPIO257 |
| 33 | GPIO259 | 34 | GPIO260 |
| 35 | GPIO269 | 36 | GPIO268 |
| 37 | GPIO267 (SPI2_CS1) | 38 | GPIO266 |
| 39 | GPIO258 | 40 | GPIO270 |

> **참고**: 모든 신호는 3.3V 레벨, 기본값은 GPIO 모드 (I2C, UART 제외)

---

## 7. 캐리어 보드 레이아웃

### A02 리비전 주요 커넥터

| 위치 | 커넥터 | 설명 |
|------|--------|------|
| J1 | SO-DIMM 소켓 | Jetson Nano 모듈 |
| J25 | DC 전원 잭 | 5V/4A 배럴 커넥터 |
| J48 | 점퍼 헤더 | DC 전원 활성화 점퍼 |
| J40 | 버튼 헤더 | 초기 리비전, FRC 핀 (3: FC REC, 4: GND) |
| - | microSD 슬롯 | 모듈 하단 |
| - | HDMI | 디스플레이 출력 |
| - | USB 3.0 (×4) | Type-A |
| - | USB Micro-B | 리커버리/디바이스 모드 |
| - | RJ45 | Gigabit Ethernet |
| - | CSI 커넥터 | 1개 (15-pin) |

### B01 리비전 주요 커넥터

| 위치 | 커넥터 | 설명 |
|------|--------|------|
| J1 | SO-DIMM 소켓 | Jetson Nano 모듈 (리비전 무관) |
| J25 | DC 전원 잭 | 5V/4A 배럴 커넥터 |
| J48 | 점퍼 헤더 | DC 전원 활성화 점퍼 |
| J50 | 버튼 헤더 | B01 리비전 (핀 9: GND, 핀 10: FC REC) |
| J5 | PoE 헤더 | PoE 모듈 지원 (4-pin) |
| - | microSD 슬롯 | 모듈 하단 |
| - | HDMI | 디스플레이 출력 |
| - | USB 3.0 (×4) | Type-A |
| - | USB Micro-B | 리커버리/디바이스 모드 |
| - | RJ45 | Gigabit Ethernet |
| - | CSI 커넥터 | **2개** (15-pin) |

---

## 8. eMMC 모델과의 차이점

| 항목 | SD 카드 버전 (P3448-0000) | eMMC 버전 (P3448-0002) |
|------|--------------------------|------------------------|
| **파트 넘버** | P3448-0000 | P3448-0002 |
| **내장 스토리지** | 없음 (microSD 전용) | 16GB eMMC 5.1 |
| **소비자 대상** | 개발자 키트, 학습용 | 양산형 (Production Module) |
| **부트 미디어** | QSPI-NOR → microSD | QSPI-NOR → eMMC |
| **SD 카드 슬롯** | 모듈에 내장 | 없음 (캐리어 보드 확장 필요) |
| **플래싱 방법** | SD 카드 이미지 직접 기록 | SDK Manager로 eMMC 플래싱 |
| **JetPack 설정** | `jetson-nano-devkit` | `jetson-nano-devkit-emmc` |
| **L4T flash 명령어** | `flash.sh jetson-nano-qspi-sd mmcblk0p1` | `flash.sh jetson-nano-devkit-emmc mmcblk0p1` |
| **가격** | $99 (개발자 키트) | $129 (모듈 단가) |

---

## 9. 초기화 및 셋업 방법

Jetson Nano 4GB (SD 카드 버전)의 초기화는 두 가지 방법이 있다:

### 방법 1: SD 카드 이미지 직접 기록 (간편, 권장)

별도의 Linux 호스트 PC 없이 Windows/Mac에서도 가능한 가장 간단한 방법.

#### Step 1: SD 카드 이미지 다운로드

1. [NVIDIA JetPack SDK 페이지](https://developer.nvidia.com/embedded/jetpack-archive) 접속
2. Jetson Nano 호환 JetPack 버전 선택 (4.6.2 권장)
3. **Jetson Nano Developer Kit SD Card Image** 다운로드
4. 파일명 예: `jetson_nano_devkit_sd_card.zip`

#### Step 2: SD 카드에 이미지 쓰기

**Windows/Mac/Linux 공통 — balenaEtcher 사용:**

1. [balenaEtcher](https://www.balena.io/etcher) 다운로드 및 설치
2. SD 카드 (32GB 이상 UHS-1 권장)를 PC에 연결
3. Etcher 실행:
   - **Flash from file**: 다운로드한 zip 파일 선택
   - **Select target**: SD 카드 선택
   - **Flash!**: 클릭하여 기록 시작 (약 10~15분 소요)
4. 완료 후 SD 카드 제거 (Windows에서 "읽을 수 없음" 메시지는 무시)

**Linux 명령줄 (선택사항):**

```bash
# SD 카드 장치 확인 (예: /dev/sdX)
lsblk

# 이미지 기록
/usr/bin/unzip -p ~/Downloads/jetson_nano_devkit_sd_card.zip | \
    sudo dd of=/dev/sdX bs=1M status=progress
```

#### Step 3: SD 카드 삽입 및 부팅

1. microSD 카드를 Jetson Nano 모듈 하단의 슬롯에 삽입
2. HDMI 디스플레이 연결
3. USB 키보드/마우스 연결
4. **전원 연결 방법 (택 1)**:
   - **DC 배럴 잭**: 5V/4A 어댑터 사용 (J48 점퍼 필요)
   - **Micro-USB**: 5V/2A 어댑터 사용 (전력 제한, 부하가 큰 작업 비권장)

> **전원 공급 시 J48 점퍼 (A02/B01 공통)**:
> DC 배럴 잭으로 전원을 공급하려면 J48 핀을 점퍼로 쇼트시켜야 한다.
> (J48 위치는 캐리어 보드 상 각 리비전에 따라 다름)

#### Step 4: 초기 설정 (First Boot)

첫 부팅 시 아래 과정이 순서대로 진행된다:

1. **NVIDIA Jetson EULA** 동의
2. **시스템 언어** 선택
3. **키보드 레이아웃** 선택
4. **시간대** 선택 (Asia/Seoul 등)
5. **사용자 계정 생성** (username / password)
6. **컴퓨터 이름** 설정
7. 로그인

#### Step 5: 시스템 확인

```bash
# JetPack 버전 확인
cat /etc/nv_tegra_release

# CUDA 버전 확인
nvcc --version

# GPU 상태 확인
sudo tegrastats

# 메모리 정보 확인
free -h

# 디스크 확인
df -h
```

---

### 방법 2: SDK Manager로 QSPI-NOR + SD 카드 플래싱

Linux 호스트 PC가 있을 경우 SDK Manager를 사용해 QSPI 부트로더와 SD 카드를 함께 플래싱할 수 있다.

#### Step 1: Host PC 준비 (Ubuntu 18.04 이상)

```bash
# SDK Manager 설치
sudo apt install ./sdkmanager_[version]-[build#]_amd64.deb
```

#### Step 2: 하드웨어 연결

1. microSD 카드를 모듈에 먼저 삽입 (16GB 이상)
2. USB Micro-B 케이블로 Host PC와 연결
3. 전원 연결 전 Force Recovery 모드로 설정

#### Step 3: Force Recovery Mode 진입

**A02 리비전:**
1. 전원 OFF 상태 확인
2. J40 헤더의 핀 3(FC REC)과 핀 4(GND)를 점퍼로 쇼트
3. J48 점퍼 쇼트 (DC 전원 활성화)
4. DC 전원 연결 → 자동 전원 ON → Force Recovery 모드 진입
5. J40 점퍼 제거

**B01 리비전:**
1. 전원 OFF 상태 확인
2. J50 헤더의 핀 9(GND)과 핀 10(FC REC)를 점퍼로 쇼트
3. J48 점퍼 쇼트 (DC 전원 활성화)
4. DC 전원 연결 → 자동 전원 ON → Force Recovery 모드 진입
5. J50 점퍼 제거

#### Step 4: SDK Manager 플래싱

1. SDK Manager 실행 → NVIDIA 계정 로그인
2. Product: Jetson, Target: Jetson Nano Developer Kit
3. JetPack 버전 선택
4. 'Jetson OS' 체크 (Jetson SDK Components는 선택)
5. 플래싱 옵션: **Pre-config** 또는 **Runtime** 선택
6. **Flash** 클릭
7. 완료 후 자동 재부팅

---

### 방법 3: SD 카드 이미지 직접 부팅 (초간편, 팩토리 상태)

NVIDIA에서 제공하는 **사전 준비된 SD 카드 이미지**를 사용하는 방법:

```
1. microSD 카드 (최소 32GB) 준비
2. NVIDIA JetPack SDK 페이지에서 SD 카드 이미지 다운로드
   https://developer.nvidia.com/embedded/jetpack
3. balenaEtcher로 SD 카드에 이미지 기록
4. SD 카드를 Jetson Nano 모듈에 삽입
5. HDMI, 키보드, 마우스 연결
6. DC 전원 연결 (J48 점퍼 필요)
7. 자동 부팅 및 초기 설정 진행
```

> **가장 빠르고 간단한 방법** — 추가 도구 없이 Windows/Mac에서도 가능.

---

## 10. Force Recovery Mode 진입 방법

### A02 리비전

```
1. 전원 OFF
2. USB Micro-B 케이블로 Host PC 연결
3. J40 핀 3(FC REC)과 핀 4(GND) 점퍼 쇼트
4. J48 점퍼 쇼트
5. DC 전원 연결 → 자동 부팅 → Recovery Mode 진입
6. J40 점퍼 제거
```

### B01 리비전

```
1. 전원 OFF
2. USB Micro-B 케이블로 Host PC 연결
3. 캐리어 보드 가장자리 J50 헤더에 점퍼 연결
   - 핀 9 (GND) ←→ 핀 10 (FC REC)
4. J48 점퍼 쇼트
5. DC 전원 연결 → 자동 부팅 → Recovery Mode 진입
6. J50 점퍼 제거
```

### 검증 명령어 (Host PC)

```bash
# Linux Host PC에서 확인
lsusb | grep -i nvidia
# 출력: Bus XXX Device XXX: ID 0955:7f21 NVIDIA Corp. APX
```

---

## 11. 참고 자료

- [NVIDIA Jetson Nano Developer Page](https://developer.nvidia.com/embedded/jetson-nano)
- [Jetson Nano Developer Kit Getting Started Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write)
- [NVIDIA JetPack SDK Archive](https://developer.nvidia.com/embedded/jetpack-archive)
- [Jetson Nano Datasheet (PDF)](https://cdn.sparkfun.com/assets/0/7/f/9/d/jetson-nano-devkit-datasheet-updates-us-v3.pdf)
- [NVIDIA Jetson Linux Developer Guide](https://docs.nvidia.com/jetson/l4t/)
- [Jetson Nano Developer Kit User Guide (2GB)](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide)
- [Jetson Nano Forums](https://forums.developer.nvidia.com/c/agx-autonomous-machines/jetson-embedded-systems/jetson-nano/70)
- [balenaEtcher](https://www.balena.io/etcher)
