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

## Phase 1 — Module ③ : Attributes
**"Prim에 데이터를 부여하는 것"**

<img src="usd-buildup\USD-004.png">

Attribute란 무엇인가
Attribute는 Prim이 갖는 이름 붙은 데이터 값입니다. 위치, 색상, 반지름, 가시성 등 Prim에 관한 모든 구체적인 수치나 상태가 Attribute로 표현됩니다.
Prim이 "Robot_01이라는 노드"라면, Attribute는 "그 로봇이 어디에 있고, 어떻게 생겼는지"를 담은 데이터입니다.
Attribute는 세 종류로 나뉩니다.
종류예시설명Schema AttributexformOp:translate, visibility해당 Type의 Schema가 정의한 표준 속성API Attributeprimvars:displayColorAPI Schema가 추가하는 속성Custom Attributecustom:serialNumber사용자가 직접 정의하는 속성

Value Type — USD의 타입 시스템
USD는 강타입 시스템입니다. Attribute를 만들 때 반드시 타입을 지정해야 하며, 나중에 바꿀 수 없습니다.
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
token과 string의 차이: token은 USD 내부에서 인터닝(interning)되어 비교가 O(1)입니다. "inherited", "invisible", "Y" 같은 고정 열거값에 사용합니다.

프로젝트 코드 — Robot_01에 Attribute 추가
.usda 텍스트 방식
usda#usda 1.0
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
Python API 방식
pythonfrom pxr import Usd, UsdGeom, Sdf, Gf

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

Attribute 읽기 · 검사
pythonprim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

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

uniform vs varying — Attribute의 가변성
Attribute 앞에 붙는 uniform 키워드는 시간에 따라 값이 바뀌지 않음을 선언합니다. xformOpOrder처럼 구조적으로 고정되어야 하는 Attribute에 씁니다.
usda# uniform: 애니메이션 불가, 모든 프레임에서 동일
uniform token[] xformOpOrder = ["xformOp:translate"]

# (기본) varying: 프레임마다 다른 값을 가질 수 있음
double3 xformOp:translate = (100, 0, 200)

지금까지 프로젝트 상태
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
Prim들이 실제 데이터를 갖게 되었습니다. 다음 모듈 ④ Relationships에서는 Prim 간의 연결 — 머티리얼 바인딩, 조명 링크 등 — 을 다룹니다. Attribute가 "값"을 담는다면, Relationship은 "다른 Prim을 가리키는 포인터"입니다.

---
## Phase 1 — Module ④ : Relationships
**"Prim과 Prim을 연결하는 포인터"**

<img src="usd-buildup\USD-005.png">

Relationship란 무엇인가
Relationship은 Prim이 다른 Prim(또는 Attribute)을 SdfPath로 가리키는 포인터입니다. Attribute가 숫자나 문자열 같은 값을 담는다면, Relationship은 씬 그래프 안의 다른 노드를 참조합니다.
핵심 차이를 한 줄로 정리하면:
Attribute   →  값(value)을 저장         ex) translate = (100, 0, 200)
Relationship → 경로(SdfPath)를 저장      ex) material:binding = </Factory/Materials/Metal>
Relationship은 타입이 없습니다. 가리키는 대상이 어떤 Prim인지는 Relationship을 사용하는 Schema가 의미를 부여합니다.

가장 중요한 Relationship — material:binding
USD에서 Relationship이 가장 많이 쓰이는 곳은 머티리얼 바인딩입니다. UsdShade의 material:binding은 Mesh나 Xform이 어떤 Material Prim을 사용할지 가리킵니다.
usdadef Mesh "Robot_01"
{
    # material:binding은 Relationship — 값이 아니라 경로를 저장
    rel material:binding = </Factory/Materials/MetalMaterial>
}
꺾쇠괄호 < > 안의 경로가 Relationship 타겟입니다. Attribute의 값 ( )과 구별되는 .usda 문법입니다.

Relationship의 특징 — 다중 타겟
Relationship은 타겟을 여러 개 가질 수 있습니다. 조명의 light:targetPrim이 대표적인 예입니다.
usdadef SphereLight "KeyLight"
{
    # 단일 타겟
    rel light:targetPrim = </Factory/Robots/Robot_01>

    # 다중 타겟 — 리스트 형태
    rel light:targetPrim = [
        </Factory/Robots/Robot_01>,
        </Factory/Robots/Robot_02>
    ]
}

프로젝트 코드 — Material 바인딩 추가
.usda 텍스트 방식
usda#usda 1.0
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
Python API 방식
pythonfrom pxr import Usd, UsdGeom, UsdShade, UsdLux, Sdf, Gf

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

Relationship 읽기 · 탐색
pythonprim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

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

Attribute vs Relationship 선택 기준
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

지금까지 프로젝트 상태
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
씬의 Prim들이 이제 서로 연결되었습니다. 다음 모듈 ⑤ Metadata에서는 Prim과 Stage 자체에 붙는 "데이터에 대한 데이터" — 문서화, 렌더링 힌트, 에디터 정보 등을 다룹니다. Attribute나 Relationship과 달리 Metadata는 합성(Composition)에 참여하지 않는 순수한 부가 정보입니다.

---

## Phase 1 — Module ⑤ : Metadata
**"데이터에 대한 데이터 — 씬의 맥락을 기록하다"**

<img src="usd-buildup\USD-006.png">

Metadata란 무엇인가
Metadata는 Prim·Attribute·Layer 자체에 붙는 부가 정보입니다. 씬의 콘텐츠(geometry, transform 등)가 아니라 씬을 설명하고 제어하는 데이터입니다.
Attribute와 Metadata의 핵심 차이는 딱 하나입니다.
Attribute  → 합성(Composition) 에 참여한다
             → 값이 레이어 간에 오버라이드·상속된다
Metadata   → 합성에 참여하지 않는다
             → 각 레이어에 독립적으로 기록된다
             → 단, doc / active / kind 등 일부는 합성 결과에 영향을 준다
Metadata가 붙을 수 있는 위치는 세 군데입니다. Stage/Layer 레벨, Prim 레벨, Attribute 레벨입니다.

Stage / Layer 레벨 Metadata
Stage를 열 때 가장 먼저 보게 되는 .usda 파일 상단의 ( ) 블록이 Layer 레벨 Metadata입니다.
usda#usda 1.0
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
defaultPrim은 이 Layer를 Reference할 때 어떤 Prim을 진입점으로 쓸지 알려줍니다. Phase 5 컴포지션에서 결정적인 역할을 합니다.
timeCodesPerSecond와 startTimeCode/endTimeCode는 Module ⑨ TimeSamples에서 다시 씁니다.

Prim 레벨 Metadata
Prim 선언 뒤 괄호 ( ) 블록에 씁니다.
usdadef Xform "Robot_01"
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
( ) 블록(Metadata)과 { } 블록(Attribute/Relationship)은 역할이 완전히 다릅니다. 괄호는 Prim 자체를 설명하고, 중괄호는 Prim의 내용(데이터)을 담습니다.

Kind — 모델 계층 구조
kind는 Prim이 씬 계층에서 어떤 역할을 하는지 나타내는 Metadata입니다. Omniverse, Houdini, USD Resolver 등 많은 도구가 kind를 기반으로 씬을 탐색합니다.
Kind의미우리 프로젝트 적용assembly여러 component를 묶는 최상위 그룹/Factorygroup중간 계층 그룹/Factory/Robotscomponent독립적으로 참조 가능한 단위/Factory/Robots/Robot_01subcomponentcomponent 내부의 파츠Robot의 개별 링크
pythonfrom pxr import Kind

# kind 설정
model_api = Usd.ModelAPI(prim)
model_api.SetKind(Kind.Tokens.component)

# kind 읽기
print(model_api.GetKind())          # "component"
print(model_api.IsModel())          # True (assembly/group/component 모두 해당)
print(model_api.IsGroup())          # False (component는 group 아님)

프로젝트 코드 — Metadata 전면 적용
.usda 텍스트 방식
usda#usda 1.0
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
Python API 방식
pythonfrom pxr import Usd, Sdf, Kind

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

Metadata 읽기 전략 — GetAllMetadata
pythonprim = stage.GetPrimAtPath("/Factory/Robots/Robot_01")

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

Phase 1 완료 — 지금까지 프로젝트 상태
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
Phase 1이 완료되었습니다. Stage · Prim · Attributes · Relationships · Metadata — USD 씬의 기초 구조가 모두 갖춰졌습니다.

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

<img src="usd-buildup\USD-008.png">

---

<img src="usd-buildup\USD-009.png">

---
