Linux
(Operation System)
OS (Operating System)
▪ 사용자와 컴퓨터 하드웨어 사이의 인터페이스 역할을 하는 소프트웨어의 집합
•   컴퓨터 시스템의 자원을 효율적으로 관리
•   사용자 및 다른 소프트웨어와의 상호작용
•   성능 최적화 및 편리한 인터페이스 제공
• 범용OS 와 전용(Embedded)OS로 구분되어 사용됨
Application Operating System
Hardware
범용OS
전용(Embedded)OSOS (Operating System) - Linux
▪  Open Source and Free 
▪  Linux에는 Red Hat, SUSE 및 Debian등 배포판이 존재
•   배포판(Distribution): Linux Kernel 외 용도에 따른 여러 소프트웨어 패키지들을 함께 담은 Linux OS 시스템
▪  NVIDIA Jetson은 Ubuntu Linux 지원
Linux 활용 분야Linux OS의 주요 구성
▪  BootLoader
▪  Kernel
▪  Daemon
▪  Shell
▪  File System
▪ X Window System (Desktop Environment)
Linux – BootLoader 
▪  BootLoader
•   컴퓨터를 부팅할 때 설치된 운영체제를 메모리에 로드하고 실행하는 역할
•   BIOS, UEFI가 부트 디바이스(하드 디스크, SSD)에서 부트로더를 로드하고 실행
•   대표적인 부트로더로는 GRUB(Grand Unified Bootloader)이 있음
•  UEFI (Unified Extensible Firmware Interface) 
•   64bit OS 부팅을 지원하는 펌웨어 (Legacy BIOS Setup 인터페이스 지원)Linux – Kernel 
▪  Kernel
•   운영체제의 핵심 부분으로, 하드웨어와 소프트웨어 간의 인터페이스 역할
•   부팅 과정에서 커널이 메모리에 로드되어 실행
•   프로세스 관리, 메모리 관리, 파일 시스템 관리, 장치 드라이버 관리 등의 기능 수행
•   쉘(Shell)에게 전달받은 사용자의 요청을 하드웨어에게 전달하여 처리할 수 있게 함
•   OS의 가장 낮은 수준
API
(Application Programming 
Interface)
Linux – Daemons 
▪  Daemon
•   데몬(daemon)은 백그라운드에서 실행되며 사용자의 직접적인 개입 없이 특정 작업을 수행하는 프로그램.
•   서버나 시스템 관리 작업을 자동화하는 역할을 하며, 주로 시스템이 부팅될 때 시작되어 지속적으로 실행.
•   리눅스 시스템 운영에 필수적인 역할을 하며, 서버 및 백그라운드 작업을 안정적으로 유지하는 핵심 요소.
•   대표적인 리눅스 데몬Linux – Shell
▪  Shell
•   사용자와 커널 간의 명령 인터페이스 역할
•   사용자가 명령어를 입력하면 셸이 이를 해석하여 커널에 전달하고, 커널의 실행 결과를 사용자에게 반환
•   즉, 사용자의 요청이 Shell에 프로그램에 통해 해석되고, 그 결과가 kernel에 전달 됨
•   대표적인 셸로는 Bash(Bourne Again Shell), sh(Bourne shell), Ash(Almquist Shell) 등이 있음
Linux - File System
▪  File System
•   리눅스 파일 시스템은 계층적인 구조를 가지고 있으며, 모든 파일과 디렉토리는 /(루트)에서 시작되고 루트 아래에 여러 하위 디렉토리가 위치
•   여러 종류의 파일 타입 지원 – 일반 파일, 심볼릭 링크 파일, 디바이스 파일 … 
•   사용자와 그룹 기반의 권한 시스템을 사용하여 파일과 디렉토리에 대한 접근 제어
•   파일 시스템은 대표적으로 Ext4, XFS, Btrfs등이 있음
•   리눅스에서는 파일 시스템을 마운트해서 사용
마운트는 특정 저장 장치의 파일 시스템을 파일 시스템 계층 구조의 특정 지점에 연결하는 과정을 의미Linux – X window System
▪  X window System
•   리눅스에서 그래픽 사용자 인터페이스(GUI)를 제공하는 시스템
•   디스플레이 장치에 창을 표시하며 마우스와 키보드 등의 입력장치의 상호작용 등을
관리해 GUI 환경의 구현을 위한 기본적인 프레임워크 제공
▪  Desktop Environment 
•   운영 체제 상단의 그래픽 사용자 인터페이스 (사용자가 모니터를 통해 볼 수 있는 작업 공간)  
•   ‘GNOME’, ‘KDE’, ‘Xfce’ 및 ‘Fluxbox’등 다양한 데스크탑 환경 (Ubuntu Linux는 GNOME 데스크탑 환경 지원 )
< GNOME >
< KDE >
< Xfce >
Linux Repository
▪  Linux에서 repository는 설치하고자 하는 프로그램/소프트웨어 패키지가 저장된 서버.
▪  Linux 배포판별 패키지 저장소(서버)로 부터 소프트웨어 검색 및 설치하는 도구 제공.
•   Ubuntu/Debian : APT(Advanced Packaging Tool), ”.deb” 패키지 파일
•   Red Hat/CentOS/Fedora : YUM(Yellowdog Updater, Modifier), “.rpm”(Red Hat Package Manager) 패키지 파일
•   Arch Linux : Pacman 
▪ Repository에 찾는 소프트웨어가 없다면, 패키지를 담고 있는 서버를 리눅스 환경에 새로 등록해야 함. Linux Terminal
▪  사용자가 명령을 입력하고 출력 결과를 텍스트로 확인하는 인터페이스
▪  터미널은 정보를 전송하는 역할, OS가 정보를 이해하기 위해 터미널은 shell을 사용(주로 bash)
▪  CLI(Command Line Interface):사용자가 텍스트로 명령어를 입력하고 결과가 텍스트로 화면에 출력
Kernel
Shell
< Terminal Application >
Jetson OS FlashFlash
▪  Flash
•   운영체제와 소프트웨어를 디바이스의 저장 장치 (micro SD card 또는 eMMC)에 설치하는 과정
•   디바이스가 부팅될 수 있도록 필요한 모든 시스템 파일과 소프트웨어를 해당 저장 장치에 기록
Flash 방법 – SDK Manager
▪  SDK Manager 사용 가능
•   SDK Manager는 Devkit(개발 참조보드)만 지원Flash 방법 – Jetson Linux 
▪  Jetson Linux
•   Jetson module들을 위한 Board Support Package로 kernel, Bootloader, Flashing utility, ubuntu 기반의 sample root file 
system등이 포함
•   현재 ALLAI JCB보드에서 지원 버전은 Jetson Linux 32.7.1(Ubuntu 18.04 LTS)와 Jetson Linux 35.x.x(Ubuntu 20.04 LTS)
•   https://developer.NVIDIA.com/embedded/linux-tegra-r3271 에서 BSP, sample root file system, kernel source 다운로드 가능
Flash 방법 - MFI
▪  MFI (Mass Flash Interface)
•   Jetson module을 대량으로 flash하기 위해 생긴 방법
•   Mass Flash Interface의 약자
•   처음 초기화 할때 사용한 이미지들이 포함되어 있으며, 동시에 여러 Jetson module flash 가능What is VirtualBox?
▪  하나의 물리적 컴퓨터에서 여러 개의 가상 머신(Virtual Machine : VM)으 로 분할하여 각기 다른 운영체제를 동시에 실행 가능
▪  Host 운영체제 (Host OS): 
•  VirtualBox가 설치된 실제 컴퓨터의 운영체제로, 다양한 호스트 운영체제 지원 (예: Windows 11)
▪  Guest 운영체제 (Guest OS) : 
•  VirtualBox내에서 실행되는 가상머신의 운영체제로, 다양한 게스트 운영체제 운영 가능 (예: Ubuntu)
Oracle VM VirtualBoxFlash 방법 – MFI로 flash 하기 위한 구성
Flash 방법 – Recovery mode bootFlash 방법 – Recovery mode boot
▪  Jetson SOM별 USB ID
Bus <bbb> Device <ddd>: ID 0955: <nnnn> NVIDIA Corp.
<bbb> 3자리 숫자로 연결된 버스 번호
<ddd> 3자리 숫자로 연결된 장치 번호
<nnnn> 4자리 숫자로 Jetson Module 구별 식별자
▪  Jetson Nano 예시
BUS 001 Device 005: ID 0955:7f21 NVIDIA Corp.
식별자
SD Card 부팅
▪  Jetson Nano Module의 Storage는 16GB eMMC
▪  현재 쓰는 Jetson Nano는 module에 포함되어 있는 내부 저장소(eMMC)로 부팅하기 때문에 sd card로 부팅하기 위해서는 SD card에도 따로 image를 flash하고 부팅 미디어를 변경해야 함
▪  SD card를 flash 하기 위해 balenaEtcher(SD card flash tool) 사용
▪  플래싱 된 JCB의 eMMC에 있는 설정파일의 루트 경로를 수정하여 부팅 미디어를 SD card로 변경
▪  Gparted를 사용하여 SD Card 용량을 모두 사용하도록 수정실습 1-2
- Jetson Nano - OS Image Flash 실습실습 1-2: Window PC 에 Virtual Box 설치 후 세팅 및 Jetson Nano Flash
Window PC 에서 Virtual Box 설치 후 세팅하기
■     Window PC 에 Virtual Box 를 설치합니다.
•    원격 Host 용으로 사용할 PC 가 Windows OS 일 경우 ‘Virtual Box”를 사용하여 “ubuntu 18.04(Guest OS)” 설치, 활용합니다.
(참고: Windows 11 OS 의 WSL 을 사용해도 가능 하지만 복잡한 설정으로
인하여 Virtual Box 환경에서 Ubuntu 를 설치하여 원격 Host PC 로 사용하는
것을 권장합니다.)
•    아래 사이트에서 Windows OS 용(Host OS) Virtual Box 설치 파일 다운로드
받습니다.
https://www.oracle.com/kr/virtualization/technologies/vm/downloads/virtualbox-downloads.html
•    “VirtualBox Extension Pack”과 “VBox GuestAdditions”도 같이 다운로드 받습니다.Finish’
•    Window PC 에 Virtual Box 설치
다운로드 받은 ‘Virtual Box”설치 파일(예: VirtualBox-7.0.14-161095-Win.exe)을 더블 클릭해서 설치를 시작합니다. 아래와 같은 화면에서 ‘Next’ 버튼을 누르고 ‘ 버튼이 나타날 때까지 설치를 진행합니다. 
•    ‘Virtual Box” 기본 설치가 완료되면 Extension Pack(예: 
Oracle_VM_VirtualBox_Extension_Pack-7.0.14.vbox-extpack)도 설치합니다.
•    (참고 : 설치하다가 아래와 같은 창이 뜰 수 있습니다. Microsoft visual c++이 설치되지 않아 발생하는 에러입니다. 다음 내용을 따라해주세요.)
•    https://learn.microsoft.com/ko-kr/cpp/windows/latest-supported-vc- redist?view=msvc-170 링크에서 vc_redist.x64.exe 파일을 다운받습니다.•    다운로드 받은 VC_redist.x64 를 실행하여 설치를 진행합니다. 
•    설치가 완료 된 뒤, VirtualBox 설치를 진행하면 Microsoft visual c++ 에러가 발생하지 않고 잘 설치됩니다.
■     Virtual box 에서 새로 만들기를 눌러주세요.■     아래 표시한 부분을 채워주고 다음을 눌러주세요. 이름에 ubuntu 가 들어가면 자동으로 종류와 버전이 Linux – Ubuntu 로 변경됩니다.
■     새로 만들 가상환경의 기본메모리와 프로세서 개수를 선택하고 다음을 눌러주세요. (초록색으로 표시된 부분 안에서 선택합니다.)■     지금 새 가상 하드 디스크 만들기를 선택하고, 디스크 크기를 여유롭게 설정해주세요. 그리고 다음을 눌러주세요. (최소 30GB 이상으로 만들어줍니다.)
■     설정한 내용을 확인하고 제대로 설정이 됐다면 완료버튼을 눌러주세요.■     Virtual box 초기화면에 설정버튼을 눌러주세요.
■     설정 - 일반에서 클립보드 공유와 드래그 앤 드롭을 양방향으로 변경해주세요. 양방향으로 변경하면 HostPC 와 virtual box 간의 공유가 가능합니다.■     설정 - 시스템에서 부팅 순서를 아래와 같이 바꿔주세요.
■     설정 - 네트워크를 아래와 같이 어댑터에 브리지로 변경해주세요.■     네트워크 연결 방법에 맞게 선택하고 확인을 눌러주세요.
■ 설정 – 공유 폴더에서 공유 폴더를 만들기 위한 설정을 진행합니다.
•      Window PC 에 다음과 같이 폴더를 생성합니다. (경로 : D:\share)
•      설정 - 공유 폴더로 들어가서 빨간색으로 표시 된 부분을 눌러 공유 폴더를 추가합니다.•      아래와 같이 공유 폴더에 윈도우 PC 에 생성한 폴더 경로를 입력하고, 확인을 누릅니다.•      아래와 같이 공유 폴더가 추가된 것을 확인합니다.
■     설정이 완료되었다면 시작을 눌러주세요.Virtual box 에서 ubuntu 설치
■     Install Ubuntu 를 눌러주세요.
■     Continue 버튼을 눌러주세요.■     아래와 같이 선택한 후 Continue 버튼을 눌러주세요.
■     아래와 같이 선택한 후 Install Now 버튼을 선택해주세요.■     Continue 버튼을 눌러주세요.
■     Continue 버튼을 눌러주세요.■     Name, user name, password 를 입력하고 Continue 버튼을 눌러주세요. (참고 : 이번 실습에서는 모두 NVIDIA 로 통일합니다.)
■     설치되는동안 기다려주세요. 설치가 완료되었다면 Restart now 버튼을 눌러주세요.■ “Please remove the installation medium, then press ENTER” 문구가 나오면 Enter 를 눌러주세요. (삽입한 iso 이미지 파일을 제거하라는 의미인데 virtual box 는 자동해제 해주기 때문에 Enter 를 누르시면 됩니다.)■     만약 아래 이미지가 떴다면 virtual box 우측 상단에 X 표시를 눌러 시스템 전원 끄기를 누른 후 다시 시작해주세요. ■     이전에 설정한 Password 를 입력하고 Enter 를 눌러주세요.
■     화면이 켜졌다면 장치 – 게스트 확장 CD 이미지 삽입을 눌러주세요.■     아래 창이 뜬다면 Run 버튼을 눌러주세요.
■     아래와 같은 창이 뜬다면 Don’t Upgrade 버튼을 눌러주세요.■     아래와 같이 “Press Return to close this window…”가 뜬다면 Enter 를 눌러주세요. 
■     게스트 확장 CD 이미지 삽입을 완료하면 아래와 같은 기능을 사용할 수 있어서 편리합니다. 
•    마우스 포인터 통합 (Mouse Pointer Integration)
•    공유 폴더 (Shared Folders)
•    더 나은 비디오 지원 (Better Video Support)
•    심리스 윈도우 (Seamless Windows)
•    클립보드 공유 (Shared Clipboard)
•    시간 동기화 (Time Synchronization)
■     Virtual box 를 reboot 합니다.
$ sudo reboot
■     공유 폴더를 위한 설정을 진행합니다.
•      vitual box 에서 파일 관리자(Nautilus)를 열고, 공유 폴더가 있는지 확인합니다.•      공유 폴더를 들어가보면 사용자가 vboxsf 그룹에 없어서 다음과 같은 에러가 발생합니다.•      아래와 같은 명령어를 실행하여 vboxsf 그룹에 사용자를 추가합니다.
$ sudo usermod -G vboxsf -a NVIDIA
(참고 : Virtual Box 를 설치할 때 사용자명을 NVIDIA 가 아닌 다른 이름으로 설치했다면 NVIDIA 가 들어가는 자리에 사용자명을 입력하면 됩니다.)
•      아래와 같은 명령어를 실행하여 현재 사용중인 아이디가 vboxsf 그룹에 들어가있는지 확인합니다.
$ cat /etc/group
•      Virtual Box 를 reboot 합니다.
$ sudo reboot
•      Window PC 에 테스트 할 텍스트 파일을 만들고, 공유 폴더 경로와 Virtual Box 내의 공유 폴더 안에 같은 파일이 있는지 확인합니다. Window PC 에 있는 파일을 Virtual Box 로 옮겨야 할 때 공유 폴더를 사용하면 편리하게 옮길 수 있습니다.Visual Studio Code 설치 후 세팅
Visual Studio Code 는 원격으로 소스 코드를 수정하고, 파일 복사, 다운로드하는데 매우 유용합니다. Window PC 또는 Virtual Box + Ubuntu 에 설치하여 원격(ssh)으로 Jetson 디바이스의 소스 코드들을 수정하는 목적으로 활용합니다. 
■     Window PC 에서 Visual Studio Code 설치
1.  Window PC 의 인터넷 브라우저를 실행하고, 주소창에 아래 site 를 입력 후, Window PC 용 Visual Studio Code 설치 파일을 다운로드 받습니다. (ver 1.84)
https://code.visualstudio.com/updates/v1_84
2.  윈도우 파일 탐색기를 열고, ‘다운로드’ 폴더로 이동하면 아래 화면과 같이 다운로드
받은
‘VSCodeUserSetup-x64-1.84.2.exe’ 
파일을 볼 수 있습니다.3.  아래 내용을 참고하여 설치를 진행합니다.
•      ‘동의합니다’를 선택한 후 ‘다음’ 버튼을 클릭합니다.
•      ‘다음’ 버튼을 클릭합니다.•      ‘다음’ 버튼을 클릭합니다.
•      ‘다음’ 버튼을 클릭합니다.•      ‘설치’ 버튼을 클릭합니다.
•      ‘종료’ 버튼을 클릭합니다.•      Windows 검색창에 Visual Studio Code 를 입력하고, 표시된 항목을 클릭하여 실행합니다.
4.  Window PC 에서 Visual Studio Code 를 설치할 경우 자동 업데이트 기능이 기본적으로 활성화되어 있습니다. 업데이트가 진행되면 Jetson Nano 와의 SSH 연결이 정상적으로 되지 않는 문제가 발생할 수 있으므로, 설치 직후 자동 업데이트 기능을 비활성화하는 것이 좋습니다.
아래 안내에 따라 자동 업데이트를 비활성화 해주세요. •         Visual Studio Code 에서 File – Preferences – Settings 을 클릭합니다.
•      검색창에 ‘update’를 입력합니다.
•      빨간색 네모로 표시된 부분을 사진처럼 변경합니다. 
⬧       Auto Update – None
⬧       Enable Windows Background updates – 체크 해제⬧       Update: Mode – None
•      다음 사진과 같은 창이 나타날 경우 restart 를 눌러주세요.
(참고: 초기 설정 시 Visual Studio Code 가 이미 1.100.x 버전으로 업데이트되어 있을 수 있습니다. 이 경우, 제어판에서 해당 프로그램을 제거한 뒤 1.84.2 버전을 다시 설치하면 자동 업데이트 없이 해당 버전으로 유지됩니다.)■     Virtual Box + Ubuntu 에서 Visual Studio Code 설치
1.  Virtual Box + Ubuntu 의 인터넷 브라우저를 실행하고, 주소창에 아래 site 를 입력 후, ubuntu 18.04 용 Visual Studio Code 설치 파일을 다운로드 받습니다. (ver 1.84)
https://code.visualstudio.com/updates/v1_84
(참고: 최신 version 의 (24.05 월 기준 ver 1.89.1) Visual Studio Code 가 ubuntu 18.04 에 설치되지 않아 구 version 의 Visual Studio Code 를 설치합니다.)
2.  리눅스 파일 탐색기(nautilus)를 열고, ‘Downloads’ 폴더로 이동하면 아래 화면과 같이
다운로드 받은
‘code_1.84.2-1699528352_amd64.deb’ 
파일을 볼 수 있습니다.
3.
‘code_1.84.2-1699528352_amd64.deb’ 
파일을 더블 클릭하면, 아래 화면과 같이
설치창이 나타납니다. ‘Install’ 버튼을 눌러 설치를 진행합니다.4.  설치가 완료되면, Host PC(Virtual Box + Ubuntu)의 바탕화면 왼쪽 아래에 있는 “Show Applications” 버튼을 눌러, 설치한 Visual Studio Code 를 찾아 실행합니다. 
또는 터미널에서 ‘code’를 입력하면 Visual Studio Code 를 실행할 수 있습니다.
Jetson Nano MFI Flash (Jetpack4.6) 및 Jetson 초기 세팅
n    Guest PC (Ubuntu) 에서 Jetson Nano OS 설치 패키지를 복사할 디렉터리를 생성합니다. (현재 경로 : ‘~’) 
$ mkdir jetson
 
n    공유 폴더를 이용하여 Host PC 에 있는 Jetson Nano OS 설치 패키지 파일 (allai-mCi-jcb100- nano.tbz2)을 Virtual Box 의 Guest PC (Ubuntu)의 ‘~/jetson’ 경로에 복사합니다. 
n    Guest PC(Ubuntu)에서 아래 명령어를 이용해서 압축파일을 풀어줍니다.  (현재 경로 : ~/jetson)
$ tar xvjf allai-mfi-jcb100-nano.tbz2
n    압축해제가 다 되면 해당 폴더로 이동해주세요. 
$ cd mfi_jetson-nano-emmc/n    Jetson Nano 와 Window PC 를 5pin 으로 연결하고, Recovery mode 를 만들어주세요. 
n    Virtual box 상단에 장치 – USB 에서 NVIDIA Corp, APX [0102] 를 선택합니다. n    Guest PC (Ubuntu) 에서 터미널 창을 열어 아래 명령어를 입력한 후 표시된 부분과 같이 ‘0955:7f21 NVIDIA Crop.’ 로 뜨는지 확인합니다. 
$ lsusb
n    압축을 해제한 폴더(~/jetson/mCi_jetson-nano-emmc/에서 아래 명령어를 실행합니다. 
$ sudo ./nvmflash.shn    아래처럼 Flash complete (SUCCESS)라고 뜨면 jetson nano Flash 가 성공적으로 완료된 것입니다.  
 
 (참고 : Flash complete (SUCCESS)가 출력됐다면, Jetson Nano 에 다음 사진과 같이
연결하고, 다음 내용부터 진행합니다.)n    Jetson Nano 에 키보드,마우스 USB 와 Power, HDMI 를 연결한 다음 아래 화면이 나타나면, 체크박스에 체크를 한 뒤 Continue 버튼을 클릭합니다. 
 
n     English 를 선택한 뒤 Continue 버튼을 클릭합니다. (설치 경로나 파일 경로에 한글이 
포함되면 호환성 문제가 발생할 수 있으므로, 언어는 영어로 설정하는 것을 권장합니다.) 
 
 n     English 를 선택한 뒤 Continue 버튼을 클릭합니다. (설치 경로나 파일 경로에 한글이 
포함되면 호환성 문제가 발생할 수 있으므로, 언어는 영어로 설정하는 것을 권장합니다.) 
 
n    Seoul 을 입력한 뒤 Continue 버튼을 클릭합니다. (Jetson Nano 에 랜선을 연결한 
상태에서는 지역이 자동으로 Seoul 로 설정되며, Continue 버튼을 클릭하여 진행합니다.) 
 
n    Name 과 username, passwd 를 모두 NVIDIA 로 입력한 후 Continue 버튼을 클릭해주세요.  (참고 : 아이디와 패스워드는 NVIDIA 로 통일합니다.)  
n    Continue 버튼을 클릭해주세요. 
 
(참고 : Jetson Nano 가 설정이 완료된 후 부팅이 됐다면, SD 카드를 세팅하기 위해 Host PC 에서 다음 내용을 진행해주세요)Host PC(Window PC) 에서 SD Card Image 굽고 Jetson 부팅 시스템 변경
n    Host PC(Window PC)에서 SD card 에 이미지 굽기위해 사용되는 tool 인 BalenaEtcher 를 설치합니다. 
 
n    제공된 SD card 를 SD 어댑터에 삽입하고, 어댑터를 USB 방식의 SD 카드 리더기에 연결한 후, 이를 Host PC(Window PC)에 꽂아 사용합니다. 
 n    BalenaEtcher 를 관리자 권한으로 실행한 후 Image File(실습자료로 제공된 ‘jcb100_nano_sd.img’ 파일)과 Target(Generic STORAGE DEVICE Media 128GB SD card)을 선택합니다. 
 
n     ‘Yes, I’m sure ’ 버튼을 클릭합니다. 
 
n    다음 내용이 나오면 취소를 눌러주세요 
 n    Flash Completed! 문구가 나오면 Flash 가 완료된 것 입니다. SD 카드 리더기를 Host PC 와 분리해주세요. 
 
n    Jetson eMMC 에 Flash 가 완료되어 부팅이 되었으면 Jetson Nano Board SD Card Slot 에 SD Card 를 꽂아줍니다. 
 
 
(참고 : SD card 이미지를 구운 후 부팅하면, user 와 passwd 는 모두 NVIDIA 로 고정되어 있습니다.)
n    Jetson Nano 에서 SD card 가 인식됐는지 확인하고, Flash 된 SD card 의 공간을 gparted 도구를 이용해서 늘려줍니다.  •      Jetson Nano 에서 부팅한 후 이미지와 같이 사이드 메뉴바에 아이콘으로 SD card 가 인식됐는지 확인합니다. 
 
•      gparted 를 설치한 후 실행합니다. 
(참고 : 인터넷이 연결되어 있지 않으면 에러가 발생할 수 있습니다. 이더넷 케이블을 연결해주세요.) 
$ sudo apt install gparted
 
$ sudo gparted
•      gparted 를 실행했을 때 다음과 같은 창이 뜰 경우 Fix 를 클릭합니다. 
•      /dev/mmcblk1 로 이동 후 번호 순서대로 클릭합니다.  
 
•      Size 를 늘려주고 Resize 를 눌러주세요.  
•      순서대로 누른 후 적용이 완료되면 close 버튼을 눌러줍니다. 
  
•      Size 가 늘어난 것을 확인합니다. 
 •      df 명령어로 크기를 한번 더 확인합니다. $ df -h 
 
n    터미널 창을 열어서 extlinux.conf 를 vi 에디터 또는 gedit 으로 열어줍니다.  
빨간색 네모로 표시된 부분을 mmcblk1p1 로 바꾸고 저장 후 닫아줍니다.
(주의 : 잘못 바꿀 경우 부팅이 안되어 다시 flash 하는 상황이 생길 수 있습니다. 실수하지 않도록 주의해주세요)
•      vi 로 편집 
$ sudo vi /boot/extlinux/extlinux.conf
  
 •      gedit 으로 편집 
$ sudo gedit /boot/extlinux/extlinux.conf
 
 n    Reboot 해주세요. 
$ sudo reboot
 
n    Reboot 이 되면 터미널을 열어서 아래 명령어를 실행하여 Filesystem ‘/dev/mmcblk1p1’이 ‘/’(root)에 Mount 되어있는지 확인해주세요. 
$ df -h
 NVIDIA Jetson
NVIDIA Jetson
▪  NVIDIA Jetson
•   CPU(Cortex-A: Tegra)와 NVIDIA GPU 그리고 NPU등을 하나의 SOC(System On Chip)에 탑재한 임베디드 플랫폼
•   Embedded Edge Device에서 NVIDIA의 고성능 병렬처리 연산 GPU를 일반 SW에서도 활용하도록 하는 'CUDA' 와 'CUDA'를 기반으로 하는 Deep-Learning (cu-DNN) 환경 및 주요 Deep-Learning 프레임워크
(예: tensorflow, pytouch)에 대한 다양한 SW 라이브러리와 예제코드 제공
•   SOM(System-On-Module) 형태로 Hardware를 설계하며, 개발 시간과 비용 절감 가능
•   Jetson Nano, TX2 NX, Xavier NX, AGX Xavier, Orin-Nano, Orin NX, AGX Orin, Thor등이 있음NVIDIA Jetson Module(SOM)
▪  NVIDIA Jetson Module (SOM)
•   AI 작업 부하를 처리하도록 특별히 설계되어 복잡한 데이터를 처리하고 edge 디바이스에서 AI 알고리즘을 실행하는데 필요한 컴퓨팅 성능을 제공
•   CPU, GPU, 메모리 및 다양한 인터페이스를 단일 소형 모듈에 통합
▪  NVIDIA Jetson Nano
•   128개의 NVIDIA의 CUDA 코어를 장착한 Maxwell 아키텍쳐
•   AI Performance : 472 GFLOPs
•   GPU : 128-core NVIDIA Maxwell™ GPU
•   CPU : Quad-Core Arm® Cortex®-A57 MPCore processor
Jetson Nano SOM
NVIDIA Jetson Series Specification #1
Feature
Jetson NANO
Jetson TX2 NX
Jetson Xavier NX
Jetson Orin Nano 4GB
Jetson Orin Nano 8GB
Jetson Orin NX 8GB
Jetson Orin NX 16GB
AI Performance   472 GFLOPs
1.33 TFLOPs
256-core NVIDIA Pascal™ GPU
40 TOPS
GPU
CPU
128-core NVIDIA Maxwell™ GPU
21 TOPs
384-core NVIDIA Volta™ GPU with 48 Tensor Cores
20 TOPS
512-core Ampere, with 16 Tensor Cores
1024-core Ampere, with 32 Tensor Cores
70 TOPS
1024 Core Ampere, with 32 Tensor Cores
100 TOPS
1024 Core Ampere, with 32 Tensor Cores
Quad-Core ARM® Cortex®-A57 Dual-Core NVIDIA Denver 2 64-
6-core NVIDIA Carmel 
6-core Arm® Cortex®-A78AE      6-core Arm® Cortex®-A78AE      6-core Arm® Cortex®-A78AE      8-core Arm® Cortex®-A78AE
MPCore
Bit CPU and Quad-Core ARM®   ARM®v8.2 64-bit CPU 6MB L2 
Memory               4 GB 64-bit LPDDR4 25.6 GB/s
DL Accelerator    -
Vision Accelerator Storage
-
16 GB eMMC 5.1
Cortex®-A57 MPCore processor
4 GB 128-bit LPDDR4
51.2 GB/s
-
-
16 GB eMMC 5.1
1x 4Kp @ 60 | 3x 4K @ 30
4x 1080 @ 60 | 8x 1080 @ 30 
(H.265)
+ 4MB L3
8 GB/16GB 128-bit LPDDR4x 59.7 GB/s
2x NVDLA Engines
-
16 GB eMMC 5.1
4GB 64-bit LPDDR5 34 GB/s
-
-
8GB 128-bit LPDDR5 68 GB/s
-
-
8GB 128-bit LPDDR5 102.4 GB/s
(1x) NVDLA V2.0 PVA v2.0
16GB 128-bit LPDDR5 102.4 GB/s
(2x) NVDLA V2.0 PVA v2.0
Supports External NVMe             Supports External NVMe             Supports external NVMe              Supports external NVMe
Video Encode     250MP/sec
1x 4K @ 30 (HEVC) 2x 1080p @ 60 (HEVC)
2x 4K @ 60 | 4x 4K @ 30 | 10x 1080p @ 60 | 22x 1080p @ 30 (H.265)
1080p30 supported by 1-2 CPU  1080p30 supported by 1-2 CPU  1x 4K60 | 3x 4K30| 6x 1080p60  1x 4K60 | 3x 4K30| 6x 1080p60 
cores
cores
| 12x 1080p30 (H.265), H.264, H.265, AV1
| 12x 1080p30 (H.265), H.264, H.265, AV1
Video Decode     500 MP/sec
1x 4K @ 60 (HEVC) 4x 1080p @ 60 (HEVC)
2x 4K @ 60 | 4x 4Kp @ 30 | 7x 1080p @ 60 | 14x 1080p @ 30 (H.265 & H.264)
2x 8K @ 30 | 6x 4K @ 60 | 12x 4K @ 30 | 22x 1080p @ 60 | 44x 1080p @ 30 (H.265)
1x 4K60 (H.265) | 2x 4K30 (H.265) | 5x 1080p60 (H.265) 11x 1080p30 (H.265) 
1x 4K60 (H.265) 5x 1080p60 (H.265)
1x 4K60 (H.265) 3x 4K30 (H.265) 6x 1080p60 (H.265)
1x 8K30 (H.265) 2x 4K60 (H.265) 9x 1080p60 (H.265)
Camera
Up to 4 cameras
12 lanes MIPI CSI-2
D-PHY 1.1 (up to 18 Gbps)
Up to 5 cameras (12 via virtual channels)
12 lanes MIPI CSI-2 (3×4 or 5×2)
D-PHY 1.2 (up to 30 Gbps)
Up to 6 cameras (24 via virtual channels)
12 lanes MIPI CSI-2
D-PHY 1.2 (up to 30 Gbps)
Up to 4 cameras (8 via virtual channels***)
8 lanes MIPI CSI-2
D-PHY 2.1 (up to 20Gbps)
1 x4 + 3 x1 (PCIe Gen3, Root Port, & Endpoint)
Up to 4 cameras (8 via virtual channels***)
8 lanes MIPI CSI-2
D-PHY 2.1 (up to 20Gbps)
Up to 4 cameras (8 via virtual channels***)
8 lanes MIPI CSI-2
D-PHY 2.1 (up to 20Gbps)
Up to 4 cameras (8 via virtual channels***)
8 lanes MIPI CSI-2
D-PHY 2.1 (up to 20Gbps)
PCI Express        1 x4
(PCIe Gen2)
Mechanical          69.6mm x 45mm
260-pin SO-DIMM connector
1 x1 + 1 x2, total 30GT/s (PCIe Gen2)
69.6mm x 45mm
260-pin SO-DIMM connector 7.5W - 15W
1 x1 + 1 x4
(PCIe Gen3, Root Port & Endpoint)
69.6mm x 45mm
260-pin SO-DIMM connector 10W - 20W
1 x4 + 3 x1 (PCIe Gen3, Root Port, & Endpoint)
1 x4 + 3 x1 (PCIe Gen4, Root Port, & Endpoint)
Power
5W - 10W
69.6mm x 45mm
260-pin SO-DIMM connector 5W - 10W
69.6mm x 45mm
260-pin SO-DIMM connector 7W - 15W
69.6mm x 45mm
260-pin SO-DIMM connector 10W - 20W
1 x4 + 3 x1 (PCIe Gen4, Root Port, & Endpoint)
69.6mm x 45mm
260-pin SO-DIMM connector 10W - 25WNVIDIA Jetson Series Specification #2
Feature
Jetson AGX Xavier 32GB
Jetson AGX Xavier 64GB
Jetson AGX Orin 32GB
Jetson AGX Orin 64GB
Jetson AGX Orin industrial
AI Performance       32 TOPS
32 TOPS
512-core NVIDIA Volta™ GPU (with 64 Tensor cores)
8-core NVIDIA Carmel ARM® v8.2 64-bit CPU 8 MB L2 + 4 MB L3
200 TOPS
275 TOPS
248 TOPS
GPU CPU
Memory
512-core NVIDIA Volta™ GPU (with 64 Tensor cores)
8-core NVIDIA Carmel ARM® v8.2 64-bit CPU 8 MB L2 + 4 MB L3
1792 Core Ampere, with 56 Tensor Cores      2048 Core Ampere, with 64 Tensor Cores      2048 Core Ampere, with 64 Tensor Cores
8-core Arm® Cortex®-A78AE v8.2 64-bit CPU 2MB L2 + 4MB L3
64 GB 256-bit LPDDR4x 136.5 GB/s              64 GB 256-bit LPDDR4x 136.5 GB/s              32GB 256-bit LPDDR5 205 GB/s
DL Accelerator        (2x) NVDLA V1.0
Vision Accelerator (2x) 7-way VLIW Processor
Storage
32 GB eMMC 5.1
Video Encode         4x 4K @ 60 (H.265) 16x 1080p @ 60 (H.265) 32x 1080p @ 30 (H.265)
Video Decode         2x 8K @ 30 (H.265) 6x 4K @ 60 (H.265) 26x 1080p @ 60 (H.265) 52x 1080p @ 30 (H.265)
(2x) NVDLA V1.0
(2x) 7-way VLIW Processor 32 GB eMMC 5.1
4x 4K @ 60 (H.265) 16x 1080p @ 60 (H.265) 32x 1080p @ 30 (H.265)
2x 8K @ 30 (H.265) 6x 4K @ 60 (H.265) 26x 1080p @ 60 (H.265) 52x 1080p @ 30 (H.265)
(2x) NVDLA V2.0
(2x) 7-way VLIW Processor 64 GB eMMC 5.1
1x 4K60 (H.265) 3x 4K30 (H.265) 6x 1080p60 (H.265) 12x 1080p30 (H.265) 1x 8K30 (H.265) 2x 4K60 (H.265) 4x 4K30 (H.265) 9x 1080p60 (H.265) 18x 1080p30 (H.265)
2-core Arm® Cortex®-A78AE v8.2 64-bit CPU 3MB L2 + 6MB L3
64GB 256-bit LPDDR5 205 GB/s
(2x) NVDLA V2.0
(2x) 7-way VLIW Processor 64 GB eMMC 5.1
2x 4K60 (H.265) 4x 4K30 (H.265) 8x 1080p60 (H.265) 16x 1080p30 (H.265)
2-core Arm® Cortex®-A78AE v8.2 
64-bit CPU 3MB L2 + 6MB L3
64GB 256-bit LPDDR5 (+ ECC) 204.8GB/s
(2x) NVDLA V2.0
(2x) 7-way VLIW Processor 64 GB eMMC 5.1
1x 4K60 (H.265) 3x 4K30 (H.265) 7x 1080p60 (H.265) 15x 1080p30 (H.265)
1x 8K30 (H.265) 3x 4K60 (H.265) 7x 4K30 (H.265) 11x 1080p60 (H.265) 22x 1080p30 (H.265)
1x 8K30 (H.265) 3x 4K60 (H.265) 7x 4K30 (H.265) 11x 1080p60 (H.265) 22x 1080p30 (H.265)
Camera
Up to 6 cameras
(36 via virtual channels)
16 lanes MIPI CSI-2 | 8 lanes SLVS-EC D-PHY 1.2 (up to 40 Gbps)
Up to 6 cameras
(36 via virtual channels)
16 lanes MIPI CSI-2 | 8 lanes SLVS-EC D-PHY 1.2 (up to 40 Gbps)
Up to 6 cameras (16 via virtual channels) 16 lanes MIPI CSI-2
D-PHY 2.1 (up to 40Gbps) | C-PHY 2.0 (up to 164Gbps)
Up to 6 cameras (16 via virtual channels) 16 lanes MIPI CSI-2
D-PHY 2.1 (up to 40Gbps) | C-PHY 2.0 (up to 164Gbps)
Up to 6 cameras (16 via virtual channels) 16 lanes MIPI CSI-2
D-PHY 2.1 (up to 40Gbps) | C-PHY 2.0 (up to 164Gbps)
PCI Express            1 x8 + 1 x4 + 1 x2 + 2 x1
(PCIe Gen4, Root Port and Endpoint)
Mechanical              100 mm x 87 mm
699-pin connector
Integrated thermal transfer plate
1 x8 + 1 x4 + 1 x2 + 2 x1
(PCIe Gen4, Root Port and Endpoint)
100mm x 87mm
699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate
10W - 30W
-25°C to 80°C at TTP
Up to 2 x8 + 1 x4 + 2 x1 (PCIe Gen4, Root Port, & Endpoint)
Up to 2 x8 + 1 x4 + 2 x1 (PCIe Gen4, Root Port, & Endpoint)
100mm x 87mm
699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate
Power
10W - 30W
Temperature           -25°C to 80°C at TTP
15W - 40W
-25°C to 80°C at TTP
100mm x 87mm
699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate
15W - 60W
-25°C to 80°C at TTP
Up to 2 x8 + 1 x4 + 2 x1 (PCIe Gen4, Root Port, & Endpoint)
100mm x 87mm
699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate
15W – 75
-25°C to 85°C at TTP
NVIDIA Jetson Developer Kit
▪  NVIDIA Jetson Developer kit
•   NVIDIA Jetson Developer Kit은 Jetson SOM을 기반으로 한 개발 보드로, AI 및 엣지 컴퓨팅 애플리케이션 을 개발하고 테스트하는데 사용
•   Jetson 사용자들이 좀 더 쉽게 소프트웨어 개발 하기 위한 표준 하드웨어 플랫폼으로 하드웨어 제작 이전
에 소프트웨어 구현 및 시험을 가능하게 해줌
Jetson Nano Developer KitJetson Module(SOM) vs Jetson Developer Kit
▪  Jetson Module(SOM)과 NVIDIA Jetson Developer kit 차이점?
[NVIDIA Jetson Module(SOM)]
•   Jetson 모듈은 양산 및 운영 환경에 적합하며, 각 모듈은 사전 설치된 소프트웨어 없이 판매됨
•   최종 양산용으로 설계되거나 판매되는 캐리어(I/O interface) 보드에 Jetson 모듈을 부착하고, 개발한 소프트웨어를 탑재 (Image Flash)하여 배포해야 함
[NVIDIA Jetson Developer Kit]
•   각 Jetson Developer Kit에는 참조용 캐리어 보드와 비양산 용도의 Jetson 모듈이 포함
•   Jetpack SDK를 통해서 소프트웨어를 개발하고 테스트하는데 사용되며, 양산 용도로 사용되지 않음
▪  Jetson Developer Kit은 양산 용도가 아니며, Jetson 모듈은 Operating-Life time내 양산 환경에 맞춰 설계 됨
NVIDIA Jetson Platform 하드웨어 구성
▪  NVIDIA Jetson SOM 구성
•   CPU/GPU
•   RAM
•   NVDLA
•   NV Encoder/NV Decoder, NV JPEG
•   ISP/VIC
•   eMMC(Storage)
•   그리고 외부 인터페이스
Jetson Xavier NX
▪  개발자는 Jetson SOM과 연결할 커넥터와 사용할 외부 인터페이스를 구현한 Carrier Board를 제작 생산하면, Jetson에서 개발한 소프트웨어 이식 가능NVIDIA Jetson Platform 소프트웨어 구성
▪  NVIDIA는 Jetson Platform 개발자를 위해 커널과 Bootloader, 소스코드, 툴 그리고 AI 소프트웨어 패키지를 모아 Jetpack이라는 소프트웨어 패키지 제공
jetpack https://docs.NVIDIA.com/jetson/archives/index.html
Developer guide https://docs.NVIDIA.com/jetson/archives/r34.1/DeveloperGuide/index.html Jetson Linux Archive https://developer.NVIDIA.com/embedded/jetson-linux-archive
•   Linux Kernel
•   Bootloader
•   BSP, Drivers
• Flash Utilities
•   Rootfs
Jetpack SDK
JCB100 (Jetson Carrier Board)
▪  JCB100
•   NVIDIA Jetson Module(SoM)을 운영하기 위한 시스템 보드
•   다양한 외부 인터페이스와 NVIDIA의 Jetson Nano Developer Kit과 Jetson Xavier NX Developer kit에 호환되 도록 설계 되어 있으며, 추가적인 외부 저장 장치 및 CAN 통신을(Jetson Nano제외) 지원할 수 있도록 설계 되어 있음.
Jetson Carrier Board (JCB100)JCB100
JCB100 인터페이스
Jetson 모듈별 인터페이스 지원 현황
JCB100Linux Network
Linux Network
▪  리눅스는 네트워크 관리와 설정에서 강력하고 유연한 기능을 제공
▪  다양한 도구와 명령어를 통해 네트워크 인터페이스를 구성하고 , 네트워크 상태를 모니터링 할 수 있음
▪  네트워크와 관련된 대표적인 명령어로는 ip, ifconfig, wget, curl, ssh 등이 있음ifconfig
▪ 유닉스 계열 운영체제에서 네트워크 설정을 간단하게 관리하기 위해 만들어짐
▪  네트워크 인터페이스 설정 및 관리 기능
▪  네트워크 상태 확인 기능
모든 네트워크 인터페이스 정보 표시
ip
▪ ifconfig 명령어의 기능을 확장하고, 더 많은 네트워크 설정을 지원
▪  네트워크 인터페이스 설정 및 관리 기능
▪  라우팅 테이블 관리 기능
▪  네트워크 장치 관리 기능
모든 네트워크 인터페이스 정보 표시wget
▪  웹에서 파일을 다운로드하기 위해 만들어짐
▪  HTTP, HTTPS, FTP등 다양한 프로토콜을 통해 파일을 다운로드
▪  배치 다운로드와 재시도 기능이 필요할 때 유용
▪  더 엄격하게 속도를 제한하고, 네트워크 트래픽을 모니터링하며 일정한 시간 간격으로 데이터를 전송
curl
▪  웹 API와의 상호작용을 위해 만들어짐
▪ HTTP, HTTPS, FTP등 다양한 프로토콜 지원
▪  유연성과 다양한 기능을 중점으로 설계ssh(secure shell)
▪  네트워크를 통해 안전하게 원격 시스템에 접속하고 명령을 실행할 수 있는 프로토콜
▪  비암호화된 통신인 Telnet을 대체하기 위해 개발
▪  암호화된 연결을 통해 데이터 전송의 기밀성과 무결성을 보장
▪ 리눅스에서 ssh에 관련된 대표적인 명령어로는 ssh(원격접속)와 scp(파일전송)가 있음
Hello!
y6nW$i
Hello!
Encrypt
Decrypt
SSH client
SSH server
ssh(secure shell) – Visual Studio Code에서 ssh 연결
▪  vscode의 ssh 연결 기능은 원격 서버의 리소스를 활용하면서 도 로컬에서 개발을 계속할 수 있는 도구
▪  개발자가 원격 시스템에서 직접 작업하는 것처럼 로컬 개발 환경을 사용할 수 있도록 해줌
▪  ssh 연결을 통해 vscode는 원격 서버에서 실행되는 서버 컴 포넌트를 시작하고, 이 서버와 로컬 vscode 클라이언트 사이 에 터널을 설정
▪  이 터널을 통해 vscode는 원격 파일 시스템을 탐색하고, 파 일을 열고 저장하며, 명령을 실행할 수 있음
▪  코드 편집, 디버깅, 터미널 사용 등 모든 작업이 ssh 터널을 통해 원격 서버와 동기화ssh(secure shell) – vscode에서 ssh 연결
<https://code.visualstudio.com/docs/remote/ssh>
Jetpack LibraryJetpack Library
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
Github: https://github.com/jetsonhacksnano실습 1-4
- Linux Network 관련 명령어 실습
- Jetson ←→  Host PC vscode SSH 연결
- Jetson 시스템 관련 명령어 실행 및 JetPack 설치실습 1-4: 리눅스 네트워크, Jetpack Library
네트워크 인터페이스 – ip, ifconfig
리눅스에서 네트워크 인터페이스를 구성하고 관리하기 위한 명령어 입니다. 네트워크 설정과 관련된 다양한 정보를 확인하고 설정할 수 있습니다.
n    ip 명령어를 입력하여 Jetson Nano 의 네트워크 인터페이스를 확인하세요. 모든 네트워크 인터페이스의 IP 주소 정보를 표시합니다.
$ ip addr show
n    모든 네트워크 인터페이스의 상태를 표시합니다.
$ ip link show
n    네트워크 인터페이스의 상태를 비활성화 상태로 변경합니다. 
$ sudo ip link set eth0 downn    네트워크 인터페이스의 상태를 활성화 상태로 변경합니다.
$ sudo ip link set eth0 up
n    시스템의 현재 라우팅 테이블을 표시합니다.
$ ip route show
n    ipconfig 명령어를 입력하여 Jetson Nano 의 네트워크 인터페이스를 확인하세요. 모든 네트워크 인터페이스 정보를 표시합니다.
$ ifconfign    특정 네트워크 인터페이스 정보를 표시합니다.
$ ifconfig eth0
n    네트워크 인터페이스의 상태를 비활성화 상태로 변경합니다. 
$ sudo ifconfig eth0 downn    네트워크 인터페이스의 상태를 활성화 상태로 변경합니다.
$ sudo ifconfig eth0 up파일 다운로드 – wget, curl
웹에서 파일을 다운로드 하기 위한 명령어 입니다. 주로 HTTP, HTTPS, FTP 프로토콜을 지원하며, 다운로드할 파일의 URL 을 입력하면 해당 파일을 로컬 컴퓨터에
다운로드합니다. 
web 의 resource 를 다운받는 과정을 실습합니다.
wget 과 curl 은 많은 옵션과 기능이 있지만 이번 시간에는 일부만 실습합니다.
n    wget 를 이용하여 파일을 다운로드 합니다. 먼저 apt 를 이용하여 wget 을 설치합니다.
$ sudo apt install wget
(참고 : 설치 중 Y/n 내용이 나올 경우 엔터를 누르세요.)
n 다운로드 할 파일의 원본 파일명으로 다운로드 합니다.
$ wget https://blog.naver.com/allai-
n    cat 명령어를 사용하여 파일 내용을 확인합니다.
$ cat allai-n    다운로드 할 파일을 특정 이름으로 다운로드합니다.
$ wget -O allai_blog.txt https://blog.naver.com/allai-
n    파일 다운로드 중 다운로드 속도를 제한합니다.
$ wget --limit-rate=0.5k https://blog.naver.com/allai-n    curl 을 이용하여 파일을 다운로드 합니다. 먼저 apt 를 이용하여 curl 을 설치합니다.
$ sudo apt install curl
(참고 : 설치 중 Y/n 내용이 나올 경우 엔터를 누르세요.)
n    다운로드 할 파일의 원본 파일명으로 다운로드합니다.
$ curl -O https://blog.naver.com/allai-
n    다운로드 할 파일을 특정 이름으로 다운로드합니다.
$ curl -o allai-blog.txt https://blog.naver.com/allai-
n    curl 과 >를 사용해서 파일을 다운로드합니다.
$ curl https://blog.naver.com/allai- > allai_resource.txt
n    다운로드 할 파일을 여러 개의 이름을 가진 파일로 다운로드합니다.
$ curl -O https://blog.naver.com/allai-/allai[0-5].txtn    파일 다운로드 중 다운로드 속도를 제한합니다.
$ curl --limit-rate 500B -o allai_limit_rate.txt https://blog.naver.com/allai-
(참고 : wget 은 다운로드 속도를 더 엄격하게 제한하며, 네트워크 트래픽을 모니터링하고 일정한 시간 간격으로 데이터를 전송하는 방식으로 속도 제한을 구현합니다. curl 은 버퍼를 사용하여 데이터를 다운로드하는 동안 대기 시간을적용합니다. 이 방식은 설정된 속도 제한보다 순간적으로 더 빠르게 다운로드될 수 있습니다. 위와 같은 이유로 curl 이 다운로드 속도가 더 빠를 수 있습니다.)
SSH 원격 시스템 실습
ssh(secure Shell)는 네트워크 상에서 다른 컴퓨터에 접속하거나 명령을 실행하거나
파일을 전송하는데 사용되는 프로토콜입니다. 보안이 취약한 네트워크에서 암호화된 통신을 제공하여, 데이터의 도청이나 변조를 방지하고 주로 원격 실행이나 파일 전송에 사용됩니다.
n    SSH 사용방법
Jetson Nano 의 ip 를 확인한 후 Window PC CMD 창 또는 Virtual Box + Ubuntu 터미널에서 ssh 명령어를 사용하여 Jetson Nano 에 접속합니다. 접속 시 비밀번호를 입력해야 하며, 입력 중에는 화면에 표시되지 않지만 정상적인 동작이므로 그대로 입력해 주시면 됩니다.
사용법 : $ ssh [아이디]@[서버 주소]
예) ssh NVIDIA@172.30.1.5
n    SCP 사용방법Jetson Nano 의 ip 를 확인한 후 다른 Window PC CMD 창 또는 Virtual Box (Ubuntu) 터미널에서 scp 를 이용하여 Jetson Nano 에 파일을 전송합니다.
•      다른 서버로 전송
사용법 : $ scp [option] [보낼 파일] [아이디]@[서버 주소]:[저장할 경로]
예) scp text.txt NVIDIA@172.30.1.5:~
<Window CMD 창> 
<Window 의 Jetson Nano 의 ‘~’ 경로로 전송 받은 test.txt 확인>
•      서버로부터 다운
사용법 : $ scp [option] [아이디]@[서버주소]:[파일경로] [저장할경로]
예) scp NVIDIA@172.30.1.5:~/test1.txt C:\Users\allai\Desktop\
<Window CMD 창><Jetson Nano ‘~’ 경로에 있는 test1.txt 파일이 Window PC 의 C:\Users\allai\Desktop\ 경로에 전송 됐는지 확인>
(참고: Ubuntu/Linux 에서는 /를, Windows PowerShell 에서는 \를 경로 구분자로 사용하므로, scp 명령어 실행 시 파일 경로 표기에 주의해 주세요.)Visual Studio Code SSH 연결
Host device : jetson Nano 
­
¯
Client device : Window or Ubuntu Host device
n    Host device (jetson nano)
•      SSH 설정 : SSH 연결을 이용해 원격으로 접근할 기기(Jetson Nano)에 openssh- server 를 설치해주세요.
$ sudo apt-get install openssh-server
(참고 : 설치 중 Y/n 내용이 나올 경우 엔터를 누르세요.)
• Jetson Nano 에서 아래 명령어를 실행하여 IP 주소를 확인해주세요.
$ ifconfig
n    Client device (Window or Ubuntu)
1. Visual Studio Code 가 실행되면 아래와 같은 순서로 ‘SSH extension’을 설치합니다.
①   왼쪽 메뉴에서 “Extension” 클릭
②   입력창에 “SSH”를 입력하고 “Remote-SSH” extension 선택
③   “install” 버튼 클릭2. Visual Studio Code 중앙의 “Remote SSH”에 대한 설명 화면에서 “install” 버튼을 누르면 설치가 시작됩니다.
‘Ctrl’ + ‘Shift’ + ‘P’
3. Visual Studio Code 가 활성화된 상태에서                          키를 동시에 누릅니다.
또는 메뉴 “Help” -> “Show All Commands”를 누르면, 아래 화면과 같이 ‘Command’입력창이 나타납니다.
4. 입력창에 “ssh”를 입력하고 아래 화면과 같이 ssh 관련 커맨드들이 나타나면……
“Remote-SSH: Add New SSH Host…”
를 선택합니다.5. 입력창이 “Enter SSH Connection Command”로 바뀌면, 아래와 같이 접속할 Jetson 디바이스의 SSH 커맨드를 입력합니다.
ssh 계정@IP 주소
예시: ssh NVIDIA@192.168.0.16
6. 새로 생성한 SSH 접속 커맨드를 저장할 위치를 묻는 화면에, default 위치를 선택합니다.“Open Config”
7.   그러면 오른쪽 하단에 아래와 같은 팝업이 나타난다.                     버튼을 누르면 생성한 SSH 접속 커맨드를 확인할 수 있습니다.
‘Ctrl’ + ‘Shift’ + ‘P’
8. 다시                          키를 동시에 눌러 아래와 같이 ‘Command’입력창이
나타나면, 
“Remote-SSH: Connect to Host…”
를 선택합니다.
9. 앞에서 생성한 SSH 접속 커맨드에 대한 IP 주소가 나타나면 선택합니다.
10. 그러면 새로운 Visual Studio Code 가 열리고, 접속 진행여부를 묻는 창이 나타나면                선택합니다. 
“Continue”11.   접속할 디바이스에 대한 “Password”를 묻는 창에 password 를 입력합니다. (예: NVIDIA)
12. 그러면 visual studio code 가 디바이스에 SSH 접속을 시도하고, 접속이 완료되면 아래 화면과 같이 왼쪽 하단에 디바이스의 IP 주소가 표시됩니다. 
13. Visual Studio Code 상단 오른쪽에 있는 “Explorer”버튼을 누르고, 버튼을 누릅니다. 
“Open Folder”14. “Open Folder”를 묻는 입력창이 나오면, default 경로(예: /home/NVIDIA/)를 선택하고 “OK” 버튼을 누릅니다.. 최초 SSH 접속일 경우 password 를 다시한번 묻는 창이 나옵니다.
15. 접속할 폴더에 대한 신뢰여부를 묻는 창이 나오면 아래와 같이           체크 박스를 선택하고              버튼을 누릅니다.
“Trust”
“Yes, ~~”16. SSH 접속 과정이 모두 끝나면, Visual Studio Code 오른쪽 패널을 통해서 Jetson 디바이스의 주요 폴더와 파일들을 선택하고, 수정할 수 있습니다. (참고: ssh 연결이 안될 경우 다음 내용을 따라하고 다시 한번 ssh 연결을 시도해주세요.)
방법 1
-    이더넷 케이블을 다시 연결합니다.
방법 2
-    Jetson nano 에서 다음 명령어를 실행합니다.
$ sudo apt purge openssh-server
$ sudo apt install openssh-serverJetson 시스템 정보 및 온도 확인
n Jetson information 관련 명령어를 확인합니다.
•      Ubuntu Version 을 확인합니다.
$ cat /etc/lsb-release
•      L4T Version 을 확인합니다.
$ cat /etc/nv_tegra_release
•      Kernel Version 을 확인합니다.
$ uname -a
n    PWM FAN 제어
Jetson 디바이스는 고성능 작업을 실행할 때 많은 열을 발생 시킬 수 있습니다. 이러한 과열 상태를 방지하기 위해 팬이 필요하며, PWM 팬은 정확한 속도 제어를 통해 장치의 온도에 맞춰 효율적으로 열을 배출할 수 있습니다.
•      현재 시스템 온도 확인 (결과 값 나누기 1000 하면 현재 시스템의 온도)
$ cat /sys/class/thermal/thermal_zone0/temp
à 시스템 온도가 약 46 도 정도임을 확인할 수 있습니다. (46000/1000)
•      온도에 따른 fan 제어를 합니다. 
fan-ctl git 을 clone 하고, clone 한 폴더로 이동합니다.
$ git clone https://github.com/jetsonworld/jetson-fan-ctl.git
$ cd jetson-fan-ctl 
•      install.sh 을 실행합니다. Install.sh 을 실행하면 서비스가 설치되고, 자동으로 실행됩니다.
$ sudo sh install.sh•      편집기로 config.json 을 수정합니다.
$ sudo vi /etc/automagic-fan/config.json
config.json 을 다음과 같이 수정합니다. 이 경우 60 도 이상에서 fan 속도가 최대로 작동하고, 40 도보다 낮아지면 팬이 꺼집니다.
{
“FAN_OFF_TEMP”:40, “FAN_MAX_TEMP”:60, “UPDATE_INTERVAL”:2, “MAX_PERF”:1
}
config.json
FAN_OFF_TEMP
이 온도(°C)보다 낮아지면 팬이 꺼짐
FAN_MAX_TEMP
FAN_MAX_TEMP 온도(°C) 이상이면 팬이 최대 속도로 작동함
UPDATE_INTERVAL 
온도 체크하는 주기 (초)
MAX_PERF 
“1”로 설정하면 Jetson 이 항상 최대 성능 모드로 동작하게 되어, 온도 변동이 줄고 팬 제어가 더 안정적으로 작동함 전력 소모를 줄이고 싶다면 “0”으로 설정하면 됨
•      service 명령어로 재부팅 없이 변경사항을 적용하세요.
$ sudo service automagic-fan restart
•      automagic-fan status 를 확인하세요.
$ sudo service automagic-fan status
(참고: 현재 시스템 온도가 설정한 FAN_OFF_TEMP 보다 낮을 경우 팬은 동작하지 않으며, 이 값을 초과할 경우 자동으로 팬이 동작하게 됩니다.)Jetpack Library, Jetson-stats 설치 및 유틸리티 사용
Jetson-stats 는 NVIDIA Jetson 시리즈를 모니터링하고 제어하기 위한 패키지입니다. 
보드를 분석하는 강력한 도구이며, jtop 이 있는 독립 실행형 응용 프로그램과 함께
사용하거나 파이썬 스크립트에서 가져올 수 있습니다. 자세한 유틸리티 사용 방법은 이후 시간에 진행하고, 이번시간에는 설치만 합니다.
n    Commercial 보드(JCB100)이기 때문에 SDK Manager 가 아닌, Linux repository 를 통해 NVIDIA-jetpack, jetson-stats 를 설치합니다.
•      apt 를 업데이트 합니다.
$ sudo apt update
•      NVIDIA-jetpack 을 설치합니다.
$ sudo apt install NVIDIA-jetpack
(참고 : 설치 중 Y/n 내용이 나올 경우 엔터를 누르세요.)
• python3-pip 를 설치합니다. (이미 설치한 경우 넘어가도 됩니다.)
$ sudo apt-get install python3-pip
•      jetson-stats 를 설치합니다.
$ sudo -H pip3 install -U jetson-stats
•      재부팅 합니다.
$ sudo reboot
n    Jetpack Library install broken error 발생 시 다음 내용을 따라해주세요. 1.  패키지 리스트 삭제
$ sudo rm -rf /var/lib/apt/lists/*
2.  apt clean
$ sudo apt-get clean
3.  apt update
$ sudo apt-get update
4.  jetpack library 설치$ sudo apt install NVIDIA-jetpack
(참고: Jetson Nano 는 NVIDIA 의 커스텀 커널과 부트로더를 기반으로 작동합니다. 따라서 Ubuntu 일반 시스템과 달리 전체 시스템 패키지를 업그레이드 (‘sudo apt upgrade’) 하면 Jetson 전용 커널 및 부팅 구성요소가 손상되어 부팅이 안되는 상태가 될 수 있습니다. 따라서 ‘sudo apt upgrade’ 명령어는 사용하지 마십시오.)
n    ‘jetson_release’ 도구를 이용하여 jetpack library 가 설치됐는지 확인합니다.
$ jetson_releasen    ‘jtop’ 도구를 이용하여 jetson nano 의 CPU, GPU, 메모리 사용량 등을 실시간으로 확인합니다.
$ jtop
•      jtop 을 실행할 경우 1 번 화면이 나타납니다 1 번은 시스템의 요약 정보
화면이며, CPU, GPU, 메모리, 디스크 사용량과 같은 전반적인 시스템 상태를 한눈에 볼 수 있습니다. 또한 각 하드웨어 자원의 온도, 전력 소비량 등을 볼 수 있습니다. 다른 메뉴로 전환하고 다시 1 번 메뉴를 보고싶으면 1 번을 누르면 됩니다.
•      2 번(GPU)을 누르면 GPU 사용 현황을 보여줍니다. AI 연산이나 영상 처리 작업 시 GPU 의 상태를 모니터링 할 때 유용합니다.•      3 번(CPU)을 누르면 CPU 사용 현황을 보여줍니다. 각 코어별로 사용률을 파악할 수 있습니다.
• 4 번(MEM)을 누르면 메모리 사용 현황을 보여줍니다. 시스템의 전체 메모리 용량과 현재 사용 중인 메모리의 양을 보여주며, 스왑 메모리 사용량도 함께 확인할 수 있습니다.•      5 번(ENG)을 누르면 엔진 상태들을 보여줍니다. Jetson Nano 의 하드웨어 가속 엔진들의 상태와 클럭 속도를 실시간으로 모니터링 할 수 있습니다.
•      6 번(CTRL)을 누르면 관리 화면을 보여줍니다. 전력 관리 상태와 클럭 최적화 설정을 모니터링하고 제어하는데 사용됩니다.•      7 번(INFO)을 누르면 정보 화면을 보여줍니다. 시스템의 주요 하드웨어 및 소프트웨어 정보를 확인할 수 있습니다.
•      Q 버튼을 누를 경우 jtop 이 종료됩니다.GPIO
GPIO
▪  General Purpose Input Output
▪  GPIO는 MCU의 일반적인 입력과 출력을 처리할 수 있는 외부 인터페이스
▪  제어를 위한 단순 신호를 출력하거나 외부에서 들어오는 신호를 디지털 입력으로 사용할 수 있음
▪  다양한 센서, LED, 버튼 등과 상호작용 가능Jetson.GPIO
▪  Jetson Nano 개발 보드에는 Raspberry Pi의 40pin 헤더와 유사한 40pin GPIO 헤더가 포함
▪  이러한 GPIO는 Jetson GPIO Library 패키지에 제공된 python 라이브러리를 사용하여 디지털 입 출력 제어 가능
▪  github : https://github.com/NVIDIA/jetson-gpio
▪  Jetson gpio sample 코드는 /usr/share/doc/jetson-gpio-common/sample/ 경로에 위치
40-pin Expansion 헤더Jetson Nano Interface - GPIO
Jetson Nano GPIO LED 제어
긴쪽+
짧은 쪽 (-)
<LED>
<Jetson Nano와 연결>LED ON/OFF
OFF
ON
실습 1-6
- Jetson nano에서 GPIO를 이용한 LED 제어실습 1-6: Jetson Nano 에서 GPIO 사용
sysfs GPIO 를 이용한 LED 제어 실습
n    Jetson Nano Interface 를 참고합니다. 이번 실습에 사용할 GPIO 는 32 번 Pin 을 사용하며, GND 는 6 번에 연결합니다.n    Jetson Nano pin 설명
40pin 양쪽에 pin 번호가 쓰여져 있습니다. pin 번호를 파악하고 다음 내용을 따라하세요. n    Jetson Nano 와 LED (+브레드보드)를 다음과 같이 연결합니다. (참고: LED 의 긴 쪽은 +이고, 짧은 쪽은 – 입니다.)n    gpio 설정을 하기위해선 Super User 모드로 들어가야 합니다.
$ sudo su
n    연결한 pin 의 sysfs gpio number 로 export 합니다.
$ echo 168 > /sys/class/gpio/export
n    연결한 pin direction 을 out 으로 변경합니다.
$ echo out > /sys/class/gpio/gpio168/direction
n    ‘echo 1’ 을 이용하여 LED 를 ON 합니다.
$ echo 1 > /sys/class/gpio/gpio168/value
n    ‘echo 0’ 을 이용하여 LED 를 OFF 합니다.
$ echo 0 > /sys/class/gpio/gpio168/value(참고: 브레드 보드와 점퍼선이 제대로 연결되지 않았을 경우 LED ON 과 LED OFF 가 잘 작동하지 않을 수 있습니다. 점퍼선을 정확히 연결해 주시기 바랍니다.)Jetson.GPIO 라이브러리를 사용해서 Python 으로 간단한 LED 제어 실습
n    Jetson.GPIO 라이브러리를 git 으로 clone 하고 폴더로 이동합니다. (참고 : ‘~’ 경로에서 실행합니다.)
$ git clone https://github.com/NVIDIA/jetson-gpio.git
$ cd jetson-gpio
n    GPIO 라이브러리의 주요함수는 다음과 같습니다.
함수명
사용 예
설명
GPIO.setmode(GPIO.BOARD)
Jetson 의 40 핀 헤더 번호 기준 사용
GPIO.setmode(GPIO.BCM)
GPIO.setmode()
Broadcom SoC 의 GPIO 번호 기준 사용
GPIO.setmode(GPIO.CVM)
CVM/CVB 커넥터에 해당하는 문자열 사용
GPIO.setmode(GPIO.TEGRA_SOC)
Tegra SoC 의 핀 이름 기반
설정
GPIO.setup()
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
GPIO 핀을 입력 또는 출력으로 설정하고, 출력 초기값도 지정 가능
GPIO.output()
GPIO.output(channel, state)
설정한 GPIO 핀의 출력값을 제어 (HIGH / LOW)
n    Github 에서 받은 예제(samples 폴더) 중 simple_out.py 파일에서 표시된 부분을 다음과 같이 수정합니다.
(경로: ~/jetson-gpio/samples/simple_out.py)
$ gedit simple_out.pyn    예제 소스를 실행합니다.
(경로 : ~/jetson-gpio/samples/simple_out.py)
$ sudo python3 simple_out.py n    ‘simple_out.py’ 코드에서 time.sleep(1) 을 time.sleep(5)로 수정한 상태로 실행하면 LED 출력이 어떻게 달라지는지 확인합니다.
$ sudo python3 simple_out.pyI2C
I2C
▪  Inter-Integrated Circuit(IIC)
▪  여러 장치 간의 통신을 위해 설계된 동기식 직렬 통신 버스
▪  저속의 기기들을 제어/통신하기 위한 방식
▪  SDA(Serial Data Line)과 SCL(Serial Clock Line). 2개의 Pin으로 구성
▪  Master/slave 방식
▪  다양한 센서(온도, 압력, 가속도 등)를 쉽게 연결 가능하며, 각 센서는 고유한 주소를 가지고 있어서 버스에서 충돌 없이 통신할 수 있음I2C
Master SDA SCL
Slave
SDA
SCL
I2C
5V
5V
SCL
SDA
Master
Slave 
Address
”01”
Slave 
Address
”02”
Slave 
Address
”12”
Slave 
Address
”34”
Slave 
Address
”127”I2C
<https://learn.sparkfun.com/tutorials/i2c>
▪   데이터 교환 전, I2C 모듈 사이의 SCL/SDA 라인은 모두 1 = High 상태를 유지
▪   통신이 시작되면 데이터 라인은 클럭 라인보다 먼저 0 = Low 신호로 바뀜 (falling-edge)
▪   통신이 종료되면 SCL  SDA 순서로 각각의 신호가 0에서 1로 바뀜 (rising-edge)
▪ Start/Stop 시점을 제외한 실제 데이터의 교환은 모두 SCL = 1(High) 을 유지하는 순간에 SDA 값을 기준으로 수행됨
Jetson nano I2C Device File 
▪ Linux 시스템에서는 모든 하드웨어 장치가 /dev 아래 파일처럼 존재
•   예) /dev/i2c-1  Jetson Nano의 I2C-1버스를 나타내는 특수 파일i2cdetect
▪  Linux 시스템에서 제공되는 i2c 유틸리티 패키지의 일부
▪ i2c 장치를 연결했을 때, i2c 버스를 검사하고 i2c 버스에 연결된 장치를 찾는데 사용하는 명령어
▪  사용자는 I2C 버스를 검색하여 연결된 모든 I2C 장치의 주소를 식별 가능
 아무것도 연결되지 않은 상태
40-pin Expansion 헤더
40-pin Expansion 헤더Jetson Nano Interface
LCD(LCD 1602 IIC I2C)LCD(LCD 1602 IIC I2C)
▪  16글자, 두 줄의 문자를 디스플레이 하도록 구성
▪  기본적으로 출력되는 문자는 키보드에서 입력이 가능한 영숫자들이며, 한글이나 한자는 기본으로 출력 불가능
▪  사용자는 I2C 버스를 검색하여 연결된 모든 I2C 장치의 주소를 식별 가능
 LCD 한 글자 출력 방식
Jetson Nano에서 I2C LCD 모듈 연결Jetson Nano에서 I2C 
LCD 주소 확인
I2c 버스 번호  0
LCD i2c장치의 주소
smbus library 
▪ Python에서 I2C 버스를 통해 SMBus 프로토콜을 사용하여 장치와 통신할 수 있도록 도와주는 라
이브러리
▪  I2C 버스에 연결된 장치와 데이터 교환을 쉽게 구현할 수 있는 함수 제공
bus = smbus.SMBus(0)                     i2c 버스 번호 (여기서는 0을 사용) addr = addr                       LCD i2c 장치 주소 (여기서는 0x27을 사용
) IMU(MPU6050-gy25)
Jetson Nano에 IMU 연결Jetson Nano에 IMU 연결
시 i2cdetect
I2c 버스 번호  0
IMU i2c장치의 주소
smbus library 
▪ Python에서 I2C 버스를 통해 SMBus 프로토콜을 사용하여 장치와 통신할 수 있도록 도와주는 라
이브러리
▪  I2C 버스에 연결된 장치와 데이터 교환을 쉽게 구현할 수 있는 함수 제공
bus = smbus.SMBus(0)                      i2c 버스 번호 (여기서는 0을 사용) Device_Address = 0x68                        IMU (mpu 6050) i2c 장치 주소실습 1-8
- Jetson Nano에서 i2c 통신 실습실습 1-8 : Jetson Nano 에서 I2C 통신 이용하기
I2C (Inter-Integrated Circuit) 통신 학습
I2c 장치를 연결했을 때, I2C 버스를 검사하고 I2C 버스에 연결된 장치를 찾는데 사용하는 명령어입니다. Linux 시스템에서 제공되는 I2C 유틸리티 패키지의 일부입니다. 이를 통해 사용자는 I2C 버스를 검색하여 연결된 모든 I2C 장치의 주소를 식별할 수 있습니다.
n    I2cdetect [옵션] <I2C 버스 번호>
•    옵션 -y : 경고 메세지를 생략하고 사용자 확인 없이 명령을 실행합니다.
•    옵션 -r : 반복적으로 읽기를 수행하여 장치를 탐지합니다.
n    i2cdetect 명령어를 실행하면 아래와 같은 테이블 형태의 출력을 볼 수 있습니다. 각 셀에는 ‘--‘또는 2 자리의 16 진수 주소가 표시됩니다. ‘--‘는 해당 주소에 장치가 없음을 의미하고, 주소 값은 해당 주소에 장치가 있음을 나타냅니다.
n    SMBus 는 Python 에서 I2C 통신을 쉽게 구현할 수 있도록 도와주는 라이브러리 입니다. SMBus(System Management Bus)는 I2C 버스의 하위 집합으로, I2C
프로토콜을 기반으로 하여 저속의 간단한 센서나 디바이스 통신에 자주 사용됩니다. 다음 명령어를 실행하여 I2C 실습에 필요한 파이썬 패키지를 설치합니다.
$ sudo apt-get install python3-smbusn    smbus 라이브러리 주요 함수 설명
함수명
설명
사용법
파라미터 설명
smbus.SMBus(0)
Jetson 의
I2C 버스(0 번)를 활성화하여
장치와의 통신 가능하게 함
smbus.SMBus(0)
-
read_byte_data()
특정 레지스터에서 1 바이트 데이터를
읽음
read_byte_data(i2c_addr, register)
- i2c_addr: I2C 장치 주소
- register: 읽을 레지스터 주소
write_byte_data()
특정 레지스터에 1 바이트 데이터를
씀
write_byte_data(i2c_addr, register, value)
- i2c_addr: I2C 장치 주소
- register: 쓸 레지스터
주소
- value: 1 바이트 값I2C 통신을 활용한 실습 - LCD
n 다음 이미지는 LCD(LCD 1602 IIC I2C) 입니다.
n    1602 LCD 는 16 글자, 두 줄의 문자를 디스플레이 하도록 구성되어 있습니다.
기본적으로 출력되는 문자는 키보드에서 입력이 가능한 영숫자들이며, 한글이나 한자는 기본으로 출력할 수 없습니다.
LCD 1 글자에는 아래 이미지와 같이 가로 5, 세로 8 의 작은 점들이 모여서 하나의 글자를 만들고 있습니다.n    글자의 색이 있는 부분은 1, 아무것도 없는 부분은 0 으로 표시합니다.
C 프로그램에서 B 는 Binary 데이터를 표시하는 첫 문자이고 그 뒤에 따라오는 글자는 1 과 0 의 조합으로 하나의 숫자 B11110 이 위의 글자 한 줄을 표현합니다. 위 이미지처럼 글자를 만들기 위해서는 다음과 같은 구조를 사용할 수 있습니다.
byte BChar [] = { B11110, 
B10001, B10001, B11110, B10001, B10001, B10001, B11110
};n    LCD (LCD 1602 IIC I2C)를 Jetson Nano 40pin 에 다음과 같이 연결해주세요.
n    다음 명령어를 실행하여 i2c 장치의 주소를 확인하세요. 여기서 연결한 I2C 버스 번호는 ‘0’ 입니다.
$ sudo i2cdetect -y -r 0n    LCD 예제 소스를 clone 하세요. (실습파일로도 제공됩니다.) (참고 : ~ 위치에서 실행합니다.)
$ git clone https://github.com/eleparts/RPi_I2C_LCD_driver.git
n    LCD 예제 소스 폴더로 이동합니다.
$ cd RPi_I2C_LCD_driver
n    드라이버 파일(RPi_I2C_driver.py) 에서 init 함수의 port 부분을 수정합니다. i2c 0 번에 연결했기 때문에 port=0 으로 수정해야합니다.
$ gedit RPi_I2C_driver.py
class i2c_device:
def __init__(self, addr, port=0):
self.addr = addr
self.bus = smbus.SMBus(port)
n    start.sh 을 실행하여 별도의 라이브러리 등록 과정 없이 예제코드를 실행할 수 있도록 드라이버 파일을 각 디렉토리에 복사해 줍니다.
$ sh start.sh
n    예제코드가 있는 디렉터리로 이동합니다.
$ cd example
n    HelloWorld.py 예제 코드를 확인합니다.
(실습코드 경로 : RPi_I2C_LCD_driver/example/HelloWorld.py)
'''
# RPi_I2C_driver - LiquidCrystal Library - Hello World
#
# This example has been implemented to enable Python in Raspberry Pi. # 
# This sketch prints "Hello World!" to the LCD
# and shows the time.
#
# This example code is in the public domain.
# http://www.arduino.cc/en/Tutorial/LiquidCrystalHelloWorld #
# The circuit:
# RaspberryPi       - 1602 I2C LCD # Vcc               - Vcc# GND               - GND
# GPIO02 (PIN3/SDA) - SDA
# GPIO03 (PIN5/SCL) - SCL
# 
# ※ I2C Enable is required in Raspberry Pi configuration.
# ※ When the voltage of the LCD / I2C board is 5V, use of 3.3V logic level converter is recommended. #
# Library originally added 18 Apr 2008
# by David A. Mellis
# library modified 5 Jul 2009
# by Limor Fried (http://www.ladyada.net)
# example added 9 Jul 2009
# by Tom Igoe
# modified 22 Nov 2010
# by Tom Igoe
# modified 7 Nov 2016
# by Arturo Guadalupi
# modified Python 20 June 2019
# by eleparts (yeon) (https://www.eleparts.co.kr/)
'''
# include the library 
import RPi_I2C_driver
from time import *
# RPi_I2C_driver.lcd( I2C address )
lcd = RPi_I2C_driver.lcd(0x27)
# Print a message to the LCD.
lcd.print("hello, world!")
time_sec = 0
while True:
# set the cursor to column 0, line 1
# (note: line 1 is the second row, since counting begins with 0): lcd.setCursor(0, 1)
# print the number of seconds:
lcd.print(time_sec) sleep(1)
# time_sec + 1time_sec += 1
n    실행할 예제코드에서 I2C address 부분이 (40 번째 줄) 아래와 같이 i2cdetect 로 확인한 i2c 장치의 주소로 되어있는지 확인합니다.
# RPi_I2C_driver.lcd(I2C address)
lcd = RPi_I2C_driver.lcd(0x27)
n    파일을 실행합니다.
$ sudo python3 HelloWorld.py
n    (참고 : 아래 사진과 같이 LCD 화면에 빛(전력)은 들어오는데 글자가 보이지 않거나 네모 표시가 뜰 경우 다음 내용을 따라해주세요)•    드라이버로 LCD 뒷면의 저항값을 조절합니다. 저항을 시계방향으로 돌리면 저항 값이 낮아지고(=밝기가 높아짐), 반시계 방향으로 돌리면 저항값이
높아집니다(=밝기가 낮아짐)
• LCD 에 전원이 연결된 채로 드라이버를 돌려 글자가 잘 보이도록 조정해주세요.
n    SerialDisplay.py 예제 코드를 확인합니다.
(실습코드 경로 : RPi_I2C_LCD_driver/example/SerialDisplay.py)
'''
# RPi_I2C_driver - LiquidCrystal Library - SerialDisplay 
#
# This example has been implemented to enable Python in Raspberry Pi. # 
# This sketch takes characters from the terminal 
# where Python is running and displays them on the LCD.
#
# This example code is in the public domain.
# http://www.arduino.cc/en/Tutorial/LiquidCrystalSerialDisplay #
# The circuit:
# RaspberryPi       - 1602 I2C LCD # Vcc               - Vcc
# GND               - GND # GPIO02 (PIN3/SDA) - SDA # GPIO03 (PIN5/SCL) - SCL
# # ※ I2C Enable is required in Raspberry Pi configuration.
# ※ When the voltage of the LCD / I2C board is 5V, use of 3.3V logic level converter is recommended. #
# Library originally added 18 Apr 2008
# by David A. Mellis
# library modified 5 Jul 2009
# by Limor Fried (http://www.ladyada.net)
# example added 9 Jul 2009
# by Tom Igoe
# modified 22 Nov 2010
# by Tom Igoe
# modified 7 Nov 2016
# by Arturo Guadalupi
# modified Python 21 June 2019
# by eleparts (yeon) (https://www.eleparts.co.kr/) '''
# include the library 
import RPi_I2C_driver
from time import *
# RPi_I2C_driver.lcd( I2C address )
lcd = RPi_I2C_driver.lcd(0x27)
while True:
# Enter data received
str = input()
# clear the screen
lcd.clear()
# display each character to the LCD
lcd.print(str)
n    실행할 예제코드에서 I2C address 부분이 (40 번째 줄) 아래와 같이 i2cdetect 로 확인한 i2c 장치의 주소로 되어있는지 확인합니다.
# RPi_I2C_driver.lcd(I2C address)
lcd = RPi_I2C_driver.lcd(0x27)
n    파일을 실행합니다. 실행한 다음에 실행한 터미널에서 영어나 숫자를 입력하고 엔터를 누르면 LCD 에 입력한 글자가 나타납니다.$ sudo python3 SerialDisplay.py
n    CustomCharactor_Test.py 예제코드를 확인합니다.
(실습코드 경로 : RPi_I2C_LCD_driver/example/CustomCharactor_Test.py)
(참고 : RPi_I2C_LCD_driver/example 하위에 해당 파일이 없을 경우 제공된 실습코드를 실행 경로로 복사하거나, 직접 코드를 작성합니다.)
'''
# RPi_I2C_driver - LiquidCrystal Library - Custom Characters
#
# This example has been implemented to enable Python in Raspberry Pi.
# 
# This sketch prints "I <heart> Ras Pi!!" and a little dancing man
# to the LCD.
#
# example code
# https://www.arduino.cc/en/Reference/LiquidCrystalCreateChar
#
# Based on Adafruit's example at
# https://github.com/adafruit/SPI_VFD/blob/master/examples/createChar/createChar.pde #
# The circuit:
# RaspberryPi       - 1602 I2C LCD # Vcc               - Vcc
# GND               - GND # GPIO02 (PIN3/SDA) - SDA # GPIO03 (PIN5/SCL) - SCL
## Modified to not use poterntiometer and analog input.
# 
# ※ I2C Enable is required in Raspberry Pi configuration.
# ※ When the voltage of the LCD / I2C board is 5V, use of 3.3V logic level converter is recommended. #
created 21 Mar 2011
by Tom Igoe
modified 11 Nov 2013
by Scott Fitzgerald
modified 7 Nov 2016
by Arturo Guadalupi
# modified Python 21 June 2019
# by eleparts (yeon) (https://www.eleparts.co.kr/) '''
# include the library 
import RPi_I2C_driver
from time import *
# make some custom characters:
heart = [
0b00000, 0b01010, 0b11111, 0b11111, 0b11111, 0b01110, 0b00100, 0b00000
]
smiley = [ 
0b00000, 0b00000, 0b01010, 0b00000, 0b00000, 0b10001, 0b01110, 0b00000
]
frownie = [ 0b00000,0b00000,
0b01010,
0b00000,
0b00000,
0b00000,
0b01110,
0b10001
]
armsDown = [
0b00100,
0b01010,
0b00100,
0b00100,
0b01110,
0b10101,
0b00100,
0b01010
]
armsUp = [
0b00100,
0b01010,
0b00100,
0b10101,
0b01110,
0b00100,
0b00100,
0b01010
]
# RPi_I2C_driver.lcd( I2C address ) lcd = RPi_I2C_driver.lcd(0x27)
# create a new character lcd.createChar(0, heart)
# create a new character lcd.createChar(1, smiley)
# create a new character lcd.createChar(2, frownie)
# create a new character lcd.createChar(3, armsDown) # create a new characterlcd.createChar(4, armsUp)
# set the cursor to the top left
lcd.setCursor(0, 0)
# Print a message to the lcd.
lcd.print("I ")
lcd.write(0) # when calling lcd.write() '0' must be cast as a byte lcd.print(" Jetson Nano!")
lcd.write(1)
while True:
lcd.setCursor(4, 1)
# draw the little man, arms down: lcd.write(3)
sleep(0.3)
lcd.setCursor(4, 1)
# draw him arms up: lcd.write(4)
sleep(0.3)
n    실행할 예제코드에서 I2C address 부분이 (97 번째 줄) 아래와 같이 i2cdetect 로 확인한 i2c 장치의 주소로 되어있는지 확인합니다.
# RPi_I2C_driver.lcd(I2C address) lcd = RPi_I2C_driver.lcd(0x27)
n    파일을 실행합니다.
$ sudo python3 CustomCharactor_Test.pyn     기본 예제 코드를 참조하여 현재 날짜와 현재 시간을 LCD 에 1 초마다 업데이트하여 표시하는 코드를 작성합니다. 날짜는 첫번째 라인에, 시간은 두번째 라인에 출력하며, 라인을 출력하는 함수는 ‘RPi_I2C_driver’에서 ‘lcd_display_string’ 함수를 사용합니다.
(실습코드 경로: RPi_I2C_LCD_driver/example/lcd_test.py)
(참고 : RPi_I2C_LCD_driver/example 하위에 해당 파일이 없을 경우 제공된 실습코드를 실행 경로로 복사하거나, 직접 코드를 작성합니다.)
'''
# RPi_I2C_driver - LiquidCrystal Library - display() and noDisplay()
#
# This example has been implemented to enable Python in Raspberry Pi. # 
# This sketch prints "Hello World!" to the LCD and uses the # display() and noDisplay() functions to turn on and off
# the display.
#
# This example code is in the public domain.
# http://www.arduino.cc/en/Tutorial/LiquidCrystalDisplay #
# The circuit:
# RaspberryPi       - 1602 I2C LCD # Vcc               - Vcc
# GND               - GND # GPIO02 (PIN3/SDA) - SDA # GPIO03 (PIN5/SCL) - SCL
# # ※ I2C Enable is required in Raspberry Pi configuration.
# ※ When the voltage of the LCD / I2C board is 5V, use of 3.3V logic level converter is recommended. #
# Library originally added 18 Apr 2008
# by David A. Mellis
# library modified 5 Jul 2009
# by Limor Fried (http://www.ladyada.net)
# example added 9 Jul 2009
# by Tom Igoe
# modified 22 Nov 2010
# by Tom Igoe
# modified 7 Nov 2016
# by Arturo Guadalupi
# modified Python 20 June 2019
# by eleparts (yeon) (https://www.eleparts.co.kr/)
'''
# include the library 
import RPi_I2C_driver
import time
from datetime import datetime
# RPi_I2C_driver.lcd( I2C address )
lcd = RPi_I2C_driver.lcd(0x27)
try:
while True:
now = datetime.now()
current_date = now.strftime("%Y-%m-%d") current_time = now.strftime("%H:%M:%S") lcd.lcd_clear()
lcd.lcd_display_string(current_date, 1) lcd.lcd_display_string(current_time, 2)      time.sleep(1)
except KeyboardInterrupt: lcd.lcd_clear()
n    파일을 실행합니다.
$ sudo python3 lcd_test.pyn    기본 예제 코드 ‘CustomCharactor_Test.py’를 참고하여 한글 Custom Character 를 만들어서 “감사”라는 한글 단어를 출력합니다.
(실습코드 경로: RPi_I2C_LCD_driver/example/CustomCharactor_Hangle_Test py)
(참고 : RPi_I2C_LCD_driver/example 하위에 해당 파일이 없을 경우 제공된 실습코드를 실행 경로로 복사하거나, 직접 코드를 작성합니다.)
'''
# RPi_I2C_driver - LiquidCrystal Library - Custom Characters
#
# This example has been implemented to enable Python in Raspberry Pi.
# 
# This sketch prints "I <heart> Ras Pi!!" and a little dancing man
# to the LCD.
#
# example code
# https://www.arduino.cc/en/Reference/LiquidCrystalCreateChar
#
# Based on Adafruit's example at
# https://github.com/adafruit/SPI_VFD/blob/master/examples/createChar/createChar.pde #
# The circuit:
# RaspberryPi       - 1602 I2C LCD # Vcc               - Vcc
# GND               - GND # GPIO02 (PIN3/SDA) - SDA# GPIO03 (PIN5/SCL) - SCL
#
# Modified to not use poterntiometer and analog input.
# 
# ※ I2C Enable is required in Raspberry Pi configuration.
# ※ When the voltage of the LCD / I2C board is 5V, use of 3.3V logic level converter is recommended. #
created 21 Mar 2011
by Tom Igoe
modified 11 Nov 2013
by Scott Fitzgerald
modified 7 Nov 2016
by Arturo Guadalupi
# modified Python 21 June 2019
# by eleparts (yeon) (https://www.eleparts.co.kr/) '''
import RPi_I2C_driver from time import *
Giyuk = [
0b11111, 0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b00001
]
Ah = [
0b00100, 0b00100, 0b00100, 0b00111, 0b00100, 0b00100, 0b00100, 0b00100
]
Mium = [0b11111,
0b10001,
0b10001,
0b10001,
0b10001,
0b10001,
0b10001,
0b11111
]
Siot = [
0b00100,
0b00100,
0b00100,
0b01010,
0b01010,
0b10001,
0b10001,
0b10001
]
# RPi_I2C_driver.lcd( I2C address ) lcd = RPi_I2C_driver.lcd(0x27)
# create a new character lcd.createChar(0, Giyuk)
# create a new character lcd.createChar(1, Ah)
# create a new character lcd.createChar(2, Mium)
# create a new character lcd.createChar(3, Siot)
# set the cursor to the top left lcd.setCursor(1, 0)
lcd.write(0)
lcd.setCursor(2, 0) lcd.write(1)
lcd.setCursor(2, 1) lcd.write(2)
lcd.setCursor(4, 0) lcd.write(3)
lcd.setCursor(5, 0)lcd.write(1)
n    파일을 실행합니다.
$ sudo python3 CustomCharactor_Hangle_Test py
n    같은 경로에 있는 다른 예제도 실행해봅니다.
IMU (MPU6050-gy25) 실습
MPU6050-GY25 모듈은 가속도와 자이로 데이터를 기반으로 물체의 움직임과 방향을 측정할 수 있는 IMU(Inertial Measurement Unit) 센서입니다.
이번 실습에서는 I2C 통신을 통해 MPU6050 의 가속도, 자이로, 온도 데이터를 읽고 출력하는 방법을 학습합니다.
n    다음 이미지는 IMU (mpu6050-gy25)입니다.n     IMU (mpu6050-gy25)를 Jetson Nano 40pin 에 다음과 같이 연결해주세요.n    다음 명령어를 실행하여 i2c 장치의 주소를 확인하세요. 여기서 연결한 I2C 버스 번호는 0 입니다.
$ i2cdetect -y -r 0
n    실습에 필요한 파이썬 패키지들을 먼저 설치합니다.
$ pip3 install PyOpenGL
$ sudo apt-get install libsdl2-dev
$ pip3 install pygame
n    python3 smbus 패키지를 사용해서 레지스터 값을 쓰고 읽어보세요. (실습코드 경로: mpu6050/smbus_test.py)
import smbus            #import SMBus module of I2C
#some MPU6050 Registers and their Address PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19 CONFIG       = 0x1A GYRO_CONFIG  = 0x1B INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
def read_raw_data(addr):#Accelero and Gyro value are 16-bit
high = bus.read_byte_data(Device_Address, addr)
low = bus.read_byte_data(Device_Address, addr+1)
#concatenate higher and lower value
value = ((high << 8) | low)
#to get signed value from mpu6050
if(value > 32768):
value = value - 65536
return value
bus = smbus.SMBus(0)    # or bus = smbus.SMBus(0) for older version boards Device_Address = 0x68    # MPU6050 device address
#write to sample rate register
bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
#Write to power management register
bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
#Write to Configuration register
bus.write_byte_data(Device_Address, CONFIG, 0)
#Write to Gyro configuration register
bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
#Write to interrupt enable register
bus.write_byte_data(Device_Address, INT_ENABLE, 1)
#Read Accelerometer raw value
acc_x = read_raw_data(ACCEL_XOUT_H) acc_y = read_raw_data(ACCEL_YOUT_H) acc_z = read_raw_data(ACCEL_ZOUT_H) print(acc_x, ",", acc_y, ",", acc_z,"\n")
#Read Gyroscope raw value
gyro_x = read_raw_data(GYRO_XOUT_H) gyro_y = read_raw_data(GYRO_YOUT_H) gyro_z = read_raw_data(GYRO_ZOUT_H) print(gyro_x, ",", gyro_y, ",", gyro_z,"\n")n    파일을 실행합니다.
$ sudo python3 smbus_test.py
(참고 : imu를 움직이면서 실행하면 값의 변화를 더 잘 볼 수 있습니다.)
n    smbus 패키지를 사용해서 mpu6050 의 회전 속도와 가속도를 실시간으로 모니터링 해보세요.
(실습코드 경로: mpu6050/mpu6050_simpletest1.py)
'''
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python http://www.electronicwings.com
'''
import smbus            #import SMBus module of I2C from time import sleep          #import
#some MPU6050 Registers and their Address PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19 CONFIG       = 0x1A GYRO_CONFIG  = 0x1B INT_ENABLE   = 0x38ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
def MPU_Init():
#write to sample rate register
bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
#Write to power management register
bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
#Write to Configuration register
bus.write_byte_data(Device_Address, CONFIG, 0)
#Write to Gyro configuration register
bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
#Write to interrupt enable register
bus.write_byte_data(Device_Address, INT_ENABLE, 1)
def read_raw_data(addr):
#Accelero and Gyro value are 16-bit
high = bus.read_byte_data(Device_Address, addr)
low = bus.read_byte_data(Device_Address, addr+1)
#concatenate higher and lower value
value = ((high << 8) | low)
#to get signed value from mpu6050
if(value > 32768):
value = value - 65536
return value
bus = smbus.SMBus(0)    # or bus = smbus.SMBus(0) for older version boards Device_Address = 0x68    # MPU6050 device address
MPU_Init()print (" Reading Data of Gyroscope and Accelerometer")
while True:
#Read Accelerometer raw value
acc_x = read_raw_data(ACCEL_XOUT_H)
acc_y = read_raw_data(ACCEL_YOUT_H)
acc_z = read_raw_data(ACCEL_ZOUT_H)
#Read Gyroscope raw value
gyro_x = read_raw_data(GYRO_XOUT_H)
gyro_y = read_raw_data(GYRO_YOUT_H)
gyro_z = read_raw_data(GYRO_ZOUT_H)
#Full scale range +/- 250 degree/C as per sensitivity scale factor
Ax = acc_x/16384.0
Ay = acc_y/16384.0
Az = acc_z/16384.0
Gx = gyro_x/131.0
Gy = gyro_y/131.0
Gz = gyro_z/131.0
print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)     
sleep(1)
n    파일을 실행합니다.
$ sudo python3 mpu6050_simpletest1.pyn    smbus 패키지를 사용해서 앞에서는 mpu6050 의 회전 속도와 가속도를 확인했다면, 이번에는 온도까지 모니터링 해보세요.
(실습코드 경로: mpu6050/mpu6050_simpletest2.py)
"""This program handles the communication over I2C
between a Jetson Nano and a MPU-6050 Gyroscope / Accelerometer combo. Made by: Dennis/TW
Released under the MIT License
Copyright 2019
"""
import smbus
from time import sleep      
class mpu6050:
# Global Variables
GRAVITIY_MS2 = 9.80665
address = None
bus = smbus.SMBus(0)
# Scale Modifiers
ACCEL_SCALE_MODIFIER_2G = 16384.0
ACCEL_SCALE_MODIFIER_4G = 8192.0
ACCEL_SCALE_MODIFIER_8G = 4096.0
ACCEL_SCALE_MODIFIER_16G = 2048.0
GYRO_SCALE_MODIFIER_250DEG = 131.0GYRO_SCALE_MODIFIER_500DEG = 65.5 GYRO_SCALE_MODIFIER_1000DEG = 32.8 GYRO_SCALE_MODIFIER_2000DEG = 16.4
# Pre-defined ranges
ACCEL_RANGE_2G = 0x00
ACCEL_RANGE_4G = 0x08
ACCEL_RANGE_8G = 0x10
ACCEL_RANGE_16G = 0x18
GYRO_RANGE_250DEG = 0x00
GYRO_RANGE_500DEG = 0x08
GYRO_RANGE_1000DEG = 0x10
GYRO_RANGE_2000DEG = 0x18
# MPU-6050 Registers
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C
SELF_TEST_X = 0x0D
SELF_TEST_Y = 0x0E
SELF_TEST_Z = 0x0F SELF_TEST_A = 0x10
ACCEL_XOUT0 = 0x3B
ACCEL_XOUT1 = 0x3C
ACCEL_YOUT0 = 0x3D
ACCEL_YOUT1 = 0x3E
ACCEL_ZOUT0 = 0x3F
ACCEL_ZOUT1 = 0x40
TEMP_OUT0 = 0x41
TEMP_OUT1 = 0x42
GYRO_XOUT0 = 0x43
GYRO_XOUT1 = 0x44
GYRO_YOUT0 = 0x45
GYRO_YOUT1 = 0x46
GYRO_ZOUT0 = 0x47
GYRO_ZOUT1 = 0x48
ACCEL_CONFIG = 0x1C GYRO_CONFIG = 0x1Bdef __init__(self, address):
self.address = address
# Wake up the MPU-6050 since it starts in sleep mode
self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)
# I2C communication methods
def read_i2c_word(self, register):
"""Read two i2c registers and combine them.
register -- the first register to read from.
Returns the combined read results.
"""
# Read the data from the registers
high = self.bus.read_byte_data(self.address, register)
low = self.bus.read_byte_data(self.address, register + 1)
value = (high << 8) + low
if (value >= 0x8000):
return -((65535 - value) + 1)
else:
return value
# MPU-6050 Methods
def get_temp(self):
"""Reads the temperature from the onboard temperature sensor of the MPU-6050. Returns the temperature in degrees Celcius.
"""
# Get the raw data
raw_temp = self.read_i2c_word(self.TEMP_OUT0)
# Get the actual temperature using the formule given in the
# MPU-6050 Register Map and Descriptions revision 4.2, page 30 actual_temp = (raw_temp / 340) + 36.53
# Return the temperature return actual_tempdef set_accel_range(self, accel_range):
"""Sets the range of the accelerometer to range.
accel_range -- the range to set the accelerometer to. Using a
pre-defined range is advised.
"""
# First change it to 0x00 to make sure we write the correct value later self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)
# Write the new range to the ACCEL_CONFIG register
self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)
def read_accel_range(self, raw = False):
"""Reads the range the accelerometer is set to.
If raw is True, it will return the raw value from the ACCEL_CONFIG register
If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it returns -1 something went wrong.
"""
# Get the raw value
raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)
if raw is True:
return raw_data
elif raw is False:
if raw_data == self.ACCEL_RANGE_2G:
return 2
elif raw_data == self.ACCEL_RANGE_4G:
return 4
elif raw_data == self.ACCEL_RANGE_8G:
return 8
elif raw_data == self.ACCEL_RANGE_16G:
return 16
else:
return -1
def get_accel_data(self, g = False):
"""Gets and returns the X, Y and Z values from the accelerometer.
If g is True, it will return the data in g
If g is False, it will return the data in m/s^2 Returns a dictionary with the measurement results."""
# Read the data from the MPU-6050
x = self.read_i2c_word(self.ACCEL_XOUT0)
y = self.read_i2c_word(self.ACCEL_YOUT0)
z = self.read_i2c_word(self.ACCEL_ZOUT0)
accel_scale_modifier = None
accel_range = self.read_accel_range(True)
if accel_range == self.ACCEL_RANGE_2G:
accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
elif accel_range == self.ACCEL_RANGE_4G:
accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
elif accel_range == self.ACCEL_RANGE_8G:
accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
elif accel_range == self.ACCEL_RANGE_16G:
accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
else:
print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G") accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
x = x / accel_scale_modifier
y = y / accel_scale_modifier
z = z / accel_scale_modifier
if g is True:
return {'x': x, 'y': y, 'z': z}
elif g is False:
x = x * self.GRAVITIY_MS2
y = y * self.GRAVITIY_MS2
z = z * self.GRAVITIY_MS2
return {'x': x, 'y': y, 'z': z}
def set_gyro_range(self, gyro_range):
"""Sets the range of the gyroscope to range.
gyro_range -- the range to set the gyroscope to. Using a pre-defined range is advised.
"""
# First change it to 0x00 to make sure we write the correct value later self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)
# Write the new range to the ACCEL_CONFIG registerself.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)
def read_gyro_range(self, raw = False):
"""Reads the range the gyroscope is set to.
If raw is True, it will return the raw value from the GYRO_CONFIG register.
If raw is False, it will return 250, 500, 1000, 2000 or -1. If the returned value is equal to -1 something went wrong.
"""
# Get the raw value
raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)
if raw is True:
return raw_data
elif raw is False:
if raw_data == self.GYRO_RANGE_250DEG:
return 250
elif raw_data == self.GYRO_RANGE_500DEG:
return 500
elif raw_data == self.GYRO_RANGE_1000DEG:
return 1000
elif raw_data == self.GYRO_RANGE_2000DEG:
return 2000
else:
return -1
def get_gyro_data(self):
"""Gets and returns the X, Y and Z values from the gyroscope. Returns the read values in a dictionary.
"""
# Read the raw data from the MPU-6050
x = self.read_i2c_word(self.GYRO_XOUT0)
y = self.read_i2c_word(self.GYRO_YOUT0)
z = self.read_i2c_word(self.GYRO_ZOUT0)
gyro_scale_modifier = None
gyro_range = self.read_gyro_range(True)
if gyro_range == self.GYRO_RANGE_250DEG:
gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG elif gyro_range == self.GYRO_RANGE_500DEG:gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
elif gyro_range == self.GYRO_RANGE_1000DEG:
gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
elif gyro_range == self.GYRO_RANGE_2000DEG:
gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
else:
print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG") gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
x = x / gyro_scale_modifier
y = y / gyro_scale_modifier
z = z / gyro_scale_modifier
return {'x': x, 'y': y, 'z': z}
def get_all_data(self):
"""Reads and returns all the available data."""
temp = get_temp()
accel = get_accel_data()
gyro = get_gyro_data()
return [accel, gyro, temp]
if __name__ == "__main__":
while(1):
mpu = mpu6050(0x68)
print("Temperature (C): ", mpu.get_temp()) accel_data = mpu.get_accel_data()
print("Acceleration x (m/s^2): ", accel_data['x']) print("Acceleration y (m/s^2): ", accel_data['y']) print("Acceleration z (m/s^2): ", accel_data['z']) gyro_data = mpu.get_gyro_data()
print("Gyroscope x (deg/s): ", gyro_data['x']) print("Gyroscope y (deg/s): ", gyro_data['y']) print("Gyroscope z (deg/s): ", gyro_data['z']) sleep(1)
n    파일을 실행합니다.
$ sudo python3 mpu6050_simpletest2.pyn    Pygame, OpenGL 패키지를 사용해서 imu 의 움직임을 시각화 합니다. (실습코드 경로: mpu6050/boxctrl_imu.py)
#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import smbus
import time
#some MPU6050 Registers and their Address PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19 CONFIG       = 0x1A GYRO_CONFIG  = 0x1B INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47bus = smbus.SMBus(0)    # or bus = smbus.SMBus(0) for older version boards Device_Address = 0x68    # MPU6050 device address
ax = ay = az = 0.0
yaw_mode = False
def MPU_Init():
#write to sample rate register
bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
#Write to power management register
bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
#Write to Configuration register
bus.write_byte_data(Device_Address, CONFIG, 0)
#Write to Gyro configuration register
bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
#Write to interrupt enable register
bus.write_byte_data(Device_Address, INT_ENABLE, 1)
def resize(width, height):
if height==0:
height=1
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, 1.0*width/height, 0.1, 100.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
def init():
glShadeModel(GL_SMOOTH)
glClearColor(0.0, 0.0, 0.0, 0.0)
glClearDepth(1.0)
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
# def drawText(position, textString):     
#    font = pygame.font.SysFont ("Courier", 18, True)
#    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     #    textData = pygame.image.tostring(textSurface, "RGBA", True)     
#    glRasterPos3d(*position)     
#    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
def draw():
global rquad
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); 
glLoadIdentity()
glTranslatef(0,0.0,-7.0)
osd_text = "pitch: " + str("{0:.2f}".format(ay)) + ", roll: " + str("{0:.2f}".format(ax))
if yaw_mode:
osd_line = osd_text + ", yaw: " + str("{0:.2f}".format(az))
else:
osd_line = osd_text
# drawText((-2,-2, 2), osd_line)
# the way I'm holding the IMU board, X and Y axis are switched # with respect to the OpenGL coordinate system
if yaw_mode:                             # experimental glRotatef(az, 0.0, 1.0, 0.0)  # Yaw,   rotate around y-axis
else:
glRotatef(0.0, 0.0, 1.0, 0.0)
glRotatef(ay ,1.0,0.0,0.0)        # Pitch, rotate around x-axis glRotatef(-1*ax ,0.0,0.0,1.0)     # Roll,  rotate around z-axis
glBegin(GL_QUADS)   glColor3f(0.0,1.0,0.0) glVertex3f( 1.0, 0.2,-1.0) glVertex3f(-1.0, 0.2,-1.0)      glVertex3f(-1.0, 0.2, 1.0)      glVertex3f( 1.0, 0.2, 1.0)      
glColor3f(1.0,0.5,0.0)  glVertex3f( 1.0,-0.2, 1.0) glVertex3f(-1.0,-0.2, 1.0)      glVertex3f(-1.0,-0.2,-1.0)      glVertex3f( 1.0,-0.2,-1.0)      glColor3f(1.0,0.0,0.0)      glVertex3f( 1.0, 0.2, 1.0)
glVertex3f(-1.0, 0.2, 1.0)      
glVertex3f(-1.0,-0.2, 1.0)      
glVertex3f( 1.0,-0.2, 1.0)      
glColor3f(1.0,1.0,0.0)  
glVertex3f( 1.0,-0.2,-1.0)
glVertex3f(-1.0,-0.2,-1.0)
glVertex3f(-1.0, 0.2,-1.0)      
glVertex3f( 1.0, 0.2,-1.0)      
glColor3f(0.0,0.0,1.0)  
glVertex3f(-1.0, 0.2, 1.0)
glVertex3f(-1.0, 0.2,-1.0)      
glVertex3f(-1.0,-0.2,-1.0)      
glVertex3f(-1.0,-0.2, 1.0)      
glColor3f(1.0,0.0,1.0)  
glVertex3f( 1.0, 0.2,-1.0)
glVertex3f( 1.0, 0.2, 1.0)
glVertex3f( 1.0,-0.2, 1.0)      
glVertex3f( 1.0,-0.2,-1.0)      
glEnd() 
def read_raw_data(addr):
#Accelero and Gyro value are 16-bit
high = bus.read_byte_data(Device_Address, addr) low = bus.read_byte_data(Device_Address, addr+1)
#concatenate higher and lower value
value = ((high << 8) | low) # ((high << 8) + low)와 같음
#to get signed value from mpu6050 if(value > 32768):
value = value - 65536 return value
def read_data():
global ax, ay, az
# Scale Modifiers
ACCEL_SCALE_MODIFIER_2G = 16384.0 ACCEL_SCALE_MODIFIER_4G = 8192.0ACCEL_SCALE_MODIFIER_8G = 4096.0
ACCEL_SCALE_MODIFIER_16G = 2048.0
acc_x = read_raw_data(ACCEL_XOUT_H)
acc_y = read_raw_data(ACCEL_XOUT_H+2)
acc_z = read_raw_data(ACCEL_XOUT_H+4)
# ACCEL_SCALE_MODIFIER_16G -> best
ax = acc_x / ACCEL_SCALE_MODIFIER_16G
ay = acc_y / ACCEL_SCALE_MODIFIER_16G
az = acc_z / ACCEL_SCALE_MODIFIER_16G
print ("\tAx=%.2f g" %ax, "\tAy=%.2f g" %ay, "\tAz=%.2f g" %az)     
def main():
global yaw_mode
MPU_Init()
# First change it to 0x00 to make sure we write the correct value later
bus.write_byte_data(Device_Address, GYRO_CONFIG, 0x00)
video_flags = OPENGL|DOUBLEBUF
pygame.init()
screen = pygame.display.set_mode((640,480), video_flags)
pygame.display.set_caption("Press Esc to quit, z toggles yaw mode")
resize(640,480)
init()
frames = 0
ticks = pygame.time.get_ticks()
while 1:
event = pygame.event.poll()
if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): pygame.quit()  #* quit pygame properly
break
if event.type == KEYDOWN and event.key == K_z: yaw_mode = not yaw_mode
read_data()
draw()
pygame.display.flip() frames = frames+1print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
if __name__ == '__main__': main()
n    파일을 실행합니다.
$ sudo python3 boxctrl_imu.py
(참고 : imu를 움직이는데 변화가 없거나 값이 0으로 나온다면, 연결 문제(접촉 불량)일 수 있습니다. 점퍼 선을 다시 연결하거나, 새로운 점퍼선으로 바꿔 주시기 바랍니다.)
(참고 : VSCode에서 원격으로 실행할 경우 GUI 관련 에러가 날 수 있기때문에, Jetson Nano에서 직접 실행합니다.)SPI
SPI
▪  Serial Peripheral Interface (SPI)
▪  고속 직렬 통신을 위해 설계된 동기식 통신 버스
▪  센서, 메모리, ADC/DAC 등 다양한 주변 장치를 연결할 때 사용
▪  Full-duplex 모드 지원 – 데이터 전송과 수신이 동시에 이루어짐
▪  Master/slave 방식
▪  하나의 마스터와 하나 이상의 슬레이브로 구성되며, 마스터는 클럭 신호를 생성하고, 슬레이브는 마스터의 클럭 신호에 동기화 됨SPI
SCLK
SCLK
Master
SPI                         MOSI                                  MOSI
MISO                                  MISO
SPI
Slave
SS
▪ SCLK : 마스터가 생성하는 클럭 신호
SS
▪  MOSI (Master out Slave in) : 마스터 출력, 슬레이브 입력 (마스터로부터의 출력)
▪  MISO (Master In Slave Out) : 마스터 입력, 슬레이브 출력 (슬레이브로부터의 출력)
▪ SS(CS) : 슬레이브 셀렉트(칩 셀렉트). 마스터가 특정 슬레이브를 선택하는 신호 (active low)
SPI 통신 - spidev
▪  Jetson에서 spi통신을 하기 위해서는 spidev라는 모듈 필요
•   spidev는 사용자 공간에서 SPI장치를 제어하기 위한 인터페이스를 제공하여 장치와 사용자 공간 통신을
가능하게 해주는 커널 모듈
▪  modprobe 명령어를 사용하여 spidev 모듈 로드 필요
▪  lsmod 명령어를 사용하여 현재 로드된 모든 커널 모듈 목록 확인 가능
▪  spidev 모듈을 로드한 후 SPI 장치가 ‘/dev/spidevX.Y 형식의 디바이스 파일로 존재
X는 SPI 버스 번호를 의미
Y는 각 슬레이브 디바이스(SS)를 의미
/dev/spidev0.0  /dev/spidev0.1  /dev/spidev1.0  /dev/spidev1.1SPI loopback test
▪  Jetson Nano의 SPI 0번 MOSI와 MISO를 점퍼선으로 연결하여 SPI Loopback test 
SPI loopback test
Loopback TEST 성공SPI 실습 물품
조도센서
저항
ADC MCP3008 
40-pin Expansion 헤더
40-pin Expansion 헤더Jetson Nano Interface
MCP3008
▪  MCP3008은 SPI 버스 프로토콜을 사용하는 아날로그 디지털 컨버터 (ADC) 
•  ADC : analog-to-digital converter
▪  조도센서 아날로그 데이터를 MCP3008 (SPI통신)를 통해 디지털 값으로 변경하여 가져와 출력
<wikipedia.org>MCP3008 Interface
방향 중요
MCP3008과 조도센서(CDS) 회로도Jetson Nano와 브레드 보드 연결 (조도센서)
SPI 0번 채널
Jetson Nano와 브레드 보드 연결 (조도센서 + LCD I2C) 
SPI 0번 채널Jetson Nano와 브레드 보드 실제 연결 (SPI 조도센서 실습) 
실습 1-10
- Jetson Nano에서 spi 통신 실습실습 1-10: Jetson Nano 에서 SPI 통신 이용하기
SPI(Serial Peripheral Interface) 통신 학습
Jetson 에서 spi 통신을 하기 위해선 spidev 라는 모듈을 로드해야 합니다. ‘spidev’란
사용자 공간에서 spi 장치를 제어하기 위한 인터페이스를 제공하여 장치와 사용자 공간 통신을 가능하게 해주는 커널 모듈입니다. 아래에 있는 modprobe 와 lsmod 설명을 읽고 두 명령어를 사용하여 spidev 모듈을 로드 시켜봅니다.
n    ‘modprobe’ 명령어에 대해 알아봅니다.
커널 모듈을 동적으로 로드하고 언로드하는데 사용되며, 종속성을 자동으로 처리하여 필요한 모든 관련 모듈을 함께 로드하거나 언로드합니다.
•    모듈 로드 : 특정 커널 모듈을 로드합니다.
$ sudo modprobe [모듈명]
•    모듈 언로드 : 특정 커널 모듈을 언로드합니다.
$ sudo modprobe -r [모듈명]
•    모듈이 존재하지 않을 경우 not found 오류 메세지가 표시됩니다.
n    lsmod 명령어에 대해 알아봅니다.
현재 로드된 모든 커널 모듈의 목록을 표시합니다. 이 명령어는 ‘proc’ 파일
시스템의 ‘/proc/modules’파일을 읽어 현재 로드 된 모듈에 대한 정보를 제공합니다.
•    모듈 목록 보기 : 현재 로드 된 모든 모듈의 목록을 표시합니다.
$ lsmod
Module                  Size  Used by
<모듈명>                  <크기> <사용 횟수> <의존성>
n     spidev 모듈을 ‘modprobe’ 명령어를 이용하여 로드합니다.
•    다음 명령어를 실행하여 spidev 모듈을 로드하세요.
(참고: 모듈을 로드하는 이 작업은 시스템을 부팅할 때마다 반복해야 합니다.)
$ sudo modprobe spidev•    다음 명령어를 실행하여 spidev 모듈이 잘 로드 됐는지 확인합니다.
$ lsmod
n    spi 장치 파일을 확인합니다.
spidev 모듈을 로드한 후 SPI 장치가 ‘/dev/spidevX.Y’ 형식의 디바이스 파일로 나타나는지 확인합니다.
$ ls /dev/spidev*
(참고 : spidev0.0 에서 0.0 이 의미하는 것은 다음과 같습니다. 첫번째 0 은 0 번 SPI 버스를 의미하며, 두번째 0 은 각 슬레이브 디바이스 (CS)를 나타냅니다.)
n    레지스터값을 확인합니다.
spi 에 해당하는 pin control 레지스터 값을 확인해주세요.
$ sudo cat /sys/kernel/debug/tegra_pinctrl_reg | grep -i spi
à Value 값이 위 내용과 같아야 spi 통신이 가능합니다.(참고: 이 레지스터들은 각 pin 마다 할당된 기능을 설정하고 제어하는 역할을 하며, 시스템에서 다양한 하드웨어 장치와의 인터페이스를 관리하거나,
입출력(I/O) 동작을 설정할 때 중요한 역할을 합니다.)
n    SPI Loopback test 을 수행합니다.
위 과정을 다 수행했다면 spi 통신 Loopback test 를 합니다. Jetson Nano 의 SPI 0 번 MOSI 와 MISO 를 점퍼선으로 연결하세요.
n    spidev-test git 을 clone 하세요
$ git clone https://github.com/rm-hull/spidev-test
n    spidev-test 폴더로 이동하세요.
$ cd spidev-test
n    spidev-test.c 코드를 컴파일하여 실행할 수 있는 파일로 만드세요.
$ gcc spidev_test.c -o spidev_test
n    spidev-test 파일을 실행해보세요. 현재 SPI0_MOSI, SPI0_MISO 를 연결했기 때문에 spidev0.0 또는 spidev0.1 로 loopback test 를 할 경우 잘 작동합니다.
$ sudo ./spidev_test -D /dev/spidev0.0 -v spi mode: 0x0
bits per word: 8
max speed: 500000 Hz (500 KHz)
TX | FF FF FF FF FF FF 40 00 00 00 00 95 FF FF FF FF FF FF FF FF FF FF FF FF FF
FF FF FF FF FF F0 0D  | ......@.... .................. .
RX | FF FF FF FF FF FF 40 00 00 00 00 95 FF FF FF FF FF FF FF FF FF FF FF FF FF
FF FF FF FF FF F0 0D  | ......@.... .................. .
$ sudo ./spidev_test -D /dev/spidev0.0 -v -p "HelloWorld123456789abcdef"
spi mode: 0x0
bits per word: 8
max speed: 500000 Hz (500 KHz)
TX | 48 65 6C 6C 6F 57 6F 72 6C 64 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 __ __ __ __ __ __ __  | HelloWorld123456789abcdef
RX | 48 65 6C 6C 6F 57 6F 72 6C 64 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 __ __ __ __ __ __ __  | HelloWorld123456789abcdef
SPI 통신을 활용한 실습 – 조도센서, ADC (MCP3008)
MCP3008 은 SPI 버스 프로토콜을 사용하는 아날로그 디지털 컨버터(ADC : analog-to- digital converter) 입니다.
조도센서 아날로그 데이터를 MCP3008 (SPI 통신)를 통해 디지털 값으로 변경하여 가져와 출력하는 내용을 실습합니다.
브레드보드와 Jetson Nano 를 다음과 같이 연결해주세요. 특히 MCP3008 의 경우 이미지와 같이 연결해야 합니다. (방향 중요)Jetson nano – MCP3080, 조도센서(CDS) 회로도
Jetson nano – 브레드보드(조도센서) 연결n    pip3 을 이용하여 spidev 라이브러리를 설치해주세요
$ pip3 install spidev
n    pip3 에 설치가 되었는지 확인합니다.
$ pip3 list | grep spidev
n    mcp3008.py 코드를 작성한 후 , 실행합니다.
import time
import spidev
spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1350000
def analog_read(channel):
r=spi.xfer2([1,(8+channel)<<4,0]) data=((r[1]&3)<<8)+r[2]
return data
while True :
reading = analog_read(0) readingstr = str(reading)
print('reading : ' , readingstr , 'Voltage:' , reading*3.3/1024 ) time.sleep(1)
(참고 : spi.open(0,0)의 첫번째 0 은 0 번 SPI 버스를 의미하며, 두번째 0 은 각 슬레이브 디바이스(CS)를 나타냅니다. 따라서 spi.open(0,0)으로 연결해야합니다. 또한
analog_read 에 쓰이는 channel 은 mcp3008 에 연결된 channel 번호인 ‘0’을 넣으면 됩니다. )
n    작성한 코드가 있는 경로로 가서 아래 명령어를 이용하여 위 코드를 실행해 보세요. (실습코드 경로: mcp3008/mcp3008.py)
$ sudo python3 mcp3008.py 
코드가 실행되는 동안 조도센서 위의 밝기를 변화시키면서 데이터가 어떻게 나오는지 확인해보세요.I2C + SPI 통신을 활용한 실습
조도센서,ADC 활용 (MCP3008) + LCD 활용 (LCD 1602 IIC I2C)
n    조도센서에서 변화 값에 따라 LCD 에 문자로 출력하는 실습을 합니다. Jetson Nano 에 조도센서, MCP3008, I2C LCD 를 아래와 같이 연결해주세요.
n    조도센서 데이터가 일정량 이상 출력되면 “light”, 손으로 조도센서를 가려서 일정량 이하로 출력되면 “dark” 문자열을 조도센서 데이터와 함께 출력하는 코드를 작성합니다. (실습코드 경로: mcp3008/mcp3008_output.py)
(참고 : LCD 코드를 사용하기 위해서는 RPi_I2C_driver.py 파일이 필요합니다. 이번에 작성할 코드 경로에 RPi_I2C_driver.py 파일을 복사하고 Import 해서 사용해주세요.)
import spidev import RPi_I2C_driver from time import *# RPi_I2C_driver.lcd( I2C address )
lcd = RPi_I2C_driver.lcd(0x27)
spi=spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz=1350000
time_sec = 0
def analog_read(channel):
r=spi.xfer2([1,(8+channel)<<4,0])
data=((r[1]&3)<<8)+r[2]
return data
while True :
reading = analog_read(0)
readingstr = str(reading)
print('reading : ' , readingstr , 'Voltage:' , reading*3.3/1024 ) lcd.clear()
if reading > 500:
lcd.print("light")
else:
lcd.print("dark")
# set the cursor to column 0, line 1
# (note: line 1 is the second row, since counting begins with 0): lcd.setCursor(0,1)
# Print a message to the LCD.
lcd.print(reading)
# print the number of seconds: sleep(0.5)
n    파일을 실행합니다.
$ sudo python3 mcp3008_output.py (참고 : 실습 환경에 따라 조도센서 데이터의 출력값은 밝고 어두운 조건에서 중간값이 달라질 수 있습니다. 제공된 코드에서는 기준값을 500 으로 설정하고 있으나, 실제 환경에서 측정된 중간값이 다를 경우 해당 값을 적절히 수정하여 사용해야 합니다.)OPENCV
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
▪  딥러닝 학습은 기존의 유명한 카페(caffe), 텐서플 로(tensorflow)등의 다른 딥러닝 프레임워크에서 진행하고, 학습된 모델을 불러와서 실행할 때에는 dnn 모듈을 사용하는 방식실습 1-12 
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