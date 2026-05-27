# NVIDIA Big-tech 교육과정 — 조 편성 및 조별 과제

> 교육과정명: **NVIDIA Big-tech 교육과정**
> 작성일: 2026-05-27

---

## 📋 조 편성 (총 6팀)

| 조 | 팀원 | 과제 | 상태 |
|:--:|------|------|:----:|
| **1** | 박찬수, 민호기 | — | 📝 주제 미정 |
| **2** | 전승현, 채민아, 임상혁 | — | 📝 주제 미정 |
| **3** | 조인행, 김남우 | NVIDIA TurtleBot3 Dual Autonomous Navigation | ✅ 진행 중 |
| **4** | 유용준, 서예진 | — | 📝 주제 미정 |
| **5** | 김지윤, 권오주 | — | 📝 주제 미정 |
| **6** | 강영빈, 권영진 | — | 📝 주제 미정 |

---

## 🔍 조별 상세

---

### 조 ① — 박찬수, 민호기

| 항목 | 내용 |
|------|------|
| **팀원** | 박찬수, 민호기 |
| **과제** | 🔲 미정 |

---

### 조 ② — 전승현, 채민아, 임상혁

| 항목 | 내용 |
|------|------|
| **팀원** | 전승현, 채민아, 임상혁 |
| **과제** | 🔲 미정 |

---

### 조 ③ — 조인행, 김남우 ✅

| 항목 | 내용 |
|------|------|
| **팀원** | 조인행, 김남우 |
| **과제** | **NVIDIA TurtleBot3 Dual Autonomous Navigation** |
| **설명** | NVIDIA Isaac Sim + Cosmos + Isaac Lab 기반 TurtleBot3 자율주행 풀스택 프로젝트 (End-to-End Autonomous Navigation + Digital Twin Closed-Loop) |
| **레포** | https://github.com/gotree94/nvidia-turtlebot3_double |
| **진행 상황** | PPT 정리 중 |

#### 기술 스택

| 기술 | 버전 | 역할 |
|------|------|------|
| NVIDIA Isaac Sim | 2025.2+ | 물리 기반 로봇 시뮬레이션 (Omniverse, PhysX 5) |
| NVIDIA Isaac Lab | 2.1+ | 강화학습 PPO 트레이닝 프레임워크 |
| NVIDIA Cosmos | 2.0 | World Foundation Model, 합성 데이터 생성, Transfer, Policy |
| NVIDIA Jetson Orin Nano | JetPack 6+ | 실시간 TensorRT 추론 및 엣지 AI 배포 |
| ROS2 | Humble / Jazzy | 로봇 미들웨어 및 분산 DDS 통신 |
| Navigation2 (Nav2) | 최신 | 경로 계획 및 제어 |
| Digital Twin | SQLite + Auto ML | 실시간 데이터 수집 → 갭 분석 → 자동 재학습 → Blue-Green 배포 |

#### 전체 파이프라인 (6단계)

```
① 환경 디지털화 (Cosmos WFM)
② 데이터 증강 (Isaac Sim + Cosmos Transfer)
③ 정책 학습 - PPO RL (Isaac Lab)
④ Sim-to-Real Zero-shot 전이 (TensorRT)
⑤ 이기종 협업 - Jetson Orin + RPi 5 (ROS2 + Nav2)
⑥ 디지털 트윈 Closed-Loop (SQLite + Auto ML)
```

---

### 조 ④ — 유용준, 서예진

| 항목 | 내용 |
|------|------|
| **팀원** | 유용준, 서예진 |
| **과제** | 🔲 미정 |

---

### 조 ⑤ — 김지윤, 권오주

| 항목 | 내용 |
|------|------|
| **팀원** | 김지윤, 권오주 |
| **과제** | 🔲 미정 |

---

### 조 ⑥ — 강영빈, 권영진

| 항목 | 내용 |
|------|------|
| **팀원** | 강영빈, 권영진 |
| **과제** | 🔲 미정 |

---

## 📌 참고 — 수업 중 논의되었던 과제 아이디어

> 아래는 조 편성 이전에 수업 채팅에서 논의되었던 과제 아이디어입니다.  
> 조 편성 이후 실제 과제와 매칭 여부는 미확인 상태이며, 참고용으로만 기재합니다.

### 💡 마을 (격자형 맵) 내비게이션 시뮬레이션
- **설명**: 격자형 마을 맵에서 출발지 → 목적지 이동, 동적 장애물 및 신호등 회피
- **기술**: ROS2, Isaac Sim, DWA Local Planner, Action Graph
- **관련 언급**: `05 allai` 님이 해당 주제로 진행 예정

### 💡 스마트 물류창고 시뮬레이션
- **설명**: 물류창고 내 Wheeled Robot 물품 운반, 목적지 이동, 충돌 회피 (멀티 로봇)
- **기술**: NVIDIA Isaac Sim, Warehouse Environment, USD Scene Templates
- **튜토리얼**: [Warehouse Creator](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/digital_twin/warehouse_logistics/ext_omni_warehouse_creator.html), [충돌 회피](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/digital_twin/warehouse_logistics/logistics_tutorial_cuopt.html)
- **관련 언급**: `01 allai` 님이 해당 주제로 진행 예정

---

## ⚠️ 공지사항 (김성인)

- 주제 미정인 조는 **오늘까지** 조별 주제를 정하여 전달 필요
- 추후 주제 변경 가능
- 프로젝트 기간이 짧으므로 **매일 진행사항 확인 예정**
- 궁금한 점은 스페이스 또는 채팅방을 통해 질문 가능
