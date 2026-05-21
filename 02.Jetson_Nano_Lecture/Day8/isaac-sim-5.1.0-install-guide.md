# Isaac Sim 5.1.0 설치 가이드 (Ubuntu 22.04 + RTX 5090)

> 작성일: 2026-05-21
> 대상 환경: 노트북, RTX 5090 (Blackwell), RAM 24GB, Ubuntu 22.04

---

## 1. 시스템 요구사항

| 항목 | 내 환경 | 상태 |
|---|---|---|
| OS | Ubuntu 22.04 | ✅ 지원 |
| GPU | RTX 5090 (Blackwell) | ✅ 문제없음 |
| NVIDIA Driver | **v570 이상 필수** (RTX 5090 지원) | ⚠️ 설치 필요 |
| GCC/G++ | **버전 11 필수** (12+ 불가) | ⚠️ 설정 필요 |
| RAM | 24GB | ⚠️ 최소 16GB 이상, 권장 32GB 미달 → 간단한 scene 위주 권장 |
| 디스크 | 최소 30GB+ 여유 공간 | ✅ 확인 필요 |

---

## 2. 사전 설치 (Ubuntu 22.04)

```bash
# NVIDIA 드라이버 설치 (RTX 5090 = v570+)
ubuntu-drivers devices
sudo apt install nvidia-driver-570
# 또는 노트북 hybrid graphics: sudo apt install nvidia-driver-570-open

# 재부팅 후 확인
sudo reboot
nvidia-smi

# GCC/G++ 11
sudo apt update
sudo apt install build-essential gcc-11 g++-11
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200
gcc --version   # 11.x.x 확인

# 기타 의존성
sudo apt install libegl1 libvulkan1 rsync python3 python3-pip
```

---

## 3. Isaac Sim 5.1.0 설치

### A) 바이너리 아카이브 (tar.xz) 를 다운로드한 경우

```bash
# 압축 해제
cd ~/Downloads
tar -xf IsaacSim-5.1.0-*-linux-x86_64.tar.xz

# 적당한 위치로 이동
mv IsaacSim-5.1.0 ~/isaacsim
cd ~/isaacsim

# 호환성 체크 (실행 전 권장)
./isaac-sim.compatibility_check.sh

# 실행
./isaac-sim.sh
```

### B) GitHub 소스 클론한 경우

```bash
git clone https://github.com/isaac-sim/IsaacSim.git ~/isaacsim
cd ~/isaacsim
git lfs install
git lfs pull
./build.sh
cd _build/linux-x86_64/release
./isaac-sim.sh
```

```
(base) gotree94@gotree94-ROG-Strix-SCAR-16-G635LX-G635LX:~/isaacsim$ ./build.sh
Script dir: /home/gotree94/isaacsim
/home/gotree94/isaacsim/tools/packman/packman: line 2: $'\r': command not found

```

---

## 4. 실행 명령어

| 명령어 | 설명 |
|---|---|
| `./isaac-sim.sh` | GUI 모드 실행 |
| `./isaac-sim.sh /path/to/scene.usd` | 특정 USD scene 로드 |
| `./isaac-sim.sh --no-window` | Headless 모드 (RAM 절약) |
| `./python.sh /path/to/script.py` | Python 스크립트 실행 |
| `./isaac-sim.compatibility_check.sh` | 호환성 진단 |

---

## 5. RAM 24GB 대비 권장 사항

RAM이 24GB로 권장(32GB)에 약간 미달하므로:

```bash
# SWAP 파일 확보 (권장)
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# /etc/fstab 에 추가해서 영구 적용
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

| 상황 | 권장 |
|---|---|
| 간단한 scene 탐색 | ✅ 문제없음 |
| 복잡한 시뮬레이션 | ⚠️ headless 모드 권장 |
| Isaac Lab / RL 학습 | ⚠️ RAM 부족할 수 있음 |
| 고해상도 RTX 렌더링 | ⚠️ 해상도 낮춰서 실행 |

---

## 6. 문제 해결

| 증상 | 해결 |
|---|---|
| `GLIBC_2.35` 에러 | Ubuntu 22.04 사용중이면 문제없음. 다른 버전이면 22.04 권장 |
| `libEGL` 에러 | `sudo apt install libegl1` |
| Vulkan/GPU 초기화 실패 | `sudo apt install libvulkan1`, 드라이버 재확인 |
| `GCC` 버전 에러 | `gcc --version` 확인, update-alternatives로 11로 설정 |
| 실행 후 바로 종료됨 | `./isaac-sim.compatibility_check.sh` 로 원인 진단 |
| RTX 5090 인식 안 됨 | `nvidia-smi` 확인. 드라이버 v570+ 인지 확인 |
| GUI 출력 안 됨 | 노트북인 경우 `prime-select` 확인: `sudo prime-select nvidia` |

---

## 7. 참고 링크

- Isaac Sim 5.1.0 공식 문서: https://docs.isaacsim.omniverse.nvidia.com/5.1.0/
- GitHub 저장소: https://github.com/isaac-sim/IsaacSim
- NVIDIA Isaac Sim 다운로드: https://developer.nvidia.com/isaac/sim
- 성능 최적화 핸드북: https://docs.isaacsim.omniverse.nvidia.com/latest/reference_material/sim_performance_optimization_handbook.html
