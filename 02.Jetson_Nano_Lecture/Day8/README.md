하드웨어 진단
항목	상태
RTX 5090 (Blackwell)	✅ 문제없음. 단, 최신 NVIDIA 드라이버 필수 (v570 이상)
RAM 24GB	⚠️ Isaac Sim 권장 RAM은 32GB 이상. 간단한 scene은 가능하지만, 복잡한 시뮬레이션/Idealab 사용시 부족할 수 있음
Ubuntu 22.04	✅ 공식 지원 버전
디스크 여유공간	Isaac Sim 설치 시 ~30GB 이상 필요 (설치 후 더 커질 수 있음)
설치 단계
1. NVIDIA 드라이버 설치 (RTX 5090 필수)
RTX 5090은 Blackwell 아키텍처이므로 드라이버 v570 이상이 반드시 필요합니다.

# 사용 가능한 드라이버 확인
ubuntu-drivers devices

# 최신 드라이버 설치 (570 권장)
sudo apt install nvidia-driver-570
# 또는 nvidia-driver-570-open (laptop hybrid graphics면 open 버전 고려)

# 재부팅
sudo reboot

# 확인
nvidia-smi
노트북 hybrid graphics: 노트북이라면 nvidia-driver-570-open이 더 잘 맞을 수 있습니다. nvidia-smi에 RTX 5090이 잡히는지 확인하세요.

2. GCC/G++ 11 설정
sudo apt update
sudo apt install build-essential gcc-11 g++-11

# GCC 11을 시스템 기본으로
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200

# 확인
gcc --version   # 11.x.x 확인
3. 기타 의존성
sudo apt install libegl1 libvulkan1 rsync python3 pip
4. Isaac Sim 설치
다운로드한 파일 형식에 따라:

A) tar.xz / tar.gz 압축파일인 경우:

cd ~/Downloads   # 다운로드 위치
# tar.xz
tar -xf IsaacSim-5.1.0-*-linux-x86_64.tar.xz
# 또는 tar.gz
tar -xzf IsaacSim-5.1.0-*-linux-x86_64.tar.gz

mv IsaacSim-5.1.0 ~/isaacsim
cd ~/isaacsim

# 호환성 체크 (권장)
./isaac-sim.compatibility_check.sh

# 실행
./isaac-sim.sh
B) GitHub에서 git clone한 경우:

cd ~/isaacsim
git lfs install
git lfs pull
./build.sh
cd _build/linux-x86_64/release
./isaac-sim.sh
RAM 24GB 관련 팁
RAM이 24GB이므로 실행 시 다음 옵션을 고려하세요:

# 간단한 scene 실행 (권장)
./isaac-sim.sh

# 복잡한 scene / Isaac Lab 사용시 swap 확보
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# headless 모드로 실행 (GUI 없이, RAM 절약)
./isaac-sim.sh --no-window
요약
✅ Ubuntu 22.04 + RTX 5090 = 훌륭한 GPU 성능
⚠️ RAM 24GB = 간단한 시뮬레이션 위주로 사용 권장
⚠️ NVIDIA Driver v570+ 필수 (RTX 5090 지원)
다운로드하신 파일이 정확히 어떤 형식인지(tar.xz, git clone, 또는 다른 방식) 알려주시면 해당 부분을 더 구체적으로 도와드릴 수 있습니다.