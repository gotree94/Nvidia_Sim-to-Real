# 실습 1-4: Linux Network / Jetpack Library 실습

---

## 1. 실습 개요

**실습 내용:**
1. 리눅스 네트워크 명령어 실습 (`ip`, `ifconfig`, `wget`, `curl` 등)
2. Jetson ←→ Host PC VSCode SSH 연결
3. Jetson 시스템 관련 명령어 실행 및 JetPack 설치

---

## 2. 네트워크 인터페이스 – ip, ifconfig

리눅스에서 네트워크 인터페이스를 구성하고 관리하기 위한 명령어.

### ip 명령어 실습

**모든 네트워크 인터페이스의 IP 주소 정보 표시**

```bash
$ ip addr show
```

![ip addr show](images/Image_002.jpg)

**모든 네트워크 인터페이스의 상태 표시**

```bash
$ ip link show
```

![ip link show](images/Image_003.jpg)

**네트워크 인터페이스 비활성화**

```bash
$ sudo ip link set eth0 down
```

![ip link set down](images/Image_004.jpg)

**네트워크 인터페이스 활성화**

```bash
$ sudo ip link set eth0 up
```

![ip link set up](images/Image_005.jpg)

**라우팅 테이블 표시**

```bash
$ ip route show
```

![ip route show](images/Image_006.png)

### ifconfig 명령어 실습

**모든 네트워크 인터페이스 정보 표시**

```bash
$ ifconfig
```

![ifconfig](images/Image_007.png)

**특정 네트워크 인터페이스 정보 표시**

```bash
$ ifconfig eth0
```

![ifconfig eth0](images/Image_008.jpg)

**인터페이스 비활성화 (ifconfig)**

```bash
$ sudo ifconfig eth0 down
```

![ifconfig down](images/Image_009.jpg)

**인터페이스 활성화 (ifconfig)**

```bash
$ sudo ifconfig eth0 up
```

![ifconfig up](images/Image_010.png)

---

## 3. 파일 다운로드 – wget, curl

웹에서 파일을 다운로드 하기 위한 명령어. 주로 HTTP, HTTPS, FTP 프로토콜을 지원하며, 다운로드할 파일의 URL을 입력하면 해당 파일을 로컬 컴퓨터에 다운로드한다.

### wget 실습

**wget 설치**

```bash
$ sudo apt install wget
```

**원본 파일명으로 다운로드**

```bash
$ wget https://blog.naver.com/allai-
```

![wget download](images/Image_011.jpg)

**파일 내용 확인**

```bash
$ cat allai-
```

![cat](images/Image_012.jpg)

**특정 이름으로 다운로드**

```bash
$ wget -O allai_blog.txt https://blog.naver.com/allai-
```

![wget -O](images/Image_013.jpg)

**다운로드 속도 제한**

```bash
$ wget --limit-rate=0.5k https://blog.naver.com/allai-
```

![wget limit-rate](images/Image_014.jpg)
![wget limit-rate result](images/Image_015.jpg)

### curl 실습

**curl 설치**

```bash
$ sudo apt install curl
```

**원본 파일명으로 다운로드**

```bash
$ curl -O https://blog.naver.com/allai-
```

![curl -O](images/Image_016.jpg)

**특정 이름으로 다운로드**

```bash
$ curl -o allai-blog.txt https://blog.naver.com/allai-
```

![curl -o](images/Image_017.jpg)

**출력 리다이렉션 다운로드**

```bash
$ curl https://blog.naver.com/allai- > allai_resource.txt
```

![curl redirect](images/Image_018.jpg)

**여러 파일 다운로드**

```bash
$ curl -O https://blog.naver.com/allai-/allai[0-5].txt
```

<img src="images/Image_019.jpg">
<img src="images/Image_020.jpg">

**다운로드 속도 제한 (curl)**

```bash
$ curl --limit-rate 500B -o allai_limit_rate.txt https://blog.naver.com/allai-
```

<img src="images/Image_021.png">

> **wget vs curl 속도 제한 차이점**: wget은 다운로드 속도를 더 엄격하게 제한하며, 네트워크 트래픽을 모니터링하고 일정한 시간 간격으로 데이터를 전송하는 방식으로 속도 제한을 구현한다. curl은 버퍼링 방식을 사용하여 더 유연한 속도 제어가 가능하다.

---

## 4. SSH를 사용한 원격 접속

**SSH 원격 시스템 실습**

   * ssh(secure Shell)는 네트워크 상에서 다른 컴퓨터에 접속하거나 명령을 실행하거나 파일을 전송하는데 사용되는 프로토콜입니다.
   * 보안이 취약한 네트워크에서 암호화된 통신을 제공하여, 데이터의 도청이나 변조를 방지하고 주로 원격 실행이나 파일 전송에 사용됩니다.

   * SSH 사용방법
      * Jetson Nano 의 ip 를 확인한 후 Window PC CMD 창 또는 Virtual Box + Ubuntu 터미널에서 ssh 명령어를 사용하여 Jetson Nano 에 접속합니다.
      * 접속 시 비밀번호를 입력해야 하며, 입력 중에는 화면에 표시되지 않지만 정상적인 동작이므로 그대로 입력해 주시면 됩니다.
```
사용법 : $ ssh [아이디]@[서버 주소]
예) ssh nvidia@172.30.1.5
```

<img src="images/Image_022.jpg">

**SCP 사용방법**

   * Jetson Nano 의 ip 를 확인한 후 다른 Window PC CMD 창 또는 Virtual Box (Ubuntu) 터미널에서 scp 를 이용하여 Jetson Nano 에 파일을 전송합니다.
   * 다른 서버로 전송
```
사용법 : $ scp [option] [보낼 파일] [아이디]@[서버 주소]:[저장할 경로]
예) scp text.txt nvidia@172.30.1.5:~
```

<img src="images/Image_023.jpg">

   * <Window 의 Jetson Nano 의 ‘~’ 경로로 전송 받은 test.txt 확인>

<img src="images/Image_024.jpg">

```bash
# Jetson Nano IP 확인 (Jetson 터미널에서)
$ ip addr show

# Host PC에서 SSH 접속
$ ssh jetson@192.168.x.x
```

---

## 5. 시스템 정보 확인

### CPU 정보 확인



### 시스템 리소스 확인



---

## 6. nvidia-jetpack 설치

```bash
$ sudo apt update
$ sudo apt install nvidia-jetpack
```

> **참고**: 설치에는 시간이 소요되며, 인터넷 연결 상태에 따라 수 분에서 수십 분까지 소요될 수 있다.











---

## 참고 자료

- [Linux ip 명령어 문서](https://man7.org/linux/man-pages/man8/ip.8.html)
- [VSCode Remote SSH](https://code.visualstudio.com/docs/remote/ssh)
- [NVIDIA JetPack SDK](https://developer.nvidia.com/embedded/jetpack)
- [GNU Wget Manual](https://www.gnu.org/software/wget/manual/)
- [curl Documentation](https://curl.se/docs/)
