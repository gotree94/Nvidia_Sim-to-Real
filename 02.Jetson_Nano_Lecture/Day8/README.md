# Day 8: CAD to Sim

* 준비물
   -	블렌더
   -	리깅할 로봇 CAD, RB10-1300E 레인보우로보틱스 - 협동로봇
   -	로봇 사양서

## 1. 리깅이란?
   * 리깅은 3D 모델이 움직일 수 있도록 뼈대를 심는 작업을 말한다
   * 로봇 리깅은 공식적으로 정의된 언어는 아니지만, 간단하게 로봇이 움직일 수 있도록 하는 작업을 뜻한다 

## 2. 파일 가져오기
   * 다운로드 받은 파일을 File > Import로 가져옵니다.
   * Convert Visible Only 체크 해제,
   * Enable Instancing 체크 해제 후
   * Unit을 Meters로 설정하고 Import
      > stp폴더와 같은 곳에 usd 파일 생성

## 3. Prim 정리
   * Looks Prim을 tn__RB101300EEVersion_lMb0r1C에 Drag & Drop 한 후 
   * 다음과 같이 블럭지정하여 Save Selected
   * 중첩되어있는 Xform 안에 있는 Mesh를 정리
   * 메쉬를 상위 Xform으로 옮기기
   * 모든 Link에 대해 반복
   * 사용하지 않는 Xform Prim을 삭제하고, 이름을 읽기 쉽게 변경
   * 로봇의 도면 또는 DH-parameter를 참조하여 새롭게 Xform 생성
   * 일단 필요할 것 같은 Xform 지점을 모두 생성하고, 
   * 이후에 분류를 권장
   * Robot Base의 Translate, Orient를 (0, 0, 0)으로 하여 Z-up을 권장 (사진의 flange는 Link6)  

## 4. Adding Color
   * Mesh의 Property 중 Material, 또는 Mesh가 다양한 Diffuse를 가지고 있는 경우 Diffuse의 Material을 다시 지정

# 5. Blender
   * 블렌더 실행 후 우측 기본 요소 제거
   * 블렌더의 경우 휠 클릭 및 드래그로 네비게이션 진행

   * USD 파일을 드래그앤 드랍하여 불러온 후 Import USD
   * 이후 Root를 확장, 내부 요소를 블럭 지정한 후

   * 화면에 마우스를 올리고, alt + p > clear parent
   * 작업할 메쉬 를 마우스로 클릭

   * 화면에서 Tab을 눌러 Edit Mode로 진행
   * 점을 클릭 또는, 점 다수를 shift로 클릭하여 선택하고 
   * ctrl + s > Cursor to Selected
   * 점을 잘못 클릭했다면 alt + a 로 선택해제

   * F3을 눌러 검색 > Origin to 3d Cursor

   * 새로운 Blender 창을 열고, USD Import 진행
   * Scale을 100으로 설정 

   * Root를 선택한 후, 기록했던 Location을 빼기

   * 새로운 축을 만들고, 세우기 위해 
   * F3 > Cursor to World Origin 하고,
   * Layout > Empty > Plain Axes로 축 생성

   * Root, Empty 를 ctrl로 차례대로 선택 후
   * ctrl + p > set parent to object (keep transform)

   * 여기서부터, clear parent, set parent를 전체적으로 반복
   * 생성했던 Xform은 clear parent,
   * 나머지는 clear and keep transform

   * 오른 쪽 항목에서 Mesh 클릭 후 ctrl 클릭으로      (Plane Axes)을 클릭하고
   * 화면에 마우스를 올린 후 ctrl + p > Set parent to Object (Keep Transform)

   * 메쉬의 origin 설정
   * 메쉬 클릭 후 (드래그 가능)
   * F3 > Object > Set Origin > Origin to Center of Mass 
   * 별도의 origin 설정이 필요할 수 있음

   * 상단의 Scripting 에 들어가서 New 클릭 후, filepath 설정 후 실행 버튼 클릭  
```
import bpy
bpy.ops.wm.usd_export(filepath='/home/shadeform/output.usdc', export_meshes=True, merge_parent_xform=True, convert_world_material=True)
```

## 6. Diffuse
   * stage의 env_light 삭제
   * 모든 메쉬를 보도록 필터링하고 선택한 후
   * Refinement Override에 체크하고 
   * Refinement Level 조정

## 7. Joints
   * 움직이는 Link에 Rigidbody 속성을 부여
   * 로봇의 기반인 Robot_Base에 우클릭하여 fixed joint를 생성
   * 생성한 fixed joint에 Articulation root 부여
   * 이후 Link끼리 Revolute Joint를 생성하고 
   * Revolute Joint의 Axis를 직접 조절
   * Revolute Joint에 Angular Drive를 추가
   * Damping과 Stiffness를 적절히 부여
   * Core API Tutorial Series
      * Core API Tutorial Series - nvidia : https://docs.isaacsim.omniverse.nvidia.com/5.1.0/core_api_tutorials/index.html
   * Jupyter notebook extension
      * window > Extensions 
   * 팝업 창에 jupyter를 검색 후, 나오는 JUPYTER NOTEBOOK INTEGRATION을 클릭 > DISABLED, AUTOLOAD 왼쪽의 버튼을 모두 클릭하여 활성화
   * 활성화된 Jupyter Notebook 사용
      * window > Jupyter Notebook
   * Jupyter Notebook 창에서
      * Omniverse (Python 3) 커널 선택
## 8. BaseSample
   * BaseSample code는 robotics 예제에서 재사용 할 수 있도록 만들어진 boilerplate 코드
   * 아래와 같은 작업들을 수행할 수 있음
      •	Stage 생성 시, world 초기화
      •	전체 앱 종료 없이 변경점만 로딩
      •	World안의 객체를 초기 값으로 변경
   * Window > Examples > Robotics Examples > General > Hello World > Load 로 
   * 로딩할 수 있으나, BaseSample를 상속하여 Jupyter Notebook에서 사용할 것임

## 9. 
   * 01.hello_world
      * world = self.get_world() 로 world를 받아온 후, 바닥판을 추가하는 예제
      * world는 singleton이기 때문에, Isaac Sim 구동 중에는 하나의 world만 존재
      * API는 python api 링크를 참조 : https://docs.isaacsim.omniverse.nvidia.com/5.0.0/reference_python_api.html

   * 02.hello_cube
      * Collider와 Rigidbody를 가지고있는 DynamicCuboid가 포함된 예제
      * https://docs.isaacsim.omniverse.nvidia.com/5.0.0/py/source/extensions/isaacsim.core.api/docs/index.html#isaacsim.core.api.objects.DynamicCuboid
      * setup_scene함수에서 world.scene.add를 사용해 scene을 구성할 수 있음

   * 03.get_assets
      * Asset의 URL을 받아오고, reference로 띄우는 예제

   * 04.hello_robot
      * 객체를 world.scene.get_object(name)으로 받아보기

   * 05.wheeled_robot
      * physics callback을 추가하여 재생버튼을 눌렀을 때 로봇이 움직이도록 해보기
      * 두 바퀴의 속도를 다르게 해보기 

   * 06.manipulator
      * Wheeled robot이외에, Franka_panda manipulator를 생성해보자

   * 07.controllers
      * PickPlaceController를 이용해, Articulation에 간편한 인터페이스로 Pick and Place 동작을 수행해보기

   * 08.integrating_robots
      * 지금까지 만든 두 로봇 장면을 합쳐보기

   * 09.tasks
      * task는 scene생성, 정보수집 및 계산 등을 용이하게 하기 위한 class
      * 지금까지 활용한 항목들을 task를 이용해서 다시 작성할 수 있다. 

   * Explore more examples
      * Window > Examples > Robotics Examples에서 다양한 robotics examples 확인 가능
      * ex) multi-robot > RoboFactory 

   * Do it yourself
      * 기존까지 구현한 Scene에 오늘 학습한 Python code를 활용해보기
         -	매니퓰레이터가 들어야 할 큐브에 mass를 높게 설정해보기
-	jetbot에 다른 controller를 적용해보기
등..
