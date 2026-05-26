# Day10 : Sim-to-Real with NVIDIA Isaac 

https://meet.google.com/rey-cayx-bve

## 1. Brev
   * 오늘 과정은 RTX Pro 6000 인스턴스를 사용하여 Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac을 진행합니다.
      * https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/index.html
   * Instance 실행 후, nvidia-ctk --version 명령어를 통해 설치여부를 확인합니다.
   * 또한

      ```
      sudo chmod 666 /var/run/docker.sock로 selkies 내부에서 도커를 사용하도록 합니다.
      sudo chmod -R 777 /home/shadeform
      ```
      
      ```
      nvidia-ctk --version
      ```

      ```
      shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ nvidia-ctk --version
      NVIDIA Container Toolkit CLI version 1.18.1
      commit: efe99418ef87500dbe059cadc9ab418b2815b9d5
      ```

## 2. Hands on 설명

   * Overview — Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac
      * https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/01-overview.html
   * Task: Centrifuge Vial Pick-and-Place


## 3. Centrifuge Vial Pick-and-Place

   * 원심분리 바이알: 실제 사람들이 만지기 꺼려하는 작업
   * SO-101: 간단한 과제로 설정하기 적절


## 4. Why Simulation Matters

   1. Time: 시간적 이점 확보
   2. Cost: 실제 로봇 시험보다 우수한 비용 효율성 확보
   3. Safety: 실제 로봇 작업 수행이 위험할 수 있음
   4. Diversity: 다양한 DR(Domain Randomization) 수행 가능

## 5. How it Works

Hands on에서는 Isaac GROOT-n1.6 VLA 모델을 사용하여 
- “pick up the vial and place it on the rack” 이라는 자연어 입력을 넣고 
-  joint feedback과 camera observation을 policy 입력으로 넣은 후 
> motor position을 결과로 받아, 동작을 수행 할 예정

## 6. What Is Sim-to-Real?
Sim-to-Real이란 Simulation 환경 내에서 policy를 학습하여 실제 하드웨어에 배포하는 것
> 시뮬레이션에서 학습하였지만, 실제에서도 잘 동작하는 것이 최종 목적

## 7. Sim-to-Real Gap
   * The Reality Gap in Robotics: Challenges, Solutions, and Best Practices
      * https://arxiv.org/pdf/2510.20808
   * Visualizing the Reality Gap — Getting Started With Isaac Lab
      * https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-lab/latest/transferring-robot-learning-policies-from-simulation-to-reality/02-the-reality-gap/01-visualizing-the-reality-gap.html

- Sensing Gaps
- Actuation Gaps
- Physics Gaps
- Modeling Gaps

## 8. 컨테이너 환경 설정

```
git clone https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop.git
cd Sim-to-Real-SO-101-Workshop
sudo apt-get update && sudo apt-get install -y git-lfs
# selkis의 경우 docker-io도 설치
git lfs install
git lfs pull
```

```
shadeform@brev-yq79qpxyp:~$ git clone https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop.git
Cloning into 'Sim-to-Real-SO-101-Workshop'...
remote: Enumerating objects: 126, done.
remote: Counting objects: 100% (126/126), done.
remote: Compressing objects: 100% (105/105), done.
remote: Total 126 (delta 22), reused 112 (delta 19), pack-reused 0 (from 0)
Receiving objects: 100% (126/126), 94.42 KiB | 2.55 MiB/s, done.
Resolving deltas: 100% (22/22), done.
shadeform@brev-yq79qpxyp:~$ cd Sim-to-Real-SO-101-Workshop
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ sudo apt-get update && sudo apt-get install -y docker.io git-lfs
Get:1 file:/var/cuda-repo-ubuntu2204-12-2-local  InRelease [1,572 B]
Get:1 file:/var/cuda-repo-ubuntu2204-12-2-local  InRelease [1,572 B]
Get:2 https://nvidia.github.io/libnvidia-container/stable/deb/amd64  InRelease [1,477 B]
Hit:3 https://apt.grafana.com stable InRelease                             
Hit:4 https://download.docker.com/linux/ubuntu jammy InRelease             
Hit:5 http://us.archive.ubuntu.com/ubuntu jammy InRelease                  
Get:6 https://repos.influxdata.com/debian stable InRelease [6,922 B]       
Hit:7 http://us.archive.ubuntu.com/ubuntu jammy-updates InRelease          
Hit:8 https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64  InRelease
Hit:9 https://pkgs.netbird.io/debian stable InRelease                      
Hit:10 http://us.archive.ubuntu.com/ubuntu jammy-backports InRelease       
Hit:11 http://security.ubuntu.com/ubuntu/ jammy-security InRelease  
Hit:12 https://packagecloud.io/ookla/speedtest-cli/ubuntu jammy InRelease
Fetched 8,399 B in 1s (16.6 kB/s)                                
Reading package lists... Done
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 containerd.io : Conflicts: containerd
E: Error, pkgProblemResolver::Resolve generated breaks, this may be caused by held packages.
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ git lfs install
git: 'lfs' is not a git command. See 'git --help'.

The most similar command is
        log
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ git lfs pull
git: 'lfs' is not a git command. See 'git --help'.

The most similar command is
        log
```

```
docker build -t teleop-docker -f docker/sim/Dockerfile .
```

```
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ docker build -t teleop-docker -f docker/sim/Dockerfile .
[+] Building 150.7s (24/24) FINISHED                         docker:default
 => [internal] load build definition from Dockerfile                   0.0s
 => => transferring dockerfile: 2.62kB                                 0.0s
 => [internal] load metadata for nvcr.io/nvidia/isaac-lab:2.3.2        1.0s
 => [internal] load .dockerignore                                      0.0s
 => => transferring context: 487B                                      0.0s
 => [ 1/19] FROM nvcr.io/nvidia/isaac-lab:2.3.2@sha256:388dbc806f48  108.8s
 => => resolve nvcr.io/nvidia/isaac-lab:2.3.2@sha256:388dbc806f48359a  0.0s
 => => sha256:cdd5dbb5f25fd8cd469d61390286ff54e1696 16.77kB / 16.77kB  0.0s
 => => sha256:f07c37e3f0c9f58f7febd0aa9a425523d282be6 6.36kB / 6.36kB  0.0s
 => => sha256:b08e2ff4391ef70ca747960a731d1f21a75fe 29.72MB / 29.72MB  0.4s
 => => sha256:88a179c20f7b61825ddcc5e15a6323a143bef4ee97f 131B / 131B  0.2s
 => => sha256:1da7123d9f2062daf2df982fa338a6c7c43f7 84.83MB / 84.83MB  0.8s
 => => sha256:388dbc806f48359a964cb9f807feb226da95d0a107f 743B / 743B  0.0s
 => => sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb557748 32B / 32B  0.3s
 => => sha256:02c044224ab8c0ca1fcf82cfcf986276182d6cc7f8a 289B / 289B  0.4s
 => => sha256:60a8ce43c0b5bad5a5157479192cc34e43e2a16173e 277B / 277B  0.5s
 => => sha256:94d1fac93cee3ac1275ea09c4ecc105b3555a3f474b 286B / 286B  0.5s
 => => extracting sha256:b08e2ff4391ef70ca747960a731d1f21a75febbd86ed  0.7s
 => => sha256:83e99b1b5b4dfee69fd1dfdda5e71b007108e2b0a65 483B / 483B  0.5s
 => => sha256:36b9c1c25bc12a0416f978e84e4bef2ade064f9 3.55kB / 3.55kB  0.6s
 => => sha256:b6c279fb3d9fd4af1fc4f542b17a45891b26fef02f9f1 99B / 99B  0.6s
 => => sha256:28be3cd701d4bb377cd628a92ecb67b1e2de13 7.50GB / 7.50GB  33.9s
 => => sha256:21db504e8800737646e2baf561051756701cce606e6 155B / 155B  0.8s
 => => sha256:76592f3487852e8723e1d642908cbdfb6488ceb 1.91kB / 1.91kB  0.8s
 => => sha256:ccdbb44ded143a3baa1deb821b52f06f7cdc07a1bc0 173B / 173B  0.8s
 => => sha256:f625311765b15365e2691f0ebabbe2fde45 141.31MB / 141.31MB  1.8s
 => => sha256:aa4d6036bd768f4f10ab6639c76ab852775b75e 2.54MB / 2.54MB  1.0s
 => => sha256:cc839ec8f78d7cbabaf75fe9c00816291f9b7057e82 161B / 161B  1.1s
 => => sha256:d06b839940c8d364eb4e4842225917c47d602e2 3.66MB / 3.66MB  1.3s
 => => extracting sha256:88a179c20f7b61825ddcc5e15a6323a143bef4ee97fd  0.0s
 => => extracting sha256:1da7123d9f2062daf2df982fa338a6c7c43f79e2e365  1.0s
 => => sha256:6fc8ed87312d82a08715f006425f3150daeda 31.30kB / 31.30kB  1.4s
 => => sha256:8a0fce89e732e0c2b04eb29b3328cfe550264ff610d 389B / 389B  1.5s
 => => sha256:32708e2591cb0adb85d1da544474c177897da79f53b 307B / 307B  1.5s
 => => sha256:d19b6b66ceea7b0b7f9ce287f69f0c425ad 642.70MB / 642.70MB  5.4s
 => => sha256:2e8bc716115c3999da57b46845bf25569cfd86a 3.16kB / 3.16kB  1.9s
 => => sha256:6ece29e71b323477c200a3d91dbae396b507825 1.69kB / 1.69kB  2.0s
 => => extracting sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb55774  0.0s
 => => extracting sha256:02c044224ab8c0ca1fcf82cfcf986276182d6cc7f8ad  0.0s
 => => extracting sha256:94d1fac93cee3ac1275ea09c4ecc105b3555a3f474bd  0.0s
 => => extracting sha256:60a8ce43c0b5bad5a5157479192cc34e43e2a16173e5  0.0s
 => => extracting sha256:83e99b1b5b4dfee69fd1dfdda5e71b007108e2b0a65c  0.0s
 => => extracting sha256:36b9c1c25bc12a0416f978e84e4bef2ade064f94112a  0.0s
 => => extracting sha256:b6c279fb3d9fd4af1fc4f542b17a45891b26fef02f9f  0.0s
 => => extracting sha256:28be3cd701d4bb377cd628a92ecb67b1e2de13bb0a5  55.2s
 => => extracting sha256:21db504e8800737646e2baf561051756701cce606e66  0.0s
 => => extracting sha256:ccdbb44ded143a3baa1deb821b52f06f7cdc07a1bc08  0.0s
 => => extracting sha256:76592f3487852e8723e1d642908cbdfb6488ceb145ca  0.0s
 => => extracting sha256:f625311765b15365e2691f0ebabbe2fde4502d33ee67  2.8s
 => => extracting sha256:aa4d6036bd768f4f10ab6639c76ab852775b75ebfd44  0.2s
 => => extracting sha256:cc839ec8f78d7cbabaf75fe9c00816291f9b7057e82d  0.0s
 => => extracting sha256:d06b839940c8d364eb4e4842225917c47d602e255f86  0.1s
 => => extracting sha256:6fc8ed87312d82a08715f006425f3150daeda2b5cf04  0.0s
 => => extracting sha256:8a0fce89e732e0c2b04eb29b3328cfe550264ff610d2  0.0s
 => => extracting sha256:32708e2591cb0adb85d1da544474c177897da79f53b9  0.0s
 => => extracting sha256:d19b6b66ceea7b0b7f9ce287f69f0c425ad06611b24  15.4s
 => => extracting sha256:2e8bc716115c3999da57b46845bf25569cfd86a391a4  0.0s
 => => extracting sha256:6ece29e71b323477c200a3d91dbae396b507825ed6bb  0.0s
 => [internal] load build context                                      0.0s
 => => transferring context: 1.47kB                                    0.0s
 => [ 2/19] WORKDIR /workspace                                         6.1s
 => [ 3/19] RUN git clone https://github.com/huggingface/lerobot.git   5.0s
 => [ 4/19] WORKDIR /workspace/lerobot                                 0.0s
 => [ 5/19] RUN git checkout e670ac5daf9b76                            0.3s
 => [ 6/19] RUN /workspace/isaaclab/_isaac_sim/python.sh -m pip insta  2.1s
 => [ 7/19] RUN printf '%s\n'     "packaging==23.0"     "numpy==1.26.  0.2s
 => [ 8/19] RUN /workspace/isaaclab/_isaac_sim/python.sh -m pip inst  12.7s
 => [ 9/19] RUN curl --proto "=https" --tlsv1.2 -sSf -L -o /tmp/ffmpe  3.3s
 => [10/19] RUN apt-get update && apt-get install -y --no-install-rec  3.5s
 => [11/19] RUN /workspace/isaaclab/_isaac_sim/python.sh -m pip insta  3.2s
 => [12/19] RUN /workspace/isaaclab/_isaac_sim/python.sh -m pip insta  1.1s
 => [13/19] WORKDIR /workspace/Sim-to-Real-SO-101-Workshop             0.0s
 => [14/19] COPY ./docker/sim/entrypoint.sh /workspace/Sim-to-Real-SO  0.0s
 => [15/19] COPY ./docker/utils.sh /workspace/Sim-to-Real-SO-101-Work  0.0s
 => [16/19] RUN chmod +x docker/sim/entrypoint.sh                      0.1s
 => [17/19] RUN /workspace/isaaclab/_isaac_sim/python.sh -m pip insta  1.5s
 => [18/19] RUN mkdir -p /tmp/pycache && chmod 1777 /tmp/pycache       0.1s
 => [19/19] RUN cat docker/utils.sh >> /root/.bashrc                   0.2s
 => exporting to image                                                 1.5s
 => => exporting layers                                                1.5s
 => => writing image sha256:3cd0a1860a998c1615200f76656fbc196e2050d71  0.0s
 => => naming to docker.io/library/teleop-docker                       0.0s
```

```
./docker/real/build.sh blackwell
```

```
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ ./docker/real/build.sh blackwell 
[+] Building 3716.2s (21/21) FINISHED                                                                                docker:default
 => [internal] load build definition from Dockerfile.blackwell                                                                 0.0s
 => => transferring dockerfile: 1.97kB                                                                                         0.0s
 => [internal] load metadata for docker.io/nvidia/cuda:13.0.0-devel-ubuntu24.04                                                0.6s
 => [internal] load .dockerignore                                                                                              0.0s
 => => transferring context: 487B                                                                                              0.0s
 => [internal] load build context                                                                                              0.0s
 => => transferring context: 63B                                                                                               0.0s
 => [ 1/16] FROM docker.io/nvidia/cuda:13.0.0-devel-ubuntu24.04@sha256:1e8ac7a54c184a1af8ef2167f28fa98281892a835c981ebcddb1f  30.1s
 => => resolve docker.io/nvidia/cuda:13.0.0-devel-ubuntu24.04@sha256:1e8ac7a54c184a1af8ef2167f28fa98281892a835c981ebcddb1fad0  0.0s
 => => sha256:1e8ac7a54c184a1af8ef2167f28fa98281892a835c981ebcddb1fad04bdd452d 743B / 743B                                     0.0s
 => => sha256:435220c0fef35cbf712e11999f8670a83835ef3cdd18564e5e8122f83078c88c 2.63kB / 2.63kB                                 0.0s
 => => sha256:0acb0bb33f9956b78fbfc026a81d9f3fbcf52f6c3c51ed7ff503b2f5db52d651 105.07MB / 105.07MB                             0.7s
 => => sha256:949aeb228afe6b802c1dbddad76439bc158a86f5900223ab13b3f60536b005a0 20.23kB / 20.23kB                               0.0s
 => => sha256:32f112e3802cadcab3543160f4d2aa607b3cc1c62140d57b4f5441384f40e927 29.72MB / 29.72MB                               0.5s
 => => sha256:9c9b39ad83d512d5af47e9c22f4458cb586f05ea478656a372c5e739cb7280e5 4.55MB / 4.55MB                                 0.2s
 => => sha256:13e8f87efde86df96bfe73da211eb196d0416702b69d92947ec617138e6db64b 6.88kB / 6.88kB                                 0.3s
 => => sha256:ddc61996788ff6833bbe82138d6fc5000e848953b90df5055cbae21479218914 186B / 186B                                     0.3s
 => => sha256:1ba07b1309cf3cbf6f4649e357d9a21e94039b6100973ef20599eb4a11a8b338 1.51GB / 1.51GB                                 7.7s
 => => sha256:84fef9f1ca4f21e9c7411db3c57fe91a1f401d7051d87a3bfed97ff70a2cf72c 59.61kB / 59.61kB                               0.6s
 => => extracting sha256:32f112e3802cadcab3543160f4d2aa607b3cc1c62140d57b4f5441384f40e927                                      0.7s
 => => sha256:492db7b3e492442f7a1ad30fea534f61ad89da451c675ccab2488e41034d0886 1.68kB / 1.68kB                                 0.7s
 => => sha256:932162d4fcf6e1094ee1544e8fde0ae2a02b2c4e9545f64f373ce3a4479189e6 1.52kB / 1.52kB                                 0.7s
 => => sha256:04c1659590951cf4645f7fc21adeeb72ce204df3349b1b68e615ed5911f543d6 2.31GB / 2.31GB                                12.3s
 => => sha256:5065c92eaa27f9fa100247b99dc946350ed4f7f2b4c5bf56da89df21462b7c4a 89.73kB / 89.73kB                               0.8s
 => => extracting sha256:9c9b39ad83d512d5af47e9c22f4458cb586f05ea478656a372c5e739cb7280e5                                      0.1s
 => => extracting sha256:0acb0bb33f9956b78fbfc026a81d9f3fbcf52f6c3c51ed7ff503b2f5db52d651                                      1.0s
 => => extracting sha256:ddc61996788ff6833bbe82138d6fc5000e848953b90df5055cbae21479218914                                      0.0s
 => => extracting sha256:13e8f87efde86df96bfe73da211eb196d0416702b69d92947ec617138e6db64b                                      0.0s
 => => extracting sha256:1ba07b1309cf3cbf6f4649e357d9a21e94039b6100973ef20599eb4a11a8b338                                      6.3s
 => => extracting sha256:84fef9f1ca4f21e9c7411db3c57fe91a1f401d7051d87a3bfed97ff70a2cf72c                                      0.0s
 => => extracting sha256:492db7b3e492442f7a1ad30fea534f61ad89da451c675ccab2488e41034d0886                                      0.0s
 => => extracting sha256:932162d4fcf6e1094ee1544e8fde0ae2a02b2c4e9545f64f373ce3a4479189e6                                      0.0s
 => => extracting sha256:04c1659590951cf4645f7fc21adeeb72ce204df3349b1b68e615ed5911f543d6                                     16.0s
 => => extracting sha256:5065c92eaa27f9fa100247b99dc946350ed4f7f2b4c5bf56da89df21462b7c4a                                      0.0s
 => [ 2/16] RUN apt-get update && apt-get install -y     software-properties-common     build-essential     cmake     git     27.8s
 => [ 3/16] RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1                                   0.1s 
 => [ 4/16] RUN python3.10 -m ensurepip --upgrade     && python3.10 -m pip install --upgrade pip setuptools wheel packaging n  3.6s 
 => [ 5/16] RUN apt-get remove -y python3-cryptography python3-cryptography-dev 2>/dev/null || true                            0.2s 
 => [ 6/16] RUN python3 -m pip install --ignore-installed cryptography                                                         1.0s 
 => [ 7/16] RUN git clone https://github.com/NVIDIA/Isaac-GR00T.git /Isaac-GR00T                                               2.0s 
 => [ 8/16] RUN cd /Isaac-GR00T &&     git checkout "ead52833afbbf4243f8cd5e7664f48a94de03b19" &&     git rev-parse --verif  148.8s 
 => [ 9/16] RUN cd /Isaac-GR00T/gr00t/eval/real_robot/SO100 &&     python3 -m pip install -e . --break-system-packages        20.0s 
 => [10/16] RUN python3 -m pip uninstall -y torch torchvision torchaudio && python3 -m pip install --pre torch torchvision t  44.7s 
 => [11/16] RUN export MAX_JOBS=2 && python3 -m pip install flash-attn --no-build-isolation --no-cache-dir                  3403.7s 
 => [12/16] RUN python3 -m pip install feetech-servo-sdk                                                                       1.9s 
 => [13/16] RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1                                     0.2s 
 => [14/16] COPY docker/utils.sh /root/tmp/utils.sh                                                                            0.0s 
 => [15/16] RUN cat /root/tmp/utils.sh >> /root/.bashrc && rm /root/tmp/utils.sh                                               0.2s 
 => [16/16] RUN apt-get update && apt-get install -y     libx11-6     libxcb1     libxkbcommon0     libxkbcommon-x11-0     li  7.4s 
 => exporting to image                                                                                                        23.9s 
 => => exporting layers                                                                                                       23.9s 
 => => writing image sha256:9a74a1353cf0dc695803aa4366542a5c3a55edad1b821baa37620f39331edbfe                                   0.0s 
 => => naming to docker.io/library/real-robot                                                                                  0.0s
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ 
```

```
터미널 창을 새로 열어
pip install -U "huggingface_hub[cli]"
```

```
shadeform@brev-yq79qpxyp:~$ pip install -U "huggingface_hub[cli]" 
Defaulting to user installation because normal site-packages is not writeable
Collecting huggingface_hub[cli]
  Downloading huggingface_hub-1.16.1-py3-none-any.whl (668 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 668.2/668.2 KB 16.0 MB/s eta 0:00:00
WARNING: huggingface-hub 1.16.1 does not provide the extra 'cli'
Collecting filelock>=3.10.0
  Downloading filelock-3.29.0-py3-none-any.whl (39 kB)
Collecting typing-extensions>=4.1.0
  Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 KB 23.6 MB/s eta 0:00:00
Collecting typer>=0.20.0
  Downloading typer-0.25.1-py3-none-any.whl (58 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 58.4/58.4 KB 27.3 MB/s eta 0:00:00
Requirement already satisfied: pyyaml>=5.1 in /usr/lib/python3/dist-packages (from huggingface_hub[cli]) (5.4.1)
Requirement already satisfied: packaging>=20.9 in /usr/lib/python3/dist-packages (from huggingface_hub[cli]) (21.3)
Collecting fsspec>=2023.5.0
  Downloading fsspec-2026.4.0-py3-none-any.whl (203 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 203.4/203.4 KB 23.5 MB/s eta 0:00:00
Collecting httpx<1,>=0.23.0
  Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 73.5/73.5 KB 28.0 MB/s eta 0:00:00
Collecting hf-xet<2.0.0,>=1.4.3
  Downloading hf_xet-1.5.0-cp37-abi3-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 36.6 MB/s eta 0:00:00
Collecting tqdm>=4.42.1
  Downloading tqdm-4.67.3-py3-none-any.whl (78 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.4/78.4 KB 41.5 MB/s eta 0:00:00
Collecting httpcore==1.*
  Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 78.8/78.8 KB 35.7 MB/s eta 0:00:00
Collecting anyio
  Downloading anyio-4.13.0-py3-none-any.whl (114 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 114.4/114.4 KB 49.4 MB/s eta 0:00:00
Requirement already satisfied: idna in /usr/lib/python3/dist-packages (from httpx<1,>=0.23.0->huggingface_hub[cli]) (3.3)
Requirement already satisfied: certifi in /usr/local/lib/python3.10/dist-packages (from httpx<1,>=0.23.0->huggingface_hub[cli]) (2026.5.20)
Collecting h11>=0.16
  Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Collecting click>=8.2.1
  Downloading click-8.4.1-py3-none-any.whl (116 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.6/116.6 KB 44.0 MB/s eta 0:00:00
Collecting annotated-doc>=0.0.2
  Downloading annotated_doc-0.0.4-py3-none-any.whl (5.3 kB)
Collecting rich>=13.8.0
  Downloading rich-15.0.0-py3-none-any.whl (310 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 310.7/310.7 KB 74.2 MB/s eta 0:00:00
Collecting shellingham>=1.3.0
  Downloading shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Collecting pygments<3.0.0,>=2.13.0
  Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 54.2 MB/s eta 0:00:00
Collecting markdown-it-py>=2.2.0
  Downloading markdown_it_py-4.2.0-py3-none-any.whl (91 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 91.7/91.7 KB 45.2 MB/s eta 0:00:00
Collecting exceptiongroup>=1.0.2
  Downloading exceptiongroup-1.3.1-py3-none-any.whl (16 kB)
Collecting mdurl~=0.1
  Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Installing collected packages: typing-extensions, tqdm, shellingham, pygments, mdurl, hf-xet, h11, fsspec, filelock, click, annotated-doc, markdown-it-py, httpcore, exceptiongroup, rich, anyio, typer, httpx, huggingface_hub
Successfully installed annotated-doc-0.0.4 anyio-4.13.0 click-8.4.1 exceptiongroup-1.3.1 filelock-3.29.0 fsspec-2026.4.0 h11-0.16.0 hf-xet-1.5.0 httpcore-1.0.9 httpx-0.28.1 huggingface_hub-1.16.1 markdown-it-py-4.2.0 mdurl-0.1.2 pygments-2.20.0 rich-15.0.0 shellingham-1.5.4 tqdm-4.67.3 typer-0.25.1 typing-extensions-4.15.0
shadeform@brev-yq79qpxyp:~$ 
```

```
hf auth login 
이후 read token 입력
token : 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
```

```
shadeform@brev-yq79qpxyp:~$ hf auth login 

    _|    _|  _|    _|    _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|_|_|_|    _|_|      _|_|_|  _|_|_|_|
    _|    _|  _|    _|  _|        _|          _|    _|_|    _|  _|            _|        _|    _|  _|        _|
    _|_|_|_|  _|    _|  _|  _|_|  _|  _|_|    _|    _|  _|  _|  _|  _|_|      _|_|_|    _|_|_|_|  _|        _|_|_|
    _|    _|  _|    _|  _|    _|  _|    _|    _|    _|    _|_|  _|    _|      _|        _|    _|  _|        _|
    _|    _|    _|_|      _|_|_|    _|_|_|  _|_|_|  _|      _|    _|_|_|      _|        _|    _|    _|_|_|  _|_|_|_|

    To log in, `huggingface_hub` requires a token generated from https://huggingface.co/settings/tokens .
Enter your token (input will not be visible): 
Add token as git credential? [y/N]: n
Token is valid (permission: read).
The token `ku_nvidia` has been saved to /home/shadeform/.cache/huggingface/stored_tokens
Your token has been saved to /home/shadeform/.cache/huggingface/token
Login successful.
The current active token is: `ku_nvidia`
shadeform@brev-yq79qpxyp:~$ 
```

```
#nvidia/GR00T-N1.6-3B · Hugging Face
https://huggingface.co/nvidia/GR00T-N1.6-3B
```

## 9. 모델 파일 다운로드

```
mkdir -p models
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real
hf download aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02 \
  --local-dir ./models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02
hf download aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70 \
  --local-dir ./models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
```

```
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ mkdir -p models
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real
hf download aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02 \
  --local-dir ./models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02
hf download aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70 \
  --local-dir ./models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
Fetching 51 files: 100%|████████████████████████████████████████████████████████████████████████████| 51/51 [01:16<00:00,  1.50s/it]
Download complete: 100%|███████████████████████████████████████████████████████████████████████| 55.4G/55.4G [01:16<00:00, 2.80GB/s]✓ Downloaded
  path: /home/shadeform/Sim-to-Real-SO-101-Workshop/models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left
Download complete: 100%|████████████████████████████████████████████████████████████████████████| 55.4G/55.4G [01:16<00:00, 723MB/s]
Fetching 51 files: 100%|████████████████████████████████████████████████████████████████████████████| 51/51 [01:15<00:00,  1.48s/it]
Download complete: 100%|███████████████████████████████████████████████████████████████████████| 55.4G/55.4G [01:15<00:00, 3.51GB/s]✓ Downloaded
  path: /home/shadeform/Sim-to-Real-SO-101-Workshop/models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real
Download complete: 100%|████████████████████████████████████████████████████████████████████████| 55.4G/55.4G [01:15<00:00, 733MB/s]
Fetching 51 files: 100%|████████████████████████████████████████████████████████████████████████████| 51/51 [01:16<00:00,  1.51s/it]
Download complete: 100%|███████████████████████████████████████████████████████████████████████| 55.4G/55.4G [01:16<00:00, 3.20GB/s]✓ Downloaded
  path: /home/shadeform/Sim-to-Real-SO-101-Workshop/models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02
Download complete: 100%|████████████████████████████████████████████████████████████████████████| 55.4G/55.4G [01:16<00:00, 720MB/s]
Fetching 19 files: 100%|████████████████████████████████████████████████████████████████████████████| 19/19 [00:41<00:00,  2.18s/it]
Download complete: 100%|███████████████████████████████████████████████████████████████████████| 22.8G/22.8G [00:41<00:00, 1.69GB/s]✓ Downloaded
  path: /home/shadeform/Sim-to-Real-SO-101-Workshop/models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
Download complete: 100%|████████████████████████████████████████████████████████████████████████| 22.8G/22.8G [00:41<00:00, 549MB/s]
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ 
```

## 10. Terminal 1

```
xhost + 
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

```
shadeform@brev-yq79qpxyp:~/Sim-to-Real-SO-101-Workshop$ xhost + 
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

Command 'xhost' not found, but can be installed with:
sudo apt install x11-xserver-utils

==========
== CUDA ==
==========

CUDA Version 13.0.0

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

root@brev-yq79qpxyp:/# 
```

## 11. Terminal 1(Selkies)

```
xhost + 
sudo docker run -it --rm --name real-robot --network host --privileged \
    --device nvidia.com/gpu=all \
    -e DISPLAY \
    -v /dev:/dev \
    -v /run/udev:/run/udev:ro \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
    -v /home/shadeform/Sim-to-Real-SO-101-Workshop/models:/workspace/models \
    -v $PWD/docker/env:/root/env \
    -v $PWD/docker/real/scripts:/Isaac-GR00T/gr00t/eval/real_robot/SO100 \
    real-robot \
    /bin/bash
```

## 12.Terminal 1

```
export 
MODEL=aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left/checkpoint-10000

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
```

## 13. Terminal 2

```
xhost + 
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

## 14. Terminal 2(Selkies)

```
xhost + 
sudo docker run --name teleop -it --privileged --device nvidia.com/gpu=all -e "ACCEPT_EULA=Y" --rm --network=host \
   -e "PRIVACY_CONSENT=Y" \
   -e DISPLAY \
   -v /dev:/dev \
   -v /run/udev:/run/udev:ro \
   -v $HOME/.Xauthority:/root/.Xauthority \
   -v /tmp/.X11-unix:/tmp/.X11-unix \
   -v /home/shadeform/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
   -v /home/shadeform/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
   -v /home/shadeform/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
   -v /home/shadeform/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
   -v /home/shadeform/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
   -v /home/shadeform/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
   -v /home/shadeform/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
   -v /home/shadeform/docker/isaac-sim/documents:/root/Documents:rw \
   -v /home/shadeform/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
   -v /home/shadeform/Sim-to-Real-SO-101-Workshop/docker/env:/root/env \
   -v /home/shadeform/Sim-to-Real-SO-101-Workshop:/workspace/Sim-to-Real-SO-101-Workshop \
   teleop-docker:latest
```

## 15. Terminal 2

```
lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --headless \
    --rerun
```

## 16. Terminal 2(Selkies)

```
apt-get update && apt-get install -y xvfb
xvfb-run -a lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --headless \
    --rerun
```

---

```
Using Brev CLI (SSH)
Install the CLI
Run this in your Windows (WSL) terminal
```

```
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"
```

```
dministrator@DESKTOP-C2MQEL4:/mnt/c/Users/Administrator$ sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"
Successfully installed brev CLI to /root/.local/bin/brev

Warning: /root/.local/bin is not in your PATH.
Add it by appending the following line to your shell profile (e.g. ~/.bashrc, ~/.zshrc):
    export PATH="${HOME}/.local/bin:${PATH}"
Then restart your shell or run 'source' on the profile to pick up the change.
```

```
Ubuntu 터미널에서:
echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc
source ~/.bashrc

적용 확인:
brev --version
```

```
dministrator@DESKTOP-C2MQEL4:/mnt/c/Users/Administrator$ echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> ~/.bashrc
dministrator@DESKTOP-C2MQEL4:/mnt/c/Users/Administrator$ source ~/.bashrc
dministrator@DESKTOP-C2MQEL4:/mnt/c/Users/Administrator$ brev --version
Command 'brev' not found, did you mean:
  command 'rev' from deb util-linux (2.37.2-4ubuntu3.4)
Try: sudo apt install <deb name>
```

```
sudo로 설치해서 바이너리가 /root/.local/bin/brev에 있고, 일반 사용자의 PATH에는 없습니다.

가장 간단한 해결 방법 (택1):

방법 1 — /usr/local/bin으로 복사 (추천)

sudo cp /root/.local/bin/brev /usr/local/bin/brev
brev --version
방법 2 — 재설치 (sudo 없이)

bash -c "$(curl -fsSL https://raw.githubusercontent.com/brevdev/brev-cli/main/bin/install-latest.sh)"
export PATH="${HOME}/.local/bin:${PATH}"
source ~/.bashrc
brev --version
```

   * Make sure you have WSL 2 installed and configured, virtualization enabled in your BIOS, and Ubuntu installed from the Microsoft Store.

```
Login to your account
Run this in your terminal
```

```
brev login
```

```
Open a terminal locally
Run this in your terminal
```

```
brev shell ku-7ea052
```

```
Open in Code Editor
Run this in your terminal
```

```
brev open ku-7ea052 cursor
```

```
Port Forward
Configure port forwarding
8080 -> 9876
Run this in your terminal
```

```
brev port-forward ku-7ea052 -p 8080:9876
```




