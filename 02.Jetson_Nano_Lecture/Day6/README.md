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

* 수행하는 분석:

| 항목	설명
| Full HDF5 Structure	전체 트리 구조를 재귀적으로 출력 (group/dataset, shape, dtype, attrs)
| Episode Summary	모든 episode의 프레임 수, actions shape, success 여부를 테이블로 요약
| Cross-Episode Key Comparison	episode 간 공통/상이한 key 필드를 매트릭스로 비교
| Subtask Annotation Search	subtask, segment, boundary, phase 등 Mimic annotation 키 탐색

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
