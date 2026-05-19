# Synthetic Manipulation Motion Generation for Robotics

> **NVIDIA Isaac GR00T Blueprint 기반 프로젝트: 소수의 인간 시연으로 로봇 조작을 위한 대규모 합성 모션 궤적 생성**

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [원본 Blueprint 이해](#2-원본-blueprint-이해)
3. [데이터셋 구조 분석 (annotated_dataset.hdf5)](#3-데이터셋-구조-분석)
4. [파일 저장 위치](#4-파일-저장-위치)
5. [하드웨어 요구사항](#5-하드웨어-요구사항)
6. [커스텀 프로젝트: 웹캠 기반 데이터 생성 파이프라인](#6-커스텀-프로젝트)
7. [구현 로드맵](#7-구현-로드맵)
8. [참고 자료](#8-참고-자료)

---

## 1. 프로젝트 개요

### 1.1 배경

모방 학습(Imitation Learning)은 에이전트가 전문가의 행동을 모방하여 학습하는 머신러닝 기법이다. 강건한 에이전트를 훈련하려면 대량의 데이터가 필요하지만, 인간 시연을 통한 수동 데이터 수집은 시간과 비용이 많이 소요된다.

**Isaac Lab Mimic**은 Isaac Lab에 포함된 기능으로, 소수의 인간 시연만으로 새로운 궤적을 합성하여 대규모 데이터셋을 생성할 수 있게 해준다.

### 1.2 워크플로우

```
[소수 인간 시연] ──→ Isaac Lab Mimic ──→ [합성 궤적] ──→ Cosmos ──→ [시각 증강 데이터]
     (5-10개)         (궤적 합성)         (780K개)       (시각 변환)    (학습용 데이터)
```

### 1.3 핵심 기술

| 구성요소 | 역할 |
|---|---|
| **NVIDIA Omniverse / Isaac Sim** | 물리 시뮬레이션 및 렌더링 |
| **Isaac Lab** | 로봇 학습 프레임워크 (오픈소스) |
| **Isaac Lab Mimic** | 소수 시연 → 대량 궤적 합성 |
| **NVIDIA Cosmos** | 시각적 증강 (텍스트-투-월드) |

---

## 2. 원본 Blueprint 이해

### 2.1 저장소

- **GitHub**: https://github.com/NVIDIA-Omniverse-blueprints/synthetic-manipulation-motion-generation
- **컨테이너 이미지**: `nvcr.io/nvidia/gr00t-smmg-bp:1.0`
- **사전 설치**: Isaac Lab 2.0.2, Isaac Sim 4.5.0

### 2.2 디렉토리 구조

```
synthetic-manipulation-motion-generation/
├── docker-compose.yml
├── launch.sh
├── README.md
├── samples/
│   └── annotated_dataset.hdf5       # 샘플 입력 데이터 (2.5MB)
└── notebook/
    ├── generate_dataset.ipynb        # 메인 노트북
    ├── notebook_utils.py             # 유틸리티 (ISAACLAB_OUTPUT_DIR 등)
    ├── notebook_widgets.py           # 위젯
    ├── cosmos_request.py             # Cosmos API 요청
    ├── app.py                        # Cosmos 웹 API
    └── stacking_prompt.toml          # Cosmos 프롬프트 설정
```

### 2.3 실행 흐름 (generate_dataset.ipynb)

```
1. 설정 초기화
   └── num_envs, generation_num_trials, input/output 파일 경로

2. 시뮬레이션 환경 스핀업
   └── Franka 큐브 쌓기 태스크 (Isaac-Stack-Cube-Franka-IK-Rel-Blueprint-Mimic-v0)

3. Interactive 파라미터 조정
   └── Franka 관절 랜덤화 범위, 큐브 위치 범위

4. 데이터 생성 (Mimic)
   └── setup_async_generation() → env_loop()
   └── 성공한 시연만 output_file에 저장

5. Cosmos 시각 증강
   ├── 5-1. 비디오 전처리 (semantic segmentation + shading)
   ├── 5-2. Cosmos URL 설정
   └── 5-3. Cosmos 추론 실행 (prompt, control_weight, sigma_max 조정)
```

---

## 3. 데이터셋 구조 분석

### 3.1 전체 HDF5 구조

```
/ (root)
└── data/                              # 메인 그룹
    ├── .attrs["total"] = 2163         # 총 에피소드 수
    ├── .attrs["env_args"] = JSON      # 환경 설정
    │
    ├── demo_0/
    │   ├── .attrs["num_samples"] = 236
    │   ├── .attrs["success"] = True
    │   │
    │   ├── actions                    # (T, 7)  float32
    │   │                               # [Δjoint1..7, gripper]
    │   │                               # range: [-1.0, 1.0]
    │   │
    │   ├── initial_state/             # (1 step) 초기 상태
    │   │   ├── articulation/robot/
    │   │   │   ├── joint_position     # (1, 9)
    │   │   │   ├── joint_velocity     # (1, 9)
    │   │   │   ├── root_pose          # (1, 7)
    │   │   │   └── root_velocity      # (1, 6)
    │   │   └── rigid_object/
    │   │       └── cube_{1,2,3}/
    │   │           ├── root_pose      # (1, 7)
    │   │           └── root_velocity  # (1, 6)
    │   │
    │   ├── obs/                       # 관측값 (매 timestep)
    │   │   ├── actions                # (T, 7) 적용된 액션
    │   │   ├── joint_pos              # (T, 9) Franka 7 + finger 2
    │   │   ├── joint_vel              # (T, 9)
    │   │   ├── eef_pos                # (T, 3) end-effector xyz
    │   │   ├── eef_quat               # (T, 4) end-effector orientation
    │   │   ├── gripper_pos            # (T, 2) 그리퍼 좌우
    │   │   ├── cube_positions         # (T, 9) 3개 큐브 xyz
    │   │   ├── cube_orientations      # (T, 12) 3개 큐브 4D quaternion
    │   │   ├── object                 # (T, 39) 모든 객체 정보 평탄화
    │   │   │
    │   │   └── datagen_info/          # Mimic 내부 데이터
    │   │       ├── eef_pose/
    │   │       │   └── franka         # (T, 4, 4) 4x4 변환 행렬
    │   │       ├── object_pose/
    │   │       │   └── cube_{1,2,3}   # (T, 4, 4) 각 큐브 변환 행렬
    │   │       ├── target_eef_pose/
    │   │       │   └── franka         # (T, 4, 4) 목표 자세
    │   │       └── subtask_term_signals/
    │   │           ├── grasp_1        # (T,) bool
    │   │           ├── grasp_2        # (T,) bool
    │   │           └── stack_1        # (T,) bool
    │   │
    │   └── states/                    # 전체 상태 (매 timestep)
    │       ├── articulation/robot/
    │       │   ├── joint_position     # (T, 9)
    │       │   ├── joint_velocity     # (T, 9)
    │       │   ├── root_pose          # (T, 7)
    │       │   └── root_velocity      # (T, 6)
    │       └── rigid_object/
    │           └── cube_{1,2,3}/
    │               ├── root_pose      # (T, 7)
    │               └── root_velocity  # (T, 6)
    │
    ├── demo_1/ ... (총 2,163개 에피소드)
    └── ...
```

### 3.2 필드별 상세 설명

| 필드 | Shape | 설명 |
|---|---|---|
| `actions` | (T, 7) | Franka 7축 △joint position + gripper. 값 범위: [-1, 1] |
| `obs/joint_pos` | (T, 9) | 7개 Franka 관절 + 2개 finger joint 위치 (rad) |
| `obs/joint_vel` | (T, 9) | 관절 속도 (rad/s) |
| `obs/eef_pos` | (T, 3) | End-effector 위치 (meter) |
| `obs/eef_quat` | (T, 4) | End-effector 방향 (xyzw quaternion) |
| `obs/gripper_pos` | (T, 2) | 그리퍼 좌/우 finger 위치 |
| `obs/cube_positions` | (T, 9) | 큐브 3개의 xyz 좌표 |
| `obs/cube_orientations` | (T, 12) | 큐브 3개의 4D quaternion (xyzw) |
| `obs/datagen_info/eef_pose/franka` | (T, 4, 4) | 4×4 동차 변환 행렬 (rotation + translation) |
| `obs/datagen_info/subtask_term_signals/grasp_1` | (T,) | 첫 번째 큐브 집기 서브태스크 활성화 구간 (bool) |
| `states/articulation/robot/joint_position` | (T, 9) | 시뮬레이션의 실제 관절 상태 |
| `initial_state/...` | (1, ...) | 에피소드 시작 시점의 초기 상태 (1 step) |

### 3.3 Subtask 신호 패턴 (실제 데이터 예시, demo_0 기준)

```
grasp_1: [False ... False] → [0-47] | [True ... True] → [48-102] | [False ... False]
grasp_2: [False ... False] → [0-131] | [True ... True] → [132-171] | [False ... False]
stack_1: [False ... False] → [0-99]  | [True ... True] → [100-165] | [False ... False → 다시 True]
```

각 에피소드는 3개의 서브태스크로 구성:
1. **grasp_1**: 빨간 큐브 집기 → 파란 큐브 위에 쌓기 (pick & place)
2. **grasp_2**: 초록 큐브 집기
3. **stack_1**: 쌓기 동작 (빨강 위에 초록)

---

## 4. 파일 저장 위치

### 4.1 Docker 컨테이너 마운트 구조

| Host | Container | 설명 |
|---|---|---|
| `./samples/annotated_dataset.hdf5` | `/workspace/isaaclab/datasets/annotated_dataset.hdf5` | 입력 데이터 (읽기 전용 유사) |
| ❌ 마운트 없음 | `/workspace/isaaclab/datasets/generated_dataset.hdf5` | **출력 데이터 (컨테이너 내부 전용)** |
| ❌ 마운트 없음 | `/workspace/isaaclab/_isaaclab_out/` | 카메라 프레임 PNG 출력 |
| ❌ 마운트 없음 | `/workspace/isaaclab/_cosmos_out/` | Cosmos 비디오 출력 |
| `./notebook/*.py` | `/workspace/isaaclab/*.py` | 노트북 유틸리티 |

### 4.2 출력 파일 접근 방법

**방법 1 — JupyterLab UI**
> `http://localhost:8888/lab` 접속 → 파일 브라우저에서 다운로드

**방법 2 — docker cp**
```bash
docker cp <container_name>:/workspace/isaaclab/datasets/generated_dataset.hdf5 ./outputs/
```

**방법 3 — docker-compose.yml에 볼륨 추가**
```yaml
volumes:
  - ./outputs:/workspace/isaaclab/datasets
```

---

## 5. 하드웨어 요구사항

### 5.1 Isaac Lab Mimic (궤적 합성)

| 구성 | 요구사항 |
|---|---|
| **GPU** | NVIDIA RTX A6000 (48GB VRAM) 이상 |
| **OS** | Ubuntu 22.04 |
| **Docker** | NVIDIA Container Toolkit |
| **입력 장치** | 키보드 (최소), SpaceMouse (권장), XR 헤드셋 (선택) |

> **실제 Franka 로봇 암은 필요 없음.** 모든 작업은 시뮬레이션 내에서 이루어짐.

### 5.2 NVIDIA Cosmos (시각 증강)

| 구성 | 요구사항 |
|---|---|
| **GPU** | NVIDIA H100 (80GB VRAM) 이상 |
| **배포** | Isaac Lab과 **별도 노드** 필요 |

### 5.3 입력 장치별 텔레오퍼레이션

| 장치 | 필수 여부 | 설명 |
|---|---|---|
| **키보드** | ✅ 최소 요구사항 | WASD/QE/Z-X/T-G/C-V 로 6자유도 제어, K=그리퍼 |
| **SpaceMouse** | ⭐ 권장 | 부드러운 시연 → 모방학습 품질 향상 |
| **XR 헤드셋** | 선택사항 | Apple Vision Pro 등 CloudXR 스트리밍 |

---

## 6. 커스텀 프로젝트

### 6.1 목표

웹캠 입력을 통해 실물 큐브와 사람 손을 인식하여 `annotated_dataset.hdf5`와 동일한 포맷의 데이터를 생성하는 파이프라인 구축.

### 6.2 전체 파이프라인

```
[웹캠]
  ├──→ ArUco 마커 기반 큐브 6DoF 추정 ──→ cube_positions, cube_orientations
  └──→ MediaPipe Pose 기반 손목 추적 ──→ eef_pos, eef_quat
                                            │
                                            ↓
                                   사람-로봇 리타겟팅
                                   (손목 → Franka IK)
                                            │
                                            ↓
                                   Isaac Lab Mimic HDF5 포맷 저장
                                            │
                                            ↓
                                   Isaac Lab Mimic으로 궤적 합성/증강
```

### 6.3 필요한 컴포넌트

#### 6.3.1 큐브 인식 (ArUco Marker)

```python
import cv2
import numpy as np

# 큐브 위 ArUco 마커 → 6DoF 자세 추정
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

# 카메라 캘리브레이션 (미리 수행)
camera_matrix = np.load("camera_matrix.npy")
dist_coeffs = np.load("dist_coeffs.npy")

# 큐브 3개 각각에 마커 ID 할당
CUBE_MARKER_IDS = {0: 1, 1: 2, 2: 3}  # cube_1 → ID 1, ...
```

#### 6.3.2 손 끝 추적 (MediaPipe)

```python
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 손목 랜드마크 (index 15 = right wrist, 16 = left wrist)
# 어깨-팔꿈치-손목 관절각 계산
# 단일 카메라 깊이 모호성 보정 필요
```

#### 6.3.3 사람-로봇 리타겟팅

실제 사람 움직임을 Franka 로봇 좌표계로 변환:

```
사람 손목 (x, y, z) → 스케일링/오프셋 → Franka EEF 위치
사람 손목 방향 (쿼터니언) → Franka EEF 방향
Franka IK (역운동학) → 7개 관절각
```

**난이도 🔴🔴**: 사람과 로봇의 기구학이 완전히 다르므로 정확한 1:1 매핑은 불가능. 근사적인 매핑 또는 시뮬레이션 기반 IK 필요.

#### 6.3.4 Subtask 태깅

키보드 인터페이스로 수동 태깅:

| 키 | 신호 |
|---|---|
| `1` | grasp_1 시작/끝 토글 |
| `2` | grasp_2 시작/끝 토글 |
| `3` | stack_1 시작/끝 토글 |
| `Space` | 에피소드 저장 |

#### 6.3.5 HDF5 저장 (robomimic 호환 포맷)

```python
import h5py
import numpy as np

def save_episode(file_path, episode_data, episode_idx):
    """Isaac Lab / robomimic 호환 HDF5 포맷 저장"""
    with h5py.File(file_path, "a") as f:
        data_group = f["data"]
        ep_group = data_group.create_group(f"demo_{episode_idx}")
        
        T = episode_data["joint_pos"].shape[0]
        ep_group.attrs["num_samples"] = T
        ep_group.attrs["success"] = True
        
        # 액션
        ep_group.create_dataset("actions", data=episode_data["actions"])
        
        # 초기 상태 (1 step)
        init = ep_group.create_group("initial_state")
        # ... articulation, rigid_object 저장
        
        # 관측
        obs = ep_group.create_group("obs")
        obs.create_dataset("joint_pos", data=episode_data["joint_pos"])
        obs.create_dataset("joint_vel", data=episode_data["joint_vel"])
        obs.create_dataset("eef_pos", data=episode_data["eef_pos"])
        # ...
        
        # 전체 상태
        states = ep_group.create_group("states")
        # ... articulation, rigid_object 저장
        
        # 데이터 생성 정보 (datagen_info)
        datagen_info = obs.create_group("datagen_info")
        # ... eef_pose, object_pose, subtask_term_signals
```

### 6.4 난이도 평가

| 작업 | 난이도 | 비고 |
|---|---|---|
| 웹캠 ArUco 마커 큐브 6DoF | 🟢 쉬움 | OpenCV 내장 기능 |
| MediaPipe 손목 3D 위치 | 🟡 보통 | 단일 카메라 깊이 부정확 |
| 사람 팔 → Franka 리타겟팅 | 🔴🔴 매우 어려움 | 기구학 차이 |
| 큐브 속도 (velocity) 측정 | 🔴 어려움 | 위치 미분 노이즈 |
| Subtask 수동 태깅 | 🟢 쉬움 | 키보드 인터페이스 |
| HDF5 포맷 맞춤 저장 | 🟡 보통 | robomimic 스펙 준수 |
| datagen_info 4×4 행렬 | 🔴 어려움 | 시뮬레이션 kinematics 필요 |
| 모든 상태 (states/) 정확 | 🔴🔴 거의 불가능 | velocity, 물리 상태 측정 한계 |

### 6.5 권장 대안 (현실적 접근)

```
[웹캠 인식] → [Isaac Sim 텔레오퍼레이션 연동] → [Isaac Lab Mimic 데이터 생성]
```

웹캠을 SpaceMouse/키보드 대체 입력으로 사용하고, **Franka kinematics와 물리 시뮬레이션은 Isaac Sim이 처리**하는 하이브리드 방식이 가장 현실적.

참고 프로젝트: **NVIDIA Isaac Teleop** (https://github.com/NVIDIA/IsaacTeleop)
- XR 헤드셋 기반 사람 손 → Franka 텔레오퍼레이션
- 손 리타겟팅 프레임워크 내장
- sim & real 통합 지원

---

## 7. 구현 로드맵

### Phase 1: 데이터 인프라 구축 (2-3주)

```
Week 1-2:
  ├── 웹캠 캘리브레이션 (카메라 매트릭스, 왜곡 계수)
  ├── ArUco 마커 생성 및 큐브 부착
  └── 큐브 6DoF 추정 테스트 (cube_positions, cube_orientations)

Week 2-3:
  ├── MediaPipe Pose 손목 추적
  ├── 손목 3D 좌표 → Franka 좌표계 변환
  └── 단일 카메라 깊이 보정 (평면 가정 또는 추가 센서)
```

### Phase 2: 데이터 파이프라인 (2-3주)

```
Week 3-4:
  ├── HDF5 저장 모듈 (robomimic 호환 포맷)
  ├── actions (delta joint) 계산
  └── subtask 수동 태깅 인터페이스

Week 4-5:
  ├── datagen_info 4×4 변환 행렬 생성
  ├── 초기 상태 (initial_state) 저장
  └── 전체 에피소드 녹화/저장 루프
```

### Phase 3: Isaac Lab 연동 (2-3주)

```
Week 5-6:
  ├── 생성된 HDF5 → Isaac Lab Mimic 입력 테스트
  ├── 궤적 합성 검증 (Mimic generate_dataset)
  └── 실패 케이스 분석 및 보정

Week 6-7:
  ├── 반복 개선 (데이터 품질 → 궤적 품질)
  ├── Cosmos 연동 테스트
  └── 전체 파이프라인 자동화
```

### Phase 4: 확장 및 고도화 (계속)

```
  ├── 큐브 종류 다양화 (색상, 크기, 형상)
  ├── 태스크 다양화 (쌓기 외: push, pull, insert)
  ├── 멀티 카메라 (깊이 정확도 향상)
  └── 실시간 시각화 및 모니터링
```

---

## 8. 참고 자료

### 저장소

| 자료 | 링크 |
|---|---|
| Blueprint GitHub | https://github.com/NVIDIA-Omniverse-blueprints/synthetic-manipulation-motion-generation |
| Isaac Lab GitHub | https://github.com/isaac-sim/IsaacLab |
| Isaac Lab 문서 | https://isaac-sim.github.io/IsaacLab/ |
| Isaac Teleop | https://github.com/NVIDIA/IsaacTeleop |
| Cosmos | https://www.nvidia.com/en-us/ai/cosmos/ |
| NVIDIA Blueprint 페이지 | https://build.nvidia.com/nvidia/isaac-gr00t-synthetic-manipulation |

### 기술 블로그

- [Building a Synthetic Motion Generation Pipeline for Humanoid Robot Learning](https://developer.nvidia.com/blog/building-a-synthetic-motion-generation-pipeline-for-humanoid-robot-learning/) (NVIDIA Technical Blog, Mar 2025)

### 라이브러리

| 라이브러리 | 용도 |
|---|---|
| OpenCV + ArUco | 큐브 마커 검출 및 6DoF 추정 |
| MediaPipe (Pose) | 사람 손목/팔 관절 추적 |
| h5py | HDF5 파일读写 |
| NumPy | 수치 연산 |
| robomimic | 참조 HDF5 포맷 스펙 |

### HDF5 분석 도구 (본 프로젝트에서 작성)

- **`inspect_hdf5.py`**: CLI 기반 HDF5 구조 분석기
  - 사용법: `python inspect_hdf5.py <path/to/annotated_dataset.hdf5>`
  - 기능: 전체 트리 구조, episode 요약, 필드 비교, subtask 정보 검색
  
- **`inspect_hdf5.ipynb`**: Jupyter 노트북 버전
  - 셀별 단계적 실행
  - 특정 episode 상세 분석
  - episode 간 key 비교

---

## 부록: HDF5 포맷 생성 체크리스트

`annotated_dataset.hdf5`와 동일한 포맷으로 데이터를 생성하기 위한 필수/선택 항목:

### ✅ 필수 (Mimic 동작)

- [ ] `actions` — (T, 7) float32
- [ ] `obs/joint_pos` — (T, 9) float32
- [ ] `obs/joint_vel` — (T, 9) float32
- [ ] `obs/eef_pos` — (T, 3) float32
- [ ] `obs/eef_quat` — (T, 4) float32
- [ ] `obs/gripper_pos` — (T, 2) float32
- [ ] `obs/cube_positions` — (T, 9) float32
- [ ] `obs/cube_orientations` — (T, 12) float32
- [ ] `states/articulation/robot/joint_position` — (T, 9) float32
- [ ] `states/rigid_object/cube_N/root_pose` — (T, 7) float32
- [ ] `initial_state/articulation/robot/joint_position` — (1, 9) float32
- [ ] `initial_state/rigid_object/cube_N/root_pose` — (1, 7) float32
- [ ] 에피소드 attrs: `num_samples`, `success`

### 🔵 권장 (Mimic 품질 향상)

- [ ] `obs/datagen_info/eef_pose/franka` — (T, 4, 4) float32
- [ ] `obs/datagen_info/object_pose/cube_N` — (T, 4, 4) float32
- [ ] `obs/datagen_info/target_eef_pose/franka` — (T, 4, 4) float32
- [ ] `obs/datagen_info/subtask_term_signals/grasp_N` — (T,) bool
- [ ] `obs/datagen_info/subtask_term_signals/stack_N` — (T,) bool
- [ ] `states/articulation/robot/joint_velocity` — (T, 9) float32
- [ ] `states/rigid_object/cube_N/root_velocity` — (T, 6) float32

### 🟡 선택 (Cosmos 시각 증강 필요 시)

- [ ] 카메라 RGB 이미지
- [ ] Semantic segmentation 이미지
- [ ] Normal map 이미지

---

> **문서 생성일**: 2026-05-19
> **기반 저장소**: https://github.com/NVIDIA-Omniverse-blueprints/synthetic-manipulation-motion-generation
> **Isaac Lab 버전**: 2.0.2 (Blueprint 컨테이너 기본)
