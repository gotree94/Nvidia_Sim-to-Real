# USD(Universal Scene Description)

> **USD(Universal Scene Description)의 핵심 개념들을 하나의 일관된 프로젝트로 엮어서 빌드업하는 방식은 매우 효과적인 교육 구조입니다.**

---

* 먼저 전체 커리큘럼 구조를 설계해 볼게요.USD 교육 커리큘럼의 전체 구조를 먼저 시각화하고, 
* 이후 각 모듈의 상세 내용을 단계적으로 빌드업하는 방식으로 설계하겠습니다

<img src="usd-buildup\USD-001.png">

전체 커리큘럼 구조입니다. 

**하나의 프로젝트 — 🏙️ Modular Robot Factory Scene**
을 5개 Phase에 걸쳐 점진적으로 완성해가는 구조입니다. 


**커리큘럼 설계 원칙**   
* 프로젝트 연속성: 매 모듈마다 같은 .usda 파일을 열어서 새로운 개념을 추가합니다. 앞 단계의 코드가 다음 단계의 기반이 됩니다.

* 빌드업 구조 요약:

| Phase | 추가되는 것 | 파일 | 
|:--------:|:--------:|:--------:|
| 1 | Stage 생성, Prim 정의, Attribute 설정 | factory_base.usda | 
| 2 | Scope/Xform 계층 구성, Primvar 적용 | factory_base.usda 확장 | 
| 3 | 로봇 팔 관절 애니메이션 (TimeSamples) | factory_anim.usda | 
| 4 | 조명 추가, 머티리얼 바인딩, 포맷 변환 | factory_lit.usda | 
| 5 | SubLayer / Reference / Payload / Inherit / Variant 조합 | factory_composed.usda | 

**교육 진행 방식 제안**

* 각 모듈은 다음 4단계로 진행합니다:
   * ① 개념 설명 — 왜 이 기능이 필요한가, 어떤 문제를 해결하는가
   * ② 코드 작성 — .usda 텍스트 포맷으로 직접 작성 (가장 학습 효과 높음)
   * ③ Python USD API — pxr.Usd 로 동일한 작업 반복
   * ④ 프로젝트 적용 — 로봇 공장 씬에 결과물 통합

---

## Phase 1 — Module ① : Stage
**"씬의 가장 바깥 그릇"**

   * Stage는 USD의 최상위 컨테이너입니다.
   * 파일을 열고 씬을 쓰고 읽는 모든 작업이 Stage를 통해서 이루어지며, Stage 없이는 USD에서 아무것도 할 수 없습니다.
   * Stage가 어떤 구조인지 먼저 그림으로 파악하겠습니다.

<img src="usd-buildup\USD-002.png">

### Stage란 무엇인가
   * Stage는 USD에서 "씬 전체를 담는 그릇"입니다.
   * 영화로 비유하면 편집실 전체에 해당합니다.
   * 여러 장의 필름(Layer)을 쌓아놓고, 그것들을 합성(Compose)한 최종 결과물을 바라보는 창구가 Stage입니다.

   * Stage가 하는 일을 세 가지로 정리하면:
      * 열기 — 디스크의 .usda / .usdc 파일(Root Layer)을 로드한다
      * 합성 — SubLayer, Reference, Inherit 등으로 연결된 모든 레이어를 LIVRPS 규칙에 따라 합성한다
      * 제공 — 합성된 결과 Prim Tree를 애플리케이션(Omniverse, Houdini, USD Hydra 등)에 노출한다


### 핵심 개념 — Layer Stack
   * Stage 안에는 Layer Stack이 있습니다. Layer Stack은 여러 .usda 파일이 쌓인 순서이며,
   * 위에 있을수록 아래를 Override합니다. 맨 위에는 런타임 전용인 Session Layer가 항상 존재합니다.

```
Layer Stack (강한 → 약한 순서)
┌─────────────────────────────┐
│  Session Layer  (메모리 전용) │  ← 가장 강함
│  Root Layer     (factory.usda)│
│  SubLayer A     (anim.usda)   │
│  SubLayer B     (lighting.usda)│  ← 가장 약함
└─────────────────────────────┘
```

### 프로젝트 코드 — factory_base.usda 생성
   * 이제 우리 프로젝트의 첫 번째 파일을 만듭니다. USD 텍스트 포맷(.usda)으로 직접 작성합니다.

**방법 1 — .usda 텍스트 직접 작성**
```usda
usda#usda 1.0
(
    doc = "Robot Factory Scene — Phase 1"
    defaultPrim = "Factory"
    upAxis = "Y"
    metersPerUnit = 0.01
)
```

   * 맨 첫 줄 #usda 1.0은 파서가 이 파일을 텍스트 USD로 인식하게 하는 매직 헤더입니다.
   * 괄호 ( ) 블록은 Stage 레벨 메타데이터로, 나중에 Metadata 모듈에서 자세히 다룹니다.

**방법 2 — Python USD API**
```python
from pxr import Usd, UsdGeom

# 새 Stage를 디스크에 생성
stage = Usd.Stage.CreateNew("factory_base.usda")

# Stage 레벨 메타데이터 설정
stage.SetMetadata("doc", "Robot Factory Scene — Phase 1")
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)

# 저장
stage.Save()
print(stage.GetRootLayer().ExportToString())
```

**방법 3 — 기존 파일 열기**

```python
# 이미 있는 파일을 Stage로 열기
stage = Usd.Stage.Open("factory_base.usda")

# Root Layer 경로 확인
root = stage.GetRootLayer()
print(root.realPath)          # 디스크 경로
print(root.ExportToString())  # 텍스트로 출력

# 현재 Stage의 모든 레이어 확인
for layer in stage.GetLayerStack():
    print(layer.identifier)
```

**Stage의 주요 API 요약**

| 메서드 | 설명 | 
|:-------:|:-------:|
| Usd.Stage.CreateNew(path) | 새 Stage + Root Layer 생성 | 
| Usd.Stage.Open(path) | 기존 파일로 Stage 열기 | 
| Usd.Stage.CreateInMemory() | 디스크 없이 메모리 Stage 생성 | 
| stage.GetRootLayer() | Root Layer 객체 반환 | 
| stage.GetLayerStack() | 현재 Layer Stack 전체 반환 | 
| stage.Save() | Root Layer 저장 | 
| stage.Export(path) | 합성 결과를 단일 파일로 flatten 저장 | 
| stage.Reload() | 디스크 변경 사항을 다시 로드 | 

## 지금까지 프로젝트 상태
```
factory_base.usda   ← Stage의 Root Layer
                       메타데이터만 있음 (Prim은 아직 없음)
```

* 다음 모듈 ② Prims에서 이 Stage 위에 첫 번째 Factory Prim을 올립니다.
* Stage가 "빈 편집실"이라면, Prim은 그 편집실에 들어오는 첫 번째 오브젝트입니다.

---

<img src="usd-buildup\USD-003.png">

---

<img src="usd-buildup\USD-004.png">

---

<img src="usd-buildup\USD-005.png">

---

<img src="usd-buildup\USD-006.png">

---

<img src="usd-buildup\USD-007.png">

---

<img src="usd-buildup\USD-008.png">

---

<img src="usd-buildup\USD-009.png">

---
