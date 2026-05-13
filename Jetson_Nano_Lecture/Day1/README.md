# STEP1 : Linux 기초 및 Jetson Nano 개발 환경 구축

## Linux 개요

### OS (Operating System)

- **정의**: 사용자와 컴퓨터 하드웨어 사이의 인터페이스 역할을 하는 소프트웨어의 집합
- **역할**:
  - 컴퓨터 시스템의 자원을 효율적으로 관리
  - 사용자 및 다른 소프트웨어와의 상호작용
  - 성능 최적화 및 편리한 인터페이스 제공
- **분류**: 범용OS vs 전용(Embedded)OS

### Linux의 특징

- **Open Source and Free**: 무료로 사용 가능하며 소스 코드 공개
- ** 배포판(Distribution)**:
  - Red Hat, SUSE, Debian 등 다양한 배포판 존재
  - Linux Kernel 외 용도에 따른 여러 소프트웨어 패키지들을 함께 담은 OS 시스템
- **지원**: NVIDIA Jetson은 Ubuntu Linux 지원

---

## Linux OS의 주요 구성

### 1. BootLoader

- **역할**: 컴퓨터를 부팅할 때 설치된 운영체제를 메모리에 로드하고 실행
- **흐름**: BIOS/UEFI → 부트 디바이스에서 부트로더 로드 및 실행
- **주요 부트로더**: GRUB (Grand Unified Bootloader)
- **UEFI**: 64bit OS 부팅을 지원하는 펌웨어 (Legacy BIOS Setup 인터페이스 지원)

### 2. Kernel

- **정의**: 운영체제의 핵심 부분, 하드웨어와 소프트웨어 간의 인터페이스 역할
- **역할**:
  - 프로세스 관리
  - 메모리 관리
  - 파일 시스템 관리
  - 장치 드라이버 관리
- **특징**: OS의 가장 낮은 수준에서 동작

### 3. Daemon (데몬)

- **정의**: 백그라운드에서 실행되며 사용자의 직접적인 개입 없이 특정 작업을 수행하는 프로그램
- **역할**: 서버나 시스템 관리 작업을 자동화
- **특징**: 시스템 부팅 시 시작되어 지속적으로 실행

### 4. Shell

- **정의**: 사용자와 커널 간의 명령 인터페이스
- **흐름**: 사용자 명령어 입력 → Shell이 해석 → Kernel에 전달 → 결과 반환
- **종류**: Bash (Bourne Again Shell), sh, Ash 등

### 5. File System

- **특징**: 계층적 구조, 모든 파일과 디렉토리는 `/`(루트)에서 시작
- **파일 타입**: 일반 파일, 심볼릭 링크 파일, 디바이스 파일 등
- **권한**: 사용자와 그룹 기반의 접근 제어
- **종류**: Ext4, XFS, Btrfs 등
- **마운트**: 저장 장치의 파일 시스템을 파일 시스템 계층 구조의 특정 지점에 연결

### 6. X Window System & Desktop Environment

- **X Window System**: 리눅스에서 GUI를 제공하는 시스템
- **Desktop Environment**: GNOME, KDE, Xfce, Fluxbox 등
- **Ubuntu**: GNOME 데스크탑 환경 지원

---

## Linux Repository

- **정의**: 설치하고자 하는 프로그램/소프트웨어 패키지가 저장된 서버

| 배포판 | 패키지 관리자 | 파일 형식 |
|---|---|---|
| Ubuntu/Debian | APT (Advanced Packaging Tool) | .deb |
| Red Hat/CentOS/Fedora | YUM (Yellowdog Updater, Modifier) | .rpm |
| Arch Linux | Pacman | - |

---

## Linux Terminal

- **정의**: 사용자가 명령을 입력하고 출력 결과를 텍스트로 확인하는 인터페이스
- **CLI (Command Line Interface)**: 텍스트로 명령어를 입력하고 결과가 텍스트로 출력

---

## Jetson OS Flash

### Flash란?

- 운영체제와 소프트웨어를 디바이스의 저장 장치 (micro SD card 또는 eMMC)에 설치하는 과정
- 부팅에 필요한 모든 시스템 파일과 소프트웨어를 저장 장치에 기록

### Flash 방법

#### 1. SDK Manager 사용

- Devkit(개발 참조보드)만 지원
- NVIDIA 공식 도구

#### 2. Jetson Linux

- Jetson module들을 위한 Board Support Package (BSP)
- Kernel, Bootloader, Flashing utility, Ubuntu 기반의 sample root filesystem 포함
- 지원 버전: Jetson Linux 32.7.1 (Ubuntu 18.04 LTS), Jetson Linux 35.x.x (Ubuntu 20.04 LTS)

#### 3. MFI (Mass Flash Interface)

- 대량 flash를 위해 설계된 방법
- 여러 Jetson module 동시 flash 가능

### Recovery Mode Boot

- Jetson SOM별 USB ID: `Bus <bbb> Device <ddd>: ID 0955: <nnnn> Nvidia Corp.`
- Jetson Nano 예시: `BUS 001 Device 005: ID 0955:7f21 NVidia Corp.`

---

## VirtualBox 설치 및 Ubuntu 설정

### VirtualBox란?

- 하나의 물리적 컴퓨터에서 여러 개의 가상 머신(VM)으로 분할하여 각기 다른 운영체제를 동시에 실행 가능
- **Host OS**: VirtualBox가 설치된 실제 컴퓨터 (Windows 11 등)
- **Guest OS**: VirtualBox내에서 실행되는 가상머신 (Ubuntu 등)

### 설치 단계

1. VirtualBox 설치 파일 다운로드 (https://www.oracle.com/kr/virtualization/technologies/vm/downloads/virtualbox-downloads.html)
2. VirtualBox Extension Pack 설치
3. (필요시) Microsoft Visual C++ 재배포 가능_PACK 설치
4. VM 생성:
   - 이름: ubuntu (자동으로 Linux - Ubuntu로 인식)
   - 메모리: 여유 있게 설정 (최소 4GB 이상 권장)
   - 디스크: 최소 30GB 이상
5. 설정:
   - 클립보드 공유: 양방향
   - 드래그 앤 드롭: 양방향
   - 네트워크: 브릿지 어댑터
   - 공유 폴더 설정
6. Ubuntu 설치:
   - 사용자명/비밀번호: nvidia (본 강의에서는統一)

### Guest Additions 설치

- 장치 → 게스트 확장 CD 이미지 삽입 → 실행
- 설치 후 마우스 통합, 공유 폴더, 더 나은 비디오 지원 등 기능 사용 가능

---

## Visual Studio Code 설치

### Windows PC에서 설치

1. Visual Studio Code 다운로드 (ver 1.84 권장)
2. 설치 진행
3. **자동 업데이트 비활성화** (Jetson Nano SSH 연결 문제 방지):
   - File → Preferences → Settings
   - Auto Update: None
   - Enable Windows Background updates: 체크 해제
   - Update: Mode → None

### VirtualBox + Ubuntu에서 설치

1. Ubuntu 18.04용 Visual Studio Code (ver 1.84) 다운로드
2. `.deb` 파일 설치: `sudo dpkg -i code_1.84.2-1699528352_amd64.deb`
3. 실행: 터미널에서 `code` 입력

---

## Jetson Nano MFI Flash (Jetpack 4.6)

### 실습 단계

1. Guest PC (Ubuntu)에서 디렉토리 생성:
   ```bash
   mkdir jetson
   cd jetson
   ```

2. 압축 파일 복사 및解压:
   ```bash
   tar xvjf allai-mfi-jcb100-nano.tbz2
   cd mfi_jetson-nano-emmc/
   ```

3. Recovery Mode 설정:
   - 5pin USB로 연결
   - Recovery Mode 진입 (Jumper 핀 설정)
   - VirtualBox: 장치 → USB → NVIDIA Corp, APX 선택

4. USB 연결 확인:
   ```bash
   lsusb
   # 0955:7f21 Nvidia Crop. 확인
   ```

5. Flash 실행:
   ```bash
   sudo ./nvmflash.sh
   ```

6. 성공 시 "Flash complete (SUCCESS)" 메시지 확인

### 초기 설정 (Jetson Nano 부팅 후)

1. 언어: English 선택
2. 지역: Seoul
3. 사용자명/비밀번호: nvidia (统一)

---

## SD 카드 Image 굽기 및 부팅 시스템 변경

### SD 카드에 Image 굽기

1. BalenaEtcher 설치 (관리자 권한 실행)
2. Image File 선택 (`jcb100_nano_sd.img`)
3. Target으로 SD 카드 선택
4. Flash 완료

### 부팅 미디어 변경 (eMMC → SD 카드)

1. SD 카드 Jetpack 설치된 Jetson Nano에 삽입
2. SD 카드 공간 확장 (gparted 사용):
   ```bash
   sudo apt install gparted
   sudo gparted
   # /dev/mmcblk1 에서 파티션 크기 조정
   ```

3. 부팅 설정 파일 수정:
   ```bash
   # extlinux.conf 수정 (mmcblk1p1로 변경)
   sudo vi /boot/extlinux/extlinux.conf
   # 또는
   sudo gedit /boot/extlinux/extlinux.conf
   ```

4. Reboot:
   ```bash
   sudo reboot
   ```

5. 확인:
   ```bash
   df -h
   # /dev/mmcblk1p1이 /에 마운트되어 있는지 확인
   ```

---

## NVIDIA Jetson 플랫폼

### Jetson이란?

- CPU (Cortex-A: Tegra) + Nvidia GPU + NPU 등을 하나의 SOC에 탑재한 임베디드 플랫폼
- CUDA와 Deep-Learning (cuDNN) 환경 및 TensorFlow, PyTorch 등 프레임워크 지원
- SOM (System-On-Module) 형태로 설계

### Jetson 시리즈

| 모델 | AI Performance | GPU | CPU |
|---|---|---|---|
| Jetson Nano | 472 GFLOPs | 128-core Maxwell | Quad-Core ARM Cortex-A57 |
| Jetson TX2 NX | 1.33 TFLOPs | 256-core Pascal | Dual-Core Denver 2 + Quad-Core A57 |
| Jetson Xavier NX | 21 TOPs | 384-core Volta | 6-core Carmel |
| Jetson Orin Nano | 20-40 TOPS | 512-1024-core Ampere | 6-core A78AE |
| Jetson AGX Orin | 200-275 TOPS | 1792-2048-core Ampere | 8-core A78AE |

---

## Jetson Module (SOM) vs Developer Kit

### Jetson Module (SOM)

- 양산 및 운영 환경에 적합
- 사전 설치된 소프트웨어 없이 판매
- 캐리어 보드에 부착 후 소프트웨어 이미지 flash하여 배포

### Jetson Developer Kit

- 참조용 캐리어 보드와 비양산 용도의 Jetson 모듈 포함
- Jetpack SDK를 통해 소프트웨어 개발 및 테스트
- 양산 용도로 사용되지 않음

---

## JCB100 (Jetson Carrier Board)

- Nvidia Jetson Module을 운영하기 위한 시스템 보드
- 다양한 외부 인터페이스 지원
- Jetson Nano Developer Kit과 Jetson Xavier NX Developer Kit에 호환
- 추가적인 외부 저장 장치 및 CAN 통신 지원 (Jetson Nano 제외)

---

## 참고 자료

- [NVIDIA Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano)
- [Jetson Linux Archive](https://developer.nvidia.com/embedded/jetson-linux-archive)
- [JetPack Documentation](https://docs.nvidia.com/jetson/archives/index.html)
- [Visual Studio Code SSH](https://code.visualstudio.com/docs/remote/ssh)
