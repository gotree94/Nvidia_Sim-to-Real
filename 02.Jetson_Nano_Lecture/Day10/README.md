# Day10 : Sim-to-Real with NVIDIA Isaac 

## 1. Brev
   * 오늘 과정은 RTX Pro 6000 인스턴스를 사용하여 Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac을 진행합니다.
      * https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/index.html
   * Instance 실행 후, nvidia-ctk --version 명령어를 통해 설치여부를 확인합니다.
   * 또한
      ```sudo chmod 666 /var/run/docker.sock로 selkies 내부에서 도커를 사용하도록 합니다.
         sudo chmod -R 777 /home/shadeform
      ```
```
nvidia-ctk --version
```

## 2. Hands on 설명

   * Overview — Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac
      * https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/01-overview.html
   * Task: Centrifuge Vial Pick-and-Place


## 3. Centrifuge Vial Pick-and-Place

   * 원심분리 바이알: 실제 사람들이 만지기 꺼려하는 작업
   * SO-101: 간단한 과제로 설정하기 적절


## 4. Why Simulation Matters

   1. Time: 시간적 이점 확보
   2. Cost: 실제 로봇 시험보다 우수한 비용 효율성 확보
   3. Safety: 실제 로봇 작업 수행이 위험할 수 있음
   4. Diversity: 다양한 DR(Domain Randomization) 수행 가능

## 5. How it Works

Hands on에서는 Isaac GROOT-n1.6 VLA 모델을 사용하여 
- “pick up the vial and place it on the rack” 이라는 자연어 입력을 넣고 
-  joint feedback과 camera observation을 policy 입력으로 넣은 후 
> motor position을 결과로 받아, 동작을 수행 할 예정

## 6. What Is Sim-to-Real?
Sim-to-Real이란 Simulation 환경 내에서 policy를 학습하여 실제 하드웨어에 배포하는 것
> 시뮬레이션에서 학습하였지만, 실제에서도 잘 동작하는 것이 최종 목적

## 7. Sim-to-Real Gap
   * The Reality Gap in Robotics: Challenges, Solutions, and Best Practices
      * https://arxiv.org/pdf/2510.20808
   * Visualizing the Reality Gap — Getting Started With Isaac Lab
      * https://docs.nvidia.com/learning/physical-ai/getting-started-with-isaac-lab/latest/transferring-robot-learning-policies-from-simulation-to-reality/02-the-reality-gap/01-visualizing-the-reality-gap.html

- Sensing Gaps
- Actuation Gaps
- Physics Gaps
- Modeling Gaps

## 8. 컨테이너 환경 설정

```
git clone https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop.git
cd Sim-to-Real-SO-101-Workshop
sudo apt-get update && sudo apt-get install -y git-lfs
# selkis의 경우 docker-io도 설치
git lfs install
git lfs pull
```

```
docker build -t teleop-docker -f docker/sim/Dockerfile .
./docker/real/build.sh blackwell 
터미널 창을 새로 열어
pip install -U "huggingface_hub[cli]" 
hf auth login 
이후 read token 입력
#nvidia/GR00T-N1.6-3B · Hugging Face
https://huggingface.co/nvidia/GR00T-N1.6-3B
```

## 9. 모델 파일 다운로드

```
mkdir -p models
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real
hf download aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02 \
  --local-dir ./models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02
hf download aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70 \
  --local-dir ./models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
```

## 10. Terminal 1

```
xhost + 
sudo docker run -it --rm --name real-robot --network host --privileged \
    --device nvidia.com/gpu=all \
    -e DISPLAY \
    -v /dev:/dev \
    -v /run/udev:/run/udev:ro \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
    -v $PWD/models:/workspace/models \
    -v $PWD/docker/env:/root/env \
    -v $PWD/docker/real/scripts:/Isaac-GR00T/gr00t/eval/real_robot/SO100 \
    real-robot \
    /bin/bash
```

## 11. Terminal 1(Selkies)

``
xhost + 
sudo docker run -it --rm --name real-robot --network host --privileged \
    --device nvidia.com/gpu=all \
    -e DISPLAY \
    -v /dev:/dev \
    -v /run/udev:/run/udev:ro \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
    -v /home/shadeform/Sim-to-Real-SO-101-Workshop/models:/workspace/models \
    -v $PWD/docker/env:/root/env \
    -v $PWD/docker/real/scripts:/Isaac-GR00T/gr00t/eval/real_robot/SO100 \
    real-robot \
    /bin/bash
```

## 12.Terminal 1

```
export 
MODEL=aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left/checkpoint-10000

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
```

## 13. Terminal 2

```
xhost + 
sudo docker run --name teleop -it --privileged --device nvidia.com/gpu=all -e "ACCEPT_EULA=Y" --rm --network=host \
   -e "PRIVACY_CONSENT=Y" \
   -e DISPLAY \
   -v /dev:/dev \
   -v /run/udev:/run/udev:ro \
   -v $HOME/.Xauthority:/root/.Xauthority \
   -v ~/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
   -v ~/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
   -v ~/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
   -v ~/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
   -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
   -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
   -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
   -v ~/docker/isaac-sim/documents:/root/Documents:rw \
   -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
   -v $PWD/docker/env:/root/env \
   -v $PWD:/workspace/Sim-to-Real-SO-101-Workshop \
   teleop-docker:latest
```

## 14. Terminal 2(Selkies)

```
xhost + 
sudo docker run --name teleop -it --privileged --device nvidia.com/gpu=all -e "ACCEPT_EULA=Y" --rm --network=host \
   -e "PRIVACY_CONSENT=Y" \
   -e DISPLAY \
   -v /dev:/dev \
   -v /run/udev:/run/udev:ro \
   -v $HOME/.Xauthority:/root/.Xauthority \
   -v /tmp/.X11-unix:/tmp/.X11-unix \
   -v /home/shadeform/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
   -v /home/shadeform/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
   -v /home/shadeform/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
   -v /home/shadeform/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
   -v /home/shadeform/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
   -v /home/shadeform/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
   -v /home/shadeform/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
   -v /home/shadeform/docker/isaac-sim/documents:/root/Documents:rw \
   -v /home/shadeform/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
   -v /home/shadeform/Sim-to-Real-SO-101-Workshop/docker/env:/root/env \
   -v /home/shadeform/Sim-to-Real-SO-101-Workshop:/workspace/Sim-to-Real-SO-101-Workshop \
   teleop-docker:latest
```

## 15. Terminal 2

```
lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --headless \
    --rerun
```

## 16. Terminal 2(Selkies)

```
apt-get update && apt-get install -y xvfb
xvfb-run -a lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --headless \
    --rerun
```





