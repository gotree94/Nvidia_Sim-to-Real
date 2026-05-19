# USD(Universal Scene Description)

> **USD(Universal Scene Description)의 핵심 개념들을 하나의 일관된 프로젝트로 엮어서 빌드업하는 방식은 매우 효과적인 교육 구조입니다.**

---

먼저 전체 커리큘럼 구조를 설계해 볼게요.USD 교육 커리큘럼의 전체 구조를 먼저 시각화하고, 이후 각 모듈의 상세 내용을 단계적으로 빌드업하는 방식으로 설계하겠습니다

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


---


---


---

