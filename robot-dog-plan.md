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

## 4. 개발 파이프라인 (단계별)

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

### Phase 4: Jetson Orin Nano Super — 본개발 + HIL

```
목적: 실제 로봇개 SW 스택 개발 및 Isaac Sim 연동 검증
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
├── 4-3. Isaac Sim HIL 연동
│   ├── Workstation에서 로봇개 URDF/USD 임포트
│   ├── ROS2 Bridge 활성화
│   ├── 시뮬레이션 센서 데이터 → Jetson으로 전송
│   ├── Jetson의 추론 결과 → 시뮬레이션으로 피드백
│   └── HIL 루프 튜닝 (지연 시간, 동기화)
│
└── 4-4. Sim-to-Real
    ├── 시뮬레이션에서 검증 완료된 SW 스택
    ├── 실제 로봇개 하드웨어에 Orin Nano Super 탑재
    ├── 센서 캘리브레이션
    └── 실환경 테스트
```

---

## 5. HIL (Hardware-in-the-Loop) 상세 흐름

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

## 6. 보드별 예상 성능 비교 (로봇개 작업 부하)

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

## 7. 공식 튜토리얼 및 참고 자료

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

---

## 8. 추천 학습 로드맵 (시간순)

```
주차  | Nano 2GB        | TX2              | Orin Nano Super        | Workstation
──────┼─────────────────┼──────────────────┼───────────────────────┼────────────────────
 1-2  │ ✅ 보드 셋업    │ 대기             │ 대기                  │ Isaac Sim 설치
      │ ROS2 기초       │                  │                       │ 튜토리얼 진행
──────┼─────────────────┼──────────────────┼───────────────────────┼────────────────────
 3-4  │ ✅ 센서 노드    │ ✅ 보드 셋업     │ 대기                  │ URDF 임포트
      │ ROS2 통신 실습  │ ROS2 기초        │                       │ TurtleBot 구동
──────┼─────────────────┼──────────────────┼───────────────────────┼────────────────────
 5-6  │ ❌ 실습 완료    │ ✅ Nav2 경량     │ ✅ 보드 셋업         │ 로봇개 USD 모델링
      │ (정리)          │ SLAM 기초        │ Isaac ROS 설치        │ 센서 구성
──────┼─────────────────┼──────────────────┼───────────────────────┼────────────────────
 7-8  │                 │ ❌ 정리          │ ✅ VSLAM 구동        │ HIL 환경 구성
      │                 │ 성능 비교        │ YOLO 추론            │ ROS2 브리지 연결
──────┼─────────────────┼──────────────────┼───────────────────────┼────────────────────
9-12  │                 │                  │ ✅ HIL 본격 연동     │ HIL 연동
      │                 │                  │ Isaac Sim ↔ Jetson   │ 반복 튜닝
──────┼─────────────────┼──────────────────┼───────────────────────┼────────────────────
13-16 │                 │                  │ ✅ Sim-to-Real       │ 최종 검증 지원
      │                 │                  │ 실제 로봇개 탑재     │
```

---

## 9. 예산 및 구매 고려 사항

| 항목 | 예상 비용 | 비고 |
|------|----------|------|
| **Workstation GPU** | **보유 중 (RTX 5090 Laptop 24GB)** ✅ | 별도 구매 불필요 |
| **Jetson Nano 2GB** | 이미 보유 | — |
| **Jetson TX2** | 이미 보유 | — |
| **Jetson Orin Nano Super DevKit 8GB** | ~$459-519 | 정식 DevKit 기준 |
| **로봇개 하드웨어** (프레임, 모터, 배터리) | 별도 | Orin Nano Super 탑재 공간 확보 필요 |

> **예산 절감 포인트**: RTX 5090 노트북을 이미 보유하고 있어, 고가의 Workstation GPU를 별도로 구매할 필요가 없습니다. Isaac Sim 운영 측면에서 가장 큰 비용 항목이 해결된 셈입니다.

---

## 10. 최종 결론

| 질문 | 답변 |
|------|------|
| **Isaac Sim이 Jetson에서 직접 구동되나요?** | ❌ **아니오.** Workstation(RTX GPU)에서만 실행됩니다. |
| **그래도 로봇개 개발이 가능한가요?** | ✅ **가능합니다.** HIL 구조가 NVIDIA의 공식 권장 파이프라인입니다. |
| **Orin Nano Super가 의미가 있나요?** | ✅ **네, 큽니다.** 67 TOPS + 102 GB/s로 교육용 제품 타겟에 적합합니다. |
| **Nano 2GB / TX2를 활용할 가치가 있나요?** | ✅ **충분합니다.** 성능 차이를 직접 체감하고, 단계별 학습이 가능합니다. |
| **최종 교육용 제품 타겟으로 무엇을 선택해야 하나요?** | **Jetson Orin Nano Super 8GB** — 가성비 + 성능 + Isaac ROS 풀지원 |

### 보유 장비 최종 점검

| 장비 | 상태 | 활용 |
|------|------|------|
| **RTX 5090 Laptop 24GB** | ✅ 보유 완료 | Isaac Sim 실행 Workstation (Ideal 이상) |
| **Jetson Nano 2GB** | ✅ 보유 완료 | ROS2 기초 학습 |
| **Jetson TX2** | ✅ 보유 완료 | 중급 SW 포팅 경험 |
| **Jetson Orin Nano Super** | 🛒 구매 필요 | 최종 교육용 제품 타겟 |

### 핵심 One-Liner

> **RTX 5090 노트북에서 Isaac Sim으로 시뮬레이션하고, Jetson Orin Nano Super는 실제 로봇개 SW를 실행하며, 둘은 ROS2로 연결된다.**
>
> **Isaac Sim 구동을 위한 추가 GPU 구매는 전혀 필요 없습니다.**
