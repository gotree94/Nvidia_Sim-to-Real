Jetpack Library
▪  Jetson용 AI 핵심 S/W 라이브러리
▪  구성요소
•   GPU 가속을 위한 CUDA(Compute Unified Device Architecture)
•   Jetson CUDA를 활용한 TensorRT 및 cuDNN(CUDA Deep Neural Network) 라이브러리 및 샘플코드
•   멀티미디어 API 패키지 (VPI (vision 프로그래밍 인터페이스) 및 OpenCV 등)
Jetpack Library 설치
▪  NVIDIA SDK Manager를 통해서 설치 (dev kit만)
▪ Commercial(예: JCB100) 보드의 경우 Linux repository를 통해서 설치
•   $ sudo apt install NVIDIA-jetpack 
•   ‘jetson_release’ 도구를 통해서 설치여부 확인 가능
NVIDIA-jetpack Library 설치 전
NVIDIA-jetpack Library 설치 후CUDA Enabled OpenCV
▪  NVIDIA 제공 OpenCV 패키지 또는 스크립트를 통해서 설치 가능
(https://github.com/mdegans/nano_build_opencv )
▪  최신 OpenCV 소스 코드 이용 시 ‘CUDA’, ‘DNN_CUDA’등 옵션 활성화 후 빌드
▪ 이후 OpenCV내 CUDA활용 sample code 및 라이브러리 활용 가능 (예: opencv_dnn) 
$ cmake -D WITH_CUDA=ON \
-D ENABLE_PRECOMPILED_HEADERS=OFF \ -D WITH_GSTREAMER=ON \
……
…… 
-D WITH_CUDNN=ON \
-D CUDA_FAST_MATH=ON \ -D OPENCV_DNN_CUDA=ON \
……
……
Jetson CUDA Enabled Tensorflow
▪    Jetpack version에 따른 CUDA Enabled Tensorflow 제공
•     NVIDIA Developer 다운로드 페이지를 통해서 설치
•     $ sudo pip3 install --extra-index-url https://developer.download.NVIDIA.com/compute/redist/jp/v512  tensorflow==2.12.0+nv23.06
▪    최신 TensorFlow 릴리스 목록과 해당 패키지 이름, NVIDIA 컨테이너 및 Jetpack 호환성은 ‘Jetson 플랫폼용 TensorFlow 릴리스 노트’에서 확인 가능
•     https://docs.NVIDIA.com/deeplearning/frameworks/install-tf-jetson-platform-release-notes/index.html
▪    ‘Tensorflow’ GPU 사용 여부 확인 (터미널 에서 python실행 후 확인) 
▪    ‘True’가 출력되면 GPU 사용Jetson’s PyTorch
▪    ‘PyTorch’(for Jetpack)은 Jetson의 GPU와 CPU에 최적화된 Tensor 라이브러리 제공
▪    높은 수준의 유연성과 빠른 성능을 지원하며 ‘Accelerated NumPy’와 같은 유사 기능 제공
▪    NVIDIA Developer site에서 Jetson/Jetpack에 따른 패키지(wheel) 제공
$ export TORCH_INSTALL=https://developer.download.NVIDIA.cn/compute/redist/jp/v511/pytorch/torch-2.0.0+nv23.05-cp38- cp38-linux_aarch64.whl
$ python3 -m pip install --upgrade pip
$ python3 -m pip install numpy==’1.26.1’
$ python3 -m pip install --no-cache $TORCH_INSTALL
▪    Jetson 용 PyTorch 확인
$ python3 
>>> import torch
>>> torch.cuda.is_available()
True
>>> torch.backends.cudnn.version()
8600
Jetson stats
▪  NVIDIA Jetson 플랫폼에서 시스템 상태를 모니터링하고 관리하는 도구
▪  Jetson 장치의 CPU, GPU, 메모리 사용량 등을 실시간으로 확인하고, 다양한 관리 작업을 수행할 수 있는 직관적인 인터페이스 제공
▪  Jetson 장치의 성능을 최적화하고, 리소스 사용을 효율적으로 관리하는데 사용
▪  설치
•   $ sudo apt-get install python3-pip 
•   $ sudo -H pip3 install -U jetson-stats
▪  ‘jtop’, ‘jetson_release’, ‘jetson_config’, ‘jetson_swap’ 등의 도구 포함jtop
Jetson 정보 Memory
CPU
GPU
프로세스 정보 그 외 정보
jtop - GPUjtop - CPU
jtop - Memoryjtop - engine
jtop - controljtop - information
jetson releaseJetson 시스템 상태 (온도) 확인
▪  현재 시스템 온도를 확인 가능
▪  출력 값에서 1000을 나눈 값이 온도
46000/1000 = 약 46도
With CUDA vs W/O CUDA
▪ With CUDA & Without CUDA 비교 데모 동영상
< 발췌 : JetsonHack, https://www.youtube.com/watch?v=art0-99fFa8 >
Website: http://jetsonhacks.com 
Github: https://github.com/jetsonhacksnano