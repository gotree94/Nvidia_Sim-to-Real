# NVIDIA Jetson TX2 Series

> **목차**
> 1. [개요](#1-개요)
> 2. [TX2 시리즈 변종](#2-tx2-시리즈-변종)
> 3. [하드웨어 상세 사양](#3-하드웨어-상세-사양)
> 4. [CPU 아키텍처 상세](#4-cpu-아키텍처-상세)
> 5. [메모리 및 스토리지](#5-메모리-및-스토리지)
> 6. [인터페이스 및 I/O](#6-인터페이스-및-io)
> 7. [개발자 키트 (Developer Kit) 구성](#7-개발자-키트-developer-kit-구성)
> 8. [초기화 및 셋업 방법](#8-초기화-및-셋업-방법)
> 9. [Force Recovery Mode 진입 방법](#9-force-recovery-mode-진입-방법)
> 10. [참고 자료](#10-참고-자료)

---

## 1. 개요

**Jetson TX2**는 NVIDIA의 Pascal 아키텍처 기반 임베디드 AI 컴퓨팅 모듈로, 2017년 3월에 출시되었다. 7.5W~15W의 저전력으로 서버급 AI 컴퓨팅 성능을 엣지 디바이스에서 제공한다. 16nm FinFET 공정의 NVIDIA Tegra "Parker" SoC를 기반으로 한다.

- **출시일**: 2017년 3월
- **SoC**: NVIDIA Tegra "Parker" (16nm FinFET)
- **폼팩터**: 50mm × 87mm (모듈), 260-pin / 400-pin SO-DIMM 커넥터
- **AI 성능**: 1.33 TFLOPS (FP16)

---

## 2. TX2 시리즈 변종

TX2 시리즈는 총 4가지 모듈 변종이 존재한다:

<table style="font-size: 0.85em; white-space: nowrap;">
  <thead>
    <tr>
      <th>모델</th>
      <th>GPU 클럭</th>
      <th>메모리</th>
      <th>스토리지</th>
      <th>전력</th>
      <th>폼팩터</th>
      <th>특징</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Jetson TX2</b></td>
      <td>1.30 GHz</td>
      <td>8GB LPDDR4 (128bit)<br>59.7GB/s</td>
      <td>32GB eMMC 5.1</td>
      <td>7.5W / 15W</td>
      <td>50×87mm<br>400-pin</td>
      <td>WLAN/BT 내장</td>
    </tr>
    <tr>
      <td><b>Jetson TX2i</b></td>
      <td>1.12 GHz</td>
      <td>8GB LPDDR4 (128bit)<br>51.2GB/s</td>
      <td>32GB eMMC 5.1</td>
      <td>10W / 20W</td>
      <td>50×87mm<br>400-pin</td>
      <td>산업용, ECC 지원</td>
    </tr>
    <tr>
      <td><b>Jetson TX2 4GB</b></td>
      <td>1.12 GHz</td>
      <td>4GB LPDDR4 (128bit)<br>51.2GB/s</td>
      <td>16GB eMMC 5.1</td>
      <td>7.5W / 15W</td>
      <td>50×87mm<br>400-pin</td>
      <td>보급형</td>
    </tr>
    <tr>
      <td><b>Jetson TX2 NX</b></td>
      <td>1.30 GHz</td>
      <td>8GB LPDDR4 (128bit)<br>59.7GB/s</td>
      <td>16GB eMMC 5.1</td>
      <td>7.5W / 15W</td>
      <td>69.6×45mm<br>260-pin</td>
      <td>Nano 크기 폼팩터</td>
    </tr>
  </tbody>
</table>

> **참고**: 일반적으로 "Jetson TX2"라 하면 8GB 메모리 + 32GB eMMC 모델을 가리킨다.

---

## 3. 하드웨어 상세 사양

### GPU

| 항목 | 사양 |
|------|------|
| 아키텍처 | NVIDIA Pascal |
| CUDA 코어 | 256개 (2 Streaming Multiprocessors × 128 CUDA cores) |
| 최대 클럭 | 1.30 GHz (TX2) / 1.12 GHz (TX2i, TX2 4GB) |
| API 지원 | CUDA 9.0, OpenGL 4.6, OpenGL ES 3.2, Vulkan 1.0 |
| 특징 | End-to-end lossless compression, Tile Caching |

### CPU

| 항목 | 사양 |
|------|------|
| 아키텍처 | ARMv8 (64-bit) HMP (Heterogeneous Multi-Processing) |
| 클러스터 1 | **NVIDIA Denver 2** (Dual-Core) - 고단일 스레드 성능 |
|  | L1 I-Cache: 128KB/core, L1 D-Cache: 64KB/core, L2: 2MB |
|  | 최대 클럭: 2.0 GHz (TX2) / 1.95 GHz (TX2i) |
| 클러스터 2 | **ARM Cortex-A57** (Quad-Core) - 멀티스레드/경량 작업 |
|  | L1 I-Cache: 48KB/core, L1 D-Cache: 32KB/core, L2: 2MB |
|  | 최대 클럭: 2.0 GHz (TX2) / 1.92 GHz (TX2i) |
| 총 코어 | 6코어 (2 + 4) |

### 메모리

| 항목 | TX2 | TX2i | TX2 4GB |
|------|-----|------|---------|
| 용량 | 8GB | 8GB | 4GB |
| 유형 | 128-bit LPDDR4 | 128-bit LPDDR4 (ECC) | 128-bit LPDDR4 |
| 채널 | 4ch × 32-bit | 4ch × 32-bit | 4ch × 32-bit |
| 최대 주파수 | 1866 MHz | 1600 MHz | 1600 MHz |
| 대역폭 | 59.7 GB/s | 51.2 GB/s | 51.2 GB/s |

### 스토리지

| 항목 | 사양 |
|------|------|
| 유형 | eMMC 5.1 |
| 버스 | 8-bit |
| 최대 주파수 | 200 MHz (HS400) |
| 용량 | 32GB (TX2, TX2i) / 16GB (TX2 4GB, TX2 NX) |

### 비디오

| 항목 | 사양 |
|------|------|
| 비디오 인코딩 | 1× 4K60 (H.265), 3× 4K30 (H.265), 4× 1080p60, 8× 1080p30 |
| 비디오 디코딩 | 2× 4K60 (H.265), 7× 1080p60, 14× 1080p30 |
| ISP | 1.4 Gpix/s, 12 lanes MIPI CSI-2, D-PHY 1.2 (2.5 Gbps/lane) |

---

## 4. CPU 아키텍처 상세

TX2의 HMP(Heterogeneous Multi-Processing) 아키텍처는 두 개의 CPU 클러스터가 고성능 코히어런트 인터커넥트로 연결된 구조:

```
┌─────────────────────────┐     ┌─────────────────────────┐
│   Denver 2 Cluster      │     │   Cortex-A57 Cluster    │
│   (고성능, 고전력)       │     │   (고효율, 저전력)       │
├─────────────────────────┤     ├─────────────────────────┤
│ Core 0: Denver 2 @ 2GHz │     │ Core 0: A57 @ 2GHz      │
│ Core 1: Denver 2 @ 2GHz │     │ Core 1: A57 @ 2GHz      │
│ L1 I/D: 128KB/64KB      │     │ Core 2: A57 @ 2GHz      │
│ L2: 2MB                 │     │ Core 3: A57 @ 2GHz      │
│                         │     │ L1 I/D: 48KB/32KB       │
│                         │     │ L2: 2MB                 │
└─────────────────────────┘     └─────────────────────────┘
         │                              │
         └────────── Coherent Interconnect ──────────┘
```

- **Denver 2**: 7-way superscalar, 동적 코드 최적화(DCO) 지원
- **Cortex-A57**: 일반 ARMv8-A, 순차적 및 병렬 부하에 적합
- **nvpmodel** 도구로 실행 중에 클러스터 구성을 전환 가능:
  - **Max-Q** (7.5W): GPU 854MHz, A57 1.2GHz - 최고 전력 효율
  - **Max-P** (15W): GPU 1.3GHz, Denver 2 2.0GHz - 최고 성능

---

## 5. 메모리 및 스토리지

- **LPDDR4**: 128-bit 인터페이스, 4채널 구현, 최대 59.7GB/s 대역폭
- **eMMC 5.1**: 8-bit 버스, HS400 모드 (200MHz)
- **SD 카드**: 외부 SD/MMC 컨트롤러 지원 (SD 4.0, SDIO 3.0)
- **SATA**: 1포트 지원 (외부 스토리지 연결 가능)

---

## 6. 인터페이스 및 I/O

### 주요 인터페이스

| 인터페이스 | TX2 | TX2i / TX2 4GB |
|-----------|-----|----------------|
| USB 3.0 | 최대 3포트 | 1포트 |
| USB 2.0 | 최대 3포트 | 3포트 |
| PCIe | Gen2, 1×4 + 1×1 또는 2×1 + 1×2 | Gen2, 1×1 + 1×2 |
| SATA | 1포트 | - |
| GbE | 1× Gigabit Ethernet | 1× Gigabit Ethernet |
| CSI Camera | 최대 6대 (12 lanes MIPI CSI-2) | 최대 5대 |
| 디스플레이 | 2× DP 1.2/eDP 1.4/HDMI 2.0, 2× 4-lane DSI | 2× DP/eDP/HDMI, 1× 2-lane DSI |
| UART | 5 | 3 |
| SPI | 3 | 2 |
| I2C | 8 | 4 |
| I2S | 4 | 4 |
| CAN | 2 | 1 |
| GPIO | 다수 | 다수 |

### 무선 연결 (TX2 모델만 해당)

- **WiFi**: 802.11a/b/g/n/ac 2×2 MIMO (최대 867 Mbps)
- **Bluetooth**: 4.1
- **안테나**: 2개 (U.FL 커넥터)

---

## 7. 개발자 키트 (Developer Kit) 구성

개발자 키트에는 다음 구성품이 포함된다:

| 구성품 | 설명 |
|--------|------|
| Jetson TX2 모듈 | Pascal GPU + 8GB LPDDR4 + 32GB eMMC (히트싱크/팬 포함) |
| 캐리어 보드 | Mini-ITX 폼팩터 (170mm × 170mm) |
| AC 어댑터 | 19V DC 출력 |
| USB 케이블 | Micro-B to USB A (플래싱용) |
| USB 케이블 | Micro-B to Female USB A |
| 안테나 | WiFi/BT 안테나 2개 |
| 고무 받침 | 4개 |

### 캐리어 보드 인터페이스

- USB 3.0 Type A
- USB 2.0 Micro AB (리커버리/호스트 모드)
- HDMI 2.0
- M.2 Key E (WiFi/BT)
- PCIe ×4 슬롯
- Gigabit Ethernet (RJ45)
- Full-size SD 카드 슬롯
- SATA 데이터 + 전원
- 40-pin 확장 헤더 (GPIO, I2C, I2S, SPI, CAN)
- 30-pin 확장 헤더
- 디스플레이 확장 헤더
- 카메라 확장 헤더
- TTL UART (플로우 컨트롤 포함)
- 전원/리셋/리커버리/사용자 버튼

---

## 8. 초기화 및 셋업 방법

TX2 개발자 키트 초기 설정은 **SDK Manager**를 사용하는 표준 방법을 따른다.

### 사전 요구사항 (Host PC)

| 항목 | 요구사항 |
|------|---------|
| OS | Ubuntu Linux x64 18.04 또는 20.04 (Native 설치, VM 권장하지 않음) |
| NVIDIA 계정 | NVIDIA Developer Program 가입 필요 |
| 저장공간 | 최소 25GB 여유 공간 |
| 인터넷 | 다운로드 및 설치 필요 |

### 방법 1: SDK Manager를 통한 표준 플래싱 (권장)

#### Step 1: SDK Manager 설치 (Host PC)

```bash
# SDK Manager 다운로드 (NVIDIA Developer 웹사이트에서 deb 패키지 다운로드)
# https://developer.nvidia.com/sdk-manager

# 설치
sudo apt install ./sdkmanager_[version]-[build#]_amd64.deb

# 실행
sdkmanager
```

#### Step 2: 하드웨어 연결

1. **HDMI 디스플레이**를 캐리어 보드 HDMI 포트에 연결 (선택사항)
2. **USB 키보드/마우스** 연결 (USB 허브 사용 권장)
3. **USB Micro-B 케이블**로 Host PC와 연결 (캐리어 보드의 Micro-AB 포트 사용)
4. **전원 어댑터(19V)** 연결

#### Step 3: Force Recovery Mode 진입

1. 장치 전원이 **꺼진 상태**인지 확인
2. **Force Recovery 버튼**을 누른 상태로 유지
3. **Power 버튼**을 누른 상태로 유지
4. **Power 버튼 먼저 해제**, 이어서 Force Recovery 버튼 해제
5. Host PC에서 `lsusb` 실행 시 `NVIDIA Corp. (ID 0955:7c18)` 확인

```bash
# Host PC에서 확인
lsusb | grep NVIDIA
# 출력: Bus XXX Device XXX: ID 0955:7c18 NVIDIA Corp. APX
```

#### Step 4: SDK Manager 플래싱

1. SDK Manager 실행 → NVIDIA 계정 로그인
2. Product Category: **Jetson** 선택
3. Target Hardware: **Jetson TX2 Developer Kit** 선택
4. SDK Version: 원하는 JetPack 버전 선택
5. Components: 필요 컴포넌트 선택 (Jetson OS + Jetson SDK Components)
6. 라이선스 동의 후 Continue
7. sudo 비밀번호 입력
8. 플래싱 프롬프트에서 **Manual Setup - Jetson TX2** 선택
9. 플래싱 완료 후 시스템 자동 재부팅

#### Step 5: 초기 설정 (First Boot)

재부팅 후 HDMI에 연결된 디스플레이에 초기 설정 화면이 표시된다:

1. **NVIDIA Jetson 소프트웨어 EULA** 검토 및 동의
2. **시스템 언어** 선택
3. **키보드 레이아웃** 선택
4. **시간대** 선택
5. **사용자 이름/비밀번호** 생성
6. **컴퓨터 이름** 설정
7. 로그인

> **Headless 설정**: 디스플레이가 없는 경우 시리얼 콘솔(putty 등)을 통해 Host PC에서 초기 설정을 진행해야 한다.

---

### 방법 2: 명령줄 플래싱 (L4T BSP 직접)

SDK Manager 없이 직접 L4T BSP를 사용하여 플래싱할 수도 있다:

```bash
# 1. L4T 릴리스 패키지 다운로드
# https://developer.nvidia.com/linux-tegra

# 2. 압축 해제 및 rootfs 조립
tar xf ${L4T_RELEASE_PACKAGE}
cd Linux_for_Tegra/rootfs/
sudo tar xpf ../../${SAMPLE_FS_PACKAGE}
cd ..
sudo ./apply_binaries.sh

# 3. Force Recovery Mode 진입 (위 방법 참조)

# 4. eMMC로 플래싱
sudo ./flash.sh jetson-tx2 mmcblk0p1

# 5. SD 카드로 플래싱 (루트 파일시스템만)
sudo ./flash.sh mmcblk1p1
```

---

### JetPack 버전 히스토리 (TX2 호환)

| JetPack | L4T | CUDA | 출시일 | 비고 |
|---------|-----|------|--------|------|
| 4.6.2 | R32.7.3 | 10.2 | 2022 | 최종 안정화 버전 |
| 4.6.1 | R32.7.2 | 10.2 | 2022 | |
| 4.6 | R32.7.1 | 10.2 | 2021 | |
| 4.5.1 | R32.6.1 | 10.2 | 2021 | |
| 4.4.1 | R32.5.2 | 10.2 | 2020 | |
| 4.3 | R32.4.3 | 10.0 | 2020 | |
| 4.2.3 | R32.2.3 | 10.0 | 2019 | |
| 4.2 | R32.2.2 | 10.0 | 2019 | |
| 3.3 | R28.2.1 | 9.0 | 2018 | 초기 버전 |
| 3.0 | R28.1 | 8.0 | 2017 | TX2 출시 버전 |

---

## 9. Force Recovery Mode 진입 방법

### 표준 방법 (버튼 사용)

```
1. 장치 전원 OFF
2. USB Micro-B 케이블 연결 (Host PC ↔ TX2)
3. 전원 어댑터 연결
4. Force Recovery (REC) 버튼 누른 상태 유지
5. Reset 버튼 누른 후 해제 (또는 Power 버튼)
6. 2초 후 Force Recovery 버튼 해제
```

### 검증 명령어

```bash
# Host PC (Linux)에서 확인
lsusb | grep -i nvidia
# 출력 예: Bus 003 Device 006: ID 0955:7c18 NVIDIA Corp. APX
```

---

## 10. 참고 자료

- [NVIDIA Jetson TX2 Developer Page](https://developer.nvidia.com/embedded/jetson-tx2)
- [Jetson TX2 Datasheet (PDF)](https://connecttech.com/pdf/jetson_tx2_datasheet.pdf)
- [NVIDIA JetPack SDK Documentation](https://developer.nvidia.com/embedded/jetpack)
- [SDK Manager Documentation](https://docs.nvidia.com/sdk-manager/)
- [Jetson Linux Developer Guide](https://docs.nvidia.com/jetson/l4t/)
- [NVIDIA Jetson Developer Forums](https://forums.developer.nvidia.com/c/agx-autonomous-machines/jetson-embedded-systems/)
- [TX1/TX2 Developer Kit User Guide (PDF)](https://developer.download.nvidia.com/embedded/L4T/r28_Release_v1.0/Docs/Jetson_TX1_and_TX2_Developer_Kits_User_Guide.pdf)
