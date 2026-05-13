# STEP4: OpenCV with CUDA 및 객체 탐지

---

## Computer Vision이란?

- 컴퓨터를 이용하여 정지 영상 또는 동영상으로부터 의미 있는 정보를 추출하는 방법 연구
- 사람이 눈으로 사물을 보고 인지하는 작업을 컴퓨터가 수행하게 하는 학문
- 밝기, 색상, 모양, 텍스처 등의 영상 정보 활용

---

## OpenCV (Open Source Computer Vision Library)

### 정의

- 컴퓨터 비전과 이미지 처리 응용 프로그램을 개발하기 위한 **오픈 소스 라이브러리**
- 다양한 언어 지원 (C++, Python, Java, MATLAB)
- 크로스 플랫폼 지원
- 하드웨어 가속 지원 (GPU를 이용한 실시간 애플리케이션 가능)

### 주요 기능

| 카테고리 | 설명 |
|---|---|
| **이미지 처리** | 필터링, 히스토그램, 컬러 변환, 리사이징, 회전, 크롭 |
| **비디오 처리** | 실시간 카메라 스트리밍, 프레임 추출, 비디오 코덱 |
| **객체 탐지** | 얼굴 탐지, 사람/차량 탐지 (YOLO, SSD), 모션 감지 |
| **컴퓨터 비전 알고리즘** | 윤곽선 검출, 엣지 검출, 코너 검출, 특징점 추출 |
| **딥러닝 연동** | DNN 모듈을 통해 ONNX, Caffe, TensorFlow, Darknet 모델 로드 |

### OpenCV 모듈

| 모듈 | 설명 |
|---|---|
| `calib3d` | 카메라 캘리브레이션, 3차원 재구성 |
| `core` | 행렬, 벡터 등 핵심 클래스 |
| `dnn` | 심층 신경망 (Deep Neural Network) |
| `features2d` | 2차원 특징 추출 및 매칭 |
| `highgui` | 영상 출력, 마우스 이벤트 |
| `imgcodecs` | 영상 파일 입출력 |
| `imgproc` | 필터링, 기하학적 변환, 색 공간 변환 |
| `ml` | 머신러닝 알고리즘 |
| `objdetect` | 얼굴, 보행자 검출 |
| `photo` | HDR, 잡음 제거 |
| `stitching` | 영상 이어 붙이기 |
| `video` | 옵티컬 플로우, 배경 차분 |
| `videoio` | 동영상 파일 입출력 |

---

## OpenCV 설치

### Python용 설치

```bash
pip3 install opencv-python
pip3 install opencv-contrib-python
```

### CUDA 지원 OpenCV 빌드 (참고)

OpenCV를 Jetson Nano에서 직접 빌드할 경우 2~3시간 소요되며, 8GB 이상의 RAM이 필요함.

#### 필수 CMake 옵션

| 옵션 | 설명 |
|---|---|
| `WITH_CUDA=ON` | CUDA 지원 활성화 |
| `CUDA_ARCH_BIN="5.3"` | Jetson Nano Maxwell GPU (Compute Capability 5.3) |
| `WITH_CUDNN=ON` | cuDNN 활성화 |
| `WITH_CUBLAS=ON` | cuBLAS 활성화 |
| `ENABLE_FAST_MATH=ON` | 빠른 수학 연산 활성화 |
| `CUDA_FAST_MATH=ON` | CUDA 빠른 수학 활성화 |
| `OPENCV_DNN_CUDA=ON` | DNN 모듈의 GPU 가속 활성화 |

#### Swap 공간 할당 (RAM 4GB 부족 시)

```bash
# dphys-swapfile 설치
sudo apt-get install dphys-swapfile

# 설정 수정
sudo vi /sbin/dphys-swapfile
CONF_SWAPSIZE=4096
CONF_SWAPFACTOR=2
CONF_MAXSWAP=4096

sudo vi /etc/dphys-swapfile
CONF_SWAPSIZE=4096

# 재부팅
sudo reboot

# 확인
free -m  # 약 6GB程度的 swap 확인

# 기존에 설치 되어있던 OpenCV 를 삭제합니다.
sudo apt purge libopencv-dev libopencv-python libopencv-samples libopencv*

# OpenCV 가 남아있는지 확인합니다. jetson_release 명령어로도 OpenCV 가 삭제되었는지 확인합니다.
pkg-config --modversion opencv4

jetson_release

#  패키지 업데이트 및 필요한 패키지를 설치합니다.
sudo apt update
sudo apt install -y python3-pip python-dev python3-dev python-numpy python3-numpy
sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/nvidia-tegra.conf"
sudo apt install -y qt5-default
sudo apt install -y build-essential cmake git unzip pkg-config libswscale-dev
sudo apt install -y libcanberra-gtk* libgtk2.0-dev
sudo apt install -y libtbb2 libtbb-dev libavresample-dev libvorbis-dev libxine2-dev
sudo apt install -y curl

# 사진, 비디오 포맷 관련된 패키지를 설치합니다.
sudo apt install -y libxvidcore-dev libx264-dev libgtk-3-dev
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y libmp3lame-dev libtheora-dev libfaac-dev libopencore-amrnb-dev
sudo apt install -y libopencore-amrwb-dev libopenblas-dev libatlas-base-dev
sudo apt install -y libblas-dev liblapack-dev libeigen3-dev libgflags-dev
sudo apt install -y protobuf-compiler libprotobuf-dev libgoogle-glog-dev 
sudo apt install -y libavcodec-dev libavformat-dev gfortran libhdf5-dev
sudo apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo apt install -y libv4l-dev v4l-utils qv4l2 v4l2ucp libdc1394-22-dev
(참고: 실습자료를 복사할 경우 복사가 잘 안될 수 있습니다. 실습자료로 제공된 opencv_install.txt 파일을 참고하세요.)

#사전 빌드 된 ’opencv-4.5.1.tar.gz’ 파일을 Jetson Nano 홈 디렉토리(‘~’)에 복사하여 넣고, 아래 명령어로 압축 해제합니다.
(’opencv-4.5.1.tar.gz’  파일을 USB disk 또는 원격 연결된 Visual Studio code 를 이용해서 Jetson Nano 에 복사하여 놓습니다.)

$ tar -xvzf opencv-4.5.1.tar.gz

# opencv-4.5.1/build 경로로 이동합니다.
$ cd opencv-4.5.1/build/

# 아래 명령어로 사전 빌드된 OpenCV 패키지를 설치합니다.
$ sudo make install
(참고: 사전에 설치하는 패키지가 제대로 설치가 안됐을 경우 OpenCV 패키지를 설치할 때 빌드로 넘어가서 시간이 오래 걸리거나 에러가 나는 경우가 있을 수 있습니다.
그럴 경우 ‘Ctrl + C ‘를 눌러 install 을 중단하고, 패키지를 제대로 설치한 후에 진행해야 합니다. 단, 100%에서 오래 걸리는 건 기다려 주시기 바랍니다.)

# 설치가 완료되면 시스템이 설치한 라이브러리를 인식할 수 있도록 다음 명령어를 실행하여 라이브러리 캐시를 업데이트 합니다.
$ sudo ldconfig
OpenCV with CUDA 설치 확인 (Jetson_release)
▪ CUDA 를 사용하는 OpenCV 가 잘 설치 되었는지 확인합니다.
$ jetson_release

Swap 제거
▪ Swap 을 제거합니다.
$ sudo /etc/init.d/dphys-swapfile stop
$ sudo apt-get remove --purge dphys-swapfile
```

# Error

```
Get:24 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 libxml2-utils arm64 2.9.4+dfsg1-6.1ubuntu1.9 [32.8 kB]     
Get:25 http://ports.ubuntu.com/ubuntu-ports bionic/main arm64 libgtk2.0-dev arm64 2.24.32-1ubuntu1 [2,476 kB]                    
Get:26 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 libcanberra-gtk-dev arm64 0.30-5ubuntu1 [2,056 B]              
Get:27 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 libcanberra-gtk-module arm64 0.30-5ubuntu1 [8,556 B]           
Get:28 http://ports.ubuntu.com/ubuntu-ports bionic/main arm64 libepoxy-dev arm64 1.4.3-1 [119 kB]                                
Get:29 http://ports.ubuntu.com/ubuntu-ports bionic/main arm64 wayland-protocols all 1.13-1 [50.5 kB]                             
Get:30 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 libgtk-3-dev arm64 3.22.30-1ubuntu4 [897 kB]               
Get:31 http://ports.ubuntu.com/ubuntu-ports bionic/main arm64 libcanberra-gtk3-dev arm64 0.30-5ubuntu1 [2,048 B]                 
Get:32 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 libpng-tools arm64 1.6.34-1ubuntu0.18.04.2 [23.5 kB]       
Fetched 7,946 kB in 1min 46s (74.7 kB/s)                                                                                         
E: Failed to fetch http://ports.ubuntu.com/ubuntu-ports/pool/main/f/fontconfig/libfontconfig1-dev_2.12.6-0ubuntu2_arm64.deb  Connection failed [IP: 91.189.92.21 80]
E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?

```

```
nvidia@tegra-ubuntu:~/opencv-4.5.1/build$ sudo make install
-- Detected processor: aarch64
-- Looking for ccache - not found
-- Found ZLIB: /usr/lib/aarch64-linux-gnu/libz.so (found suitable version "1.2.11", minimum required is "1.2.3") 
Cleaning INTERNAL cached variable: WEBP_LIBRARY
Cleaning INTERNAL cached variable: WEBP_INCLUDE_DIR
-- Could NOT find OpenJPEG (minimal suitable version: 2.0, recommended version >= 2.3.1). OpenJPEG will be built from sources
-- OpenJPEG: VERSION = 2.3.1, BUILD = opencv-4.5.1-openjp2-2.3.1
-- OpenJPEG libraries will be built from sources: libopenjp2 (version "2.3.1")
-- Found ZLIB: /usr/lib/aarch64-linux-gnu/libz.so (found version "1.2.11") 
-- CUDA detected: 10.2
-- CUDA: Using CUDA_ARCH_BIN=5.3
-- CUDA NVCC target flags: -gencode;arch=compute_53,code=sm_53;-D_FORCE_INLINES
-- Could not find OpenBLAS include. Turning OpenBLAS_FOUND off
-- Could not find OpenBLAS lib. Turning OpenBLAS_FOUND off
-- Could NOT find Atlas (missing: Atlas_CLAPACK_INCLUDE_DIR) 
-- A library with BLAS API found.
-- A library with LAPACK API found.
-- Could NOT find JNI (missing: JAVA_AWT_LIBRARY JAVA_JVM_LIBRARY JAVA_INCLUDE_PATH JAVA_INCLUDE_PATH2 JAVA_AWT_INCLUDE_PATH) 
-- VTK is not found. Please set -DVTK_DIR in CMake to VTK build directory, or to VTK install subdirectory with VTKConfig.cmake file
CMake Error at cmake/OpenCVModule.cmake:274 (message):
  No modules has been found: /home/nvidia/opencv_contrib-4.5.1/modules
Call Stack (most recent call first):
  cmake/OpenCVModule.cmake:356 (_glob_locations)
  modules/CMakeLists.txt:7 (ocv_glob_modules)


-- OpenCV Python: during development append to PYTHONPATH: /home/nvidia/opencv-4.5.1/build/python_loader
CMake Error at modules/core/CMakeLists.txt:40 (message):
  CUDA: OpenCV requires enabled 'cudev' module from 'opencv_contrib'
  repository: https://github.com/opencv/opencv_contrib


-- Configuring incomplete, errors occurred!
See also "/home/nvidia/opencv-4.5.1/build/CMakeFiles/CMakeOutput.log".
See also "/home/nvidia/opencv-4.5.1/build/CMakeFiles/CMakeError.log".
Makefile:2433: recipe for target 'cmake_check_build_system' failed
make: *** [cmake_check_build_system] Error 1
nvidia@tegra-ubuntu:~/opencv-4.5.1/build$ ^C
nvidia@tegra-ubuntu:~/opencv-4.5.1/build$ 

```

```
확인해야 할 사항 (Tegra에서 실행)
opencv_contrib 디렉토리 존재 여부:
ls -la /home/nvidia/opencv_contrib-4.5.1/
ls -la /home/nvidia/opencv_contrib-4.5.1/modules/
CMakeCache.txt 확인 (어떤 옵션으로 설정했는지):
cat /home/nvidia/opencv-4.5.1/build/CMakeCache.txt | grep -i OPENCV_EXTRA
CMakeLists.txt에서 opencv_contrib 참조:
cat /home/nvidia/opencv-4.5.1/CMakeLists.txt | grep -i contrib

# 1. opencv_contrib가 올바른 경로에 있는지 확인
ls -la ~/opencv_contrib-4.5.1/modules/ 2>/dev/null || echo "modules folder not found"

# 2. 올바른 버전인지 확인
cd ~/opencv_contrib-4.5.1
git tag | grep "4.5.1"

# 3. CMake 재실행 (절대 경로 사용)
cd ~/opencv-4.5.1/build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=/home/nvidia/opencv_contrib-4.5.1/modules \
      -D WITH_CUDA=ON \
      -D CUDA_ARCH_BIN=5.3 \
      -D CUDA_FAST_MATH=ON \
      ..

# 4. 성공하면 make install
make -j$(nproc)
sudo make install
```

```
-- 
-- Configuring done
WARNING: Target "tbb" has EXCLUDE_FROM_ALL set and will not be built by default but an install rule has been provided for it.  CMake does not define behavior for this case.
-- Generating done
-- Build files have been written to: /home/nvidia/opencv-4.5.1/build
[  0%] Built target gen-pkgconfig
[  1%] Built target libopenjp2
[  3%] Built target carotene_objs
[  4%] Built target tegra_hal
[  5%] Built target ade
[  5%] Built target opencv_videoio_plugins
[  5%] Built target opencv_cudev
[  6%] Built target tbb
[  6%] Built target ittnotify
[  9%] Built target opencv_core
[ 12%] Built target opencv_imgproc
[ 14%] Built target libtiff
[ 19%] Built target libwebp
[ 23%] Built target IlmImf
[ 24%] Built target opencv_imgcodecs
[ 24%] Built target opencv_videoio
Scanning dependencies of target opencv_highgui
[ 24%] Building CXX object modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o
/home/nvidia/opencv-4.5.1/modules/highgui/src/window_gtk.cpp:48:10: fatal error: gtk/gtk.h: No such file or directory
 #include <gtk/gtk.h>
          ^~~~~~~~~~~
compilation terminated.
modules/highgui/CMakeFiles/opencv_highgui.dir/build.make:110: recipe for target 'modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o' failed
make[2]: *** [modules/highgui/CMakeFiles/opencv_highgui.dir/src/window_gtk.cpp.o] Error 1
CMakeFiles/Makefile2:6752: recipe for target 'modules/highgui/CMakeFiles/opencv_highgui.dir/all' failed
make[1]: *** [modules/highgui/CMakeFiles/opencv_highgui.dir/all] Error 2
Makefile:165: recipe for target 'all' failed
make: *** [all] Error 2

```

```
GTK 개발 라이브러리 설치
sudo apt-get update
sudo apt-get install libgtk2.0-dev
또는 GTK3 사용 시:

sudo apt-get install libgtk-3-dev
이전 네트워크 문제로 실패했던 경우
이전 apt-get 에러에서 이미 이 패키지들을 다운로드 시도했으나 실패했습니다:

Get:25 http://ports.ubuntu.com/ubuntu-ports bionic/main arm64 libgtk2.0-dev arm64 2.24.32-1ubuntu1 [2,476 kB]
이제 네트워크가 복구되었다면 다시 시도:

# 네트워크 재시도
sudo apt-get update --fix-missing

# GTK 설치
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev

# 또는 필수 패키지만
sudo apt-get install -y libgtk2.0-dev
설치 후 빌드 재개
cd ~/opencv-4.5.1/build
make -j$(nproc)
sudo make install
그래도 안 되면
GTK 없이 highgui 없이 빌드하는 옵션:

cd ~/opencv-4.5.1/build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_EXTRA_MODULES_PATH=/home/nvidia/opencv_contrib-4.5.1/modules \
      -D WITH_CUDA=ON \
      -D BUILD_opencv_highgui=OFF \
      ..

make -j$(nproc)
sudo make install
```
* 고려대실습 환경에에서일부 사이트의 연결을 맏아서 위의 실슴에 필요한 라이브러리를 모두 가지고 오지 못함.

---

## OpenCV C++ 프로그래밍

OPENCV VERSION
▪    OpenCV 버전을 출력하는 코드를 작성하여 cmake 로 빌드 후 실행해보겠습니다.
(실습코드 경로: opencv_ex/opencv_cpp/opencv_version/opencv_version.cpp)
```c
#include "opencv2/opencv.hpp"
int main(int argc, char** argv) {
printf("OpenCV version : %s\n", CV_VERSION); return 0;
}
```
▪    CMakeLists.txt 를 작성합니다.
```
cmake_minimum_required(VERSION 3.0)
project(opencv_version)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS}) add_executable(opencv_version opencv_version.cpp) target_link_libraries(opencv_version ${OpenCV_LIBS})
```

```
$ mkdir build
$ cd build
$ cmake ..
```

### CMakeLists.txt 기본 구조

```cmake
cmake_minimum_required(VERSION 3.0)
project(opencv_example)

find_package(OpenCV REQUIRED)

include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(opencv_example main.cpp)

target_link_libraries(opencv_example ${OpenCV_LIBS})
```

### 빌드 방법

```bash
mkdir build
cd build
cmake ..
make
./opencv_example
```

---

## OpenCV 파이썬 프로그래밍

### OpenCV 버전 확인

```python
import cv2
print(cv2.__version__)
```

### 카메라 영상 출력

```python
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open failed!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame read failed!")
        break
    
    cv2.imshow("VideoFrame", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

```
import cv2

cap = cv2.VideoCapture(0)

# 해상도 지정 (너비, 높이)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 또는 한 번에
cap.set(3, 1280)  # CAP_PROP_FRAME_WIDTH = 3
cap.set(4, 720)   # CAP_PROP_FRAME_HEIGHT = 4

# 확인
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"해상도: {width}x{height}")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

```
#include <opencv2/opencv.hpp>
int main() {
// Open the default camera using default API // 0 is the ID of the default camera
cv::VideoCapture cap(0);
// Check if camera opened successfully
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
}
```

CMakeLists.txt 파일을 생성합니다.
```
cmake_minimum_required(VERSION 3.0)
project(camera_capture)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS}) add_executable(camera_capture camera_capture.cpp) target_link_libraries(camera_capture ${OpenCV_LIBS})
```

```
$ mkdir build
$ cd build
$ cmake ..
$ make
```

```
./camera_capture
```


---

## OpenCV 실습 - 이미지 처리

### 에지 검출 (Canny)

```python
import cv2

img = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)
edges = cv2.Canny(img, 50, 150)

cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## 레이블링 (Labeling)

### Connected Components

- 이진화된 이미지에서 서로 연결된 픽셀들을 그룹화하여 고유한 라벨을 부여
- 객체의 위치, 크기, 모양 등 분석에 사용

### 연결성 종류

- **4-방향 연결성**: 상하좌우 인접 픽셀
- **8-방향 연결성**: 상하좌우 + 대각선 방향

### Python 예제

```python
import cv2
import numpy as np

# 기본 레이블링 (임시 Mat 사용)
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

print(f"Number of labels: {cnt}")
print(labels)
```

### 이미지 레이블링 (객체 탐지)

```python
import cv2

src = cv2.imread('keyboard.bmp', cv2.IMREAD_GRAYSCALE)

# Otsu 알고리즘으로 이진화
_, bin_img = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# 레이블링 (통계 포함)
cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img)

dst = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)

for i in range(1, cnt):
    x, y, w, h, area = stats[i]
    if area < 20:
        continue
    
    cv2.rectangle(dst, (x, y), (x+w, y+h), (0, 255, 255), 2)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 카메라 실시간 레이블링

```python
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    cnt, labels, stats, _ = cv2.connectedComponentsWithStats(bin_img)
    
    dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if area < 20:
            continue
        cv2.rectangle(dst, (x, y), (x+w, y+h), (0, 255, 255), 2)
    
    cv2.imshow('frame', frame)
    cv2.imshow('labeled', dst)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## OpenCV with CUDA

### CUDA 지원 확인

```python
import cv2

cuda_device_count = cv2.cuda.getCudaEnabledDeviceCount()
print(f"CUDA Enabled Device Count: {cuda_device_count}")
# 출력: 1 (Jetson Nano에서 CUDA 활성화됨)
```

### CPU vs GPU 허프 변환 성능 비교

```python
import cv2
import numpy as np
import time

height, width = 4096, 4096

# 이미지 생성
image = np.zeros((height, width, 3), dtype=np.uint8)
cv2.line(image, (0, 0), (width, height), (255, 255, 255), 10)
cv2.line(image, (width, 0), (0, height), (255, 255, 255), 10)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

# CPU 허프 변환
start_cpu = time.time()
lines_cpu = cv2.HoughLines(edges, 1, np.pi / 180, 200)
end_cpu = time.time()
print(f"CUDA (X) 허프 변환 시간: {end_cpu - start_cpu:.4f} seconds")

# GPU 허프 변환 (CUDA 사용)
if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    gpu_image = cv2.cuda_GpuMat()
    gpu_image.upload(gray_image)
    
    gpu_edges = cv2.cuda.createCannyEdgeDetector(50, 150, 3)
    gpu_edge_output = gpu_edges.detect(gpu_image)
    
    hough_detector = cv2.cuda.createHoughSegmentDetector(1, np.pi / 180, 200, 10)
    
    start_gpu = time.time()
    result_gpu = hough_detector.detect(gpu_edge_output)
    end_gpu = time.time()
    print(f"CUDA (O) 허프 변환 시간: {end_gpu - start_gpu:.4f} seconds")
```

---

## OpenCV DNN - Face Detection

### 딥러닝 프레임워크별 모델 형식

| 프레임워크 | 모델 파일 | 설정 파일 | Framework 문자열 |
|---|---|---|---|
| Caffe | `.caffemodel` | `.prototxt` | "caffe" |
| TensorFlow | `.pb` | `.pbtxt` | "tensorflow" |
| Torch | `.t7`, `.net` | - | "torch" |
| Darknet | `.weights` | `.cfg` | "darknet" |
| DLDT | `.bin` | `.xml` | "dldt" |
| ONNX | `.onnx` | - | "onnx" |

### SSD (Single Shot Detector)

- 입력 영상에서 특정 객체의 클래스와 위치, 크기 정보를 실시간으로 추출
- Face Detection 모델은 오직 얼굴 위치와 크기 검출

### Face Detection 모델 파일

| 파일 | 설명 |
|---|---|
| `res10_300x300_ssd_iter_140000_fp16.caffemodel` | Caffe 가중치 파일 (FP16) |
| `deploy.prototxt` | 네트워크 설정 파일 |

### CPU Face Detection 코드

```python
import cv2
import time

model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'

cap = cv2.VideoCapture(0)

net = cv2.dnn.readNet(model, config)

if net.empty():
    print('Net open failed!')
    exit()

while True:
    start_time = time.time()
    
    ret, frame = cap.read()
    if not ret:
        break
    
    # Blob 생성 (300x300으로 크기 조정, 평균값 차감)
    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    
    # 검출
    detect = net.forward()
    
    # 결과 해석
    h, w = frame.shape[:2]
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
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    elapsed_time = time.time() - start_time
    fps = 1 / elapsed_time
    
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    cv2.imshow('CPU Face Detection', frame)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

### CUDA Face Detection 코드

```python
import cv2
import time

model = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
config = 'deploy.prototxt'

cap = cv2.VideoCapture(0)

net = cv2.dnn.readNet(model, config)

# CUDA 백엔드 및 타겟 설정
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

if net.empty():
    print('Net open failed!')
    exit()

while True:
    start_time = time.time()
    
    ret, frame = cap.read()
    if not ret:
        break
    
    # GPU 메모리에 프레임 업로드
    gpu_frame = cv2.cuda_GpuMat()
    gpu_frame.upload(frame)
    
    # Blob 생성 및 추론
    blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123))
    net.setInput(blob)
    detect = net.forward()
    
    # 결과 해석 (CPU Face Detection과 동일)
    h, w = frame.shape[:2]
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
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    elapsed_time = time.time() - start_time
    fps = 1 / elapsed_time
    
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    cv2.imshow('GPU Face Detection', frame)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

### CPU vs GPU 비교

| 항목 | CUDA 사용 안함 | CUDA 사용 |
|---|---|---|
| 딥러닝 백엔드 | 없음 (기본 CPU) | `DNN_BACKEND_CUDA` |
| 연산 방식 | CPU에서 CNN 연산 | GPU에서 CNN 연산 |
| 프레임 처리 | `cap.read()` (CPU) | `cv2.cuda_GpuMat().upload()` |
| 추론 위치 | CPU | GPU |
| 추론 속도 | 상대적으로 느림 | CUDA 병렬 연산으로 향상 |
| FPS | 약 2-4 FPS | 약 6-12 FPS |

---

## OpenCV DNN - Object Detection (YOLO)

### YOLO 모델 파일

| 파일 | 설명 |
|---|---|
| `yolov3.weights` | YOLOv3 사전 학습된 가중치 |
| `yolov3.cfg` | YOLOv3 네트워크 설정 |
| `yolov3-tiny.weights` | YOLOv3-tiny 가중치 (경량화) |
| `yolov3-tiny.cfg` | YOLOv3-tiny 설정 |
| `coco.names` | 탐지 가능한 80개 클래스 목록 |

### YOLOv3 vs YOLOv3-tiny

| 항목 | YOLOv3 | YOLOv3-tiny |
|---|---|---|
| 모델 복잡도 | 깊고 복잡함 | 경량화 |
| 추론 속도 | 느림 | 빠름 |
| 정확도 | 높음 | 다소 낮음 |
| 적용 환경 | 고성능 GPU/서버 | 임베디드, 모바일 |

### YOLO Object Detection (CPU)

```python
import cv2
import numpy as np
import time

# 네트워크 로드
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# 클래스 목록 로드
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# 출력 레이어 설정
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# 색상 랜덤 생성
colors = np.random.uniform(0, 255, size=(len(classes), 3))

cap = cv2.VideoCapture(0)

while True:
    start_time = time.time()
    
    ret, frame = cap.read()
    if not ret:
        break
    
    height, width, channels = frame.shape
    
    # Blob 생성 (416x416)
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    
    # 검출
    outs = net.forward(output_layers)
    
    # 결과 파싱
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
    
    # Non-Maximum Suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    # 결과 출력
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
            color = colors[i % len(colors)]
            
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
    
    elapsed_time = time.time() - start_time
    fps = 1 / elapsed_time
    
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.namedWindow("Object Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Object Detection", 800, 600)
    cv2.imshow("Object Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

### YOLO Object Detection (CUDA)

```python
import cv2
import numpy as np
import time

# 네트워크 로드
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# CUDA 백엔드 설정
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# (나머지는 CPU 버전과 동일...)
```

> **참고**: Jetson Nano에서 YOLOv3 실시간 처리는 부담이 될 수 있으며, YOLOv3-tiny가 더 적합함

---

## 성능 최적화 팁

### Jetson Nano에서 OpenCV CUDA 활용

1. **모델 선택**: 경량 모델 사용 (YOLOv3-tiny, MobileNet 등)
2. **해상도 조절**: 입력 영상 해상도 축소
3. **프레임 스킵**: 모든 프레임 대신 건너뛰며 처리
4. **TensorRT 최적화**: TensorRT로 모델 변환하여 추론 가속
5. **Power Mode**: 최대 성능 모드 사용

```bash
# 최대 성능 모드
sudo nvpmodel -m 0
sudo jetson_clocks
```

<img src="./img/001.jpg" width="50%"> <br>
<img src="./img/002.jpg" width="50%"> <br>
<img src="./img/003.jpg" width="50%"> <br>
<img src="./img/004.jpg" width="50%"> <br>
<img src="./img/005.jpg" width="50%"> <br>
<img src="./img/006.jpg" width="50%"> <br>
<img src="./img/007.jpg" width="50%"> <br>
<img src="./img/008.jpg" width="50%">


---

## 참고 자료

- [OpenCV Documentation](https://docs.opencv.org/)
- [OpenCV Tutorial](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)
- [OpenCV GitHub](https://github.com/opencv/opencv)
- [YOLO Website](https://pjreddie.com/darknet/yolo/)
- [OpenCV DNN Module](https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html)
- [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt)
