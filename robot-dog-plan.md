# 로봇개 개발 계획 — Isaac Sim + ROS2 + Jetson HIL Pipeline

> **작성일**: 2026-05-14
> **타겟 HW**: Jetson Orin Nano Super (교육용 제품화)
> **보조 HW**: Jetson Nano 2GB, Jetson TX2 (경험/학습용)
> **Workstation GPU**: RTX 5090 Laptop 24GB (보유 중)

---

## 1. 전체 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────┐
│              1. 개발 Workstation (노트북)                       │
│        (Isaac Sim 실행 — RTX 5090 Laptop 24GB)                 │
│  - 물리 시뮬레이션 (PhysX)                                      │
│  - 센서 데이터 생성 (LiDAR, Camera, IMU)                        │
│  - 3D 렌더링 / GUI 시각화                                       │
│  - Omniverse Streaming (Headless → 원격 접속)                   │
│  - 24GB VRAM — 복잡한 로봇개 시뮬레이션 충분                   │
└────────────────────────┬────────────────────────────────────────┘
                         │ ROS2 Network (Ethernet / WiFi)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│             2. Jetson Orin Nano Super (최종 타겟)               │
│          ★ 교육용 로봇개의 실제 두뇌보드 ★                      │
│  - ROS2 제어 노드 (cmd_vel, odom, joint_states)                 │
│  - Isaac ROS 추론 (VSLAM, PeopleSegNet, Detections)             │
│  - 센서 퓨전 (EKF, IMU + Odometry)                             │
│  - 경로 계획 / 장애물 회피                                      │
│  - 67 TOPS — 다중 AI 모델 동시 실행 가능                       │
└─────────────────────────────────────────────────────────────────┘
```

### 보조 하드웨어 (교육/경험용)

```
┌─────────────────────┐   ┌─────────────────────┐
│ Jetson Nano 2GB     │   │ Jetson TX2          │
│ (ROS2 기초 실습)     │   │ (중급 SW 포팅 경험)  │
│                      │   │                     │
│ - ROS2 pub/sub 기초  │   │ - ROS2 네비게이션    │
│ - 간단한 센서 노드   │   │ - 경량 추론 모델     │
│ - Linux 임베디드 경험 │   │ - 성능 차이 체감     │
└─────────────────────┘   └─────────────────────┘
```

---

## 2. Isaac Sim 직접 구동 가능성 (매우 중요)

Isaac Sim은 **Jetson 계열 보드에서는 절대 직접 실행할 수 없습니다.**

| 요소 | Isaac Sim 요구사항 | **RTX 5090 Laptop 24GB** | Jetson Orin Nano Super |
|------|:------------------:|:------------------------:|:----------------------:|
| **GPU** | RTX 3070 이상 (RT Cores 필수) | **RTX 5090 (Blackwell)** ✅ | Ampere 1024 CUDA (RT Cores 없음) |
| **VRAM** | 최소 8GB | **24GB** ✅ | 8GB (공유 메모리) |
| **RT Cores** | 필수 | **4세대 RT Cores** ✅ | 없음 |
| **판정** | — | **Ideal 수준 초과** ✅ | **Isaac Sim 직접 구동 불가** |

> **RTX 5090 Laptop 24GB면 Isaac Sim 시스템 요구사항을 크게 상회합니다.** 데스크톱 RTX 4090 이상급 성능으로, 로봇개 시뮬레이션에 필요한 고해상도 센서 + 물리 연산 + 실시간 렌더링을 모두 여유 있게 처리 가능합니다.
>
> Isaac Sim은 **Workstation(본 노트북)에서 실행**하고, Jetson은 ROS2로 연결된 **Hardware-in-the-Loop(HIL) 파트너**로서 역할을 분담합니다.

---

## 3. Jetson Orin Nano Super 상세 스펙

| 항목 | Orin Nano 8GB | Orin Nano 8GB **Super** | 향상률 |
|------|:------------:|:----------------------:|:-----:|
| **AI 성능** | **40 TOPS** | **67 TOPS** | **+67%** |
| GPU 클럭 | 625 MHz | **1020 MHz** | **+63%** |
| 메모리 대역폭 | 68 GB/s | **102 GB/s** | **+50%** |
| CPU 클럭 | 1.5 GHz | 1.7 GHz | +13% |
| CUDA Cores | 1024 | 1024 | 동일 |
| Tensor Cores | 32 | 32 | 동일 |
| 메모리 | 8GB LPDDR5 | 8GB LPDDR5 | 동일 |
| 전력 | 5-15W | ~15-25W | 증가 |

### Super 버전이 로봇개에 중요한 이유

| 작업 | Nano (40 TOPS) | Nano **Super** (67 TOPS) |
|-----|:-------------:|:-----------------------:|
| VSLAM + 객체 감지 동시 처리 | ⚠️ 버퍼링 발생 가능 | ✅ 여유 있음 |
| 다중 카메라 (3~4대) 스트림 처리 | ❌ 대역폭 부족 | ✅ 102 GB/s로 가능 |
| YOLOv8 모델 추론 | m (중간)까지 가능 | l (대형)까지 가능 |
| 동시 실행 AI 모델 수 | 1~2개 | 2~3개 |
| 추후 SW 업데이트로 기능 향상 | 여유 적음 | ✅ 여유 있음 |

---

## 4. 생성형 AI 이론

로봇개에 지능을 탑재하기 위해 필요한 생성형 AI 기초 이론입니다.

### 4.1 Transformer 구조 이해

```
입력 시퀀스
    │
    ▼
┌────────────────────────────────────────┐
│           Embedding + Positional Encoding│
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│     Multi-Head Self-Attention          │
│  - Query, Key, Value 계산              │
│  - Scaled Dot-Product Attention        │
│  - 여러 Head의 결과 Concatenation      │
└────────────────────────────────────────┘
    │
    ▼
┌────────────────────────────────────────┐
│     Feed-Forward Network (FFN)         │
│  - 두 개의 선형 변환 + ReLU           │
└────────────────────────────────────────┘
    │ (반복: N개 레이어)
    ▼
┌────────────────────────────────────────┐
│           출력 (로짓)                  │
└────────────────────────────────────────┘
```

| 구성 요소 | 설명 | 로봇개 활용에서의 의미 |
|----------|------|---------------------|
| **Self-Attention** | 입력 내 모든 토큰 간 관계 학습 | 센서 시퀀스(카메라 프레임, LiDAR 스캔)의 시공간 관계 파악 |
| **Multi-Head** | 여러 관점에서 동시에 Attention | 시각, 거리, 음성 등 멀티모달 입력 병렬 처리 |
| **Positional Encoding** | 순서 정보 주입 | 시간에 따른 센서 데이터 변화 인코딩 |
| **Cross-Attention** | 두 시퀀스 간 관계 (Encoder-Decoder) | 명령(텍스트) → 행동(모터 명령) 매핑의 핵심 |

### 4.2 Edge 환경에서의 생성형 AI 활용

Jetson Orin Nano Super(67 TOPS)와 같은 **엣지 디바이스**에서 생성형 AI를 구동할 때의 고려사항:

| 고려사항 | 설명 | 대응 전략 |
|---------|------|---------|
| **제한된 VRAM** | 8GB 공유 메모리 (시스템 + GPU 공유) | 모델 양자화 (INT8/FP16), 4비트 양자화 |
| **전력 제약** | 15-25W TDP | 효율적 배치 처리, 아이들 시 추론 중단 |
| **추론 지연 시간** | 실시간 제어를 위한 빠른 응답 | ONNX TensorRT 변환, 커널 최적화 |
| **모델 크기** | LLM/VLM의 수 GB 파라미터 | 경량 모델 선정 (Gemma 2B, Phi-3 mini, LLaVA-7B) |

**엣지-클라우드 하이브리드 아키텍처**:
```
로봇개(Orin Nano Super)              클라우드/Workstation
     │                                        │
     │ 실시간 추론 (경량 모델)                  │
     │ -物体 감지 (YOLOv8)                    │
     │ - VSLAM                                │
     │ - 단순 명령 이해 (소형 LLM)             │
     │                                        │
     │ ← 비동기 ─── 고급 추론 요청 ───────── │
     │    (복잡한 명령, 맥락 이해)             │
     │                                        │
     │ ← 주기적 ─── 모델 업데이트 ────────── │
     │    (파인튜닝된 가중치 동기)              │
```

---

## 5. 생성형 AI 실습

### 5.1 LLM (Large Language Model) 구동

Orin Nano Super에서 구동 가능한 경량 LLM:

| 모델 | 파라미터 | 메모리 (INT4) | 활용 |
|------|---------|:------------:|------|
| **Gemma 2B** | 2B | ~1.5 GB | 로봇 음성 명령 이해 |
| **Phi-3 mini** | 3.8B | ~2.5 GB | 상황 설명, 간단한 추론 |
| **LLaMA 3.2 3B** | 3B | ~2.0 GB | 대화형 명령 처리 |

**실습 예시**: 음성 명령 → LLM → 로봇 행동 변환 파이프라인
```
음성 입력 → Whisper (STT) → LLM (명령 분석) → cmd_vel 변환 → 로봇개 구동
```

### 5.2 VLM (Vision-Language Model) 구동

로봇개의 **시각 정보 + 언어 명령**을 결합하는 모델:

| 모델 | 활용 | 비고 |
|------|------|------|
| **LLaVA-Next 7B** (INT4) | "빨간 공을 가리켜" → 시각적 객체 지시 | 7B 모델도 INT4 양자화로 구동 가능 |
| **PaliGemma 3B** | 장면 설명, 객체 속성 질의 | 경량, Orin에 적합 |
| **RT-2 / Octo** | VLA — 시각-언어-행동 통합 | 로봇개에 가장 직접적 |

### 5.3 VLA (Vision-Language-Action) 모델

**Sim-to-Real의 핵심**: VLA는 시각 입력 + 언어 명령을 받아 **직접 모터 제어값을 출력**합니다.

```
카메라 이미지 ─┐
              ├── VLA 모델 ──→ 모터 위치/속도 명령
언어 명령 ────┘
```

| 모델 | 특징 | 로봇개 적용 |
|------|------|-----------|
| **Octo** | 오픈소스, 다양한 로봇형태 학습 | 걷기, 회전, 앉기 등 기본 동작 |
| **RT-2** | 구글, 인터넷 규모 사전학습 | 복잡한 명령-행동 매핑 |
| **π0 (Pi-zero)** | Flow matching 기반 VLA | 부드러운 연속 동작 생성 |

### 5.4 프롬프트 설계 및 비전-언어 모델 활용

**프롬프트 엔지니어링 패턴 (로봇개)**:

```
[시스템 프롬프트]
당신은 로봇개 제어 시스템입니다. 다음 규칙을 따르세요:
- 안전을 최우선으로 합니다
- 모터 한계를 초과하는 명령은 거절합니다
- 항상 현재 상태를 고려하여 응답합니다

[사용자 입력]
"앞에 있는 장애물을 피해서 오른쪽으로 가"
```

| 기법 | 설명 | 적용 |
|------|------|------|
| **Few-shot** | 예시 명령-행동 쌍 제공 | 새 동작 학습 가속 |
| **Chain-of-Thought** | "관찰 → 추론 → 행동" 단계적 출력 | 복잡한 장애물 회피 경로 |
| **Structured Output** | JSON 형식의 제어 명령 강제 | 파싱 없이 직접 모터 제어 |

---

## 6. OpenUSD (Universal Scene Description)

### 6.1 OpenUSD 개념

OpenUSD는 **3D 장면 데이터를 표현, 교환, 합성**하기 위한 프레임워크입니다. Isaac Sim의 모든 3D 콘텐츠는 USD로 표현됩니다.

```
USD 기본 개념
├── Prim (Primitive): 장면의 모든 요소 (로봇, 센서, 환경)
├── Layer: 데이터 계층 구조 (수정 내역 분리 관리)
├── Composition: 여러 USD 파일을 합성하는 규칙
├── Variant: 같은 모델의 다른 버전 (로봇개 스킨 변경 등)
└── Schema: 데이터 타입 정의 (리깅, 물리 속성)
```

### 6.2 로봇개 개발에서의 USD 활용

| 활용 | 설명 |
|------|------|
| **로봇 모델링** | 로봇개 형상, 관절 구조, 물리 속성을 USD로 정의 |
| **환경 구성** | 시뮬레이션 환경(실내/실외)을 USD 에셋으로 구성 |
| **센서 부착** | 카메라, LiDAR, IMU를 USD Scene에 배치 |
| **애니메이션** | 보행, 달리기 등 동작을 USD 애니메이션으로 저장 |
| **에셋 재사용** | 여러 시나리오에서 동일 USD 참조 (Non-destructive) |

### 6.3 USD 작업 흐름

```
Workstation (Isaac Sim)          버전 관리             Jetson (추론)
      │                              │                      │
      ├── 로봇개 USD 설계 ──────► USD 파일 저장 ──────► URDF 추출
      │   (리깅, 콜리전, 관절)       (Git LFS)          (ROS2 호환)
      │                                                    │
      ├── 환경 USD 구성                               로봇개 HW-SW
      │   (바닥, 장애물, 조명)                         (변환 불필요)
      │
      └── 시뮬레이션 파라미터 USD
          (마찰력, 중력, 센서 노이즈)
```

### 6.4 ROS2와 USD의 관계

```
Isaac Sim (USD)                      ROS2
┌──────────────────┐          ┌──────────────────┐
│  로봇 USD 모델    │  ───►   │  robot_state_publisher │
│  (관절, 링크)     │  URDF   │  → /joint_states  │
└──────────────────┘          └──────────────────┘
┌──────────────────┐          ┌──────────────────┐
│  센서 USD 설정    │  ───►   │  sensor_msgs     │
│  (FOV, 해상도)    │  ROS2   │  → /camera, /scan│
└──────────────────┘          └──────────────────┘
```

> **핵심 포인트**: USD는 Isaac Sim의 **표현 형식**이고, ROS2는 **통신 형식**입니다. USD로 모델링하고 ROS2로 데이터를 주고받습니다.

---

## 7. 개발 파이프라인 (단계별)

### Phase 1: Workstation 환경 구축

```
보유 장비
├── GPU: RTX 5090 Laptop 24GB ✅ (Ideal 수준 초과)
├── 시스템 RAM: 확인 필요 (Isaac Sim 최소 32GB, 권장 64GB)
├── 저장소: 50GB 이상 SSD 확보 필요
├── OS: Ubuntu 22.04 듀얼부팅 또는 WSL2 고려
└── 네트워크: Jetson과 동일 LAN (유선 권장)
```

> Isaac Sim은 Windows 네이티브도 지원하지만, ROS2 연동 안정성을 위해 **Ubuntu 22.04 듀얼부팅**을 권장합니다. (노트북이므로 WSL2도 대안이 될 수 있으나 GPU 가속 ROS2 노드에서 제약이 있을 수 있습니다.)

설치:
- NVIDIA Isaac Sim (공식 페이지에서 다운로드)
- ROS2 Humble (Ubuntu)
- Isaac Sim Compatibility Checker 로 사전 검증

### Phase 2: Jetson Nano 2GB — ROS2 기초 체험

```
목적: ROS2 생태계 첫 경험, 임베디드 리눅스 적응
기간: 1~2주

학습 내용
├── Jetson Nano 2GB 셋업 (JetPack, Headless SSH)
├── ROS2 기본: publisher / subscriber / service
├── 간단한 센서 노드 작성 (GPIO, I2C)
├── rqt_graph, ros2 topic, ros2 bag 기초
└── 한계 인지: 2GB로는 Isaac ROS 패키지 실행 불가
```

> **이 보드의 가치**: "된다/안된다"를 직접 체험하고, ROS2의 기본 개념을 저리스크 환경에서 익히는 것

### Phase 3: Jetson TX2 — 중간 단계

```
목적: 실제 로봇 SW 스택 포팅 경험, 성능 병목 이해
기간: 2~4주

학습 내용
├── JetPack 4.x / 5.x 설치 및 환경 비교
├── ROS2 네비게이션 스택 (Nav2) 기초 실행
├── SLAM Toolbox / Cartographer 경량 테스트
├── Isaac ROS 중 경량 패키지 선별 실행
│   (예: isaac_ros_dnn_inference — 작은 모델만)
└── Orin Nano Super와의 성능 차이 정량 측정
```

> **이 보드의 가치**: Pascal 256-core의 한계를 체감하고, Orin Super와의 차이를 데이터로 비교 가능

### Phase 4: Jetson Orin Nano Super — 본개발 + HIL 연동

```
목적: 실제 로봇개 SW 스택 개발 및 Isaac Sim HIL 연동
기간: 지속적

단계
├── 4-1. 보드 셋업
│   ├── JetPack 6.x 설치
│   ├── Docker + Isaac ROS 컨테이너 구성
│   └── jtop 모니터링 환경 구축
│
├── 4-2. 로봇개 기본 SW 스택
│   ├── ROS2 제어 노드 (cmd_vel → joint 명령 변환)
│   ├── IMU / Odometry 퓨전 (robot_localization)
│   ├── VSLAM (Isaac ROS VSLAM 또는 ORB-SLAM3)
│   └── 경로 계획 (Nav2 또는 커스텀)
│
└── 4-3. Isaac Sim HIL 연동
    ├── Workstation에서 로봇개 URDF/USD 임포트
    ├── ROS2 Bridge 활성화
    ├── 시뮬레이션 센서 데이터 → Jetson으로 전송
    ├── Jetson의 추론 결과 → 시뮬레이션으로 피드백
    └── HIL 루프 튜닝 (지연 시간, 동기화)
```

### Phase 5: OpenUSD 실습

```
목적: USD를 활용한 로봇 모델링 및 환경 구성
기간: 2~3주

학습 내용
├── USD 기본 구조 이해 (Prim, Layer, Composition)
├── Isaac Sim에서 로봇개 USD 모델 임포트/수정
├── 관절 리깅 (Articulation, Joint, Collision)
├── 물리 속성 부여 (질량, 관성, 마찰)
├── 센서 USD 설정 (카메라 POV, LiDAR 해상도)
├── Variant를 활용한 환경 조건 변경 (주/야, 실내/외)
└── USD 레이어를 활용한 Non-destructive 편집
```

### Phase 6: Isaac Sim 물리 시뮬레이션 심화

```
목적: 물리 엔진 활용, 현실적인 로봇 시뮬레이션 구현
기간: 3~4주

학습 내용
├── PhysX 물리 엔진 이해 (강체, 관절, 충돌)
├── 로봇개 보행 시뮬레이션 (관절 제어, 안정성)
├── 지형 상호작용 (경사로, 계단, 요철)
├── 현실적인 센서 피드백 생성
│   ├── 카메라 노이즈 + 조명 변동
│   ├── LiDAR 드롭아웃/반사 노이즈
│   └── IMU 드리프트 모델링
├── Domination / Branch / Stepping 모드 활용
└── 다중 에피소드 배치 시뮬레이션 (RL 학습용)
```

### Phase 7: AI 파이프라인 개발

```
목적: 모델 선정 → 학습 → 최적화 → Jetson 배포까지 전 과정
기간: 지속적

단계
├── 7-1. 모델 선정
│   ├── 과제 분석 (물체 감지 / VSLAM / VLA / 음성 명령)
│   ├── Jetson Orin Nano Super 제약 내 모델 선택
│   │   - YOLOv8n/m (감지), FastSAM (분할)
│   │   - Gemma 2B / Phi-3 (LLM)
│   │   - LLaVA-Next 7B INT4 (VLM)
│   │   - Octo (VLA)
│   └── 모델 벤치마크 (TOPS, 메모리, 지연시간)
│
├── 7-2. 데이터 수집 및 합성
│   ├── Isaac Sim Replicator로 합성 데이터 생성
│   ├── 도메인 랜덤화 (조명, 텍스처, 자세)
│   ├── GT 레이블 자동 생성 (바운딩 박스, 세그멘테이션)
│   └── ROS2 bag 기록 → 실제 센서 데이터 수집
│
├── 7-3. 모델 학습 및 최적화
│   ├── 전이 학습 (Pre-trained → 로봇개 도메인)
│   ├── NVIDIA TAO Toolkit 활용 학습
│   ├── INT8 양자화 (TensorRT)
│   └── 모델 압축 (가지치기, 증류)
│
└── 7-4. Jetson 배포 및 모니터링
    ├── TensorRT 엔진 빌드 (Orin Nano Super)
    ├── DeepStream / Isaac ROS 파이프라인 통합
    ├── Triton Inference Server (엣지 모드)
    └── 성능 모니터링 (지연 시간, FPS, 전력)
```

---

## 8. HIL (Hardware-in-the-Loop) 상세 흐름

이 구조가 이 프로젝트의 **핵심 기술 파이프라인**입니다.

```
[Isaac Sim — Workstation]                    [Jetson Orin Nano Super]
         │                                           │
         │  ┌─ /camera/image_raw (시뮬레이션) ──────► │  Isaac ROS 추론
         │  │  ┌─ /scan (시뮬레이션 LiDAR) ──────────► │  (PeopleSegNet,
         │  │  │  ┌─ /imu (시뮬레이션 IMU) ──────────► │   VSLAM, Detections)
         │  │  │  │                                     │
         │  │  │  │                                     ▼
         │  │  │  │                              로봇개 제어 SW
         │  │  │  │                              (경로 계획, cmd_vel)
         │  │  │  │                                     │
         │  ◄──┴──┴──┴─ /cmd_vel ────────────────────── │
         │                     (시뮬레이션 로봇 구동)     │
         │                                           │
         ▼                                           ▼
   물리 시뮬레이션 루프                      실제 구동될 SW 검증
   (센서 피드백 생성)                        (버그/병목 조기 발견)
```

### HIL이 주는 이점

| 항목 | HIL 없음 (순수 시뮬레이션) | HIL 도입 |
|------|--------------------------|---------|
| AI 추론 | Workstation GPU 사용 (실환경과 다름) | **실제 Jetson에서 추론** |
| SW 검증 | PC 환경에서만 테스트 | **타겟 HW에서 직접 검증** |
| 성능 측정 | 불가 | **실측 가능 (FPS, 지연시간)** |
| 센서 특성 반영 | 완벽한 이상값 | **실제 센서 노이즈 특성 반영** |
| Sim-to-Real 갭 | 큼 | **HIL로 갭 축소** |

---

## 9. Sim-to-Real 연계

HIL을 넘어, 시뮬레이션 데이터를 실제 로봇개에 적용하는 전 과정입니다.

### 9.1 합성 데이터 생성 (Synthetic Data Generation)

Isaac Sim의 **Replicator**를 활용한 합성 데이터 파이프라인:

```
                    Isaac Sim Replicator
┌──────────────────────────────────────────────────┐
│  3D Scene           │   Sensor Simulation       │
│  ┌──────────┐       │   ┌──────────────────┐    │
│  │ 로봇개    │       │   │ 카메라 (RGB, Depth)│    │
│  │ 환경      │       │   │ LiDAR            │    │
│  │ 장애물    │       │   │ Segmentation     │    │
│  │ 조명      │       │   │ Bounding Box     │    │
│  └──────────┘       │   └──────────────────┘    │
│         │           │           │                │
│         ▼           │           ▼                │
│  도메인 랜덤화      │    GT 레이블 자동 생성    │
│  ┌──────────────┐   │   ┌────────────────────┐  │
│  │ 조명 변경     │   │   │ 객체 위치/클래스    │  │
│  │ 텍스처 변경   │   │   │ 키포인트           │  │
│  │ 카메라 자세   │   │   │ 관절 각도          │  │
│  │ 배경 변경     │   │   │ 충돌/접촉 정보     │  │
│  └──────────────┘   │   └────────────────────┘  │
└──────────────────────────────────────────────────┘
```

| 데이터 유형 | 생성 방법 | 용도 |
|-----------|---------|------|
| **RGB 이미지** | Isaac Sim 카메라 렌더링 | 객체 감지, VSLAM 학습 |
| **Depth + Segmentation** | Replicator GT | 장애물 회피 학습 |
| **LiDAR 포인트 클라우드** | LiDAR 센서 시뮬레이션 | SLAM, 매핑 |
| **관절 상태 + IMU** | PhysX 물리 연산 결과 | 보행 제어 학습 |
| **멀티모달 쌍** | 동기화된 센서 출력 | VLM/VLA 학습 데이터 |

**도메인 랜덤화** (Domain Randomization): 합성 데이터만으로 학습한 모델이 실제 환경에서도 동작하도록 하기 위한 핵심 기법

```
도메인 랜덤화 파라미터 (Isaac Sim)
├── 조명: 방향, 강도, 색온도 무작위화
├── 텍스처: 바닥/벽 재질 랜덤 교체
├── 카메라: 노이즈, 블러, 노출 랜덤화
├── 객체: 위치, 크기, 색상 무작위화
└── 물리: 마찰, 중력, 질량 미세 변동
```

### 9.2 시뮬레이션 데이터 활용 모델 검증

```
훈련 데이터 (합성 + 실제)       검증 (HIL)          실환경 배포
      │                           │                    │
      ▼                           ▼                    ▼
┌──────────────┐          ┌──────────────┐     ┌──────────────┐
│ 사전학습 모델  │  ───►   │  HIL 검증    │ ──► │  실제 로봇개 │
│ (ImageNet 등) │          │  (Isaac Sim  │     │  (Orin Super)│
└──────────────┘          │   + Jetson)  │     └──────────────┘
      │                    └──────────────┘            │
      │                          │                     │
      ▼                          ▼                     ▼
┌──────────────┐          ┌──────────────┐     ┌──────────────┐
│ 합성 데이터   │          │  시뮬레이션   │     │  실환경       │
│ 파인튜닝     │          │  정확도 측정  │     │  성능 측정    │
└──────────────┘          └──────────────┘     └──────────────┘
```

**모델 검증 메트릭**:

| 단계 | 측정 항목 | 목표 |
|------|----------|------|
| 합성 데이터 학습 후 | 시뮬레이션 내 정확도 | mAP > 0.85 (감지) |
| HIL 검증 | 시뮬레이션 데이터 → Jetson 추론 | 지연 < 30ms |
| 실환경 테스트 | 실제 센서 → Jetson 추론 | Sim-to-Real 갭 < 10% |
| Sim-to-Real Ratio | (실환경 정확도 / 시뮬레이션 정확도) | > 0.9 |

### 9.3 Sim-to-Real 전체 파이프라인

```
1. Isaac Sim에서 로봇개 USD 모델링
         │
2. 센서 설정 및 환경 구성 (도메인 랜덤화 포함)
         │
3. 합성 데이터 생성 (Replicator)
         │
4. 모델 학습 (TAO Toolkit / PyTorch)
         │
5. TensorRT 변환 + INT8 양자화
         │
6. HIL 검증 (Isaac Sim → Jetson Orin Nano Super)
         │
7. 실제 로봇개 하드웨어 탑재
         │
8. 실환경 테스트 → Sim-to-Real Ratio 측정
         │
9. 갭 분석 → 도메인 랜덤화 파라미터 조정 → 3번으로 반복
```

---

## 10. AI 파이프라인 개발

로봇개에 탑재될 AI 기능의 **모델 선정 → 학습 → 최적화 → 배포** 전 과정을 다룹니다.

### 10.1 로봇개 AI 기능 분류

| 계층 | 기능 | 추천 모델 | 실행 주체 |
|------|------|----------|---------|
| **인지 (Perception)** | 객체 감지 | YOLOv8n/m | Jetson (실시간) |
| | 사람 인식/추종 | PeopleSemSegNet | Jetson (실시간) |
| | 장면 이해 | LLaVA-Next 7B (INT4) | Jetson (요청 시) |
| **판단 (Reasoning)** | 음성 명령 이해 | Whisper + Gemma 2B | Jetson (요청 시) |
| | 복잡한 추론 | 클라우드 LLM | Workstation (비동기) |
| **행동 (Action)** | 보행 제어 | DRL 정책 (Isaac Lab 학습) | Jetson (실시간) |
| | VLA 명령-행동 | Octo / RT-2 | Jetson (실시간) |
| **매핑 (Mapping)** | VSLAM | Isaac ROS VSLAM | Jetson (실시간) |
| | 경로 계획 | Nav2 커스텀 | Jetson (실시간) |

### 10.2 모델 선정 의사결정 트리

```
로봇개에 필요한 AI 기능?
│
├── 실시간 객체 감지? → YOLOv8n (가장 가벼움) / YOLOv8m (더 정확함)
│
├── 사람/장애물 분할? → FastSAM / PeopleSemSegNet
│
├── 언어 명령 이해?
│   ├── 간단한 명령 ("앞으로 가", "멈춰") → 소형 LLM (Gemma 2B, Phi-3)
│   └── 복잡한 지시 → VLM (LLaVA-Next 7B INT4) 또는 클라우드 LLM
│
├── 시각-언어-행동 통합?
│   └── Octo (오픈소스, Jetson 구동 가능)
│
└── 심층 강화학습?
    └── Isaac Lab + PPO (Workstation 학습 → Jetson 배포)
```

### 10.3 학습 데이터 흐름

```
          Isaac Sim                    Workstation                 Jetson Orin Nano Super
              │                            │                             │
  ┌───────────┴───────────┐                │                             │
  │ 합성 데이터 생성        │                │                             │
  │ (Replicator)          │                │                             │
  └───────────┬───────────┘                │                             │
              ▼                            │                             │
  ┌────────────────────┐    ┌────────────────────────────┐              │
  │ 도메인 랜덤화       │───►│ 모델 학습 (TAOKit/PyTorch) │              │
  │ GT 레이블           │    └────────────┬───────────────┘              │
  └────────────────────┘                 │                              │
                                         ▼                              │
                               ┌────────────────────┐                   │
                               │ ONNX → TensorRT    │──────────────────►│
                               │ INT8 양자화        │  TensorRT 엔진     │
                               └────────────────────┘                   │
                                                                        ▼
                                                               ┌────────────────┐
                                                               │ Isaac ROS      │
                                                               │ DeepStream     │
                                                               │ 추론 파이프라인│
                                                               └────────────────┘
```

### 10.4 모델 최적화 상세

Orin Nano Super(67 TOPS, 8GB)에서 최대 성능을 내기 위한 최적화:

| 최적화 기법 | 효과 | 적용 |
|-----------|------|------|
| **INT8 양자화** | 메모리 4배 감소, 처리량 2-3배 향상 | TensorRT 필수 |
| **TensorRT 엔진** | 커널 융합, 메모리 재사용 | 모든 모델에 적용 |
| **배치 처리** | GPU 활용률 향상 | 다중 카메라 입력 |
| **DLA (Deep Learning Accelerator)** | 전력 효율 추론 | Orin Super DLA 활용 |
| **CUDA 그래프** | 커널 실행 오버헤드 제거 | 실시간 루프 최적화 |
| **가지치기 (Pruning)** | 모델 크기 30-50% 감소 | TAO Toolkit |
| **지식 증류 (Distillation)** | 큰 모델 → 작은 모델로 전이 | 학습 파이프라인 |

### 10.5 실시간 제어 루프 (Jetson 내부)

```
          센서 입력
             │
   ┌─────────▼─────────┐
   │  Camera (30fps)   │
   │  LiDAR (10Hz)     │
   │  IMU (200Hz)      │
   └─────────┬─────────┘
             │
   ┌─────────▼─────────┐
   │  YOLOv8 감지       │  ← TensorRT (INT8)
   │  VSLAM             │  ← Isaac ROS
   │  IMU 퓨전          │  ← robot_localization
   └─────────┬─────────┘
             │
   ┌─────────▼─────────┐
   │  상황 이해 + 판단  │  ← Gemma 2B / Octo (주기적)
   │  경로 계획         │  ← Nav2 커스텀
   └─────────┬─────────┘
             │
   ┌─────────▼─────────┐
   │  cmd_vel → 관절 변환 │  ← ROS2 제어 노드
   │  모터 명령 전송     │
   └──────────────────┘
             │
         로봇개 행동
```

---

## 11. 보드별 예상 성능 비교 (로봇개 작업 부하)

| 작업 항목 | Nano 2GB | TX2 | Orin Nano Super |
|----------|:--------:|:---:|:--------------:|
| ROS2 기본 노드 실행 | ✅ 가능 | ✅ 가능 | ✅ 가능 |
| Nav2 경로 계획 | ❌ | ⚠️ 느림 | ✅ ✅ 여유 |
| VSLAM | ❌ | ❌ (메모리 부족) | ✅ 가능 |
| YOLOv8n 실시간 추론 | ❌ | ⚠️ 5-10 FPS | ✅ 90-100 FPS |
| PeopleSemSegNet | ❌ | ❌ (메모리 부족) | ✅ 가능 |
| 다중 센서 동시처리 | ❌ | ❌ (대역폭 부족) | ✅ 102 GB/s |
| Isaac ROS 풀스택 | ❌ | ❌ | ✅ ✅ |
| HIL 연동 (Isaac Sim) | ❌ | ❌ | ✅ ✅ |
| **교육용 제품화** | ❌ | ❌ | **✅ 적합** |

---

## 12. 공식 튜토리얼 및 참고 자료

### Isaac Sim 공식 튜토리얼

| 튜토리얼 | 링크 | 주요 내용 |
|---------|------|---------|
| URDF Import: Turtlebot | [링크](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/ros_tutorials/tutorial_ros_turtlebot.html) | TurtleBot3 URDF를 Isaac Sim으로 가져오기 |
| Driving TurtleBot via ROS2 (5.1.0) | [링크](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/ros2_tutorials/tutorial_ros2_drive_turtlebot.html) | ROS2 Twist 메시지로 TurtleBot3 구동 |
| Driving TurtleBot via ROS2 (4.5.0) | [링크](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/ros2_tutorials/tutorial_ros2_drive_turtlebot.html) | (4.5.0 버전) |
| ROS2 Bridge Python 예제 | [링크](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/ros2_tutorials/tutorial_ros2_python.html) | Python 스크립트로 ROS2 브리지 제어 |
| Omniverse Streaming Client | [링크](https://docs.isaacsim.omniverse.nvidia.com/4.5.0/installation/manual_livestream_clients.html) | Headless Isaac Sim 원격 스트리밍 |

### Jetson + HIL 공식 과정

| 과정 | 링크 | 주요 내용 |
|------|------|---------|
| NVIDIA DLI - Getting Started with Isaac Sim | [링크](https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-sim/latest/index.html) | Isaac Sim 종합 입문 과정 |
| HIL in Isaac Sim — Jetson 환경 설정 | [링크](https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-sim/latest/leveraging-ros-2-and-hil-in-isaac-sim/03-setting-up-the-jetson-environment.html) | Jetson Orin에 Isaac ROS 설정 |
| HIL — Isaac ROS 배포 | [링크](https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-sim/latest/leveraging-ros-2-and-hil-in-isaac-sim/04-deploying-isaac-ros-on-jetson.html) | Isaac Sim + Jetson HIL 실습 |

### YouTube

| 영상 | 링크 |
|------|------|
| Isaac Sim TurtleBot Crash Course: ROS2 Navigation | https://www.youtube.com/watch?v=3cWQsvpwvQU |
| Isaac Sim & Isaac Lab: Full Guide (Nikodem Bartnik) | https://www.youtube.com/watch?v=tQziqSx-F80 |

### NVIDIA GTC 발표

| 세션 | 링크 |
|------|------|
| Building Multi-Robot Scenarios with Isaac Sim and ROS2 (GTC 2026) | https://www.nvidia.com/en-us/on-demand/session/gtc26-dlit81699 |

### 생성형 AI / LLM / VLM

| 자료 | 링크 | 비고 |
|------|------|------|
| NVIDIA TensorRT LLM | https://github.com/NVIDIA/TensorRT-LLM | Jetson LLM 최적화 |
| LLaVA (VLM) | https://llava-vl.github.io/ | 비전-언어 모델 |
| Octo (VLA) | https://octo-models.github.io/ | 로봇 VLA 모델 |
| NVIDIA TAO Toolkit | https://developer.nvidia.com/tao-toolkit | 모델 학습/최적화 |
| Hugging Face Optimum | https://huggingface.co/docs/optimum/index | 엣지 양자화 |

### OpenUSD

| 자료 | 링크 | 비고 |
|------|------|------|
| OpenUSD 공식 문서 | https://openusd.org/ | USD 기본 개념 |
| NVIDIA Omniverse USD | https://developer.nvidia.com/usd | Omniverse USD 가이드 |
| Isaac Sim USD 튜토리얼 | https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup/tutorial_rig_robot.html | 로봇 USD 리깅 |

### Sim-to-Real / 합성 데이터

| 자료 | 링크 | 비고 |
|------|------|------|
| Isaac Sim Replicator | https://docs.isaacsim.omniverse.nvidia.com/latest/replicator/index.html | 합성 데이터 생성 |
| Domain Randomization | https://openai.com/index/generalizing-from-simulation/ | OpenAI DR 논문 |

---

## 13. 추천 학습 로드맵 (시간순)

```
주차  | Nano 2GB         | TX2               | Orin Nano Super          | Workstation
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
 1-2  │ ✅ 보드 셋업     │ 대기              │ 대기                    │ Isaac Sim 설치
      │ 🎓 생성형 AI 이론 │                   │                         │ Transformer 기초 학습
      │    (Transformer)  │                   │                         │
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
 3-4  │ ✅ 센서 노드     │ ✅ 보드 셋업      │ 대기                    │ 🎓 생성형 AI 실습
      │ ROS2 통신 실습   │ ROS2 기초         │                         │ LLM/VLM/VLA 구동
      │                  │                   │                         │ 프롬프트 설계
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
 5-6  │ ❌ 실습 완료     │ ✅ Nav2 경량      │ ✅ 보드 셋업           │ 🎓 OpenUSD 학습
      │ (정리)           │ SLAM 기초         │ Isaac ROS 설치          │ USD 구조, 레이어
      │                  │                   │ 🎓 생성형 AI 실습       │ USD 리깅 실습
      │                  │                   │    (소형 LLM 구동)      │
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
 7-8  │                  │ ❌ 정리           │ ✅ VSLAM 구동          │ 로봇개 USD 모델링
      │                  │ 성능 비교         │ YOLO 추론              │ 물리 시뮬레이션 설정
      │                  │                   │                         │ URDF 임포트
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
 9-10 │                  │                   │ ✅ HIL 연동             │ Isaac Sim 물리 심화
      │                  │                   │ Isaac Sim ↔ Jetson      │ 관절/지형/센서 노이즈
      │                  │                   │                         │ 센서 피드백 생성
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
11-12 │                  │                   │ ✅ AI 파이프라인        │ 합성 데이터 생성
      │                  │                   │    모델 선정/최적화     │ (Replicator)
      │                  │                   │    TensorRT 변환        │ 도메인 랜덤화
      │                  │                   │                         │ GT 레이블 생성
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
13-14 │                  │                   │ ✅ Sim-to-Real 검증    │ HIL 반복 튜닝
      │                  │                   │    실환경 테스트        │ 모델 재학습 지원
      │                  │                   │    Sim-to-Real Ratio    │
──────┼──────────────────┼───────────────────┼─────────────────────────┼────────────────────
15-16 │                  │                   │ ✅ 최종 제품화         │ 최종 검증
      │                  │                   │    Orin Super 탑재      │ 문서화
```

---

## 14. 예산 및 구매 고려 사항

| 항목 | 예상 비용 | 비고 |
|------|----------|------|
| **Workstation GPU** | **보유 중 (RTX 5090 Laptop 24GB)** ✅ | 별도 구매 불필요 |
| **Jetson Nano 2GB** | 이미 보유 | — |
| **Jetson TX2** | 이미 보유 | — |
| **Jetson Orin Nano Super DevKit 8GB** | ~$459-519 | 정식 DevKit 기준 |
| **로봇개 하드웨어** (프레임, 모터, 배터리) | 별도 | Orin Nano Super 탑재 공간 확보 필요 |

> **예산 절감 포인트**: RTX 5090 노트북을 이미 보유하고 있어, 고가의 Workstation GPU를 별도로 구매할 필요가 없습니다. Isaac Sim 운영 측면에서 가장 큰 비용 항목이 해결된 셈입니다.

---

## 15. 최종 결론

| 질문 | 답변 |
|------|------|
| **Isaac Sim이 Jetson에서 직접 구동되나요?** | ❌ **아니오.** Workstation(RTX GPU)에서만 실행됩니다. |
| **그래도 로봇개 개발이 가능한가요?** | ✅ **가능합니다.** HIL 구조가 NVIDIA의 공식 권장 파이프라인입니다. |
| **Orin Nano Super가 의미가 있나요?** | ✅ **네, 큽니다.** 67 TOPS + 102 GB/s로 교육용 제품 타겟에 적합합니다. |
| **Nano 2GB / TX2를 활용할 가치가 있나요?** | ✅ **충분합니다.** 성능 차이를 직접 체감하고, 단계별 학습이 가능합니다. |
| **최종 교육용 제품 타겟으로 무엇을 선택해야 하나요?** | **Jetson Orin Nano Super 8GB** — 가성비 + 성능 + Isaac ROS 풀지원 |

### 교육 과정 전체 구성

```
이론                              실습
┌────────────────────┐      ┌────────────────────┐
│ 생성형 AI 이론      │ ──►  │ 생성형 AI 실습     │
│ (Transformer, Edge) │      │ (LLM/VLM/VLA 구동) │
└────────────────────┘      └────────────────────┘
        │                           │
        ▼                           ▼
┌──────────────────────────────────────────────┐
│              OpenUSD + Isaac Sim             │
│     (3D 모델링 → 물리 시뮬레이션 → HIL)      │
└──────────────────────────────────────────────┘
        │                           │
        ▼                           ▼
┌────────────────────┐      ┌────────────────────┐
│ AI 파이프라인       │ ──►  │ Sim-to-Real       │
│ (모델→학습→최적화)  │      │ (합성데이터→실환경) │
└────────────────────┘      └────────────────────┘
```

### 보유 장비 최종 점검

| 장비 | 상태 | 활용 |
|------|------|------|
| **RTX 5090 Laptop 24GB** | ✅ 보유 완료 | Isaac Sim 실행 Workstation (Ideal 이상) + LLM/VLM 학습 |
| **Jetson Nano 2GB** | ✅ 보유 완료 | ROS2 기초 학습 |
| **Jetson TX2** | ✅ 보유 완료 | 중급 SW 포팅 경험 |
| **Jetson Orin Nano Super** | 🛒 구매 필요 | 최종 교육용 제품 타겟 |

### 최종 요약

| 영역 | 내용 | 난이도 |
|------|------|:------:|
| **생성형 AI 이론** | Transformer 구조, Edge 환경 생성형 AI | ★★★ |
| **생성형 AI 실습** | LLM/VLM/VLA 구동, 프롬프트 설계 | ★★★ |
| **OpenUSD** | USD 기반 로봇 모델링, 환경 구성 | ★★ |
| **Isaac Sim 물리 시뮬레이션** | PhysX, 관절 제어, 센서 피드백 | ★★★ |
| **HIL (Hardware-in-the-Loop)** | Isaac Sim ↔ Jetson ROS2 연동 | ★★★★ |
| **AI 파이프라인 개발** | 모델 선정 → 학습 → TensorRT → 배포 | ★★★★ |
| **Sim-to-Real 연계** | 합성 데이터 생성, 도메인 랜덤화, 모델 검증 | ★★★★★ |

### 핵심 One-Liner

> **RTX 5090 노트북에서 Isaac Sim으로 시뮬레이션하고, Jetson Orin Nano Super는 실제 로봇개 SW를 실행하며, 둘은 ROS2로 연결된다. 생성형 AI와 USD를 기반으로 한 Sim-to-Real 파이프라인이 전체 과정의 백본이다.**
>
> **Isaac Sim 구동을 위한 추가 GPU 구매는 전혀 필요 없습니다.**
