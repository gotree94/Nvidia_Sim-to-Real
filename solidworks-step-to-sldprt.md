# SolidWorks STEP → 개별 SLDPRT 분리 저장 방법

## 문제 상황

STEP 파일(`.step`)을 SolidWorks에서 열고 SLDASM으로 저장하면, 최상위 어셈블리 파일만 저장되고 하위 부품들(SLDPRT)은 생성되지 않는다.

---

## 원인: 3D Interconnect

SolidWorks 2017부터 도입된 **3D Interconnect** 기능이 **기본적으로 켜져 있기 때문**이다.

| 상태 | 동작 |
|------|------|
| 3D Interconnect **ON** (기본값) | STEP 파일을 SolidWorks 내부 형식으로 "변환"하지 않고, 원본 STEP 파일에 **링크**만 유지한 채 트리에 표시 |
| 3D Interconnect **OFF** | 예전 방식대로 STEP을 진짜 SolidWorks 데이터로 **변환(Import)** → 저장 시 개별 SLDPRT 생성 |

---

## 방법 1: 3D Interconnect 비활성화 (권장)

가장 간단하고 확실한 방법.

### Step-by-step

1. **Tools** > **Options** 메뉴 클릭
2. **Import** 탭으로 이동
3. **"Enable 3D Interconnect"** 체크 **해제**
4. **OK** 클릭
5. STEP 파일을 **닫고 다시 열기**

### 저장 방법

1. **File** > **Save As** > 파일 형식을 **SOLIDWORKS Assembly (\*.sldasm)** 으로 선택
2. 저장 버튼 클릭
3. **"Save modified documents"** 창이 뜨면서 각 가상 부품을 저장할지 물어봄
4. **"Save All"** 클릭 → 모든 부품이 개별 `*.sldprt` 파일로 자동 생성됨

> **참고**: 이 설정은 SolidWorks를 재시작해도 유지되므로, 다시 켜기 전까지는 항상 예전 방식으로 동작한다.

---

## 방법 2: 3D Interconnect ON 상태에서 해결하기

3D Interconnect를 계속 켜둬야 하는 경우, 각 부품의 링크를 수동으로 끊는다.

### Step-by-step

1. STEP 파일을 연다 (3D Interconnect ON 상태)
2. FeatureManager 디자인 트리에서 각 부품을 **우클릭**
3. **"Make Independent"** 선택
   - STEP 파일과의 링크가 끊어지고 SolidWorks 네이티브 데이터로 변환됨
4. 모든 부품에 대해 반복
5. **File** > **Save As** > SLDASM으로 저장 → SLDPRT 생성 옵션 제공됨

### 단점

- 부품이 많을수록 노가다가 필요함
- 대형 어셈블리에는 부적합

---

## 방법 3: Save Bodies 활용 (멀티바디 파트로 열었을 때)

STEP 가져오기 옵션을 **"Import assembly as multiple body part"** 로 설정한 경우.

### Step-by-step

1. STEP 파일 열기 옵션에서 **"Import assembly as multiple body part"** 선택
2. 단일 SLDPRT(멀티바디 파트)로 열림
3. **Insert** > **Features** > **Save Bodies** 클릭
4. 각 바디(부품)를 개별 SLDPRT로 저장할 위치 지정
5. 하단의 **"Create Assembly"** 버튼 클릭 → 자동으로 어셈블리(SLDASM)까지 생성됨

### 장점
- 3D Interconnect ON/OFF 관계없이 사용 가능
- 바디별로 저장할 대상을 선택 가능

---

## 옵션 설정 비교

| 3D Interconnect | STEP Import 옵션 | 저장 결과 |
|---|---|---|
| ON (기본) | Default | SLDASM만 저장, SLDPRT 없음 |
| ON | Import multiple bodies as parts | SLDASM만 저장, SLDPRT 없음 |
| OFF | Default | **SLDASM + 개별 SLDPRT 자동 생성** ✅ |
| ON + Make Independent | (모두 동일) | **SLDASM + 개별 SLDPRT 생성 가능** |
| ON/OFF | Import assembly as multiple body part | 멀티바디 SLDPRT → Save Bodies 필요 |

---

## 요약

| 목표 | 권장 방법 |
|---|---|
| 가장 간단하게 SLDPRT까지 한 번에 저장 | **3D Interconnect OFF** → STEP 열기 → Save As SLDASM → Save All |
| 3D Interconnect를 유지해야 함 | 각 부품 우클릭 → **Make Independent** → Save As |
| 멀티바디 파트로 가져온 경우 | **Insert > Features > Save Bodies** → Create Assembly |
