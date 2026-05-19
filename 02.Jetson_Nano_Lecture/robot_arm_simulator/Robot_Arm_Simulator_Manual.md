# Robot Arm Simulator — Synthetic Manipulation Motion Generation

> **PyQt5 + OpenGL 기반 로봇팔 시뮬레이터: 마우스/키보드로 Franka 로봇팔을 조종하고, Isaac Lab Mimic 호환 HDF5 데이터셋을 생성하는 데스크톱 애플리케이션**

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [시스템 아키텍처](#2-시스템-아키텍처)
3. [파일 구조](#3-파일-구조)
4. [설치 및 실행](#4-설치-및-실행)
5. [조작 방법](#5-조작-방법)
6. [핵심 구현 상세](#6-핵심-구현-상세)
7. [HDF5 출력 포맷](#7-hdf5-출력-포맷)
8. [원본 Blueprint와의 관계](#8-원본-blueprint와의-관계)
9. [확장 방안](#9-확장-방안)

---

## 1. 프로젝트 개요

### 1.1 목적

NVIDIA Isaac Lab Mimic을 위한 **입력 데이터셋**(`annotated_dataset.hdf5`)을 생성하는 독립형 데스크톱 애플리케이션.

### 1.2 핵심 아이디어

> **NVIDIA Isaac Sim, Docker, H100 GPU 없이도** 순수 Python + PyQt5 + OpenGL만으로 Franka 로봇팔을 시뮬레이션하고, 사람이 키보드/마우스로 직접 조종하여 시연(demonstration) 데이터를 녹화한 뒤, Isaac Lab Mimic이 읽을 수 있는 HDF5 포맷으로 저장한다.

### 1.3 주요 기능

| 기능 | 설명 |
|---|---|
| **3D 로봇팔 렌더링** | PyOpenGL 기반 실시간 3D 뷰포트 (카메라 회전/확대) |
| **FK/IK** | Franka Emika Panda의 정/역운동학 (DH 파라미터 기반) |
| **키보드 조종** | 7개 관절 개별 제어 + 그리퍼 토글 |
| **큐브 시뮬레이션** | 3개 컬러 큐브 (빨강/파랑/초록) 잡기/놓기 |
| **서브태스크 태깅** | grasp_1, grasp_2, stack_1 신호를 키보드 1/2/3으로 기록 |
| **데이터 녹화** | 매 프레임 관절각, EEF 자세, 큐브 상태를 버퍼에 저장 |
| **HDF5 내보내기** | robomimic/Isaac Lab 호환 포맷으로 저장 (Ctrl+S) |

---

## 2. 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                    main.py (진입점)                        │
│  - QApplication 생성                                      │
│  - 다크 테마 스타일시트                                    │
│  - viewer, recorder, window 조립                          │
└──────────────────────────┬───────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
      ┌────────────┐ ┌──────────┐ ┌──────────────┐
      │ robot_     │ │ main_    │ │ recorder.py  │
      │ viewer.py  │ │ window   │ │              │
      │            │ │ .py      │ │ HDF5 파일 저장│
      │ OpenGL     │ │          │ │ robomimic    │
      │ 3D 렌더링  │ │ 슬라이더 │ │ 호환 포맷     │
      │ 큐브/암    │ │ 버튼     │ │              │
      │ 그리기     │ │ 키바인딩 │ │              │
      └──────┬─────┘ └────┬─────┘ └──────┬───────┘
             │            │              │
             ▼            ▼              ▼
      ┌──────────────────────────────────────────┐
      │           kinematics.py                   │
      │  - DH 변환 행렬                           │
      │  - Forward Kinematics (7-DOF)             │
      │  - Jacobian (6×7)                         │
      │  - Inverse Kinematics (damped least-sq)   │
      │  - 쿼터니언 변환                          │
      └────────────────┬─────────────────────────┘
                       │
                       ▼
      ┌──────────────────────────────────────────┐
      │              config.py                    │
      │  - Franka DH 파라미터                     │
      │  - 관절 제한값 (radians)                  │
      │  - 링크/관절 시각화 치수                  │
      │  - 색상, 큐브 초기 위치                   │
      └──────────────────────────────────────────┘
```

### 2.1 데이터 흐름

```
[키보드 입력] ──→ main_window.py
                       │
                       ▼
               self.joint_angles 업데이트 (7개 float)
                       │
                       ├──→ robot_viewer.py: FK 계산하여 3D 렌더링
                       │
                       └──→ recorder.py (녹화 중일 때만)
                               │
                               ▼
                         버퍼에 프레임 저장
                               │
                    Ctrl+S ────┤
                               ▼
                         HDF5 파일 쓰기
                         (compression=gzip)
```

---

## 3. 파일 구조

```
C:\Users\user\Desktop\robot_arm_simulator/
├── main.py                (3.8 KB)  앱 진입점
├── config.py              (3.1 KB)  Franka 파라미터, DH 테이블, 색상
├── kinematics.py          (8.4 KB)  FK/IK, Jacobian, 쿼터니언
├── robot_viewer.py        (12.0 KB) PyOpenGL 3D 뷰포트
├── main_window.py         (17.9 KB) 전체 UI (슬라이더, 버튼, 키맵)
├── recorder.py            (12.8 KB) 데이터 녹화 + HDF5 내보내기
└── requirements.txt       (192 B)   PyQt5, PyOpenGL, numpy, h5py
```

### 3.1 각 파일 책임

| 파일 | 책임 | 의존성 |
|---|---|---|
| `config.py` | DH 파라미터, 관절 한계, 시각화 상수 | numpy |
| `kinematics.py` | FK/T, Jacobian, IK, quaternion 연산 | numpy, config |
| `robot_viewer.py` | OpenGL 초기화, 조명, 기하 도형 드로잉, 마우스 카메라 | PyOpenGL, PyQt5, kinematics, config |
| `recorder.py` | 프레임 버퍼링, subtask 신호 관리, HDF5 계층 구조 저장 | numpy, h5py, kinematics, config |
| `main_window.py` | 슬라이더/버튼/레이아웃, 키보드 맵, 큐브 부착 물리, 타임 루프 | PyQt5, kinematics, recorder, config |
| `main.py` | QApplication 생성, 스타일시트 적용, 컴포넌트 조립 | 모든 모듈 |

### 3.2 `config.py` 주요 상수

```python
# DH 파라미터: (theta_offset, d, a, alpha) — Franka Emika Panda
DH_PARAMS = [
    (0.0,      0.333,  0.0,     0.0),       # Joint 1
    (-π/2,     0.0,    0.0,     -π/2),      # Joint 2
    (π/2,      0.316,  0.0,      π/2),      # Joint 3
    (π/2,      0.0,    0.0825,   π/2),      # Joint 4
    (-π/2,     0.384, -0.0825,  -π/2),      # Joint 5
    (π/2,      0.0,    0.0,      π/2),      # Joint 6
    (π/2,      0.088,  0.0,      π/2),      # Joint 7
]

# 관절 제한 [min, max] (radians)
JOINT_LIMITS = [
    [-2.8973,  2.8973],   # q1
    [-1.7628,  1.7628],   # q2
    [-2.8973,  2.8973],   # q3
    [-3.0718, -0.0698],   # q4 (Franka q4는 음수 범위)
    [-2.8973,  2.8973],   # q5
    [-0.0175,  3.7525],   # q6
    [-2.8973,  2.8973],   # q7
]

HOME_POSITION = [0.0, -0.3, 0.0, -2.0, 0.0, 2.0, 0.8]
```

### 3.3 `kinematics.py` 핵심 API

```python
def franka_fk(joint_angles)        # (7,) → 4×4 EEF 변환 행렬
def franka_fk_all_joints(angles)   # (7,) → [T₁, T₂, ..., T₇] 각 관절 프레임
def franka_fk_with_ee(angles)      # (7,) → [T₁, ..., T₇, T_ee]
def franka_jacobian(angles)        # (7,) → 6×7 기하 Jacobian
def franka_ik(T_target, q_init)    # 4×4 + (7,) → (7,) or None
def rotation_matrix_to_quat(R)     # 3×3 → (w, x, y, z)
def quat_to_rotation_matrix(q)     # (w, x, y, z) → 3×3
def quat_multiply(q1, q2)          # 쿼터니언 곱
```

---

## 4. 설치 및 실행

### 4.1 요구사항

| 패키지 | 버전 | 용도 |
|---|---|---|
| Python | ≥ 3.8 | |
| PyQt5 | ≥ 5.15 | GUI 프레임워크 |
| PyOpenGL | ≥ 3.1.6 | 3D 렌더링 |
| numpy | ≥ 1.21 | 수치 연산 |
| h5py | ≥ 3.0 | HDF5 파일 입출력 |

### 4.2 설치

```bash
cd C:\Users\user\Desktop\robot_arm_simulator
pip install -r requirements.txt
```

### 4.3 실행

```bash
python main.py
```

### 4.4 필요 하드웨어

- **디스플레이 연결 필수** (OpenGL 컨텍스트 필요)
- GPU: 내장 그래픽으로도 충분 (PyOpenGL 경량)
- RAM: 512MB 이상

---

## 5. 조작 방법

### 5.1 키보드

| 키 | 기능 | 설명 |
|---|---|---|
| **W / S** | Joint 1 (±) | 베이스 회전 (Z축) |
| **A / D** | Joint 2 (±) | 숄더 |
| **Q / E** | Joint 3 (±) | 상완 |
| **Z / X** | Joint 4 (±) | 팔꿈치 |
| **T / G** | Joint 5 (±) | 전완 |
| **C / V** | Joint 6 (±) | 손목 |
| **F / H** | Joint 7 (±) | 손목 회전 |
| **K** | 그리퍼 토글 | 열림(0.04m) ↔ 닫힘(0.0m) |
| **Space** | 녹화 시작/중지 | 토글 |
| **1** | grasp_1 서브태스크 | 첫 번째 큐브 집기 신호 |
| **2** | grasp_2 서브태스크 | 두 번째 큐브 집기 신호 |
| **3** | stack_1 서브태스크 | 쌓기 동작 신호 |
| **R** | 리셋 | 홈 포지션으로 복귀 |
| **Ctrl+S** | 저장 | HDF5 파일로 내보내기 |

### 5.2 마우스

| 동작 | 기능 |
|---|---|
| **왼쪽 버튼 드래그** | 3D 뷰포트 카메라 회전 (azimuth/elevation) |
| **스크롤 휠** | 확대/축소 (0.5m ~ 8.0m) |

### 5.3 UI 컨트롤

| 컨트롤 | 위치 | 설명 |
|---|---|---|
| **Joint 1-7 슬라이더** | 우측 패널 상단 | 각 관절을 0-1000 스케일로 조절 |
| **Gripper 슬라이더** | 우측 패널 중단 | 그리퍼 개폐 정도 |
| **EEF Pose 표시** | 우측 패널 | 현재 end-effector 위치 + 쿼터니언 |
| **Record 버튼** | 우측 패널 | ⏺ 클릭 시 녹화 시작/중지 |
| **Save HDF5 버튼** | 우측 패널 | 저장 대화상자 열기 |
| **Cancel 버튼** | 우측 패널 | 현재 녹화 취소 |
| **Subtask 버튼** | 우측 패널 하단 | grasp_1/2, stack_1 수동 토글 |
| **상태 표시창** | 우측 패널 최하단 | 로그 메시지 출력 |

---

## 6. 핵심 구현 상세

### 6.1 Forward Kinematics

Denavit-Hartenberg convention 사용:

```python
def dh_transform(theta, d, a, alpha):
    ct, st = cos(theta), sin(theta)
    ca, sa = cos(alpha), sin(alpha)
    return [[ct, -st*ca,  st*sa, a*ct],
            [st,  ct*ca, -ct*sa, a*st],
            [0,      sa,     ca,    d],
            [0,       0,      0,    1]]
```

7개 DH 변환을 순차 곱하여 EEF 4×4 변환 행렬 계산. EEF 오프셋 `(0, 0, 0.103)m` 추가 적용.

### 6.2 Inverse Kinematics

Damped Least-Squares (Levenberg-Marquardt):

```
error = SE3_error(T_target, T_current)    # (6,) position + orientation
J     = franka_jacobian(q)                # (6×7)
λ     = 0.01 * trace(J J^T) / 6           # adaptive damping
dq    = J^T (J J^T + λI)⁻¹ error          # damped pseudoinverse
q    += 0.5 * dq                           # damping factor
q     = clamp(q, JOINT_LIMITS)            # 관절 제한 적용
```

### 6.3 3D 렌더링 파이프라인

```
paintGL() 호출 (60 FPS 타이머)
  │
  ├── glClear() ─── 배경색 (dark navy #1e1e2e)
  ├── gluLookAt() ─── 카메라 (azimuth/elevation/distance)
  ├── _draw_grid() ─── 바닥 그리드 (10×10)
  ├── _draw_table() ─── 작업 테이블
  ├── _draw_cubes() ─── 3개 컬러 큐브 (quaternion 회전 적용)
  └── _draw_robot()
        ├── 베이스 (flat box)
        ├── 링크 i=1..7: cylinder(prev_joint → joint_i)
        ├── 관절 i=1..7: sphere(radius = JOINT_RADII[i])
        ├── EEF: red sphere
        ├── 그리퍼: 2개 finger (EEF y축 방향)
        └── 부착된 큐브 (EEF 위치에 렌더링)
```

### 6.4 큐브 부착 물리

단순화된 규칙 기반:

```
1. K 키로 그리퍼 닫힘 (gripper_width < 0.005m)
2. EEF와 큐브 사이 거리 < 0.08m 이면 자동 부착
3. 부착된 큐브는 EEF 위치에 따라 이동
4. K 키로 그리퍼 열리면 큐브를 현재 EEF 위치에 드롭
```

### 6.5 녹화 시스템

```python
recorder.start_episode()        # 버퍼 초기화
while recording:
    recorder.record_frame(
        joint_angles,           # (7,) rad
        gripper_width,          # float
        cube_positions,         # dict {name: (3,)}
        cube_orientations,      # dict {name: (4,)}
        cube_attached           # dict {name: bool}
    )
    # 매 프레임:
    #   joint_vel = finite_difference(joint_angles)
    #   actions   = [Δq1..7, gripper_cmd]
    #   T_ee      = franka_fk(joint_angles) → eef_pos, eef_quat
    #   subtask_signals → datagen_info/subtask_term_signals/

idx = recorder.finish_episode(success=True)
```

### 6.6 HDF5 저장 구조

```python
with h5py.File("annotated_dataset.hdf5", "w") as f:
    data = f.create_group("data")
    data.attrs["total"] = N
    data.attrs["env_args"] = json.dumps({"env_name": "...", "type": 2})

    for i in range(N):
        ep = data.create_group(f"demo_{i}")
        ep.attrs["num_samples"] = T
        ep.attrs["success"] = True

        ep.create_dataset("actions", data=..., compression="gzip")
        # obs/, states/, initial_state/ 모두 동일한 계층 구조로 저장
```

---

## 7. HDF5 출력 포맷

### 7.1 전체 구조

```
/data
├── .attrs["total"] = N
├── .attrs["env_args"] = '{"env_name": "Franka-CubeStack-Custom-v0", "type": 2}'
│
├── demo_0/
│   ├── .attrs["num_samples"] = 236
│   ├── .attrs["success"] = True
│   ├── actions                          (T, 8)    [Δq₁..Δq₇, gripper_cmd]
│   │
│   ├── initial_state/
│   │   ├── articulation/robot/
│   │   │   ├── joint_position           (1, 9)
│   │   │   ├── joint_velocity           (1, 9)
│   │   │   ├── root_pose                (1, 7)
│   │   │   └── root_velocity            (1, 6)
│   │   └── rigid_object/
│   │       ├── cube_1/root_pose         (1, 7)
│   │       └── cube_2/root_pose         (1, 7)
│   │       └── cube_3/root_pose         (1, 7)
│   │
│   ├── obs/
│   │   ├── actions                      (T, 8)    적용된 액션
│   │   ├── joint_pos                    (T, 9)
│   │   ├── joint_vel                    (T, 9)
│   │   ├── eef_pos                      (T, 3)
│   │   ├── eef_quat                     (T, 4)
│   │   ├── gripper_pos                  (T, 2)
│   │   ├── cube_positions               (T, 9)
│   │   ├── cube_orientations            (T, 12)
│   │   ├── object                       (T, 39)
│   │   └── datagen_info/
│   │       ├── eef_pose/franka          (T, 4, 4)
│   │       ├── object_pose/cube_{1,2,3} (T, 4, 4)
│   │       ├── target_eef_pose/franka   (T, 4, 4)
│   │       └── subtask_term_signals/
│   │           ├── grasp_1              (T,) bool
│   │           ├── grasp_2              (T,) bool
│   │           └── stack_1              (T,) bool
│   │
│   └── states/
│       ├── articulation/robot/
│       │   ├── joint_position           (T, 9)
│       │   ├── joint_velocity           (T, 9)
│       │   ├── root_pose                (T, 7)
│       │   └── root_velocity            (T, 6)
│       └── rigid_object/
│           └── cube_{1,2,3}/
│               ├── root_pose            (T, 7)
│               └── root_velocity        (T, 6)
│
├── demo_1/ ...
└── ...
```

### 7.2 원본 `annotated_dataset.hdf5`와의 차이점

| 항목 | 원본 (NVIDIA) | 본 프로젝트 | 영향 |
|---|---|---|---|
| 물리 엔진 | PhysX (Isaac Sim) | 없음 | Mimic이 자체 합성하므로 입력 시연에는 무방 |
| velocities | 실제 시뮬레이션 값 | 위치 유한차분 근사 | Mimic이 재계산 가능 |
| datagen_info | 정확한 변환 행렬 | FK 기반 계산 | 동일 |
| subtask 신호 | 실제 태스크 자동 감지 | 수동 키보드 태깅 | 정확도는 사용자 의존 |
| 카메라 이미지 | 포함 가능 | 미포함 | Cosmos 증강에 필요 시 추가 가능 |

---

## 8. 원본 Blueprint와의 관계

### 8.1 포지셔닝

```
NVIDIA Stack (원본)                 본 프로젝트
══════════════════                 ════════════════
Isaac Sim (시뮬레이터)     →    PyQt5 + OpenGL (3D 뷰어)
Isaac Lab (학습 프레임워크) →    없음 (Mimic이 대신 처리)
Isaac Lab Mimic (궤적 합성) →    사용 (출력 데이터를 Mimic 입력으로)
NVIDIA Cosmos (시각 증강)  →    선택사항 (추후 연동 가능)
Docker + H100 GPU          →    필요 없음 (일반 PC)
```

### 8.2 데이터 흐름

```
본 프로젝트                                NVIDIA Stack
══════════════                            ════════════
키보드 조종 ──→ 시연 녹화                      
                │                              
                ▼                              
        annotated_dataset.hdf5 ──→ Isaac Lab Mimic
                                    (궤적 합성)
                                        │
                                        ▼
                                generated_dataset.hdf5
                                        │
                                        ▼
                                    NVIDIA Cosmos
                                    (시각 증강)
                                        │
                                        ▼
                                최종 학습 데이터셋
```

---

## 9. 확장 방안

### 9.1 단기 확장 (쉬움)

| 항목 | 설명 | 예상 작업량 |
|---|---|---|
| **웹캠 연동** | OpenCV로 웹캠 영상을 UI에 오버레이 | 2-3시간 |
| **다중 카메라 뷰** | 고정/추적/EEF 시점 전환 | 1-2시간 |
| **태스크 다양화** | push, pull, insert 등 새로운 태스크 템플릿 | 2-3시간 |
| **데이터 증강** | 관절 노이즈 추가, 속도 변형 | 1-2시간 |
| **재생 모드** | 녹화된 시연을 다시 재생 (검증용) | 2-3시간 |

### 9.2 중기 확장 (보통)

| 항목 | 설명 | 비고 |
|---|---|---|
| **URDF 로더** | 임의의 로봇 URDF 파일 로드 | assimp/trimesh 필요 |
| **충돌 감지** | 간단한 AABB/OBB 충돌 검사 | 자체 구현 가능 |
| **모션 재생 속도 조절** | 시간 scaling | recorder에 time stamp 추가 |
| **Cosmos REST API 연동** | 생성된 HDF5를 Cosmos로 전송 | cosmos_request.py 참조 |

### 9.3 장기 확장 (어려움)

| 항목 | 설명 | 비고 |
|---|---|---|
| **물리 엔진 내장** | PyBullet 또는 MuJoCo 연동 | sim-to-real gap 감소 |
| **모방 학습 정책 훈련** | Diffusion Policy 등 직접 훈련 | GPU + 대규모 데이터 필요 |
| **웹 기반 버전** | Three.js/WebGL로 포팅 | 브라우저에서 실행 가능 |

---

## 부록: 키보드 맵 참고표

```
┌──────┬──────────────┬──────────────────────────────┐
│ 키   │ 증가(-)      │ 감소(+)                      │
├──────┼──────────────┼──────────────────────────────┤
│ W/S  │ Joint 1 +0.03│ Joint 1 -0.03 (베이스 회전)  │
│ A/D  │ Joint 2 +0.02│ Joint 2 -0.02               │
│ Q/E  │ Joint 3 +0.02│ Joint 3 -0.02               │
│ Z/X  │ Joint 4 +0.02│ Joint 4 -0.02               │
│ T/G  │ Joint 5 +0.02│ Joint 5 -0.02               │
│ C/V  │ Joint 6 +0.02│ Joint 6 -0.02               │
│ F/H  │ Joint 7 +0.02│ Joint 7 -0.02               │
├──────┼──────────────┼──────────────────────────────┤
│ K    │ 토글          │ 그리퍼 open(0.04) ↔ close(0) │
│ 1    │ 토글          │ grasp_1 subtask 신호         │
│ 2    │ 토글          │ grasp_2 subtask 신호         │
│ 3    │ 토글          │ stack_1 subtask 신호         │
│ R    │ 리셋          │ HOME_POSITION으로 복귀       │
│ Space│ 토글          │ 녹화 시작/중지               │
│ Ctrl+S│ 저장         │ HDF5 파일 저장 대화상자      │
└──────┴──────────────┴──────────────────────────────┘
```

---

> **프로젝트 위치**: `C:\Users\user\Desktop\robot_arm_simulator/`
> **실행 방법**: `cd robot_arm_simulator && pip install -r requirements.txt && python main.py`
> **HDF5 출력**: `recorder.save_to_hdf5()` → Isaac Lab Mimic 호환 포맷
> **라이선스**: MIT (참고: NVIDIA Isaac Lab은 BSD-3-Clause)
