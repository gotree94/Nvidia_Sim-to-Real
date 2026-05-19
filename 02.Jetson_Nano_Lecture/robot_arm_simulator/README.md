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

---

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

