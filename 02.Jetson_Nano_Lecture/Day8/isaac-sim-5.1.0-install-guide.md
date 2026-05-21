# Isaac Sim 5.1.0 설치 가이드 (Ubuntu 22.04 + RTX 5090)

> 대상 환경: **노트북 ROG Strix SCAR 16 (G635LX)**
> **GPU**: RTX 5090 | **RAM**: 24GB | **OS**: Ubuntu 22.04
> **User**: gotree94 | **설치 방식**: **Git clone → build.sh 빌드**

---

## 1. 사전 준비

```bash
cd /home/gotree94

sudo apt update
sudo apt install build-essential gcc-11 g++-11 libegl1 libvulkan1 rsync python3 python3-pip git-lfs

# GCC 11 고정
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200
gcc --version   # 11.x.x 확인
```

---

## 2. NVIDIA 드라이버 (RTX 5090 = Blackwell, v570+ 필수)

```bash
ubuntu-drivers devices
sudo apt install nvidia-driver-570     # 또는 nvidia-driver-570-open (hybrid)
sudo reboot
nvidia-smi   # RTX 5090, Driver 570.x 확인
```

---

## 3. 소스 빌드

```bash
cd /home/gotree94/isaacsim

# git LFS 대용량 파일 (필수)
git lfs install
git lfs pull

# CRLF 개행문자 변환 (Windows에서 받은 경우)
sed -i 's/\r$//' tools/packman/packman
find . -name "*.sh" -exec sed -i 's/\r$//' {} \;

# 빌드 (30분~1시간 소요)
./build.sh
```

```
(base) gotree94@gotree94-ROG-Strix-SCAR-16-G635LX-G635LX:~/isaacsim$ ./build.sh
Script dir: /home/gotree94/isaacsim
>>> Fetching all dependencies.
Using NVCC binary: /home/gotree94/isaacsim/_build/target-deps/cuda/bin/nvcc
Using CUDA includes directory: /home/gotree94/isaacsim/_build/target-deps/cuda/include
Using CUDA libs directory: /home/gotree94/isaacsim/_build/target-deps/cuda/lib64
** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/_repo/deps/repo_kit_tools/kit-template/premake5-kit.lua(183)

Script dir: /home/gotree94/isaacsim
Selected environment: integ for app version: 5.1.0-rc.19 with regex: 
ISAACSIM_BUILD_SHA aa503a9
ISAACSIM_BUILD_DATE Thu Nov 20 17:21:27 2025 -0600
ISAACSIM_BUILD_BRANCH main
ISAACSIM_BUILD_BRANCH main
ISAACSIM_BUILD_VERSION 5.1.0-rc.19
ISAACSIM_BUILD_REPO https://github.com/isaac-sim/IsaacSim.git
Generating version header file: main aa503a9 5.1.0-rc.19 Thu Nov 20 17:21:27 2025 -0600 https://github.com/isaac-sim/IsaacSim.git
** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/_build/linux-x86_64/release/kit/dev/ogn/ogn_helpers.lua(433)

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/_build/linux-x86_64/release/kit/dev/ogn/ogn_helpers.lua(406)

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/source/extensions/isaacsim.asset.importer.urdf/premake5.lua(27)

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @C function

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/source/extensions/isaacsim.asset.importer.urdf/premake5.lua(28)

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/source/extensions/isaacsim.asset.gen.conveyor/premake5.lua(47)

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/source/extensions/isaacsim.asset.importer.mjcf/premake5.lua(28)

** Warning: the flags value FatalCompileWarnings has been deprecated and will be removed.
   Use `fatalwarnings { "All" }` instead.
   @/home/gotree94/isaacsim/source/extensions/isaacsim.asset.importer.mjcf/premake5.lua(29)

Script dir: /home/gotree94/isaacsim
Build number: '5.1.0-rc.19+main.0.aa503a9b.local'
Written to file: '/home/gotree94/isaacsim/_build/linux-x86_64/debug/VERSION'
Script dir: /home/gotree94/isaacsim
Build number: '5.1.0-rc.19+main.0.aa503a9b.local'
Written to file: '/home/gotree94/isaacsim/_build/linux-x86_64/release/VERSION'
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-pip_list.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-pip_list.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-pycocotools.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-pycocotools.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-omni.kit.app.app_framework.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-omni.kit.app.app_framework.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.simulation_app.hello_world.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.simulation_app.hello_world.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.simulation_app.change_resolution.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.simulation_app.change_resolution.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.simulation_app.load_stage.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.simulation_app.load_stage.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_createstage_config.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_createstage_config.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_multiprocess.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_multiprocess.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_viewport_ready.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_viewport_ready.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_headless_no_rendering.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_headless_no_rendering.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.cloner.clone_ants.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.cloner.clone_ants.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.add_cubes.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.add_cubes.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.add_frankas.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.add_frankas.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.data_logging.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.data_logging.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.control_robot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.control_robot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.simulate_robot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.simulate_robot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.simulation_callbacks.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.simulation_callbacks.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.time_stepping.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.time_stepping.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.visual_materials.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.visual_materials.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.omnigraph_triggers.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.omnigraph_triggers.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.cloth.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.cloth.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.rigid_contact_view.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.rigid_contact_view.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.core.api.detailed_contact_data.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.core.api.detailed_contact_data.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_add_depth_sensor.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_add_depth_sensor.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_opencv_fisheye.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_opencv_fisheye.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_opencv_pinhole.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_opencv_pinhole.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_pre_isp_pipeline.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_pre_isp_pipeline.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_ros.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_ros.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_view.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_view.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.rtx.inspect_lidar_metadata.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.rtx.inspect_lidar_metadata.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.rtx.inspect_radar_metadata.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.rtx.inspect_radar_metadata.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.rtx.resolve_object_ids_from_gmo.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.rtx.resolve_object_ids_from_gmo.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.rtx.rotating_lidar_rtx.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.rtx.rotating_lidar_rtx.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.rtx.specify_non_visual_materials.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.rtx.specify_non_visual_materials.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.physx.rotating_lidar_physX.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.physx.rotating_lidar_physX.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.manipulators.franka.franka_gripper.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.manipulators.franka.franka_gripper.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.manipulators.cobotta_900.follow_target_example.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.manipulators.cobotta_900.follow_target_example.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.manipulators.cobotta_900.pick_up_example.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.manipulators.cobotta_900.pick_up_example.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.manipulators.cobotta_900.gripper_control.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.manipulators.cobotta_900.gripper_control.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.manipulators.franka_pick_up.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.manipulators.franka_pick_up.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.manipulators.ur10_pick_up.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.manipulators.ur10_pick_up.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.robot.wheeled_robots.examples.jetbot_differential_move.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.robot.wheeled_robots.examples.jetbot_differential_move.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-omni.isaac.dynamic_control.franka_articulation.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-omni.isaac.dynamic_control.franka_articulation.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.asset.importer.urdf.urdf_import.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.asset.importer.urdf.urdf_import.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.asset.importer.mjcf.mjcf_import.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.asset.importer.mjcf.mjcf_import.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.infinigen_sdg_default.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.infinigen_sdg_default.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.infinigen_sdg_config.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.infinigen_sdg_config.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.scene_based_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.scene_based_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.scene_based_sdg_basic_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.scene_based_sdg_basic_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.scene_based_sdg_default_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.scene_based_sdg_default_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.scene_based_sdg_kitti_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.scene_based_sdg_kitti_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.scene_based_sdg_coco_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.scene_based_sdg_coco_writer.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.pose_generation.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.pose_generation.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.pose_generation_ycbvideo.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.pose_generation_ycbvideo.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.pose_generation_ycbvideo_output_check.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.pose_generation_ycbvideo_output_check.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.pose_generation_dope.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.pose_generation_dope.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.pose_generation_dope_output_check.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.pose_generation_dope_output_check.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.object_based_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.object_based_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.object_based_sdg_config.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.object_based_sdg_config.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.object_based_sdg_config_dope.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.object_based_sdg_config_dope.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.object_based_sdg_config_centerpose.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.object_based_sdg_config_centerpose.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.writer_augmentation_numpy.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.writer_augmentation_numpy.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.writer_augmentation_warp.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.writer_augmentation_warp.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.annotator_augmentation_numpy.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.annotator_augmentation_numpy.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.annotator_augmentation_warp.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.annotator_augmentation_warp.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.amr_navigation.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.amr_navigation.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.amr_navigation_use_temp_rp.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.amr_navigation_use_temp_rp.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-replicator.cosmos_writer_warehouse.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-replicator.cosmos_writer_warehouse.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.hello_world.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.hello_world.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_time_stepping.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_time_stepping.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_articulation_root.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_articulation_root.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_fabric_frame_delay.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_fabric_frame_delay.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_rendering.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_rendering.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_save_stage.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_save_stage.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_delete_in_contact.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_delete_in_contact.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.test_articulation_determinism.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.test_articulation_determinism.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-omni.isaac.dynamic_control.test_zero_step.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-omni.isaac.dynamic_control.test_zero_step.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.ros2.bridge.enable_extension.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.ros2.bridge.enable_extension.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_carter_camera_multi_robot_nav.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_carter_camera_multi_robot_nav.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_people_sim.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_people_sim.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_camera_tf_delay.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_camera_tf_delay.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_publish_camera_data.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.ros2.bridge.test_publish_camera_data.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_extra_args.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_extra_args.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_frame_delay_basic.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_frame_delay_basic.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_frame_delay_under_load.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_frame_delay_under_load.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_ogn.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_ogn.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_syntheticdata.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_syntheticdata.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_fetch_results.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_fetch_results.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_unsaved_on_exit.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_unsaved_on_exit.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.benchmark.services.test_no_rendering.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.benchmark.services.test_no_rendering.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_external.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_external.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.cortex.framework.bringup.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.cortex.framework.bringup.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.core.api.tensor_api_handles.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.core.api.tensor_api_handles.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.behavior.behaviors.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.behavior.behaviors.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.cosmos_writer_simple.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.cosmos_writer_simple.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.custom_event_and_write.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.custom_event_and_write.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.replicator.examples.ar_capture_pipeline.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.replicator.examples.ar_capture_pipeline.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.replicator.examples.ar_capture_pipeline_gpu.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.replicator.examples.ar_capture_pipeline_gpu.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.replicator.examples.motion_blur_short.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.replicator.examples.motion_blur_short.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.subscribers_and_events.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.subscribers_and_events.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.custom_fps_writer_annotator.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.custom_fps_writer_annotator.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_01.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_01.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_02.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_02.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_03.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_03.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_04.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.sdg_getting_started_04.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.simready_assets_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.simready_assets_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.multi_camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.multi_camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.examples.simulation_get_data.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.examples.simulation_get_data.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.replicator.grasping.grasping_workflow_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.replicator.grasping.grasping_workflow_sdg.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.sensors.physics.contact_sensor.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.sensors.physics.contact_sensor.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-isaacsim.sensors.camera.camera_annotator_device.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-isaacsim.sensors.camera.camera_annotator_device.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-python_sh.import_torch.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-python_sh.import_torch.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-python_sh.import_scipy.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-python_sh.import_scipy.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-python_sh.path_length.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-python_sh.path_length.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-python_sh.import_sys.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-python_sh.import_sys.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-omni.syntheticdata.test_basic.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-omni.syntheticdata.test_basic.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-omni.replicator.agent.test_scripting.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-omni.replicator.agent.test_scripting.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-tutorials-getting_started.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-tutorials-getting_started.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-tutorials-getting_started_robot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-tutorials-getting_started_robot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-nativepython-testing-isaacsim.simulation_app.test_ovd.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-nativepython-testing-isaacsim.simulation_app.test_ovd.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_camera.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_robots_nova_carter_ros2.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_robots_nova_carter_ros2.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_robots_nova_carter.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_robots_nova_carter.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_rtx_lidar_rotary.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_rtx_lidar_rotary.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_rtx_lidar_solid_state.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_rtx_lidar_solid_state.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_sdg_simple.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_sdg_simple.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_sdg_advanced.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_sdg_advanced.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_robots_ur10.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_robots_ur10.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_physx_lidar.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_physx_lidar.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_robots_o3dyn.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_robots_o3dyn.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_scene_loading.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_scene_loading.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_robots_evobot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_robots_evobot.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_single_view_depth_sensor.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_single_view_depth_sensor.sh
/home/gotree94/isaacsim/_build/linux-x86_64/debug/tests/tests-standalone_benchmarks-benchmark_robots_humanoid.sh
/home/gotree94/isaacsim/_build/linux-x86_64/release/tests/tests-standalone_benchmarks-benchmark_robots_humanoid.sh
Building configurations...
Running action 'gmake2'...
Done (1010ms).
>>> Stage Files Step. Doing file copy and folder linking.
>>> File doesn't exist: /home/gotree94/isaacsim/prebuild.toml. Skipping.
>>> Processing file: /home/gotree94/isaacsim/_build/generated/prebuild.toml
>>> VS Code setup. Writing: /home/gotree94/isaacsim/_build/linux-x86_64/release/setup_python_env.sh
>>> Custom Pre-Build Step. Running '/home/gotree94/isaacsim/repo.sh precache_exts -c release'...
Script dir: /home/gotree94/isaacsim
Setting env var: OMNI_TRUSTED_CERTIFICATE=ALL
running kit for app precache, cmd: /home/gotree94/isaacsim/_build/linux-x86_64/release/kit/kit /home/gotree94/isaacsim/_build/linux-x86_64/release/apps/isaacsim.exp.extscache.kit --allow-root --portable --ext-precache-mode --/crashreporter/gatherUserStory=0 --/app/settings/persistent=0 --/app/settings/loadUserConfig=0 --/app/extensions/generateVersionLock=1 --/app/extensions/parallelPullEnabled=1 --/app/enableStdoutOutput=1 --/app/extensions/detailedSolverExplanation=1 --/app/extensions/registryEnabled=1 --/app/extensions/mkdirExtFolders=0 --/app/extensions/registryCacheFull='/home/gotree94/isaacsim/_build/linux-x86_64/release/extscache' --/log/flushStandardStreamOutput=1 --/exts/omni.kit.registry.nucleus/registries/0/name="kit/default" --/exts/omni.kit.registry.nucleus/registries/0/url="omniverse://kit-extensions.ov.nvidia.com/exts/kit/default" --/exts/omni.kit.registry.nucleus/registries/1/name="kit/sdk" --/exts/omni.kit.registry.nucleus/registries/1/url="omniverse://kit-extensions.ov.nvidia.com/exts/kit/sdk/${kit_version_short}/${kit_git_hash}" --/app/extensions/target/config=release --ext-folder /home/gotree94/isaacsim/_build/linux-x86_64/release/exts --ext-folder /home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated
[Info] [carb] Logging to file: /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/logs/Kit/isaacsim.exp.extscache/0.0/kit_20260521_105500.log
*** Building release ***
Build arguments: ['make', '--directory=/home/gotree94/isaacsim/_compiler/gmake2', '--stop', 'config=release_x86_64', '-j14', '--output-sync']
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building omni.isaac.dynamic_control.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.manipulators.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.utils.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.writers.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.physx.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.physx.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.importer.urdf.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.importer.urdf.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.physics.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.physics.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.cloner.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.includes.tests (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.examples.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.api.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.nodes.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.nodes.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.tf_viewer.humble (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.tf_viewer.jazzy (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.tf_viewer.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.tf_viewer.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.surface_gripper.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.surface_gripper.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.gen.conveyor.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.wheeled_robots.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.wheeled_robots.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.importer.mjcf.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.importer.mjcf.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.check (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.humble (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.jazzy (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.backend_tests (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building omni.kit.loop-isaac.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building omni.kit.loop-isaac.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.gen.omap.generator (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.simulation_manager.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.mobility_gen (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.rtx.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.domain_randomization.ogn (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building omni.isaac.dynamic_control.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.writers (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.physx.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.physics.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.examples (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.nodes.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.surface_gripper.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.gen.conveyor.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.gen.conveyor.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.robot.wheeled_robots.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.ros2.bridge.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.rtx.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.sensors.rtx.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.replicator.domain_randomization (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.gen.omap.plugin (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.asset.gen.omap.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
make: Entering directory '/home/gotree94/isaacsim/_compiler/gmake2'
==== Building isaacsim.core.simulation_manager.python (release_x86_64) ====
make: Leaving directory '/home/gotree94/isaacsim/_compiler/gmake2'
>>> Custom Post-Build Step. Running '/home/gotree94/isaacsim/repo.sh generate_vscode_settings -c release'...
Script dir: /home/gotree94/isaacsim
>>> VS Code setup. Writing: /home/gotree94/isaacsim/_build/linux-x86_64/release/setup_python_env.sh
>>> VS Code setup. Writing: /home/gotree94/isaacsim//.vscode/settings.json
>>> VS Code setup. Writing: /home/gotree94/isaacsim/_build/linux-x86_64/release/setup_python_env.sh
>>> VS Code setup. Writing: /home/gotree94/isaacsim/_build/linux-x86_64/release/.vscode/settings.json
>>> Custom Post-Build Step. Running '/home/gotree94/isaacsim/repo.sh edit_sysconfig -c release'...
Script dir: /home/gotree94/isaacsim
Processing sysconfig file: /home/gotree94/isaacsim/_build/linux-x86_64/release/kit/python/lib/python3.11/_sysconfigdata__linux_x86_64-linux-gnu.py
File already contains Isaac Sim modifications, skipping
>>> Custom Post-Build Step. Running '/home/gotree94/isaacsim/repo.sh usd -c release'...
Script dir: /home/gotree94/isaacsim
/home/gotree94/isaacsim/_build/target-deps/python/python: No module named jinja2
Collecting jinja2==3.1.4 (from -r /home/gotree94/.cache/packman/chk/repo_usd/5.0.12/omni/repo/usd/../../../requirements-usdGenSchema.txt (line 1))
  Using cached jinja2-3.1.4-py3-none-any.whl (133 kB)
Collecting markupsafe==2.1.5 (from -r /home/gotree94/.cache/packman/chk/repo_usd/5.0.12/omni/repo/usd/../../../requirements-usdGenSchema.txt (line 4))
  Using cached MarkupSafe-2.1.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (28 kB)
Installing collected packages: markupsafe, jinja2
Successfully installed jinja2-3.1.4 markupsafe-2.1.5
WARNING: Target directory /home/gotree94/isaacsim/_build/repo_usd/packages/jinja2-3.1.4.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory /home/gotree94/isaacsim/_build/repo_usd/packages/markupsafe already exists. Specify --upgrade to force replacement.
WARNING: Target directory /home/gotree94/isaacsim/_build/repo_usd/packages/MarkupSafe-2.1.5.dist-info already exists. Specify --upgrade to force replacement.
WARNING: Target directory /home/gotree94/isaacsim/_build/repo_usd/packages/jinja2 already exists. Specify --upgrade to force replacement.

[notice] A new release of pip is available: 24.3.1 -> 26.1.1
[notice] To update, run: /home/gotree94/isaacsim/_build/target-deps/python/python -m pip install --upgrade pip
#################################################################################################
#  USD_DISABLE_PRIM_DEFINITIONS_FOR_USDGENSCHEMA is overridden to 'true'.  Default is 'false'.  #
#################################################################################################
Processing schema classes:
IsaacRobotAPI, IsaacLinkAPI, IsaacReferencePointAPI, IsaacJointAPI, IsaacSurfaceGripper, IsaacAttachmentPointAPI
Loading Templates from /home/gotree94/.cache/packman/chk/usd.py311.manylinux_2_35_x86_64.stock.release/0.24.05.kit.7-gl.16400+05f48f24/lib/usd/usd/resources/codegenTemplates
	unchanged /home/gotree94/isaacsim/source/extensions/isaacsim.robot.schema/robot_schema/plugInfo.json
Generating Schematics:
	unchanged /home/gotree94/isaacsim/source/extensions/isaacsim.robot.schema/robot_schema/generatedSchema.usda
BUILD (RELEASE) SUCCEEDED (Took 8.55 seconds)
(base) gotree94@gotree94-ROG-Strix-SCAR-16-G635LX-G635LX:~/isaacsim$ 


```
---

## 4. 실행

```bash
cd /home/gotree94/isaacsim

./isaac-sim.sh                          # GUI 실행
./isaac-sim.sh --no-window              # Headless (RAM 절약)
./python.sh my_script.py                # Python 스크립트
./isaac-sim.compatibility_check.sh      # 호환성 진단
```

---

## 5. RAM 24GB → SWAP 설정 (필수)

```bash
sudo fallocate -l 32G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 6. 문제 해결

| 증상 | 원인 / 해결 |
|---|---|
| `git: 'lfs' is not a git command` | git-lfs 미설치 → `sudo apt install git-lfs` |
| `$'\r': command not found` | CRLF 개행문자 → `sed -i 's/\r$//' tools/packman/packman` |
| `GCC` 버전 에러 | `gcc --version` 11 확인, update-alternatives 실행 |
| 빌드 중 `killed` (OOM) | RAM 부족 → SWAP 설정 필수 (5번) |
| `nvidia-smi` 실행 안 됨 | 드라이버 미설치 → 2번 실행 |
| `libEGL` / Vulkan 에러 | `sudo apt install libegl1 libvulkan1` |
| OpenGL/X11 에러 (노트북) | `sudo prime-select nvidia` |

---

## 7. 링크

- 공식 문서: https://docs.isaacsim.omniverse.nvidia.com/5.1.0/
- GitHub: https://github.com/isaac-sim/IsaacSim
