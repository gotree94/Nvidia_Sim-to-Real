# Isaac Sim 5.1.0 설치 가이드 (Ubuntu 22.04 + RTX 5090)

> 대상 환경: **노트북 ROG Strix SCAR 16 (G635LX)**
> **GPU**: RTX 5090 | **RAM**: 24GB | **OS**: Ubuntu 22.04
> **User**: gotree94 | **설치 방식**: **Git clone → build.sh 빌드**

---

## 1. 사전 준비

```bash
cd /home/gotree94

sudo apt update
sudo apt install build-essential gcc-11 g++-11 libegl1 libvulkan1 rsync python3 python3-pip git-lfs

# GCC 11 고정
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200
gcc --version   # 11.x.x 확인
```

---

## 2. NVIDIA 드라이버 (RTX 5090 = Blackwell, v570+ 필수)

```bash
ubuntu-drivers devices
sudo apt install nvidia-driver-570     # 또는 nvidia-driver-570-open (hybrid)
sudo reboot
nvidia-smi   # RTX 5090, Driver 570.x 확인
```

---

## 3. 소스 빌드

```bash
cd /home/gotree94/isaacsim

# git LFS 대용량 파일 (필수)
git lfs install
git lfs pull

# CRLF 개행문자 변환 (Windows에서 받은 경우)
sed -i 's/\r$//' tools/packman/packman
find . -name "*.sh" -exec sed -i 's/\r$//' {} \;

# 빌드 (30분~1시간 소요)
./build.sh
```

---

## 4. 실행

```bash
cd /home/gotree94/isaacsim

./isaac-sim.sh                          # GUI 실행
./isaac-sim.sh --no-window              # Headless (RAM 절약)
./python.sh my_script.py                # Python 스크립트
./isaac-sim.compatibility_check.sh      # 호환성 진단
```

---

## 5. RAM 24GB → SWAP 설정 (필수)

```bash
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 6. 문제 해결

| 증상 | 원인 / 해결 |
|---|---|
| `git: 'lfs' is not a git command` | git-lfs 미설치 → `sudo apt install git-lfs` |
| `$'\r': command not found` | CRLF 개행문자 → `sed -i 's/\r$//' tools/packman/packman` |
| `GCC` 버전 에러 | `gcc --version` 11 확인, update-alternatives 실행 |
| 빌드 중 `killed` (OOM) | RAM 부족 → SWAP 설정 필수 (5번) |
| `nvidia-smi` 실행 안 됨 | 드라이버 미설치 → 2번 실행 |
| `libEGL` / Vulkan 에러 | `sudo apt install libegl1 libvulkan1` |
| OpenGL/X11 에러 (노트북) | `sudo prime-select nvidia` |

---

## 7. 링크

- 공식 문서: https://docs.isaacsim.omniverse.nvidia.com/5.1.0/
- GitHub: https://github.com/isaac-sim/IsaacSim
