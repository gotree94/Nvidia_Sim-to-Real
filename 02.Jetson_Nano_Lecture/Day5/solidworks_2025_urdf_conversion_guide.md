# SolidWorks 2025 3D 설계 → URDF 변환 가이드

> 작성일: 2026-05-18
> 대상: SolidWorks 2025 사용자

---

## 목차

1. [URDF 기본 구조](#1-urdf-기본-구조)
2. [공식 sw2urdf 호환성 현황](#2-공식-sw2urdf-호환성-현황)
3. [변환 방법 4가지](#3-변환-방법-4가지)
   - [방법 1: sw2urdf 소스 직접 빌드](#방법-1-sw2urdf-소스에서-직접-빌드)
   - [방법 2: STL 내보내기 → Python URDF 생성 (추천)](#방법-2-stl-내보내기--python-urdf-생성-추천)
   - [방법 3: Python 전용 변환 툴 활용](#방법-3-python-전용-변환-툴-활용)
   - [방법 4: 중간 포맷 경유 (STEP → 타 CAD)](#방법-4-중간-포맷-경유-step--타-cad)
4. [실전 추천 워크플로우: 하이브리드 방식](#4-실전-추천-워크플로우-하이브리드-방식)
5. [변환 시 핵심 주의사항](#5-변환-시-핵심-주의사항)
6. [참고 링크](#6-참고-링크)

---

## 1. URDF 기본 구조

URDF(Unified Robot Description Format)는 ROS에서 로봇을 기술하는 XML 기반 포맷입니다.

### 주요 XML 요소

| 요소 | 설명 | 필수 속성 |
|---|---|---|
| `<robot>` | 최상위 루트 | `name` |
| `<link>` | 로봇의 각 파트 (강체) | `name` |
| `<joint>` | 링크 간 연결 관계 | `name`, `type`, `parent`, `child` |
| `<visual>` | 링크의 시각적 표현 (메쉬/형상) | `geometry` |
| `<collision>` | 충돌 검출용 형상 | `geometry` |
| `<inertial>` | 관성 정보 (질량, 관성 텐서) | `mass`, `inertia` |

### 링크 기본 구조

```xml
<link name="link1">
  <inertial>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <mass value="1.0"/>
    <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/>
  </inertial>
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://my_robot/meshes/link1.stl"/>
    </geometry>
    <material name="gray">
      <color rgba="0.5 0.5 0.5 1.0"/>
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://my_robot/meshes/link1_collision.stl"/>
    </geometry>
  </collision>
</link>
```

### 조인트 기본 구조

```xml
<joint name="joint1" type="revolute">
  <parent link="base_link"/>
  <child link="link1"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-3.14" upper="3.14" effort="10.0" velocity="1.0"/>
</joint>
```

### 조인트 타입

| 타입 | 설명 |
|---|---|
| `revolute` | 회전 + 각도 제한 있음 (limit 필수) |
| `continuous` | 무제한 회전 |
| `prismatic` | 직선 이동 |
| `fixed` | 고정 |
| `floating` | 6자유도 |
| `planar` | 평면 이동 |

---

## 2. 공식 sw2urdf 호환성 현황

`ros/solidworks_urdf_exporter` (sw2urdf)는 공식 SolidWorks → URDF 변환 플러그인입니다.

| SolidWorks 버전 | sw2urdf 버전 | 릴리스일 | 상태 |
|---|---|---|---|
| 2018 SP5 / 2019 | v1.5.1 | 2019-08 | 지원 종료 |
| 2020 | v1.6.0 | 2020-10 | 지원 종료 |
| 2021 | v1.6.1 | 2021-11 | **마지막 공식 릴리스** |
| 2022 | ❌ | — | 미지원 |
| 2023 | ❌ | — | 미지원 |
| 2024 | ❌ | — | 미지원 |
| **2025** | **❌** | **—** | **미지원 (본 가이드 대상)** |
| 2026 | ❌ | — | GitHub 이슈만 오픈됨 |

> GitHub 레포지토리: https://github.com/ros/solidworks_urdf_exporter
>
> 2021년 이후로 공식 릴리스가 중단되었으며, 131개 fork 중 SolidWorks 2025를 공식 지원하는 fork는 확인되지 않았습니다.

---

## 3. 변환 방법 4가지

### 방법 1: sw2urdf 소스에서 직접 빌드

공식 소스 코드를 직접 받아 SolidWorks 2025 API로 빌드하는 방법입니다.

#### 절차

```bash
# 1. 소스 클론
git clone https://github.com/ros/solidworks_urdf_exporter.git
cd solidworks_urdf_exporter
```

```
# 2. Visual Studio 2022에서 SW2URDF.sln 열기
#    (관리자 권한으로 실행 필수)

# 3. SolidWorks 2025 API DLL 참조 경로 업데이트
#    C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\api\ 폴더의 DLL 참조

# 4. .NET Desktop Development 워크로드 확인
#    Visual Studio Installer → 수정 → 체크

# 5. 빌드 (F6)

# 6. 생성된 DLL을 SolidWorks 2025에 Add-in으로 등록
```

#### SolidWorks API 툴 설치

SolidWorks 설치 시 **"SolidWorks API SDK"** 또는 **"SolidWorks API Tools"** 가 함께 설치되어야 합니다. 설치되어 있지 않다면 SolidWorks 설치 프로그램에서 Modify → API SDK 추가 설치가 필요합니다.

#### 장단점

| 장점 | 단점 |
|---|---|
| SolidWorks 내에서 GUI로 직접 작업 가능 | API 호환성 보장되지 않음 |
| 좌표계/관절 설정이 직관적 | COM Interop 이슈 발생 가능 |
| 메쉬 export가 자동화됨 | VS + .NET 환경 설정 필요 |

#### 성공 확률: 중간

SolidWorks API는 하위 호환성을 유지하는 편이나, COM Interop과 .Net Framework 버전 차이로 인해 빌드 후 정상 동작하지 않을 수 있습니다. 최신 버전에서 성공 사례가 일부 있으나 공식 확인된 것은 아닙니다.

---

### 방법 2: STL 내보내기 → Python URDF 생성 (★★★★ 추천)

가장 확실하고 제어 가능한 방법입니다. SolidWorks 버전에 독립적입니다.

#### 전체 워크플로우

```
SolidWorks 2025
  │
  ├─ 1. 어셈블리에서 각 링크를 별도 파트로 분리
  │
  ├─ 2. 각 파트를 STL로 내보내기
  │    File → Save As → STL (*.stl)
  │    (옵션: DAE 포맷이 색상 보존에 더 유리)
  │
  ├─ 3. 각 joint의 origin(xyz/rpy)과 axis 방향을
  │    SolidWorks Measure 도구로 측정하여 기록
  │
  └─ 4. Python 스크립트로 URDF 생성
```

#### Python URDF 생성 예제

```python
import trimesh
import numpy as np
from xml.etree import ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """XML을 보기 좋게 출력"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def compute_inertia_from_mesh(stl_path, mass=1.0):
    """STL 메쉬로부터 관성 텐서 계산"""
    mesh = trimesh.load(stl_path)
    # mesh.moment_inertia는 단위 질량 기준 → 실제 질량 곱하기
    inertia = mesh.moment_inertia * mass
    # mesh가 원점 기준 (필요시 translate)
    center_of_mass = mesh.center_mass
    return center_of_mass, mass, inertia


def create_link_element(name, stl_path, mass=1.0):
    """URDF link 요소 생성"""
    com, mass, inertia = compute_inertia_from_mesh(stl_path, mass)
    ixx, ixy, ixz, iyy, iyz, izz = (
        inertia[0][0], inertia[0][1], inertia[0][2],
        inertia[1][1], inertia[1][2], inertia[2][2]
    )

    link = ET.Element("link", name=name)

    # 관성 정보
    inertial = ET.SubElement(link, "inertial")
    ET.SubElement(inertial, "origin",
                  xyz=f"{com[0]} {com[1]} {com[2]}",
                  rpy="0 0 0")
    ET.SubElement(inertial, "mass", value=str(mass))
    ET.SubElement(inertial, "inertia",
                  ixx=str(ixx), ixy=str(ixy), ixz=str(ixz),
                  iyy=str(iyy), iyz=str(iyz), izz=str(izz))

    # 시각 정보
    visual = ET.SubElement(link, "visual")
    ET.SubElement(visual, "origin", xyz="0 0 0", rpy="0 0 0")
    geom_v = ET.SubElement(visual, "geometry")
    ET.SubElement(geom_v, "mesh",
                  filename=f"package://my_robot/meshes/{name}.stl")

    # 충돌 정보 (시각과 동일한 mesh 사용)
    collision = ET.SubElement(link, "collision")
    ET.SubElement(collision, "origin", xyz="0 0 0", rpy="0 0 0")
    geom_c = ET.SubElement(collision, "geometry")
    ET.SubElement(geom_c, "mesh",
                  filename=f"package://my_robot/meshes/{name}_collision.stl")

    return link


def create_joint_element(name, parent, child, joint_type="revolute",
                         origin_xyz="0 0 0", origin_rpy="0 0 0",
                         axis_xyz="0 0 1",
                         lower="-3.14159", upper="3.14159",
                         effort="10.0", velocity="1.0"):
    """URDF joint 요소 생성"""
    joint = ET.Element("joint", name=name, type=joint_type)
    ET.SubElement(joint, "parent", link=parent)
    ET.SubElement(joint, "child", link=child)
    ET.SubElement(joint, "origin", xyz=origin_xyz, rpy=origin_rpy)
    ET.SubElement(joint, "axis", xyz=axis_xyz)

    if joint_type in ("revolute", "prismatic"):
        ET.SubElement(joint, "limit",
                      lower=lower, upper=upper,
                      effort=effort, velocity=velocity)

    return joint


def build_robot_urdf(links_info, joints_info, output_path):
    """전체 URDF 조립하여 파일로 저장"""
    robot = ET.Element("robot", name="my_robot")

    for name, stl_path, mass in links_info:
        robot.append(create_link_element(name, stl_path, mass))

    for info in joints_info:
        robot.append(create_joint_element(**info))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(prettify(robot))

    print(f"URDF saved to: {output_path}")


# ─── 사용 예시 ───────────────────────────────────────────
if __name__ == "__main__":
    # 링크 정보: (name, stl_path, mass)
    links = [
        ("base_link", "meshes/base_link.stl", 2.5),
        ("upper_arm", "meshes/upper_arm.stl", 1.8),
        ("forearm",   "meshes/forearm.stl",   1.2),
    ]

    # 조인트 정보: (name, parent, child, joint_type, ...)
    joints = [
        {"name": "shoulder", "parent": "base_link", "child": "upper_arm",
         "joint_type": "revolute",
         "origin_xyz": "0 0 0.15", "origin_rpy": "0 0 0",
         "axis_xyz": "0 1 0",
         "lower": "-2.094", "upper": "2.094"},
        {"name": "elbow", "parent": "upper_arm", "child": "forearm",
         "joint_type": "revolute",
         "origin_xyz": "0 0 0.3", "origin_rpy": "0 0 0",
         "axis_xyz": "0 1 0",
         "lower": "-2.094", "upper": "2.094"},
    ]

    build_robot_urdf(links, joints, "my_robot.urdf")
```

#### 필요 패키지 설치

```bash
pip install trimesh numpy
```

#### 장단점

| 장점 | 단점 |
|---|---|
| SolidWorks 버전에 완전히 독립적 | 조인트 origin/axis를 수동 측정 필요 |
| 관성(inertia)을 trimesh로 정확 계산 | 초기 설정에 시간 소요 |
| CI/CD 파이프라인에 통합 가능 | SolidWorks GUI 편의성 포기 |
| 버전 관리 용이 (Python 스크립트) | |

---

### 방법 3: Python 전용 변환 툴 활용

SolidWorks 외부에서 STL/STEP을 처리하는 Python 기반 도구들을 활용합니다.

#### 추천 라이브러리

| 라이브러리 | 용도 | 설치 |
|---|---|---|
| `trimesh` | 메쉬 로드, 관성 계산, 변환 | `pip install trimesh` |
| `pyassimp` | 다양한 3D 포맷 읽기 (STEP, OBJ, DAE) | `pip install pyassimp` |
| `urdfpy` | URDF 읽기/쓰기 | `pip install urdfpy` |
| `scikit-robot` | URDF 메쉬 포맷 변환 (3dxml → dae) | `pip install scikit-robot` |

#### Blender + Phobos 활용

SolidWorks → STL export → Blender Import → Phobos Add-on으로 URDF 생성

```
1. Blender 설치 (https://www.blender.org)
2. Phobos Add-on 설치
   (https://github.com/dfki-ric/phobos)
3. STL 파일 Import
4. Phobos로 링크/조인트 구조 편집
5. URDF export

장점: GUI 기반 편집, 관절 설정 직관적
단점: Blender 학습 필요, 대형 어셈블리에 느림
```

#### scikit-robot 메쉬 변환

sw2urdf가 export한 3dxml 메쉬를 DAE로 변환할 때 유용합니다.

```bash
pip install scikit-robot -U
convert-urdf-mesh <URDF_PATH> --output <OUTPUT_URDF_PATH>
```

---

### 방법 4: 중간 포맷 경유 (STEP → 타 CAD)

SolidWorks 2025에서 STEP으로 저장한 후, URDF exporter가 있는 다른 CAD 제품으로 가져오는 방법입니다.

| 경유 CAD | 변환 도구 | 특징 |
|---|---|---|
| **Fusion 360** | `f2urdf` 애드인 | 무료 (개인/취미용), STEP import 가능 |
| **Onshape** | `onshape-to-robot` | 웹 기반, 무료 계정 가능 |
| **Blender** | `Phobos` add-on | 완전 무료, 모든 포맷 지원 |

#### Onshape-to-robot 예시

```bash
pip install onshape-to-robot

# config.yaml 작성 후 실행
onshape-to-robot config.yaml
```

#### 장단점

| 장점 | 단점 |
|---|---|
| GUI 기반으로 관절 설정 용이 | STEP 변환 시 좌표계/관절 정보 손실 |
| 초보자에게 가장 쉬운 접근법 | 재변환 시마다 STEP 재임포트 필요 |
| | CAD 툴을 추가로 배워야 함 |

---

## 4. 실전 추천 워크플로우: 하이브리드 방식

초기 구축에는 시간이 들지만, 이후 설계 변경에 강건한 방식입니다.

### 1회성 설정

```
Step 1: SolidWorks 2025
  ├─ 어셈블리 트리 구조 정리 (깔끔한 링크/서브어셈블리 명명)
  └─ 각 파트명을 URDF link name과 매핑할 규칙 정의

Step 2: STL 일괄 내보내기용 SolidWorks 매크로 작성
  ├─ 모든 파트를 순회하며 STL export (또는 수동 export)
  └─ 일관된 mesh 저장 경로 유지

Step 3: Python 템플릿 스크립트 작성
  ├─ trimesh로 STL → 관성 계산
  ├─ 미리 측정한 조인트 origin/axis 값을 변수로 정의
  └─ URDF XML 자동 생성

Step 4: ROS 툴로 검증
  ├─ check_urdf my_robot.urdf
  └─ Rviz로 시각화 확인
```

### 설계 변경 시

```
1. SolidWorks에서 파트 수정
2. 매크로로 STL 재export
3. Python 스크립트 재실행 → URDF 업데이트
4. check_urdf / Rviz로 확인
```

### 검증 명령어

```bash
# URDF 문법 및 연결 구조 검증
check_urdf my_robot.urdf

# URDF to PDF (구조 다이어그램)
urdf_to_graphiz my_robot.urdf

# Rviz 시각화
rosrun urdf_tutorial display.launch model:=my_robot.urdf
```

---

## 5. 변환 시 핵심 주의사항

### 좌표계 정렬 (가장 중요)

```
각 링크의 <origin>은 부모 조인트 기준 상대 좌표입니다.

측정 팁:
- SolidWorks Measure 도구로 두 좌표계 간 거리/각도 측정
- 조인트 축 방향 확인: X(1 0 0), Y(0 1 0), Z(0 0 1)
- RPY는 Z-Y-X (roll-pitch-yaw) 순서
```

### 관성 (Inertia) 문제

```yaml
문제: CAD export 관성 값이 부정확하거나 누락됨
해결: trimesh.moment_inertia 로 STL 기반 재계산

팁:
- mass는 SolidWorks 물성치에서 확인
- origin은 center_of_mass 사용
- 관성이 0이면 physics simulation에서 불안정
```

### 메쉬 최적화

| 항목 | 권장사항 |
|---|---|
| STL face 수 | 링크당 10,000 ~ 50,000 face 권장 |
| collision mesh | visual mesh와 별도로 단순화된 mesh 사용 |
| 포맷 | STL (범용), DAE (색상), OBJ (범용) |
| decimation | Meshlab, Blender, trimesh.simplify 사용 |

### 조인트 타입 선택

| 상황 | 타입 | 비고 |
|---|---|---|
| 일반 회전 관절 | `revolute` | lower/upper로 각도 제한 |
| 연속 회전 (바퀴) | `continuous` | limit 불필요 |
| 선형 액추에이터 | `prismatic` | lower/upper로 변위 제한 |
| 고정 연결 | `fixed` | 용접/브라켓 등 |

---

## 6. 참고 링크

### 공식 리소스

| 리소스 | URL |
|---|---|
| sw2urdf GitHub | https://github.com/ros/solidworks_urdf_exporter |
| sw2urdf ROS Wiki | http://wiki.ros.org/sw_urdf_exporter |
| URDF 튜토리얼 | http://wiki.ros.org/urdf/Tutorials |
| URDF 사양 | http://wiki.ros.org/urdf/XML |

### 변환 도구

| 도구 | 대상 | URL |
|---|---|---|
| f2urdf | Fusion 360 | https://github.com/syuntoku14/fusion2urdf |
| onshape-to-robot | Onshape | https://github.com/Rhoban/onshape-to-robot |
| Phobos | Blender | https://github.com/dfki-ric/phobos |
| urdfpy | Python | https://github.com/mmatl/urdfpy |
| trimesh | Python | https://github.com/mikedh/trimesh |

### ROS 검증 도구

```bash
sudo apt install ros-<distro>-urdf-tutorial
sudo apt install ros-<distro>-joint-state-publisher-gui
```

---

### 빠른 선택 가이드

| 상황 | 추천 방법 |
|---|---|
| SolidWorks 2025에 익숙하고 GUI 선호 | 방법 1: sw2urdf 소스 빌드 시도 |
| 안정적이고 재현 가능한 파이프라인 필요 | **방법 2: STL → Python (최우선 추천)** |
| Blender도 같이 사용 중 | 방법 3: Blender + Phobos |
| 초보자, 다른 CAD 사용 가능 | 방법 4: STEP → Onshape/Fusion 경유 |
