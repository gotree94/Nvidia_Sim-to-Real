# Jetson Nano 부팅 방식 비교: SD 카드 vs eMMC

## Jetson Nano 보드별 스토리지 구성

| 제품 | eMMC 존재? | 설계 방식 | 비고 |
|---|---|---|---|
| **Jetson Nano Module (Production)** — 단품 SOM | **✅ 16GB eMMC 있음** | 260-pin SO-DIMM SOM | NVIDIA 공식 데이터시트 기준 |
| **Jetson Nano Dev Kit (B01)** — 정품 | **✅ 모듈에 eMMC 있음** (단, **기본 부트 미디어는 SD 카드**) | 분리형 SOM + Carrier 보드 | NVIDIA가 공식 OS 이미지를 SD 카드용으로 제공. eMMC를 사용하려면 별도 flash 과정 필요 |
| **Jetson Nano Dev Kit (B01)** — SUB variant | **✅ eMMC로 부팅** | 분리형 SOM + Carrier 보드 | 써드파티(ThinkRobotics, Yahboom 등)가 생산 모듈의 eMMC에 OS를 미리 flash 해서 제공 |
| **Jetson Nano 2GB Dev Kit** | **❌ eMMC 없음** | 일체형 보드 (SoC 직납) | SD 카드가 유일한 저장소. $59 보급형 |
| **Jetson Nano Production Module** (단독 판매) | **✅ 16GB eMMC 있음** | 260-pin SO-DIMM SOM | OEM / 커스텀 Carrier 보드용 |

> ⚠️ **중요:** B01 Dev Kit에 포함된 **Jetson Nano 모듈(SOM) 자체에는 eMMC가 탑재**되어 있습니다.  
> 하지만 NVIDIA가 Dev Kit의 **공식 부트 미디어를 SD 카드로 지정**했고, 공식 OS 이미지도 SD 카드용으로만 제공합니다.  
> eMMC를 사용하려면 **SDK Manager / Force Recovery Mode를 통해 별도 flash 과정**이 필요합니다.  
> 이 때문에 실제로 eMMC를 사용하는 경우가 드물어, "eMMC가 없다"고 오해하는 경우가 많습니다.  
>
> **2GB Dev Kit은 eMMC가 정말 없습니다** — 이 모델은 SoC가 기판에 직접 납땜되고 eMMC가 아예 빠진 보급형 모델입니다.

---

## 1. SD 카드 전용 부팅

### 부팅 플로우

```
전원 ON → BootROM → SD 카드 (MBR/GPT) → TegraBoot (부트로더) → U-Boot → kernel → rootfs
```

- BootROM이 SD 카드의 **섹터 0 (MBR)**부터 부트로더를 순차적으로 읽음
- 부트로더, 커널, rootfs까지 **모든 구성 요소가 SD 카드에 위치**

### 성능

| 항목 | 속도 |
|---|---|
| 순차 읽기 | ~20-40 MB/s |
| 순차 쓰기 | ~10-30 MB/s |
| 4KB 랜덤 읽기 | ~2-5 MB/s |
| 4KB 랜덤 쓰기 | ~1-3 MB/s |

- SD 카드 속도는 **UHS-I (최대 104MB/s)** 인터페이스로 제한
- 실제 체감 성능은 사용하는 SD 카드 등급(Class 10, UHS-I U3 등)에 따라 달라짐

### 장점

- ✅ **OS 교체가 간편함** — SD 카드만 물리적으로 교체하면 끝
- ✅ 개발/테스트 환경을 여러 개 준비해서 스왑 가능
- ✅ 초기 설정이 쉬움 (이미지 굽기 → 삽입 → 부팅)

### 단점

- ❌ **SD 카드 I/O가 전체 시스템 병목**
- ❌ **전원 차단 시 파일시스템 손상(커럽션) 위험** 높음
- ❌ SD 카드 쓰기 수명이 상대적으로 짧음 (특히 로그/캐시 많을 때)
- ❌ 진동/온도 변화에 물리적으로 취약

---

## 2. eMMC 플래싱 후 SD 카드 보조 사용

### 부팅 플로우

```
전원 ON → BootROM → eMMC boot partition (boot1/boot2) → TegraBoot → U-Boot → kernel → rootfs (eMMC user area or SD)
```

- BootROM이 **eMMC의 하드웨어 부트 파티션(boot1/boot2)**에서 부트로더를 **RAW 섹터 접근**으로 로드
- 커널과 rootfs는 **eMMC user 파티션** 또는 **SD 카드** 중 선택 가능
- 일반적인 구성: 부트로더 + 커널 + rootfs는 eMMC, 추가 데이터/모델은 SD 카드

### 성능

| 항목 | eMMC 5.1 속도 |
|---|---|
| 순차 읽기 | ~150-200 MB/s |
| 순차 쓰기 | ~80-120 MB/s |
| 4KB 랜덤 읽기 | ~20-40 MB/s |
| 4KB 랜덤 쓰기 | ~10-20 MB/s |

> SD 카드 대비 **순차 3~5배, 랜덤 10배 이상** 빠름

### 장점

- ✅ **훨씬 빠른 부팅 및 앱 로딩 속도** (부트 시간 30-50% 단축)
- ✅ **솔더링된 패키지**로 물리적으로 안정적 (진동, 접촉 불량 없음)
- ✅ **eMMC 자체 웨어 레벨링, 배드 블록 관리, ECC** 내장
- ✅ OS(eMMC)와 데이터(SD)를 분리하여 **내구성과 관리 효율 향상**
- ✅ 전원 차단에 SD 카드보다 **훨씬 강건**

### 단점

- ❌ **초기 플래싱 과정이 복잡** (NVIDIA SDK Manager 또는 `jetson-disk-image-creator` 필요)
- ❌ OS 이미지 교체하려면 **eMMC를 다시 플래싱**해야 함 (시간 소요)
- ❌ eMMC 용량이 16GB로 제한되어 있어 큰 데이터는 SD 카드에 따로 관리 필요

---

## 3. 상세 비교표

| 항목 | SD 카드 전용 부팅 | eMMC 부팅 + SD 보조 |
|---|---|---|
| **부트 속도** | 느림 (~20-40 MB/s) | 빠름 (~150-200 MB/s) |
| **OS 로딩 속도** | 느림 | 빠름 |
| **앱/라이브러리 실행 속도** | 느림 (랜덤 I/O 병목) | 빠름 |
| **OS 스왑 편의성** | ★★★★★ (카드 교체) | ★★☆☆☆ (재플래싱 필요) |
| **내구성 / 신뢰성** | ★★☆☆☆ | ★★★★★ |
| **전원 차단 리스크** | 높음 | 낮음 |
| **스토리지 용량** | SD 카드 용량에 의존 (최대 128GB+) | eMMC 16GB + SD 확장 가능 |
| **OS / 데이터 분리** | 불가능 (단일 카드) | 가능 (eMMC=OS, SD=/data) |
| **초기 설정 난이도** | 쉬움 (balenaEtcher 등으로 이미지 굽기) | 복잡함 (SDKMgr 또는 CLI 플래싱) |
| **프로덕션 적합도** | 낮음 | 높음 |

---

## 4. 부트 플로우 상세 비교

### SD 카드 부팅

```
BootROM
  └─ SDMMC 컨트롤러 초기화
      └─ SD 카드 섹터 0 (MBR) 읽기
          └─ BPB (BIOS Parameter Block) 파싱
              └─ TegraBoot (bootloader) 로드
                  └─ U-Boot 로드
                      └─ kernel + device tree 로드
                          └─ rootfs 마운트 (SD 카드 파티션)
```

### eMMC 부팅

```
BootROM
  └─ 내장 eMMC 컨트롤러 초기화
      └─ eMMC boot partition (boot1) — RAW 섹터 접근
          └─ TegraBoot (bootloader) 로드
              └─ U-Boot 로드
                  └─ kernel + device tree 로드 (eMMC user area)
                      └─ rootfs 마운트 (eMMC user area 또는 SD 카드)
```

> **핵심 차이:** eMMC 부팅은 BootROM이 **FAT 파티션을 거치지 않고 RAW 섹터 직접 접근**하므로 초기 부트로딩이 더 빠르고 안정적입니다.

---

## 5. 사용 시나리오별 권장 구성

| 시나리오 | 권장 부팅 방식 | 이유 |
|---|---|---|
| **프로토타이핑 / 개발** | SD 카드 전용 | OS 이미지를 자주 갈아끼워야 함 |
| **임베디드 프로덕션 제품** | eMMC 전용 | 신뢰성과 성능이 중요 |
| **엣지 AI / 로봇** | eMMC 부팅 + SD는 데이터 저장 | OS는 안정적으로, 모델/데이터는 대용량 SD |
| **교육 / 워크샵** | SD 카드 전용 | 참가자별로 다른 환경을 카드로 분배 |
| **CI/CD 테스트 팜** | SD 카드 전용 | 자동 이미지 교체가 용이 |

---

## 6. 초기 설정 요약

### SD 카드 부팅 설정

```
1. SD 카드를 PC에 연결
2. Jetson Nano 공식 이미지 다운로드 (https://developer.nvidia.com/jetson-nano-sd-card-image)
3. balenaEtcher / Rufus로 SD 카드에 이미지 굽기
4. SD 카드를 Jetson Nano에 삽입
5. 전원 ON → 자동 부팅
```

### eMMC 플래싱 설정

```
1. NVIDIA SDK Manager 설치 (호스트 PC)
2. Jetson Nano를 **Force Recovery Mode (FMR)**로 진입:
   - Jumper 핀으로 FMR 설정 → 전원 → USB 연결
3. SDK Manager에서 대상 보드 선택 → "Jetson Nano"
4. JetPack SDK + rootfs 이미지 선택
5. 플래싱 실행 (약 20-40분 소요)
6. 완료 후 재부팅 → eMMC에서 부팅
```

---

## 참고 자료

- [NVIDIA Jetson Nano Developer Kit User Guide](https://developer.download.nvidia.com/assets/embedded/secure/jetson/Nano/docs/JetsonNano_DeveloperKit_UserGuide.pdf)
- [Jetson Nano SD Card Image](https://developer.nvidia.com/jetson-nano-sd-card-image)
- [NVIDIA SDK Manager](https://developer.nvidia.com/sdk-manager)
