# Physical AI & NVIDIA Omniverse / OpenUSD Overview

## Introduction

### Foundations - Physical AI Trends

- **Physical AI** - AI that understands and interacts with the physical world
- **OpenUSD** - Universal Scene Description, a framework for 3D scene description
- **Isaac Sim** - NVIDIA's robotics simulation platform
  - Isaac Sim core essentials
  - Basic Tutorial
  - CAD to Sim → Robot Rigging → Task Control
- **World Model / NVIDIA Cosmos** - World modeling and synthetic data generation

### Hands On

- **Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac**

### Physical AI Trends

> F.03 Livestream - Day 5
>
> Watch a team of humanoid robots running a full 100+ Hour shift at human performance levels. This is fully autonomous running Helix-02.

---

## Three Core Pillars

### Graphics

| Concept | Description |
|---|---|
| **OpenUSD (Universal Scene Description)** | Framework for graphics definition and pipeline construction |
| **OMNIVERSE CAD Converter** | Converts industrial designs into SimReady Assets |

<img src="2026_001.png">

### Physics

| Concept | Description |
|---|---|
| **NVIDIA Warp** | Framework for writing differentiable physics kernels |
| **CUDA Acceleration** | GPU kernel optimization for hardware utilization |
| **Mechanics Modeling** | Statics and dynamics in robot implementation within simulation |

<img src="2026_002.png">

### Software

| Concept | Description |
|---|---|
| **Basic Coding Experience** | Fundamental coding including deep learning frameworks |
| **Simulation Step & Loop** | Understanding physics engine stepping |
| **Lifecycle** | Creation and destruction of simulation objects |

<img src="2026_003.png">

---

## Traditional Robotics vs Physical AI

| Traditional Robotics | Robots with Physical AI |
|---|---|
| Rule-based execution | Policy-based execution |
| Hard-coded trajectories with zero adaptability | Generative trajectories with full adaptability |
| Designed for repeatability | Designed for generalization |
| **Highly vulnerable to noise** | **Robust noise grounding** |

<img src="2026_004.png"> <img src="2026_005.png">

---

## NVIDIA Omniverse

NVIDIA Omniverse is a collection of libraries and microservices for developing physically based industrial digital twins and robotics AI applications.

<img src="2026_006.png">

- Originally built on **5 pillars**: Nucleus, Connect, Kit, Simulation, RTX Renderer
- The definition has evolved as the ecosystem has grown and diversified

### Resources

- [NVIDIA Omniverse Libraries](https://developer.nvidia.com/omniverse)
- [NVIDIA Omniverse Blueprints](https://developer.nvidia.com/omniverse/blueprints)


#### cosmos-transfer1-7b

- Free Endpoint
- Generates physics-aware video world states for physical AI development using text prompts and multiple spatial control inputs derived from real-world data or simulation.

https://build.nvidia.com/nvidia/cosmos-transfer1-7b

**Original : white esspresso coffee maker**
```
A contemporary and sophisticated black luxury kitchen bathed in natural daylight, featuring a spacious layout with an expansive dark granite island at its center. There is a white coffee maker on the island in front of the white robot arm. The cabinetry is finished in a matte black, with elegant silver hardware adding a refined touch. The countertops, made of dark granite, gleam under the soft glow of three pendant lights with sleek metallic finishes. A white robot arm interacts with a white coffee cup and white esspresso coffee maker on the kitchen island. The kitchen is equipped with top-of-the-line stainless steel appliances, including a professional-grade gas range with a large custom vent hood, seamlessly integrated into the design. A double-door refrigerator is neatly concealed within the cabinetry. The backsplash is composed of a slab of black marble with gold veins, complementing the crisp aesthetic while reflecting the ambient lighting. The island features a deep sink with a high-end chrome faucet, surrounded by plush, high-backed barstools upholstered in leather. Open shelving on the side of the island provides space for cookbooks and decorative elements, adding a personalized touch. Large windows flood the space with natural light, offering a glimpse of a desert landscape outside.
```

```
현대적이고 세련된 블랙 럭셔리 주방이 자연광으로 가득하다. 넓은 레이아웃 중앙에는 웅장한 다크 그라나이트 아일랜드가 자리 잡고 있다. 아일랜드 위에는 화이트 커피 메이커가 로봇 팔 앞에 놓여 있다. 캐비닛은 무광 블랙 마감에 우아한 실버 하드웨어가 세련된 포인트를 더한다. 다크 그라나이트로 만들어진 조리대는 메탈릭 마감의 세련된 펜던트 조명 세 개가 내리는 부드러운 빛 아래에서 은은하게 빛난다. 흰색 로봇 팔이 주방 아일랜드 위의 흰색 커피 잔과 화이트 에스프레소 커피 메이커와 상호작용하고 있다. 주방은 최고급 스테인리스 스틸 가전제품을 갖추고 있으며, 대형 커스텀 벤트 후드가 달린 프로페셔널 등급의 가스레인지가 디자인에 매끄럽게 통합되어 있다. 양문형 냉장고는 캐비닛 안에 깔끔하게 숨겨져 있다. 백스플래시는 금색 줄무늬가 있는 블랙 대리석 슬라브로 구성되어 있어, 깔끔한 미적 감각을 보완하고 주변 조명을 반사한다. 아일랜드에는 깊은 싱크대와 고급스러운 크롬 수도꼭지가 설치되어 있으며, 주변에는 가죽으로 덮인 하이백 바스툴이 놓여 있다. 아일랜드 측면의 오픈 선반에는 요리책과 장식 소품을 두어 개인적인 터치를 더했다. 큰 창문을 통해 자연광이 실내를 가득 채우고, 창밖으로 사막 풍경이 펼쳐진다.
```

**Chage : White -> Red**
```
A contemporary and sophisticated black luxury kitchen bathed in natural daylight, featuring a spacious layout with an expansive dark granite island at its center. There is a white coffee maker on the island in front of the white robot arm. The cabinetry is finished in a matte black, with elegant silver hardware adding a refined touch. The countertops, made of dark granite, gleam under the soft glow of three pendant lights with sleek metallic finishes. A white robot arm interacts with a white coffee cup and red esspresso coffee maker on the kitchen island. The kitchen is equipped with top-of-the-line stainless steel appliances, including a professional-grade gas range with a large custom vent hood, seamlessly integrated into the design. A double-door refrigerator is neatly concealed within the cabinetry. The backsplash is composed of a slab of black marble with gold veins, complementing the crisp aesthetic while reflecting the ambient lighting. The island features a deep sink with a high-end chrome faucet, surrounded by plush, high-backed barstools upholstered in leather. Open shelving on the side of the island provides space for cookbooks and decorative elements, adding a personalized touch. Large windows flood the space with natural light, offering a glimpse of a desert landscape outside.
```


---

### Google 계정

```
비밀번호 : 0519Kosa#
#	수강생	이메일		
1	김지윤	allai01@allai.co.kr		
2	강영빈	allai02@allai.co.kr		
3	유용준	allai03@allai.co.kr		
4	서예진	allai04@allai.co.kr		
5	전승현	allai05@allai.co.kr		
6	권영진	allai06@allai.co.kr		
7	원주성	allai07@allai.co.kr		
8	권오주	allai08@allai.co.kr		
9	박찬수	allai09@allai.co.kr		
10	임희수	allai10@allai.co.kr		
11	이호기	allai11@allai.co.kr		
12	김남우	allai12@allai.co.kr		
13	채민아	allai13@allai.co.kr		
14	조인행	allai14@allai.co.kr		
15	임상혁	allai15@allai.co.kr		
```

* nvidia 계정
https://build.nvidia.com/nvidia/cosmos-transfer1-7b

* nvidia 계정
https://huggingface.co/

* Deepseek 사용해보기
 * https://build.nvidia.com/deepseek-ai/deepseek-v4-pro
---


### Omniverse Kit SDK

The SDK for developing various Omniverse Applications.

- [Overview — Omniverse Kit](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/)
- Isaac Sim
- USD Explorer
- Modular extension architecture for custom development

---

## OpenUSD

**OpenUSD (Universal Scene Description)** is a framework for describing 3D data.

- Originally open-sourced by **Pixar in 2016**
- Managed by **AOUSD (Alliance for OpenUSD)** since 2023
- Standard for complex 3D data collaboration

> *Example: Toy Story 4 (2019)*

### UsdView

A lightweight, fast USD file viewer.

* https://docs.omniverse.nvidia.com/usd/latest/usdview/quickstart.html

* For Windows : https://developer.nvidia.com/downloads/usd/usd_binaries/25.08/usd.py312.windows-x86_64.usdview.release-v25.08.71e038c1.zip
    * 다운로드 이후에 C드라이브 바로 아래에 압축을 해제하고 usd라는 폴더명으로 변경할것
* For Liux : https://developer.nvidia.com/downloads/usd/usd_binaries/25.08/usd.py312.manylinux_2_35_x86_64.usdview.release-v25.08.71e038c1.zip

```bash
# See: https://docs.omniverse.nvidia.com/usd/latest/guide/usdview-quickstart.html
# Follow the page above to install and try
```

--- 

## Project

* https://build.nvidia.com/nvidia/isaac-gr00t-synthetic-manipulation
* https://github.com/NVIDIA-Omniverse-blueprints/synthetic-manipulation-motion-generation

* 이 프로젝트는 Isaac Lab 의 Mimic 기능과 NVIDIA 의 Cosmos를 활용해,
* 적은 수의 인간 시연 데이터만으로 대규모 로봇 imitation learning(모방 학습) 데이터셋을 자동 생성하는 워크플로우입니다.

**핵심 흐름은 두 단계입니다.**

1. 모션 궤적(Motion Trajectory) 생성
   * 인간이 직접 수행한 소수의 로봇 시연 데이터를 기반으로,
   * Isaac Lab Mimic이 새로운 환경 배치(큐브 위치, 로봇 초기 자세 등)에 맞춰 새로운 로봇 동작 궤적을 합성합니다.
   * 예제에서는 Franka Emika Panda 로봇 팔이 큐브를 쌓는 작업을 수행합니다.
   * 환경 랜덤화(randomization)를 통해 다양한 상황의 데이터를 자동 생성합니다.

2. 시각적 데이터 증강(Visual Augmentation)
   * 생성된 로봇 동작 영상을 입력으로 사용해,
   * Cosmos 모델이 조명, 질감, 배경 등 시각 요소를 다양하게 변형합니다.
   * 이를 통해 실제 환경에 가까운 다양한 영상 데이터를 생성하여 모델 일반화 성능을 높입니다.

3. 프로젝트의 목적은:
   * 비싼 인간 시연 데이터 수집 비용을 줄이고,
   * 적은 원본 데이터로도
   * 대규모·고다양성 imitation learning 데이터셋을 자동 구축하는 것입니다.

* 전체 파이프라인은:
   * 인간 시연 → Mimic 기반 궤적 생성 → 영상 변환(Cosmos) → 학습용 데이터셋 생성 순서로 진행됩니다.

**hdf5**

* .hdf5(또는 .h5)는 HDF5 (Hierarchical Data Format version 5) 형식의 파일입니다.
* 대용량·복합 데이터를 저장하기 위해 많이 사용하는 바이너리 데이터 포맷입니다.

* 특징은 다음과 같습니다.

   * 폴더처럼 계층 구조를 가짐
      * 그룹(Group) 안에 데이터셋(Dataset)을 저장
   * 매우 큰 데이터 저장 가능
      * 이미지, 영상 프레임, 센서 데이터, 시계열 데이터 등
   * 머신러닝·과학 계산 분야에서 널리 사용
   * 압축 및 빠른 읽기/쓰기 지원

* 이번 프로젝트에서는 .hdf5 파일이 다음 용도로 사용됩니다.
   * 인간 시연 데이터 저장
      * annotated_dataset.hdf5
    * 새로 생성된 로봇 trajectory 저장
      * generated_dataset.hdf5

* 안에는 보통 이런 정보가 들어 있습니다.
   * 로봇 관절 상태(joint states)
   * 행동(action)
   * 관측(observation)
   * RGB 이미지
   * depth/segmentation 이미지
   * 성공 여부
   * 시뮬레이션 timestep 정보

* 예를 들어 내부 구조는 이런 느낌입니다:

```
/demo_0
    /observations
        rgb
        depth
        joint_pos
    /actions
    /rewards

/demo_1
```

* 파이썬에서는 보통 h5py 라이브러리로 읽습니다.
* 예시:

```python
import h5py

f = h5py.File("generated_dataset.hdf5", "r")

print(list(f.keys()))
```

* 데이터 확인:

```python
print(f["demo_0/actions"][:])
```

* 머신러닝에서는:
   * TensorFlow
   * PyTorch
   * 로봇 시뮬레이터
   * 과학 계산 툴

등에서 자주 사용됩니다.

### annotated_dataset.hdf5 파일의 구조 파악

**1. CLI 스크립트: inspect_hdf5.py**

```
python inspect_hdf5.py datasets/annotated_dataset.hdf5
```

```
(base) C:\Users\user\Desktop>python inspect_hdf5.py annotated_dataset.hdf5

========================================================================
  Full HDF5 Structure: annotated_dataset.hdf5
========================================================================

🔓 File: annotated_dataset.hdf5
   Root attributes:

📁 data/
  📎 attr: env_args = '{"env_name": "Isaac-Stack-Cube-Franka-IK-Rel-Mimic-v0", "type": 2}'
  📎 attr: total = np.int64(2163)
  📎 attr: env_args = '{"env_name": "Isaac-Stack-Cube-Franka-IK-Rel-Mimic-v0", "type": 2}'
  📎 attr: total = np.int64(2163)
  📁 demo_0/
    📎 attr: num_samples = np.int64(236)
    📎 attr: success = np.True_
    📄 actions  shape=(236, 7)  dtype=float32
        📍 row[0]: [0. 0. 0. 0. 0. 0. 1.]
        📊 stats: min=-1.0000, max=1.0000, mean=0.0115
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0256 -0.178  -0.1263 -2.5081  0.0064  2.4062  0.7304  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5767  0.0825  0.0203  0.9418  0.      0.     -0.3362]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5912 -0.0448  0.0203  0.881   0.      0.      0.4731]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4601  0.0867  0.0203  0.9969  0.      0.     -0.0788]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(236, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=0.0109
      📄 cube_orientations  shape=(236, 12)  dtype=float32
          📍 row[0]: [ 0.9418  0.      0.     -0.3362  0.881   0.      0.      0.4731  0.9969
  0.      0.     -0.0788]
          📊 stats: min=-0.4209, max=0.9986, mean=0.2332
      📄 cube_positions  shape=(236, 9)  dtype=float32
          📍 row[0]: [ 0.5767  0.0825  0.0203  0.5912 -0.0448  0.0203  0.4601  0.0867  0.0203]
          📊 stats: min=-0.0549, max=0.5912, mean=0.2202
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(236, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9959 -0.0482  0.077   0.4622 -0.0498 -0.9986  0.019  -0.0434]
              📊 stats: min=-0.9989, max=1.0000, mean=0.0040
        📁 object_pose/
          📄 cube_1  shape=(236, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.7739  0.6333  0.      0.5767 -0.6333  0.7739 -0.      0.0825]
              📊 stats: min=-0.6334, max=1.0000, mean=0.2641
          📄 cube_2  shape=(236, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.5524 -0.8336  0.      0.5912  0.8336  0.5524  0.     -0.0448]
              📊 stats: min=-0.8336, max=1.0000, mean=0.2411
          📄 cube_3  shape=(236, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9876  0.1571  0.      0.4601 -0.1571  0.9876 -0.      0.0867]
              📊 stats: min=-0.7636, max=1.0000, mean=0.2830
        📁 subtask_term_signals/
          📄 grasp_1  shape=(236,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(236,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(236,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(236, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9959 -0.0482  0.077   0.4622 -0.0498 -0.9986  0.019  -0.0434]
              📊 stats: min=-0.9996, max=1.0000, mean=0.0019
      📄 eef_pos  shape=(236, 3)  dtype=float32
          📍 row[0]: [ 0.4622 -0.0434  0.2504]
          📊 stats: min=-0.0545, max=0.5847, mean=0.2373
      📄 eef_quat  shape=(236, 4)  dtype=float32
          📍 row[0]: [-0.0105  0.9989 -0.0245  0.0383]
          📊 stats: min=-0.3351, max=0.9989, mean=0.2046
      📄 gripper_pos  shape=(236, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0002
      📄 joint_pos  shape=(236, 9)  dtype=float32
          📍 row[0]: [-0.0188  0.0114 -0.0156  0.0067  0.002   0.0287  0.0352  0.      0.    ]
          📊 stats: min=-0.2304, max=1.0925, mean=0.1939
      📄 joint_vel  shape=(236, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-0.6832, max=0.5923, mean=0.0204
      📄 object  shape=(236, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.5767  0.0825  0.0203  0.9418  0.      0.     -0.3362  0.5912]
          📊 stats: min=-0.4209, max=0.9986, mean=0.1210
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(236, 9)  dtype=float32
              📍 row[0]: [ 0.0256 -0.178  -0.1263 -2.5081  0.0064  2.4062  0.7304  0.04    0.04  ]
              📊 stats: min=-2.5829, max=3.0383, mean=0.2379
          📄 joint_velocity  shape=(236, 9)  dtype=float32
              📍 row[0]: [ 0.  0. -0. -0.  0. -0. -0. -0.  0.]
              📊 stats: min=-0.6832, max=0.5923, mean=0.0204
          📄 root_pose  shape=(236, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(236, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(236, 7)  dtype=float32
              📍 row[0]: [ 0.5762  0.082   0.0203  0.9418 -0.     -0.     -0.3362]
              📊 stats: min=-0.3363, max=0.9418, mean=0.1834
          📄 root_velocity  shape=(236, 6)  dtype=float32
              📍 row[0]: [ 0.0002 -0.0002 -0.0001  0.0061  0.0021 -0.0003]
              📊 stats: min=-0.3266, max=0.0547, mean=0.0026
        📁 cube_2/
          📄 root_pose  shape=(236, 7)  dtype=float32
              📍 row[0]: [ 0.5907 -0.0442  0.0203  0.8831 -0.     -0.      0.4691]
              📊 stats: min=-0.0549, max=0.9040, mean=0.2868
          📄 root_velocity  shape=(236, 6)  dtype=float32
              📍 row[0]: [ 0.0002  0.0002 -0.0001 -0.0006  0.0056 -0.0011]
              📊 stats: min=-13.3399, max=4.5865, mean=-0.6029
        📁 cube_3/
          📄 root_pose  shape=(236, 7)  dtype=float32
              📍 row[0]: [ 0.4605  0.0861  0.0203  0.9969 -0.     -0.     -0.0781]
              📊 stats: min=-0.4209, max=0.9986, mean=0.2125
          📄 root_velocity  shape=(236, 6)  dtype=float32
              📍 row[0]: [ 0.0001 -0.0001 -0.0001 -0.0016  0.0006 -0.0001]
              📊 stats: min=-20.2164, max=1.9579, mean=-1.4423
  📁 demo_1/
    📎 attr: num_samples = np.int64(233)
    📎 attr: success = np.True_
    📄 actions  shape=(233, 7)  dtype=float32
        📍 row[0]: [0. 0. 0. 0. 0. 0. 1.]
        📊 stats: min=-1.0000, max=1.0000, mean=0.0113
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.047  -0.2128 -0.0902 -2.5194  0.0137  2.3945  0.6787  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5803  0.0601  0.0203  0.8793  0.      0.     -0.4764]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4574 -0.0312  0.0203  0.9317  0.      0.      0.3633]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [0.4721 0.0898 0.0203 0.9795 0.     0.     0.2016]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(233, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=0.0107
      📄 cube_orientations  shape=(233, 12)  dtype=float32
          📍 row[0]: [ 0.8793  0.      0.     -0.4764  0.9317  0.      0.      0.3633  0.9795
  0.      0.      0.2016]
          📊 stats: min=-0.4764, max=0.9878, mean=0.2344
      📄 cube_positions  shape=(233, 9)  dtype=float32
          📍 row[0]: [ 0.5803  0.0601  0.0203  0.4574 -0.0312  0.0203  0.4721  0.0898  0.0203]
          📊 stats: min=-0.0345, max=0.5803, mean=0.2150
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(233, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9945  0.056   0.0882  0.4597  0.054  -0.9982  0.0247 -0.0164]
              📊 stats: min=-1.0000, max=1.0000, mean=0.1100
        📁 object_pose/
          📄 cube_1  shape=(233, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.5462  0.8377  0.      0.5803 -0.8377  0.5462 -0.      0.0601]
              📊 stats: min=-0.8377, max=1.0000, mean=0.2345
          📄 cube_2  shape=(233, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.736  -0.677   0.      0.4574  0.677   0.736   0.     -0.0312]
              📊 stats: min=-0.6770, max=1.0000, mean=0.2693
          📄 cube_3  shape=(233, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9187 -0.3949  0.      0.4721  0.3949  0.9187  0.      0.0898]
              📊 stats: min=-0.3992, max=1.0000, mean=0.2806
        📁 subtask_term_signals/
          📄 grasp_1  shape=(233,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(233,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(233,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(233, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9945  0.056   0.0882  0.4597  0.054  -0.9982  0.0247 -0.0164]
              📊 stats: min=-1.0000, max=1.0000, mean=0.1117
      📄 eef_pos  shape=(233, 3)  dtype=float32
          📍 row[0]: [ 0.4597 -0.0164  0.2605]
          📊 stats: min=-0.0298, max=0.5754, mean=0.2307
      📄 eef_quat  shape=(233, 4)  dtype=float32
          📍 row[0]: [-0.0111  0.9986  0.0275  0.0444]
          📊 stats: min=-0.0472, max=0.9987, mean=0.3037
      📄 gripper_pos  shape=(233, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0002
      📄 joint_pos  shape=(233, 9)  dtype=float32
          📍 row[0]: [ 0.0026 -0.0234  0.0205 -0.0046  0.0093  0.017  -0.0165  0.      0.    ]
          📊 stats: min=-0.9968, max=0.6442, mean=0.0669
      📄 joint_vel  shape=(233, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0023, max=0.7522, mean=0.0069
      📄 object  shape=(233, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.5803  0.0601  0.0203  0.8793  0.      0.     -0.4764  0.4574]
          📊 stats: min=-0.4764, max=0.9878, mean=0.1190
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(233, 9)  dtype=float32
              📍 row[0]: [ 0.047  -0.2128 -0.0902 -2.5194  0.0137  2.3945  0.6787  0.04    0.04  ]
              📊 stats: min=-2.5609, max=2.9022, mean=0.1104
          📄 joint_velocity  shape=(233, 9)  dtype=float32
              📍 row[0]: [-0. -0.  0. -0. -0. -0.  0. -0. -0.]
              📊 stats: min=-1.0023, max=0.7522, mean=0.0069
          📄 root_pose  shape=(233, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(233, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(233, 7)  dtype=float32
              📍 row[0]: [ 0.5803  0.0601  0.0203  0.8793 -0.     -0.     -0.4764]
              📊 stats: min=-0.4764, max=0.8793, mean=0.1520
          📄 root_velocity  shape=(233, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.      0.0012  0.0006  0.0001]
              📊 stats: min=-0.4754, max=0.7049, mean=0.0039
        📁 cube_2/
          📄 root_pose  shape=(233, 7)  dtype=float32
              📍 row[0]: [ 0.4574 -0.0312  0.0203  0.9317 -0.      0.      0.3633]
              📊 stats: min=-0.0450, max=0.9764, mean=0.2653
          📄 root_velocity  shape=(233, 6)  dtype=float32
              📍 row[0]: [ 0.      0.     -0.     -0.0004  0.0009  0.    ]
              📊 stats: min=-21.4622, max=5.1609, mean=-0.8863
        📁 cube_3/
          📄 root_pose  shape=(233, 7)  dtype=float32
              📍 row[0]: [ 0.4721  0.0898  0.0203  0.9795 -0.     -0.      0.2016]
              📊 stats: min=-0.0583, max=0.9878, mean=0.2612
          📄 root_velocity  shape=(233, 6)  dtype=float32
              📍 row[0]: [ 0.0002  0.0003 -0.0001 -0.0075  0.0062  0.    ]
              📊 stats: min=-18.6861, max=7.7831, mean=-0.6430
  📁 demo_2/
    📎 attr: num_samples = np.int64(194)
    📎 attr: success = np.True_
    📄 actions  shape=(194, 7)  dtype=float32
        📍 row[0]: [ 0.  0. -0.  0.  0.  0.  1.]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0414
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0265 -0.1701 -0.1343 -2.5197 -0.0141  2.3456  0.705   0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5826 -0.074   0.0203  0.956   0.      0.     -0.2933]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.401   0.0317  0.0203  0.9995  0.      0.     -0.0309]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4398 -0.0905  0.0203  0.9858  0.      0.     -0.1678]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(194, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0421
      📄 cube_orientations  shape=(194, 12)  dtype=float32
          📍 row[0]: [ 0.956   0.      0.     -0.2933  0.9995  0.      0.     -0.0309  0.9858
  0.      0.     -0.1678]
          📊 stats: min=-0.3309, max=0.9997, mean=0.1821
      📄 cube_positions  shape=(194, 9)  dtype=float32
          📍 row[0]: [ 0.5826 -0.074   0.0203  0.401   0.0317  0.0203  0.4398 -0.0905  0.0203]
          📊 stats: min=-0.1005, max=0.5855, mean=0.1743
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(194, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9999 -0.0155 -0.0041  0.4437 -0.0155 -0.9998  0.0131 -0.0462]
              📊 stats: min=-1.0000, max=1.0000, mean=-0.0041
        📁 object_pose/
          📄 cube_1  shape=(194, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.828   0.5607  0.      0.5826 -0.5607  0.828  -0.     -0.074 ]
              📊 stats: min=-0.5607, max=1.0000, mean=0.2616
          📄 cube_2  shape=(194, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9981  0.0618  0.      0.401  -0.0618  0.9981 -0.      0.0317]
              📊 stats: min=-0.5857, max=1.0000, mean=0.2682
          📄 cube_3  shape=(194, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9437  0.3309  0.      0.4398 -0.3309  0.9437 -0.     -0.0905]
              📊 stats: min=-0.6245, max=1.0000, mean=0.2671
        📁 subtask_term_signals/
          📄 grasp_1  shape=(194,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(194,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(194,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(194, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9999 -0.0155 -0.0041  0.4437 -0.0155 -0.9998  0.0131 -0.0462]
              📊 stats: min=-1.0000, max=1.0000, mean=-0.0068
      📄 eef_pos  shape=(194, 3)  dtype=float32
          📍 row[0]: [ 0.4437 -0.0462  0.236 ]
          📊 stats: min=-0.1024, max=0.5876, mean=0.1961
      📄 eef_quat  shape=(194, 4)  dtype=float32
          📍 row[0]: [-0.0065  0.9999 -0.0078 -0.0021]
          📊 stats: min=-0.3052, max=0.9999, mean=0.1879
      📄 gripper_pos  shape=(194, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0002
      📄 joint_pos  shape=(194, 9)  dtype=float32
          📍 row[0]: [-0.0179  0.0193 -0.0236 -0.0049 -0.0185 -0.0319  0.0098  0.      0.    ]
          📊 stats: min=-0.3166, max=0.6872, mean=0.1379
      📄 joint_vel  shape=(194, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.1194, max=1.0275, mean=0.0119
      📄 object  shape=(194, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.5826 -0.074   0.0203  0.956   0.      0.     -0.2933  0.401 ]
          📊 stats: min=-0.3309, max=0.9997, mean=0.0943
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(194, 9)  dtype=float32
              📍 row[0]: [ 0.0265 -0.1701 -0.1343 -2.5197 -0.0141  2.3456  0.705   0.04    0.04  ]
              📊 stats: min=-2.6885, max=2.9996, mean=0.1819
          📄 joint_velocity  shape=(194, 9)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  0.  0. -0. -0. -0.  0.]
              📊 stats: min=-1.1194, max=1.0275, mean=0.0119
          📄 root_pose  shape=(194, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(194, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(194, 7)  dtype=float32
              📍 row[0]: [ 0.5826 -0.074   0.0203  0.956  -0.      0.     -0.2933]
              📊 stats: min=-0.2933, max=0.9560, mean=0.1702
          📄 root_velocity  shape=(194, 6)  dtype=float32
              📍 row[0]: [-0.     -0.     -0.      0.0009 -0.0003 -0.0001]
              📊 stats: min=-0.4415, max=0.5018, mean=0.0009
        📁 cube_2/
          📄 root_pose  shape=(194, 7)  dtype=float32
              📍 row[0]: [ 0.401   0.0317  0.0203  0.9995 -0.     -0.     -0.0309]
              📊 stats: min=-0.3078, max=0.9997, mean=0.1859
          📄 root_velocity  shape=(194, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.     -0.0005 -0.      0.    ]
              📊 stats: min=-16.1258, max=6.9953, mean=-0.9279
        📁 cube_3/
          📄 root_pose  shape=(194, 7)  dtype=float32
              📍 row[0]: [ 0.4398 -0.0905  0.0203  0.9858 -0.     -0.     -0.1678]
              📊 stats: min=-0.3309, max=0.9919, mean=0.1801
          📄 root_velocity  shape=(194, 6)  dtype=float32
              📍 row[0]: [ 0.0001 -0.0002 -0.0001  0.0023  0.0001 -0.0005]
              📊 stats: min=-13.0702, max=4.5584, mean=-0.8069
  📁 demo_3/
    📎 attr: num_samples = np.int64(209)
    📎 attr: success = np.True_
    📄 actions  shape=(209, 7)  dtype=float32
        📍 row[0]: [ 0.  0. -0.  0.  0.  0.  1.]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0191
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0432 -0.2001 -0.09   -2.5258  0.0228  2.3657  0.7198  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [0.4548 0.0114 0.0203 0.999  0.     0.     0.0445]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5433  0.0768  0.0203  0.995   0.      0.     -0.1003]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5592 -0.0597  0.0203  0.8985  0.      0.     -0.4389]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(209, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0198
      📄 cube_orientations  shape=(209, 12)  dtype=float32
          📍 row[0]: [ 0.999   0.      0.      0.0445  0.995   0.      0.     -0.1003  0.8985
  0.      0.     -0.4389]
          📊 stats: min=-0.7438, max=1.0000, mean=0.1926
      📄 cube_positions  shape=(209, 9)  dtype=float32
          📍 row[0]: [ 0.4548  0.0114  0.0203  0.5433  0.0768  0.0203  0.5592 -0.0597  0.0203]
          📊 stats: min=-0.0597, max=0.5648, mean=0.1804
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(209, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9992  0.0049  0.0408  0.4503  0.0036 -0.9995  0.032  -0.0168]
              📊 stats: min=-0.9999, max=1.0000, mean=-0.0256
        📁 object_pose/
          📄 cube_1  shape=(209, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.996  -0.089   0.      0.4548  0.089   0.996   0.      0.0114]
              📊 stats: min=-0.0891, max=1.0000, mean=0.2799
          📄 cube_2  shape=(209, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9799  0.1997  0.      0.5433 -0.1997  0.9799 -0.      0.0768]
              📊 stats: min=-0.2756, max=1.0000, mean=0.2849
          📄 cube_3  shape=(209, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.6147  0.7888  0.      0.5592 -0.7888  0.6147 -0.     -0.0597]
              📊 stats: min=-0.9997, max=1.0000, mean=0.2104
        📁 subtask_term_signals/
          📄 grasp_1  shape=(209,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(209,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(209,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(209, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9992  0.0049  0.0408  0.4503  0.0036 -0.9995  0.032  -0.0168]
              📊 stats: min=-1.0000, max=1.0000, mean=-0.0302
      📄 eef_pos  shape=(209, 3)  dtype=float32
          📍 row[0]: [ 0.4503 -0.0168  0.2491]
          📊 stats: min=-0.0572, max=0.5764, mean=0.2178
      📄 eef_quat  shape=(209, 4)  dtype=float32
          📍 row[0]: [-0.016   0.9997  0.0021  0.0204]
          📊 stats: min=-0.7376, max=0.9997, mean=0.1268
      📄 gripper_pos  shape=(209, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0003
      📄 joint_pos  shape=(209, 9)  dtype=float32
          📍 row[0]: [-0.0012 -0.0107  0.0207 -0.011   0.0184 -0.0118  0.0246  0.      0.    ]
          📊 stats: min=-0.1910, max=1.7399, mean=0.1863
      📄 joint_vel  shape=(209, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0978, max=1.4364, mean=0.0216
      📄 object  shape=(209, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [0.4548 0.0114 0.0203 0.999  0.     0.     0.0445 0.5433]
          📊 stats: min=-0.7438, max=1.0000, mean=0.0883
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(209, 9)  dtype=float32
              📍 row[0]: [ 0.0432 -0.2001 -0.09   -2.5258  0.0228  2.3657  0.7198  0.04    0.04  ]
              📊 stats: min=-2.5742, max=2.7535, mean=0.2305
          📄 joint_velocity  shape=(209, 9)  dtype=float32
              📍 row[0]: [ 0. -0. -0. -0.  0. -0. -0. -0.  0.]
              📊 stats: min=-1.0978, max=1.4364, mean=0.0216
          📄 root_pose  shape=(209, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(209, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(209, 7)  dtype=float32
              📍 row[0]: [ 0.4548  0.0114  0.0203  0.999   0.     -0.      0.0445]
              📊 stats: min=-0.0011, max=0.9990, mean=0.2186
          📄 root_velocity  shape=(209, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.     -0.0006  0.0001  0.    ]
              📊 stats: min=-0.5394, max=0.8850, mean=0.0012
        📁 cube_2/
          📄 root_pose  shape=(209, 7)  dtype=float32
              📍 row[0]: [ 0.5433  0.0768  0.0203  0.995   0.      0.     -0.1003]
              📊 stats: min=-0.1391, max=1.0000, mean=0.2210
          📄 root_velocity  shape=(209, 6)  dtype=float32
              📍 row[0]: [-0.     -0.     -0.      0.0002 -0.0005  0.    ]
              📊 stats: min=-12.5528, max=3.0735, mean=-0.5601
        📁 cube_3/
          📄 root_pose  shape=(209, 7)  dtype=float32
              📍 row[0]: [ 0.5592 -0.0597  0.0203  0.8985 -0.     -0.     -0.4389]
              📊 stats: min=-0.7438, max=0.8985, mean=0.1221
          📄 root_velocity  shape=(209, 6)  dtype=float32
              📍 row[0]: [ 0.0003 -0.0003 -0.      0.0074  0.006   0.0001]
              📊 stats: min=-12.9606, max=19.0976, mean=-0.3566
  📁 demo_4/
    📎 attr: num_samples = np.int64(232)
    📎 attr: success = np.True_
    📄 actions  shape=(232, 7)  dtype=float32
        📍 row[0]: [ 0.  0. -0.  0.  0.  0.  1.]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0106
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0258 -0.1745 -0.0731 -2.5373 -0.0055  2.3705  0.6764  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [0.4488 0.0227 0.0203 0.8925 0.     0.     0.4511]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [0.5869 0.0206 0.0203 0.9529 0.     0.     0.3032]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.448  -0.0926  0.0203  0.9997  0.      0.     -0.0233]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(232, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0112
      📄 cube_orientations  shape=(232, 12)  dtype=float32
          📍 row[0]: [ 0.8925  0.      0.      0.4511  0.9529  0.      0.      0.3032  0.9997
  0.      0.     -0.0233]
          📊 stats: min=-0.3660, max=0.9997, mean=0.2949
      📄 cube_positions  shape=(232, 9)  dtype=float32
          📍 row[0]: [ 0.4488  0.0227  0.0203  0.5869  0.0206  0.0203  0.448  -0.0926  0.0203]
          📊 stats: min=-0.0945, max=0.5869, mean=0.1686
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(232, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9977  0.0667  0.0076  0.444   0.0667 -0.9977  0.0085 -0.0197]
              📊 stats: min=-1.0000, max=1.0000, mean=-0.0570
        📁 object_pose/
          📄 cube_1  shape=(232, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.5929 -0.8052  0.      0.4488  0.8052  0.5929  0.      0.0227]
              📊 stats: min=-0.8052, max=1.0000, mean=0.2301
          📄 cube_2  shape=(232, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.8162 -0.5778  0.      0.5869  0.5778  0.8162  0.      0.0206]
              📊 stats: min=-0.8063, max=1.0000, mean=0.2449
          📄 cube_3  shape=(232, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9989  0.0465  0.      0.448  -0.0465  0.9989 -0.     -0.0926]
              📊 stats: min=-0.6812, max=1.0000, mean=0.2733
        📁 subtask_term_signals/
          📄 grasp_1  shape=(232,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(232,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(232,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(232, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9977  0.0667  0.0076  0.444   0.0667 -0.9977  0.0085 -0.0197]
              📊 stats: min=-1.0000, max=1.0000, mean=-0.0586
      📄 eef_pos  shape=(232, 3)  dtype=float32
          📍 row[0]: [ 0.444  -0.0197  0.2332]
          📊 stats: min=-0.0856, max=0.5968, mean=0.2051
      📄 eef_quat  shape=(232, 4)  dtype=float32
          📍 row[0]: [-0.0041  0.9994  0.0334  0.0039]
          📊 stats: min=-0.8604, max=0.9999, mean=0.0518
      📄 gripper_pos  shape=(232, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0003
      📄 joint_pos  shape=(232, 9)  dtype=float32
          📍 row[0]: [-0.0186  0.0149  0.0376 -0.0225 -0.0099 -0.007  -0.0188  0.      0.    ]
          📊 stats: min=-0.2277, max=2.2021, mean=0.2347
      📄 joint_vel  shape=(232, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.2174, max=1.5776, mean=0.0266
      📄 object  shape=(232, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [0.4488 0.0227 0.0203 0.8925 0.     0.     0.4511 0.5869]
          📊 stats: min=-0.3660, max=0.9997, mean=0.1233
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(232, 9)  dtype=float32
              📍 row[0]: [ 0.0258 -0.1745 -0.0731 -2.5373 -0.0055  2.3705  0.6764  0.04    0.04  ]
              📊 stats: min=-2.6780, max=3.0237, mean=0.2791
          📄 joint_velocity  shape=(232, 9)  dtype=float32
              📍 row[0]: [ 0.  0.  0.  0.  0.  0.  0. -0. -0.]
              📊 stats: min=-1.2174, max=1.5776, mean=0.0266
          📄 root_pose  shape=(232, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(232, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(232, 7)  dtype=float32
              📍 row[0]: [0.4488 0.0227 0.0203 0.8925 0.     0.     0.4511]
              📊 stats: min=-0.0026, max=0.8934, mean=0.2621
          📄 root_velocity  shape=(232, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.      0.0002  0.0009 -0.0001]
              📊 stats: min=-0.6465, max=1.0092, mean=0.0010
        📁 cube_2/
          📄 root_pose  shape=(232, 7)  dtype=float32
              📍 row[0]: [ 0.5869  0.0206  0.0203  0.9529 -0.     -0.      0.3032]
              📊 stats: min=-0.0393, max=0.9628, mean=0.2685
          📄 root_velocity  shape=(232, 6)  dtype=float32
              📍 row[0]: [ 0.      0.0001 -0.     -0.0011  0.0013  0.    ]
              📊 stats: min=-10.6375, max=20.9267, mean=0.1434
        📁 cube_3/
          📄 root_pose  shape=(232, 7)  dtype=float32
              📍 row[0]: [ 0.448  -0.0926  0.0203  0.9997 -0.     -0.     -0.0233]
              📊 stats: min=-0.3660, max=0.9997, mean=0.1916
          📄 root_velocity  shape=(232, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.0001 -0.0034  0.0002  0.    ]
              📊 stats: min=-20.5630, max=0.5697, mean=-1.5947
  📁 demo_5/
    📎 attr: num_samples = np.int64(185)
    📎 attr: success = np.True_
    📄 actions  shape=(185, 7)  dtype=float32
        📍 row[0]: [ 0.  0. -0.  0.  0.  0.  1.]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0180
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0348 -0.1906 -0.1079 -2.4962 -0.0058  2.3795  0.7205  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5957 -0.0628  0.0203  0.9999  0.      0.     -0.0111]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [0.4698 0.0368 0.0203 0.9919 0.     0.     0.1273]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4455 -0.092   0.0203  0.9976  0.      0.     -0.0693]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(185, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0188
      📄 cube_orientations  shape=(185, 12)  dtype=float32
          📍 row[0]: [ 0.9999  0.      0.     -0.0111  0.9919  0.      0.      0.1273  0.9976
  0.      0.     -0.0693]
          📊 stats: min=-0.1317, max=0.9999, mean=0.2601
      📄 cube_positions  shape=(185, 9)  dtype=float32
          📍 row[0]: [ 0.5957 -0.0628  0.0203  0.4698  0.0368  0.0203  0.4455 -0.092   0.0203]
          📊 stats: min=-0.0920, max=0.6064, mean=0.1801
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(185, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9973 -0.0025  0.0738  0.4635 -0.0033 -0.9999  0.0111 -0.032 ]
              📊 stats: min=-0.9999, max=1.0000, mean=0.0404
        📁 object_pose/
          📄 cube_1  shape=(185, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9998  0.0221  0.      0.5957 -0.0221  0.9998 -0.     -0.0628]
              📊 stats: min=-0.0628, max=1.0000, mean=0.2845
          📄 cube_2  shape=(185, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9676 -0.2525  0.      0.4698  0.2525  0.9676  0.      0.0368]
              📊 stats: min=-0.5715, max=1.0000, mean=0.2751
          📄 cube_3  shape=(185, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9904  0.1382  0.      0.4455 -0.1382  0.9904 -0.     -0.092 ]
              📊 stats: min=-0.2737, max=1.0000, mean=0.2763
        📁 subtask_term_signals/
          📄 grasp_1  shape=(185,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(185,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(185,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(185, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9973 -0.0025  0.0738  0.4635 -0.0033 -0.9999  0.0111 -0.032 ]
              📊 stats: min=-1.0000, max=1.0000, mean=0.0408
      📄 eef_pos  shape=(185, 3)  dtype=float32
          📍 row[0]: [ 0.4635 -0.032   0.2588]
          📊 stats: min=-0.0905, max=0.6065, mean=0.2009
      📄 eef_quat  shape=(185, 4)  dtype=float32
          📍 row[0]: [-0.0056  0.9993 -0.0015  0.0369]
          📊 stats: min=-0.0992, max=0.9993, mean=0.2348
      📄 gripper_pos  shape=(185, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0003
      📄 joint_pos  shape=(185, 9)  dtype=float32
          📍 row[0]: [-0.0096 -0.0012  0.0028  0.0186 -0.0102  0.002   0.0253  0.      0.    ]
          📊 stats: min=-0.4622, max=0.7370, mean=0.1043
      📄 joint_vel  shape=(185, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.3019, max=1.2684, mean=0.0149
      📄 object  shape=(185, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.5957 -0.0628  0.0203  0.9999  0.      0.     -0.0111  0.4698]
          📊 stats: min=-0.2386, max=0.9999, mean=0.1220
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(185, 9)  dtype=float32
              📍 row[0]: [ 0.0348 -0.1906 -0.1079 -2.4962 -0.0058  2.3795  0.7205  0.04    0.04  ]
              📊 stats: min=-2.6142, max=2.8760, mean=0.1479
          📄 joint_velocity  shape=(185, 9)  dtype=float32
              📍 row[0]: [-0.  0.  0. -0. -0.  0.  0.  0.  0.]
              📊 stats: min=-1.3019, max=1.2684, mean=0.0149
          📄 root_pose  shape=(185, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(185, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(185, 7)  dtype=float32
              📍 row[0]: [ 0.5957 -0.0628  0.0203  0.9999  0.     -0.     -0.0111]
              📊 stats: min=-0.0628, max=0.9999, mean=0.2203
          📄 root_velocity  shape=(185, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.     -0.0002 -0.      0.    ]
              📊 stats: min=-0.6240, max=0.9716, mean=-0.0002
        📁 cube_2/
          📄 root_pose  shape=(185, 7)  dtype=float32
              📍 row[0]: [ 0.4698  0.0368  0.0203  0.9919 -0.      0.      0.1273]
              📊 stats: min=-0.0642, max=0.9987, mean=0.2578
          📄 root_velocity  shape=(185, 6)  dtype=float32
              📍 row[0]: [ 0.      0.     -0.     -0.0009  0.0006  0.    ]
              📊 stats: min=-6.8365, max=6.8620, mean=-0.0476
        📁 cube_3/
          📄 root_pose  shape=(185, 7)  dtype=float32
              📍 row[0]: [ 0.4455 -0.092   0.0203  0.9976 -0.     -0.     -0.0693]
              📊 stats: min=-0.1317, max=0.9995, mean=0.1998
          📄 root_velocity  shape=(185, 6)  dtype=float32
              📍 row[0]: [ 0.0001 -0.0001 -0.0001 -0.002   0.0009 -0.0001]
              📊 stats: min=-20.8871, max=6.4928, mean=-0.9502
  📁 demo_6/
    📎 attr: num_samples = np.int64(247)
    📎 attr: success = np.True_
    📄 actions  shape=(247, 7)  dtype=float32
        📍 row[0]: [0. 0. 0. 0. 0. 0. 1.]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0280
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0514 -0.1765 -0.1372 -2.4739 -0.0014  2.3719  0.6941  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4572 -0.0538  0.0203  0.9484  0.      0.      0.3171]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5985  0.0743  0.0203  0.9289  0.      0.     -0.3703]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4914  0.092   0.0203  0.9773  0.      0.     -0.2117]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(247, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0286
      📄 cube_orientations  shape=(247, 12)  dtype=float32
          📍 row[0]: [ 0.9484  0.      0.      0.3171  0.9289  0.      0.     -0.3703  0.9773
  0.      0.     -0.2117]
          📊 stats: min=-0.5655, max=0.9851, mean=0.2106
      📄 cube_positions  shape=(247, 9)  dtype=float32
          📍 row[0]: [ 0.4572 -0.0538  0.0203  0.5985  0.0743  0.0203  0.4914  0.092   0.0203]
          📊 stats: min=-0.0687, max=0.5986, mean=0.1754
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(247, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9972  0.0083  0.0744  0.4693  0.0071 -0.9998  0.0168 -0.0377]
              📊 stats: min=-0.9999, max=1.0000, mean=-0.0228
        📁 object_pose/
          📄 cube_1  shape=(247, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.7989 -0.6015  0.      0.4572  0.6015  0.7989  0.     -0.0538]
              📊 stats: min=-0.6015, max=1.0000, mean=0.2513
          📄 cube_2  shape=(247, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.7257  0.688   0.      0.5985 -0.688   0.7257 -0.      0.0743]
              📊 stats: min=-0.8204, max=1.0000, mean=0.2433
          📄 cube_3  shape=(247, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9104  0.4137  0.      0.4914 -0.4137  0.9104 -0.      0.092 ]
              📊 stats: min=-0.9327, max=1.0000, mean=0.2638
        📁 subtask_term_signals/
          📄 grasp_1  shape=(247,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(247,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(247,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(247, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9972  0.0083  0.0744  0.4693  0.0071 -0.9998  0.0168 -0.0377]
              📊 stats: min=-0.9998, max=1.0000, mean=-0.0266
      📄 eef_pos  shape=(247, 3)  dtype=float32
          📍 row[0]: [ 0.4693 -0.0377  0.2611]
          📊 stats: min=-0.0696, max=0.6003, mean=0.2114
      📄 eef_quat  shape=(247, 4)  dtype=float32
          📍 row[0]: [-0.0083  0.9993  0.0039  0.0373]
          📊 stats: min=-0.9808, max=0.9993, mean=0.1481
      📄 gripper_pos  shape=(247, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0002
      📄 joint_pos  shape=(247, 9)  dtype=float32
          📍 row[0]: [ 0.007   0.0129 -0.0265  0.0409 -0.0058 -0.0056 -0.0011  0.      0.    ]
          📊 stats: min=-0.6247, max=0.9947, mean=0.1896
      📄 joint_vel  shape=(247, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.7791, max=1.3574, mean=0.0168
      📄 object  shape=(247, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.4572 -0.0538  0.0203  0.9484  0.      0.      0.3171  0.5985]
          📊 stats: min=-0.5655, max=0.9851, mean=0.0880
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(247, 9)  dtype=float32
              📍 row[0]: [ 0.0514 -0.1765 -0.1372 -2.4739 -0.0014  2.3719  0.6941  0.04    0.04  ]
              📊 stats: min=-2.7308, max=3.1441, mean=0.2334
          📄 joint_velocity  shape=(247, 9)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  0.  0.  0. -0. -0. -0.]
              📊 stats: min=-1.7791, max=1.3574, mean=0.0168
          📄 root_pose  shape=(247, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(247, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(247, 7)  dtype=float32
              📍 row[0]: [ 0.4572 -0.0538  0.0203  0.9484  0.     -0.      0.3171]
              📊 stats: min=-0.0540, max=0.9486, mean=0.2413
          📄 root_velocity  shape=(247, 6)  dtype=float32
              📍 row[0]: [ 0.      0.     -0.     -0.0005  0.0012  0.0001]
              📊 stats: min=-2.2075, max=1.2445, mean=0.0022
        📁 cube_2/
          📄 root_pose  shape=(247, 7)  dtype=float32
              📍 row[0]: [ 0.5985  0.0743  0.0203  0.9289 -0.     -0.     -0.3703]
              📊 stats: min=-0.4722, max=0.9331, mean=0.1580
          📄 root_velocity  shape=(247, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.      0.0011  0.0007 -0.0001]
              📊 stats: min=-21.4559, max=16.6146, mean=-0.1328
        📁 cube_3/
          📄 root_pose  shape=(247, 7)  dtype=float32
              📍 row[0]: [ 0.4914  0.092   0.0203  0.9773 -0.     -0.     -0.2117]
              📊 stats: min=-0.5655, max=0.9851, mean=0.1869
          📄 root_velocity  shape=(247, 6)  dtype=float32
              📍 row[0]: [ 0.0001 -0.0002 -0.0001  0.0037 -0.     -0.0007]
              📊 stats: min=-22.1768, max=22.7128, mean=-0.3849
  📁 demo_7/
    📎 attr: num_samples = np.int64(218)
    📎 attr: success = np.True_
    📄 actions  shape=(218, 7)  dtype=float32
        📍 row[0]: [0. 0. 0. 0. 0. 0. 1.]
        📊 stats: min=-1.0000, max=1.0000, mean=0.0024
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0598 -0.205  -0.0573 -2.5182 -0.0221  2.3837  0.6857  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5384 -0.0826  0.0203  0.9187  0.      0.      0.3949]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4334 -0.0626  0.0203  0.983   0.      0.      0.1838]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4824  0.0665  0.0203  0.9383  0.      0.     -0.3459]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(218, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=0.0018
      📄 cube_orientations  shape=(218, 12)  dtype=float32
          📍 row[0]: [ 0.9187  0.      0.      0.3949  0.983   0.      0.      0.1838  0.9383
  0.      0.     -0.3459]
          📊 stats: min=-0.4704, max=0.9830, mean=0.2607
      📄 cube_positions  shape=(218, 9)  dtype=float32
          📍 row[0]: [ 0.5384 -0.0826  0.0203  0.4334 -0.0626  0.0203  0.4824  0.0665  0.0203]
          📊 stats: min=-0.0829, max=0.5422, mean=0.1740
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(218, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9905  0.1178  0.0703  0.4578  0.1184 -0.993  -0.0033  0.0008]
              📊 stats: min=-0.9999, max=1.0000, mean=0.0251
        📁 object_pose/
          📄 cube_1  shape=(218, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.6881 -0.7257  0.      0.5384  0.7257  0.6881  0.     -0.0826]
              📊 stats: min=-0.7257, max=1.0000, mean=0.2408
          📄 cube_2  shape=(218, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9324 -0.3613  0.      0.4334  0.3613  0.9324  0.     -0.0626]
              📊 stats: min=-0.6882, max=1.0000, mean=0.2556
          📄 cube_3  shape=(218, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.7607  0.6491  0.      0.4824 -0.6491  0.7607 -0.      0.0665]
              📊 stats: min=-0.8304, max=1.0000, mean=0.2516
        📁 subtask_term_signals/
          📄 grasp_1  shape=(218,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(218,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(218,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(218, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9905  0.1178  0.0703  0.4578  0.1184 -0.993  -0.0033  0.0008]
              📊 stats: min=-0.9999, max=1.0000, mean=0.0200
      📄 eef_pos  shape=(218, 3)  dtype=float32
          📍 row[0]: [0.4578 0.0008 0.2566]
          📊 stats: min=-0.0857, max=0.5522, mean=0.1978
      📄 eef_quat  shape=(218, 4)  dtype=float32
          📍 row[0]: [0.0037 0.9976 0.0592 0.035 ]
          📊 stats: min=-0.4548, max=0.9976, mean=0.2295
      📄 gripper_pos  shape=(218, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0003
      📄 joint_pos  shape=(218, 9)  dtype=float32
          📍 row[0]: [ 0.0154 -0.0156  0.0534 -0.0034 -0.0265  0.0062 -0.0095  0.      0.    ]
          📊 stats: min=-0.8437, max=1.2230, mean=0.1054
      📄 joint_vel  shape=(218, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-0.9384, max=1.1681, mean=0.0185
      📄 object  shape=(218, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.5384 -0.0826  0.0203  0.9187  0.      0.      0.3949  0.4334]
          📊 stats: min=-0.4704, max=0.9830, mean=0.1091
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(218, 9)  dtype=float32
              📍 row[0]: [ 0.0598 -0.205  -0.0573 -2.5182 -0.0221  2.3837  0.6857  0.04    0.04  ]
              📊 stats: min=-2.6176, max=2.9424, mean=0.1492
          📄 joint_velocity  shape=(218, 9)  dtype=float32
              📍 row[0]: [ 0. -0.  0.  0. -0.  0.  0. -0. -0.]
              📊 stats: min=-0.9384, max=1.1681, mean=0.0185
          📄 root_pose  shape=(218, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(218, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(218, 7)  dtype=float32
              📍 row[0]: [ 0.5384 -0.0826  0.0203  0.9187  0.     -0.      0.3949]
              📊 stats: min=-0.0829, max=0.9194, mean=0.2557
          📄 root_velocity  shape=(218, 6)  dtype=float32
              📍 row[0]: [ 0.      0.     -0.     -0.0001  0.0011 -0.    ]
              📊 stats: min=-0.2374, max=0.2136, mean=0.0015
        📁 cube_2/
          📄 root_pose  shape=(218, 7)  dtype=float32
              📍 row[0]: [ 0.4334 -0.0626  0.0203  0.983   0.     -0.      0.1838]
              📊 stats: min=-0.0829, max=0.9830, mean=0.2512
          📄 root_velocity  shape=(218, 6)  dtype=float32
              📍 row[0]: [ 0.      0.0001 -0.     -0.0012  0.0012 -0.    ]
              📊 stats: min=-3.0980, max=0.7083, mean=-0.0828
        📁 cube_3/
          📄 root_pose  shape=(218, 7)  dtype=float32
              📍 row[0]: [ 0.4824  0.0665  0.0203  0.9383 -0.     -0.     -0.3459]
              📊 stats: min=-0.4704, max=0.9419, mean=0.1639
          📄 root_velocity  shape=(218, 6)  dtype=float32
              📍 row[0]: [ 0.0001 -0.0002 -0.      0.0042  0.0017 -0.0004]
              📊 stats: min=-15.0526, max=20.8388, mean=0.1548
  📁 demo_8/
    📎 attr: num_samples = np.int64(230)
    📎 attr: success = np.True_
    📄 actions  shape=(230, 7)  dtype=float32
        📍 row[0]: [0. 0. 0. 0. 0. 0. 1.]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0175
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0637 -0.1707 -0.0954 -2.4832  0.0156  2.4151  0.7244  0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5561  0.024   0.0203  0.9842  0.      0.     -0.1772]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4164 -0.033   0.0203  0.8977  0.      0.      0.4407]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5679 -0.0979  0.0203  0.89    0.      0.     -0.456 ]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(230, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0181
      📄 cube_orientations  shape=(230, 12)  dtype=float32
          📍 row[0]: [ 0.9842  0.      0.     -0.1772  0.8977  0.      0.      0.4407  0.89
  0.      0.     -0.456 ]
          📊 stats: min=-0.7971, max=0.9842, mean=0.2017
      📄 cube_positions  shape=(230, 9)  dtype=float32
          📍 row[0]: [ 0.5561  0.024   0.0203  0.4164 -0.033   0.0203  0.5679 -0.0979  0.0203]
          📊 stats: min=-0.0989, max=0.5898, mean=0.1970
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(230, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9945  0.0198  0.1025  0.4754  0.0175 -0.9996  0.0233 -0.0121]
              📊 stats: min=-0.9997, max=1.0000, mean=0.0396
        📁 object_pose/
          📄 cube_1  shape=(230, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9372  0.3488  0.      0.5561 -0.3488  0.9372 -0.      0.024 ]
              📊 stats: min=-0.3495, max=1.0000, mean=0.2796
          📄 cube_2  shape=(230, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.6116 -0.7912  0.      0.4164  0.7912  0.6116  0.     -0.033 ]
              📊 stats: min=-0.9524, max=1.0000, mean=0.2113
          📄 cube_3  shape=(230, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.5842  0.8116  0.      0.5679 -0.8116  0.5842 -0.     -0.0979]
              📊 stats: min=-0.9938, max=1.0000, mean=0.2051
        📁 subtask_term_signals/
          📄 grasp_1  shape=(230,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(230,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(230,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(230, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9945  0.0198  0.1025  0.4754  0.0175 -0.9996  0.0233 -0.0121]
              📊 stats: min=-0.9996, max=1.0000, mean=0.0373
      📄 eef_pos  shape=(230, 3)  dtype=float32
          📍 row[0]: [ 0.4754 -0.0121  0.2592]
          📊 stats: min=-0.1093, max=0.5817, mean=0.2115
      📄 eef_quat  shape=(230, 4)  dtype=float32
          📍 row[0]: [-0.0112  0.9986  0.0093  0.0514]
          📊 stats: min=-0.9369, max=0.9986, mean=0.2257
      📄 gripper_pos  shape=(230, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0003
      📄 joint_pos  shape=(230, 9)  dtype=float32
          📍 row[0]: [0.0193 0.0187 0.0153 0.0316 0.0112 0.0376 0.0292 0.     0.    ]
          📊 stats: min=-1.0565, max=0.9847, mean=0.1239
      📄 joint_vel  shape=(230, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-2.6084, max=2.6100, mean=0.0172
      📄 object  shape=(230, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.5561  0.024   0.0203  0.9842  0.      0.     -0.1772  0.4164]
          📊 stats: min=-0.7971, max=0.9842, mean=0.1052
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(230, 9)  dtype=float32
              📍 row[0]: [ 0.0637 -0.1707 -0.0954 -2.4832  0.0156  2.4151  0.7244  0.04    0.04  ]
              📊 stats: min=-2.7530, max=3.2463, mean=0.1675
          📄 joint_velocity  shape=(230, 9)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  0.  0.  0. -0. -0.  0.]
              📊 stats: min=-2.6084, max=2.6100, mean=0.0172
          📄 root_pose  shape=(230, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(230, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(230, 7)  dtype=float32
              📍 row[0]: [ 0.5561  0.024   0.0203  0.9842 -0.     -0.     -0.1772]
              📊 stats: min=-0.1776, max=0.9842, mean=0.2012
          📄 root_velocity  shape=(230, 6)  dtype=float32
              📍 row[0]: [-0.     -0.     -0.      0.0006 -0.0006 -0.    ]
              📊 stats: min=-1.8148, max=0.5145, mean=-0.0014
        📁 cube_2/
          📄 root_pose  shape=(230, 7)  dtype=float32
              📍 row[0]: [ 0.4164 -0.033   0.0203  0.8977 -0.      0.      0.4407]
              📊 stats: min=-0.0418, max=0.9252, mean=0.2814
          📄 root_velocity  shape=(230, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.     -0.0001  0.0008 -0.0001]
              📊 stats: min=-21.6549, max=13.0099, mean=-0.4287
        📁 cube_3/
          📄 root_pose  shape=(230, 7)  dtype=float32
              📍 row[0]: [ 0.5679 -0.0979  0.0203  0.89   -0.     -0.     -0.456 ]
              📊 stats: min=-0.7971, max=0.8900, mean=0.1164
          📄 root_velocity  shape=(230, 6)  dtype=float32
              📍 row[0]: [ 0.0003 -0.0003 -0.0001  0.0075  0.0052  0.0003]
              📊 stats: min=-7.9993, max=1.6479, mean=-0.4322
  📁 demo_9/
    📎 attr: num_samples = np.int64(179)
    📎 attr: success = np.True_
    📄 actions  shape=(179, 7)  dtype=float32
        📍 row[0]: [ 0.      0.     -0.      0.     -0.0014  0.      1.    ]
        📊 stats: min=-1.0000, max=1.0000, mean=-0.0142
    📁 initial_state/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(1, 9)  dtype=float32
              📍 row[0]: [ 0.0607 -0.1806 -0.1247 -2.5103 -0.0021  2.397   0.675   0.04    0.04  ]
          📄 joint_velocity  shape=(1, 9)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4835 -0.0648  0.0203  0.8946  0.      0.     -0.4468]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_2/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.4257  0.0286  0.0203  0.9956  0.      0.     -0.0932]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
        📁 cube_3/
          📄 root_pose  shape=(1, 7)  dtype=float32
              📍 row[0]: [ 0.5676 -0.0038  0.0203  0.9619  0.      0.      0.2736]
          📄 root_velocity  shape=(1, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
    📁 obs/
      📄 actions  shape=(179, 7)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.0000, max=1.0000, mean=-0.0150
      📄 cube_orientations  shape=(179, 12)  dtype=float32
          📍 row[0]: [ 0.8946  0.      0.     -0.4468  0.9956  0.      0.     -0.0932  0.9619
  0.      0.      0.2736]
          📊 stats: min=-0.4468, max=0.9998, mean=0.2335
      📄 cube_positions  shape=(179, 9)  dtype=float32
          📍 row[0]: [ 0.4835 -0.0648  0.0203  0.4257  0.0286  0.0203  0.5676 -0.0038  0.0203]
          📊 stats: min=-0.0681, max=0.5867, mean=0.1694
      📁 datagen_info/
        📁 eef_pose/
          📄 franka  shape=(179, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9965  0.0497  0.067   0.4608  0.0486 -0.9987  0.0167 -0.0269]
              📊 stats: min=-1.0000, max=1.0000, mean=0.0804
        📁 object_pose/
          📄 cube_1  shape=(179, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.6008  0.7994  0.      0.4835 -0.7994  0.6008 -0.     -0.0648]
              📊 stats: min=-0.7994, max=1.0000, mean=0.2275
          📄 cube_2  shape=(179, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9826  0.1855  0.      0.4257 -0.1855  0.9826 -0.      0.0286]
              📊 stats: min=-0.6134, max=1.0000, mean=0.2644
          📄 cube_3  shape=(179, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.8503 -0.5262  0.      0.5676  0.5262  0.8503  0.     -0.0038]
              📊 stats: min=-0.5998, max=1.0000, mean=0.2660
        📁 subtask_term_signals/
          📄 grasp_1  shape=(179,)  dtype=bool
              📍 samples: [False False False]
          📄 grasp_2  shape=(179,)  dtype=bool
              📍 samples: [False False False]
          📄 stack_1  shape=(179,)  dtype=bool
              📍 samples: [False False False]
        📁 target_eef_pose/
          📄 franka  shape=(179, 4, 4)  dtype=float32
              📍 row[0]: shape=(4, 4), first 8 vals: [ 0.9964  0.0497  0.0684  0.4608  0.0486 -0.9987  0.0167 -0.0269]
              📊 stats: min=-1.0000, max=1.0000, mean=0.0833
      📄 eef_pos  shape=(179, 3)  dtype=float32
          📍 row[0]: [ 0.4608 -0.0269  0.2497]
          📊 stats: min=-0.0710, max=0.5802, mean=0.1905
      📄 eef_quat  shape=(179, 4)  dtype=float32
          📍 row[0]: [-0.0075  0.9991  0.0246  0.0337]
          📊 stats: min=-0.1090, max=0.9997, mean=0.2892
      📄 gripper_pos  shape=(179, 2)  dtype=float32
          📍 row[0]: [ 0.04 -0.04]
          📊 stats: min=-0.0400, max=0.0400, mean=0.0003
      📄 joint_pos  shape=(179, 9)  dtype=float32
          📍 row[0]: [ 0.0163  0.0088 -0.014   0.0045 -0.0065  0.0195 -0.0202  0.      0.    ]
          📊 stats: min=-0.8659, max=0.7735, mean=0.0420
      📄 joint_vel  shape=(179, 9)  dtype=float32
          📍 row[0]: [0. 0. 0. 0. 0. 0. 0. 0. 0.]
          📊 stats: min=-1.1465, max=1.0029, mean=0.0017
      📄 object  shape=(179, 39)  dtype=float32
          📍 row[0]: shape=(39,), first 8 vals: [ 0.4835 -0.0648  0.0203  0.8946  0.      0.     -0.4468  0.4257]
          📊 stats: min=-0.4468, max=0.9998, mean=0.0986
    📁 states/
      📁 articulation/
        📁 robot/
          📄 joint_position  shape=(179, 9)  dtype=float32
              📍 row[0]: [ 0.0607 -0.1806 -0.1247 -2.5104 -0.0021  2.3972  0.6749  0.04    0.04  ]
              📊 stats: min=-2.6343, max=2.8462, mean=0.0850
          📄 joint_velocity  shape=(179, 9)  dtype=float32
              📍 row[0]: [ 0.0001  0.     -0.     -0.0008  0.0002  0.0036 -0.0002  0.     -0.    ]
              📊 stats: min=-1.1465, max=1.0029, mean=0.0017
          📄 root_pose  shape=(179, 7)  dtype=float32
              📍 row[0]: [ 0.  0. -0.  1. -0. -0. -0.]
              📊 stats: min=-0.0000, max=1.0000, mean=0.1429
          📄 root_velocity  shape=(179, 6)  dtype=float32
              📍 row[0]: [0. 0. 0. 0. 0. 0.]
              📊 stats: min=0.0000, max=0.0000, mean=0.0000
      📁 rigid_object/
        📁 cube_1/
          📄 root_pose  shape=(179, 7)  dtype=float32
              📍 row[0]: [ 0.4835 -0.0648  0.0203  0.8946 -0.     -0.     -0.4468]
              📊 stats: min=-0.4468, max=0.8946, mean=0.1267
          📄 root_velocity  shape=(179, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.      0.0012  0.0005  0.0001]
              📊 stats: min=-1.1103, max=0.6846, mean=-0.0005
        📁 cube_2/
          📄 root_pose  shape=(179, 7)  dtype=float32
              📍 row[0]: [ 0.4257  0.0286  0.0203  0.9956 -0.     -0.     -0.0932]
              📊 stats: min=-0.1060, max=0.9998, mean=0.2349
          📄 root_velocity  shape=(179, 6)  dtype=float32
              📍 row[0]: [ 0.     -0.     -0.     -0.0003  0.     -0.    ]
              📊 stats: min=-5.0245, max=6.5802, mean=-0.2979
        📁 cube_3/
          📄 root_pose  shape=(179, 7)  dtype=float32
              📍 row[0]: [ 0.5676 -0.0038  0.0203  0.9619 -0.     -0.      0.2736]
              📊 stats: min=-0.0991, max=0.9767, mean=0.2568
          📄 root_velocity  shape=(179, 6)  dtype=float32
              📍 row[0]: [ 0.0002  0.0002 -0.     -0.0039  0.0042  0.0001]
              📊 stats: min=-20.7391, max=12.4189, mean=-0.2873


------------------------------------------------------------------------
  Episode Summary
------------------------------------------------------------------------
  Total episodes (from attr 'total'):     2163
  Total episode groups found:             10

  Key          #samples   Actions shape        Success?
  ------------ ---------- -------------------- ----------
  demo_0       236        (236, 7)             True
  demo_1       233        (233, 7)             True
  demo_2       194        (194, 7)             True
  demo_3       209        (209, 7)             True
  demo_4       232        (232, 7)             True
  demo_5       185        (185, 7)             True
  demo_6       247        (247, 7)             True
  demo_7       218        (218, 7)             True
  demo_8       230        (230, 7)             True
  demo_9       179        (179, 7)             True


------------------------------------------------------------------------
  Cross-Episode Key Comparison
------------------------------------------------------------------------

  Field                         demo_0      demo_1      demo_2      demo_3      demo_4      demo_5      demo_6      demo_7      demo_8      demo_9
  ------------------------------------------------------------------------------------------------------------------------------------------------------
  actions                       ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/                ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/articulation/   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/articulation/robot/✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/articulation/robot/joint_position✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/articulation/robot/joint_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/articulation/robot/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/articulation/robot/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_1/✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_1/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_1/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_2/✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_2/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_2/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_3/✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_3/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  initial_state/rigid_object/cube_3/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/                          ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/actions                   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/cube_orientations         ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/cube_positions            ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/             ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/eef_pose/    ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/eef_pose/franka✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/object_pose/ ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/object_pose/cube_1✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/object_pose/cube_2✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/object_pose/cube_3✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/subtask_term_signals/✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/subtask_term_signals/grasp_1✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/subtask_term_signals/grasp_2✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/subtask_term_signals/stack_1✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/target_eef_pose/✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/datagen_info/target_eef_pose/franka✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/eef_pos                   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/eef_quat                  ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/gripper_pos               ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/joint_pos                 ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/joint_vel                 ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  obs/object                    ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/                       ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/articulation/          ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/articulation/robot/    ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/articulation/robot/joint_position✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/articulation/robot/joint_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/articulation/robot/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/articulation/robot/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/          ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_1/   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_1/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_1/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_2/   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_2/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_2/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_3/   ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_3/root_pose✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅
  states/rigid_object/cube_3/root_velocity✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅           ✅


------------------------------------------------------------------------
  Subtask / Annotation Information (Mimic)
------------------------------------------------------------------------
  Found 'subtask' in demo_0:
    📁 obs/datagen_info/subtask_term_signals/
    📄 obs/datagen_info/subtask_term_signals/grasp_1  shape=(236,)  dtype=bool
       value = [False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False]
    📄 obs/datagen_info/subtask_term_signals/grasp_2  shape=(236,)  dtype=bool
       value = [False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True False False False False False
 False False False False False False False False]
    📄 obs/datagen_info/subtask_term_signals/stack_1  shape=(236,)  dtype=bool
       value = [False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False False
 False False False False False False False False False False False  True
  True  True  True  True  True  True  True  True]


========================================================================
  End of Report
========================================================================
```


* 수행하는 분석:

| 항목	| 설명 | 
|:--------:|:--------:|
| Full HDF5 Structure	| 전체 트리 구조를 재귀적으로 출력 (group/dataset, shape, dtype, attrs) | 
| Episode Summary	| 모든 episode의 프레임 수, actions shape, success 여부를 테이블로 요약 | 
| Cross-Episode Key Comparison	| episode 간 공통/상이한 key 필드를 매트릭스로 비교 | 
| Subtask Annotation Search	| subtask, segment, boundary, phase 등 Mimic annotation 키 탐색 | 

**2. Jupyter Notebook: inspect_hdf5.ipynb**

* 셀별로 나누어 단계적으로 실행:
   * 셀 1: 전체 트리 구조 한눈에 보기
   * 셀 2: 메타 정보 (총 episode 수, env_args)
   * 셀 3: Episode 요약 테이블 (프레임 수, actions/states shape, success)
   * 셀 4: 특정 episode (demo_0)의 상세 필드와 샘플 값 확인
   * 셀 5: 모든 episode에 공통/가변적인 key 분석
   * 셀 6: Subtask annotation 정보 찾기

* 예상되는 HDF5 구조 (Isaac Lab Mimic)

```
/data
 ├── attrs: total=N, env_args={...}
 ├── demo_0/
 │   ├── attrs: num_samples=T, success=True
 │   ├── actions       (T × action_dim)
 │   ├── states        (T × state_dim)  
 │   └── obs/
 │       ├── joint_pos (T × 7)     # Franka 7-DOF joint positions
 │       ├── joint_vel (T × 7)     # joint velocities
 │       └── ... (카메라 RGB, depth 등)
 ├── demo_1/
 └── ...
```

* Isaac Lab은 robomimic 호환 HDF5 포맷을 사용합니다.
* 각 episode는 demo_0, demo_1, ... 형식의 그룹으로 저장되며, actions, states, obs/ 하위의 관측값들이 T × dim shape의 데이터셋으로 들어갑니다.
* Subtask 경계 정보는 episode의 attributes나 별도 데이터셋에 저장될 수 있습니다.


---

### Stage

A **Stage** is the composited result of layers — the current screen output.

- **Layer**: Typically a single `.usd` file
- **Composition**: The combination of multiple layers
- Reference: [USD Fundamentals](https://docs.omniverse.nvidia.com/usd/latest/guide/usd-fundamentals.html)
- https://docs.nvidia.com/learn-openusd/latest/stage-setting/index.html

### Scene Graph Structure

The Stage provides a hierarchical **scene graph** that describes what exists in the scene.

#### Stage - Basic Setup

```python
# usdview basic settings
stage = usdviewApi.stage
stage.SetEditTarget(stage.GetRootLayer())
stage.RemovePrim('/hello')
stage.ClearDefaultPrim()
stage.Save()
```

```python
stage.DefinePrim("/World", "Xform")
# Print the stage as a string
print(stage.ExportToString(addSourceFileComment=False))
```

### Prims

A **Prim (Primitive)** is a container for data, attributes, and relationships of scene objects.

- **Unique Path**: Distinguishes each Prim (e.g., `/World/Environment`)
- **Imageable / Non-Imageable**

```python
# Import the Sdf class
from pxr import Sdf

# Return the path of a Usd.Prim as an Sdf.Path object
Usd.Prim.GetPath()

# Retrieve a Usd.Prim at the specified path from the Stage
Usd.Stage.GetPrimAtPath()
```

#### Prim - Define & Remove

```python
from pxr import Usd

# Define a new primitive at path "/hello"
stage.DefinePrim("/hello")

# Define a new Sphere primitive at "/world"
stage.DefinePrim("/world", "Sphere")
```

#### GPrim Types

| GPrim | Description |
|---|---|
| `Cube` | Cube / Box |
| `Sphere` | Sphere |
| `Cylinder` | Cylinder |
| `Capsule` | Pill-shaped |
| `Cone` | Cone |

#### Prim - Typed API

```python
from pxr import UsdGeom

# Define a Sphere at "/hello"
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Define(stage, "/hello")
sphere.CreateRadiusAttr().Set(2)

# Remove a prim
stage.RemovePrim("/hello")
```

#### Prim - Hierarchy with Scope & Xform

```python
# Define a Scope at /Geometry
geom_scope: UsdGeom.Scope = UsdGeom.Scope.Define(stage, "/Geometry")

# Define an Xform as a child of /Geometry
xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage,
    geom_scope.GetPath().AppendPath("GroupTransform"))

# Define a Cube as a child of /Geometry/GroupTransform
cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage,
    xform.GetPath().AppendPath("Box"))
```

#### Prim - Child Access

```python
prim: Usd.Prim = stage.GetPrimAtPath("/Geometry")
child_prim: Usd.Prim

if child_prim := prim.GetChild("Box"):
    print("Child prim exists")
else:
    print("Child prim DOES NOT exist")
```

### Attributes

**Attributes** are name-value properties with specific data types.

```python
# Get property names of a Prim
prop_names = prim.GetPropertyNames()

# Get/Set attributes on a UsdGeom.Sphere
sphere_prim.GetRadiusAttr().Get()
sphere_prim.GetDoubleSidedAttr().Set(True)
```

#### Attributes - Transform Example

```python
from pxr import Usd, UsdGeom, Gf

world_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/World")
sphere = UsdGeom.Sphere.Define(stage,
    world_xform.GetPath().AppendPath("Sphere"))

cube: UsdGeom.Cube = UsdGeom.Cube.Define(stage,
    world_xform.GetPath().AppendPath("Cube"))
UsdGeom.XformCommonAPI(cube).SetTranslate(Gf.Vec3d(5, 0, 0))
```

#### Attributes - Listing Properties

```python
# Get the property names
cube_prop_names = cube.GetPrim().GetPropertyNames()
for prop_name in cube_prop_names:
    print(prop_name)
```

#### Attributes - Getting Attributes

```python
cube_attrs = cube.GetPrim().GetAttributes()
for attr in cube_attrs:
    print(attr)

cube_size = cube.GetSizeAttr()
cube_displaycolor = cube.GetDisplayColorAttr()
cube_extent = cube.GetExtentAttr()

print(f"Size: {cube_size.Get()}")
print(f"Display Color: {cube_displaycolor.Get()}")
print(f"Extent: {cube_extent.Get()}")
```

#### Attributes - Modifying Values

```python
cube_size.Set(cube_size.Get() * 2)
cube_extent.Set(cube_extent.Get() * 2)
cube_displaycolor.Set([(0.0, 1.0, 0.0)])
```

### Relationship

**Relationships** are USD Properties containing `SdfPath` links.

- Define relationships between objects
- Used for **Reference**, etc.

```python
# Adding References in Isaac Sim
# https://docs.isaacsim.omniverse.nvidia.com/latest/py/source/extensions/isaacsim.core.utils/docs/index.html#module-isaacsim.core.utils.stage
```

### TimeCodes and TimeSamples

Time-based animation storage mechanism.

- Isaac Sim uses PhysX for physics simulation, but specific animations may still be needed
- **Linear interpolation** is automatically applied when working with code
- Non-linear results should be handled in DCC tools

https://dpel.aswf.io/alab-trailer/

#### TimeCodes - Basic Setup

```python
cube_xform_api = UsdGeom.XformCommonAPI(cube)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)
```

#### TimeCodes - Keyframes

```python
sphere: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Sphere")
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)

sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)
```

* example 1
```
cube_xform_api = UsdGeom.XformCommonAPI(cube)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)


sphere: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Sphere")
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)
# Set translation of the sphere at time 1
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)
# Set translation of the sphere at time 30
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)
# Set translation of the sphere at time 45
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)
# Set translation of the sphere at time 50
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)
# Set translation of the sphere at time 60
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)
```

[동영상 보기](TimeCodes_and_TimeSamples.mp4)
![](TimeCodes_and_TimeSamples.mp4)
<video src="TimeCodes_and_TimeSamples.mp4" controls width="640"></video>
[![](thumbnail.png)](TimeCodes_and_TimeSamples.mp4)



* example 2
```
cube_xform_api = UsdGeom.XformCommonAPI(cube)
cube_xform_api.SetScale(Gf.Vec3f(5, 5, 0.1))
cube_xform_api.SetTranslate(Gf.Vec3d(0, 0, -2))

stage.SetStartTimeCode(1)
stage.SetEndTimeCode(60)


sphere: UsdGeom.Sphere = UsdGeom.Sphere.Get(stage, "/World/Sphere")
sphere_xform_api = UsdGeom.XformCommonAPI(sphere)
sphere_color_attr = sphere.GetDisplayColorAttr()

import random
random.seed(42)


def _y_to_color(y):
    t = max(0.0, min(1.0, (y + 5.0) / 10.5))
    if t < 0.5:
        u = t / 0.5
        r, g, b = 0.0, u, 1.0 - u
    else:
        u = (t - 0.5) / 0.5
        r, g, b = u, 1.0 - u, 0.0
    return Gf.Vec3f(r, g, b)


# Set translation of the sphere at time 1
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=1)
sphere_color_attr.Set(_y_to_color(5.50), time=1)
# Set translation of the sphere at time 30
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -4.50, 0), time=30)
sphere_color_attr.Set(_y_to_color(-4.50), time=30)
# Set translation of the sphere at time 45
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -5.00, 0), time=45)
sphere_color_attr.Set(_y_to_color(-5.00), time=45)
# Set translation of the sphere at time 50
sphere_xform_api.SetTranslate(Gf.Vec3d(0, -3.25, 0), time=50)
sphere_color_attr.Set(_y_to_color(-3.25), time=50)
# Set translation of the sphere at time 60
sphere_xform_api.SetTranslate(Gf.Vec3d(0,  5.50, 0), time=60)
sphere_color_attr.Set(_y_to_color(5.50), time=60)


# Random cube scale at each frame
for _t in range(1, 61):
    cube_xform_api.SetScale(Gf.Vec3f(
        random.uniform(3.0, 7.0),
        random.uniform(3.0, 7.0),
        random.uniform(0.05, 0.3)
    ), time=_t)
```

---

* 내부의 기능을 확인할때
```
print(sphere_xform_api.__dir__()) 
또는
print(dir(sphere_xform_api))
```

```
>>> print(sphere_xform_api.__dir__())
['__module__', '__doc__', '__reduce__', '__instance_size__', 'RotationOrder', 'RotationOrderXYZ', 'RotationOrderXZY', 'RotationOrderYXZ', 'RotationOrderYZX', 'RotationOrderZXY', 'RotationOrderZYX', 'OpFlags', 'OpTranslate', 'OpRotate', 'OpScale', 'OpPivot', '__init__', 'Get', 'GetSchemaAttributeNames', '_GetStaticTfType', '__bool__', '__repr__', 'SetXformVectors', 'GetXformVectors', 'GetXformVectorsByAccumulation', 'SetTranslate', 'SetPivot', 'SetRotate', 'SetScale', 'GetResetXformStack', 'SetResetXformStack', 'CreateXformOps', 'GetRotationTransform', 'ConvertRotationOrderToOpType', 'ConvertOpTypeToRotationOrder', 'CanConvertOpTypeToRotationOrder', 'GetPrim', 'GetPath', 'GetSchemaClassPrimDefinition', 'IsAPISchema', 'IsConcrete', 'IsTyped', 'IsAppliedAPISchema', 'IsMultipleApplyAPISchema', 'GetSchemaKind', '__getattribute__', '__new__', '__weakref__', '__dict__', '__hash__', '__str__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__reduce_ex__', '__getstate__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
>>> 
```

### Scope

**Scope** groups prims for organized material application, etc.

```
Materials
├── Plastic
│   ├── Cable
│   ├── Plastic Part 1
│   └── Plastic Part 2
└── Metal
    ├── Metal Part 1
    └── ...
```

### Xform

**Xform** represents **spatial transformations**:

- **Translation**
- **Rotation** (Euler or Quaternion — conversion may be needed depending on context)
- **Scale**

> Parent transforms affect child transforms.

### Metadata

Metadata refers to global information excluding Attributes and Relationships.

- Typically time-invariant values
- Can be time-varying if needed
- Representative metadata: `set active`, `interpolation`

### Lighting

USD lighting is managed under the `UsdLux` domain.

| Light Type | Description |
|---|---|
| `DistantLight` | Directional light |
| `CylinderLight` | Cylindrical area light |
| `RectLight` | Rectangular area light |
| `DiskLight` | Disk-shaped area light |
| `SphereLight` | Spherical area light |
| `DomeLight` | Environment / dome light |
| `PortalLight` | Light portal |

### Modules

Key Python modules for OpenUSD development:

| Module | Purpose |
|---|---|
| `Usd` | Core USD scene description |
| `Sdf` | Scene Description Format (scene graph, paths, layers) |
| `Gf` | Graphics Foundation (math types: vectors, matrices, etc.) |

> See: [Modules — Omniverse Kit](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/)

### Primvars

**Primvars** enable hierarchical object data manipulation and management in complex 3D scenes.

- In Isaac Sim, primvars are typically related to rendering properties such as:
  - Display color
  - Interpolation

### File Formats

| Format | Description |
|---|---|
| `.usdc` | Compressed binary — lightweight, faster loading |
| `.usda` | ASCII text — human-readable, easily overwritten |
| `.usd` | Either `.usda` or `.usdc` (mostly `.usdc`) |
| `.usdz` | Zipped archive for delivery — may contain online asset references that need local replacement |

---

## Composition

A Stage is rendered by compositing multiple layers of **"opinions"**.

The compositing technique is called the **Composition Arc**, and the order determines which opinions are strongest:

### LIVRPS

| Order | Arc | Description |
|---|---|---|
| **L** | **L**ook | Reference to a material look |
| **I** | **I**nherits | Class inheritance |
| **V** | **V**ariantSets | Variant selection |
| **R** | **R**eferences | External file reference |
| **P** | **P**ayloads | Deferred loading reference |
| **S** | **S**pecializes | Specialization override |

> **LIVRPS** Reference: [What Is LIVERPS? — Learn OpenUSD](https://openusd.org/release/glossary.html#liverps)
>
> In Isaac Sim, **L** and **I** are rarely used; most components are loaded via **R** and **P**.

### Key Composition Concepts

#### Interoperability

OpenUSD provides standardized C++ and Python libraries for data representation and is compatible with various DCC (Digital Content Creation) tools.

- One 3D scene can be split across multiple files and recombined
- Facilitates collaboration

#### Non-Destructive Editing

Original data is preserved through the Composition approach:

- Layer-based modification overrides
- Separate workspaces during collaboration

#### Extensibility

Standard USD can be extended with custom schemas and plugins:

- RTX Renderer
- USD Physics (Omniverse PhysX integration)

#### Modularity & Scalability

- Each `.usd` file can be developed independently (non-destructive)
- Stage-level management of `.usd` files keeps large scenes manageable

#### Interactive vs Static State

USD fundamentally stores **static "state"** at specific points in time.

- Interactive/runtime values are **not** stored in USD
- Memory-efficient for complex scene representation
- Applications like **Isaac Sim** handle runtime interaction

---

## Capturing Objects

Use applications like **KIRI Engine** or **Reality Composer** to capture simple objects with a smartphone.

1. Capture an object directly
2. Load the captured object (unlimited `.usdz` file)

> If the captured file is not clearly visible, adjust the **FOV**:
>
> **Camera > Free Camera Settings... > Fov value** (lower it)

---

<img src="ChatGPT Image 2026년 5월 19일 오전 09_45_07.png">

<img src="010.png">

* NVIDIA 로봇 생태계 전체 구조를 5개 레이어로 정리했습니다. 각 카드는 클릭하면 해당 주제를 더 깊이 파고들 수 있습니다.

* 핵심 구조 요약:
   * Omniverse — 모든 것의 공통 기반. OpenUSD 기반 3D 시뮬레이션 플랫폼으로 Isaac Sim, Cosmos, 디지털트윈이 여기서 돌아갑니다.
   * AI 파운데이션 레이어 — GR00T N1.7 (VLA 모델, Apache 2.0), Cosmos WFM (합성 데이터), GR00T-Dreams/Mimic (데이터 파이프라인).
   * 시뮬레이션 레이어 — Isaac Sim (물리 정확 시뮬레이터), Isaac Lab (RL 학습 프레임워크), Newton Engine (Google DeepMind 공동개발 물리 엔진), Isaac ROS (CUDA 가속 ROS 2).
   * 하드웨어 3대 컴퓨터 — DGX (훈련), OVX (시뮬레이션), Jetson AGX Thor (온로봇, Blackwell 기반, 2070 FP4 TFLOPS).
   * 파트너 생태계 — Boston Dynamics, Figure AI, Agility Robotics, 현대차그룹 등 2백만 이상 개발자와 150개 이상 파트너사.

---



## Additional Resources

- [Kitchen Set — Universal Scene Description 26.05 documentation](https://openusd.org/release/tut_kitchen_set.html)
- [City Set — Universal Scene Description 26.05 documentation](https://openusd.org/release/tut_city_set.html)
- [UsdSkel Examples — Universal Scene Description 26.05 documentation](https://openusd.org/release/tut_usdskel_examples.html)
