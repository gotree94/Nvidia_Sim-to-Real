# 4장 NVIDIA Jetson

## NVIDIA Jetson

- CPU(Cortex-A: Tegra)와 NVIDIA GPU 그리고 NPU등을 하나의 SOC(System On Chip)에 탑재한 임베디드 플랫폼
- Embedded Edge Device에서 NVIDIA의 고성능 병렬처리 연산 GPU를 일반 SW에서도 활용하도록 하는 'CUDA' 와 'CUDA'를 기반으로 하는 Deep-Learning (cu-DNN) 환경 및 주요 Deep-Learning 프레임워크 (예: tensorflow, PyTorch)에 대한 다양한 SW 라이브러리와 예제코드 제공
- SOM(System-On-Module) 형태로 Hardware를 설계하며, 개발 시간과 비용 절감 가능
- Jetson Nano, TX2 NX, Xavier NX, AGX Xavier, Orin-Nano, Orin NX, AGX Orin, Thor등이 있음

## NVIDIA Jetson Module(SOM)

- AI 작업 부하를 처리하도록 특별히 설계되어 복잡한 데이터를 처리하고 edge 디바이스에서 AI 알고리즘을 실행하는데 필요한 컴퓨팅 성능을 제공
- CPU, GPU, 메모리 및 다양한 인터페이스를 단일 소형 모듈에 통합

### NVIDIA Jetson Nano

- 128개의 NVIDIA의 CUDA 코어를 장착한 Maxwell 아키텍쳐
- AI Performance : 472 GFLOPs
- GPU : 128-core NVIDIA Maxwell™ GPU
- CPU : Quad-Core Arm® Cortex®-A57 MPCore processor

Jetson Nano SOM

## NVIDIA Jetson Series Specification #1

| Feature | Jetson NANO | Jetson TX2 NX | Jetson Xavier NX | Jetson Orin Nano 4GB | Jetson Orin Nano 8GB | Jetson Orin NX 8GB | Jetson Orin NX 16GB |
|---|---|---|---|---|---|---|---|
| AI Performance | 472 GFLOPs | 1.33 TFLOPs | 40 TOPS | 21 TOPs | 20 TOPS | 70 TOPS | 100 TOPS |
| GPU | 128-core NVIDIA Maxwell™ GPU | 256-core NVIDIA Pascal™ GPU | 384-core NVIDIA Volta™ GPU with 48 Tensor Cores | 512-core Ampere, with 16 Tensor Cores | 1024-core Ampere, with 32 Tensor Cores | 1024 Core Ampere, with 32 Tensor Cores | 1024 Core Ampere, with 32 Tensor Cores |
| CPU | Quad-Core ARM® Cortex®-A57 MPCore | Dual-Core NVIDIA Denver 2 64-Bit CPU and Quad-Core ARM® Cortex®-A57 MPCore processor | 6-core NVIDIA Carmel ARM®v8.2 64-bit CPU 6MB L2 + 4MB L3 | 6-core Arm® Cortex®-A78AE | 6-core Arm® Cortex®-A78AE | 6-core Arm® Cortex®-A78AE | 8-core Arm® Cortex®-A78AE |
| Memory | 4 GB 64-bit LPDDR4 25.6 GB/s | 4 GB 128-bit LPDDR4 51.2 GB/s | 8 GB/16GB 128-bit LPDDR4x 59.7 GB/s | 4GB 64-bit LPDDR5 34 GB/s | 8GB 128-bit LPDDR5 68 GB/s | 8GB 128-bit LPDDR5 102.4 GB/s | 16GB 128-bit LPDDR5 102.4 GB/s |
| DL Accelerator | - | - | 2x NVDLA Engines | - | - | (1x) NVDLA V2.0 PVA v2.0 | (2x) NVDLA V2.0 PVA v2.0 |
| Vision Accelerator | - | - | - | - | - | - | - |
| Storage | 16 GB eMMC 5.1 | 16 GB eMMC 5.1 | 16 GB eMMC 5.1 | Supports External NVMe | Supports External NVMe | Supports external NVMe | Supports external NVMe |
| Video Encode | 250MP/sec 1x 4K @ 30 (HEVC) 2x 1080p @ 60 (HEVC) | 2x 4K @ 60 \| 4x 4K @ 30 \| 10x 1080p @ 60 \| 22x 1080p @ 30 (H.265) | 1080p30 supported by 1-2 CPU cores | 1080p30 supported by 1-2 CPU cores | 1x 4K60 \| 3x 4K30 \| 6x 1080p60 \| 12x 1080p30 (H.265), H.264, H.265, AV1 | 1x 4K60 \| 3x 4K30 \| 6x 1080p60 \| 12x 1080p30 (H.265), H.264, H.265, AV1 |
| Video Decode | 500 MP/sec 1x 4K @ 60 (HEVC) 4x 1080p @ 60 (HEVC) | 2x 4K @ 60 \| 4x 4Kp @ 30 \| 7x 1080p @ 60 \| 14x 1080p @ 30 (H.265 & H.264) | 2x 8K @ 30 \| 6x 4K @ 60 \| 12x 4K @ 30 \| 22x 1080p @ 60 \| 44x 1080p @ 30 (H.265) | 1x 4K60 (H.265) \| 2x 4K30 (H.265) \| 5x 1080p60 (H.265) 11x 1080p30 (H.265) | 1x 4K60 (H.265) 5x 1080p60 (H.265) | 1x 4K60 (H.265) 3x 4K30 (H.265) 6x 1080p60 (H.265) | 1x 8K30 (H.265) 2x 4K60 (H.265) 9x 1080p60 (H.265) |
| Camera | Up to 4 cameras 12 lanes MIPI CSI-2 D-PHY 1.1 (up to 18 Gbps) | Up to 5 cameras (12 via virtual channels) 12 lanes MIPI CSI-2 (3x4 or 5x2) D-PHY 1.2 (up to 30 Gbps) | Up to 6 cameras (24 via virtual channels) 12 lanes MIPI CSI-2 D-PHY 1.2 (up to 30 Gbps) | Up to 4 cameras (8 via virtual channels) 8 lanes MIPI CSI-2 D-PHY 2.1 (up to 20Gbps) | Up to 4 cameras (8 via virtual channels) 8 lanes MIPI CSI-2 D-PHY 2.1 (up to 20Gbps) | Up to 4 cameras (8 via virtual channels) 8 lanes MIPI CSI-2 D-PHY 2.1 (up to 20Gbps) | Up to 4 cameras (8 via virtual channels) 8 lanes MIPI CSI-2 D-PHY 2.1 (up to 20Gbps) |
| PCI Express | 1 x4 (PCIe Gen2) | 1 x1 + 1 x2, total 30GT/s (PCIe Gen2) | 1 x1 + 1 x4 (PCIe Gen3, Root Port & Endpoint) | 1 x4 + 3 x1 (PCIe Gen3, Root Port, & Endpoint) | 1 x4 + 3 x1 (PCIe Gen3, Root Port, & Endpoint) | 1 x4 + 3 x1 (PCIe Gen4, Root Port, & Endpoint) | 1 x4 + 3 x1 (PCIe Gen4, Root Port, & Endpoint) |
| Mechanical | 69.6mm x 45mm 260-pin SO-DIMM connector | 69.6mm x 45mm 260-pin SO-DIMM connector | 69.6mm x 45mm 260-pin SO-DIMM connector | 69.6mm x 45mm 260-pin SO-DIMM connector | 69.6mm x 45mm 260-pin SO-DIMM connector | 69.6mm x 45mm 260-pin SO-DIMM connector | 69.6mm x 45mm 260-pin SO-DIMM connector |
| Power | 5W - 10W | 7.5W - 15W | 10W - 20W | 5W - 10W | 7W - 15W | 10W - 20W | 10W - 25W |

## NVIDIA Jetson Series Specification #2

| Feature | Jetson AGX Xavier 32GB | Jetson AGX Xavier 64GB | Jetson AGX Orin 32GB | Jetson AGX Orin 64GB | Jetson AGX Orin industrial |
|---|---|---|---|---|---|
| AI Performance | 32 TOPS | 32 TOPS | 200 TOPS | 275 TOPS | 248 TOPS |
| GPU | 512-core NVIDIA Volta™ GPU (with 64 Tensor cores) | 512-core NVIDIA Volta™ GPU (with 64 Tensor cores) | 1792 Core Ampere, with 56 Tensor Cores | 2048 Core Ampere, with 64 Tensor Cores | 2048 Core Ampere, with 64 Tensor Cores |
| CPU | 8-core NVIDIA Carmel ARM® v8.2 64-bit CPU 8 MB L2 + 4 MB L3 | 8-core NVIDIA Carmel ARM® v8.2 64-bit CPU 8 MB L2 + 4 MB L3 | 8-core Arm® Cortex®-A78AE v8.2 64-bit CPU 2MB L2 + 4MB L3 | 8-core Arm® Cortex®-A78AE v8.2 64-bit CPU 2MB L2 + 4MB L3 | 2-core Arm® Cortex®-A78AE v8.2 64-bit CPU 3MB L2 + 6MB L3 |
| Memory | 64 GB 256-bit LPDDR4x 136.5 GB/s | 64 GB 256-bit LPDDR4x 136.5 GB/s | 32GB 256-bit LPDDR5 205 GB/s | 64GB 256-bit LPDDR5 205 GB/s | 64GB 256-bit LPDDR5 (+ ECC) 204.8GB/s |
| DL Accelerator | (2x) NVDLA V1.0 | (2x) NVDLA V1.0 | (2x) NVDLA V2.0 | (2x) NVDLA V2.0 | (2x) NVDLA V2.0 |
| Vision Accelerator | (2x) 7-way VLIW Processor | (2x) 7-way VLIW Processor | (2x) 7-way VLIW Processor | (2x) 7-way VLIW Processor | (2x) 7-way VLIW Processor |
| Storage | 32 GB eMMC 5.1 | 32 GB eMMC 5.1 | 64 GB eMMC 5.1 | 64 GB eMMC 5.1 | 64 GB eMMC 5.1 |
| Video Encode | 4x 4K @ 60 (H.265) 16x 1080p @ 60 (H.265) 32x 1080p @ 30 (H.265) | 4x 4K @ 60 (H.265) 16x 1080p @ 60 (H.265) 32x 1080p @ 30 (H.265) | 1x 4K60 (H.265) 3x 4K30 (H.265) 6x 1080p60 (H.265) 12x 1080p30 (H.265) | 1x 8K30 (H.265) 2x 4K60 (H.265) 4x 4K30 (H.265) 9x 1080p60 (H.265) 18x 1080p30 (H.265) | 2x 4K60 (H.265) 4x 4K30 (H.265) 8x 1080p60 (H.265) 16x 1080p30 (H.265) |
| Video Decode | 2x 8K @ 30 (H.265) 6x 4K @ 60 (H.265) 26x 1080p @ 60 (H.265) 52x 1080p @ 30 (H.265) | 2x 8K @ 30 (H.265) 6x 4K @ 60 (H.265) 26x 1080p @ 60 (H.265) 52x 1080p @ 30 (H.265) | 1x 4K60 (H.265) 3x 4K30 (H.265) 6x 1080p60 (H.265) 12x 1080p30 (H.265) 1x 8K30 (H.265) 2x 4K60 (H.265) 4x 4K30 (H.265) 9x 1080p60 (H.265) 18x 1080p30 (H.265) | 1x 8K30 (H.265) 3x 4K60 (H.265) 7x 4K30 (H.265) 11x 1080p60 (H.265) 22x 1080p30 (H.265) | 1x 8K30 (H.265) 3x 4K60 (H.265) 7x 4K30 (H.265) 11x 1080p60 (H.265) 22x 1080p30 (H.265) |
| Camera | Up to 6 cameras (36 via virtual channels) 16 lanes MIPI CSI-2 \| 8 lanes SLVS-EC D-PHY 1.2 (up to 40 Gbps) | Up to 6 cameras (36 via virtual channels) 16 lanes MIPI CSI-2 \| 8 lanes SLVS-EC D-PHY 1.2 (up to 40 Gbps) | Up to 6 cameras (16 via virtual channels) 16 lanes MIPI CSI-2 D-PHY 2.1 (up to 40Gbps) \| C-PHY 2.0 (up to 164Gbps) | Up to 6 cameras (16 via virtual channels) 16 lanes MIPI CSI-2 D-PHY 2.1 (up to 40Gbps) \| C-PHY 2.0 (up to 164Gbps) | Up to 6 cameras (16 via virtual channels) 16 lanes MIPI CSI-2 D-PHY 2.1 (up to 40Gbps) \| C-PHY 2.0 (up to 164Gbps) |
| PCI Express | 1 x8 + 1 x4 + 1 x2 + 2 x1 (PCIe Gen4, Root Port and Endpoint) | 1 x8 + 1 x4 + 1 x2 + 2 x1 (PCIe Gen4, Root Port and Endpoint) | Up to 2 x8 + 1 x4 + 2 x1 (PCIe Gen4, Root Port, & Endpoint) | Up to 2 x8 + 1 x4 + 2 x1 (PCIe Gen4, Root Port, & Endpoint) | Up to 2 x8 + 1 x4 + 2 x1 (PCIe Gen4, Root Port, & Endpoint) |
| Mechanical | 100 mm x 87 mm 699-pin connector Integrated thermal transfer plate | 100mm x 87mm 699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate | 100mm x 87mm 699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate | 100mm x 87mm 699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate | 100mm x 87mm 699-pin Molex Mirror Mezz Connector Integrated Thermal Transfer Plate |
| Power | 10W - 30W | 10W - 30W | 15W - 40W | 15W - 60W | 15W - 75W |
| Temperature | -25°C to 80°C at TTP | -25°C to 80°C at TTP | -25°C to 80°C at TTP | -25°C to 80°C at TTP | -25°C to 85°C at TTP |

## NVIDIA Jetson Developer Kit

- NVIDIA Jetson Developer Kit은 Jetson SOM을 기반으로 한 개발 보드로, AI 및 엣지 컴퓨팅 애플리케이션을 개발하고 테스트하는데 사용
- Jetson 사용자들이 좀 더 쉽게 소프트웨어 개발 하기 위한 표준 하드웨어 플랫폼으로 하드웨어 제작 이전에 소프트웨어 구현 및 시험을 가능하게 해줌

Jetson Nano Developer Kit

## Jetson Module(SOM) vs Jetson Developer Kit

### NVIDIA Jetson Module(SOM)

- Jetson 모듈은 양산 및 운영 환경에 적합하며, 각 모듈은 사전 설치된 소프트웨어 없이 판매됨
- 최종 양산용으로 설계되거나 판매되는 캐리어(I/O interface) 보드에 Jetson 모듈을 부착하고, 개발한 소프트웨어를 탑재 (Image Flash)하여 배포해야 함

### NVIDIA Jetson Developer Kit

- 각 Jetson Developer Kit에는 참조용 캐리어 보드와 비양산 용도의 Jetson 모듈이 포함
- Jetpack SDK를 통해서 소프트웨어를 개발하고 테스트하는데 사용되며, 양산 용도로 사용되지 않음

Jetson Developer Kit은 양산 용도가 아니며, Jetson 모듈은 Operating-Life time내 양산 환경에 맞춰 설계 됨

## NVIDIA Jetson Platform 하드웨어 구성

### NVIDIA Jetson SOM 구성

- CPU/GPU
- RAM
- NVDLA
- NV Encoder/NV Decoder, NV JPEG
- ISP/VIC
- eMMC(Storage)
- 그리고 외부 인터페이스

Jetson Xavier NX

- 개발자는 Jetson SOM과 연결할 커넥터와 사용할 외부 인터페이스를 구현한 Carrier Board를 제작 생산하면, Jetson에서 개발한 소프트웨어 이식 가능

## NVIDIA Jetson Platform 소프트웨어 구성

NVIDIA는 Jetson Platform 개발자를 위해 커널과 Bootloader, 소스코드, 툴 그리고 AI 소프트웨어 패키지를 모아 Jetpack이라는 소프트웨어 패키지 제공

- Jetpack: https://docs.NVIDIA.com/jetson/archives/index.html
- Developer guide: https://docs.NVIDIA.com/jetson/archives/r34.1/DeveloperGuide/index.html
- Jetson Linux Archive: https://developer.NVIDIA.com/embedded/jetson-linux-archive

**Jetpack SDK 구성:**
- Linux Kernel
- Bootloader
- BSP, Drivers
- Flash Utilities
- Rootfs

## JCB100 (Jetson Carrier Board)

- JCB100
  - NVIDIA Jetson Module(SoM)을 운영하기 위한 시스템 보드
  - 다양한 외부 인터페이스와 NVIDIA의 Jetson Nano Developer Kit과 Jetson Xavier NX Developer kit에 호환되도록 설계 되어 있으며, 추가적인 외부 저장 장치 및 CAN 통신을(Jetson Nano제외) 지원할 수 있도록 설계 되어 있음.

Jetson Carrier Board (JCB100)

## JCB100

## JCB100 인터페이스

## Jetson 모듈별 인터페이스 지원 현황

## JCB100
