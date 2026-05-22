# Synthetic Data Generation
Data Generation with MobilityGen
Occupancy Map 이란?								Data Generation With MobilityGen

0과 1 사이의 값으로 나타낸 맵으로 0은 free space, 1은 occupied space를 나타낸다

Data Generation with MobilityGen

가이드에 따라 데이터를 생성
시뮬레이션 환경에서는 Ground Truth기반으로 Occupancy map을 미리 만들게된다
Cosmos-transfer
Cosmos-transfer1 build.nvidia.com

Cosmos-transfer1 소개영상
Cosmos-transfer2.5 소개영상

Physical AI NVIDIA Page
NVIDIA Cosmos - 월드 파운데이션 모델로 구현하는 피지컬 AI
Cosmos-transfer2.5
먼저 Huggingface에 가입합니다
가입 후, 계정 > Settings > Create new Access Token > Read Token 생성


Cosmos-transfer2.5
nvidia/Cosmos-Predict2.5-2B · Hugging Face
nvidia/Cosmos-Transfer2.5-2B · Hugging Face
nvidia/Cosmos-Guardrail1 · Hugging Face

다음 링크에 들어가서 Model 사용 허가 신청

Cosmos-transfer2.5
아래 Launchable instance 실행 후, cuda12.8 설치 링크 참고하여 설치
설치 후 다음 명령어를 이용하여 확인 
출력이 다음과 같지 않다면, 
echo 'export PATH=/usr/local/cuda-12.8/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
시도 

Cosmos-transfer2.5
이후 transfer2.5 setup 과정 실행
주의! H100은 Graphics Engine이 없습니다(원격 GUI 사용 불가)


Cosmos-transfer2.5

https://github.com/nvidia-cosmos/cosmos-transfer2.5/blob/main/docs/inference.md
다음 페이지에 따라 예제를 직접 수정해보고, assets/robot_example/robot_prompt 를 수정하여 같은 영상에 다른 prompt 적용해보기
Cosmos-transfer2.5 Examples
모델에 입력할 Prompt는 매우 세밀한 묘사를 하도록 작성해야하며, 
많은 시도를 필요로 합니다.



Cosmos-cosmos2.5 Examples
Input이 애매하거나, 모델이 아직 완벽하지 않기 때문에 오류가 발생하기도 합니다.
Cosmos Synthetic Data Generation 
Cosmos Synthetic Data Generation

Cosmos에 들어갈 input data를 생성하는 script


Cosmos Synthetic Data Generation 

Do it yourself
Isaac Sim과 Cosmos-transfer2.5를 사용하여 산출물을 만들고 아래 항목들을 제출

-	Stage 구성에 사용한 usd 전체
-	Stage 구성 및 Synthetic Data Generation 용도로 사용한 데이터 전체
-	Cosmos-transfer2.5 에 들어간 input 폴더 및 prompt
-	결과 영상











