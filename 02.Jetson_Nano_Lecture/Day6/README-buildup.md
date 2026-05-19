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
#usda 1.0
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

## Phase 1 — Module ② : Prims

**"씬을 구성하는 모든 것의 기본 단위"**

<img src="usd-buildup\USD-003.png">

**Prim이란 무엇인가**
   * Prim(Primitive)은 USD 씬 그래프를 구성하는 모든 노드입니다.
   * 3D 메시, 카메라, 조명, 머티리얼, 논리적 그룹 — 씬에 존재하는 모든 것이 Prim입니다.
   * 파일시스템으로 비유하면 Prim은 디렉터리 또는 파일에 해당합니다.
   * Prim들은 /Factory/Robots/Robot_01처럼 슬래시로 구분되는 경로(SdfPath)로 식별되며, 이 경로가 씬 그래프의 주소입니다.

**Prim의 세 가지 Specifier**
   * 모든 Prim은 선언될 때 반드시 하나의 Specifier를 가집니다. 이것이 Prim의 "존재 방식"을 결정합니다.

| Specifier | 키워드 | 의미 | 
|:-------:|:-------:|:-------:|
| Defined | def | 실제로 씬에 존재하는 Prim
| Abstract | class | 공유 데이터 정의용, 렌더링 안 됨 | 
| Override | over | 다른 레이어의 Prim을 수정 | 

* def는 가장 일반적인 선언, class는 Phase 5 Inherit에서, over는 컴포지션 오버라이드에서 핵심 역할을 합니다.

**Prim Type — Schema**
   * Prim에는 Type을 지정할 수 있습니다. Type은 USD Schema 시스템이 정의한 클래스이며, 어떤 Attribute와 동작을 기본으로 갖는지를 결정합니다.

```
def Xform   "Factory"   { }    ← 트랜스폼을 가질 수 있는 그룹
def Scope   "Robots"    { }    ← 트랜스폼 없는 논리 컨테이너
def Mesh    "Floor"     { }    ← 폴리곤 지오메트리
def Camera  "MainCam"   { }    ← 카메라
def SphereLight "Key"   { }    ← 조명
```

   * Type이 없는 Prim(def "MyPrim")도 유효합니다. 이를 typeless Prim이라 하며, 커스텀 데이터를 담는 용도로 사용합니다.

**SdfPath — Prim의 주소**
```
/                           ← PseudoRoot (Stage의 가상 루트)
/Factory                    ← 최상위 Prim
/Factory/Floor              ← 자식 Prim
/Factory/Robots/Robot_01    ← 손자 Prim
/Factory/Robots/Robot_01.visibility  ← Attribute 경로 (점 이후)
/Factory/Robots/Robot_01.rel:material ← Relationship 경로
```

   * SdfPath는 문자열처럼 보이지만 USD 내부에서는 인터닝된 토큰으로 관리되어 비교가 매우 빠릅니다.

**프로젝트 코드 — 첫 번째 Prim 추가**
   * .usda 텍스트 방식

```
#usda 1.0
(
    doc = "Robot Factory Scene — Phase 1"
    defaultPrim = "Factory"
    upAxis = "Y"
    metersPerUnit = 0.01
)

def Xform "Factory"
{
    def Scope "Robots"
    {
        def Xform "Robot_01"
        {
        }

        def Xform "Robot_02"
        {
        }
    }

    def Scope "Lights"
    {
    }

    def Mesh "Floor"
    {
    }
}
```

**Python API 방식**

```python
from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.Open("factory_base.usda")

# Prim 정의 — DefinePrim(path, typeName)
factory  = stage.DefinePrim("/Factory", "Xform")
robots   = stage.DefinePrim("/Factory/Robots", "Scope")
robot_01 = stage.DefinePrim("/Factory/Robots/Robot_01", "Xform")
robot_02 = stage.DefinePrim("/Factory/Robots/Robot_02", "Xform")
lights   = stage.DefinePrim("/Factory/Lights", "Scope")
floor    = stage.DefinePrim("/Factory/Floor", "Mesh")

# defaultPrim 설정 — Reference할 때 진입점이 됨
stage.SetDefaultPrim(factory)

stage.Save()
```

**Prim 순회 — 씬 그래프 탐색**

```python
# 1. 전체 트리 순회
for prim in stage.Traverse():
    indent = "  " * len(prim.GetPath().pathComponents)
    print(f"{indent}{prim.GetPath()}  [{prim.GetTypeName()}]")

# 출력 예시:
# /Factory  [Xform]
#   /Factory/Robots  [Scope]
#     /Factory/Robots/Robot_01  [Xform]
#     /Factory/Robots/Robot_02  [Xform]
#   /Factory/Lights  [Scope]
#   /Factory/Floor  [Mesh]

# 2. 특정 Prim 가져오기
prim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")
print(prim.IsValid())       # True
print(prim.GetTypeName())   # "Xform"
print(prim.GetParent().GetPath())  # /Factory/Robots

# 3. 자식 순회
robots = stage.GetPrimAtPath("/Factory/Robots")
for child in robots.GetChildren():
    print(child.GetName())  # Robot_01, Robot_02

# 4. 특정 타입만 필터링
for prim in stage.Traverse():
    if prim.IsA(UsdGeom.Xform):
        print(prim.GetPath())
```

**Prim의 활성 상태 — Active / Inactive**

   * Prim은 active 또는 inactive 상태를 가질 수 있습니다.
   * Inactive Prim은 합성에서 완전히 배제됩니다. 이는 씬에서 오브젝트를 완전히 제거하지 않고 숨기는 강력한 방법입니다.

```python
robot_02 = stage.GetPrimAtPath("/Factory/Robots/Robot_02")

# 비활성화 — 씬에서 사실상 제거
robot_02.SetActive(False)

# 다시 활성화
robot_02.SetActive(True)

# .usda에서는
# def Xform "Robot_02" (active = false) { }
```

* 지금까지 프로젝트 상태
```
factory_base.usda
└── /Factory                 (Xform, defaultPrim)
    ├── /Factory/Robots       (Scope)
    │   ├── /Factory/Robots/Robot_01  (Xform)
    │   └── /Factory/Robots/Robot_02  (Xform)
    ├── /Factory/Lights       (Scope)
    └── /Factory/Floor        (Mesh)
```

   * Prim 트리가 완성되었습니다.
   * 하지만 이 Prim들은 아직 아무런 데이터를 갖고 있지 않습니다.
   * 다음 모듈 ③ Attributes에서 각 Prim에 실제 데이터(위치, 크기, 색상 등)를 부여합니다.

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
