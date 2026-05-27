# NVIDIA Big-tech 교육과정 — 조 편성 및 조별 과제

> 교육과정명: **NVIDIA Big-tech 교육과정**
> 작성일: 2026-05-27

---

## 📋 allai ID — 성명 매핑

| allai ID | 성명 | 이메일 |
|:--------:|:----:|:------:|
| allai01 | **김지윤** | allai01@allai.co.kr |
| allai02 | **강영빈** | allai02@allai.co.kr |
| allai03 | **유용준** | allai03@allai.co.kr |
| allai04 | **서예진** | allai04@allai.co.kr |
| allai05 | **전승현** | allai05@allai.co.kr |
| allai06 | **권영진** | allai06@allai.co.kr |
| allai07 | **원주성** | allai07@allai.co.kr |
| allai08 | **권오주** | allai08@allai.co.kr |
| allai09 | **박찬수** | allai09@allai.co.kr |
| allai10 | **임희수** | allai10@allai.co.kr |
| allai11 | **이호기** | allai11@allai.co.kr |
| allai12 | **김남우** | allai12@allai.co.kr |
| allai13 | **채민아** | allai13@allai.co.kr |
| allai14 | **조인행** | allai14@allai.co.kr |
| allai15 | **임상혁** | allai15@allai.co.kr |

> **전체 15명**, allai07(원주성), allai10(임희수), allai11(이호기)는 현재 편성된 조에 포함되지 않음

---

## 📋 조 편성 (총 6팀)

| 조 | 팀원 | 과제 | 상태 |
|:--:|------|------|:----:|
| **1** | 박찬수(allai09), 이호기(allai11) | — | 📝 주제 미정 |
| **2** | **전승현**(allai05), 채민아(allai13), 임상혁(allai15) | **마을(격자형 맵) 내비게이션 시뮬레이션** | ✅ 주제 확정 |
| **3** | 조인행(allai14), 김남우(allai12) | **NVIDIA TurtleBot3 Dual Autonomous Navigation** | ✅ 진행 중 (PPT 정리) |
| **4** | 유용준(allai03), 서예진(allai04) | — | 📝 주제 미정 |
| **5** | **김지윤**(allai01), 권오주(allai08) | **스마트 물류창고 시뮬레이션** | ✅ 주제 확정 |
| **6** | 강영빈(allai02), 권영진(allai06) | — | 📝 주제 미정 |

---

## 🔍 조별 상세

---

### 조 ① — 박찬수, 이호기

| 항목 | 내용 |
|------|------|
| **allai ID** | allai09(박찬수), allai11(이호기) |
| **과제** | 🔲 미정 |

---

### 조 ② — 전승현, 채민아, 임상혁 ✅

| 항목 | 내용 |
|------|------|
| **allai ID** | allai05(전승현), allai13(채민아), allai15(임상혁) |
| **과제** | **🏘️ 마을(격자형 맵) 내비게이션 시뮬레이션** |
| **제안자** | 전승현 (`05 allai`) |
| **설명** | 격자형 마을 맵에서 출발 지점부터 지정된 목적지들까지 이동하는 내비게이션 시뮬레이션. 이동 중 동적 장애물과 신호등을 두어 회피하는 것이 목표 |
| **기술 스택** | ROS2, Isaac Sim, DWA Local Planner, Action Graph |

#### 세부 계획 (김성인 교수님 제안)

| 단계 | 내용 |
|:----:|------|
| 1 | 격자형 마을 맵 구현 |
| 2 | 기존 강의 내 DWA 등 Local Planner 코드 활용 |
| 3 | Isaac Sim 맵 + Action Graph으로 가상 맵에서 ROS2 동작 |

---

### 조 ③ — 조인행, 김남우 ✅

| 항목 | 내용 |
|------|------|
| **allai ID** | allai14(조인행), allai12(김남우) |
| **과제** | **🤖 NVIDIA TurtleBot3 Dual Autonomous Navigation** |
| **설명** | NVIDIA Isaac Sim + Cosmos + Isaac Lab 기반 TurtleBot3 자율주행 풀스택 프로젝트 (End-to-End Autonomous Navigation + Digital Twin Closed-Loop) |
| **기반 자료** | 수업 DLI 과정 한글 정리 → turtlebot3_double 프로젝트로 확장 |
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

#### 전체 파이프라인

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
| **allai ID** | allai03(유용준), allai04(서예진) |
| **과제** | 🔲 미정 |

---

### 조 ⑤ — 김지윤, 권오주 ✅

| 항목 | 내용 |
|------|------|
| **allai ID** | allai01(김지윤), allai08(권오주) |
| **과제** | **🏭 스마트 물류창고 시뮬레이션** |
| **제안자** | 김지윤 (`01 allai`) |
| **설명** | 물류창고 내 Wheeled Robot을 가져와 변형하고, 물건 위치와 목적지를 주어 이동. 여유 시 로봇 여러 대 추가하여 충돌 회피까지 구현 |
| **기술 스택** | NVIDIA Isaac Sim, Warehouse Environment, USD Scene Templates |

#### 참고 자료 (김성인 교수님 제안)

| 자료 | 링크 |
|:----|:----:|
| USD Scene Templates Pack | https://docs.omniverse.nvidia.com/usd/latest/usd_content_samples/downloadable_packs.html |
| Warehouse Creator 튜토리얼 | https://docs.isaacsim.omniverse.nvidia.com/5.1.0/digital_twin/warehouse_logistics/ext_omni_warehouse_creator.html |
| 충돌 회피 튜토리얼 | https://docs.isaacsim.omniverse.nvidia.com/5.1.0/digital_twin/warehouse_logistics/logistics_tutorial_cuopt.html |

---

### 조 ⑥ — 강영빈, 권영진

| 항목 | 내용 |
|------|------|
| **allai ID** | allai02(강영빈), allai06(권영진) |
| **과제** | 🔲 미정 |

---

## 📌 편성되지 않은 인원

| allai ID | 성명 | 비고 |
|:--------:|:----:|:----:|
| allai07 | 원주성 | 조 편성에 포함되지 않음 |
| allai10 | 임희수 | 조 편성에 포함되지 않음 |

---

## ⚠️ 공지사항 (김성인)

- 주제 미정인 조 **(④ 유용준·서예진, ⑥ 강영빈·권영진)** 는 **오늘까지** 조별 주제를 정하여 전달 필요
- 추후 주제 변경 가능
- 프로젝트 기간이 짧으므로 **매일 진행사항 확인 예정**
- 궁금한 점은 스페이스 또는 채팅방을 통해 질문 가능

---

## 📋 Chat Log — 과제 논의 원문 (참고)

```
05 allai(전승현), 오후 1:10
→ 마을(격자형 맵) 내비게이션 제안

김성인, 오후 1:15
→ 격자형 맵 구현 → DWA 등 Local Planner 활용 → Isaac Sim + Action Graph 제안

01 allai(김지윤), 오후 1:24
→ 스마트 물류창고 시뮬레이션 제안

김성인, 오후 1:31
→ NVIDIA Warehouse Environment / USD Scene 템플릿 / 튜토리얼 링크 제공

김성인, (수정됨)
→ 유용준·서예진, 강영빈·권영진 — 주제 미제출 상태 공지
```
