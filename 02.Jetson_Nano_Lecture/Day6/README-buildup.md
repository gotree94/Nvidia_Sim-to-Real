# USD(Universal Scene Description)

> **USD(Universal Scene Description)의 핵심 개념들을 하나의 일관된 프로젝트로 엮어서 빌드업하는 방식은 매우 효과적인 교육 구조입니다.**
---

## 목차
   * Phase 1 — Module ① : Stage
   * Phase 1 — Module ② : Prims
   * Phase 1 — Module ③ : Attributes
   * Phase 1 — Module ④ : Relationships
   * Phase 1 — Module ⑤ : Metadata
   * Phase 2 — Module ⑦ : Xform
   * Phase 2 — Module ⑧ : Primvars
   * Phase 3 — Module ⑨ : TimeCodes & TimeSamples
   * Phase 4 — Module ⑩ : Lighting
   * Phase 4 — Module ⑪ : File Formats
   * Phase 4 — Module ⑫ : Modules (USD Schema Libraries)
   * Phase 5 — Module ⑬ : Composition

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

## Phase 1 — Module ③ : Attributes
**"Prim에 데이터를 부여하는 것"**

<img src="usd-buildup\USD-004.png">

**Attribute란 무엇인가**
   * Attribute는 Prim이 갖는 이름 붙은 데이터 값입니다.
   * 위치, 색상, 반지름, 가시성 등 Prim에 관한 모든 구체적인 수치나 상태가 Attribute로 표현됩니다.
   * Prim이 "Robot_01이라는 노드"라면, Attribute는 "그 로봇이 어디에 있고, 어떻게 생겼는지"를 담은 데이터입니다.

   * Attribute는 세 종류로 나뉩니다.
| 종류 | 예시 | 설명 |
|:-------:|:-------:|:-------:|
| Schema Attribute | xformOp:translate, visibility | 해당 Type의 Schema가 정의한 표준 속성 |
| API Attribute | primvars:displayColor | API Schema가 추가하는 속성 | 
| Custom Attribute | custom:serialNumber | 사용자가 직접 정의하는 속성 | 

**Value Type — USD의 타입 시스템**

   * USD는 강타입 시스템입니다. Attribute를 만들 때 반드시 타입을 지정해야 하며, 나중에 바꿀 수 없습니다.

```
# 스칼라 타입
bool    int     uint    int64
float   double  half
string  token   asset

# 벡터/행렬 타입
float2   float3   float4
double2  double3  double4
matrix4d  quatf   quatd

# 배열 타입 (뒤에 [] 붙임)
float[]   double3[]   int[]   string[]

# 특수 타입
asset    → 파일 경로 참조  @path/to/file.usda@
token    → 인터닝된 문자열, Enum 역할
```
   * token과 string의 차이: token은 USD 내부에서 인터닝(interning)되어 비교가 O(1)입니다. "inherited", "invisible", "Y" 같은 고정 열거값에 사용합니다.

**프로젝트 코드 — Robot_01에 Attribute 추가**
   * .usda 텍스트 방식

```usda
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
            # xformOp 네임스페이스: UsdGeom이 정의한 트랜스폼 Attribute
            double3 xformOp:translate = (100, 0, 200)
            double  xformOp:rotateY:pivot = 45.0
            uniform token[] xformOpOrder = ["xformOp:translate",
                                            "xformOp:rotateY:pivot"]

            # visibility: Schema가 정의한 표준 Attribute
            token visibility = "inherited"

            # custom Attribute: 네임스페이스 앞에 custom 키워드
            custom int custom:serialNumber = 1001
            custom string custom:model = "ARM-7X"
        }

        def Xform "Robot_02"
        {
            double3 xformOp:translate = (300, 0, 200)
            uniform token[] xformOpOrder = ["xformOp:translate"]
            custom int custom:serialNumber = 1002
            custom string custom:model = "ARM-7X"
        }
    }

    def Mesh "Floor"
    {
        # Mesh Schema의 표준 Attribute
        point3f[] points = [
            (-500, 0, -500), (500, 0, -500),
            (500, 0,  500), (-500, 0,  500)
        ]
        int[] faceVertexCounts  = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]

        # displayColor: UsdGeom Primvar (Module ⑧에서 자세히)
        color3f[] primvars:displayColor = [(0.3, 0.3, 0.3)]
    }
}
```

**Python API 방식**

```python
from pxr import Usd, UsdGeom, Sdf, Gf

stage = Usd.Stage.Open("factory_base.usda")

# ── Robot_01 Attribute 설정 ──────────────────────────────
robot_01 = UsdGeom.Xform(stage.GetPrimAtPath("/Factory/Robots/Robot_01"))

# UsdGeom.XformCommonAPI로 트랜스폼 간편 설정
xform_api = UsdGeom.XformCommonAPI(robot_01)
xform_api.SetTranslate(Gf.Vec3d(100, 0, 200))
xform_api.SetRotate(Gf.Vec3f(0, 45, 0))   # XYZ 오일러

# 직접 Attribute 생성 및 값 설정
prim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

# custom Attribute 생성: CreateAttribute(name, type, custom=True)
serial_attr = prim.CreateAttribute(
    "custom:serialNumber", Sdf.ValueTypeNames.Int, custom=True
)
serial_attr.Set(1001)

model_attr = prim.CreateAttribute(
    "custom:model", Sdf.ValueTypeNames.String, custom=True
)
model_attr.Set("ARM-7X")

# ── Floor Mesh Attribute 설정 ─────────────────────────────
floor_prim = UsdGeom.Mesh(stage.GetPrimAtPath("/Factory/Floor"))

floor_prim.GetPointsAttr().Set([
    Gf.Vec3f(-500, 0, -500), Gf.Vec3f( 500, 0, -500),
    Gf.Vec3f( 500, 0,  500), Gf.Vec3f(-500, 0,  500),
])
floor_prim.GetFaceVertexCountsAttr().Set([4])
floor_prim.GetFaceVertexIndicesAttr().Set([0, 1, 2, 3])

stage.Save()
```

**Attribute 읽기 · 검사**

```python
prim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

# 모든 Attribute 나열
for attr in prim.GetAttributes():
    print(f"{attr.GetName():40s} {attr.GetTypeName()}")

# 특정 Attribute 가져오기
serial = prim.GetAttribute("custom:serialNumber")

# 값 읽기 — 기본값 (TimeCode 없음)
print(serial.Get())                  # 1001

# 타임코드 지정 읽기 (Module ⑨에서 심화)
print(serial.Get(Usd.TimeCode(1)))   # 타임코드 1의 값

# Attribute 존재 여부
print(serial.IsValid())              # True
print(serial.HasValue())             # True
print(serial.GetTypeName())          # int

# 값이 없는 Attribute는 None 반환
attr = prim.GetAttribute("nonexistent")
print(attr.IsValid())                # False
```

**uniform vs varying — Attribute의 가변성**
   * Attribute 앞에 붙는 uniform 키워드는 시간에 따라 값이 바뀌지 않음을 선언합니다. xformOpOrder처럼 구조적으로 고정되어야 하는 Attribute에 씁니다.

```usda
# uniform: 애니메이션 불가, 모든 프레임에서 동일
uniform token[] xformOpOrder = ["xformOp:translate"]

# (기본) varying: 프레임마다 다른 값을 가질 수 있음
double3 xformOp:translate = (100, 0, 200)
```

* 지금까지 프로젝트 상태

```
factory_base.usda
└── /Factory
    ├── /Factory/Robots
    │   ├── /Factory/Robots/Robot_01
    │   │     xformOp:translate  = (100, 0, 200)   ← 추가됨
    │   │     xformOp:rotateY    = 45.0             ← 추가됨
    │   │     custom:serialNumber = 1001            ← 추가됨
    │   │     custom:model        = "ARM-7X"        ← 추가됨
    │   └── /Factory/Robots/Robot_02
    │         xformOp:translate  = (300, 0, 200)   ← 추가됨
    │         custom:serialNumber = 1002            ← 추가됨
    ├── /Factory/Lights
    └── /Factory/Floor
          points / faceVertexCounts / faceVertexIndices  ← 추가됨
          primvars:displayColor = [(0.3, 0.3, 0.3)]      ← 추가됨
```

   * Prim들이 실제 데이터를 갖게 되었습니다.
   * 다음 모듈 ④ Relationships에서는 Prim 간의 연결 — 머티리얼 바인딩, 조명 링크 등 — 을 다룹니다.
   * Attribute가 "값"을 담는다면, Relationship은 "다른 Prim을 가리키는 포인터"입니다.

---
## Phase 1 — Module ④ : Relationships
**"Prim과 Prim을 연결하는 포인터"**

<img src="usd-buildup\USD-005.png">

**Relationship란 무엇인가**
   * Relationship은 Prim이 다른 Prim(또는 Attribute)을 SdfPath로 가리키는 포인터입니다.
   * Attribute가 숫자나 문자열 같은 값을 담는다면, Relationship은 씬 그래프 안의 다른 노드를 참조합니다.

   * 핵심 차이를 한 줄로 정리하면:
```
Attribute   →  값(value)을 저장         ex) translate = (100, 0, 200)
Relationship → 경로(SdfPath)를 저장      ex) material:binding = </Factory/Materials/Metal>
```
   * Relationship은 타입이 없습니다. 가리키는 대상이 어떤 Prim인지는 Relationship을 사용하는 Schema가 의미를 부여합니다.

**가장 중요한 Relationship — material:binding**
   
   * USD에서 Relationship이 가장 많이 쓰이는 곳은 머티리얼 바인딩입니다. UsdShade의 material:binding은 Mesh나 Xform이 어떤 Material Prim을 사용할지 가리킵니다.

```usd
adef Mesh "Robot_01"
{
    # material:binding은 Relationship — 값이 아니라 경로를 저장
    rel material:binding = </Factory/Materials/MetalMaterial>
}
```

   * 꺾쇠괄호 < > 안의 경로가 Relationship 타겟입니다. Attribute의 값 ( )과 구별되는 .usda 문법입니다.

**Relationship의 특징 — 다중 타겟**

   * Relationship은 타겟을 여러 개 가질 수 있습니다. 조명의 light:targetPrim이 대표적인 예입니다.

```usda
def SphereLight "KeyLight"
{
    # 단일 타겟
    rel light:targetPrim = </Factory/Robots/Robot_01>

    # 다중 타겟 — 리스트 형태
    rel light:targetPrim = [
        </Factory/Robots/Robot_01>,
        </Factory/Robots/Robot_02>
    ]
}
```

**프로젝트 코드 — Material 바인딩 추가**
   * .usda 텍스트 방식

```usda
#usda 1.0
(
    defaultPrim = "Factory"
    upAxis = "Y"
    metersPerUnit = 0.01
)

def Xform "Factory"
{
    def Scope "Materials"
    {
        def Material "MetalMaterial"
        {
            # Shader 연결은 Module ⑫에서 심화
            token outputs:surface.connect =
                </Factory/Materials/MetalMaterial/PBRShader.outputs:surface>

            def Shader "PBRShader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor  = (0.2, 0.2, 0.25)
                float   inputs:metallic      = 0.9
                float   inputs:roughness     = 0.2
                token   outputs:surface
            }
        }

        def Material "FloorMaterial"
        {
            token outputs:surface.connect =
                </Factory/Materials/FloorMaterial/PBRShader.outputs:surface>

            def Shader "PBRShader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (0.3, 0.3, 0.3)
                float   inputs:metallic     = 0.0
                float   inputs:roughness    = 0.8
                token   outputs:surface
            }
        }
    }

    def Scope "Robots"
    {
        def Xform "Robot_01"
        {
            double3 xformOp:translate        = (100, 0, 200)
            uniform token[] xformOpOrder     = ["xformOp:translate"]
            custom int    custom:serialNumber = 1001

            # Relationship 선언 — rel 키워드
            rel material:binding = </Factory/Materials/MetalMaterial>
        }

        def Xform "Robot_02"
        {
            double3 xformOp:translate        = (300, 0, 200)
            uniform token[] xformOpOrder     = ["xformOp:translate"]
            custom int    custom:serialNumber = 1002

            rel material:binding = </Factory/Materials/MetalMaterial>
        }
    }

    def Scope "Lights"
    {
        def SphereLight "KeyLight"
        {
            float  inputs:intensity = 500.0
            float  inputs:radius    = 10.0
            color3f inputs:color    = (1.0, 0.95, 0.85)
            double3 xformOp:translate    = (0, 400, 0)
            uniform token[] xformOpOrder = ["xformOp:translate"]

            # 다중 타겟 Relationship
            rel light:targetPrim = [
                </Factory/Robots/Robot_01>,
                </Factory/Robots/Robot_02>
            ]
        }
    }

    def Mesh "Floor"
    {
        point3f[] points = [
            (-500,0,-500),(500,0,-500),(500,0,500),(-500,0,500)
        ]
        int[] faceVertexCounts  = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]

        rel material:binding = </Factory/Materials/FloorMaterial>
    }
}
```

**Python API 방식**

```python
from pxr import Usd, UsdGeom, UsdShade, UsdLux, Sdf, Gf

stage = Usd.Stage.Open("factory_base.usda")

# ── Material Prim 생성 ─────────────────────────────────────
materials_scope = stage.DefinePrim("/Factory/Materials", "Scope")

# MetalMaterial
metal_mat = UsdShade.Material.Define(stage, "/Factory/Materials/MetalMaterial")
metal_shader = UsdShade.Shader.Define(
    stage, "/Factory/Materials/MetalMaterial/PBRShader"
)
metal_shader.CreateIdAttr("UsdPreviewSurface")
metal_shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(
    Gf.Vec3f(0.2, 0.2, 0.25)
)
metal_shader.CreateInput("metallic",   Sdf.ValueTypeNames.Float).Set(0.9)
metal_shader.CreateInput("roughness",  Sdf.ValueTypeNames.Float).Set(0.2)
surface_output = metal_shader.CreateOutput(
    "surface", Sdf.ValueTypeNames.Token
)
metal_mat.CreateSurfaceOutput().ConnectToSource(surface_output)

# ── material:binding Relationship 설정 ─────────────────────
robot_01 = stage.GetPrimAtPath("/Factory/Robots/Robot_01")
robot_02 = stage.GetPrimAtPath("/Factory/Robots/Robot_02")

# UsdShade API로 바인딩 (내부적으로 rel material:binding을 씀)
UsdShade.MaterialBindingAPI(robot_01).Bind(metal_mat)
UsdShade.MaterialBindingAPI(robot_02).Bind(metal_mat)

# ── 직접 Relationship 생성·조작 ────────────────────────────
key_light_prim = stage.GetPrimAtPath("/Factory/Lights/KeyLight")

# Relationship 생성
target_rel = key_light_prim.CreateRelationship("light:targetPrim")

# 타겟 추가
target_rel.AddTarget(Sdf.Path("/Factory/Robots/Robot_01"))
target_rel.AddTarget(Sdf.Path("/Factory/Robots/Robot_02"))

# 타겟 조회
for target in target_rel.GetTargets():
    print(target)   # /Factory/Robots/Robot_01, /Factory/Robots/Robot_02

stage.Save()
```

**Relationship 읽기 · 탐색**

```python
prim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

# 모든 Relationship 나열
for rel in prim.GetRelationships():
    print(f"{rel.GetName():30s} → {rel.GetTargets()}")

# 특정 Relationship 가져오기
mat_binding = prim.GetRelationship("material:binding")

# 타겟 경로 조회
targets = mat_binding.GetTargets()
# [Sdf.Path('/Factory/Materials/MetalMaterial')]

# 타겟 Prim으로 직접 이동
for path in targets:
    target_prim = stage.GetPrimAtPath(path)
    print(target_prim.GetTypeName())   # Material

# UsdShade API로 바인딩된 Material 조회 (고수준)
bound = UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial()
print(bound[0].GetPath())   # /Factory/Materials/MetalMaterial
```

**Attribute vs Relationship 선택 기준**
```
언제 Attribute를 쓰나?
  → 값 자체를 저장할 때
     translate = (100, 0, 200)
     roughness = 0.2
     serialNumber = 1001

언제 Relationship을 쓰나?
  → 씬 안의 다른 Prim/Attribute를 가리킬 때
     material:binding  = </Factory/Materials/Metal>
     light:targetPrim  = </Factory/Robots/Robot_01>
     skel:skeleton     = </Factory/Robots/Robot_01/Skeleton>
     proxyPrim         = </Factory/Robots/Robot_01_Proxy>
```

**지금까지 프로젝트 상태**

```
factory_base.usda
└── /Factory
    ├── /Factory/Materials                         ← 추가됨
    │   ├── /Factory/Materials/MetalMaterial       ← 추가됨
    │   │     rel material:binding ←── Robot_01, Robot_02 가 참조
    │   └── /Factory/Materials/FloorMaterial       ← 추가됨
    ├── /Factory/Robots
    │   ├── /Factory/Robots/Robot_01
    │   │     rel material:binding → MetalMaterial ← 추가됨
    │   └── /Factory/Robots/Robot_02
    │         rel material:binding → MetalMaterial ← 추가됨
    ├── /Factory/Lights
    │   └── /Factory/Lights/KeyLight
    │         rel light:targetPrim → [Robot_01, Robot_02] ← 추가됨
    └── /Factory/Floor
          rel material:binding → FloorMaterial    ← 추가됨
```
   * 씬의 Prim들이 이제 서로 연결되었습니다.
   * 다음 모듈 ⑤ Metadata에서는 Prim과 Stage 자체에 붙는 "데이터에 대한 데이터" — 문서화, 렌더링 힌트, 에디터 정보 등을 다룹니다.
   * Attribute나 Relationship과 달리 Metadata는 합성(Composition)에 참여하지 않는 순수한 부가 정보입니다.

---

## Phase 1 — Module ⑤ : Metadata
**"데이터에 대한 데이터 — 씬의 맥락을 기록하다"**

<img src="usd-buildup\USD-006.png">

**Metadata란 무엇인가**
   * Metadata는 Prim·Attribute·Layer 자체에 붙는 부가 정보입니다. 씬의 콘텐츠(geometry, transform 등)가 아니라 씬을 설명하고 제어하는 데이터입니다.
   * Attribute와 Metadata의 핵심 차이는 딱 하나입니다.

```
Attribute  → 합성(Composition) 에 참여한다
             → 값이 레이어 간에 오버라이드·상속된다
Metadata   → 합성에 참여하지 않는다
             → 각 레이어에 독립적으로 기록된다
             → 단, doc / active / kind 등 일부는 합성 결과에 영향을 준다
```
   * Metadata가 붙을 수 있는 위치는 세 군데입니다. Stage/Layer 레벨, Prim 레벨, Attribute 레벨입니다.

**Stage / Layer 레벨 Metadata**
   * Stage를 열 때 가장 먼저 보게 되는 .usda 파일 상단의 ( ) 블록이 Layer 레벨 Metadata입니다.

```usda
#usda 1.0
(
    doc            = "Robot Factory Scene — Phase 1"
    defaultPrim    = "Factory"
    upAxis         = "Y"
    metersPerUnit  = 0.01
    startTimeCode  = 1.0
    endTimeCode    = 240.0
    timeCodesPerSecond = 24.0

    customLayerData = {
        string  author    = "나무"
        string  version   = "0.1.0"
        string  project   = "RobotFactory"
        bool    approved  = false
    }
)
```

   * defaultPrim은 이 Layer를 Reference할 때 어떤 Prim을 진입점으로 쓸지 알려줍니다. Phase 5 컴포지션에서 결정적인 역할을 합니다.
   * timeCodesPerSecond와 startTimeCode/endTimeCode는 Module ⑨ TimeSamples에서 다시 씁니다.

**Prim 레벨 Metadata**
   * Prim 선언 뒤 괄호 ( ) 블록에 씁니다.

```usda
def Xform "Robot_01"
(
    doc    = "조립 라인 1번 로봇 팔 — ARM-7X 모델"
    active = true
    kind   = "component"

    customData = {
        string  manufacturer = "FactoryBot Inc."
        int     revision     = 3
        string[]  tags       = ["robot", "arm", "welding"]
    }
)
{
    double3 xformOp:translate = (100, 0, 200)
    rel material:binding = </Factory/Materials/MetalMaterial>
}
```

   * ( ) 블록(Metadata)과 { } 블록(Attribute/Relationship)은 역할이 완전히 다릅니다.
   * 괄호는 Prim 자체를 설명하고, 중괄호는 Prim의 내용(데이터)을 담습니다.

**Kind — 모델 계층 구조**
   * kind는 Prim이 씬 계층에서 어떤 역할을 하는지 나타내는 Metadata입니다.
   * Omniverse, Houdini, USD Resolver 등 많은 도구가 kind를 기반으로 씬을 탐색합니다.

| Kind | 의미 | 우리 프로젝트 적용 | 
|:-----------:|:-----------:|:-----------:|
| assembly | 여러 component를 묶는 최상위 그룹 | /Factory | 
| group | 중간 계층 그룹 | /Factory/Robots | 
| component | 독립적으로 참조 가능한 단위 | /Factory/Robots/Robot_0 | 
| 1subcomponent | component 내부의 파츠 | Robot의 개별 링크 | 

```python
from pxr import Kind

# kind 설정
model_api = Usd.ModelAPI(prim)
model_api.SetKind(Kind.Tokens.component)

# kind 읽기
print(model_api.GetKind())          # "component"
print(model_api.IsModel())          # True (assembly/group/component 모두 해당)
print(model_api.IsGroup())          # False (component는 group 아님)
```

**프로젝트 코드 — Metadata 전면 적용**
   * .usda 텍스트 방식

```usda
#usda 1.0
(
    doc               = "Robot Factory Scene — Phase 1"
    defaultPrim       = "Factory"
    upAxis            = "Y"
    metersPerUnit     = 0.01
    startTimeCode     = 1.0
    endTimeCode       = 240.0
    timeCodesPerSecond = 24.0

    customLayerData = {
        string author  = "나무"
        string version = "0.1.0"
        string project = "RobotFactory"
    }
)

def Xform "Factory"
(
    doc  = "로봇 공장 최상위 그룹"
    kind = "assembly"
)
{
    def Scope "Robots"
    (
        doc  = "공장 내 모든 로봇 팔 그룹"
        kind = "group"
    )
    {
        def Xform "Robot_01"
        (
            doc  = "조립 라인 1번 — ARM-7X 모델"
            kind = "component"
            customData = {
                string manufacturer = "FactoryBot Inc."
                int    revision     = 3
            }
        )
        {
            double3 xformOp:translate    = (100, 0, 200)
            uniform token[] xformOpOrder = ["xformOp:translate"]
            custom int custom:serialNumber = 1001
            rel material:binding = </Factory/Materials/MetalMaterial>
        }

        def Xform "Robot_02"
        (
            doc  = "조립 라인 2번 — ARM-7X 모델"
            kind = "component"
            customData = {
                string manufacturer = "FactoryBot Inc."
                int    revision     = 3
            }
        )
        {
            double3 xformOp:translate    = (300, 0, 200)
            uniform token[] xformOpOrder = ["xformOp:translate"]
            custom int custom:serialNumber = 1002
            rel material:binding = </Factory/Materials/MetalMaterial>
        }
    }

    def Scope "Lights"
    (
        doc  = "공장 조명 그룹"
        kind = "group"
    )
    {
        def SphereLight "KeyLight"
        (
            doc = "주 조명 — 로봇 작업 구역 조명"
        )
        {
            float   inputs:intensity     = 500.0
            float   inputs:radius        = 10.0
            color3f inputs:color         = (1.0, 0.95, 0.85)
            double3 xformOp:translate    = (0, 400, 0)
            uniform token[] xformOpOrder = ["xformOp:translate"]
            rel light:targetPrim = [
                </Factory/Robots/Robot_01>,
                </Factory/Robots/Robot_02>
            ]
        }
    }

    def Mesh "Floor"
    (
        doc = "공장 바닥면 — 20m x 20m"
    )
    {
        point3f[] points = [
            (-500,0,-500),(500,0,-500),(500,0,500),(-500,0,500)
        ]
        int[] faceVertexCounts  = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]
        rel material:binding = </Factory/Materials/FloorMaterial>
    }
}
```

**Python API 방식**

```python
from pxr import Usd, Sdf, Kind

stage = Usd.Stage.Open("factory_base.usda")

# ── Layer 레벨 Metadata ──────────────────────────────────
root = stage.GetRootLayer()
root.documentation = "Robot Factory Scene — Phase 1"
root.startTimeCode = 1.0
root.endTimeCode   = 240.0
root.timeCodesPerSecond = 24.0

# customLayerData — dict 형태로 설정
root.customLayerData = {
    "author":  "나무",
    "version": "0.1.0",
    "project": "RobotFactory",
}

# ── Prim 레벨 Metadata ────────────────────────────────────
factory = stage.GetPrimAtPath("/Factory")
factory.SetMetadata("doc",  "로봇 공장 최상위 그룹")
factory.SetMetadata("kind", Kind.Tokens.assembly)

robot_01 = stage.GetPrimAtPath("/Factory/Robots/Robot_01")
robot_01.SetMetadata("doc",  "조립 라인 1번 — ARM-7X 모델")
robot_01.SetMetadata("kind", Kind.Tokens.component)

# customData — SetCustomData 로 딕셔너리 통째로
robot_01.SetCustomData({
    "manufacturer": "FactoryBot Inc.",
    "revision":     3,
})

# customData 개별 키 설정/읽기
robot_01.SetCustomDataByKey("revision", 4)
print(robot_01.GetCustomDataByKey("manufacturer"))  # "FactoryBot Inc."

# ── Metadata 읽기 ─────────────────────────────────────────
print(robot_01.GetMetadata("doc"))    # "조립 라인 1번 — ARM-7X 모델"
print(robot_01.GetCustomData())       # {'manufacturer': ..., 'revision': ...}

# kind 기반 씬 탐색 — IsModel() 필터
for prim in stage.Traverse():
    if Usd.ModelAPI(prim).IsModel():
        print(f"{prim.GetPath()}  kind={Usd.ModelAPI(prim).GetKind()}")

stage.Save()
```

**Metadata 읽기 전략 — GetAllMetadata**

```python
prim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

# 모든 Metadata를 딕셔너리로 반환
all_meta = prim.GetAllMetadata()
for key, val in all_meta.items():
    print(f"  {key:20s} = {val}")

# 출력 예:
#   doc                  = 조립 라인 1번 — ARM-7X 모델
#   kind                 = component
#   customData           = {'manufacturer': 'FactoryBot Inc.', 'revision': 3}
#   typeName             = Xform
#   specifier            = def
```

**Phase 1 완료 — 지금까지 프로젝트 상태**

```
factory_base.usda
│
│  [Layer Metadata]
│  doc / defaultPrim / upAxis / metersPerUnit
│  startTimeCode=1  endTimeCode=240  timeCodesPerSecond=24
│  customLayerData: author / version / project
│
└── /Factory                    (Xform, kind=assembly)    ← Metadata 추가
    ├── /Factory/Materials
    │   ├── MetalMaterial        (Material)
    │   └── FloorMaterial        (Material)
    ├── /Factory/Robots          (Scope, kind=group)       ← Metadata 추가
    │   ├── Robot_01             (Xform, kind=component)   ← Metadata 추가
    │   │     translate / rotateY / serialNumber
    │   │     rel material:binding → MetalMaterial
    │   │     customData: manufacturer / revision
    │   └── Robot_02             (Xform, kind=component)   ← Metadata 추가
    ├── /Factory/Lights          (Scope, kind=group)       ← Metadata 추가
    │   └── KeyLight             (SphereLight)
    │         rel light:targetPrim → [Robot_01, Robot_02]
    └── /Factory/Floor           (Mesh)
          rel material:binding → FloorMaterial
```

   * Phase 1이 완료되었습니다.
   * Stage · Prim · Attributes · Relationships · Metadata — USD 씬의 기초 구조가 모두 갖춰졌습니다.

---

## Phase 2로 진입합니다
  * 다음 모듈 ⑥ Scope부터는 공장 씬의 공간 구조를 다듬습니다.
  * 지금까지 만든 /Factory/Robots, /Factory/Lights가 Scope로 선언된 이유, 그리고 Scope와 Xform의 차이가 설계적으로 왜 중요한지를 다룹니다.

## Phase 2 — Module ⑥ : Scope
**"트랜스폼 없는 논리적 컨테이너"**

<img src="usd-buildup\USD-007.png"> 

**Scope란 무엇인가**
   * Scope는 UsdGeom이 정의한 가장 단순한 Prim 타입입니다. 유일한 역할은 자식 Prim들을 논리적으로 묶는 것이며, 트랜스폼 스택에 아무런 영향을 주지 않습니다.
   * 렌더러와 DCC 툴은 트랜스폼을 계산할 때 Scope를 완전히 건너뜁니다. Scope 위에 xformOp:translate를 써도 무시됩니다 — Scope는 Schema상 XformOp를 지원하지 않습니다.

```
Scope 사용 = "이 Prim들은 같은 범주다" 라는 선언
Xform 사용 = "이 Prim들은 함께 이동한다" 라는 선언
```

**Scope를 써야 하는 세 가지 상황**
   * 1. 에셋 분류 컨테이너 — Materials, Lights, Cameras처럼 씬을 카테고리로 나눌 때. 이 그룹들은 공간적으로 이동할 필요가 없습니다.
   * 2. 논리적 필터링 단위 — DCC 툴이나 파이프라인 스크립트가 GetChildren()으로 특정 범주의 Prim만 빠르게 수집할 때.
   * 3. Reference 진입점 — 외부 .usda 파일을 Reference로 가져올 때 진입 컨테이너로 씁니다. Xform이면 Reference 시 의도치 않은 트랜스폼이 누적될 수 있습니다.

**Scope vs Xform vs Group 비교**

```
타입          트랜스폼   렌더링   주 용도
──────────────────────────────────────────────────────
Scope         없음       없음     논리 분류, 에셋 컨테이너
Xform         있음       없음     공간 그룹, 계층 트랜스폼
UsdGeom.Mesh  없음*      있음     폴리곤 지오메트리
Camera        있음       없음     카메라 뷰
*Mesh는 xformOp를 직접 가질 수 있지만 보통 부모 Xform으로 이동
```

**프로젝트 코드 — Scope 계층 정비**
   * Phase 1에서 만든 구조를 재검토합니다.
   * /Factory/Robots와 /Factory/Lights는 Scope로 충분하지만, 공장 전체를 라인 단위로 이동시켜야 하는 경우를 대비해 Line_A 조립 그룹을 Xform으로 추가합니다.

**.usda 텍스트 방식**

```usda
#usda 1.0
(
    doc               = "Robot Factory Scene — Phase 2"
    defaultPrim       = "Factory"
    upAxis            = "Y"
    metersPerUnit     = 0.01
    startTimeCode     = 1.0
    endTimeCode       = 240.0
    timeCodesPerSecond = 24.0
    customLayerData = {
        string author  = "나무"
        string version = "0.2.0"
    }
)

def Xform "Factory"
(
    doc  = "로봇 공장 최상위 그룹"
    kind = "assembly"
)
{
    # ── Scope: 논리 분류 컨테이너 ─────────────────────────
    def Scope "Materials"
    (
        doc = "머티리얼 에셋 컨테이너 — 트랜스폼 불필요"
    )
    {
        def Material "MetalMaterial" { }
        def Material "FloorMaterial" { }
    }

    # Scope: 조명은 개별 위치를 갖지만
    # 그룹 자체를 이동할 일이 없으므로 Scope
    def Scope "Lights"
    (
        doc  = "조명 에셋 컨테이너"
        kind = "group"
    )
    {
        def SphereLight "KeyLight"
        (
            doc = "주 조명"
        )
        {
            float   inputs:intensity     = 500.0
            color3f inputs:color         = (1.0, 0.95, 0.85)
            double3 xformOp:translate    = (0, 400, 0)
            uniform token[] xformOpOrder = ["xformOp:translate"]
        }
    }

    # ── Xform: 공간 이동이 필요한 조립 라인 ──────────────
    # Line_A 전체를 한 번에 이동할 수 있다
    def Xform "Line_A"
    (
        doc  = "조립 라인 A — 전체를 이동 가능한 Xform 그룹"
        kind = "group"
    )
    {
        double3 xformOp:translate    = (0, 0, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]

        # Robots는 Line_A 안의 논리 분류 → Scope
        def Scope "Robots"
        (
            doc  = "라인 A 로봇 그룹"
            kind = "group"
        )
        {
            def Xform "Robot_01"
            (
                doc  = "조립 라인 A — 1번 로봇"
                kind = "component"
                customData = {
                    string manufacturer = "FactoryBot Inc."
                    int    revision     = 3
                }
            )
            {
                double3 xformOp:translate    = (100, 0, 200)
                uniform token[] xformOpOrder = ["xformOp:translate"]
                custom int custom:serialNumber = 1001
                rel material:binding = </Factory/Materials/MetalMaterial>
            }

            def Xform "Robot_02"
            (
                doc  = "조립 라인 A — 2번 로봇"
                kind = "component"
                customData = {
                    string manufacturer = "FactoryBot Inc."
                    int    revision     = 3
                }
            )
            {
                double3 xformOp:translate    = (300, 0, 200)
                uniform token[] xformOpOrder = ["xformOp:translate"]
                custom int custom:serialNumber = 1002
                rel material:binding = </Factory/Materials/MetalMaterial>
            }
        }
    }

    # Floor는 이동 불필요 — Xform 없이 Mesh 직접
    def Mesh "Floor"
    (
        doc = "공장 바닥면 20m x 20m"
    )
    {
        point3f[] points = [
            (-500,0,-500),(500,0,-500),(500,0,500),(-500,0,500)
        ]
        int[] faceVertexCounts  = [4]
        int[] faceVertexIndices = [0, 1, 2, 3]
        rel material:binding = </Factory/Materials/FloorMaterial>
    }
}
```

**Python API 방식**

```python
from pxr import Usd, UsdGeom, Sdf

stage = Usd.Stage.Open("factory_base.usda")

# Scope 생성 — DefinePrim 두 번째 인자로 "Scope"
materials = stage.DefinePrim("/Factory/Materials", "Scope")
lights    = stage.DefinePrim("/Factory/Lights",    "Scope")

# Xform 생성 — 라인 단위 이동 가능 그룹
line_a = UsdGeom.Xform.Define(stage, "/Factory/Line_A")
line_a.GetPrim().SetMetadata("doc", "조립 라인 A — Xform 그룹")

# Line_A 아래 Scope로 로봇 분류
robots = stage.DefinePrim("/Factory/Line_A/Robots", "Scope")

# Prim 타입 확인
prim = stage.GetPrimAtPath("/Factory/Line_A/Robots")
print(prim.GetTypeName())             # Scope
print(prim.IsA(UsdGeom.Scope))        # True
print(prim.IsA(UsdGeom.Xform))        # False

# Scope 타입 체크 유틸
def is_logical_container(prim):
    return prim.GetTypeName() == "Scope"

# Scope 하위 Prim만 수집
def collect_by_scope(stage, scope_path):
    scope = stage.GetPrimAtPath(scope_path)
    if not scope.IsValid():
        return []
    return [c for c in scope.GetChildren()]

robots_list = collect_by_scope(stage, "/Factory/Line_A/Robots")
for r in robots_list:
    print(r.GetPath())   # /Factory/Line_A/Robots/Robot_01 ...

stage.Save()
```

**Scope 탐색 패턴 — 파이프라인 활용**

```python
# 씬 안의 모든 Scope 찾기 (에셋 분류 구조 파악)
for prim in stage.Traverse():
    if prim.GetTypeName() == "Scope":
        children = list(prim.GetChildren())
        print(f"{prim.GetPath()}  ({len(children)} children)")

# 특정 Scope의 직계 자식만 처리
# — Traverse()는 전체 하위 트리를 내려가므로
#   GetChildren()으로 한 레벨만 보는 것이 명확
scope = stage.GetPrimAtPath("/Factory/Line_A/Robots")
for child in scope.GetChildren():
    if child.IsActive():
        print(f"  active robot: {child.GetName()}")
```

**지금까지 프로젝트 상태**

```
factory_base.usda
└── /Factory                          (Xform, kind=assembly)
    ├── /Factory/Materials            (Scope) ← 논리 분류
    │   ├── MetalMaterial             (Material)
    │   └── FloorMaterial             (Material)
    ├── /Factory/Lights               (Scope) ← 논리 분류
    │   └── KeyLight                  (SphereLight)
    ├── /Factory/Line_A               (Xform) ← 공간 이동 가능 ★ 추가
    │   └── /Factory/Line_A/Robots    (Scope) ← 논리 분류
    │       ├── Robot_01              (Xform, kind=component)
    │       └── Robot_02              (Xform, kind=component)
    └── /Factory/Floor                (Mesh)
```
   
   * Scope와 Xform의 역할 분리가 명확해졌습니다.
   * 다음 모듈 ⑦ Xform에서는 트랜스폼 자체를 깊이 파고듭니다.
   * xformOp 네임스페이스가 왜 그런 구조인지, xformOpOrder가 왜 필수인지, 그리고 로봇 팔의 관절 계층을 올바르게 쌓는 방법을 다룹니다.

---
## Phase 2 — Module ⑦ : Xform

**"공간을 지배하는 트랜스폼 시스템"**

<img src="usd-buildup\USD-008.png"> <img src="usd-buildup\USD-009.png">

**xformOp 네임스페이스가 존재하는 이유**

   * USD 이전의 3D 포맷들은 트랜스폼을 단일 행렬이나 TRS(Translate-Rotate-Scale) 세 값으로 저장했습니다.
   * USD는 다른 접근을 선택했습니다. 트랜스폼을 Op(연산) 목록으로 저장하고, 그 목록을 순서대로 곱해서 최종 행렬을 만듭니다.

* 이 설계의 이유는 세 가지입니다.
```
1. 피벗 회전 표현
   translate → rotatePivot → rotateY → rotatePivotInverse
   → 단일 행렬로는 표현할 수 없는 피벗 기반 회전이 가능

2. DCC 툴 간 호환
   Maya의 트랜스폼 스택을 Houdini로 가져올 때
   Op 목록을 그대로 보존하면 결과가 동일

3. 애니메이션 분리
   translate만 키프레임, rotate는 고정
   → 각 Op를 독립적으로 애니메이션 가능
```

**xformOp의 종류**

```
# 이동
xformOp:translate          double3
xformOp:translate:pivot    double3   (suffix 버전)

# 회전 — 오일러
xformOp:rotateX            double
xformOp:rotateY            double
xformOp:rotateZ            double
xformOp:rotateXYZ          double3   (XYZ 오일러 한번에)
xformOp:rotateXZY          double3
xformOp:rotateYXZ          double3
... (6가지 순열)

# 회전 — 쿼터니언
xformOp:orient             quatd

# 스케일
xformOp:scale              double3

# 행렬 직접 지정
xformOp:transform          matrix4d  (전체 행렬을 직접)

# 반전 Op — 피벗 복원용
!invert!xformOp:translate:pivot
```

* !invert! 접두사는 해당 Op의 역행렬을 적용합니다. 피벗 회전의 전형적인 패턴은 다음과 같습니다.

```usda
uniform token[] xformOpOrder = [
    "xformOp:translate",
    "xformOp:translate:pivot",
    "xformOp:rotateY",
    "!invert!xformOp:translate:pivot"
]
```

**xformOpOrder — 반드시 명시해야 하는 이유**

* xformOpOrder가 없으면 USD는 xformOp:* Attribute들이 있어도 트랜스폼을 계산하지 않습니다.
* 어떤 Op를 어떤 순서로 곱할지 명시적으로 선언해야 합니다.

```usda
# 잘못된 예 — xformOpOrder 없음
def Xform "Robot_01"
{
    double3 xformOp:translate = (100, 0, 200)
    double  xformOp:rotateY   = 45.0
    # → 트랜스폼이 적용되지 않음!
}

# 올바른 예 — xformOpOrder 명시
def Xform "Robot_01"
{
    double3 xformOp:translate = (100, 0, 200)
    double  xformOp:rotateY   = 45.0
    uniform token[] xformOpOrder = [
        "xformOp:translate",
        "xformOp:rotateY"
    ]
    # → translate 후 rotateY 적용
}
```
* uniform이 붙는 이유는 xformOpOrder는 프레임마다 달라지면 안 되기 때문입니다. Op의 종류와 순서는 씬 전체에서 고정된 구조입니다.

**프로젝트 코드 — 로봇 팔 관절 계층 구축**
**.usda 텍스트 방식**

```usda
def Xform "Robot_01"
(
    doc  = "조립 라인 A — 1번 로봇 팔"
    kind = "component"
)
{
    # Base 위치 — 공장 바닥 기준
    double3 xformOp:translate    = (100, 0, 200)
    double  xformOp:rotateY      = 0.0
    uniform token[] xformOpOrder = [
        "xformOp:translate",
        "xformOp:rotateY"
    ]

    rel material:binding = </Factory/Materials/MetalMaterial>
    custom int custom:serialNumber = 1001

    # ── 관절 계층 ─────────────────────────────────────────
    def Xform "Shoulder"
    (
        doc = "어깨 관절 — Z축 회전"
    )
    {
        # 부모(Robot_01) 로컬 좌표 기준 위치
        double3 xformOp:translate    = (0, 80, 0)
        double  xformOp:rotateZ      = 0.0
        uniform token[] xformOpOrder = [
            "xformOp:translate",
            "xformOp:rotateZ"
        ]

        def Xform "Elbow"
        (
            doc = "팔꿈치 관절 — Z축 회전"
        )
        {
            double3 xformOp:translate    = (0, 120, 0)
            double  xformOp:rotateZ      = 0.0
            uniform token[] xformOpOrder = [
                "xformOp:translate",
                "xformOp:rotateZ"
            ]

            def Xform "Wrist"
            (
                doc = "손목 관절 — Z축 회전"
            )
            {
                double3 xformOp:translate    = (0, 80, 0)
                double  xformOp:rotateZ      = 0.0
                uniform token[] xformOpOrder = [
                    "xformOp:translate",
                    "xformOp:rotateZ"
                ]

                def Xform "EndEffector"
                (
                    doc = "엔드 이펙터 — 용접 툴 장착점"
                )
                {
                    double3 xformOp:translate    = (0, 40, 0)
                    uniform token[] xformOpOrder = ["xformOp:translate"]
                }
            }
        }
    }
}
```

**Python API 방식**

```python
from pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.Open("factory_base.usda")

# ── 관절 계층 생성 헬퍼 ───────────────────────────────────
def make_joint(stage, path, translate, rotate_z=0.0, doc=""):
    """Xform Prim을 만들고 translate + rotateZ Op를 설정."""
    xform = UsdGeom.Xform.Define(stage, path)
    prim  = xform.GetPrim()
    if doc:
        prim.SetMetadata("doc", doc)

    # translate Op 추가
    t_op = xform.AddTranslateOp()
    t_op.Set(Gf.Vec3d(*translate))

    # rotateZ Op 추가 (기본값 0 — 애니메이션은 Module ⑨)
    r_op = xform.AddRotateZOp()
    r_op.Set(rotate_z)

    return xform

# ── Robot_01 관절 트리 구축 ───────────────────────────────
base      = "/Factory/Line_A/Robots/Robot_01"
shoulder  = make_joint(stage, f"{base}/Shoulder",
                       translate=(0, 80, 0),  doc="어깨 관절")
elbow     = make_joint(stage, f"{base}/Shoulder/Elbow",
                       translate=(0, 120, 0), doc="팔꿈치 관절")
wrist     = make_joint(stage, f"{base}/Shoulder/Elbow/Wrist",
                       translate=(0, 80, 0),  doc="손목 관절")
ee_path   = f"{base}/Shoulder/Elbow/Wrist/EndEffector"
ee        = UsdGeom.Xform.Define(stage, ee_path)
t_op      = ee.AddTranslateOp()
t_op.Set(Gf.Vec3d(0, 40, 0))

# Robot_02도 동일 구조 복사
base2 = "/Factory/Line_A/Robots/Robot_02"
make_joint(stage, f"{base2}/Shoulder",
           translate=(0, 80, 0),  doc="어깨 관절")
make_joint(stage, f"{base2}/Shoulder/Elbow",
           translate=(0, 120, 0), doc="팔꿈치 관절")
make_joint(stage, f"{base2}/Shoulder/Elbow/Wrist",
           translate=(0, 80, 0),  doc="손목 관절")

stage.Save()
```

**World Transform 계산 — 계층 누적 확인**

```python
from pxr import UsdGeom, Usd

stage = Usd.Stage.Open("factory_base.usda")

# 특정 시간에서 World Transform 행렬 가져오기
time = Usd.TimeCode.Default()

def get_world_xform(stage, path):
    prim     = stage.GetPrimAtPath(path)
    xformable = UsdGeom.Xformable(prim)
    # GetLocalToWorldTransform → 루트까지 누적된 행렬
    matrix   = xformable.ComputeLocalToWorldTransform(time)
    return matrix

# 각 관절의 World 위치 출력
joints = [
    "/Factory/Line_A/Robots/Robot_01",
    "/Factory/Line_A/Robots/Robot_01/Shoulder",
    "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow",
    "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow/Wrist",
    "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow/Wrist/EndEffector",
]

for path in joints:
    m = get_world_xform(stage, path)
    # 행렬의 4번째 행 = World 위치 (translation 성분)
    tx, ty, tz = m[3][0], m[3][1], m[3][2]
    name = path.split("/")[-1]
    print(f"{name:15s}  world=({tx:6.1f}, {ty:6.1f}, {tz:6.1f})")

# 출력 예:
# Robot_01        world=( 100.0,   0.0, 200.0)
# Shoulder        world=( 100.0,  80.0, 200.0)
# Elbow           world=( 100.0, 200.0, 200.0)
# Wrist           world=( 100.0, 280.0, 200.0)
# EndEffector     world=( 100.0, 320.0, 200.0)
```

**XformCommonAPI vs 직접 Op 추가 — 선택 기준**

```python
# ── XformCommonAPI (간편, 제한적) ──────────────────────────
# TRS만 쓰는 단순한 경우에 적합
api = UsdGeom.XformCommonAPI(xform)
api.SetTranslate(Gf.Vec3d(100, 0, 200))
api.SetRotate(Gf.Vec3f(0, 45, 0),
              UsdGeom.XformCommonAPI.RotationOrderYXZ)
api.SetScale(Gf.Vec3f(1, 1, 1))
# → xformOpOrder를 자동 관리, 피벗·suffix 미지원

# ── 직접 Op 추가 (유연, 명시적) ───────────────────────────
# 피벗 회전, suffix, !invert! 가 필요한 경우
xform.AddTranslateOp().Set(Gf.Vec3d(100, 0, 200))
xform.AddRotateYOp(
    opSuffix="pivot"          # suffix → xformOp:rotateY:pivot
).Set(45.0)
# → xformOpOrder에 자동 추가됨

# ── 현재 Op 목록 조회 ──────────────────────────────────────
ops = xform.GetOrderedXformOps()
for op in ops:
    print(f"  {op.GetOpName():35s} = {op.Get()}")
```

**resetXformStack — 부모 트랜스폼 차단**
   * 특수한 경우에 부모의 트랜스폼을 상속받지 않고 완전히 독립적인 World 좌표를 쓰고 싶을 때 resetXformStack 플래그를 씁니다.

```usda
def Xform "FixedCamera"
{
    double3 xformOp:translate    = (0, 200, -500)
    uniform token[] xformOpOrder = [
        "xformOp:resetXformStack",   # ← 부모 트랜스폼 무시
        "xformOp:translate"
    ]
}
```

```python
# Python에서 resetXformStack 추가
xform.SetResetXformStack(True)
```
* 주의: 일반 씬에서 남용하면 계층 구조의 의미가 깨집니다. 카메라나 환경 맵처럼 씬 계층과 독립적으로 고정되어야 할 오브젝트에만 씁니다.

**지금까지 프로젝트 상태**
```
factory_base.usda
└── /Factory
    ├── /Factory/Materials           (Scope)
    ├── /Factory/Lights              (Scope)
    │   └── KeyLight
    ├── /Factory/Line_A              (Xform) translate=(0,0,0)
    │   └── Robots                  (Scope)
    │       ├── Robot_01            (Xform) translate=(100,0,200) rotateY=0
    │       │   └── Shoulder        (Xform) translate=(0,80,0)  rotateZ=0 ★
    │       │       └── Elbow       (Xform) translate=(0,120,0) rotateZ=0 ★
    │       │           └── Wrist   (Xform) translate=(0,80,0)  rotateZ=0 ★
    │       │               └── EndEffector (Xform) translate=(0,40,0)   ★
    │       └── Robot_02            (Xform) — 동일 관절 계층
    └── /Factory/Floor              (Mesh)
```
   * 로봇 팔의 관절 계층이 완성되었습니다.
   * 각 관절의 rotateZ 값이 현재 0.0으로 고정되어 있는데, 이것이 Module ⑨ TimeSamples에서 프레임마다 달라지는 애니메이션 데이터로 채워집니다.
   * 다음 모듈 ⑧ Primvars에서는 렌더러에 데이터를 전달하는 특수한 Attribute인 Primvar를 다룹니다.
   * 지금 Floor에 붙어 있는 primvars:displayColor가 왜 일반 Attribute와 다른지, 그리고 interpolation이 Mesh 렌더링에 어떤 영향을 주는지를 깊이 파고듭니다.

---

## Phase 2 — Module ⑧ : Primvars
**"렌더러에게 데이터를 전달하는 특수 Attribute"**

<img src="usd-buildup\USD-010.png"> <img src="usd-buildup\USD-011.png">

**Primvar란 무엇인가**
   * Primvar(Primitive Variable)는 primvars: 네임스페이스를 가진 특수 Attribute입니다. 일반 Attribute와 세 가지 점에서 다릅니다.

```
일반 Attribute     렌더러가 직접 읽지 않음
                   자식에게 상속되지 않음
                   interpolation 없음

Primvar            렌더러·Shader가 직접 연결해서 읽음
                   자식 Prim으로 자동 상속(cascading)
                   interpolation 메타데이터로 보간 방식 지정
```
   * 렌더러 관점에서 Primvar는 Mesh의 각 점·면·버텍스에 데이터를 어떻게 분배할지를 지정하는 채널입니다.
   * UV 좌표, 버텍스 컬러, 노멀, 커스텀 렌더 데이터가 모두 Primvar로 전달됩니다.

**Interpolation 4가지**
| 모드 | 값 개수 | 의미 | 
|:------:|:------:|:------:|
| constant | 1 | Prim 전체에 단일 값 | 
| uniform | face 수 | 면마다 하나의 값, 면 내부는 동일 | 
| varying / vertex | vertex 수 | 버텍스마다 값, 면 내부는 선형 보간 | 
| faceVaryingface | Vertex 수 | UV처럼 면마다 독립적인 버텍스 값 | 

* faceVarying이 UV 텍스처 좌표에 쓰이는 이유는 — 하나의 버텍스가 여러 면에 공유되더라도 면마다 UV 좌표가 달라야 하기 때문입니다.

**프로젝트 코드 — Primvar 추가**
   * .usda 텍스트 방식

```usda
def Mesh "Floor"
(
    doc = "공장 바닥면"
)
{
    point3f[] points = [
        (-500,0,-500),(500,0,-500),(500,0,500),(-500,0,500)
    ]
    int[] faceVertexCounts  = [4]
    int[] faceVertexIndices = [0, 1, 2, 3]

    # constant — 바닥 전체 한 가지 색
    color3f[] primvars:displayColor = [(0.25, 0.25, 0.25)]
    (
        interpolation = "constant"
    )

    # faceVarying — UV 좌표 (면당 독립 버텍스)
    texCoord2f[] primvars:st = [
        (0,0),(1,0),(1,1),(0,1)
    ]
    (
        interpolation = "faceVarying"
    )
    int[] primvars:st:indices = [0, 1, 2, 3]

    rel material:binding = </Factory/Materials/FloorMaterial>
}

def Xform "Robot_01"
(
    doc  = "조립 라인 A — 1번 로봇"
    kind = "component"
)
{
    double3 xformOp:translate    = (100, 0, 200)
    uniform token[] xformOpOrder = ["xformOp:translate"]

    # constant — 로봇 전체 단일 색 (자식 Shoulder/Elbow/Wrist 로 상속)
    color3f[] primvars:displayColor = [(0.15, 0.15, 0.6)]
    (
        interpolation = "constant"
    )

    # 커스텀 렌더 데이터 — 렌더러 파라미터 전달용
    float primvars:robotGloss = 0.85
    (
        interpolation = "constant"
    )

    rel material:binding = </Factory/Materials/MetalMaterial>
    custom int custom:serialNumber = 1001
}
```

**Python API 방식**

```python
from pxr import Usd, UsdGeom, Sdf, Gf, Vt

stage = Usd.Stage.Open("factory_base.usda")

# ── Floor Primvar 설정 ─────────────────────────────────────
floor_mesh = UsdGeom.Mesh(stage.GetPrimAtPath("/Factory/Floor"))
pvAPI      = UsdGeom.PrimvarsAPI(floor_mesh.GetPrim())

# displayColor — constant
dc = pvAPI.CreatePrimvar(
    "displayColor",
    Sdf.ValueTypeNames.Color3fArray,
    UsdGeom.Tokens.constant
)
dc.Set(Vt.Vec3fArray([Gf.Vec3f(0.25, 0.25, 0.25)]))

# UV (st) — faceVarying
st = pvAPI.CreatePrimvar(
    "st",
    Sdf.ValueTypeNames.TexCoord2fArray,
    UsdGeom.Tokens.faceVarying
)
st.Set(Vt.Vec2fArray([
    Gf.Vec2f(0,0), Gf.Vec2f(1,0),
    Gf.Vec2f(1,1), Gf.Vec2f(0,1),
]))
st.SetIndices(Vt.IntArray([0, 1, 2, 3]))

# ── Robot_01 Primvar 설정 ──────────────────────────────────
robot_prim = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
robot_pvAPI = UsdGeom.PrimvarsAPI(robot_prim)

# displayColor — constant (자식 Shoulder/Elbow/Wrist로 상속)
rc = robot_pvAPI.CreatePrimvar(
    "displayColor",
    Sdf.ValueTypeNames.Color3fArray,
    UsdGeom.Tokens.constant
)
rc.Set(Vt.Vec3fArray([Gf.Vec3f(0.15, 0.15, 0.6)]))

# 커스텀 렌더 파라미터
gloss = robot_pvAPI.CreatePrimvar(
    "robotGloss",
    Sdf.ValueTypeNames.Float,
    UsdGeom.Tokens.constant
)
gloss.Set(0.85)

stage.Save()
```

**Primvar 읽기 — 상속 추적**

```python
from pxr import UsdGeom

# 자식 Prim에서 상속된 Primvar 포함해서 조회
shoulder = stage.GetPrimAtPath(
    "/Factory/Line_A/Robots/Robot_01/Shoulder"
)
pvAPI = UsdGeom.PrimvarsAPI(shoulder)

# 자신이 직접 가진 Primvar만
for pv in pvAPI.GetPrimvars():
    print(f"  own  {pv.GetName():30s} interp={pv.GetInterpolation()}")

# 상속 포함 (부모 체인 탐색)
for pv in pvAPI.FindInheritablePrimvars():
    print(f"  inh  {pv.GetName():30s} = {pv.Get()}")

# 특정 Primvar 직접 접근
dc = pvAPI.FindPrimvarWithInheritance("displayColor")
if dc:
    print(dc.Get())           # [(0.15, 0.15, 0.6)]  Robot_01에서 상속
    print(dc.GetInterpolation())  # constant
    print(dc.GetPrimvarName())    # displayColor
```

**indices — 메모리 절약 패턴**
   * Primvar는 SetIndices()로 값 배열을 인덱싱할 수 있습니다. 동일한 값을 반복하지 않고 인덱스로 참조하는 방식입니다.

```usda
# 4개 face에 2가지 색만 쓰는 경우
color3f[] primvars:displayColor = [(1,0,0), (0,0,1)]
(
    interpolation = "uniform"
)
# face 0,2는 빨강(인덱스 0), face 1,3은 파랑(인덱스 1)
int[] primvars:displayColor:indices = [0, 1, 0, 1]
```

**지금까지 프로젝트 상태**

```
factory_base.usda
└── /Factory
    ├── /Factory/Materials           (Scope)
    ├── /Factory/Lights              (Scope)
    ├── /Factory/Line_A              (Xform)
    │   └── Robots                  (Scope)
    │       ├── Robot_01            (Xform)
    │       │   primvars:displayColor = [(0.15,0.15,0.6)]  ★ 추가
    │       │   primvars:robotGloss  = 0.85                ★ 추가
    │       │   └── Shoulder / Elbow / Wrist / EndEffector
    │       │         (displayColor 자동 상속)             ★
    │       └── Robot_02            (Xform)
    └── /Factory/Floor              (Mesh)
          primvars:displayColor = [(0.25,0.25,0.25)]       ★ 추가
          primvars:st (UV, faceVarying)                     ★ 추가
```

Phase 2 완료입니다. Scope·Xform·Primvars — 씬의 공간 구조와 렌더 데이터 채널이 모두 갖춰졌습니다.

---

## Phase 3

다음 모듈 ⑨ TimeCodes & TimeSamples에서는 지금까지 0.0으로 고정된 각 관절의 rotateZ 값에 키프레임을 심어 로봇 팔이 실제로 움직이게 만듭니다.

## Phase 3 — Module ⑨ : TimeCodes & TimeSamples

**"로봇 팔이 움직인다 — 씬에 시간을 심다"**

<img src="usd-buildup\USD-012.png">

* TimeCode란 무엇인가

USD의 시간 단위는 TimeCode입니다. 초(second)가 아니라 추상적인 숫자입니다. timeCodesPerSecond로 실제 시간과 연결합니다.
timeCodesPerSecond = 24.0
startTimeCode = 1.0
endTimeCode   = 240.0

→ TimeCode 1 = 0초
  TimeCode 24 = 1초
  TimeCode 240 = 10초 (총 10초 애니메이션)
TimeCode를 초와 분리한 이유는 파이프라인마다 fps가 다르기 때문입니다. 24fps 영화, 30fps 게임, 60fps 로보틱스 시뮬레이션이 같은 USD 파일을 timeCodesPerSecond만 바꿔서 공유할 수 있습니다.

TimeSamples — Attribute에 키프레임 심기
Attribute는 Default Value(시간 무관 고정값)와 TimeSamples(프레임별 값 딕셔너리) 중 하나 또는 둘 다를 가질 수 있습니다.
TimeSample이 있는 프레임에서는 TimeSample 값이 우선합니다. TimeSample이 없는 프레임에서는 앞뒤 샘플 사이를 선형 보간합니다.
attr.Get(TimeCode(30))  →  f1=0°, f60=45° 사이  →  22.5°  (선형 보간)
attr.Get(TimeCode(60))  →  정확히 키프레임      →  45.0°
attr.Get(TimeCode.Default()) → Default Value   →  0.0°

프로젝트 코드 — 로봇 팔 관절 애니메이션
.usda 텍스트 방식
usda#usda 1.0
(
    doc                = "Robot Factory Scene — Phase 3 Animation"
    defaultPrim        = "Factory"
    upAxis             = "Y"
    metersPerUnit      = 0.01
    startTimeCode      = 1.0
    endTimeCode        = 240.0
    timeCodesPerSecond = 24.0
)

def Xform "Factory"
{
    def Xform "Line_A"
    {
        def Scope "Robots"
        {
            def Xform "Robot_01"
            {
                double3 xformOp:translate    = (100, 0, 200)
                double  xformOp:rotateY      = 0.0
                uniform token[] xformOpOrder = [
                    "xformOp:translate",
                    "xformOp:rotateY"
                ]

                def Xform "Shoulder"
                {
                    double3 xformOp:translate    = (0, 80, 0)
                    uniform token[] xformOpOrder = [
                        "xformOp:translate",
                        "xformOp:rotateZ"
                    ]

                    # TimeSamples — 중괄호 안에 TimeCode: value
                    double xformOp:rotateZ.timeSamples = {
                        1:    0.0,
                        60:   45.0,
                        120: -30.0,
                        180:  60.0,
                        240:   0.0
                    }

                    def Xform "Elbow"
                    {
                        double3 xformOp:translate    = (0, 120, 0)
                        uniform token[] xformOpOrder = [
                            "xformOp:translate",
                            "xformOp:rotateZ"
                        ]

                        double xformOp:rotateZ.timeSamples = {
                            1:    0.0,
                            60:   30.0,
                            120: -60.0,
                            180:  45.0,
                            240:   0.0
                        }

                        def Xform "Wrist"
                        {
                            double3 xformOp:translate    = (0, 80, 0)
                            uniform token[] xformOpOrder = [
                                "xformOp:translate",
                                "xformOp:rotateZ"
                            ]

                            double xformOp:rotateZ.timeSamples = {
                                1:    0.0,
                                60:  -20.0,
                                120:  40.0,
                                180: -50.0,
                                240:   0.0
                            }

                            def Xform "EndEffector"
                            {
                                double3 xformOp:translate    = (0, 40, 0)
                                uniform token[] xformOpOrder = ["xformOp:translate"]
                            }
                        }
                    }
                }
            }
        }
    }
}
Python API 방식
pythonfrom pxr import Usd, UsdGeom, Gf

stage = Usd.Stage.Open("factory_base.usda")

# ── TimeSample 헬퍼 ────────────────────────────────────────
def set_rotate_z_anim(stage, path, keyframes: dict):
    """
    keyframes = {timeCode: degrees, ...}
    path의 xformOp:rotateZ 에 TimeSample 설정
    """
    prim  = stage.GetPrimAtPath(path)
    xform = UsdGeom.Xform(prim)

    # 이미 Op가 있으면 가져오고, 없으면 추가
    ops = {op.GetOpName(): op for op in xform.GetOrderedXformOps()}
    if "xformOp:rotateZ" in ops:
        rz_attr = ops["xformOp:rotateZ"].GetAttr()
    else:
        rz_attr = xform.AddRotateZOp().GetAttr()

    # 키프레임 설정
    for tc, deg in keyframes.items():
        rz_attr.Set(deg, Usd.TimeCode(tc))

# ── 각 관절 키프레임 설정 ──────────────────────────────────
base = "/Factory/Line_A/Robots/Robot_01"

set_rotate_z_anim(stage, f"{base}/Shoulder", {
    1:   0.0,
    60:  45.0,
    120: -30.0,
    180: 60.0,
    240: 0.0,
})

set_rotate_z_anim(stage, f"{base}/Shoulder/Elbow", {
    1:   0.0,
    60:  30.0,
    120: -60.0,
    180: 45.0,
    240: 0.0,
})

set_rotate_z_anim(stage, f"{base}/Shoulder/Elbow/Wrist", {
    1:   0.0,
    60:  -20.0,
    120: 40.0,
    180: -50.0,
    240: 0.0,
})

# ── visibility 애니메이션 (held 보간) ──────────────────────
robot_02 = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_02")
vis_attr = UsdGeom.Imageable(robot_02).GetVisibilityAttr()

# held 보간: 다음 키까지 값 유지
vis_attr.Set("inherited",  Usd.TimeCode(1))    # f1~119 보임
vis_attr.Set("invisible",  Usd.TimeCode(120))  # f120부터 사라짐
vis_attr.Set("inherited",  Usd.TimeCode(180))  # f180부터 다시 보임

stage.Save()

TimeSample 읽기 · 검사
pythonprim  = stage.GetPrimAtPath(
    "/Factory/Line_A/Robots/Robot_01/Shoulder"
)
xform = UsdGeom.Xform(prim)
ops   = {op.GetOpName(): op for op in xform.GetOrderedXformOps()}
rz    = ops["xformOp:rotateZ"].GetAttr()

# 모든 TimeSample 시간 목록
print(rz.GetTimeSamples())
# [1.0, 60.0, 120.0, 180.0, 240.0]

# 특정 시간의 값
print(rz.Get(Usd.TimeCode(60)))    # 45.0
print(rz.Get(Usd.TimeCode(90)))    # 7.5  (60→120 선형 보간)
print(rz.Get())                     # 0.0  (Default Value)

# TimeSample 범위 확인
lo, hi = rz.GetBracketingTimeSamples(90)
print(lo, hi)   # 60.0  120.0

# Stage 전체 시간 범위
print(stage.GetStartTimeCode())    # 1.0
print(stage.GetEndTimeCode())      # 240.0
print(stage.GetTimeCodesPerSecond()) # 24.0

레이어 간 시간 오프셋 — offset / scale
SubLayer나 Reference를 연결할 때 시간을 이동하거나 배속할 수 있습니다. 로봇 팔 애니메이션을 두 로봇이 서로 엇갈려 시작하게 만들 때 유용합니다.
usda#usda 1.0
(
    subLayers = [
        @robot_anim.usda@ (
            offset = 24    # 1초 뒤에 시작
            scale  = 1.0   # 동일 속도
        ),
        @robot_anim.usda@ (
            offset = 72    # 3초 뒤에 시작
            scale  = 0.5   # 2배 느리게
        )
    ]
)
pythonfrom pxr import Sdf

root = stage.GetRootLayer()

# SubLayer에 시간 오프셋 적용
layer_offset = Sdf.LayerOffset(offset=24.0, scale=1.0)
root.subLayerOffsets[0] = layer_offset

지금까지 프로젝트 상태
factory_base.usda  (= factory_anim.usda 로 저장 권장)
└── /Factory/Line_A/Robots
    ├── Robot_01
    │   └── Shoulder
    │         rotateZ.timeSamples = {1:0, 60:45, 120:-30, 180:60, 240:0} ★
    │         └── Elbow
    │               rotateZ.timeSamples = {1:0, 60:30, 120:-60 ...}      ★
    │               └── Wrist
    │                     rotateZ.timeSamples = {1:0, 60:-20, 120:40 ...} ★
    │                     └── EndEffector
    └── Robot_02
          visibility.timeSamples = {1:"inherited", 120:"invisible" ...}  ★

* Phase 3 완료입니다. 로봇 팔이 10초 동안 세 관절이 독립적으로 움직이는 애니메이션이 완성되었습니다.

Phase 4로 진입합니다
다음 모듈 ⑩ Lighting에서는 공장 씬에 조명 체계를 구축합니다. UsdLux의 조명 타입들과 Light Linking으로 로봇에만 선택적으로 조명을 비추는 방법을 다룹니다.

---

## Phase 4 — Module ⑩ : Lighting

**"씬에 빛을 더하다 — UsdLux 조명 시스템"**

<img src="usd-buildup\USD-013.png">

UsdLux — USD 조명 시스템
UsdLux는 USD의 조명 스키마 라이브러리입니다. 렌더러에 독립적인 표준 조명 인터페이스를 제공하며, Hydra를 통해 어떤 렌더러(RenderMan, Arnold, Karma, Omniverse RTX)에서도 동일하게 해석됩니다.
모든 UsdLux 조명 Prim은 공통 Attribute를 공유합니다.
inputs:intensity     float    밝기 (선형 배율)
inputs:exposure      float    EV 단위 밝기 (2^exposure × intensity)
inputs:color         color3f  조명 색상
inputs:diffuse       float    디퓨즈 기여도 (0~1)
inputs:specular      float    스페큘러 기여도 (0~1)
inputs:normalize     bool     면적 변화에 따른 밝기 정규화

조명 타입별 핵심 Attribute
SphereLight   inputs:radius            구형 광원 크기
DiskLight     inputs:radius            원형 면 광원
RectLight     inputs:width/height      직사각형 면 광원
CylinderLight inputs:length/radius     원통형 광원
DistantLight  inputs:angle             태양광 (방향성)
DomeLight     inputs:texture:file      HDR 환경맵 asset 경로
PortalLight   (DomeLight 자식)         실내 창문 최적화

프로젝트 코드 — 공장 조명 체계 구축
.usda 텍스트 방식
usdadef Scope "Lights"
(
    doc  = "공장 조명 그룹"
    kind = "group"
)
{
    # ── 주 조명: 로봇 작업 구역 ────────────────────────────
    def SphereLight "KeyLight"
    (
        doc = "주 조명 — 로봇 작업 구역 전용"
    )
    {
        float   inputs:intensity  = 500.0
        float   inputs:radius     = 20.0
        color3f inputs:color      = (1.0, 0.95, 0.85)
        float   inputs:exposure   = 0.0
        bool    inputs:normalize  = true

        double3 xformOp:translate    = (200, 400, 200)
        uniform token[] xformOpOrder = ["xformOp:translate"]

        # Light Linking — Robot_01, Robot_02 에만 조명
        rel light:lightLink = [
            </Factory/Line_A/Robots/Robot_01>,
            </Factory/Line_A/Robots/Robot_02>
        ]
        # Shadow Linking — 동일 대상에만 그림자
        rel light:shadowLink = [
            </Factory/Line_A/Robots/Robot_01>,
            </Factory/Line_A/Robots/Robot_02>
        ]
    }

    # ── 보조 조명: 바닥 전체 Fill ─────────────────────────
    def RectLight "FillLight"
    (
        doc = "보조 조명 — 바닥 및 전체 Fill"
    )
    {
        float   inputs:intensity = 200.0
        float   inputs:width     = 800.0
        float   inputs:height    = 800.0
        color3f inputs:color     = (0.8, 0.85, 1.0)
        float   inputs:diffuse   = 1.0
        float   inputs:specular  = 0.2

        double3 xformOp:translate    = (0, 600, 0)
        double3 xformOp:rotateX      = 90.0
        uniform token[] xformOpOrder = [
            "xformOp:translate",
            "xformOp:rotateX"
        ]

        rel light:lightLink = [</Factory/Floor>]
    }

    # ── 환경 조명: HDR DomeLight ──────────────────────────
    def DomeLight "EnvLight"
    (
        doc = "HDR 환경 조명 — 씬 전체 앰비언트"
    )
    {
        float   inputs:intensity    = 0.6
        float   inputs:exposure     = 0.0
        # HDR 텍스처 — asset 타입
        asset   inputs:texture:file = @./textures/factory_hdr.hdr@
        token   inputs:texture:format = "latlong"

        double3 xformOp:rotateY      = 90.0
        uniform token[] xformOpOrder = ["xformOp:rotateY"]
        # lightLink 없음 → 씬 전체에 자동 적용
    }
}
Python API 방식
pythonfrom pxr import Usd, UsdGeom, UsdLux, Sdf, Gf

stage = Usd.Stage.Open("factory_base.usda")

lights_scope = stage.GetPrimAtPath("/Factory/Lights")

# ── KeyLight — SphereLight ────────────────────────────────
key = UsdLux.SphereLight.Define(stage, "/Factory/Lights/KeyLight")
key.GetPrim().SetMetadata("doc", "주 조명 — 로봇 작업 구역 전용")

key.CreateIntensityAttr(500.0)
key.CreateRadiusAttr(20.0)
key.CreateColorAttr(Gf.Vec3f(1.0, 0.95, 0.85))
key.CreateNormalizeAttr(True)

# 위치 설정
xf = UsdGeom.Xformable(key.GetPrim())
xf.AddTranslateOp().Set(Gf.Vec3d(200, 400, 200))

# Light Linking — Relationship 직접 설정
light_link = key.GetPrim().CreateRelationship(
    "light:lightLink", custom=False
)
light_link.AddTarget(Sdf.Path("/Factory/Line_A/Robots/Robot_01"))
light_link.AddTarget(Sdf.Path("/Factory/Line_A/Robots/Robot_02"))

shadow_link = key.GetPrim().CreateRelationship(
    "light:shadowLink", custom=False
)
shadow_link.AddTarget(Sdf.Path("/Factory/Line_A/Robots/Robot_01"))
shadow_link.AddTarget(Sdf.Path("/Factory/Line_A/Robots/Robot_02"))

# ── FillLight — RectLight ─────────────────────────────────
fill = UsdLux.RectLight.Define(stage, "/Factory/Lights/FillLight")
fill.CreateIntensityAttr(200.0)
fill.CreateWidthAttr(800.0)
fill.CreateHeightAttr(800.0)
fill.CreateColorAttr(Gf.Vec3f(0.8, 0.85, 1.0))

xf2 = UsdGeom.Xformable(fill.GetPrim())
xf2.AddTranslateOp().Set(Gf.Vec3d(0, 600, 0))
xf2.AddRotateXOp().Set(90.0)

fill_link = fill.GetPrim().CreateRelationship(
    "light:lightLink", custom=False
)
fill_link.AddTarget(Sdf.Path("/Factory/Floor"))

# ── DomeLight — HDR 환경 조명 ─────────────────────────────
dome = UsdLux.DomeLight.Define(stage, "/Factory/Lights/EnvLight")
dome.CreateIntensityAttr(0.6)
dome.CreateTextureFileAttr("./textures/factory_hdr.hdr")
dome.CreateTextureFormatAttr(UsdLux.Tokens.latlong)

xf3 = UsdGeom.Xformable(dome.GetPrim())
xf3.AddRotateYOp().Set(90.0)
# lightLink 없음 → 씬 전체 자동 적용

stage.Save()

조명 검사 — LightAPI
pythonfrom pxr import UsdLux

# 씬의 모든 조명 Prim 수집
lights = [
    p for p in stage.Traverse()
    if UsdLux.LightAPI(p)
]

for light in lights:
    api = UsdLux.LightAPI(light)
    print(f"{light.GetPath()}")
    print(f"  intensity = {api.GetIntensityAttr().Get()}")
    print(f"  color     = {api.GetColorAttr().Get()}")

    # Light Linking 대상 확인
    ll = light.GetRelationship("light:lightLink")
    if ll and ll.GetTargets():
        for t in ll.GetTargets():
            print(f"  links → {t}")
    else:
        print(f"  links → (전체 씬)")

ShadowAPI — 그림자 세부 제어
usdadef SphereLight "KeyLight"
{
    float inputs:intensity = 500.0

    # Shadow 활성화
    bool  inputs:shadow:enable   = true
    float inputs:shadow:distance = 1000.0
    float inputs:shadow:falloff  = 0.1
    color3f inputs:shadow:color  = (0.0, 0.0, 0.05)
}

지금까지 프로젝트 상태
factory_base.usda
└── /Factory
    ├── /Factory/Lights                          (Scope)
    │   ├── KeyLight    (SphereLight)            ★ 재구성
    │   │     intensity=500  radius=20
    │   │     rel light:lightLink  → [Robot_01, Robot_02]
    │   │     rel light:shadowLink → [Robot_01, Robot_02]
    │   ├── FillLight   (RectLight)              ★ 추가
    │   │     intensity=200  800×800
    │   │     rel light:lightLink  → [Floor]
    │   └── EnvLight    (DomeLight)              ★ 추가
    │         intensity=0.6
    │         texture:file = factory_hdr.hdr
    │         (lightLink 없음 — 전체 씬 적용)
    ├── /Factory/Line_A/Robots/...  (애니메이션 유지)
    └── /Factory/Floor              (Mesh)

Phase 4 조명 완료입니다. 세 종류의 조명이 Light Linking으로 각각 담당 영역을 나눠 비추고 있습니다.
다음 모듈 ⑪ File Formats에서는 .usda / .usdc / .usdz의 차이와 변환 방법, 그리고 파이프라인에서 어떤 포맷을 언제 써야 하는지를 다룹니다.

---

## Phase 4 — Module ⑪ : File Formats

**"usda · usdc · usdz — 포맷을 알면 파이프라인이 보인다"**

<img src="usd-buildup\USD-014.png">

포맷 선택 원칙
세 포맷은 용도가 다릅니다. 파일 확장자만 다른 게 아니라 파이프라인에서의 역할이 완전히 구분됩니다.
.usda   개발·디버깅·교육·Git 버전 관리
.usdc   프로덕션 파이프라인 (렌더팜, 대용량 씬)
.usdz   외부 배포 (AR, 모바일, 고객 납품)
.usd    파이프라인 중립 (내부 포맷을 숨기고 싶을 때)
.usdc의 Crate 포맷은 메모리 맵 파일 접근을 지원합니다. 1GB짜리 씬을 열 때 전체를 메모리에 올리지 않고 필요한 부분만 읽어오는 것이 가능합니다. 대형 스튜디오에서 .usda를 프로덕션에 쓰지 않는 이유입니다.

포맷 감지 — 매직 헤더
USD는 파일을 열 때 내용의 첫 바이트를 보고 포맷을 자동 판별합니다.
.usda / .usd (텍스트)   →  파일 첫 줄: #usda 1.0
.usdc / .usd (바이너리) →  파일 첫 8바이트: PXR-USDC
.usdz                   →  ZIP 시그니처: PK\x03\x04
python# 파이썬에서 포맷 확인
from pxr import Sdf

layer = Sdf.Layer.FindOrOpen("factory.usd")
print(layer.GetFileFormat().GetFormatId())
# "usda" 또는 "usdc"

프로젝트 코드 — 포맷 변환 전체 흐름
Python API 방식
pythonfrom pxr import Usd, Sdf

# ── 1. 개발 단계: .usda 작업 ──────────────────────────────
stage = Usd.Stage.Open("factory_base.usda")
# ... 편집 작업 ...
stage.Save()   # factory_base.usda 저장

# ── 2. usda → usdc 변환 ───────────────────────────────────
# 방법 A: Export (Stage 레벨)
stage.Export("factory_base.usdc")
# 방법 B: Layer 레벨 직접 변환
src = Sdf.Layer.FindOrOpen("factory_base.usda")
Sdf.Layer.CreateNew("factory_base.usdc")
dst = Sdf.Layer.FindOrOpen("factory_base.usdc")
dst.TransferContent(src)
dst.Save()

# ── 3. Flatten — 모든 레이어 합성 후 단일 파일 ───────────
# SubLayer / Reference가 여러 파일로 나뉜 경우 하나로 합침
flat_stage = Usd.Stage.Open("factory_composed.usda")
flat_stage.Flatten().Export("factory_flat.usda")
# 또는
flat_stage.Export("factory_flat.usdc")

# ── 4. usdz 패키징 ────────────────────────────────────────
from pxr import UsdUtils

# 의존 파일 자동 수집 + zip 패키징
UsdUtils.CreateNewUsdzPackage(
    assetPath   = "factory_base.usda",   # 루트 파일
    usdzFilePath= "factory.usdz"          # 출력 usdz
)

# ── 5. usdz 내용 확인 ─────────────────────────────────────
import zipfile
with zipfile.ZipFile("factory.usdz", "r") as z:
    for name in z.namelist():
        info = z.getinfo(name)
        print(f"  {name:40s} {info.file_size:>10,} bytes")

커맨드라인 도구
USD 설치 시 함께 제공되는 CLI 도구들입니다. Omniverse Kit, USD 빌드 모두 포함합니다.
bash# ── 포맷 변환 ─────────────────────────────────────────────
usdcat factory.usda -o factory.usdc        # usda → usdc
usdcat factory.usdc -o factory.usda        # usdc → usda (역변환)
usdcat --flatten factory.usda -o flat.usda # 모든 레이어 병합

# ── usdz 패키징 ───────────────────────────────────────────
usdzip -r factory.usdz factory.usdc textures/  # 패키징
usdzip -l factory.usdz                         # 내용 목록
usdzip -d factory.usdz ./extracted/            # 압축 해제

# ── 씬 검증 ──────────────────────────────────────────────
usdchecker factory.usda          # 스키마 유효성 검사
usdchecker factory.usdz          # usdz 규격 준수 검사

# ── 씬 시각화 (headless) ──────────────────────────────────
usdview factory.usda             # GUI 뷰어 실행
usdrecord factory.usda out.png   # 정지 이미지 렌더

# ── 정보 출력 ─────────────────────────────────────────────
usddumpcrate factory.usdc        # usdc 내부 구조 덤프

의존성 분석 — UsdUtils.ComputeAllDependencies
프로젝트가 여러 파일로 나뉘어 있을 때 전체 의존 파일 목록을 파악하는 것이 중요합니다.
pythonfrom pxr import UsdUtils, Ar

# 루트 파일에서 모든 의존 파일 재귀 수집
layers, assets, unresolved = \
    UsdUtils.ComputeAllDependencies("factory_composed.usda")

print("=== Layers (USD 파일) ===")
for l in layers:
    print(f"  {l}")

print("=== Assets (텍스처, HDR 등) ===")
for a in assets:
    print(f"  {a}")

if unresolved:
    print("=== Unresolved (경로 오류) ===")
    for u in unresolved:
        print(f"  !! {u}")

프로젝트 파일 구조 — Phase 4 기준
현재까지 만든 파일들을 포맷 전략에 맞게 정리합니다.
robot_factory/
├── factory_base.usda       ← 개발 원본 (Git 관리)
├── factory_base.usdc       ← 프로덕션 변환본
├── factory_anim.usda       ← 애니메이션 레이어 (개발)
├── factory_anim.usdc       ← 애니메이션 레이어 (프로덕션)
├── textures/
│   └── factory_hdr.hdr     ← DomeLight HDR
└── factory.usdz            ← 배포용 패키지

지금까지 프로젝트 상태
factory_base.usda   (개발 원본 — 전 모듈 누적)
factory_base.usdc   ← ★ 프로덕션 변환 추가
factory_anim.usdc   ← ★ 애니메이션 레이어 변환 추가
factory.usdz        ← ★ 배포 패키지 생성
포맷 체계가 갖춰졌습니다. 다음 모듈 ⑫ Modules에서는 USD가 제공하는 스키마 라이브러리 전체를 조망합니다. 지금까지 써온 UsdGeom, UsdShade, UsdLux가 모두 Module 시스템의 일부이며, UsdPhysics, UsdSkel, UsdRender 등 로봇 시뮬레이션에 직결되는 모듈들을 프로젝트에 연결합니다.

## Phase 4 — Module ⑫ : Modules (USD Schema Libraries)

**"UsdGeom부터 UsdPhysics까지 — USD의 부품 창고"**

USD Schema 모듈 상세

모듈 시스템의 구조
USD의 모든 Schema는 두 종류로 나뉩니다.
IsA Schema (타입 스키마)
  → Prim의 타입 자체를 정의
  → def Xform / def Mesh / def SphereLight
  → prim.IsA(UsdGeom.Xform) 로 타입 체크

API Schema (믹스인 스키마)
  → 기존 Prim에 기능을 추가
  → 타입을 바꾸지 않고 Attribute·Relationship을 추가
  → UsdShade.MaterialBindingAPI(prim).Bind(mat)
  → 여러 API Schema를 동시에 적용 가능

UsdGeom — 지오메트리 스키마
지금까지 가장 많이 써온 모듈입니다. 프로젝트에 이미 적용된 것들을 정리합니다.
pythonfrom pxr import UsdGeom

# ── Typed Schema (IsA) ────────────────────────────────────
UsdGeom.Xform       # 트랜스폼 그룹
UsdGeom.Scope       # 논리 컨테이너
UsdGeom.Mesh        # 폴리곤 메시
UsdGeom.Sphere      # 구체 (implicit)
UsdGeom.Cylinder    # 원기둥
UsdGeom.Cone        # 원뿔
UsdGeom.Cube        # 정육면체
UsdGeom.Camera      # 카메라

# ── API Schema ────────────────────────────────────────────
UsdGeom.XformCommonAPI   # TRS 단순화 API
UsdGeom.PrimvarsAPI      # Primvar 읽기/쓰기
UsdGeom.VisibilityAPI    # visibility 제어
UsdGeom.ModelAPI         # kind / Model 계층

# ── Stage 레벨 유틸 ───────────────────────────────────────
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
UsdGeom.SetStageMetersPerUnit(stage, 0.01)
UsdGeom.GetStageUpAxis(stage)        # "Y"
UsdGeom.GetStageMetersPerUnit(stage) # 0.01

UsdShade — 머티리얼·셰이더 스키마
pythonfrom pxr import UsdShade, Sdf, Gf

# Material 정의
mat = UsdShade.Material.Define(stage, "/Factory/Materials/Metal")

# Shader 정의 — UsdPreviewSurface (범용 PBR)
shader = UsdShade.Shader.Define(
    stage, "/Factory/Materials/Metal/PBRShader"
)
shader.CreateIdAttr("UsdPreviewSurface")

# Shader 입력 설정
shader.CreateInput("diffuseColor",
    Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(0.2, 0.2, 0.25))
shader.CreateInput("metallic",
    Sdf.ValueTypeNames.Float).Set(0.9)
shader.CreateInput("roughness",
    Sdf.ValueTypeNames.Float).Set(0.2)
shader.CreateInput("opacity",
    Sdf.ValueTypeNames.Float).Set(1.0)

# Shader 출력 → Material 표면 연결
surface_out = shader.CreateOutput(
    "surface", Sdf.ValueTypeNames.Token
)
mat.CreateSurfaceOutput().ConnectToSource(surface_out)

# 텍스처 연결 — UsdUVTexture
tex = UsdShade.Shader.Define(
    stage, "/Factory/Materials/Metal/DiffuseTex"
)
tex.CreateIdAttr("UsdUVTexture")
tex.CreateInput("file",
    Sdf.ValueTypeNames.Asset).Set("./textures/metal_diffuse.png")
tex.CreateInput("wrapS",
    Sdf.ValueTypeNames.Token).Set("repeat")
tex.CreateInput("wrapT",
    Sdf.ValueTypeNames.Token).Set("repeat")

# 텍스처 출력 → Shader 입력 연결
rgb_out = tex.CreateOutput("rgb", Sdf.ValueTypeNames.Float3)
shader.GetInput("diffuseColor").ConnectToSource(rgb_out)

# 바인딩
robot_prim = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
UsdShade.MaterialBindingAPI(robot_prim).Bind(mat)

UsdPhysics — 로봇 관절에 물리 구속 추가 ★
로봇 시뮬레이션에서 핵심입니다. 각 관절에 RevoluteJoint를 추가하면 Isaac Sim / MuJoCo / PhysX 에서 물리 기반 제어가 가능해집니다.
.usda 텍스트 방식
usda# Stage 레벨에 Physics Scene 추가
def PhysicsScene "PhysicsScene"
{
    vector3f physics:gravityDirection = (0, -1, 0)
    float    physics:gravityMagnitude = 981.0
}

def Xform "Robot_01"
{
    # RigidBodyAPI — 강체 물리 속성 적용
    bool physics:rigidBodyEnabled = true
    bool physics:kinematicEnabled = true  # 키네마틱 (외부 제어)

    def Xform "Shoulder"
    {
        bool physics:rigidBodyEnabled = true

        # RevoluteJoint — Z축 회전 관절 구속
        def PhysicsRevoluteJoint "ShoulderJoint"
        {
            # 연결 대상
            rel physics:body0 = </Factory/Line_A/Robots/Robot_01>
            rel physics:body1 = </Factory/Line_A/Robots/Robot_01/Shoulder>

            # 회전 축
            uniform token physics:axis = "Z"

            # 관절 한계 (도 단위)
            bool  physics:lowerLimitEnabled = true
            bool  physics:upperLimitEnabled = true
            float physics:lowerLimit = -90.0
            float physics:upperLimit =  90.0
        }
    }
}
Python API 방식
pythonfrom pxr import UsdPhysics, Gf

# ── Physics Scene 추가 ────────────────────────────────────
physics_scene = UsdPhysics.Scene.Define(
    stage, "/Factory/PhysicsScene"
)
physics_scene.CreateGravityDirectionAttr(Gf.Vec3f(0, -1, 0))
physics_scene.CreateGravityMagnitudeAttr(981.0)

# ── RigidBodyAPI — Robot_01 Base에 적용 ──────────────────
robot_prim = stage.GetPrimAtPath(
    "/Factory/Line_A/Robots/Robot_01"
)
rigid_api = UsdPhysics.RigidBodyAPI.Apply(robot_prim)
rigid_api.CreateRigidBodyEnabledAttr(True)
rigid_api.CreateKinematicEnabledAttr(True)

# ── CollisionAPI — 충돌 형상 추가 ────────────────────────
shoulder_prim = stage.GetPrimAtPath(
    "/Factory/Line_A/Robots/Robot_01/Shoulder"
)
UsdPhysics.RigidBodyAPI.Apply(shoulder_prim)
col_api = UsdPhysics.CollisionAPI.Apply(shoulder_prim)
col_api.CreateCollisionEnabledAttr(True)

# ── RevoluteJoint — Shoulder 관절 ────────────────────────
shoulder_joint = UsdPhysics.RevoluteJoint.Define(
    stage,
    "/Factory/Line_A/Robots/Robot_01/Shoulder/ShoulderJoint"
)

# 연결 Body 설정
shoulder_joint.CreateBody0Rel().AddTarget(
    "/Factory/Line_A/Robots/Robot_01"
)
shoulder_joint.CreateBody1Rel().AddTarget(
    "/Factory/Line_A/Robots/Robot_01/Shoulder"
)

# 회전 축 및 한계
shoulder_joint.CreateAxisAttr(UsdPhysics.Tokens.z)
shoulder_joint.CreateLowerLimitAttr(-90.0)
shoulder_joint.CreateUpperLimitAttr(90.0)

# Elbow, Wrist도 동일 패턴
for joint_path, body0, body1, lo, hi in [
    (
        "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow/ElbowJoint",
        "/Factory/Line_A/Robots/Robot_01/Shoulder",
        "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow",
        -120.0, 120.0
    ),
    (
        "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow/Wrist/WristJoint",
        "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow",
        "/Factory/Line_A/Robots/Robot_01/Shoulder/Elbow/Wrist",
        -60.0, 60.0
    ),
]:
    j = UsdPhysics.RevoluteJoint.Define(stage, joint_path)
    j.CreateBody0Rel().AddTarget(body0)
    j.CreateBody1Rel().AddTarget(body1)
    j.CreateAxisAttr(UsdPhysics.Tokens.z)
    j.CreateLowerLimitAttr(lo)
    j.CreateUpperLimitAttr(hi)

stage.Save()

UsdRender — 렌더 설정 추가
pythonfrom pxr import UsdRender, UsdGeom

# ── Camera 추가 ───────────────────────────────────────────
cam_prim = UsdGeom.Camera.Define(
    stage, "/Factory/Cameras/MainCamera"
)
cam_prim.CreateFocalLengthAttr(35.0)
cam_prim.CreateFocusDistanceAttr(500.0)
cam_prim.CreateFStopAttr(5.6)

cam_xf = UsdGeom.Xformable(cam_prim.GetPrim())
cam_xf.AddTranslateOp().Set(Gf.Vec3d(0, 300, -800))
cam_xf.AddRotateXOp().Set(-20.0)

# ── RenderSettings ────────────────────────────────────────
render_settings = UsdRender.Settings.Define(
    stage, "/Render/Settings"
)
render_settings.CreateResolutionAttr(Gf.Vec2i(1920, 1080))
render_settings.CreatePixelAspectRatioAttr(1.0)

# 카메라 연결
render_settings.CreateCameraRel().AddTarget(
    "/Factory/Cameras/MainCamera"
)

# RenderProduct — 출력 이미지 정의
product = UsdRender.Product.Define(
    stage, "/Render/Product"
)
product.CreateProductNameAttr("./renders/factory_beauty.exr")

stage.Save()

API Schema 적용 패턴 — Apply() 메서드
API Schema는 Apply() 클래스 메서드로 기존 Prim에 붙입니다.
pythonfrom pxr import UsdPhysics, UsdShade, UsdGeom

prim = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")

# API Schema 적용
rigid   = UsdPhysics.RigidBodyAPI.Apply(prim)
col     = UsdPhysics.CollisionAPI.Apply(prim)
binding = UsdShade.MaterialBindingAPI.Apply(prim)

# 적용된 API Schema 목록 확인
for api in prim.GetAppliedSchemas():
    print(api)
# PhysicsRigidBodyAPI
# PhysicsCollisionAPI
# MaterialBindingAPI

# API Schema 적용 여부 확인
print(UsdPhysics.RigidBodyAPI.CanApply(prim))  # True
print(prim.HasAPI(UsdPhysics.RigidBodyAPI))    # True

**지금까지 프로젝트 상태**
```
factory_base.usda
└── /Factory
    ├── /Factory/PhysicsScene          ★ UsdPhysics 추가
    │     gravityDirection=(0,-1,0)
    │     gravityMagnitude=981
    ├── /Factory/Cameras               ★ UsdGeom.Camera 추가
    │   └── MainCamera
    ├── /Factory/Materials             (UsdShade — 텍스처 연결 강화)
    ├── /Factory/Lights                (UsdLux — 기존 유지)
    ├── /Factory/Line_A
    │   └── Robots
    │       └── Robot_01
    │           physics:rigidBodyEnabled = true  ★
    │           └── Shoulder
    │               └── ShoulderJoint  (RevoluteJoint, Z, -90~90) ★
    │               └── Elbow
    │                   └── ElbowJoint (RevoluteJoint, Z,-120~120) ★
    │                   └── Wrist
    │                       └── WristJoint (RevoluteJoint, Z,-60~60) ★
    └── /Factory/Floor
/Render/Settings                       ★ UsdRender 추가
    resolution=1920×1080
    camera → MainCamera
```
Phase 4 완전 완료입니다. UsdGeom · UsdShade · UsdLux · UsdPhysics · UsdRender — 로봇 공장 씬에 필요한 모든 Schema 모듈이 적용되었습니다.

Phase 5로 진입합니다
지금까지 만든 모든 것이 단일 파일 안에 있었습니다. Phase 5에서는 이 씬을 여러 레이어로 분리하고, 컴포지션 시스템으로 다시 조립합니다. 다음 모듈 ⑬ Composition에서는 SubLayer · Reference · Payload · Inherit · Variant · Specialize — LIVRPS 여섯 가지 컴포지션 아크의 전체 그림을 먼저 조망합니다.

계속 진행할까요? 다음 → ⑬ Composition입력 내용: OKOK22:32Claude 응답: Phase 5 — Module ⑬ : CompositionPhase 5 — Module ⑬ : Composition
"씬을 레고처럼 조립하다 — 6가지 컴포지션 아크"

---

<img src="usd-buildup\USD-015.png">

컴포지션 아크 상세 — 개념과 코드

LIVRPS란
USD 컴포지션의 핵심 규칙입니다. 여러 아크가 같은 Prim의 같은 Attribute에 오피니언(의견)을 가질 때 어느 것이 이기는가를 결정하는 우선순위 체계입니다.
L  Local         — 현재 레이어의 직접 선언       (가장 강함)
I  Inherit       — class Prim 상속
V  Variant       — VariantSet 선택
R  Reference     — 외부 파일 참조
P  Payload       — 지연 로딩 참조
S  SubLayer      — 레이어 스택                   (가장 약함)
같은 레이어 안에서는 L이 항상 이깁니다. 즉, over로 선언한 로컬 오피니언이 Reference에서 가져온 값을 덮어씁니다. 이것이 비파괴 오버라이드의 핵심 원리입니다.

① SubLayer — 레이어 스택 쌓기
SubLayer는 여러 .usda 파일을 같은 씬의 다른 관점으로 쌓는 방법입니다. 영화 편집의 트랙 개념과 동일합니다.
factory_composed.usda        ← Root Layer (마스터)
  subLayers:
    factory_lighting.usda    ← 조명 담당자 작업
    factory_anim.usda        ← 애니메이터 작업
    factory_base.usda        ← 모델링 담당자 작업 (가장 약함)
위에 있을수록 강합니다. factory_lighting.usda가 factory_base.usda의 값을 덮어씁니다.
.usda 텍스트 방식
usda# factory_composed.usda — 마스터 컴포지션 파일
#usda 1.0
(
    doc            = "Robot Factory — Composed Master"
    defaultPrim    = "Factory"
    upAxis         = "Y"
    metersPerUnit  = 0.01

    subLayers = [
        @factory_lighting.usda@,   # 조명 레이어 (강)
        @factory_anim.usda@,       # 애니메이션 레이어
        @factory_base.usda@        # 베이스 레이어 (약)
    ]
)
# 이 파일 자체에는 Prim이 없어도 됨
# 세 레이어가 합성되어 /Factory 트리가 완성됨
Python API 방식
pythonfrom pxr import Usd, Sdf

# 마스터 Stage 생성
stage = Usd.Stage.CreateNew("factory_composed.usda")
root  = stage.GetRootLayer()

# SubLayer 추가 — 인덱스 0이 가장 강함
root.subLayerPaths.append("factory_lighting.usda")
root.subLayerPaths.append("factory_anim.usda")
root.subLayerPaths.append("factory_base.usda")

# SubLayer 시간 오프셋 (Module ⑨에서 소개한 기능)
root.subLayerOffsets[1] = Sdf.LayerOffset(offset=0, scale=1.0)

stage.Save()

# 합성 결과 확인
for prim in stage.Traverse():
    print(prim.GetPath())

② Reference — 에셋 재사용의 핵심
Reference는 외부 파일의 Prim을 현재 씬의 특정 경로에 배치합니다. 같은 robot_arm.usda를 Robot_01과 Robot_02 두 곳에 배치하면 파일을 복사하지 않고도 두 개의 로봇이 생깁니다.
robot_arm.usda          ← 로봇 팔 에셋 정의
factory_base.usda
  /Factory/Robots/Robot_01  references → robot_arm.usda </RobotArm>
  /Factory/Robots/Robot_02  references → robot_arm.usda </RobotArm>
.usda 텍스트 방식
usda# robot_arm.usda — 재사용 가능한 로봇 팔 에셋
#usda 1.0
(
    defaultPrim = "RobotArm"
)
def Xform "RobotArm"
(
    doc  = "재사용 로봇 팔 에셋"
    kind = "component"
)
{
    custom string custom:model = "ARM-7X"

    def Xform "Shoulder"
    {
        double3 xformOp:translate    = (0, 80, 0)
        double  xformOp:rotateZ      = 0.0
        uniform token[] xformOpOrder = [
            "xformOp:translate", "xformOp:rotateZ"
        ]
        def Xform "Elbow"
        {
            double3 xformOp:translate    = (0, 120, 0)
            double  xformOp:rotateZ      = 0.0
            uniform token[] xformOpOrder = [
                "xformOp:translate", "xformOp:rotateZ"
            ]
            def Xform "Wrist"
            {
                double3 xformOp:translate    = (0, 80, 0)
                double  xformOp:rotateZ      = 0.0
                uniform token[] xformOpOrder = [
                    "xformOp:translate", "xformOp:rotateZ"
                ]
            }
        }
    }
}
usda# factory_base.usda — Reference로 로봇 배치
def Scope "Robots"
{
    # Robot_01 — robot_arm.usda의 defaultPrim을 참조
    def Xform "Robot_01"
    (
        references = @./robot_arm.usda@
    )
    {
        # Reference 위에 로컬 오버라이드 (L이 R보다 강함)
        double3 xformOp:translate    = (100, 0, 200)
        uniform token[] xformOpOrder = ["xformOp:translate"]
        custom int custom:serialNumber = 1001
    }

    # Robot_02 — 동일 에셋, 다른 위치
    def Xform "Robot_02"
    (
        references = @./robot_arm.usda@
    )
    {
        double3 xformOp:translate    = (300, 0, 200)
        uniform token[] xformOpOrder = ["xformOp:translate"]
        custom int custom:serialNumber = 1002
    }
}
Python API 방식
pythonfrom pxr import Usd, Sdf

stage = Usd.Stage.Open("factory_base.usda")

# Reference 추가
robot_01 = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
robot_01.GetReferences().AddReference("./robot_arm.usda")

# 특정 Prim 경로를 지정해서 참조
robot_02 = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_02")
robot_02.GetReferences().AddReference(
    assetPath = "./robot_arm.usda",
    primPath  = Sdf.Path("/RobotArm")   # defaultPrim 대신 명시
)

# Reference 목록 확인
edit = robot_01.GetPrimStack()
for spec in edit:
    print(spec.referenceList)

stage.Save()

③ Payload — 지연 로딩
Payload는 Reference와 문법이 거의 동일하지만 로딩 시점이 다릅니다. Stage를 열 때 Payload는 기본적으로 로드되지 않습니다. 명시적으로 Load해야 합니다.
usdadef Xform "Robot_01"
(
    # 고해상도 메시는 Payload로 — 필요할 때만 로드
    payload = @./robot_arm_detail.usda@
)
{
    # Payload 밖의 데이터는 항상 로드됨 (bbox 등 경량 데이터)
    float3 extent = [(-50,-10,-50), (50, 330, 50)]
    custom string custom:model = "ARM-7X"
}
pythonfrom pxr import Usd

# ── Payload 로딩 전략 선택 ────────────────────────────────

# 1. 전체 Payload 로드 (기본)
stage = Usd.Stage.Open(
    "factory_composed.usda",
    load=Usd.Stage.LoadAll       # 모든 Payload 즉시 로드
)

# 2. Payload 없이 열기 (경량 탐색용)
stage = Usd.Stage.Open(
    "factory_composed.usda",
    load=Usd.Stage.LoadNone      # Payload 전혀 로드 안 함
)

# 3. 특정 Prim만 선택 로드
stage.Load("/Factory/Line_A/Robots/Robot_01")   # 이 Prim만 로드
stage.Unload("/Factory/Line_A/Robots/Robot_02") # 이 Prim 언로드

# 로드 상태 확인
prim = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
print(prim.IsLoaded())   # True / False

# 현재 로드된 Prim 목록
for path in stage.GetLoadSet():
    print(path)

④ Inherit — class Prim으로 공통 속성 관리
Inherit은 class Prim의 속성을 여러 Prim이 공유하는 메커니즘입니다. Reference와 다른 핵심 특징은 런타임에 class를 수정하면 모든 상속 Prim에 즉시 반영된다는 점입니다.
usda#usda 1.0

# class Prim — 렌더링 안 됨, 데이터 공유 전용
class Xform "_RobotBase"
{
    # 모든 로봇이 공유할 기본 속성
    color3f[] primvars:displayColor = [(0.15, 0.15, 0.6)]
    (
        interpolation = "constant"
    )
    float primvars:robotGloss = 0.85
    custom string custom:manufacturer = "FactoryBot Inc."
    custom int    custom:revision     = 3
}

def Xform "Robot_01"
(
    inherits = </_RobotBase>   # class 상속
)
{
    # _RobotBase의 속성을 모두 물려받음
    # 로컬에서 오버라이드 가능 (L > I)
    double3 xformOp:translate    = (100, 0, 200)
    uniform token[] xformOpOrder = ["xformOp:translate"]
    custom int custom:serialNumber = 1001
    # displayColor는 _RobotBase에서 상속 — 여기서 재선언 불필요
}

def Xform "Robot_02"
(
    inherits = </_RobotBase>
)
{
    double3 xformOp:translate    = (300, 0, 200)
    uniform token[] xformOpOrder = ["xformOp:translate"]
    custom int custom:serialNumber = 1002
}
pythonfrom pxr import Usd, UsdGeom, Sdf, Gf, Vt

stage = Usd.Stage.Open("factory_base.usda")

# class Prim 생성
base_class = stage.CreateClassPrim("/_RobotBase")

# class에 공통 속성 설정
pvAPI = UsdGeom.PrimvarsAPI(base_class)
dc = pvAPI.CreatePrimvar(
    "displayColor",
    Sdf.ValueTypeNames.Color3fArray,
    UsdGeom.Tokens.constant
)
dc.Set(Vt.Vec3fArray([Gf.Vec3f(0.15, 0.15, 0.6)]))

base_class.CreateAttribute(
    "custom:manufacturer",
    Sdf.ValueTypeNames.String, custom=True
).Set("FactoryBot Inc.")

# Inherit 추가
robot_01 = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
robot_01.GetInherits().AddInherit(Sdf.Path("/_RobotBase"))

robot_02 = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_02")
robot_02.GetInherits().AddInherit(Sdf.Path("/_RobotBase"))

# 런타임 일괄 변경 — class 수정 → 모든 Robot에 즉시 반영
base_class.GetAttribute("custom:manufacturer").Set("FactoryBot v2")
# Robot_01, Robot_02 모두 즉시 "FactoryBot v2"로 변경됨

stage.Save()

⑤ Variant — 스위처블 옵션
Variant는 하나의 Prim이 여러 가지 버전 중 하나를 선택적으로 표시하는 메커니즘입니다. LOD 전환, 색상 옵션, 모델 타입 전환에 씁니다.
usdadef Xform "Robot_01"
(
    # VariantSet 선언과 현재 선택값
    variants = {
        string modelType = "ARM-7X"
        string lodLevel  = "high"
    }
    variantSets = ["modelType", "lodLevel"]
)
{
    double3 xformOp:translate    = (100, 0, 200)
    uniform token[] xformOpOrder = ["xformOp:translate"]

    variantSet "modelType" = {
        "ARM-7X" {
            custom string custom:model    = "ARM-7X"
            custom float  custom:payload  = 7.5
            # ARM-7X 전용 지오메트리 Reference 등
        }
        "ARM-9X" {
            custom string custom:model    = "ARM-9X"
            custom float  custom:payload  = 9.2
        }
    }

    variantSet "lodLevel" = {
        "high" {
            payload = @./robot_arm_high.usda@
        }
        "low" {
            payload = @./robot_arm_low.usda@
        }
    }
}
pythonfrom pxr import Usd

stage = Usd.Stage.Open("factory_base.usda")
prim  = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")

# VariantSet 생성
model_vs = prim.GetVariantSets().AddVariantSet("modelType")
lod_vs   = prim.GetVariantSets().AddVariantSet("lodLevel")

# Variant 추가 및 내용 편집
for variant_name, model, payload_val in [
    ("ARM-7X", "ARM-7X", 7.5),
    ("ARM-9X", "ARM-9X", 9.2),
]:
    model_vs.AddVariant(variant_name)
    model_vs.SetVariantSelection(variant_name)

    # with 블록 안에서 편집 → 해당 Variant 안에 기록됨
    with model_vs.GetVariantEditContext():
        prim.CreateAttribute(
            "custom:model",
            Sdf.ValueTypeNames.String, custom=True
        ).Set(model)
        prim.CreateAttribute(
            "custom:payloadKg",
            Sdf.ValueTypeNames.Float, custom=True
        ).Set(payload_val)

# LOD Variant
for lod, ref_path in [("high", "./robot_arm_high.usda"),
                       ("low",  "./robot_arm_low.usda")]:
    lod_vs.AddVariant(lod)
    lod_vs.SetVariantSelection(lod)
    with lod_vs.GetVariantEditContext():
        prim.GetPayloads().AddPayload(ref_path)

# 현재 선택 설정
model_vs.SetVariantSelection("ARM-7X")
lod_vs.SetVariantSelection("high")

# 선택 조회
print(model_vs.GetVariantSelection())  # "ARM-7X"
print(lod_vs.GetVariantSelection())    # "high"

# 런타임에 전환
model_vs.SetVariantSelection("ARM-9X")  # 즉시 전환

stage.Save()

지금까지 프로젝트 상태
robot_factory/
├── robot_arm.usda              ← 재사용 에셋 (defaultPrim=RobotArm)
├── robot_arm_high.usda         ← LOD high 메시
├── robot_arm_low.usda          ← LOD low 메시
├── factory_base.usda           ← 베이스 레이어
│     /_RobotBase (class)       ← Inherit 공통 속성
│     /Factory/Robots/Robot_01  ← references robot_arm.usda  ★
│                                  inherits /_RobotBase       ★
│                                  variantSet modelType/lod   ★
│     /Factory/Robots/Robot_02  ← 동일 구조
├── factory_anim.usda           ← 애니메이션 레이어
├── factory_lighting.usda       ← 조명 레이어
└── factory_composed.usda       ← 마스터 (SubLayer 스택) ★
      subLayers = [lighting, anim, base]
5가지 컴포지션 아크가 모두 프로젝트에 적용되었습니다. 다음 모듈 ⑭ LIVRPS에서는 이 아크들이 충돌할 때 우선순위가 어떻게 작동하는지, 그리고 over를 사용한 비파괴 오버라이드 패턴을 실전 예제로 깊이 파고듭니다.

계속 진행할까요? 다음 → ⑭ LIVRPS입력 내용: 네네06:40Claude 응답: Phase 5 — Module ⑭ : LIVRPSPhase 5 — Module ⑭ : LIVRPS
"오피니언 충돌 시 누가 이기는가 — 우선순위의 모든 것"

  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widget
오피니언(Opinion)이란
USD에서 오피니언은 "어떤 레이어가 어떤 Attribute에 대해 주장하는 값"입니다. 여러 레이어가 같은 Attribute에 대해 서로 다른 값을 주장할 때 LIVRPS 규칙이 중재합니다.
오피니언 = (레이어, Attribute 경로, 값) 의 3-tuple

예:
  factory_lighting.usda  →  /Factory/Lights/KeyLight.inputs:intensity = 800
  factory_base.usda      →  /Factory/Lights/KeyLight.inputs:intensity = 500

→ SubLayer 스택에서 factory_lighting이 위에 있으므로
  최종값 = 800  (더 강한 오피니언 채택)

같은 레이어 안에서의 LIVRPS
같은 .usda 파일 안에서도 LIVRPS가 작동합니다. 한 Prim에 Local 선언과 Reference가 공존할 때입니다.
usdadef Xform "Robot_01"
(
    # R: Reference — robot_arm.usda 의 모든 값을 가져옴
    references = @./robot_arm.usda@
)
{
    # L: Local 오버라이드 — Reference 값을 덮어씀
    # robot_arm.usda에 translate가 있어도 이 값이 최종
    double3 xformOp:translate    = (100, 0, 200)
    uniform token[] xformOpOrder = ["xformOp:translate"]

    # robot_arm.usda의 custom:model은 여기서 선언 안 했으므로
    # Reference 값인 "ARM-7X" 그대로 유지됨
}
이 패턴이 비파괴 오버라이드의 본질입니다. 원본 파일을 수정하지 않고 참조 위에서 값을 덮어씁니다.

over — 전용 오버라이드 Prim
def는 Prim을 새로 정의합니다. over는 이미 존재하는 Prim을 수정하기 위한 전용 선언입니다. over로 선언된 Prim은 다른 아크가 실제 Prim을 제공하지 않으면 씬에 존재하지 않습니다.
usda# factory_override.usda — 오버라이드 전용 레이어
#usda 1.0
(
    # 이 파일은 subLayer로 factory_base.usda 위에 올라감
)

# over: Prim을 새로 만들지 않고 기존 Prim의 값만 수정
over "Factory"
{
    over "Lights"
    {
        over "KeyLight"
        {
            # 조명 강도만 오버라이드 — 나머지는 base 값 유지
            float inputs:intensity = 1200.0
            color3f inputs:color   = (1.0, 0.8, 0.7)
        }
    }

    over "Line_A"
    {
        over "Robots"
        {
            over "Robot_01"
            {
                # serialNumber만 수정
                custom int custom:serialNumber = 9001
            }
        }
    }
}

SubLayer 스택 안에서의 우선순위
SubLayer 스택은 LIVRPS의 S 레벨에서 작동하지만, 스택 안에서도 위에 있을수록 강합니다.
factory_composed.usda
  subLayers = [
    @factory_override.usda@,   ← 가장 강한 SubLayer
    @factory_lighting.usda@,
    @factory_anim.usda@,
    @factory_base.usda@        ← 가장 약한 SubLayer
  ]

/Factory/Lights/KeyLight.inputs:intensity 의 오피니언:
  factory_override.usda  → 1200.0   ← 채택
  factory_lighting.usda  → 800.0
  factory_base.usda      → 500.0

프로젝트 코드 — LIVRPS 전체 시나리오
실전 시나리오: 같은 robot_arm.usda 에셋을 쓰지만, 촬영 감독 버전과 QA 버전이 서로 다른 오버라이드를 가집니다.
usda# shot_director.usda — 촬영 감독 오버라이드
#usda 1.0
(
    doc = "촬영 감독 버전 — 조명·색상 조정"
    subLayers = [
        @factory_composed.usda@   # 베이스 합성 씬
    ]
)

# L: SubLayer 위에서 로컬 오버라이드
over "Factory"
{
    over "Lights"
    {
        over "KeyLight"
        {
            float inputs:intensity = 1500.0   # L > S (base의 500)
        }
    }

    over "Line_A"
    {
        over "Robots"
        {
            over "Robot_01"
            (
                # Variant 전환 — V 레벨에서 작동
                variants = {
                    string modelType = "ARM-9X"
                }
            )
            {
                # L: 로컬 색상 오버라이드
                color3f[] primvars:displayColor = [(0.8, 0.2, 0.1)]
            }
        }
    }
}
Python으로 오피니언 추적
pythonfrom pxr import Usd, Sdf, UsdGeom

stage = Usd.Stage.Open("shot_director.usda")

attr = stage.GetAttributeAtPath(
    "/Factory/Lights/KeyLight.inputs:intensity"
)

# 최종 합성값
print(attr.Get())   # 1500.0

# 오피니언 스택 전체 조회 — 어느 레이어가 어떤 값을 주장하는가
for spec in attr.GetPropertyStack(Usd.TimeCode.Default()):
    print(f"  {spec.layer.identifier:40s} → {spec.default}")

# 출력:
#   shot_director.usda                       → 1500.0  (L, 채택)
#   factory_override.usda                    → 1200.0
#   factory_lighting.usda                    → 800.0
#   factory_base.usda                        → 500.0

# Prim 스택 — Prim 레벨 오피니언 추적
prim = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
for spec in prim.GetPrimStack():
    print(f"  {spec.layer.identifier:40s}  specifier={spec.specifier}")

# 출력:
#   shot_director.usda    specifier=over
#   factory_base.usda     specifier=def   (실제 Prim 정의)
#   robot_arm.usda        specifier=def   (Reference 원본)

레이어 오프셋과 LIVRPS 상호작용
SubLayer에 offset/scale을 주면 시간 축에서도 우선순위가 유지됩니다.
pythonfrom pxr import Sdf

root = stage.GetRootLayer()

# SubLayer 인덱스 0(가장 강한)에 오프셋 적용
root.subLayerOffsets[0] = Sdf.LayerOffset(offset=24.0, scale=1.0)

# → 이 레이어의 TimeSample f1 = 마스터 타임라인 f25
# → LIVRPS 강도는 그대로 유지 (시간만 이동)

자주 하는 실수 — def vs over
usda# 잘못된 패턴 — over 대신 def를 오버라이드로 쓰는 경우
# (SubLayer 위에서)
def Xform "Robot_01"      # ← def를 쓰면 Reference가 무시됨!
{
    float inputs:intensity = 1500.0
}

# 올바른 패턴
over "Robot_01"            # ← over: 기존 Prim 위에 값만 덮어씀
{
    float inputs:intensity = 1500.0
}
def를 오버라이드 목적으로 쓰면 해당 레이어에서 Prim이 새로 정의되어 Reference 연결이 끊어질 수 있습니다. 오버라이드는 반드시 over를 써야 합니다.

지금까지 프로젝트 상태
robot_factory/
├── robot_arm.usda              (에셋 — defaultPrim=RobotArm)
├── factory_base.usda           (베이스 레이어)
│     /_RobotBase               (class — Inherit 공통 속성)
│     /Factory/Robots/Robot_01  (references + inherits + variantSet)
├── factory_anim.usda           (애니메이션 레이어)
├── factory_lighting.usda       (조명 레이어)
├── factory_override.usda       (over 오버라이드 레이어) ★ 추가
├── factory_composed.usda       (SubLayer 마스터)
└── shot_director.usda          (촬영 감독 버전) ★ 추가
      subLayers = [factory_composed]
      over KeyLight intensity=1500
      over Robot_01 variant=ARM-9X, color override
LIVRPS 우선순위 체계가 완성되었습니다. 다음 모듈 ⑮ Key Composition Concepts에서는 지금까지 배운 모든 것을 종합합니다. PrimStack · PropertyStack · 합성 엔진 내부 동작 · 실전 파이프라인 패턴을 정리하고 전체 프로젝트를 최종 완성합니다.

계속 진행할까요? 다음 → ⑮ Key Composition Concepts (최종)입력 내용: 넵넵06:41Claude 응답: Phase 5 — Module ⑮ : Key Composition ConceptsPhase 5 — Module ⑮ : Key Composition Concepts
"합성 엔진의 내부 — 모든 것을 하나로"

  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation-duration: 0.25s;
    animation-timing-function: cubic-bezier(0.19, 1, 0.22, 1);
  }
VvisualizeVvisualize show_widget
합성 엔진이 하는 일
Stage를 열면 USD 합성 엔진은 다음 5단계를 수행합니다.
1. Layer Stack 구성
   → Root Layer + SubLayer를 순서대로 수집

2. Composition Index 구축
   → 각 Prim 경로에 대해 어떤 아크(R/P/I/V)가 있는지 인덱싱
   → 재귀적으로 Reference → 그 Reference의 SubLayer까지 탐색

3. PrimStack 생성
   → 각 Prim의 SdfPrimSpec 목록을 LIVRPS 순서로 정렬

4. Value Resolution
   → 실제 값을 요청받을 때 PrimStack을 순회
   → 가장 강한 오피니언을 찾으면 즉시 반환 (lazy evaluation)

5. Composed Prim Tree 제공
   → 애플리케이션에 최종 합성된 Prim Tree를 노출
중요한 점은 4단계가 lazy하다는 것입니다. attr.Get()을 호출하기 전까지 값을 실제로 계산하지 않습니다. 이것이 수백만 개의 Prim을 가진 씬을 빠르게 열 수 있는 이유입니다.

NameChildren 합산 — 자식 Prim은 합집합
LIVRPS는 Attribute 값에 적용되지만, 자식 Prim 목록은 모든 아크의 합집합입니다.
robot_arm.usda:
  /RobotArm/Shoulder/Elbow/Wrist

factory_base.usda (Reference 후 로컬 추가):
  /Factory/Robots/Robot_01  references → robot_arm.usda
  /Factory/Robots/Robot_01/DebugMarker  ← 로컬에서 추가

최종 자식 목록:
  Shoulder  (robot_arm.usda에서)
  DebugMarker (factory_base.usda 로컬에서)
  → 합집합 = [Shoulder, DebugMarker]

Instancing — 메모리 공유
같은 Reference를 수백 개 배치할 때 Instancing으로 메모리를 공유합니다.
usda# 100개의 로봇을 배치하되 메모리는 하나만 사용
def Xform "Robot_01" (references = @robot_arm.usda@ instanceable = true) {}
def Xform "Robot_02" (references = @robot_arm.usda@ instanceable = true) {}
# ... 100개
pythonfrom pxr import Usd

# instanceable 설정
prim = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
prim.SetInstanceable(True)

# 인스턴스 여부 확인
print(prim.IsInstanceable())   # True
print(prim.IsInstance())       # True (합성 후 실제 인스턴스)
print(prim.IsPrototype())      # False

# 프로토타입(공유 데이터) 접근
proto = prim.GetPrototype()
if proto:
    print(proto.GetPath())     # /__Prototype_1

# 같은 프로토타입을 쓰는 모든 인스턴스 수집
for inst in proto.GetInstances():
    print(inst.GetPath())

Asset Resolution — @경로@ 해석
Reference·Payload·Texture의 @path@는 실제 파일 경로가 아닙니다. ArResolver가 이 경로를 실제 디스크 경로로 변환합니다.
pythonfrom pxr import Ar

# 기본 Resolver — 상대 경로를 절대 경로로 변환
resolver = Ar.GetResolver()

# 경로 해석
resolved = resolver.Resolve("./robot_arm.usda")
print(resolved)   # /home/나무/robot_factory/robot_arm.usda

# 커스텀 Resolver — 스튜디오 에셋 DB 연동
# (플러그인으로 등록, 경로 형식 완전 커스텀 가능)
# 예: "asset:robot_arm_v003" → /pipeline/assets/robot/v003/robot_arm.usdc

**프로젝트 최종 완성 코드**
   * 지금까지 만든 모든 요소를 하나로 조립합니다.

```python
from pxr import (
    Usd, UsdGeom, UsdShade, UsdLux,
    UsdPhysics, UsdRender, UsdUtils,
    Sdf, Gf, Vt, Kind
)

# ══════════════════════════════════════════════════════════
# 1. 레이어 분리 구조 확인
# ══════════════════════════════════════════════════════════
# factory_base.usda      — Prim 구조 + Material + Physics
# factory_anim.usda      — TimeSamples 애니메이션
# factory_lighting.usda  — 조명
# factory_override.usda  — over 오버라이드
# factory_composed.usda  — SubLayer 마스터
# shot_director.usda     — 최종 샷 오버라이드

# ══════════════════════════════════════════════════════════
# 2. 마스터 Stage 열기 및 전체 합성 확인
# ══════════════════════════════════════════════════════════
stage = Usd.Stage.Open("shot_director.usda")

print("=== Layer Stack ===")
for layer in stage.GetLayerStack():
    print(f"  {layer.identifier}")

print("\n=== Composed Prim Tree ===")
for prim in stage.Traverse():
    depth  = len(prim.GetPath().pathComponents) - 1
    indent = "  " * depth
    kind   = Usd.ModelAPI(prim).GetKind()
    print(f"{indent}{prim.GetName():30s} [{prim.GetTypeName()}]"
          f"  kind={kind}")

# ══════════════════════════════════════════════════════════
# 3. 오피니언 추적 유틸
# ══════════════════════════════════════════════════════════
def trace_opinions(stage, attr_path):
    """특정 Attribute의 모든 오피니언을 LIVRPS 순으로 출력."""
    attr = stage.GetAttributeAtPath(attr_path)
    if not attr:
        print(f"  Attribute not found: {attr_path}")
        return
    print(f"\n=== Opinions for {attr_path} ===")
    print(f"  Final value: {attr.Get()}")
    for spec in attr.GetPropertyStack(Usd.TimeCode.Default()):
        marker = "✓ ADOPTED" if spec == \
            attr.GetPropertyStack(Usd.TimeCode.Default())[0] \
            else "  skipped"
        print(f"  {marker}  {spec.layer.identifier:40s}"
              f" → {spec.default}")

trace_opinions(stage,
    "/Factory/Lights/KeyLight.inputs:intensity")
trace_opinions(stage,
    "/Factory/Line_A/Robots/Robot_01.xformOp:translate")

# ══════════════════════════════════════════════════════════
# 4. Variant 런타임 전환
# ══════════════════════════════════════════════════════════
robot = stage.GetPrimAtPath("/Factory/Line_A/Robots/Robot_01")
vsets = robot.GetVariantSets()

print("\n=== VariantSets ===")
for name in vsets.GetNames():
    vs  = vsets.GetVariantSet(name)
    sel = vs.GetVariantSelection()
    print(f"  {name}: {vs.GetVariantNames()}  current='{sel}'")

# 전환
vsets.GetVariantSet("modelType").SetVariantSelection("ARM-9X")
vsets.GetVariantSet("lodLevel").SetVariantSelection("low")
print("\nAfter switch:")
print(f"  model = {robot.GetAttribute('custom:model').Get()}")

# ══════════════════════════════════════════════════════════
# 5. 의존성 분석 + usdz 패키징
# ══════════════════════════════════════════════════════════
layers, assets, unresolved = \
    UsdUtils.ComputeAllDependencies("shot_director.usda")

print(f"\n=== Dependencies ===")
print(f"  Layers : {len(layers)}")
print(f"  Assets : {len(assets)}")
print(f"  Broken : {len(unresolved)}")
```

## 전체 커리큘럼 최종 프로젝트 상태


<img src=""usd-buildup\USD-020.png">

**핵심 패턴 3가지 — 실전 요약**
   * 지금까지 배운 15개 모듈을 실전에서 어떻게 조합할지 최종 정리합니다.

**패턴 1 — 에셋 파이프라인**

```
에셋 정의          robot_arm.usda       (def, defaultPrim)
    ↓ Reference
씬 배치            factory_base.usda    (위치·오버라이드)
    ↓ SubLayer
애니메이션 추가    factory_anim.usda    (TimeSamples)
    ↓ SubLayer
조명 추가          factory_lighting.usda
    ↓ SubLayer
샷 오버라이드      shot_director.usda   (over, Variant 전환)
    ↓ Export
배포               robot_factory.usdz
```

**패턴 2 — 비파괴 오버라이드**

```python
# 원본을 건드리지 않고 값 변경
# 항상 over + SubLayer 조합
over_layer = Sdf.Layer.CreateNew("my_override.usda")
with Usd.EditContext(stage, over_layer):
    prim = stage.GetPrimAtPath("/Factory/Lights/KeyLight")
    prim.GetAttribute("inputs:intensity").Set(2000.0)
over_layer.Save()
# factory_base.usda는 변경 없음
```

**패턴 3 — 런타임 씬 조작**

```python
# Variant 전환 → 즉시 씬 변경
robot.GetVariantSets().GetVariantSet("lodLevel")\
     .SetVariantSelection("low")

# Payload 선택적 로드 → 메모리 관리
stage.Unload("/Factory/Line_A/Robots/Robot_02")

# class 수정 → 모든 상속 Prim 일괄 변경
base = stage.GetPrimAtPath("/_RobotBase")
base.GetAttribute("custom:manufacturer").Set("NewFactory Corp")
# Robot_01, Robot_02 모두 즉시 반영
```

**커리큘럼 완료 — 전체 요약**

| Phase | 모듈 | 핵심 개념 | 프로젝트 기여 | 
|:-------:|:-------:|:-------:|:-------:|
| 1 | Stage | 씬 진입점, Layer Stack | factory_base.usda 생성 | 
| 1 | Prims | SdfPath, Specifier, Kind | /Factory 트리 구성 | 
| 1 | Attributes | 타입 시스템, Default Value | 위치·재질·커스텀 데이터 | 
| 1 | Relationships | SdfPath 포인터 | material:binding, light:link | 
| 1 | Metadata | doc, kind, customData | 씬 문서화, 계층 분류 | 
| 2 | Scope | 논리 컨테이너 | Materials/Lights/Robots 분류 | 
| 2 | Xform | xformOp 스택 | 관절 계층 구조 | 
| 2 | Primvars | interpolation, 상속 | 버텍스 컬러, UV | 
| 3 | TimeSamples | TimeCode, 키프레임 | 로봇 팔 애니메이션 | 
| 4 | Lighting | UsdLux, Light Linking | 3종 조명 체계 | 
| 4 | File Format | susda/usdc/usdz | 개발→프로덕션→배포 | 
| 4 | Modules | IsA/API Schema | Physics, Render 추가 | 
| 5 | Composition | 6 아크 | 레이어 분리 조립 | 
| 5 | LIVRPS | 우선순위 해석 | 비파괴 오버라이드 |  
| 5 | Key Concepts | 합성 엔진, Instancing | 최종 패키징 | 


🎉 전체 커리큘럼 완료입니다.
15개 모듈, 5개 Phase, 하나의 Robot Factory Scene — Stage에서 시작해 Composition 마스터리까지 USD의 전체 개념 체계를 단일 프로젝트로 완성했습니다. 특정 모듈을 더 깊이 파고들거나, 실제 Omniverse / Houdini 환경에서의 적용 방법이 필요하시면 말씀해 주세요.

