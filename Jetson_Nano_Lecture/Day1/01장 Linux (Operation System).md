# 1장 Linux (Operation System)

## OS (Operating System)

- 사용자와 컴퓨터 하드웨어 사이의 인터페이스 역할을 하는 소프트웨어의 집합
  - 컴퓨터 시스템의 자원을 효율적으로 관리
  - 사용자 및 다른 소프트웨어와의 상호작용
  - 성능 최적화 및 편리한 인터페이스 제공
  - 범용OS 와 전용(Embedded)OS로 구분되어 사용됨

Application
Operating System
Hardware

범용OS
전용(Embedded)OS

## OS (Operating System) - Linux

- Open Source and Free
- Linux에는 Red Hat, SUSE 및 Debian등 배포판이 존재
  - 배포판(Distribution): Linux Kernel 외 용도에 따른 여러 소프트웨어 패키지들을 함께 담은 Linux OS 시스템
- NVIDIA Jetson은 Ubuntu Linux 지원

## Linux 활용 분야

## Linux OS의 주요 구성

- BootLoader
- Kernel
- Daemon
- Shell
- File System
- X Window System (Desktop Environment)

## Linux – BootLoader

- **BootLoader**
  - 컴퓨터를 부팅할 때 설치된 운영체제를 메모리에 로드하고 실행하는 역할
  - BIOS, UEFI가 부트 디바이스(하드 디스크, SSD)에서 부트로더를 로드하고 실행
  - 대표적인 부트로더로는 GRUB(Grand Unified Bootloader)이 있음
- **UEFI (Unified Extensible Firmware Interface)**
  - 64bit OS 부팅을 지원하는 펌웨어 (Legacy BIOS Setup 인터페이스 지원)

## Linux – Kernel

- **Kernel**
  - 운영체제의 핵심 부분으로, 하드웨어와 소프트웨어 간의 인터페이스 역할
  - 부팅 과정에서 커널이 메모리에 로드되어 실행
  - 프로세스 관리, 메모리 관리, 파일 시스템 관리, 장치 드라이버 관리 등의 기능 수행
  - 쉘(Shell)에게 전달받은 사용자의 요청을 하드웨어에게 전달하여 처리할 수 있게 함
  - OS의 가장 낮은 수준

```
API
(Application Programming
Interface)
```

## Linux – Daemons

- **Daemon**
  - 데몬(daemon)은 백그라운드에서 실행되며 사용자의 직접적인 개입 없이 특정 작업을 수행하는 프로그램
  - 서버나 시스템 관리 작업을 자동화하는 역할을 하며, 주로 시스템이 부팅될 때 시작되어 지속적으로 실행
  - 리눅스 시스템 운영에 필수적인 역할을 하며, 서버 및 백그라운드 작업을 안정적으로 유지하는 핵심 요소
  - 대표적인 리눅스 데몬

## Linux – Shell

- **Shell**
  - 사용자와 커널 간의 명령 인터페이스 역할
  - 사용자가 명령어를 입력하면 셸이 이를 해석하여 커널에 전달하고, 커널의 실행 결과를 사용자에게 반환
  - 즉, 사용자의 요청이 Shell에 프로그램에 통해 해석되고, 그 결과가 kernel에 전달 됨
  - 대표적인 셸로는 Bash(Bourne Again Shell), sh(Bourne shell), Ash(Almquist Shell) 등이 있음

## Linux - File System

- **File System**
  - 리눅스 파일 시스템은 계층적인 구조를 가지고 있으며, 모든 파일과 디렉토리는 /(루트)에서 시작되고 루트 아래에 여러 하위 디렉토리가 위치
  - 여러 종류의 파일 타입 지원 – 일반 파일, 심볼릭 링크 파일, 디바이스 파일 ...
  - 사용자와 그룹 기반의 권한 시스템을 사용하여 파일과 디렉토리에 대한 접근 제어
  - 파일 시스템은 대표적으로 Ext4, XFS, Btrfs등이 있음
  - 리눅스에서는 파일 시스템을 마운트해서 사용
    - 마운트는 특정 저장 장치의 파일 시스템을 파일 시스템 계층 구조의 특정 지점에 연결하는 과정을 의미

## Linux – X Window System

- **X Window System**
  - 리눅스에서 그래픽 사용자 인터페이스(GUI)를 제공하는 시스템
  - 디스플레이 장치에 창을 표시하며 마우스와 키보드 등의 입력장치의 상호작용 등을 관리해 GUI 환경의 구현을 위한 기본적인 프레임워크 제공
- **Desktop Environment**
  - 운영 체제 상단의 그래픽 사용자 인터페이스 (사용자가 모니터를 통해 볼 수 있는 작업 공간)
  - 'GNOME', 'KDE', 'Xfce' 및 'Fluxbox'등 다양한 데스크탑 환경 (Ubuntu Linux는 GNOME 데스크탑 환경 지원)

< GNOME >
< KDE >
< Xfce >

## Linux Repository

- Linux에서 repository는 설치하고자 하는 프로그램/소프트웨어 패키지가 저장된 서버
- Linux 배포판별 패키지 저장소(서버)로 부터 소프트웨어 검색 및 설치하는 도구 제공
  - Ubuntu/Debian : APT(Advanced Packaging Tool), ".deb" 패키지 파일
  - Red Hat/CentOS/Fedora : YUM(Yellowdog Updater, Modifier), ".rpm"(Red Hat Package Manager) 패키지 파일
  - Arch Linux : Pacman
- Repository에 찾는 소프트웨어가 없다면, 패키지를 담고 있는 서버를 리눅스 환경에 새로 등록해야 함

## Linux Terminal

- 사용자가 명령을 입력하고 출력 결과를 텍스트로 확인하는 인터페이스
- 터미널은 정보를 전송하는 역할, OS가 정보를 이해하기 위해 터미널은 shell을 사용(주로 bash)
- CLI(Command Line Interface): 사용자가 텍스트로 명령어를 입력하고 결과가 텍스트로 화면에 출력

Kernel
Shell
< Terminal Application >
