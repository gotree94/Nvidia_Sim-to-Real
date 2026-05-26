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

```
dministrator@DESKTOP-C2MQEL4:~$ sudo apt update && sudo apt upgrade -y
[sudo] password for dministrator:
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://security.ubuntu.com/ubuntu jammy-security InRelease [129 kB]
Get:3 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [128 kB]
Get:4 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages [3250 kB]
Get:5 http://archive.ubuntu.com/ubuntu jammy-backports InRelease [127 kB]
Get:6 http://archive.ubuntu.com/ubuntu jammy/universe amd64 Packages [14.1 MB]
Get:7 http://security.ubuntu.com/ubuntu jammy-security/main Translation-en [457 kB]
Get:8 http://security.ubuntu.com/ubuntu jammy-security/main amd64 c-n-f Metadata [14.3 kB]
Get:9 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 Packages [5781 kB]
Get:10 http://security.ubuntu.com/ubuntu jammy-security/restricted Translation-en [1103 kB]
Get:11 http://security.ubuntu.com/ubuntu jammy-security/restricted amd64 c-n-f Metadata [680 B]
Get:12 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 Packages [1031 kB]
Get:13 http://security.ubuntu.com/ubuntu jammy-security/universe Translation-en [227 kB]
Get:14 http://security.ubuntu.com/ubuntu jammy-security/universe amd64 c-n-f Metadata [22.9 kB]
Get:15 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 Packages [64.3 kB]
Get:16 http://security.ubuntu.com/ubuntu jammy-security/multiverse Translation-en [12.6 kB]
Get:17 http://security.ubuntu.com/ubuntu jammy-security/multiverse amd64 c-n-f Metadata [388 B]
Get:18 http://archive.ubuntu.com/ubuntu jammy/universe Translation-en [5652 kB]
Get:19 http://archive.ubuntu.com/ubuntu jammy/universe amd64 c-n-f Metadata [286 kB]
Get:20 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 Packages [217 kB]
Get:21 http://archive.ubuntu.com/ubuntu jammy/multiverse Translation-en [112 kB]
Get:22 http://archive.ubuntu.com/ubuntu jammy/multiverse amd64 c-n-f Metadata [8372 B]
Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages [3523 kB]
Get:24 http://archive.ubuntu.com/ubuntu jammy-updates/main Translation-en [528 kB]
Get:25 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 c-n-f Metadata [19.8 kB]
Get:26 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 Packages [6001 kB]
Get:27 http://archive.ubuntu.com/ubuntu jammy-updates/restricted Translation-en [1143 kB]
Get:28 http://archive.ubuntu.com/ubuntu jammy-updates/restricted amd64 c-n-f Metadata [600 B]
Get:29 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 Packages [1269 kB]
Get:30 http://archive.ubuntu.com/ubuntu jammy-updates/universe Translation-en [316 kB]
Get:31 http://archive.ubuntu.com/ubuntu jammy-updates/universe amd64 c-n-f Metadata [30.5 kB]
Get:32 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 Packages [71.6 kB]
Get:33 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse Translation-en [15.5 kB]
Get:34 http://archive.ubuntu.com/ubuntu jammy-updates/multiverse amd64 c-n-f Metadata [756 B]
Get:35 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 Packages [70.2 kB]
Get:36 http://archive.ubuntu.com/ubuntu jammy-backports/main Translation-en [11.4 kB]
Get:37 http://archive.ubuntu.com/ubuntu jammy-backports/main amd64 c-n-f Metadata [412 B]
Get:38 http://archive.ubuntu.com/ubuntu jammy-backports/restricted amd64 c-n-f Metadata [116 B]
Get:39 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 Packages [30.8 kB]
Get:40 http://archive.ubuntu.com/ubuntu jammy-backports/universe Translation-en [16.9 kB]
Get:41 http://archive.ubuntu.com/ubuntu jammy-backports/universe amd64 c-n-f Metadata [676 B]
Get:42 http://archive.ubuntu.com/ubuntu jammy-backports/multiverse amd64 c-n-f Metadata [116 B]
Fetched 45.8 MB in 6s (7831 kB/s)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
84 packages can be upgraded. Run 'apt list --upgradable' to see them.
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Calculating upgrade... Done
The following NEW packages will be installed:
  netplan-generator python3-netplan
The following packages will be upgraded:
  bind9-dnsutils bind9-host bind9-libs bsdextrautils bsdutils coreutils curl distro-info-data eject fdisk
  gir1.2-packagekitglib-1.0 iproute2 kmod libavahi-client3 libavahi-common-data libavahi-common3 libblkid1
  libcairo-gobject2 libcairo2 libcap2 libcap2-bin libcurl3-gnutls libcurl4 libfdisk1 libgdk-pixbuf-2.0-0
  libgdk-pixbuf2.0-bin libgdk-pixbuf2.0-common libgnutls30 libkmod2 liblcms2-2 libmount1 libnetplan0 libnftables1
  libnghttp2-14 libnss-systemd libntfs-3g89 libpackagekit-glib2-18 libpam-cap libpam-systemd libpng16-16
  libpolkit-agent-1-0 libpolkit-gobject-1-0 libsmartcols1 libssh-4 libssl3 libsystemd0 libtiff5 libudev1 libuuid1 lshw
  mount netplan.io nftables ntfs-3g openssh-client openssl packagekit packagekit-tools pkexec policykit-1 polkitd
  python3-cryptography python3-jwt python3-openssl python3-pyasn1 rsync sed snapd sudo systemd systemd-sysv
  systemd-timesyncd tzdata ubuntu-advantage-tools ubuntu-pro-client ubuntu-pro-client-l10n udev util-linux
  uuid-runtime vim vim-common vim-runtime vim-tiny xxd
84 upgraded, 2 newly installed, 0 to remove and 0 not upgraded.
63 standard LTS security updates
Need to get 67.3 MB of archives.
After this operation, 1979 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 bsdutils amd64 1:2.37.2-4ubuntu3.5 [80.7 kB]
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 coreutils amd64 8.32-4.1ubuntu1.3 [1437 kB]
Get:3 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 sed amd64 4.8-1ubuntu2.1 [188 kB]
Get:4 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 util-linux amd64 2.37.2-4ubuntu3.5 [1067 kB]
Get:5 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libnss-systemd amd64 249.11-0ubuntu3.20 [133 kB]
Get:6 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libsystemd0 amd64 249.11-0ubuntu3.20 [317 kB]
Get:7 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 systemd-timesyncd amd64 249.11-0ubuntu3.20 [31.2 kB]
Get:8 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 systemd-sysv amd64 249.11-0ubuntu3.20 [10.5 kB]
Get:9 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpam-systemd amd64 249.11-0ubuntu3.20 [203 kB]
Get:10 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 systemd amd64 249.11-0ubuntu3.20 [4585 kB]
Get:11 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 udev amd64 249.11-0ubuntu3.20 [1559 kB]
Get:12 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libudev1 amd64 249.11-0ubuntu3.20 [76.4 kB]
Get:13 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libblkid1 amd64 2.37.2-4ubuntu3.5 [103 kB]
Get:14 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcap2 amd64 1:2.44-1ubuntu0.22.04.3 [18.5 kB]
Get:15 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libssl3 amd64 3.0.2-0ubuntu1.23 [1906 kB]
Get:16 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 kmod amd64 29-1ubuntu1.1 [102 kB]
Get:17 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libkmod2 amd64 29-1ubuntu1.1 [48.1 kB]
Get:18 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libgnutls30 amd64 3.7.3-4ubuntu1.9 [971 kB]
Get:19 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libmount1 amd64 2.37.2-4ubuntu3.5 [122 kB]
Get:20 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 mount amd64 2.37.2-4ubuntu3.5 [114 kB]
Get:21 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 ntfs-3g amd64 1:2021.8.22-3ubuntu1.3 [408 kB]
Get:22 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libntfs-3g89 amd64 1:2021.8.22-3ubuntu1.3 [161 kB]
Get:23 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 rsync amd64 3.2.7-0ubuntu0.22.04.6 [444 kB]
Get:24 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libsmartcols1 amd64 2.37.2-4ubuntu3.5 [50.7 kB]
Get:25 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libuuid1 amd64 2.37.2-4ubuntu3.5 [23.6 kB]
Get:26 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 uuid-runtime amd64 2.37.2-4ubuntu3.5 [32.1 kB]
Get:27 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 distro-info-data all 0.52ubuntu0.12 [5488 B]
Get:28 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 eject amd64 2.37.2-4ubuntu3.5 [26.8 kB]
Get:29 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpam-cap amd64 1:2.44-1ubuntu0.22.04.3 [7928 B]
Get:30 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcap2-bin amd64 1:2.44-1ubuntu0.22.04.3 [26.0 kB]
Get:31 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 iproute2 amd64 5.15.0-1ubuntu2.1 [1072 kB]
Get:32 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 netplan.io amd64 0.107.1-3ubuntu0.22.04.3 [56.3 kB]
Get:33 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 netplan-generator amd64 0.107.1-3ubuntu0.22.04.3 [57.1 kB]
Get:34 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3-netplan amd64 0.107.1-3ubuntu0.22.04.3 [23.1 kB]
Get:35 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libnetplan0 amd64 0.107.1-3ubuntu0.22.04.3 [117 kB]
Get:36 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 openssl amd64 3.0.2-0ubuntu1.23 [1186 kB]
Get:37 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 sudo amd64 1.9.9-1ubuntu2.6 [820 kB]
Get:38 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 tzdata all 2026a-0ubuntu0.22.04.1 [348 kB]
Get:39 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 ubuntu-pro-client-l10n amd64 37.2ubuntu~22.04 [20.7 kB]
Get:40 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 ubuntu-pro-client amd64 37.2ubuntu~22.04 [237 kB]
Get:41 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 ubuntu-advantage-tools all 37.2ubuntu~22.04 [10.9 kB]
Get:42 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim amd64 2:8.2.3995-1ubuntu2.30 [1732 kB]
Get:43 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-tiny amd64 2:8.2.3995-1ubuntu2.30 [707 kB]
Get:44 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-runtime all 2:8.2.3995-1ubuntu2.30 [6824 kB]
Get:45 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 xxd amd64 2:8.2.3995-1ubuntu2.30 [51.1 kB]
Get:46 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 vim-common all 2:8.2.3995-1ubuntu2.30 [81.5 kB]
Get:47 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libnghttp2-14 amd64 1.43.0-1ubuntu0.3 [76.7 kB]
Get:48 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 bind9-dnsutils amd64 1:9.18.39-0ubuntu0.22.04.4 [158 kB]
Get:49 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 bind9-host amd64 1:9.18.39-0ubuntu0.22.04.4 [52.1 kB]
Get:50 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 bind9-libs amd64 1:9.18.39-0ubuntu0.22.04.4 [1263 kB]
Get:51 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 bsdextrautils amd64 2.37.2-4ubuntu3.5 [71.4 kB]
Get:52 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 nftables amd64 1.0.2-1ubuntu3.1 [67.2 kB]
Get:53 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libnftables1 amd64 1.0.2-1ubuntu3.1 [332 kB]
Get:54 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpng16-16 amd64 1.6.37-3ubuntu0.5 [192 kB]
Get:55 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 lshw amd64 02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1 [322 kB]
Get:56 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 openssh-client amd64 1:8.9p1-3ubuntu0.15 [904 kB]
Get:57 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libssh-4 amd64 0.9.6-2ubuntu0.22.04.7 [187 kB]
Get:58 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 curl amd64 7.81.0-1ubuntu1.24 [194 kB]
Get:59 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcurl4 amd64 7.81.0-1ubuntu1.24 [291 kB]
Get:60 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libfdisk1 amd64 2.37.2-4ubuntu3.5 [140 kB]
Get:61 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 fdisk amd64 2.37.2-4ubuntu3.5 [122 kB]
Get:62 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpackagekit-glib2-18 amd64 1.2.5-2ubuntu3.1 [124 kB]
Get:63 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 gir1.2-packagekitglib-1.0 amd64 1.2.5-2ubuntu3.1 [25.3 kB]
Get:64 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libavahi-client3 amd64 0.8-5ubuntu5.5 [28.1 kB]
Get:65 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libavahi-common3 amd64 0.8-5ubuntu5.5 [23.9 kB]
Get:66 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libavahi-common-data amd64 0.8-5ubuntu5.5 [24.0 kB]
Get:67 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcairo-gobject2 amd64 1.16.0-5ubuntu2.1 [19.5 kB]
Get:68 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcairo2 amd64 1.16.0-5ubuntu2.1 [628 kB]
Get:69 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libcurl3-gnutls amd64 7.81.0-1ubuntu1.24 [285 kB]
Get:70 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libgdk-pixbuf2.0-common all 2.42.8+dfsg-1ubuntu0.5 [5560 B]
Get:71 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libtiff5 amd64 4.3.0-6ubuntu0.13 [185 kB]
Get:72 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libgdk-pixbuf-2.0-0 amd64 2.42.8+dfsg-1ubuntu0.5 [148 kB]
Get:73 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libgdk-pixbuf2.0-bin amd64 2.42.8+dfsg-1ubuntu0.5 [14.2 kB]
Get:74 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 liblcms2-2 amd64 2.12~rc1-2ubuntu0.1 [159 kB]
Get:75 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 pkexec amd64 0.105-33ubuntu0.1 [15.2 kB]
Get:76 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 polkitd amd64 0.105-33ubuntu0.1 [80.1 kB]
Get:77 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 policykit-1 amd64 0.105-33ubuntu0.1 [2438 B]
Get:78 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpolkit-agent-1-0 amd64 0.105-33ubuntu0.1 [16.9 kB]
Get:79 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 libpolkit-gobject-1-0 amd64 0.105-33ubuntu0.1 [43.3 kB]
Get:80 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 packagekit-tools amd64 1.2.5-2ubuntu3.1 [28.8 kB]
Get:81 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 packagekit amd64 1.2.5-2ubuntu3.1 [442 kB]
Get:82 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3-cryptography amd64 3.4.8-1ubuntu2.4 [236 kB]
Get:83 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3-jwt all 2.3.0-1ubuntu0.3 [17.3 kB]
Get:84 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3-openssl all 21.0.0-1ubuntu0.1 [45.4 kB]
Get:85 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 python3-pyasn1 all 0.4.8-1ubuntu0.2 [52.0 kB]
Get:86 http://archive.ubuntu.com/ubuntu jammy-updates/main amd64 snapd amd64 2.75.2+ubuntu22.04 [32.7 MB]
Fetched 67.3 MB in 7s (10.0 MB/s)
Extracting templates from packages: 100%
Preconfiguring packages ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../bsdutils_1%3a2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking bsdutils (1:2.37.2-4ubuntu3.5) over (1:2.37.2-4ubuntu3.4) ...
Setting up bsdutils (1:2.37.2-4ubuntu3.5) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../coreutils_8.32-4.1ubuntu1.3_amd64.deb ...
Unpacking coreutils (8.32-4.1ubuntu1.3) over (8.32-4.1ubuntu1.2) ...
Setting up coreutils (8.32-4.1ubuntu1.3) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../sed_4.8-1ubuntu2.1_amd64.deb ...
Unpacking sed (4.8-1ubuntu2.1) over (4.8-1ubuntu2) ...
Setting up sed (4.8-1ubuntu2.1) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../util-linux_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking util-linux (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Setting up util-linux (2.37.2-4ubuntu3.5) ...
fstrim.service is a disabled or a static unit not running, not starting it.
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../libnss-systemd_249.11-0ubuntu3.20_amd64.deb ...
Unpacking libnss-systemd:amd64 (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Preparing to unpack .../libsystemd0_249.11-0ubuntu3.20_amd64.deb ...
Unpacking libsystemd0:amd64 (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Setting up libsystemd0:amd64 (249.11-0ubuntu3.20) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../0-systemd-timesyncd_249.11-0ubuntu3.20_amd64.deb ...
Unpacking systemd-timesyncd (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Preparing to unpack .../1-systemd-sysv_249.11-0ubuntu3.20_amd64.deb ...
Unpacking systemd-sysv (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Preparing to unpack .../2-libpam-systemd_249.11-0ubuntu3.20_amd64.deb ...
Unpacking libpam-systemd:amd64 (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Preparing to unpack .../3-systemd_249.11-0ubuntu3.20_amd64.deb ...
Unpacking systemd (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Preparing to unpack .../4-udev_249.11-0ubuntu3.20_amd64.deb ...
Unpacking udev (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Preparing to unpack .../5-libudev1_249.11-0ubuntu3.20_amd64.deb ...
Unpacking libudev1:amd64 (249.11-0ubuntu3.20) over (249.11-0ubuntu3.17) ...
Setting up libudev1:amd64 (249.11-0ubuntu3.20) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../libblkid1_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking libblkid1:amd64 (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Setting up libblkid1:amd64 (2.37.2-4ubuntu3.5) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../libcap2_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libcap2:amd64 (1:2.44-1ubuntu0.22.04.3) over (1:2.44-1ubuntu0.22.04.2) ...
Setting up libcap2:amd64 (1:2.44-1ubuntu0.22.04.3) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../libssl3_3.0.2-0ubuntu1.23_amd64.deb ...
Unpacking libssl3:amd64 (3.0.2-0ubuntu1.23) over (3.0.2-0ubuntu1.21) ...
Setting up libssl3:amd64 (3.0.2-0ubuntu1.23) ...
(Reading database ... 42622 files and directories currently installed.)
Preparing to unpack .../kmod_29-1ubuntu1.1_amd64.deb ...
Unpacking kmod (29-1ubuntu1.1) over (29-1ubuntu1) ...
Preparing to unpack .../libkmod2_29-1ubuntu1.1_amd64.deb ...
Unpacking libkmod2:amd64 (29-1ubuntu1.1) over (29-1ubuntu1) ...
Preparing to unpack .../libgnutls30_3.7.3-4ubuntu1.9_amd64.deb ...
Unpacking libgnutls30:amd64 (3.7.3-4ubuntu1.9) over (3.7.3-4ubuntu1.8) ...
Setting up libgnutls30:amd64 (3.7.3-4ubuntu1.9) ...
(Reading database ... 42623 files and directories currently installed.)
Preparing to unpack .../libmount1_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking libmount1:amd64 (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Setting up libmount1:amd64 (2.37.2-4ubuntu3.5) ...
(Reading database ... 42623 files and directories currently installed.)
Preparing to unpack .../mount_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking mount (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Preparing to unpack .../ntfs-3g_1%3a2021.8.22-3ubuntu1.3_amd64.deb ...
Unpacking ntfs-3g (1:2021.8.22-3ubuntu1.3) over (1:2021.8.22-3ubuntu1.2) ...
Preparing to unpack .../libntfs-3g89_1%3a2021.8.22-3ubuntu1.3_amd64.deb ...
Unpacking libntfs-3g89 (1:2021.8.22-3ubuntu1.3) over (1:2021.8.22-3ubuntu1.2) ...
Preparing to unpack .../rsync_3.2.7-0ubuntu0.22.04.6_amd64.deb ...
Unpacking rsync (3.2.7-0ubuntu0.22.04.6) over (3.2.7-0ubuntu0.22.04.4) ...
Preparing to unpack .../libsmartcols1_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking libsmartcols1:amd64 (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Setting up libsmartcols1:amd64 (2.37.2-4ubuntu3.5) ...
(Reading database ... 42623 files and directories currently installed.)
Preparing to unpack .../libuuid1_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking libuuid1:amd64 (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Setting up libuuid1:amd64 (2.37.2-4ubuntu3.5) ...
(Reading database ... 42623 files and directories currently installed.)
Preparing to unpack .../00-uuid-runtime_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking uuid-runtime (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Preparing to unpack .../01-distro-info-data_0.52ubuntu0.12_all.deb ...
Unpacking distro-info-data (0.52ubuntu0.12) over (0.52ubuntu0.11) ...
Preparing to unpack .../02-eject_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking eject (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Preparing to unpack .../03-libpam-cap_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libpam-cap:amd64 (1:2.44-1ubuntu0.22.04.3) over (1:2.44-1ubuntu0.22.04.2) ...
Preparing to unpack .../04-libcap2-bin_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libcap2-bin (1:2.44-1ubuntu0.22.04.3) over (1:2.44-1ubuntu0.22.04.2) ...
Preparing to unpack .../05-iproute2_5.15.0-1ubuntu2.1_amd64.deb ...
Unpacking iproute2 (5.15.0-1ubuntu2.1) over (5.15.0-1ubuntu2) ...
Preparing to unpack .../06-netplan.io_0.107.1-3ubuntu0.22.04.3_amd64.deb ...
Unpacking netplan.io (0.107.1-3ubuntu0.22.04.3) over (0.106.1-7ubuntu0.22.04.4) ...
Selecting previously unselected package netplan-generator.
Preparing to unpack .../07-netplan-generator_0.107.1-3ubuntu0.22.04.3_amd64.deb ...
Unpacking netplan-generator (0.107.1-3ubuntu0.22.04.3) ...
Selecting previously unselected package python3-netplan.
Preparing to unpack .../08-python3-netplan_0.107.1-3ubuntu0.22.04.3_amd64.deb ...
Unpacking python3-netplan (0.107.1-3ubuntu0.22.04.3) ...
Preparing to unpack .../09-libnetplan0_0.107.1-3ubuntu0.22.04.3_amd64.deb ...
Unpacking libnetplan0:amd64 (0.107.1-3ubuntu0.22.04.3) over (0.106.1-7ubuntu0.22.04.4) ...
Preparing to unpack .../10-openssl_3.0.2-0ubuntu1.23_amd64.deb ...
Unpacking openssl (3.0.2-0ubuntu1.23) over (3.0.2-0ubuntu1.21) ...
Preparing to unpack .../11-sudo_1.9.9-1ubuntu2.6_amd64.deb ...
Unpacking sudo (1.9.9-1ubuntu2.6) over (1.9.9-1ubuntu2.5) ...
Preparing to unpack .../12-tzdata_2026a-0ubuntu0.22.04.1_all.deb ...
Unpacking tzdata (2026a-0ubuntu0.22.04.1) over (2025b-0ubuntu0.22.04.1) ...
Preparing to unpack .../13-ubuntu-pro-client-l10n_37.2ubuntu~22.04_amd64.deb ...
Unpacking ubuntu-pro-client-l10n (37.2ubuntu~22.04) over (37.1ubuntu0~22.04) ...
Preparing to unpack .../14-ubuntu-pro-client_37.2ubuntu~22.04_amd64.deb ...
Unpacking ubuntu-pro-client (37.2ubuntu~22.04) over (37.1ubuntu0~22.04) ...
Preparing to unpack .../15-ubuntu-advantage-tools_37.2ubuntu~22.04_all.deb ...
Unpacking ubuntu-advantage-tools (37.2ubuntu~22.04) over (37.1ubuntu0~22.04) ...
Preparing to unpack .../16-vim_2%3a8.2.3995-1ubuntu2.30_amd64.deb ...
Unpacking vim (2:8.2.3995-1ubuntu2.30) over (2:8.2.3995-1ubuntu2.24) ...
Preparing to unpack .../17-vim-tiny_2%3a8.2.3995-1ubuntu2.30_amd64.deb ...
Unpacking vim-tiny (2:8.2.3995-1ubuntu2.30) over (2:8.2.3995-1ubuntu2.24) ...
Preparing to unpack .../18-vim-runtime_2%3a8.2.3995-1ubuntu2.30_all.deb ...
Unpacking vim-runtime (2:8.2.3995-1ubuntu2.30) over (2:8.2.3995-1ubuntu2.24) ...
Preparing to unpack .../19-xxd_2%3a8.2.3995-1ubuntu2.30_amd64.deb ...
Unpacking xxd (2:8.2.3995-1ubuntu2.30) over (2:8.2.3995-1ubuntu2.24) ...
Preparing to unpack .../20-vim-common_2%3a8.2.3995-1ubuntu2.30_all.deb ...
Unpacking vim-common (2:8.2.3995-1ubuntu2.30) over (2:8.2.3995-1ubuntu2.24) ...
Preparing to unpack .../21-libnghttp2-14_1.43.0-1ubuntu0.3_amd64.deb ...
Unpacking libnghttp2-14:amd64 (1.43.0-1ubuntu0.3) over (1.43.0-1ubuntu0.2) ...
Preparing to unpack .../22-bind9-dnsutils_1%3a9.18.39-0ubuntu0.22.04.4_amd64.deb ...
Unpacking bind9-dnsutils (1:9.18.39-0ubuntu0.22.04.4) over (1:9.18.39-0ubuntu0.22.04.2) ...
Preparing to unpack .../23-bind9-host_1%3a9.18.39-0ubuntu0.22.04.4_amd64.deb ...
Unpacking bind9-host (1:9.18.39-0ubuntu0.22.04.4) over (1:9.18.39-0ubuntu0.22.04.2) ...
Preparing to unpack .../24-bind9-libs_1%3a9.18.39-0ubuntu0.22.04.4_amd64.deb ...
Unpacking bind9-libs:amd64 (1:9.18.39-0ubuntu0.22.04.4) over (1:9.18.39-0ubuntu0.22.04.2) ...
Preparing to unpack .../25-bsdextrautils_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking bsdextrautils (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Preparing to unpack .../26-nftables_1.0.2-1ubuntu3.1_amd64.deb ...
Unpacking nftables (1.0.2-1ubuntu3.1) over (1.0.2-1ubuntu3) ...
Preparing to unpack .../27-libnftables1_1.0.2-1ubuntu3.1_amd64.deb ...
Unpacking libnftables1:amd64 (1.0.2-1ubuntu3.1) over (1.0.2-1ubuntu3) ...
Preparing to unpack .../28-libpng16-16_1.6.37-3ubuntu0.5_amd64.deb ...
Unpacking libpng16-16:amd64 (1.6.37-3ubuntu0.5) over (1.6.37-3ubuntu0.4) ...
Preparing to unpack .../29-lshw_02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1_amd64.deb ...
Unpacking lshw (02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1) over (02.19.git.2021.06.19.996aaad9c7-2build1) ...
Preparing to unpack .../30-openssh-client_1%3a8.9p1-3ubuntu0.15_amd64.deb ...
Unpacking openssh-client (1:8.9p1-3ubuntu0.15) over (1:8.9p1-3ubuntu0.13) ...
Preparing to unpack .../31-libssh-4_0.9.6-2ubuntu0.22.04.7_amd64.deb ...
Unpacking libssh-4:amd64 (0.9.6-2ubuntu0.22.04.7) over (0.9.6-2ubuntu0.22.04.6) ...
Preparing to unpack .../32-curl_7.81.0-1ubuntu1.24_amd64.deb ...
Unpacking curl (7.81.0-1ubuntu1.24) over (7.81.0-1ubuntu1.22) ...
Preparing to unpack .../33-libcurl4_7.81.0-1ubuntu1.24_amd64.deb ...
Unpacking libcurl4:amd64 (7.81.0-1ubuntu1.24) over (7.81.0-1ubuntu1.22) ...
Preparing to unpack .../34-libfdisk1_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking libfdisk1:amd64 (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Preparing to unpack .../35-fdisk_2.37.2-4ubuntu3.5_amd64.deb ...
Unpacking fdisk (2.37.2-4ubuntu3.5) over (2.37.2-4ubuntu3.4) ...
Preparing to unpack .../36-libpackagekit-glib2-18_1.2.5-2ubuntu3.1_amd64.deb ...
Unpacking libpackagekit-glib2-18:amd64 (1.2.5-2ubuntu3.1) over (1.2.5-2ubuntu3) ...
Preparing to unpack .../37-gir1.2-packagekitglib-1.0_1.2.5-2ubuntu3.1_amd64.deb ...
Unpacking gir1.2-packagekitglib-1.0 (1.2.5-2ubuntu3.1) over (1.2.5-2ubuntu3) ...
Preparing to unpack .../38-libavahi-client3_0.8-5ubuntu5.5_amd64.deb ...
Unpacking libavahi-client3:amd64 (0.8-5ubuntu5.5) over (0.8-5ubuntu5.4) ...
Preparing to unpack .../39-libavahi-common3_0.8-5ubuntu5.5_amd64.deb ...
Unpacking libavahi-common3:amd64 (0.8-5ubuntu5.5) over (0.8-5ubuntu5.4) ...
Preparing to unpack .../40-libavahi-common-data_0.8-5ubuntu5.5_amd64.deb ...
Unpacking libavahi-common-data:amd64 (0.8-5ubuntu5.5) over (0.8-5ubuntu5.4) ...
Preparing to unpack .../41-libcairo-gobject2_1.16.0-5ubuntu2.1_amd64.deb ...
Unpacking libcairo-gobject2:amd64 (1.16.0-5ubuntu2.1) over (1.16.0-5ubuntu2) ...
Preparing to unpack .../42-libcairo2_1.16.0-5ubuntu2.1_amd64.deb ...
Unpacking libcairo2:amd64 (1.16.0-5ubuntu2.1) over (1.16.0-5ubuntu2) ...
Preparing to unpack .../43-libcurl3-gnutls_7.81.0-1ubuntu1.24_amd64.deb ...
Unpacking libcurl3-gnutls:amd64 (7.81.0-1ubuntu1.24) over (7.81.0-1ubuntu1.22) ...
Preparing to unpack .../44-libgdk-pixbuf2.0-common_2.42.8+dfsg-1ubuntu0.5_all.deb ...
Unpacking libgdk-pixbuf2.0-common (2.42.8+dfsg-1ubuntu0.5) over (2.42.8+dfsg-1ubuntu0.4) ...
Preparing to unpack .../45-libtiff5_4.3.0-6ubuntu0.13_amd64.deb ...
Unpacking libtiff5:amd64 (4.3.0-6ubuntu0.13) over (4.3.0-6ubuntu0.12) ...
Preparing to unpack .../46-libgdk-pixbuf-2.0-0_2.42.8+dfsg-1ubuntu0.5_amd64.deb ...
Unpacking libgdk-pixbuf-2.0-0:amd64 (2.42.8+dfsg-1ubuntu0.5) over (2.42.8+dfsg-1ubuntu0.4) ...
Preparing to unpack .../47-libgdk-pixbuf2.0-bin_2.42.8+dfsg-1ubuntu0.5_amd64.deb ...
Unpacking libgdk-pixbuf2.0-bin (2.42.8+dfsg-1ubuntu0.5) over (2.42.8+dfsg-1ubuntu0.4) ...
Preparing to unpack .../48-liblcms2-2_2.12~rc1-2ubuntu0.1_amd64.deb ...
Unpacking liblcms2-2:amd64 (2.12~rc1-2ubuntu0.1) over (2.12~rc1-2build2) ...
Preparing to unpack .../49-pkexec_0.105-33ubuntu0.1_amd64.deb ...
Unpacking pkexec (0.105-33ubuntu0.1) over (0.105-33) ...
Preparing to unpack .../50-polkitd_0.105-33ubuntu0.1_amd64.deb ...
Unpacking polkitd (0.105-33ubuntu0.1) over (0.105-33) ...
Preparing to unpack .../51-policykit-1_0.105-33ubuntu0.1_amd64.deb ...
Unpacking policykit-1 (0.105-33ubuntu0.1) over (0.105-33) ...
Preparing to unpack .../52-libpolkit-agent-1-0_0.105-33ubuntu0.1_amd64.deb ...
Unpacking libpolkit-agent-1-0:amd64 (0.105-33ubuntu0.1) over (0.105-33) ...
Preparing to unpack .../53-libpolkit-gobject-1-0_0.105-33ubuntu0.1_amd64.deb ...
Unpacking libpolkit-gobject-1-0:amd64 (0.105-33ubuntu0.1) over (0.105-33) ...
Preparing to unpack .../54-packagekit-tools_1.2.5-2ubuntu3.1_amd64.deb ...
Unpacking packagekit-tools (1.2.5-2ubuntu3.1) over (1.2.5-2ubuntu3) ...
Preparing to unpack .../55-packagekit_1.2.5-2ubuntu3.1_amd64.deb ...
Unpacking packagekit (1.2.5-2ubuntu3.1) over (1.2.5-2ubuntu3) ...
Preparing to unpack .../56-python3-cryptography_3.4.8-1ubuntu2.4_amd64.deb ...
Unpacking python3-cryptography (3.4.8-1ubuntu2.4) over (3.4.8-1ubuntu2.2) ...
Preparing to unpack .../57-python3-jwt_2.3.0-1ubuntu0.3_all.deb ...
Unpacking python3-jwt (2.3.0-1ubuntu0.3) over (2.3.0-1ubuntu0.2) ...
Preparing to unpack .../58-python3-openssl_21.0.0-1ubuntu0.1_all.deb ...
Unpacking python3-openssl (21.0.0-1ubuntu0.1) over (21.0.0-1) ...
Preparing to unpack .../59-python3-pyasn1_0.4.8-1ubuntu0.2_all.deb ...
Unpacking python3-pyasn1 (0.4.8-1ubuntu0.2) over (0.4.8-1ubuntu0.1) ...
Preparing to unpack .../60-snapd_2.75.2+ubuntu22.04_amd64.deb ...
Unpacking snapd (2.75.2+ubuntu22.04) over (2.73+ubuntu22.04) ...
Setting up liblcms2-2:amd64 (2.12~rc1-2ubuntu0.1) ...
Setting up libnftables1:amd64 (1.0.2-1ubuntu3.1) ...
Setting up nftables (1.0.2-1ubuntu3.1) ...
Setting up bsdextrautils (2.37.2-4ubuntu3.5) ...
Setting up python3-jwt (2.3.0-1ubuntu0.3) ...
Setting up distro-info-data (0.52ubuntu0.12) ...
Setting up openssh-client (1:8.9p1-3ubuntu0.15) ...
Setting up libgdk-pixbuf2.0-common (2.42.8+dfsg-1ubuntu0.5) ...
Setting up libnghttp2-14:amd64 (1.43.0-1ubuntu0.3) ...
Setting up libnetplan0:amd64 (0.107.1-3ubuntu0.22.04.3) ...
Setting up libpackagekit-glib2-18:amd64 (1.2.5-2ubuntu3.1) ...
Setting up libntfs-3g89 (1:2021.8.22-3ubuntu1.3) ...
Setting up lshw (02.19.git.2021.06.19.996aaad9c7-2ubuntu0.22.04.1) ...
Setting up xxd (2:8.2.3995-1ubuntu2.30) ...
Setting up ntfs-3g (1:2021.8.22-3ubuntu1.3) ...
Setting up tzdata (2026a-0ubuntu0.22.04.1) ...

Current default time zone: 'Asia/Seoul'
Local time is now:      Tue May 26 14:50:12 KST 2026.
Universal Time is now:  Tue May 26 05:50:12 UTC 2026.
Run 'dpkg-reconfigure tzdata' if you wish to change it.

Setting up libcap2-bin (1:2.44-1ubuntu0.22.04.3) ...
Setting up eject (2.37.2-4ubuntu3.5) ...
Setting up gir1.2-packagekitglib-1.0 (1.2.5-2ubuntu3.1) ...
Setting up vim-common (2:8.2.3995-1ubuntu2.30) ...
Setting up python3-cryptography (3.4.8-1ubuntu2.4) ...
Setting up libavahi-common-data:amd64 (0.8-5ubuntu5.5) ...
Setting up libpng16-16:amd64 (1.6.37-3ubuntu0.5) ...
Setting up sudo (1.9.9-1ubuntu2.6) ...
Setting up libssh-4:amd64 (0.9.6-2ubuntu0.22.04.7) ...
Setting up libfdisk1:amd64 (2.37.2-4ubuntu3.5) ...
Setting up mount (2.37.2-4ubuntu3.5) ...
Setting up uuid-runtime (2.37.2-4ubuntu3.5) ...
uuidd.service is a disabled or a static unit not running, not starting it.
Setting up python3-pyasn1 (0.4.8-1ubuntu0.2) ...
Setting up python3-netplan (0.107.1-3ubuntu0.22.04.3) ...
Setting up libcurl4:amd64 (7.81.0-1ubuntu1.24) ...
Setting up libtiff5:amd64 (4.3.0-6ubuntu0.13) ...
Setting up curl (7.81.0-1ubuntu1.24) ...
Setting up vim-runtime (2:8.2.3995-1ubuntu2.30) ...
Setting up openssl (3.0.2-0ubuntu1.23) ...
Setting up libpam-cap:amd64 (1:2.44-1ubuntu0.22.04.3) ...
Setting up ubuntu-pro-client (37.2ubuntu~22.04) ...
Installing new version of config file /etc/apparmor.d/ubuntu_pro_esm_cache ...
Setting up libpolkit-gobject-1-0:amd64 (0.105-33ubuntu0.1) ...
Setting up rsync (3.2.7-0ubuntu0.22.04.6) ...
rsync.service is a disabled or a static unit not running, not starting it.
Setting up libkmod2:amd64 (29-1ubuntu1.1) ...
Setting up ubuntu-pro-client-l10n (37.2ubuntu~22.04) ...
Setting up vim (2:8.2.3995-1ubuntu2.30) ...
Setting up bind9-libs:amd64 (1:9.18.39-0ubuntu0.22.04.4) ...
Setting up iproute2 (5.15.0-1ubuntu2.1) ...
Setting up python3-openssl (21.0.0-1ubuntu0.1) ...
Setting up libavahi-common3:amd64 (0.8-5ubuntu5.5) ...
Setting up libcurl3-gnutls:amd64 (7.81.0-1ubuntu1.24) ...
Setting up systemd (249.11-0ubuntu3.20) ...
Setting up vim-tiny (2:8.2.3995-1ubuntu2.30) ...
Setting up kmod (29-1ubuntu1.1) ...
Setting up libcairo2:amd64 (1.16.0-5ubuntu2.1) ...
Setting up fdisk (2.37.2-4ubuntu3.5) ...
Setting up systemd-timesyncd (249.11-0ubuntu3.20) ...
Setting up udev (249.11-0ubuntu3.20) ...
Setting up libpolkit-agent-1-0:amd64 (0.105-33ubuntu0.1) ...
Setting up libgdk-pixbuf-2.0-0:amd64 (2.42.8+dfsg-1ubuntu0.5) ...
Setting up libcairo-gobject2:amd64 (1.16.0-5ubuntu2.1) ...
Setting up ubuntu-advantage-tools (37.2ubuntu~22.04) ...
Setting up netplan-generator (0.107.1-3ubuntu0.22.04.3) ...
Setting up bind9-host (1:9.18.39-0ubuntu0.22.04.4) ...
Setting up libavahi-client3:amd64 (0.8-5ubuntu5.5) ...
Setting up snapd (2.75.2+ubuntu22.04) ...
Installing new version of config file /etc/apparmor.d/usr.lib.snapd.snap-confine.real ...
snapd.failure.service is a disabled or a static unit not running, not starting it.
snapd.gpio-chardev-setup.target is a disabled or a static unit not running, not starting it.
snapd.snap-repair.service is a disabled or a static unit not running, not starting it.
Setting up systemd-sysv (249.11-0ubuntu3.20) ...
Setting up libnss-systemd:amd64 (249.11-0ubuntu3.20) ...
Setting up netplan.io (0.107.1-3ubuntu0.22.04.3) ...
Setting up libgdk-pixbuf2.0-bin (2.42.8+dfsg-1ubuntu0.5) ...
Setting up libpam-systemd:amd64 (249.11-0ubuntu3.20) ...
Setting up bind9-dnsutils (1:9.18.39-0ubuntu0.22.04.4) ...
Setting up polkitd (0.105-33ubuntu0.1) ...
Setting up pkexec (0.105-33ubuntu0.1) ...
Setting up policykit-1 (0.105-33ubuntu0.1) ...
Setting up packagekit (1.2.5-2ubuntu3.1) ...
Setting up packagekit-tools (1.2.5-2ubuntu3.1) ...
Processing triggers for libc-bin (2.35-0ubuntu3.13) ...
Processing triggers for man-db (2.10.2-1) ...
Processing triggers for dbus (1.12.20-2ubuntu4.1) ...
Processing triggers for install-info (6.8-4build1) ...
Processing triggers for hicolor-icon-theme (0.17-2) ...
dministrator@DESKTOP-C2MQEL4:~$ sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"
Successfully installed brev CLI to /root/.local/bin/brev

Warning: /root/.local/bin is not in your PATH.
Add it by appending the following line to your shell profile (e.g. ~/.bashrc, ~/.zshrc):
    export PATH="${HOME}/.local/bin:${PATH}"
Then restart your shell or run 'source' on the profile to pick up the change.
dministrator@DESKTOP-C2MQEL4:~$ echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc
source ~/.bashrc
dministrator@DESKTOP-C2MQEL4:~$ brev --version
Current Version: v0.6.326
dministrator@DESKTOP-C2MQEL4:~$ brev login

   ▸     Starting Login

Logging in with email allai12@allai.co.kr
Press enter to continue or type a different email: allai12@allai.co.kr
Login here: https://api.ngc.nvidia.com/login?code=eb1f572d4bbe2b3785948272f13c37d3ac74b5321ad0682fd4450250479667e8&redirect_uri=https%3A%2F%2Fbrev.nvidia.com%2Fcli-login&email=allai12%40allai.co.kr

Waiting for login to complete...

   ▸    Successfully logged in.
current organization: ALLAI
switch organizations:
        brev set allai12-1-1x8e
list your instances:
        brev ls
dministrator@DESKTOP-C2MQEL4:~$
```

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
