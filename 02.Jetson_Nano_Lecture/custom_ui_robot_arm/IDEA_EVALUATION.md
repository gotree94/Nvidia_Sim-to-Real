# 아이디어 평가: 커스텀 UI 로봇암 시뮬레이터

> **NVIDIA Isaac Sim / Isaac Lab / Cosmos 스택 없이, 순수 Python GUI로 Franka 로봇팔을 시뮬레이션하고 데이터셋을 생성하는 접근법에 대한 평가**

---

## 1. 평가 개요

### 1.1 아이디어 요약

웹캠, Isaac Sim, Docker, H100 GPU 등 고사양 인프라 없이, **PyQt5 + PyOpenGL + NumPy**만으로 데스크톱 애플리케이션을 구축하여:

1. Franka 로봇팔을 3D로 렌더링
2. 키보드/마우스로 직접 조종
3. 데이터를 녹화하여 Isaac Lab Mimic 호환 HDF5로 저장
4. Mimic이 이를 입력받아 대규모 합성 궤적 생성

### 1.2 기존 접근법과의 비교

| 항목 | NVIDIA Blueprint (원본) | Isaac Sim 텔레오퍼레이션 | **👉 커스텀 UI (본 제안)** |
|---|---|---|---|
| **시뮬레이터** | Isaac Sim (Omniverse) | Isaac Sim | PyQt5 + PyOpenGL |
| **GPU** | RTX A6000 (48GB) | RTX A6000 | **내장 GPU로 충분** |
| **Docker** | 필수 | 필수 | **불필요** |
| **설치 난이도** | 높음 | 높음 | **pip install 4개** |
| **데이터 포맷** | robomimic HDF5 | robomimic HDF5 | **동일 포맷** |
| **물리 엔진** | PhysX (정확) | PhysX (정확) | **없음** |
| **실전 데이터 품질** | 높음 | 높음 | 중간 (Mimic이 보완) |
| **개발 시간** | 즉시 사용 | 즉시 사용 | **2-3주 구축 필요** |
| **확장성** | 제한적 (NVIDIA 종속) | 제한적 | **자유로움** |

---

## 2. 기술적 타당성

### 2.1 가능한 것 (✅)

| 기능 | 구현 방법 | 난이도 |
|---|---|---|
| **Franka 7-DOF FK** | Denavit-Hartenberg 파라미터 행렬 곱 | 🟢 쉬움 |
| **Jacobian + IK** | Jacobian pseudoinverse + damped least-squares | 🟡 보통 |
| **3D 렌더링** | PyOpenGL gluCylinder/gluSphere로 링크/관절 표현 | 🟡 보통 |
| **키보드 관절 제어** | W/S/A/D/Q/E 등 14개 키 → 관절각 증분 | 🟢 쉬움 |
| **마우스 시점 제어** | 드래그 → azimuth/elevation, 휠 → zoom | 🟢 쉬움 |
| **데이터 프레임 녹화** | 매 timestep 버퍼에 joint_pos/eef_pos 등 저장 | 🟢 쉬움 |
| **HDF5 내보내기** | h5py로 robomimic 계층 구조 생성 | 🟡 보통 |
| **서브태스크 태깅** | 키보드 1/2/3으로 grasp/stack 신호 기록 | 🟢 쉬움 |
| **큐브 잡기/놓기** | EEF-큐브 거리 기반 단순 부착 | 🟢 쉬움 |

### 2.2 불가능/부정확한 것 (❌/🟡)

| 기능 | 이유 | 완화 방안 |
|---|---|---|
| **정확한 물리 시뮬레이션** | 충돌/중력/마찰 없음 | Mimic이 물리적으로 타당한 궤적으로 합성 |
| **관절 속도 (velocity)** | 실제 센서 없음, 위치 유한차분 | Mimic이 자체 계산 가능 |
| **물체 속도 (root_velocity)** | 측정 불가 | Mimic 생성 시 자동 계산 |
| **datagen_info 4×4 행렬** | FK 기반 근사치 | 원본과 동일한 kinematic chain 사용 |
| **현실 세계와의 일치** | sim-to-real gap | Mimic이 domain randomization으로 보완 |

### 2.3 핵심 리스크

| 리스크 | 심각도 | 대응 |
|---|---|---|
| **사람이 키보드로 만든 시연의 품질** | 🟡 중간 | SpaceMouse 권장, 느린 속도로 정밀 조작 |
| **서브태스크 태깅 실수** | 🟡 중간 | 녹화 후 검증/재태깅 기능 필요 |
| **HDF5 포맷 불일치** | 🔴 낮음 | robomimic 스펙 정확히 준수 |
| **Mimic 호환성** | 🟡 중간 | NVIDIA 샘플 데이터로 포맷 검증 완료 |

---

## 3. 아키텍처 설계

### 3.1 전체 구조

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                               │
│              QApplication + 다크 테마 + 조립                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │  app.py  │  │renderer │  │recorder  │
       │ (Main    │  │ .py     │  │ .py      │
       │  Window) │  │ (OpenGL │  │ (HDF5    │
       │          │  │  3D)    │  │  저장)   │
       │ 슬라이더 │  │         │  │          │
       │ 키바인딩 │  │ 로봇암  │  │ robomimic│
       │ 큐브물리 │  │ 큐브    │  │ 호환포맷 │
       └────┬─────┘  │ 그리기  │  └────┬─────┘
            │        └────┬─────┘       │
            ▼             ▼             ▼
       ┌──────────────────────────────────────┐
       │           kinematics.py               │
       │  DH 변환 → FK → Jacobian → IK       │
       │  쿼터니언 변환, SE(3) 에러            │
       └────────────────┬─────────────────────┘
                        ▼
       ┌──────────────────────────────────────┐
       │              config.py                │
       │  Franka DH 파라미터, 관절 한계, 색상  │
       └──────────────────────────────────────┘
```

### 3.2 데이터 흐름

```
[입력] 키보드/마우스/슬라이더
    │
    ▼
app.py: joint_angles += delta (매 16ms)
    │
    ├──→ renderer.py: FK 계산 → 3D 그리기
    │
    └──→ recorder.py (녹화 중일 때)
            │
            ▼
        버퍼: list of dict (joints, eef, cubes, subtask)
            │
    [Ctrl+S] ▼
        HDF5 파일 쓰기
        /data/demo_0/actions, obs/, states/, ...
```

### 3.3 게임 루프 (60 FPS)

```
app.py의 QTimer(16ms)
    │
    ├── 1. 키 반복 처리 (key_states dict)
    │      └── joint_angles += key_step * direction
    │
    ├── 2. 큐브 부착 업데이트
    │      └── gripper closed + EEF-큐브 거리 < threshold → attach
    │
    ├── 3. renderer.update() (OpenGL 다시 그리기)
    │
    ├── 4. UI 라벨 업데이트 (EEF pos, quat)
    │
    └── 5. recorder.record_frame() (녹화 중일 때)
```

---

## 4. 기술 스택 평가

### 4.1 필수 패키지

| 패키지 | 용도 | 대안 | 채택 이유 |
|---|---|---|---|
| **PyQt5** | GUI 프레임워크 | PySide6, tkinter | 가장 성숙, QOpenGLWidget 내장 |
| **PyOpenGL** | 3D 렌더링 | ModernGL, matplotlib 3D | GLU 의존성 (Cylinder, Sphere) |
| **NumPy** | 수치 연산 | - | 표준 |
| **h5py** | HDF5 입출력 | - | Isaac Lab 호환 필수 |

### 4.2 선택적 패키지

| 패키지 | 용도 | 비고 |
|---|---|---|
| **scipy** | 고급 최적화 (IK) | numpy만으로 충분, 선택사항 |
| **trimesh** | STL/URDF 3D 메시 로드 | 시각적 품질 향상 |
| **OpenCV** | 웹캠 연동 | 향후 확장 시 |

---

## 5. 구현 계획

### Phase 1: 코어 엔진 (1주)

| 작업 | 내용 | 파일 |
|---|---|---|
| DH 파라미터 정의 | Franka Panda 정확한 파라미터 | `config.py` |
| Forward Kinematics | 4×4 변환 행렬 체인 | `kinematics.py` |
| Jacobian + IK | Damped least-squares | `kinematics.py` |
| OpenGL 초기화 | 조명, 카메라, 재질 | `renderer.py` |
| 로봇 형상 그리기 | 링크(원기둥) + 관절(구) | `renderer.py` |

### Phase 2: UI 및 제어 (1주)

| 작업 | 내용 | 파일 |
|---|---|---|
| 메인 윈도우 레이아웃 | Splitter: 3D뷰 + 컨트롤패널 | `app.py` |
| 관절 슬라이더 | 7개 QSlider + QLabel | `app.py` |
| 키보드 맵 | 20개 키 → 관절/기능 바인딩 | `app.py` |
| 마우스 시점 | 드래그 회전, 휠 확대 | `renderer.py` |
| 다크 테마 | QSS 스타일시트 | `app.py` |

### Phase 3: 데이터 파이프라인 (1주)

| 작업 | 내용 | 파일 |
|---|---|---|
| 프레임 버퍼 | list of ndarray | `recorder.py` |
| subtask 태깅 | grasp_1/2, stack_1 | `recorder.py`, `app.py` |
| 큐브 부착 물리 | EEF 거리 기반 attach/detach | `app.py` |
| HDF5 저장 | robomimic 호환 계층 구조 | `recorder.py` |
| initial_state 쓰기 | 첫 프레임 별도 저장 | `recorder.py` |

### Phase 4: 완성 및 테스트 (3일)

| 작업 | 내용 |
|---|---|
| HDF5 포맷 검증 | inspect_hdf5.py로 NVIDIA 샘플과 비교 |
| 키 반복 속도 튜닝 | 자연스러운 조작감 |
| 에러 처리 | 파일 저장 실패, 포맷 불일치 |
| 사용자 매뉴얼 | README.md, 조작법 |

---

## 6. HDF5 호환성

### 6.1 대상 포맷: Isaac Lab Mimic / robomimic

```
/data
  ├── attrs: total=N, env_args={...}
  └── demo_N/
        ├── attrs: num_samples=T, success=True
        ├── actions                   (T, 8)  [Δq, gripper_cmd]
        ├── obs/joint_pos             (T, 9)
        ├── obs/joint_vel             (T, 9)
        ├── obs/eef_pos               (T, 3)
        ├── obs/eef_quat              (T, 4)
        ├── obs/cube_positions        (T, 9)
        ├── obs/cube_orientations     (T, 12)
        ├── obs/datagen_info/
        │     └── subtask_term_signals/{grasp_1,grasp_2,stack_1}
        ├── states/articulation/robot/joint_position  (T, 9)
        └── initial_state/articulation/robot/joint_position  (1, 9)
```

### 6.2 검증 방법

```bash
# NVIDIA 샘플과 동일한 구조인지 확인
python inspect_hdf5.py annotated_dataset.hdf5
python inspect_hdf5.py my_output.hdf5
# → 동일한 key 트리인지 비교
```

---

## 7. 확장 로드맵

### 7.1 단기 (다음 주)

| 항목 | 설명 |
|---|---|
| **웹캡 오버레이** | OpenCV 영상을 UI 모서리에 표시 |
| **멀티 뷰포트** | Top/Side/Perspective 3분할 |
| **재생 모드** | 녹화된 시연을 다시 재생 |

### 7.2 중기 (1-2개월)

| 항목 | 설명 |
|---|---|
| **URDF 로더** | 모든 로봇 형상 지원 |
| **PyBullet 물리** | 충돌/중력 시뮬레이션 |
| **Cosmos 연동** | 생성된 HDF5를 Cosmos REST API로 전송 |
| **Diffusion Policy 훈련** | 수집된 데이터로 정책 직접 학습 |

### 7.3 장기 (3개월+)

| 항목 | 설명 |
|---|---|
| **다중 로봇 지원** | UR5, KUKA, 사용자 정의 로봇 |
| **웹 포팅** | Three.js/WebGL 브라우저 버전 |
| **분산 녹화** | 여러 클라이언트에서 동시 데이터 수집 |

---

## 8. 결론

### 8.1 평가 요약

| 평가 항목 | 점수 | 설명 |
|---|---|---|
| **기술적 실현 가능성** | ⭐⭐⭐⭐⭐ | 순수 Python + OpenGL로 충분히 구현 가능 |
| **NVIDIA 대비 생산성** | ⭐⭐⭐⭐ | Docker/GPU 설정 시간 0, pip install 5분 |
| **데이터 품질** | ⭐⭐⭐ | 물리 부정확하나 Mimic이 보완 가능 |
| **확장성** | ⭐⭐⭐⭐⭐ | 100% 오픈소스, NVIDIA 종속 없음 |
| **실제 연구 활용도** | ⭐⭐⭐⭐ | Mimic + Cosmos 파이프라인 그대로 사용 가능 |

### 8.2 최종 판정

> **✅ 실행할만한 가치가 있는 접근법이다.**
>
> NVIDIA의 고가 인프라에 접근할 수 없는 환경에서도 Isaac Lab Mimic을 활용한 합성 데이터 생성 파이프라인을 구축할 수 있다. 물리 시뮬레이션의 부재는 Mimic이 자체 궤적 합성 과정에서 물리적 타당성을 보장해주므로 핵심적인 문제가 아니다. 다만, 사람이 키보드로 조종하는 시연 데이터의 품질(Smoothness, Consistency)이 최종 결과물의 품질을 결정하므로, SpaceMouse 도입이나 속도 조절 기능으로 보완하는 것이 좋다.

### 8.3 권장 사항

1. **Phase 1-4를 순차적으로 진행** (총 약 3주)
2. **중간 검증**: 매 Phase 완료 후 inspect_hdf5.py로 포맷 검증
3. **SpaceMouse 연동**: 키보드보다 부드러운 시연을 위해 권장
4. **데이터 증강**: 수집 후 약간의 노이즈/변형을 가해 다양성 확보
5. **Mimic 테스트**: 첫 HDF5 생성 후 반드시 Isaac Lab Mimic으로 궤적 합성 테스트
