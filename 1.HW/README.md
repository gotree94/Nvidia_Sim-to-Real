# NVIDIA Jetson Hardware — 보드별 상세 가이드

내가 보유한 Jetson 보드 3종(TX2, Nano 4GB SD, Orin Nano Super)의 하드웨어 스펙과 초기 설정 방법을 정리한 문서 모음.

## 목차

| # | 파일 | 대상 보드 | 핵심 내용 |
|---|------|----------|----------|
| 1 | [1-1_Jetson_TX2.md](./1-1_Jetson_TX2.md) | **Jetson TX2** | Pascal GPU 256코어, Denver2+A57 HMP 6코어 CPU<br>8GB LPDDR4, 32GB eMMC, SDK Manager 플래싱 |
| 2 | [1-2_Jetson_Nano_4GB_SD.md](./1-2_Jetson_Nano_4GB_SD.md) | **Jetson Nano 4GB (no eMMC)** | Maxwell GPU 128코어, 4GB LPDDR4, microSD 전용 부팅<br>A02/B01 리비전 차이, SD 카드 이미지 기록 |
| 3 | [1-3_Jetson_Orin_Nano_Super.md](./1-3_Jetson_Orin_Nano_Super.md) | **Jetson Orin Nano Super** | Ampere GPU 1024코어 + 32 Tensor 코어, 8GB LPDDR5, 67 TOPS<br>NVMe SSD, MAXN SUPER 모드 |

## 보드 비교 요약

| 항목 | TX2 | Nano 4GB (SD) | Orin Nano Super |
|------|-----|---------------|-----------------|
| **출시** | 2017 | 2019 | 2024 |
| **SoC** | Tegra "Parker" (16nm) | Tegra X1 (T210, 28nm) | Orin (8nm) |
| **GPU** | Pascal 256-core | Maxwell 128-core | Ampere 1024-core + 32 Tensor Cores |
| **GPU 클럭** | 1.30 GHz | 921 MHz | 625 MHz ~ 1,020 MHz (Super) |
| **CPU** | Denver2 2-core + A57 4-core | A57 4-core | A78AE 6-core |
| **CPU 클럭** | 2.0 GHz | 1.43 GHz | 1.7 GHz (Super) |
| **메모리** | 8GB LPDDR4 | 4GB LPDDR4 | 8GB LPDDR5 |
| **메모리 대역폭** | 59.7 GB/s | 25.6 GB/s | **102 GB/s** |
| **스토리지** | 32GB eMMC 5.1 | microSD (별도) | microSD / NVMe SSD |
| **AI 성능** | 1.33 TFLOPS (FP16) | 0.47 TFLOPS (FP16) | **67 TOPS (INT8)** |
| **전력** | 7.5W / 15W | 5W / 10W | 7W / 15W / 25W (Super) |
| **Tensor Core** | ❌ | ❌ | ✅ 32개 |
| **초기화 방식** | SDK Manager (Linux) | SD 카드 이미지 (가장 간편) | SDK Manager (권장) / SD 이미지 |
| **폼팩터** | 50×87mm (모듈), Mini-ITX (키트) | 69.6×45mm (모듈), 100×80mm (키트) | 69.6×45mm (모듈), 103×90.5mm (키트) |

## 초기화 방법 요약

| 보드 | 가장 간단한 방법 | 필요 장비 |
|------|----------------|----------|
| **TX2** | SDK Manager로 eMMC 플래싱 | Linux Host PC, USB Micro-B, 19V 어댑터 |
| **Nano 4GB SD** | SD 카드에 이미지 직접 기록 (Etcher) | Windows/Mac/Linux, microSD 카드, 5V/4A 어댑터 |
| **Orin Nano Super** | SDK Manager로 NVMe/SD 플래싱 | Linux Host PC, USB-C 케이블, NVMe SSD(권장) |

## 아키텍처 세대 비교

```
TX2 (2017)                  Nano 4GB (2019)            Orin Nano Super (2024)
┌─────────────────┐        ┌─────────────────┐        ┌──────────────────────┐
│ 16nm FinFET     │        │ 28nm            │        │ 8nm                  │
│                 │        │                 │        │                      │
│ Pascal GPU      │        │ Maxwell GPU     │        │ Ampere GPU           │
│ 256 CUDA cores  │        │ 128 CUDA cores  │        │ 1024 CUDA cores      │
│ No Tensor Core  │        │ No Tensor Core  │        │ 32 Tensor Cores ✅   │
│                 │        │                 │        │                      │
│ Denver2 + A57   │        │ A57 ×4          │        │ A78AE ×6             │
│ 6-core HMP      │        │                 │        │ 2-cluster HMP        │
│                 │        │                 │        │                      │
│ LPDDR4 128-bit  │        │ LPDDR4 64-bit   │        │ LPDDR5 128-bit       │
│ 59.7 GB/s       │        │ 25.6 GB/s       │        │ 102 GB/s             │
│                 │        │                 │        │                      │
│ 7.5W / 15W      │        │ 5W / 10W        │        │ 7W / 25W (Super)     │
└─────────────────┘        └─────────────────┘        └──────────────────────┘
```

> Orin Nano Super는 Tensor Core가 있어서 **Transformer 계열 최신 AI 모델(LLM, VLM, ViT)**을 엣지에서 실행할 수 있다는 점이 TX2/Nano와의 가장 큰 차이.
