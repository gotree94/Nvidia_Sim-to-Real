# Synthetic Data Generation

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

## Data Generation with MobilityGen
   * Occupancy Map 이란?
     * Data Generation With MobilityGen : https://docs.isaacsim.omniverse.nvidia.com/5.1.0/synthetic_data_generation/tutorial_replicator_mobility_gen.html
   * 0과 1 사이의 값으로 나타낸 맵으로 0은 free space, 1은 occupied space를 나타낸다

 * Replay 하기전에 변경할것
 * sudo chmod -R 777 /home/shadeform

<img src="img/001.png">

## Data Generation with MobilityGen
   * 가이드에 따라 데이터를 생성
   * 시뮬레이션 환경에서는 Ground Truth기반으로 Occupancy map을 미리 만들게된다

<img src="img/002-1.png">

<img src="img/002-2.jpg">

## Cosmos-transfer
   * Cosmos-transfer1 build.nvidia.com : https://build.nvidia.com/nvidia/cosmos-transfer1-7b
   * Cosmos-transfer1 소개영상 : https://www.youtube.com/watch?v=0Yr5SdrVnxc
   * Cosmos-transfer2.5 소개영상 : https://www.youtube.com/watch?v=ttyb_9rX0fk
   * Physical AI NVIDIA Page : https://research.nvidia.com/publication/2025-09_world-simulation-video-foundation-models-physical-ai
   * NVIDIA Cosmos - 월드 파운데이션 모델로 구현하는 피지컬 AI : https://www.nvidia.com/ko-kr/ai/cosmos/#nv-accordion-6744152f25-item-31e94fa711

## Cosmos-transfer2.5
   * 먼저 Huggingface에 가입합니다 : https://huggingface.co/join
   * 가입 후, 계정 > Settings > Create new Access Token > Read Token 생성

<img src="img/003.png">

## Cosmos-transfer2.5
   * nvidia/Cosmos-Predict2.5-2B · Hugging Face : https://huggingface.co/nvidia/Cosmos-Predict2.5-2B
   * nvidia/Cosmos-Transfer2.5-2B · Hugging Face : https://huggingface.co/nvidia/Cosmos-Transfer2.5-2B
   * nvidia/Cosmos-Guardrail1 · Hugging Face : https://huggingface.co/nvidia/Cosmos-Guardrail1
   * 다음 링크에 들어가서 Model 사용 허가 신청

<img src="img/004-1.png">
<img src="img/004-2.png">

## Cosmos-transfer2.5
   * 아래 Launchable instance 실행 후, cuda12.8 설치 링크 참고하여 설치
   * 설치 후 다음 명령어를 이용하여 확인 
   * 출력이 다음과 같지 않다면, 시도 
```
echo 'export PATH=/usr/local/cuda-12.8/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```
<img src="img/005.png">


## Cosmos-transfer2.5
   * 이후 transfer2.5 setup 과정 실행 : https://github.com/nvidia-cosmos/cosmos-transfer2.5/blob/main/docs/setup.md
     * Balckwell에서는 버전이 바뀌어서 링크 참고 : https://github.com/nvidia-cosmos/cosmos-transfer2.5/blob/main/docs/setup.md
   * 주의! H100은 Graphics Engine이 없습니다(원격 GUI 사용 불가)

<img src="img/006.png">

**테스트 하면서 확인중**

```
ubuntu@fb087a37cf33:~/Desktop/Projects$ nvidia-smi
Fri May 22 05:36:54 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.126.09             Driver Version: 580.126.09     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA RTX PRO 6000 Blac...    On  |   00000000:01:00.0 Off |                    0 |
| N/A   30C    P0             81W /  600W |    1355MiB /  97887MiB |     29%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A             616      G   /usr/lib/xorg/Xorg                      133MiB |
|    0   N/A  N/A             659      C   /usr/bin/python3                        626MiB |
|    0   N/A  N/A             774      G   /usr/bin/kwin_x11                         9MiB |
|    0   N/A  N/A             840      G   /usr/bin/plasmashell                     69MiB |
|    0   N/A  N/A            7647      G   /usr/lib/firefox/firefox                421MiB |
+-----------------------------------------------------------------------------------------+

```

# Cosmos-Transfer2.5 설치 기록

> 환경: brevlab — NVIDIA RTX PRO 6000 Blackwell (96 GB) / 16 CPUs / 192 GiB RAM / Ubuntu 22.04

---

## 1. GPU 및 드라이버 확인

```bash
nvidia-smi
```

| 항목 | 값 |
|---|---|
| GPU | NVIDIA RTX PRO 6000 Blackwell |
| VRAM | 97,887 MiB (~96 GB) |
| Driver | 580.126.09 |
| CUDA Version | 13.0 |

---

## 2. CUDA Toolkit PATH 설정

```bash
nano ~/.bashrc
```

맨 밑 줄에 추가:

```bash
export PATH=/usr/local/cuda-13.0/bin:$PATH
```

```bash
source ~/.bashrc
```

> 첫 확인 시 nvcc는 CUDA 11.5 (apt nvidia-cuda-toolkit)였으나, 이후 13.0으로 재설치됨.

---

## 3. git-lfs 설치

```bash
sudo apt update && sudo apt install -y git-lfs
git lfs install
```

---

## 4. Repository clone

SSH 키가 없어 HTTPS 사용.

```bash
git clone https://github.com/nvidia-cosmos/cosmos-transfer2.5.git
cd cosmos-transfer2.5
git lfs pull
```

---

## 5. 시스템 패키지 설치

```bash
sudo apt install -y curl ffmpeg libx11-dev tree wget
```

---

## 6. uv 설치

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

---

## 7. Python 3.10 + 의존성 설치 (CUDA 13.0)

```bash
uv python install 3.10
uv sync --python 3.10 --extra cu130
source .venv/bin/activate
```

설치 후 프롬프트에 `(cosmos-transfer2)` 확인.

---

## 8. CUDA Toolkit 13.0 재설치

apt `nvidia-cuda-toolkit`으로 설치된 CUDA 11.5를 제거하고 13.0으로 재설치.

```bash
# 기존 CUDA 11.5 제거
sudo apt remove -y nvidia-cuda-toolkit

# CUDA 13.0 repository 등록
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update

# CUDA Toolkit 13.0 설치
sudo apt-get -y install cuda-toolkit-13-0
```

확인:

```bash
nvcc --version
```

| 항목 | 값 |
|---|---|
| nvcc | NVIDIA (R) Cuda compiler driver (2025) |
| Release | 13.0, V13.0.88 |
| 빌드 | cuda_13.0.r13.0/compiler.36424714_0 |

---

## 9. Hugging Face 로그인

```bash
# huggingface_hub CLI 설치
uv tool install -U "huggingface_hub[cli]"

# 로그인
hf auth login
```

- Read 권한이 있는 HF Token 입력
- [NVIDIA Open Model License](https://huggingface.co/nvidia/Cosmos-Transfer2.5-2B) 동의 필요

---

## 10. Inference 테스트 실행 (선택)

```bash
# 예제 1: depth control
python examples/inference.py \
    -i assets/robot_example/depth/robot_depth_spec.json \
    -o outputs/depth

# 예제 2: distilled edge
python examples/inference.py \
    -i assets/robot_example/distilled/edge/robot_edge_spec.json \
    -o outputs/distilled/edge \
    --model=edge/distilled
```

---

## 최종 설치 완료 항목

| # | 단계 | 상태 |
|---|---|---|
| 1 | GPU 환경 확인 (RTX PRO 6000, 96 GB) | ✅ |
| 2 | NVIDIA Driver 580.126.09 (CUDA 13.0) | ✅ |
| 3 | CUDA Toolkit 13.0 (nvcc V13.0.88) | ✅ |
| 4 | ~/.bashrc PATH 설정 (/usr/local/cuda-13.0/bin) | ✅ |
| 5 | git-lfs 설치 | ✅ |
| 6 | Repository clone + lfs pull | ✅ |
| 7 | 시스템 패키지 설치 | ✅ |
| 8 | uv 설치 | ✅ |
| 9 | Python 3.10 + 의존성 (cu130) | ✅ |
| 10 | 가상환경 활성화 (cosmos-transfer2) | ✅ |
| 11 | Hugging Face 로그인 | ✅ |
| 12 | Inference 테스트 실행 | ✅ |


```
ubuntu@fb087a37cf33:~/Desktop/Projects/cosmos-transfer2.5/assets$ ls *example
car_example:
car_input.mp4  car_prompt.txt  depth  edge  multicontrol  seg  vis

humanoid_example:
depth  edge  humanoid_guided_mask.mp4  humanoid_input.mp4  humanoid_prompt.txt  seg  vis

image_example:
calm_street.mp4  coastal_highway_guided_mask.mp4  coastal_highway.mp4  image2image_guided.json  image2image.json  image_style.json  sunset.jpg

multiview_example:
input_videos  multiview_autoregressive_spec.json  multiview_spec.json  prompt.txt  world_scenario_videos

plenoptic_example:
batch.jsonl  cameras  metadata.csv  rot_left.json  sample.json  sample_output  videos

robot_example:
depth  distilled  edge  multicontrol  robot_input.mp4  robot_prompt.txt  seg  vis
```

```
python examples/inference.py -i assets/car_example/depth/car_depth_spec.json -o outputs/depth
```

---
**참고사항**

# brevlab RTX Pro 6000 — Setup Checklist

## 인스턴스 접속 후 첫 확인

```bash
# 1. NVIDIA 드라이버 확인
nvidia-smi
# → Driver Version >= 570.124.06

# 2. GPU 확인
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
# → "NVIDIA RTX PRO 6000", 96 GB

# 3. OS 확인
cat /etc/os-release
# → Ubuntu 22.04+

# 4. CUDA 버전 확인
nvcc --version || python3 -c "import torch; print(torch.version.cuda)"
# → 12.8 이상 (uv sync가 PyTorch wheel로 설치하므로 host toolkit 없어도 무방)

# 5. Docker 확인 (선택)
docker --version && nvidia-ctk --version
```

## 설치 절차

### 1. git-lfs 설치

```bash
sudo apt install git-lfs
git lfs install
```

### 2. Repository clone

```bash
git clone git@github.com:nvidia-cosmos/cosmos-transfer2.5.git
cd cosmos-transfer2.5
git lfs pull
```

### 3. 시스템 패키지 설치

```bash
sudo apt update && sudo apt -y install curl ffmpeg libx11-dev tree wget
```

### 4. uv 설치

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 5. Python + 의존성 설치

```bash
uv python install           # Python 3.13
uv sync --extra=cu128       # CUDA 12.8 + PyTorch 2.7
source .venv/bin/activate
```

## HF Token 설정 (필수)

Cosmos 체크포인트는 gated model이므로 NVIDIA Open Model License 동의 및 HF Token 필요.

```bash
# CLI 로그인 (대화형)
hf auth login

# 또는 환경변수 설정
export HF_TOKEN="hf_..."
```

## 체크포인트 다운로드

실행 시 자동 다운로드됩니다. 캐시 위치 변경은 `HF_HOME` 환경변수로 설정.

---

> **참고**: Docker 사용 시 `--runtime=nvidia --ipc=host` 필요. Virtual Environment(위 절차)가 brevlab 환경에서는 더 간단합니다.


---


## Cosmos-transfer2.5
   * https://github.com/nvidia-cosmos/cosmos-transfer2.5/blob/main/docs/inference.md
   * 다음 페이지에 따라 예제를 직접 수정해보고, assets/robot_example/robot_prompt 를 수정하여 같은 영상에 다른 prompt 적용해보기

## Cosmos-transfer2.5 Examples
  * 모델에 입력할 Prompt는 매우 세밀한 묘사를 하도록 작성해야하며, 많은 시도를 필요로 합니다.

```
The video captures a robotic manipulation demonstration conducted in an outdoor-like setting. Instead of a laboratory environment, the background features a vivid green grass surface that creates a natural and open atmosphere. Two robotic arms are positioned on either side of a black shirt, which is neatly spread out on a yellow cushion placed on the ground. Behind them, there is a couch made of paper material, adding an interesting, lightweight element to the scene. The left robotic arm is white with a black gripper and begins the task by moving toward the shirt with precise, controlled motions. Its gripper opens and closes as it aligns itself for an accurate grasp. The right robotic arm, which is black with a more articulated gripper, remains still at first, ready to cooperate in the manipulation. Once the left arm grips one side of the shirt and lifts it slightly, the right arm moves in to secure the opposite edge. The two arms then work in synchronized motion, gently lifting and holding the shirt between them. Their precise, coordinated movements emphasize both the stability of their grip and the flexibility required to handle soft fabric. The camera remains fixed on the scene, ensuring a clear, uninterrupted view of the entire manipulation process against the grassy background and paper-textured sofa.

<img width="11653" height="41" alt="image" src="https://github.com/user-attachments/assets/1606fb5b-1496-4901-bf74-17b7ed3a6ca1" />
```

<img src="img/007.jpg">


## Cosmos-cosmos2.5 Examples
   * Input이 애매하거나, 모델이 아직 완벽하지 않기 때문에 오류가 발생하기도 합니다.

```
The video has been transformed from a modern urban driving scene to one set along a scenic beachfront. It appears to be filmed with a dashcam or a similar fixed camera mounted inside the vehicle. On both sides of the wide road, there are low-rise buildings, giving the area a relaxed and open atmosphere. These buildings are mostly small shops, cafés, and inns, contributing to a coastal town vibe. Several cars are visible on the road ahead, but unlike the original scene, they are all white, creating a clean and uniform look. Traffic is light, and the vehicles maintain a steady pace as they move forward. Traffic cones are placed along the road to guide cars through a lane closure or roadwork area. On the left side of the road, palm trees line the sidewalk, adding a tropical and beachside feeling to the scene. Pedestrians can be seen walking leisurely or standing near the buildings. The architecture is characterized by light-colored concrete and wood accents rather than glass facades, enhancing the seaside ambiance. The sky is clear and sunny, making the scene bright and highly visible. The car maintains a constant speed as it approaches an intersection where the road splits into different directions. The camera remains fixed throughout the drive, providing a stable view of the palm-lined road, the white cars, and the relaxed coastal surroundings. The overall atmosphere is calm, warm, and reminiscent of a peaceful beachfront town.
<img width="9997" height="32" alt="image" src="https://github.com/user-attachments/assets/d99e5133-92a1-4a0f-b404-bb596ab2ba18" />
```

```
비디오는 현대적인 도심 주행 장면에서 아름다운 해변가 풍경으로 변환되었습니다. 차량 내부에 장착된 대시캠 또는 이와 유사한 고정 카메라로 촬영된 것으로 보입니다. 넓은 도로 양쪽에는 저층 건물들이 자리 잡고 있어 지역 전체에 여유롭고 개방적인 분위기를 줍니다. 이 건물들은 대부분 작은 상점, 카페, 여관들로 구성되어 해안 마을의 분위기를 자아냅니다. 도로 앞쪽에는 여러 대의 차량이 보이지만, 원본 장면과 달리 모두 흰색으로 깔끔하고 통일감 있는 모습을 보여줍니다. 교통량은 적고, 차량들은 일정한 속도로 앞으로 나아갑니다. 도로를 따라 차선 통제 또는 공사 구역을 안내하는 교통 콘이 설치되어 있습니다. 도로 왼쪽에는 야자수가 인도를 따라 늘어서 있어 장면에 열대 해변가 느낌을 더합니다. 보행자들은 건물 근처에서 여유롭게 걷거나 서 있는 모습이 보입니다. 건축 양식은 유리 외관보다는 밝은 색상의 콘크리트와 목재 악센트가 특징으로, 해변가 분위기를 한층 살려줍니다. 하늘은 맑고 화창하여 장면이 밝고 선명하게 보입니다. 차량은 도로가 여러 방향으로 갈라지는 교차로에 접근하면서 일정한 속도를 유지합니다. 카메라는 주행 내내 고정되어 있어 야자수가 늘어선 도로, 흰색 차량, 여유로운 해안가 풍경을 안정적으로 보여줍니다. 전반적인 분위기는 평화로운 해변가 마을을 연상시키는 고요하고 따뜻한 느낌입니다
```

<img src="img/008.jpg">

## Cosmos Synthetic Data Generation 
   * Cosmos Synthetic Data Generation : https://docs.isaacsim.omniverse.nvidia.com/5.1.0/replicator_tutorials/tutorial_replicator_cosmos.html
   * Cosmos에 들어갈 input data를 생성하는 script

## Cosmos Synthetic Data Generation 

```
This scene depicts the interior of a factory. The floor is made of white epoxy material, and inside the factory, rows of metal racks are lined up, each stacked with blue boxes. On the factory floor, several items have fallen off the racks, and safety cones and warning markings are placed nearby to prevent entry into restricted areas. On the right side of the scene, a white male worker wearing a fluorescent safety jacket and a hat is working. The factory walls are made of red brick, and the structural frame above the bricks is constructed of steel. Fluorescent lights hanging from the ceiling illuminate the space, adding to the realistic atmosphere of the scene. The entire image is rendered with such a high level of realism that it does not look like computer graphics or a simulated environment at all.
<img width="5509" height="32" alt="image" src="https://github.com/user-attachments/assets/6a532b44-5cce-47f5-9808-9740adf2b228" />
```

```
이 장면은 공장 내부를 묘사하고 있습니다. 바닥은 흰색 에폭시 재질로 되어 있으며, 공장 내부에는 여러 줄의 금속 랙이 정렬되어 있고 각각 파란색 상자가 쌓여 있습니다. 공장 바닥에는 랙에서 떨어진 몇몇 물건들이 있으며, 출입 제한 구역 진입을 막기 위해 안전 콘과 경고 표시가 근처에 배치되어 있습니다. 장면 오른쪽에는 형광 안전 조끼와 모자를 착용한 백인 남성 작업자가 작업 중입니다. 공장 벽은 붉은 벽돌로 되어 있고, 벽돌 위의 구조 프레임은 강철로 구성되어 있습니다. 천장에 매달린 형광등이 공간을 비추며 장면의 사실적인 분위기를 더하고 있습니다. 전체 이미지는 컴퓨터 그래픽이나 시뮬레이션 환경처럼 보이지 않을 정도로 높은 수준의 사실감으로 렌더링되어 있습니다.
```


<img src="img/009-1.jpg">

<img src="img/009-2.jpg">

## Do it yourself
   * Isaac Sim과 Cosmos-transfer2.5를 사용하여 산출물을 만들고 아래 항목들을 제출
      -	Stage 구성에 사용한 usd 전체
      -	Stage 구성 및 Synthetic Data Generation 용도로 사용한 데이터 전체
      -	Cosmos-transfer2.5 에 들어간 input 폴더 및 prompt
      -	결과 영상











