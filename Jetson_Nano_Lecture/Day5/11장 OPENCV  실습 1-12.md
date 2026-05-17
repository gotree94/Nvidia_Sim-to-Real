OPENCV
Computer vision
▪  컴퓨터를 이용하여 정지 영상 또는 동영상으로부터 의미 있는 정보를 추출하는 방법을 연구하는 학문
▪  사람이 눈으로 사물을 보고 인지하는 작업을 컴퓨터가 동등하게 수행할 수 있게끔 연구 하는 학문
▪  사람의 눈이 하는 작업을 카메라가 대신하고, 사람의 뇌가 하는 작업을 수학적 알고리즘을 통해 컴퓨터가 유사하게 수행할 수 있도록 만드는 작업
▪  주로 밝기, 색상, 모양, 텍스처 등의 영상 정보 활용What is OpenCV?
▪  Open Source Computer Vision Library
▪  컴퓨터 비전과 이미지 처리 응용 프로그램을 개발하기 위한 오픈 소스 라이브러리
▪  다양한 언어(C++, Python, Java, MATLAB)를 지원하고, 크로스 플랫폼에서 사용 가능
▪ 많은 함수가 하드웨어 가속을 지원하며, GPU를 이용한 실시간 어플리케이션에도 적합
주요 기능
▪   이미지 처리
•    필터링(블러, 샤프닝, 경계 검출 등)
•    히스토그램 계산 및 equalization
•    컬러 변환(RGB ↔ Grayscale, HSV 등), 이미지 리사이징, 회전, 크롭
▪   비디오 처리
•    실시간 카메라 스트리밍 처리, 프레임 추출 및 저장, 영상 코덱 지원 및 비디오 파일 입출력
▪   객체 탐지(Object Detection)
•    얼굴 탐지(Haar cascade, DNN), 사람, 차량 탐지 (YOLO, SSD 등과 연동), 배경 제거, 모션 감지
▪   컴퓨터 비전 알고리즘
•    윤곽선 검출(contour), 엣지(Edge) 검출(Canny 등), 코너 검출(Harris, Shi-Tomasi), 특징점 추출(SIFT, SURF, ORB 등)
•    카메라 캘리브레이션, 스테레오 매칭, 깊이 추정
▪   딥러닝 연동
•    OpenCV DNN 모듈을 통해 ONNX, Caffe, TensorFlow, Darknet 모델 로드 가능
•    YOLO, SSD, MobileNet 등 실시간 객체 탐지 구현 가능OpenCV Library
▪  OpenCV 라이브러리는 다수의 모듈로 구성
•    calib3d : 카메라 캘리브레이션과 3차원 재구성
•    core : 행렬, 벡터 등 OpenCV 핵심 클래스와 연산 함수
•    dnn : 심층 신경망 기능
•    features2d : 2차원 특징 추출과 특징 벡터 기술, 매칭 방법
•    flann : 다차원 공간에서 빠른 최근방 이웃 검색
•    highgui : 영상의 화면 출력, 마우스 이벤트 처리 등 사용자 인터페이스
•    imgcodecs : 영상 파일 입출력
•    imgproc : 필터링, 기하학적 변환, 색 공간 변환 등 영상 처리 기능
•    ml : 통계적 분류, 회귀 등 머신 러닝 알고리즘
•    objdetect : 얼굴, 보행자 검출 등 객체 검출
•    photo : HDR, 잡음 제거 등 사진 처리 기능
•    stitching : 영상 이어 붙이기
•    video : 옵티컬 플로우, 배경 차분 등 동영상 처리 기술
•    videoio : 동영상 파일 입출력
•    world : 여러 OpenCV 모듈을 포함하는 하나의 통합 모듈
OpenCV 파이썬 코드 예시
▪   이미지 edge 검출OpenCV 파이썬 코드 예시
▪   실시간 카메라 영상 출력
OpenCV
▪  OpenCV 설치
•   $ pip3 install opencv-python
•   $ pip3 install opencv-contrib-python
▪  OpenCV Cmake 옵션
•   https://docs.opencv.org/4.10.0/db/d05/tutorial_config_reference.html
▪  OpenCV tutorial
•   https://docs.opencv.org/4.x/d9/df8/tutorial_root.html
▪  OpenCV github
•   https://github.com/opencv/opencv
▪   OpenCV documentation
•   https://docs.opencv.org/
•   https://docs.opencv.org/4.10.0/Jetson Nano OpenCV
▪  Jetson Library를 설치할 때 기본적으로 CUDA, cuDNN, TensorRT, OpenCV 등의 라이브러리 설치 되지만, OpenCV는 CUDA를 사용하지 않는 OpenCV로 설치
▪  CUDA를 사용하는 OpenCV를 설치하기 위해 OpenCV는 소스를 직접 빌드해서 설치
Jetson Nano에서 OpenCV build 할 때 Swap 사용
▪  Swap은 컴퓨터 시스템에서 사용되는 메모리 관리 기법으로, 주 메모리(RAM)의 공간이 부족할 때 보조 저장 장치(HDD 또는 SSD)의 일부를 임시 메모리로 사용하는 것을 의미
▪  OpenCV 전체 빌드에는 약 8GB 이상의 램이 필요하며, Jetson Nano는 4GB의 램을 가지고 있기 때문에 swap 공간 할당 필요
▪  dphys-swapfile을 이용하여 swap 파일 사용
<https://recoverhdd.com/blog/swap-file-in-windows.html>Jetson Nano Camera 사용
▪ 로지텍 C270 카메라를 이용해서 Jetson Nano에서 실시간으로 OpenCV 코드 실행 가능
OpenCV DNN
▪  OpenCV DNN (deep neural network)
▪  OpenCV에 내장된 다양한 심층 학습 모델을 사용 하여 얼굴 감지와 같은 작업 수행 가능
▪  딥러닝 학습은 기존의 유명한 카페(caffe), 텐서플 로(tensorflow)등의 다른 딥러닝 프레임워크에서 진행하고, 학습된 모델을 불러와서 실행할 때에는 dnn 모듈을 사용하는 방식


실습 1-12 
- Jetson Nano에서 OpenCV with CUDA 설 치 및 사용실습 1-12: Jetson Nano 에서 OpenCV with CUDA 설치 및 사용
OpenCV(open source computer vision library)는 컴퓨터 비전과 이미지 처리 작업을
수행하는데 널리 사용되는 라이브러리입니다.
Jetson Nano 에서 Jetson-library 를 설치하면 기본적으로 CUDA, cuDNN, TensorRT, OpenCV 등의 라이브러리가 함께 설치됩니다. 그러나 기본적으로 제공되는 OpenCV 는 CUDA 를 지원하지 않는 버전이기 때문에, CUDA 가속이 적용된 OpenCV 로 교체하는 과정이 필요합니다. 이를 위해, 기존에 설치된 OpenCV 를 제거한 후, CUDA 를 지원하는 OpenCV 를 재설치하는 과정을 먼저 진행한 후 OpenCV 실습을 진행합니다.
Jetson Nano 에서 OpenCV 를 빌드할 때, CUDA 가속을 활성화하려면 CMake 옵션을 적절하게 설정해야 합니다. 이 때, 필수적으로 포함해야 할 주요 CMake 옵션은 다음과 같습니다.
CMake 옵션
설명
WITH_CUDA=ON
OpenCV 의 CUDA 지원을 활성화하여 GPU 가속 기능을 사용할 수 있도록 설정
CUDA_ARCH_BIN=”5.3”
Jetson Nano 의 Maxwell GPU(Compute Capability 5.3)에서 실행 가능하도록 CUDA 커널을 컴파일
WITH_CUDNN=ON
딥러닝 가속 라이브러리 활성화하여, YOLO, SSD, Faster R-CNN 같은 모델을 OpenCV 에서 실행할 때 GPU 가속을 지원
WITH_CUBLAS=ON
CUDA 기반의 행렬 연산 라이브러리(cuBLAS) 활성화하여 고속 행렬 연산 수행
ENABLE_FAST_MATH=ON
CUDA 연산에서 빠른 수학 연산(Fast Math)을 활성화하여 실행 속도를 높임
CUDA_FAST_MATH=ON
ENABLE_FAST_MATH=ON 과 유사하지만, 특정 CUDA 연산에서 추가적인 최적화를 수행OPENCV_DNN_CUDA=ON
OpenCV 의 딥러닝 모듈(cv::dnn)이 GPU 에서 실행될 수 있도록 설정하여 딥러닝 모델 추론 속도 향상
OPENCV_EXTRA_MODULES_PATH =../../opencv_contrib-4.5.1/modules
opencv_contrib 모듈을 추가하여 CUDA 기반의 다양한 추가 기능을 사용할 수 있도록 확장
Jetson Nano 에서 OpenCV 를 직접 빌드할 경우 2~3 시간 정도의 시간이 소요되므로, 이미 빌드된 OpenCV 폴더를 가져와 install 명령어를 사용하여 설치하는 방식을
활용합니다.
▪    jetson_release 로 기존에 설치 된 OpenCV 버전을 확인합니다.
$ jetson_releaseOpenCV 직접 Build 방법
(참고용/읽고 넘어가기)
Build 방식은 참고용입니다. (Jetson nano 에서는 OpenCV 소스코드 빌드 소요 시간이 오래 걸립니다. 이러한 이유로 빌드 과정은 읽고 넘어갑니다.)
실제 실습은 아래에 있는 ‘OpenCV Install’ 부터 시작합니다.
OpenCV 를 Jetson Nano 에서 직접 빌드 및 설치하려면 약 (8GB 이상의 RAM 이
필요하며, Jetosn Nano 는 RAM 이 4GB 이기 때문에 swap 공간을 할당해주어야 합니다.)
▪    dphys-swapfile 를 설치합니다.
$ sudo apt-get install dphys-swapfile
▪    /sbin/dphys-swapfile 수정
$ sudo vi /sbin/dphys-swapfile
CONF_SWAPSIZE=4096
CONF_SWAPFACTOR=2
CONF_MAXSWAP=4096▪    /etc/dphys-swapfile 주석 해제 및 수정
$ sudo vi /etc/dphys-swapfile
CONF_SWAPSIZE=4096
CONF_SWAPFACTOR=2
CONF_MAXSWAP=4096
▪    reboot 합니다.
$ sudo reboot
▪    swap 확인
$ free -m
à swap 6074 정도로 출력되면 됩니다.
▪ 기존에 깔려있던 OpenCV 를 삭제합니다.
$ sudo apt purge libopencv-dev libopencv-python libopencv-samples libopencv*▪    OpenCV 가 남아있는지 확인합니다. jetson_release 명령어로도 OpenCV 가 삭제되었는지 확인합니다.
$ pkg-config --modversion opencv4
$ jetson_release
▪    패키지 업데이트 및 필요한 패키지를 설치합니다.
$ sudo apt update
$ sudo apt install -y python3-pip python-dev python3-dev python-numpy python3-
numpy
$ sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/NVIDIA-tegra.conf"
$ sudo apt install -y qt5-default
$ sudo apt install -y build-essential cmake git unzip pkg-config libswscale-dev
$ sudo apt install -y libcanberra-gtk* libgtk2.0-dev$ sudo apt install -y libtbb2 libtbb-dev libavresample-dev libvorbis-dev libxine2-
dev
$ sudo apt install -y curl
▪    사진, 비디오 포맷 관련된 패키지를 설치합니다.
$ sudo apt install -y libxvidcore-dev libx264-dev libgtk-3-dev
$ sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
$ sudo apt install -y libmp3lame-dev libtheora-dev libfaac-dev libopencore-
amrnb-dev
$ sudo apt install -y libopencore-amrwb-dev libopenblas-dev libatlas-base-dev
$ sudo apt install -y libblas-dev liblapack-dev libeigen3-dev libgflags-dev
$ sudo apt install -y protobuf-compiler libprotobuf-dev libgoogle-glog-dev 
$ sudo apt install -y libavcodec-dev libavformat-dev gfortran libhdf5-dev
$ sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
$ sudo apt install -y libv4l-dev v4l-utils qv4l2 v4l2ucp libdc1394-22-dev
▪    opencv & contrib modules 을 설치 및 압축 해제합니다. # 현재 경로 : ~
$ curl -L https://github.com/opencv/opencv/archive/4.5.1.zip -o opencv-4.5.1.zip
$ curl -L https://github.com/opencv/opencv_contrib/archive/4.5.1.zip -o 
opencv_contrib-4.5.1.zip
$ unzip opencv-4.5.1.zip
$ unzip opencv_contrib-4.5.1.zip
▪    opencv-4.5.1 폴더에서 Build 폴더를 생성하고 build 폴더로 이동합니다.
$ cd opencv-4.5.1/
$ mkdir build
$ cd build
▪    CMake 를 사용하여 빌드 구성을 정의합니다.
$ cmake -D WITH_CUDA=ON \
-D ENABLE_PRECOMPILED_HEADERS=OFF \
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.5.1/modules \
-D WITH_GSTREAMER=ON \-D WITH_LIBV4L=ON \
-D BUILD_opencv_python2=ON \
-D BUILD_opencv_python3=ON \
-D BUILD_TESTS=ON \
-D BUILD_PERF_TESTS=OFF \
-D BUILD_EXAMPLES=OFF \
-D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
-D CUDA_ARCH_BIN="5.3" \
-D CUDA_ARCH_PTX="" \
-D WITH_CUDNN=ON \
-D WITH_CUBLAS=ON \
-D ENABLE_FAST_MATH=ON \
-D CUDA_FAST_MATH=ON \
-D OPENCV_DNN_CUDA=ON \
-D ENABLE_NEON=ON \
-D WITH_QT=OFF \
-D WITH_OPENMP=ON \
-D WITH_OPENGL=ON \
-D BUILD_TIFF=ON \
-D WITH_FFMPEG=ON \
-D WITH_TBB=ON \
-D BUILD_TBB=ON \
-D WITH_EIGEN=ON \
-D WITH_V4L=ON \
-D OPENCV_ENABLE_NONFREE=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D BUILD_opencv_python3=TRUE \
-D OPENCV_GENERATE_PKGCONFIG=ON ..
▪    OpenCV 를 빌드합니다. nproc 명령어로 코어 개수를 확인하고 코어 개수에 따라 옵션을 주세요. OpenCV 빌드는 약 2 시간정도 걸립니다.$ nproc
$ make -j4
▪    빌드가 완료되면 다음 명령어로 OpenCV 를 설치합니다.
$ sudo make install
▪    설치가 완료되면 시스템이 설치한 라이브러리를 인식할 수 있도록 다음 명령어를 실행하여 라이브러리 캐시를 업데이트 합니다.
$ sudo ldconfigOpenCV Install
(시간 관계상 여기부터 시작합니다)
이미 빌드 된 OpenCV 폴더를 가져와 install 명령어를 사용하여 설치하는 방식을 활용합니다.
Swap 공간 할당
▪    dphys-swapfile 를 설치합니다.
$ sudo apt-get install dphys-swapfile
▪    /sbin/dphys-swapfile 수정
$ sudo vi /sbin/dphys-swapfile
CONF_SWAPSIZE=4096
CONF_SWAPFACTOR=2
CONF_MAXSWAP=4096▪    /etc/dphys-swapfile 주석 해제 및 수정
$ sudo vi /etc/dphys-swapfile
CONF_SWAPSIZE=4096
CONF_SWAPFACTOR=2
CONF_MAXSWAP=4096
▪    reboot 합니다.
$ sudo reboot
▪    swap 확인
$ free -m
à swap 6074 정도로 출력되면 됩니다.▪    기존에 설치 되어있던 OpenCV 를 삭제합니다.
$ sudo apt purge libopencv-dev libopencv-python libopencv-samples libopencv*
▪    OpenCV 가 남아있는지 확인합니다. jetson_release 명령어로도 OpenCV 가 삭제되었는지 확인합니다.
$ pkg-config --modversion opencv4
$ jetson_release
▪    패키지 업데이트 및 필요한 패키지를 설치합니다.
$ sudo apt update
$ sudo apt install -y python3-pip python-dev python3-dev python-numpy python3-
numpy
$ sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/NVIDIA-tegra.conf"
$ sudo apt install -y qt5-default
$ sudo apt install -y build-essential cmake git unzip pkg-config libswscale-dev
$ sudo apt install -y libcanberra-gtk* libgtk2.0-dev$ sudo apt install -y libtbb2 libtbb-dev libavresample-dev libvorbis-dev libxine2-
dev
$ sudo apt install -y curl
▪    사진, 비디오 포맷 관련된 패키지를 설치합니다.
$ sudo apt install -y libxvidcore-dev libx264-dev libgtk-3-dev
$ sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
$ sudo apt install -y libmp3lame-dev libtheora-dev libfaac-dev libopencore-
amrnb-dev
$ sudo apt install -y libopencore-amrwb-dev libopenblas-dev libatlas-base-dev
$ sudo apt install -y libblas-dev liblapack-dev libeigen3-dev libgflags-dev
$ sudo apt install -y protobuf-compiler libprotobuf-dev libgoogle-glog-dev 
$ sudo apt install -y libavcodec-dev libavformat-dev gfortran libhdf5-dev
$ sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
$ sudo apt install -y libv4l-dev v4l-utils qv4l2 v4l2ucp libdc1394-22-dev
(참고: 실습자료를 복사할 경우 복사가 잘 안될 수 있습니다. 실습자료로 제공된 opencv_install.txt 파일을 참고하세요.)
▪    사전 빌드 된 ’opencv-4.5.1.tar.gz’ 파일을 Jetson Nano 홈 디렉토리(‘~’)에 복사하여 넣고, 아래 명령어로 압축 해제합니다.
(’opencv-4.5.1.tar.gz’  파일을 USB disk 또는 원격 연결된 Visual Studio code 를 이용해서 Jetson Nano 에 복사하여 놓습니다.)
$ tar -xvzf opencv-4.5.1.tar.gz
▪    opencv-4.5.1/build 경로로 이동합니다.
$ cd opencv-4.5.1/build/
▪    아래 명령어로 사전 빌드된 OpenCV 패키지를 설치합니다.
$ sudo make install
(참고: 사전에 설치하는 패키지가 제대로 설치가 안됐을 경우 OpenCV 패키지를 설치할 때 빌드로 넘어가서 시간이 오래 걸리거나 에러가 나는 경우가 있을 수 있습니다. 그럴 경우 ‘Ctrl + C ‘를 눌러 install 을 중단하고, 패키지를 제대로 설치한 후에 진행해야 합니다. 단, 100%에서 오래 걸리는 건 기다려 주시기 바랍니다.)▪    설치가 완료되면 시스템이 설치한 라이브러리를 인식할 수 있도록 다음 명령어를 실행하여 라이브러리 캐시를 업데이트 합니다.
$ sudo ldconfig
OpenCV with CUDA 설치 확인 (Jetson_release)
▪ CUDA 를 사용하는 OpenCV 가 잘 설치 되었는지 확인합니다.
$ jetson_release
Swap 제거
▪ Swap 을 제거합니다.
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo apt-get remove --purge dphys-swapfileOPENCV C++
Build 된 OpenCV 를 c++ 에서 사용하기 위해 코드를 작성한 후 cmake 를 통해 빌드한 뒤 실행합니다. OpenCV 의 간단한 예제를 통해 C++ 환경에서 OpenCV 를 어떻게
활용할 수 있는지 살펴보겠습니다.
OPENCV VERSION
▪    OpenCV 버전을 출력하는 코드를 작성하여 cmake 로 빌드 후 실행해보겠습니다.
(실습코드 경로: opencv_ex/opencv_cpp/opencv_version/opencv_version.cpp)
#include "opencv2/opencv.hpp"
int main(int argc, char** argv) {
printf("OpenCV version : %s\n", CV_VERSION); return 0;
}
▪    CMakeLists.txt 를 작성합니다.
cmake_minimum_required(VERSION 3.0)
project(opencv_version)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS}) add_executable(opencv_version opencv_version.cpp) target_link_libraries(opencv_version ${OpenCV_LIBS})
▪    CMakeLists.txt 설명
•      cmake_minimum_required(VERSION 3.0) - 프로젝트를 빌드하는데 필요한 최소 CMake 버전을 설정합니다. VERSION3.0 의 경우 프로젝트를 빌드하려면 CMake3.0 이상이 필요합니다. 호환성 문제를 방지하고, 특정 CMake 기능이
프로젝트에서 사용 가능하도록 보장합니다.
•      project(opencv_version) - 프로젝트의 이름을 설정하며, CMake 의 내부 관리와 프로젝트 내에서 이름을 통해 참조하는데 사용됩니다.
•      find_package(OpenCV REQUIRED) – Cmake 에 Opencv 를 라이브러리를 찾게 하도록 합니다. REQUIRED 키워드는 OpenCV 가 필수적임을 나타내며, CMake 가 OpenCV 를 찾지 못하면 오류를 발생시키고 빌드 프로세스를 중단시킵니다.•      include_directories(${OpenCV_INCLUDE_DIRS}) – 컴파일러에게 OpenCV 헤더 파일이 있는 디렉토리를 추가하도록 지시합니다. ${OpenCV_INCLUDE_DIRS}) 변수는 find_package(OpenCV) 명령어에 의해 설정된 경로를 포함하며, 이는 OpenCV 헤더 파일을 사용할 수 있도록 설정합니다.
•      add_executable(opencv_version opencv_version.cpp) – opencv_version 이라는 실행파일을 생성하도록 CMake 에 지시합니다. opencv_version 실행파일은 opencv_version.cpp 소스 파일에서 컴파일됩니다.
•      target_link_libraries(opencv_version ${OpenCV_LIBS}) – opencv_version 실행파일이 OpenCV 라이브러리와 연결되도록 설정합니다. ${OpenCV_LIBS} 변수는 find_package(OpenCV) 명령어에 의해 설정된 OpenCV 라이브러리
목록을 포함합니다. 이는 컴파일러와 링커가 OpenCV 라이브러리를 사용하도록 설정하는 부분입니다.
▪    작성한 소스코드가 있는 경로에서 ‘build’ 디렉토리를 생성한 후 ‘cmake ..’를 실행하여 ‘Makefile’을 생성 확인합니다.
$ mkdir build
$ cd build
$ cmake ..▪    ‘make’ 명령어를 실행해서 소스코드를 빌드합니다. 이때 컴파일러는 위에서 생성한 ‘Makefile’을 참조합니다. 
$ make
▪    생성된 실행파일을 실행합니다.
$ ./opencv_versionOPENCV CAMERA CAPTURE
▪ 로지텍 C270 카메라를 Jetson Nano 에 연결합니다.
▪    연결한 후 다음 명령어를 실행하여 카메라가 연결되었는지 확인합니다. 다음과 같이 video 장치가 출력되면 정상적으로 연결이 된 것입니다.
$ ls /dev/video*
/dev/video0
(참고 : 연결이 정상적으로 안되면 다음과 같은 문구가 뜨기 때문에 다시 연결선을 확인해주세요.)
ls: cannot access '/dev/video*': No such file or directory
▪    이미지와 달리 영상은 프레임을 계속 받아와서 출력하는 것이기 때문에 loop 를 이용하여 프레임을 계속 출력해야 합니다.
OpenCV 함수들을 사용하여 카메라로 영상을 실시간으로 출력하는 코드를 작성합니다. 
(실습코드 경로 :
opencv_ex/opencv_cpp/opencv_camera/camera_capture/camera_capture.cpp)
#include <opencv2/opencv.hpp>
int main() {
// Open the default camera using default API // 0 is the ID of the default camera
cv::VideoCapture cap(0);// Check if camera opened successfully
if (!cap.isOpened()) {
printf("Error: Could not open camera");
return -1;
}
// Get the frame width and height
int width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
int height = cap.get(cv::CAP_PROP_FRAME_HEIGHT); printf("width, height = %d, %d\n", width, height);
// Create a window for display
cv::namedWindow("Camera Capture", cv::WINDOW_AUTOSIZE);
while (true) {
cv::Mat frame;
// Capture frame-by-frame
cap >> frame;
// If the frame is empty, break immediately
if (frame.empty()) {
printf("Error: Captured empty frame");
break;
}
// Display the resulting frame
cv::imshow("Camera Capture", frame);
// Press 'q' on the keyboard to exit the loop
if (cv::waitKey(10) == 'q') {
break;
}
}
// When everything is done, release the video capture object
cap.release();
// Closes all the windows
cv::destroyAllWindows(); return 0;
}▪    주요 함수 설명
•      VideoCapture cap(0) – VideoCapture 객체를 생성하여 카메라를 엽니다. 이 때, cap(N)에서 N 은 /dev/videoN 장치 파일에서 N 에 해당합니다. 즉, /dev/video0 이기 때문에 cap(0)으로 작성합니다.
•      cap.isOpened() – VideoCapture 객체가 성공적으로 카메라를 열었는지 확인하며, 실패한 경우 에러 메세지를 출력하고 프로그램을 종료합니다.
•      cap.get(cv::CAP_PROP_FRAME_WIDTH), cap.get(cv::CAP_PROP_FRAME_HEIGHT) – 카메라로부터 캡쳐되는 프레임의 너비와 높이를 가져옵니다. 프레임의 너비와 높이를 다른 값으로 설정하고 싶을 경우 cap.set()을 사용합니다.
•      namedWindow(‘Camera Capture”, cv::WINDOW_AUTOSIZE) – ‘Camera Capture’라는 이름의 창을 생성하고, WINDOW_AUTOSIZE 를 사용하여 프레임 크기에 맞춰 자동으로 창 크기를 조절합니다.
•      cap >> frame – VideoCapture 객체에서 한 프레임을 읽어와 >> 연산자를 사용하여 frame 변수에 저장합니다.
•      frame.empty() – 캡쳐된 프레임이 비어 있는지 확인합니다. 프레임이 비어있는 경우, 에러 메세지를 출력하고 루프를 종료합니다.
•      cv::imshow(“Camera Capture”, frame) – Camera Capture 창에 캡쳐된 프레임을 표시합니다. 이 때 큰 따옴표 안에 있는 내용은 namedWindow 에서 사용한 내용과 동일해야 창에 이미지를 제대로 표시할 수 있습니다.
•      cv::waitkey(10) == ‘q’ – 10ms 동안 키 입력을 기다립니다. 입력된 키가 ‘q’라면 루프를 종료합니다. 그렇지 않으면 계속 루프를 진행합니다.
•      cap.release() – 비디오 캡처 객체를 해제합니다. 즉, 카메라 장치를 해제합니다.
•      cv::destroyAllWindows() – 모든 Opencv 창을 닫습니다.▪    CMakeLists.txt 파일을 생성합니다.
cmake_minimum_required(VERSION 3.0)
project(camera_capture)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS}) add_executable(camera_capture camera_capture.cpp) target_link_libraries(camera_capture ${OpenCV_LIBS})
▪    ‘build’ 폴더 생성 후 이동하여 ‘cmake ..’로 ‘Makefile’을 생성합니다. 그리고 ‘make’ 명령어로 소스코드를 컴파일하고 컴파일 완료된 파일을 실행합니다.
$ mkdir build
$ cd build
$ cmake ..
$ make
▪    camera_capture 파일을 실행합니다.$ ./camera_capture
(참고 : vscode 에서 remote ssh 를 사용하는 경우 다음과 같은 에러가 발생합니다.)
terminate called after throwing an instance of 'cv::Exception'
what():  OpenCV(4.5.1) /home/NVIDIA/opencv-
4.5.1/modules/highgui/src/window_gtk.cpp:624: error: (-2:Unspecified error) Can't initialize GTK backend in function 'cvInitSystem'
Aborted (core dumped)
이는 OpenCV 가 GUI(그래픽 사용자 인터페이스) 기능을 사용하려고 할 때 발생하며, 일반적으로 원격 서버나 GUI 환경이 없는 시스템에서 발생합니다. GUI 기능을 사용할 경우 호스트 컴퓨터 (Jetson Nano)로 실행해야 합니다.OPENCV CAMERA BINARIZATION
▪    OpenCV 를 이용하여 BINARIZATION(이진화)에 대해 알아봅니다.
이진화는 이미지 또는 영상의 각 픽셀을 두 개의 부류로 나누는 작업이며, 입력 부분을 주요 객체 영역과 배경 영역으로 나누거나 또는 중요도가 높은 관심 영역과 그렇지 않은 비관심 영역으로 구분하는 용도로 이진화가 사용됩니다. 보통은
그레이스케일 이미지에 대해 이진화를 수행하고, 영상의 픽셀 값이 특정 값보다 크면 255 로 설정하고, 작으면 0 으로 설정합니다. 이 때 각 픽셀과의 크기 비교 대상이 되는 값을 임계값(threshold)또는 문턱치라고 합니다.
임계값은 그레이스케일 범위인 0~255 사이의 정수를 지정할 수 있고, 영상의
이진화를 수식으로 표현하면 다음과 같습니다. Src 와 dst 는 각각 입력 영상과 출력 영상을 의미하고, T 는 임계값을 의미합니다. 임계값은 사용자의 경험에 의해 임의로 지정하거나, 또는 영상의 특성을 분석하여 자동으로 결정할 수도 있습니다.
!"#(%, ')   *
 255     "-.(%, ') > 0 일 때
0                                 그 외 
▪    영상을 이진화하는 코드를 작성해봅니다.
(실습코드
경로 :opencv_ex/opencv_cpp/opencv_camera/camera_binarization/binarization.cpp)
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;
int main()
{
VideoCapture cap(0);
if (!cap.isOpened()) {
printf("Error: Could not open camera"); return -1;
}
namedWindow("Binary", WINDOW_AUTOSIZE);while (true) {
Mat frame;
cap >> frame;
if (frame.empty()) {
printf("Error: Captured empty frame");
break;
}
Mat gray;
cvtColor(frame, gray, COLOR_BGR2GRAY); 
Mat binary;
threshold(gray, binary, 128, 255, THRESH_BINARY); //threshold 128 imshow("Binary", binary);
if (waitKey(10) == 'q') { break;
}
}
cap.release(); destroyAllWindows(); return 0;
}
▪    주요 함수 설명
•      cvtColor(frame, gray, COLOR_BGR2GRAY) – BGR 이미지를 그레이 스케일로 변환합니다.
•      threshold(gray, binary, 128, 255, THRESH_BINARY) – 그레이 스케일 이미지를 이진화합니다. 여기서는 임계값을 128 을 사용하고 있습니다.
▪    CMakeLists.txt 파일을 생성합니다.
cmake_minimum_required(VERSION 3.0) project(camera_binarization)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS}) add_executable(binarization binarization.cpp) target_link_libraries(binarization ${OpenCV_LIBS})▪    ‘build’ 폴더 생성 후 이동하여 ‘cmake ..’로 ‘Makefile’ 생성 후 ‘make’ 명령어로 소스 코드를 컴파일 합니다.
$ mkdir build
$ cd build
$ cmake ..
$ make
▪    컴파일이 완료되면 binarization 파일을 실행합니다.
$ ./binarizationOPENCV CAMERA LABELING
▪    OpenCV 를 이용하여 LABELING(레이블링)에 대해 알아봅니다.
레이블링 기법은 영상 내부에 있는 각 객체의 위치, 크기, 모양 등 특징을 분석할 때 사용됩니다. 영상의 레이블링은 일반적으로 이진화 된 영상에서 수행되며, 이 때 검은색 픽셀은 배경으로 간주하고, 흰색 픽셀은 객체로 간주합니다. 
하나의 객체는 한 개 이상의 인접한 픽셀로 이루어지며, 하나의 객체를 구성하는 모든 픽셀에는 같은 레이블 번호가 지정됩니다. 즉, 영상 내에서 주위에 같은 밝기의 픽셀 값을 가지는 픽셀들을 그룹화하여 그룹별로 번호를 매기는 방법을 말합니다.
특정 픽셀과 이웃한 픽셀의 연결 관계는 크게 두 가지 방식으로 정의 할 수
있습니다. 첫 번째는 특정 픽셀의 상하좌우로 붙어있는 픽셀끼리 연결되어 있다고 정의하는 4-방향 연결성(4-way-connectivity)이 있고, 두 번째는 상하좌우로 연결된픽셀뿐만 아니라 대각선 방향으로 인접한 픽셀도 연결되어 있다고 간주하는 8-방향 연결성(8-way connectivity)이 있습니다.
▪    총 3 개의 레이블링 실습을 합니다. 첫번째는 픽셀 데이터로 사용하는 임시 Mat 객체로 레이블링이 어떻게 작용하는지 보고, 두번째는 이미지를 활용한 레이블링, 세번째는 카메라를 활용한 레이블링을 실습합니다. 이번 시간에는 argument 를 이용해 세가지의 레이블링을 하나의 실행파일에서 실행할 수 있도록 소스코드를 작성하며, 다음과 같은 내용을 확인해 볼 수 있습니다.
(실습코드 경로 :
opencv_ex/opencv_cpp/opencv_camera/camera_labeling/labeling.cpp)
1.  argument 1 은 uchar 자료형 배열 data 를 픽셀 데이터로 사용하는 임시 Mat 객체를 생성한 후, 모든 원소에 255 를 곱한 결과 행렬을 src 로 저장한 뒤, connectedComponents 함수에 의해 labels 행렬 원소 값이 어떻게 반환되는지 볼 수 있습니다. Labels 행렬 원소 값은 객체 별로 그룹화가 되어있으며, 배경 영역까지 포함한 영역 개수(총 4 개)가 반환됩니다.
2.  argument 2 는 src(이미지)로 keyboard.bmp 를 사용하였고, 키보드에서 흰색 글자만을 찾아서 사각형으로 표시한 결과 영상입니다. 
3.  argument 3 은 src(영상)로 camera 영상을 사용하였고, 로지텍 카메라 영상에서 레이블링을 하고 사각형으로 표시한 결과 영상입니다.#include <opencv2/opencv.hpp>
#include <sstream>
using namespace cv;
void labelingBasic();
void labelingImageStats();
void labelingCameraStats();
int main(int argc, char* argv[])
{
if (argc < 2) {
printf("Usage: %s <option>\n", argv[0]); printf("Options:\n");
printf("  1 - Run labelingBasic()\n"); printf("  2 - Run labelingImageStats()\n"); printf("  3 - Run labelingCameraStats()\n"); return -1;
}
int option = std::stoi(argv[1]); switch (option) {
case 1:
labelingBasic();
break;
case 2:
labelingImageStats(); break;
case 3:
labelingCameraStats(); break;
default:
printf("Invalid option\n"); break;
}
return 0;
}
void labelingBasic()
{
uchar data[] = {
0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0,0, 0, 0, 0, 0, 0, 0, 0,
};
Mat src = Mat(8, 8, CV_8UC1, data) * 255;
Mat labels;
int labelCount = connectedComponents(src, labels);
// Convert OpenCV Mat to string using stringstream for readable output
std::stringstream ss1;
ss1 << src;
printf("src:\n%s\n", ss1.str().c_str());
std::stringstream ss2;
ss2 << labels;
printf("labels:\n%s\n", ss2.str().c_str());
printf("Number of labels: %d\n", labelCount);
}
void labelingImageStats()
{
Mat src = imread("../keyboard.bmp", IMREAD_GRAYSCALE);
if (src.empty()) {
printf("Image load failed!\n");
return;
}
Mat bin;
threshold(src, bin, 0, 255, THRESH_BINARY | THRESH_OTSU);
Mat labels, stats, centroids;
int count = connectedComponentsWithStats(bin, labels, stats, centroids);
Mat dst;
cvtColor(src, dst, COLOR_GRAY2BGR);
for (int i = 1; i < count; i++) {
int* p = stats.ptr<int>(i);
if (p[4] < 20) continue;
rectangle(dst, Rect(p[0], p[1], p[2], p[3]), Scalar(0, 255, 255), 2);
}
imshow("src", src); imshow("dst", dst); waitKey();destroyAllWindows();
}
void labelingCameraStats()
{
VideoCapture cap(0);
if (!cap.isOpened()) {
printf("Error: Could not open camera\n");
return;
}
while (true) {
Mat frame;
cap >> frame;
if (frame.empty()) {
printf("Error: Captured empty frame\n");
break;
}
Mat gray;
cvtColor(frame, gray, COLOR_BGR2GRAY);
Mat bin;
threshold(gray, bin, 0, 255, THRESH_BINARY | THRESH_OTSU);
Mat labels, stats, centroids;
int count = connectedComponentsWithStats(bin, labels, stats, centroids);
Mat dst;
cvtColor(gray, dst, COLOR_GRAY2BGR);
for (int i = 1; i < count; i++) {
int* p = stats.ptr<int>(i);
if (p[4] < 20) continue;
rectangle(dst, Rect(p[0], p[1], p[2], p[3]), Scalar(0, 255, 255), 2);
}
imshow("Camera frame", frame); imshow("Labeled", dst);
if (waitKey(10) == 'q') { break;
}
}
cap.release(); destroyAllWindows();}
▪    주요 함수 설명
•      int main(int argc, char* argv[]) – argc는 명령줄 인수의 개수를 의미하며, argv는 명령줄 인수를 담고 있는 문자열 배열을 의미합니다. 인수들을 통해 프로그램 실행 시 다양한 입력을 받을 수 있습니다.
예) labeling 1
•      connectedComponents(src, labels) – 이진화된 이미지에서 서로 연결된 픽셀들을 그룹화하여 고유한 라벨을 부여합니다. src 는 이진화된 입력 이미지며, labels 은 각 픽셀에 라벨을 할당한 행렬입니다. 반환값은 배경을 포함한 감지된 라벨의 갯수입니다.
•      imread(imagePath, cv::IMREAD_GRAYSCALE) – 이미지를 디스크에서 읽어오며, 읽어올 이미지의 파일 경로를 상대경로로 사용할 경우 실행 파일 기준 상대 경로로 지정해야 합니다. GRAYSCALE 을 사용해서 이미지를 그레이스케일로 읽어올 수 있습니다.
•      threshold(src, bin, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU) – Otsu
알고리즘을 사용하여 입력 이미지의 히스토그램을 기반으로 최적의 임계값을 선택하고, 해당 임계값을 기준으로 이진화된 이미지를 생성합니다.
•      connectedComponentsWithStats(bin, labels, stats, centroids) – 각 객체의 크기, 위치, 중심점을 계산하여 정보를 제공하는 역할을 합니다.
•      rectangle(dst, Rect(p[0], p[1], p[2], p[3]), Scalar(0, 255, 255)) – 이미지에 사각형을 그립니다. 
▪    CMakeLists.txt 파일을 생성합니다.
cmake_minimum_required(VERSION 2.8) project(camera_labeling) find_package(OpenCV REQUIRED)include_directories(${OpenCV_INCLUDE_DIRS}) add_executable(labeling labeling.cpp) target_link_libraries(labeling ${OpenCV_LIBS})
▪    ‘build’ 폴더 생성하고 경로 이동 후 ‘cmake ..’를 실행해서 ‘Makefile’을 생성합니다. 그리고 ‘make’ 명령어로 소스코드를 컴파일합니다.
$ mkdir build
$ cd build
$ cmake ..
$ make
▪    컴파일이 완료되면 ‘labeling’프로그램을 실행합니다. 이때 ‘1’을 파라메터(argument) 로 입력합니다. 이진 이미지에서 서로 연결된 객체들을 라벨링 하는 것을 볼 수 있습니다. 배경을 포함하여 총 4 개의 연결된 영역을 감지했음을 알 수 있습니다.
$ ./labeling 1▪    ‘2’를 파라메터(argument) 값으로 하고 ‘labeling’프로그램을 실행합니다.
$ ./labeling 2
그러면 소스코드에 포함된 bitmap 파일(keyboard.bmp)을 읽고 이 이미지 데이터를 가지고 라벨링 합니다. 
▪    ‘3’를 파라메터(argument) 값으로 하고 ‘labeling’프로그램을 실행합니다.
$ ./labeling 3이번에는 카메라(로지텍 USB Cam)영상 이미지 데이터를 가지고 라벨링 합니다. OPENCV PYTHON
opencv-python 은 OpenCV 의 python 바인딩으로, python 환경에서 컴퓨터 비전
애플리케이션을 보다 쉽게 개발할 수 있도록 지원하는 라이브러리입니다.
이를 활용하면 OpenCV 의 다양한 기능을 python 코드로 간결하게 구현할 수 있으며, 보다 직관적인 방식으로 이미지 처리 및 컴퓨터 비전 작업을 수행할 수 있습니다.
이번 실습에서는 이전에 C++로 작성한 OpenCV 프로그램을 Python 으로 구현하여 비교하면서, python 환경에서 OpenCV 를 사용하는 방법을 익히겠습니다.
python 으로 실행할 때는 앞에 python3 [파일명]으로 실행하면 됩니다.
OPENCV VERSION
▪    python 으로 OpenCV 버전을 출력하는 코드를 작성합니다. (실습코드 경로 :opencv_ex/opencv_py/opencv_version.py)
import cv2
print(cv2.__version__)
▪    opencv_version.py 를 실행합니다.
$ python3 opencv_version.py
OPENCV CAMERA
▪    python 으로 camera 영상을 출력하는 코드를 작성합니다. (실습코드 경로 :opencv_ex/opencv_py/opencv_camera.py)
import cv2
def main():
capture = cv2.VideoCapture(0)
if not capture.isOpened():
print("Error: Could not open camera.") return
width = capture.get(cv2.CAP_PROP_FRAME_WIDTH) height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT) print("width, height = ", width, height)
while True:
ret, frame = capture.read()if not ret:
print("Error: Could not read frame") break
cv2.imshow("VideoFrame", frame)
if cv2.waitKey(1) == ord('q'): break
capture.release()
cv2.destroyAllWindows()
if __name__ == "__main__": main()
▪    opencv_camera.py 를 실행합니다.
$ python3 opencv_camera.pyOPENCV LABELING
▪    앞에서 cpp 로 작성했던 Labeling 코드를 python 으로 작성해 봅니다. (실습코드 경로 : opencv_ex/opencv_py/labeling.py)
import cv2
import numpy as np
import sys
def labeling_basic():
data = np.array([[0, 0, 1, 1, 0, 0, 0, 0],
[1, 1, 1, 1, 0, 0, 1, 0],
[1, 1, 1, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 0],
[0, 0, 0, 1, 1, 1, 1, 0],
[0, 0, 0, 1, 0, 0, 1, 0],
[0, 0, 1, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8)
src = data * 255
cnt, labels = cv2.connectedComponents(src)
print('src:\n', src)
print('labels:\n', labels)
print('number of labels:', cnt)
def labeling_image_stats():
# Relative path based on executable file
src = cv2.imread('keyboard.bmp', cv2.IMREAD_GRAYSCALE)
if src is None:
print("Image load failed!")
return
_, bin = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | 
cv2.THRESH_OTSU)
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(bin) dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
for i in range(1, cnt):
x, y, w, h, area = stats[i]
if area < 20:
continue
pt1 = (x, y)
pt2 = (x + w, y + h)
cv2.rectangle(dst, pt1, pt2, (0, 255, 255))cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()
def labeling_camera_stats():
cap = cv2.VideoCapture(0)  # Open the default camera
if not cap.isOpened():
print("Error: Could not open camera")
return
while True:
ret, frame = cap.read()  # Capture a frame from the camera if not ret:
print("Error: Captured empty frame")
break
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cnt, labels, stats, centroids = 
cv2.connectedComponentsWithStats(bin)
dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
for i in range(1, cnt):
x, y, w, h, area = stats[i]
if area < 20:
continue
pt1 = (x, y)
pt2 = (x + w, y + h)
cv2.rectangle(dst, pt1, pt2, (0, 255, 255))
cv2.imshow('Camera frame', frame) cv2.imshow('Labeled', dst)
if cv2.waitKey(10) == ord('q'): break
cap.release()
cv2.destroyAllWindows()
if __name__ == "__main__": if len(sys.argv) < 2:print("Usage: python script.py <option>")
print("Options:")
print("  1 - Run labeling_basic")
print("  2 - Run labeling_image_stats with image input") print("  3 - Run labeling_camera_stats with camera input") sys.exit(-1)
option = int(sys.argv[1])
if option == 1:
labeling_basic()
elif option == 2:
labeling_image_stats() elif option == 3:
labeling_camera_stats() else:
print("Invalid option")
▪    argument 1 을 넣어서 labeling.py 를 실행합니다.
$ python3 labeling.py 1
▪    argument 2 넣어서 labeling.py 를 실행합니다.
$ python3 labeling.py 2▪    argument 3 을 넣어서 labeling.py 를 실행합니다.
$ python3 labeling.py 3
OpenCV 에서 CUDA 사용 여부에 따른 성능 차이
OpenCV 는 기본적으로 CPU 에서 연산을 수행하지만, CUDA 를 활용하면 GPU 를 통해 연산을 가속화할 수 있습니다. CPU 연산과 CUDA 가속을 비교하면, 속도 및 자원 사용량에서 큰 차이를 보입니다. 이번 실습에서는 CUDA 를 사용한 OpenCV 코드와 사용하지 않는 코드를 비교하여, FPS 차이, GPU 사용량 변화, 성능 개선 정도를
분석해봅니다. 
이를 통해 CUDA 가속이 Face Detection 과 같은 딥러닝 기반 연산에서 어떤 영향을 미치는지 확인해보겠습니다.n    Python 으로 CUDA 지원 여부를 확인합니다.
코드 작성 후 실행합니다.
(실습코드 경로 : opencv_ex/opencv_cuda/check_cuda.py)
import cv2
cuda_device_count = cv2.cuda.getCudaEnabledDeviceCount() print(f"CUDA Enabled Device Count: {cuda_device_count}")
$ python3 check_cuda.py
출력: CUDA Enabled Device Count: 1
n    OpenCV 에서 CPU 와 GPU 의 허프 변환(Hough Transform) 실행 속도를 비교합니다. GPU 는    대형 이미지에서 연산 속도가 현저히 빨라질 가능성이 높기 때문에
height 와 width 를 크게 설정하고, 실행 속도를 비교합니다.
코드 작성 후 실행합니다.
(실습코드 경로 : opencv_ex/opencv_cuda/hough_performance_test.py)
import cv2
import numpy as np
import time
height, width = 4096, 4096
image = np.zeros((height, width, 3), dtype=np.uint8)
cv2.line(image, (0, 0), (width, height), (255, 255, 255), 10) cv2.line(image, (width, 0), (0, height), (255, 255, 255), 10) gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
start_cpu = time.time()
lines_cpu = cv2.HoughLines(edges, 1, np.pi / 180, 200)
end_cpu = time.time()
print(f"CUDA (X) 허프 변환 시간 : {end_cpu - start_cpu} seconds")
if not cv2.cuda.getCudaEnabledDeviceCount(): print("CUDA 가 활성화된 장치가 없습니다.")
else:
gpu_image = cv2.cuda_GpuMat() gpu_image.upload(gray_image)gpu_edges = cv2.cuda.createCannyEdgeDetector(50, 150, 3)
gpu_edge_output = gpu_edges.detect(gpu_image)
hough_detector = cv2.cuda.createHoughSegmentDetector(1, np.pi / 180, 200, 10)
start_gpu = time.time()
result_gpu = hough_detector.detect(gpu_edge_output)
end_gpu = time.time()
print(f"CUDA (O) 허프 변환 시간 : {end_gpu - start_gpu} seconds")
$ python3 hough_performance_test.py
CUDA 를 사용한 허프 변환과 사용하지 않은 허프 변환의 성능 차이를 확인할 수 있습니다. 실행 결과를 보면 CUDA 를 사용한 경우가 훨씬 빠르게 연산됨을 알 수 있습니다. 이는 GPU 가 병렬 연산을 수행하여 대형 이미지에서도 연산 속도를 크게 향상시킬 수 있음을 보여줍니다.
OpenCV – Face Detection 에서 CUDA 사용여부에 따른 성능 차이
OpenCV DNN 모듈은 이미 만들어진 네트워크에서 순방향 실행을 위한 용도로
설계되었으며, opencv 에 내장된 다양한 심층 학습 모델을 사용하여 얼굴 감지와 같은 작업을 수행할 수 있게 해줍니다.
딥러닝 학습은 기존의 유명한 카페(caffe), 텐서플로(tensorflow) 등의 다른 딥러닝
프레임워크에서 진행하고, 학습된 모델을 불러와서 실행할 때에는 dnn 모듈을 사용하는 방식입니다. 즉 카페, 텐서플로, 토치 등의 프레임워크에서 미리 학습된 모델을 불러와서 추론(inference)을 실행할 수 있습니다.
딥러닝 프레임워크
Model 파일 확장자
Config 파일 확장자
Framework 문자열
카페
*.caffemodel
*.prototxt
“caffe”
텐서플로
*.pb
*.pbtxt
“tensorflow”
토치
*.t7 또는 *.net
“torch”
다크넷
*.weights
*.cfg
“darknet”
DLDT
*.bin
*.xml
“dldt”ONNX
*.onnx
“onnx”
SSD 알고리즘은 입력 영상에서 특정 객체의 클래스와 위치, 크기 정보를 실시간으로 추출할 수 있는 객체 검출 딥러닝 알고리즘이며, 원래 다수의 클래스 객체를 검출할 수 있지만 opencv 에서 제공하는 얼굴 검출은 오직 얼굴 객체의 위치와 크기를 알아내도록 훈련된 학습 모델을 사용합니다.
이번에는 SSD(single shot detector)를 이용하여 학습된 caffemodel 을 이용하여 face detection 을 실습합니다.
n    opencv_dnn 을 사용하여 사람 얼굴을 인식하는 코드를 작성합니다.
이번 코드에서는 CUDA 가속 없이 CPU 만을 활용하여 OpenCV 함수를 실행합니다. 이후, CUDA 가속(GPU)을 적용한 코드와 성능 차이를 비교하여 분석합니다.
(실습코드 경로 : opencv_ex/opencv_cuda/face_detector/dnnface.py)
import sys
import numpy as np
import cv2
import time
model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel' config = 'deploy.prototxt'
cap = cv2.VideoCapture(0)
if not cap.isOpened():
print('Camera open failed!') sys.exit()net = cv2.dnn.readNet(model, config)
if net.empty():
print('Net open failed!')
sys.exit()
frame_count = 0
total_time = 0
while True:
start_time = time.time()
ret, frame = cap.read()
if not ret or frame is None:
break
blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123)) net.setInput(blob)
detect = net.forward()
end_time = time.time()
elapsed_time = end_time - start_time
fps = 1 / elapsed_time
(h, w) = frame.shape[:2]
detect = detect[0, 0, :, :]
for i in range(detect.shape[0]):
confidence = detect[i, 2]
if confidence < 0.5:
continue
x1 = int(detect[i, 3] * w)
y1 = int(detect[i, 4] * h)
x2 = int(detect[i, 5] * w)
y2 = int(detect[i, 6] * h)
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
label = f'Face: {confidence:.3f}'
cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
cv2.imshow('CPU Face Detection', frame)
if cv2.waitKey(1) == 27: breakprint(f'CPU 평균 FPS: {fps:.2f}')
cap.release()
cv2.destroyAllWindows()
n    이 파일을 실행하려면 실행 파일 경로에 다음 파일이 있어야합니다. model = ‘res10_300x300_ssd_iter_140000_fp16.caffemodel’
config = ‘deploy.prototxt’
파일명
설명
res10_300x300_ssd _iter_140000_fp16. caffemodel
Caffe 프레임워크로 학습된 가중치(Weights) 파일. Face Detection 모델 (ResNet-10 기반 SSD 구조)을 FP16
정밀도로 학습한 결과를 저장하며, 추론 시 이 가중치를 사용
deploy.prototxt
Caffe 프레임워크에서 사용하는 네트워크 구성(Config) 파일. 레이어 구조, 입력/출력 크기, 필터 크기 등 모델의 구조적 정보가 정의되어 있음
이 파일들은 설치한 OpenCV 폴더의 samples/dnn/ 경로에 있는
‘download_models.py’ 파일로 다운 받을 수 있습니다. (실습 파일로도 제공됩니다.)
[model 파일을 직접 다운받는 경우]
opencv-4.5.1 폴더 내에 ‘download_models.py’ 파일이 있는 디렉터리로 이동한 후, 해당 파일을 실행하여 caffemodel 을 다운로드합니다.
(경로 : ~/opencv-4.5.1/samples/dnn/download_models.py)
$ cd ~/opencv-4.5.1/samples/dnn
$ python3 download_models.py opencv_face_detector_fp16
•     'download_models.py’ 를 이용하여 모델 다운로드•     'download_models.py' 실행한 후 폴더 생성 확인
•     폴더 안에 다운받은 모델 확인
[config 파일을 직접 복사하는 경우]
(경로 : ~/opencv-4.5.1/samples/dnn/face_detector/deploy.prototxt)n    model 파일과 config 파일을 ‘opencv_cuda/face_detector/’ 경로로 복사합니다.
n    Model 파일과 config 파일 두 개 모두 dnnface.py 실행파일이 있는 경로에 복사 했다면 파일을 실행하여 카메라로 사람 얼굴을 인식할 수 있습니다.
$ python3 dnnface.py
단일 프레임 기준으로 CUDA 를 사용하지 않는 코드는 대략 초당 2~4 프레임
정도의 속도로 동작하며, GPU 및 GPU Shared RAM 사용량이 적습니다. 다만, 특정 연산이 GPU 에서 처리될 가능성이 있어 간헐적으로 GPU 사용률이 순간적으로 튀는 현상이 발생할 수 있습니다.
이후 실행해볼 CUDA 가속 코드에서는 GPU 사용률이 상대적으로 증가하는 것을 확인할 수 있으며, 연산 방식의 차이로 인해 FPS 변화도 나타날 수 있습니다.
•    cuda 없이 dnnface 실행 했을 때 FPS 와 gpu 사용량n 이번 코드에서는 CUDA 사용 OpenCV 함수를 사용하여 face detection 을 실행합니다. 이전에 실행했던 코드와 비교하여 성능 차이를 확인해봅니다. (실습코드 경로 : opencv_ex/opencv_cuda/face_detector/dnnface_cuda.py)
import sys
import numpy as np
import cv2
import time
model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'
cap = cv2.VideoCapture(0)
if not cap.isOpened():
print('Camera open failed!')
sys.exit()
net = cv2.dnn.readNet(model, config)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
if net.empty():
print('Net open failed!')
sys.exit()
frame_count = 0
total_time = 0
while True:
start_time = time.time()
ret, frame = cap.read()
if not ret or frame is None:
break
gpu_frame = cv2.cuda_GpuMat()
gpu_frame.upload(frame)  
blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123)) net.setInput(blob)
detect = net.forward()
end_time = time.time()
elapsed_time = end_time - start_time fps = 1 / elapsed_time
(h, w) = frame.shape[:2]detect = detect[0, 0, :, :]
for i in range(detect.shape[0]):
confidence = detect[i, 2]
if confidence < 0.5:
continue
x1 = int(detect[i, 3] * w)
y1 = int(detect[i, 4] * h)
x2 = int(detect[i, 5] * w)
y2 = int(detect[i, 6] * h)
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
label = f'Face: {confidence:.3f}'
cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
cv2.imshow('GPU Face Detection', frame)
if cv2.waitKey(1) == 27: break
print(f'GPU 평균 FPS: {fps:.2f}')
cap.release()
cv2.destroyAllWindows()
n     CUDA 사용하는 코드와 사용하지 않는 코드 비교
CUDA 를 사용하는 코드는 딥러닝 모델 연산을 GPU 에서 실행하여 속도를
향상시키고, 프레임을 GPU 메모리에 업로드하여 병렬 연산을 수행하는 것이 전에 작성했던 코드와 가장 큰 차이점입니다.
비교 항목
CUDA 사용하지 않음
CUDA 사용
딥러닝 백엔드
없음 (기본적으로 CPU 사용)
Cv2.dnn.DNN_BACKEND_CUDA 설정 (GPU 사용)
연산 방식
CPU 에서 CNN 연산
수행
CUDA 기반 GPU 에서 CNN 연산 수행
영상 처리
cap.read()로 CPU 에서 직접 처리
cv2.cuda_GpuMat().upload(frame)
을 사용해 GPU 메모리에 업로드후 처리
net.foward() 실행 위치
CPU 에서 실행됨
GPU 에서 실행됨
추론 속도
상대적으로 느림
CUDA 병렬 연산으로 속도 향상
고해상도 영상 처리
프레임 크기가
커질수록 속도 저하
CUDA 최적화로 속도 유지
n    model 파일과 config 파일 두 개 모두 dnnface_cuda.py 실행파일이 있는 경로에
있는지 확인한 후 파일을 실행합니다. 이번 코드는 명시적으로 CUDA 를 사용하도록 설정하여 속도를 향상시킵니다. GPU 를 활용하면 CNN 연산을 CUDA 에서 실행하여 실시간 탐지 성능이 향상됩니다.
$ python3 dnnface_cuda.py
단일 프레임 기준으로 CUDA 를 활용한 face detector 는 대략 초당 6~12 프레임 정도로 동작합니다. 이전에 실행했던 CUDA 미사용 face detector 와 비교했을 때, GPU 및 GPU Shared RAM 사용량에서 확연한 차이를 확인할 수 있습니다.
•    cuda 사용하여 dnnface 실행 했을 때 FPS 와 gpu 사용량OpenCV – Object Detection 에서 CUDA 사용여부에 따른 성능 차이
이전에 face detection 예제를 통해 CUDA 사용 여부에 따른 성능 차이를 확인했다면, 이번에는 OpenCV 의 DNN 모듈을 활용하여 YOLOv3 또는 YOLOv3-tiny 기반의 객체 검출을 수행하고,  CUDA 를 사용한 경우와 사용하지 않은 경우의 성능과 결과를
비교해보겠습니다.
n    Object detection 을 실행하려면 weights, cfg, coco.names 파일이 필요합니다. 특히 weights 파일과 cfg 파일은 버전이 서로 일치해야 올바른 모델 구동이 가능합니다. 
(이 파일들은 실습자료로 제공되며, https://github.com/pjreddie/darknet 또는 https://pjreddie.com/darknet/yolo/ 링크에서도 찾을 수 있습니다.)
파일명
설명
역할
weights
사전에 학습된 가중치(Weights)파일 예) yolov3.weights
학습을 통해 얻은 파라미터(가중치) 값들을 저장하여 추론 시 사용
cfg
네트워크 구조(Architecture)
파일
예) yolov3.cfg
레이어(계층) 구성, 필터 크기, 채널 수 등 모델의 설정을 정의하고 추론 로직에 반영
coco.names
탐지할 객체 클래스(Class)
목록
예) coco.names
모델이 인식할 수 있는 객체 이름을 나열하며, 각 인덱스에 해당하는 라벨로 사용
이번 실습에서는 YOLOv3 과 YOLOv3-tiny 모델을 사용할 예정이며, 두 모델은
다음과 같은 차이가 있습니다. 사용 환경과 요구 사항에 따라 적절한 모델을 선택할 수 있습니다.항목
YOLOv3
YOLOv3-tiny
모델 복잡도
깊고 복잡한 구조, 많은 계층과 파라미터
경량화된 구조, 계층과 파라미터가 적음
추론 속도
상대적으로 느림
매우 빠름
정확도
높은 정확도 (특히 작은 객체 검출 우수)
다소 낮은 정확도
적용 환경
고성능 GPU/서버 환경, 정확도가 중요한 경우
임베디드, 모바일 등 실시간 처리가 필요한 경우
n    OpenCV DNN 과 YOLOv3 모델을 사용하여 물체를 인식하는 코드를 작성합니다. 이번 코드에서는 CUDA 가속 없이 CPU 만을 활용하여 OpenCV 함수를 실행합니다. (실습코드 경로 : opencv_ex/opencv_cuda/object_detector/object_detector.py)
import cv2
import numpy as np
import time
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []
with open("coco.names", "r") as f:
classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in
net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
cap = cv2.VideoCapture(0)
if not cap.isOpened():
print("Camera open failed!")
exit()
while True:
start_time = time.time()
ret, frame = cap.read()
if not ret or frame is None:
break
height, width, channels = frame.shapeblob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)
class_ids = []
confidences = []
boxes = []
for out in outs:
for detection in out:
scores = detection[5:]
class_id = np.argmax(scores)
confidence = scores[class_id]
if confidence > 0.5:
center_x = int(detection[0] * width)
center_y = int(detection[1] * height)
w = int(detection[2] * width)
h = int(detection[3] * height)
x = int(center_x - w / 2)
y = int(center_y - h / 2)
boxes.append([x, y, w, h])
confidences.append(float(confidence))
class_ids.append(class_id)
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
font = cv2.FONT_HERSHEY_PLAIN
if len(indexes) > 0:
for i in indexes.flatten():
x, y, w, h = boxes[i]
label = str(classes[class_ids[i]])
color = colors[i % len(colors)]
cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2) cv2.putText(frame, f"{label}: {confidences[i]:.2f}", (x, y -
10), font, 1, color, 2)
elapsed_time = time.time() - start_time
fps = 1 / elapsed_time
cv2.putText(frame, f"FPS: {fps:.2f}", (10, 60), 
cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.namedWindow("Camera Object Detection", cv2.WINDOW_NORMAL) cv2.resizeWindow("Camera Object Detection", 800, 600)
cv2.imshow("Camera Object Detection", frame)
if cv2.waitKey(1) & 0xFF == 27: break
cap.release()cv2.destroyAllWindows()
$ python3 object_detector.py
YOLOv3 은 모델 구조가 비교적 크고 연산량이 많아, CUDA 가속을 사용하지 않고 실행할 경우 실시간 처리가 어려울 수 있습니다. 실제로 실행해보면 FPS 가 크게 떨어지는 현상을 확인할 수 있습니다. 
n    OpenCV DNN 과 YOLOv3 모델을 사용하여 물체를 인식하는 코드를 작성합니다. 이번 코드에서는 CUDA 가속을 사용하여 OpenCV 함수를 실행합니다.
(실습코드 경로 : opencv_ex/opencv_cuda/object_detector/object_detector_cuda.py)
import cv2
import numpy as np
import time
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
classes = []
with open("coco.names", "r") as f:
classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames() output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]colors = np.random.uniform(0, 255, size=(len(classes), 3))
cap = cv2.VideoCapture(0)
if not cap.isOpened():
print("Camera open failed!")
exit()
while True:
start_time = time.time()
ret, frame = cap.read()
if not ret or frame is None:
break
height, width, channels = frame.shape
blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)
class_ids = []
confidences = []
boxes = []
for out in outs:
for detection in out:
scores = detection[5:]
class_id = np.argmax(scores)
confidence = scores[class_id]
if confidence > 0.5:
center_x = int(detection[0] * width) center_y = int(detection[1] * height)
w = int(detection[2] * width)
h = int(detection[3] * height)
x = int(center_x - w / 2)
y = int(center_y - h / 2)
boxes.append([x, y, w, h]) confidences.append(float(confidence))
class_ids.append(class_id)
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
font = cv2.FONT_HERSHEY_PLAIN
if len(indexes) > 0:
for i in indexes.flatten():
x, y, w, h = boxes[i]
label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}" color = colors[i % len(colors)]
cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)cv2.putText(frame, label, (x, y - 10), font, 1, color, 2)
elapsed_time = time.time() - start_time
fps = 1 / elapsed_time
cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), font, 2, (0, 0, 255), 2)
cv2.namedWindow("GPU YOLO Object Detection", cv2.WINDOW_NORMAL) cv2.resizeWindow("GPU YOLO Object Detection", 800, 600)
cv2.imshow("GPU YOLO Object Detection", frame)
if cv2.waitKey(1) & 0xFF == 27: break
cap.release()
cv2.destroyAllWindows()
$ python3 object_detector_cuda.py
CUDA 가속을 적용하면 GPU 의 병렬 연산 덕분에 CPU 전용 실행보다 빠른 추론 속도를 얻을 수 있습니다. 다만, Jetson Nano 와 같은 성능이 제한된 임베디드 디바이스에서는, GPU 가속을 사용해도 완벽한 실시간 처리에는 미치지 못할 수 있습니다. 그럼에도 불구하고, CUDA 를 적용하면 CPU 전용 실행에 비해 FPS 가 개선되고, CPU 부하도 줄어드는 장점을 확인할 수 있습니다.n    Jetson Nano 처럼 성능이 제한된 임베디드 디바이스에서는 YOLOv3 의 큰 모델 크기와 높은 연산량 때문에 실시간 처리에 부담이 될 수 있습니다. 반면, YOLOv3- tiny 는 모델 구조가 간소화되어 추론 속도가 빨라지고 자원 소모도 적어, Jetson Nano 환경에 더 적합할 수 있습니다. (만약 실시간 처리가 필수적이라면, Jetson Nano 보다 성능이 뛰어난 Jetson Orin NX 나 Jetson Orin Nano 같은 디바이스를 고려하는 것이 좋습니다.)
이전에 했던 object_detector.py 와 object_detector_cuda.py 에서 아래와 같이 yolov3 관련 줄을 주석 처리하고, yolov3-tiny 부분의 주석을 해제한 뒤, yolov3-tiny.weights, yolov3-tiny.cfg 파일이 실행 파일과 동일한 경로에 있는지 확인한 후에 다음 명령어로 각각 실행하여 비교해봅니다.
# CUDA 가속 사용 안할 때
$ python3 object_detector.py
# CUDA 가속 사용할 때
$ python3 object_detector_cuda.py
이 때, 이전에 사용했던 yolov3 모델과 새로운 yolov3-tiny 모델을 각각 실행해 보고, CUDA 가속을 적용한 코드와 적용하지 않은 코드를 비교하여 성능(추론 속도) 
차이를 직접 확인해볼 수 있습니다.