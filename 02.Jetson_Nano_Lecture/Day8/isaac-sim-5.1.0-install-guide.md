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

```
(base) gotree94@gotree94-ROG-Strix-SCAR-16-G635LX-G635LX:~/isaacsim$ ./_build/linux-x86_64/release/isaac-sim.sh
[Info] [carb] Logging to file: /home/gotree94/.nvidia-omniverse/logs/Kit/Isaac-Sim Full/5.1/kit_20260521_105743.log
[0.129s] [ext: omni.kit.async_engine-0.0.3] startup
[0.407s] [ext: omni.metrics.core-0.0.3] startup
[0.407s] [ext: omni.client.lib-1.1.0] startup
[0.435s] [ext: omni.blobkey-1.1.2] startup
[0.436s] [ext: omni.stats-1.0.1] startup
[0.436s] [ext: omni.datastore-0.0.0] startup
[0.440s] [ext: omni.client-1.3.0] startup
[0.449s] [ext: omni.ujitso.default-1.0.0] startup
[0.451s] [ext: omni.hsscclient-1.1.2] startup
[0.453s] [ext: omni.gpu_foundation.shadercache.vulkan-1.0.0] startup
[0.457s] [ext: omni.assets.plugins-0.0.0] startup
[0.457s] [ext: omni.gpu_foundation-0.0.0] startup
[0.464s] [ext: carb.windowing.plugins-1.0.0] startup
[0.473s] [ext: omni.kit.renderer.init-0.0.0] startup
MESA: warning: Driver does not support the 0x7d67 PCI ID.
MESA: warning: Driver does not support the 0x7d67 PCI ID.

|---------------------------------------------------------------------------------------------|
| Driver Version: 580.126.09    | Graphics API: Vulkan
|=============================================================================================|
| GPU | Name                             | Active | LDA | GPU Memory | Vendor-ID | LUID       |
|     |                                  |        |     |            | Device-ID | UUID       |
|     |                                  |        |     |            | Bus-ID    |            |
|---------------------------------------------------------------------------------------------|
| 0   | NVIDIA GeForce RTX 5090 Laptop.. | Yes: 0 |     | 24463   MB | 10de      | 0          |
|     |                                  |        |     |            | 2c58      | 8b55332d.. |
|     |                                  |        |     |            | 2         |            |
|=============================================================================================|
| OS: 22.04.5 LTS (Jammy Jellyfish) ubuntu, Version: 22.04.5, Kernel: 6.8.0-94-generic
| XServer Vendor: The X.Org Foundation, XServer Version: 12101004 (1.21.1.4)
| Processor: Intel(R) Core(TM) Ultra 9 275HX
| Cores: 24 | Logical Cores: 24
|---------------------------------------------------------------------------------------------|
| Total Memory (MB): 63646 | Free Memory: 59665
| Total Page/Swap (MB): 30517 | Free Page/Swap: 30516
|---------------------------------------------------------------------------------------------|
2026-05-21T01:57:44Z [1,123ms] [Warning] [gpu.foundation.plugin] CPU performance profile is set to powersave. This profile sets the CPU to the lowest frequency reducing performance.
2026-05-21T01:57:44Z [1,135ms] [Warning] [gpu.foundation.plugin] PCIe link width current (8) and maximum (16) for device 0 don't match.
2026-05-21T01:57:44Z [1,135ms] [Warning] [gpu.foundation.plugin] IOMMU is enabled.
[1.329s] [ext: omni.kit.pipapi-0.0.0] startup
[1.332s] [ext: omni.kit.pip_archive-0.0.0] startup
[1.332s] [ext: omni.pip.compute-1.6.3] startup
[1.332s] [ext: omni.materialx.libs-1.0.7] startup
[1.338s] [ext: omni.pip.cloud-1.4.3] startup
[1.341s] [ext: omni.isaac.core_archive-3.0.0] startup
[1.341s] [ext: omni.usd.config-1.0.6] startup
[1.345s] [ext: omni.gpucompute.plugins-0.0.0] startup
[1.345s] [ext: omni.usd.libs-1.0.1] startup
[1.391s] [ext: omni.services.pip_archive-0.16.0] startup
[1.391s] [ext: omni.mdl-56.0.3] startup
[1.570s] [ext: omni.iray.libs-0.0.0] startup
[1.576s] [ext: omni.mdl.neuraylib-0.2.12] startup
[1.581s] [ext: omni.kit.usd.mdl-1.1.5] startup
[1.640s] [ext: omni.isaac.ml_archive-3.0.4] startup
[1.641s] [ext: omni.kit.loop-isaac-1.3.7] startup
[1.642s] [ext: omni.kit.test-2.0.1] startup
[1.747s] [ext: omni.kit.telemetry-0.5.2] startup
[1.771s] [ext: omni.appwindow-1.1.10] startup
[1.796s] [ext: omni.kit.renderer.core-1.1.0] startup
[1.877s] [ext: omni.kit.renderer.capture-0.0.0] startup
[1.879s] [ext: omni.kit.renderer.imgui-2.0.5] startup
[1.975s] [ext: omni.ui-2.27.1] startup
[1.985s] [ext: omni.kit.mainwindow-1.0.3] startup
[1.986s] [ext: carb.audio-0.1.0] startup
[1.988s] [ext: omni.uiaudio-1.0.0] startup
[1.989s] [ext: omni.kit.uiapp-0.0.0] startup
[1.989s] [ext: omni.usd.schema.metrics.assembler-107.3.1] startup
[1.990s] [ext: omni.usd.schema.audio-0.0.0] startup
[1.993s] [ext: omni.usd.schema.omniscripting-1.0.0] startup
[1.996s] [ext: omni.usd.schema.isaac-3.0.5] startup
[1.996s] [ext: omni.anim.graph.schema-107.3.3] startup
[2.002s] [ext: omni.usd.schema.semantics-0.0.0] startup
[2.004s] [ext: omni.usd.schema.omnigraph-1.0.0] startup
[2.007s] [ext: omni.usd.schema.anim-0.0.0] startup
[2.016s] [ext: omni.usd.schema.geospatial-0.0.0] startup
[2.018s] [ext: omni.kit.window.popup_dialog-2.0.24] startup
[2.030s] [ext: omni.activity.core-1.0.3] startup
[2.031s] [ext: omni.kit.widget.nucleus_connector-2.0.1] startup
[2.036s] [ext: omni.usd_resolver-1.0.0] startup
[2.038s] [ext: omni.kit.usd_undo-0.1.8] startup
[2.039s] [ext: omni.graph.exec-0.9.6] startup
[2.039s] [ext: omni.usd.core-1.5.3] startup
[2.041s] [ext: omni.kit.actions.core-1.0.0] startup
[2.043s] [ext: omni.resourcemonitor-107.0.1] startup
[2.045s] [ext: omni.kit.exec.core-0.13.4] startup
[2.046s] [ext: usdrt.scenegraph-7.6.1] startup
[2.070s] [ext: omni.timeline-1.0.14] startup
[2.071s] [ext: omni.kit.commands-1.4.10] startup
[2.077s] [ext: omni.kit.audiodeviceenum-1.0.2] startup
[2.079s] [ext: omni.hydra.usdrt_delegate-7.5.1] startup
[2.083s] [ext: omni.hydra.scene_delegate-0.3.4] startup
[2.085s] [ext: omni.usd-1.13.10] startup
[2.149s] [ext: omni.inspect-1.0.2] startup
[2.150s] [ext: omni.kit.notification_manager-1.0.10] startup
[2.159s] [ext: omni.graph.core-2.184.5] startup
[2.161s] [ext: isaacsim.core.deprecation_manager-0.2.7] startup
[2.163s] [ext: omni.usd.schema.flow-107.1.1] startup
[2.164s] [ext: omni.usd.schema.omni_lens_distortion-0.0.0] startup
[2.164s] [ext: omni.anim.navigation.schema-107.3.3] startup
[2.166s] [ext: isaacsim.robot.schema-3.6.0] startup
[2.172s] [ext: omni.usd.schema.scene.visualization-2.0.2] startup
[2.173s] [ext: omni.usd.schema.omni_sensors-0.0.0] startup
[2.174s] [ext: omni.kit.asset_converter-5.0.17] startup
[2.183s] [ext: omni.usd.schema.render_settings.rtx-0.0.0] startup
[2.184s] [ext: omni.usd.schema.physx-107.3.26] startup
[2.203s] [ext: omni.kit.collaboration.telemetry-1.1.0] startup
[2.204s] [ext: omni.volume-0.5.2] startup
[2.205s] [ext: omni.kit.manipulator.selector-1.1.3] startup
[2.207s] [ext: omni.kit.collaboration.channel_manager-1.0.14] startup
[2.210s] [ext: omni.kit.menu.core-1.1.2] startup
[2.212s] [ext: omni.kit.usd.layers-2.2.11] startup
[2.228s] [ext: omni.kit.menu.utils-2.0.5] startup
[2.246s] [ext: omni.ui.scene-1.11.5] startup
[2.248s] [ext: omni.kit.primitive.mesh-1.0.17] startup
[2.257s] [ext: omni.kit.manipulator.viewport-107.0.1] startup
[2.258s] [ext: omni.fabric.commands-1.1.6] startup
[2.265s] [ext: omni.kit.helper.file_utils-0.1.9] startup
[2.268s] [ext: omni.kit.widget.nucleus_info-2.0.2] startup
[2.269s] [ext: omni.kit.widget.filebrowser-2.12.3] startup
[2.285s] [ext: omni.kit.search_core-1.0.8] startup
[2.286s] [ext: omni.kit.widget.options_menu-1.1.6] startup
[2.292s] [ext: omni.kit.widget.search_delegate-1.0.7] startup
[2.294s] [ext: omni.kit.widget.path_field-2.0.11] startup
[2.297s] [ext: omni.kit.widget.options_button-1.0.3] startup
[2.298s] [ext: omni.index.libs-380600.8087.0] startup
[2.298s] [ext: omni.kit.widget.browser_bar-2.0.10] startup
[2.300s] [ext: omni.kit.widget.context_menu-1.2.5] startup
[2.302s] [ext: omni.index-1.0.1] startup
[2.303s] [ext: omni.ujitso.client-0.0.0] startup
[2.303s] [ext: omni.hydra.rtx.shadercache.vulkan-1.0.0] startup
[2.304s] [ext: omni.kit.widget.versioning-1.4.10] startup
[2.309s] [ext: omni.kit.clipboard-1.0.5] startup
[2.311s] [ext: omni.hydra.rtx-1.0.0] startup
2026-05-21T01:57:45Z [2,270ms] [Warning] [omni.log] Source: omni.hydra was already registered.
[2.329s] [ext: omni.kit.window.filepicker-2.13.4] startup
[2.375s] [ext: omni.kit.context_menu-1.8.6] startup
[2.380s] [ext: omni.kit.viewport.scene_camera_model-1.0.6] startup
[2.383s] [ext: omni.kit.hydra_texture-1.4.6] startup
[2.385s] [ext: omni.kit.window.file_importer-1.1.18] startup
[2.389s] [ext: omni.kit.viewport.legacy_gizmos-1.0.19] startup
[2.391s] [ext: omni.kit.raycast.query-1.1.0] startup
[2.394s] [ext: omni.kit.material.library-2.0.7] startup
[2.409s] [ext: omni.kit.widget.viewport-107.1.3] startup
[2.420s] [ext: omni.kit.widget.searchable_combobox-1.0.6] startup
[2.422s] [ext: omni.kit.window.drop_support-1.0.5] startup
[2.423s] [ext: omni.kit.viewport.registry-104.0.6] startup
[2.424s] [ext: omni.hydra.engine.stats-1.0.3] startup
[2.425s] [ext: omni.kit.widget.settings-1.2.6] startup
[2.431s] [ext: omni.kit.viewport.window-107.2.0] startup
[2.461s] [ext: omni.kit.window.preferences-1.8.0] startup
[2.480s] [ext: omni.kit.widget.toolbar-2.0.1] startup
[2.491s] [ext: omni.kit.viewport.utility-1.1.2] startup
[2.493s] [ext: omni.kit.manipulator.transform-107.0.0] startup
[2.504s] [ext: omni.kit.widget.prompt-1.0.7] startup
[2.506s] [ext: omni.kit.manipulator.tool.snap-1.5.13] startup
[2.513s] [ext: omni.kit.widget.live_session_management.ui-1.0.3] startup
[2.519s] [ext: omni.kit.viewport.manipulator.transform-107.0.4] startup
[2.522s] [ext: omni.kit.collaboration.presence_layer-1.1.2] startup
[2.528s] [ext: omni.kit.manipulator.prim.core-107.0.8] startup
[2.541s] [ext: omni.kit.property.adapter.core-1.0.2] startup
[2.543s] [ext: omni.kit.manipulator.prim.fabric-107.0.4] startup
[2.546s] [ext: omni.kit.widget.live_session_management-1.2.23] startup
[2.552s] [ext: omni.kit.property.adapter.usd-1.0.2] startup
[2.553s] [ext: omni.kit.manipulator.prim.usd-107.0.3] startup
[2.555s] [ext: omni.kit.property.adapter.fabric-1.0.3] startup
[2.558s] [ext: omni.kit.manipulator.prim-107.0.0] startup
[2.558s] [ext: omni.kit.window.content_browser_registry-0.0.6] startup
[2.559s] [ext: omni.kit.widget.filter-1.1.4] startup
[2.560s] [ext: omni.kit.window.file_exporter-1.0.33] startup
[2.562s] [ext: omni.kit.stage_template.core-1.1.22] startup
[2.563s] [ext: omni.kit.widget.searchfield-1.1.8] startup
[2.566s] [ext: omni.kit.widget.highlight_label-1.0.3] startup
[2.567s] [ext: omni.kit.window.file-2.0.5] startup
[2.575s] [ext: omni.kit.hotkeys.core-1.3.10] startup
[2.576s] [ext: omni.kit.window.property-1.12.1] startup
[2.581s] [ext: omni.kit.window.content_browser-3.1.3] startup
[2.594s] [ext: omni.kit.widget.stage-3.1.4] startup
[2.622s] [ext: omni.convexdecomposition-107.3.26] startup
[2.624s] [ext: omni.kit.property.usd-4.5.12] startup
[2.666s] [ext: omni.kit.manipulator.selection-106.0.1] startup
[2.668s] [ext: omni.kvdb-107.3.26] startup
[2.670s] [ext: omni.usdphysics-107.3.26] startup
[2.671s] [ext: omni.physx.foundation-107.3.26] startup
[2.672s] [ext: omni.localcache-107.3.26] startup
[2.673s] [ext: omni.debugdraw-0.1.4] startup
[2.675s] [ext: omni.physx.cooking-107.3.26] startup
[2.677s] [ext: omni.physics-107.3.26] startup
[2.679s] [ext: omni.physx-107.3.26] startup
[2.688s] [ext: omni.physics.stageupdate-107.3.26] startup
[2.690s] [ext: omni.physics.physx-107.3.26] startup
2026-05-21T01:57:46Z [2,640ms] [Warning] [carb] Acquiring non optional plugin interface which is not listed as dependency: [omni::physx::IPhysxBenchmarks v1.0] (plugin: <default plugin>), by client: omni.physics.physx.plugin. Add it to CARB_PLUGIN_IMPL_DEPS() macro of a client.
[2.691s] [ext: omni.kit.numpy.common-0.1.3] startup
[2.692s] [ext: omni.kit.window.cursor-1.1.4] startup
[2.693s] [ext: omni.isaac.dynamic_control-2.0.7] startup
2026-05-21T01:57:46Z [2,645ms] [Warning] [omni.isaac.dynamic_control] omni.isaac.dynamic_control is deprecated as of Isaac Sim 4.5. No action is needed from end-users.
[2.697s] [ext: omni.kit.viewport.menubar.core-107.2.1] startup
[2.721s] [ext: omni.kit.viewport.actions-107.0.2] startup
[2.726s] [ext: isaacsim.core.version-2.0.6] startup
[2.727s] [ext: omni.kit.widget.layers-1.8.6] startup
[2.755s] [ext: omni.kit.viewport.menubar.display-107.0.3] startup
[2.757s] [ext: isaacsim.storage.native-1.5.1] startup
[2.761s] [ext: omni.usdphysics.ui-107.3.26] startup
[2.798s] [ext: omni.physx.commands-107.3.26] startup
[2.824s] [ext: omni.graph.tools-1.79.2] startup
[2.882s] [ext: omni.usd.metrics.assembler-107.3.1] startup
[2.887s] [ext: omni.physx.ui-107.3.26] startup
[2.946s] [ext: omni.physics.tensors-107.3.26] startup
[2.957s] [ext: omni.warp.core-1.8.2] startup
[3.147s] [ext: omni.usd.metrics.assembler.physics-107.3.26] startup
[3.153s] [ext: omni.kit.widget.text_editor-1.1.1] startup
[3.154s] [ext: omni.physx.tensors-107.3.26] startup
[3.158s] [ext: isaacsim.core.utils-3.5.1] startup
[3.162s] [ext: omni.graph-1.141.2] startup
[3.234s] [ext: omni.ui_query-1.1.8] startup
[3.236s] [ext: omni.kit.window.extensions-1.4.27] startup
[3.258s] [ext: isaacsim.core.simulation_manager-1.4.4] startup
2026-05-21T01:57:46Z [3,428ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.simulation_manager. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:46Z [3,428ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.simulation_manager' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:46Z [3,428ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.simulation_manager-1.4.4] Failed to startup python extension.
[3.541s] [ext: omni.kit.widget.graph-2.0.0] startup
[3.562s] [ext: omni.graph.image.core-0.6.1] startup
[3.563s] [ext: isaacsim.core.prims-0.6.1] startup
2026-05-21T01:57:47Z [3,533ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.prims. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/articulation.py", line 27, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:47Z [3,533ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.prims' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:47Z [3,533ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.prims-0.6.1] Failed to startup python extension.
[3.645s] [ext: omni.kit.stage_templates-2.0.0] startup
[3.652s] [ext: omni.kit.graph.delegate.default-1.2.3] startup
[3.653s] [ext: omni.graph.image.nodes-1.3.1] startup
[3.654s] [ext: omni.graph.action_core-1.1.7] startup
[3.655s] [ext: isaacsim.core.api-4.8.0] startup
2026-05-21T01:57:47Z [3,620ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.api. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/__init__.py", line 17, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/__init__.py", line 15, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/physics_context.py", line 20, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:47Z [3,620ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.api' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:47Z [3,620ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.api-4.8.0] Failed to startup python extension.
[3.732s] [ext: omni.kit.graph.editor.core-1.5.3] startup
[3.742s] [ext: omni.syntheticdata-0.6.13] startup
[3.778s] [ext: omni.graph.ui-1.101.6] startup
[3.844s] [ext: omni.kit.widget.material_preview-1.0.16] startup
[3.849s] [ext: omni.kit.graph.usd.commands-1.3.1] startup
[3.851s] [ext: omni.videoencoding-0.1.2] startup
[3.853s] [ext: omni.graph.action_nodes-1.50.4] startup
[3.855s] [ext: omni.kit.window.material_graph-1.9.1] startup
[3.882s] [ext: omni.graph.nodes-1.170.10] startup
[3.894s] [ext: omni.graph.action-1.130.0] startup
[3.904s] [ext: omni.kit.ui_test-1.3.7] startup
[3.938s] [ext: omni.graph.visualization.nodes-2.1.3] startup
[3.978s] [ext: omni.graph.ui_nodes-1.50.5] startup
[3.982s] [ext: omni.kit.selection-0.1.6] startup
[3.991s] [ext: omni.warp-1.8.2] startup
[4.005s] [ext: isaacsim.gui.components-1.2.1] startup
[4.038s] [ext: isaacsim.gui.menu-2.4.4] startup
2026-05-21T01:57:47Z [4,066ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.gui.menu. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.gui.menu/isaacsim/gui/menu/__init__.py", line 16, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.gui.menu/isaacsim/gui/menu/extension.py", line 22, in <module>
    from .create_menu import CreateMenuExtension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.gui.menu/isaacsim/gui/menu/create_menu.py", line 23, in <module>
    from isaacsim.core.utils.viewports import set_camera_view
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/viewports.py", line 25, in <module>
    from isaacsim.core.utils.prims import is_prim_path_valid, set_prim_hide_in_stage_window, set_prim_no_delete
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 18, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:47Z [4,066ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.gui.menu' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.gui.menu' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:47Z [4,067ms] [Error] [omni.ext.plugin] [ext: isaacsim.gui.menu-2.4.4] Failed to startup python extension.
[4.137s] [ext: omni.graph.scriptnode-1.50.0] startup
[4.149s] [ext: isaacsim.test.docstring-1.1.0] startup
[4.193s] [ext: isaacsim.core.experimental.utils-0.3.0] startup
2026-05-21T01:57:47Z [4,163ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
[4.215s] [ext: omni.replicator.core-1.12.27] startup
2026-05-21T01:57:47Z [4,211ms] [Warning] [pxr.Semantics] pxr.Semantics is deprecated - please use Semantics instead
Warp 1.8.2 initialized:
   CUDA Toolkit 12.8, Driver 13.0
   Devices:
     "cpu"      : "x86_64"
     "cuda:0"   : "NVIDIA GeForce RTX 5090 Laptop GPU" (23 GiB, sm_120, mempool enabled)
   Kernel cache:
     /home/gotree94/.cache/warp/1.8.2
2026-05-21T01:57:47Z [4,354ms] [Warning] [omni.graph.core.plugin] Found duplicate of category 'Replicator' - was 'Annotators', adding 'Fabric Reader'
2026-05-21T01:57:47Z [4,354ms] [Warning] [omni.graph.core.plugin] Category 'Replicator' not accepted on node type 'omni.replicator.core.FabricReader' in extension 'omni.replicator.core'
2026-05-21T01:57:47Z [4,355ms] [Warning] [omni.replicator.core.scripts.extension] No material configuration file, adding configuration to material settings directly.
[4.408s] [ext: isaacsim.core.experimental.prims-0.8.1] startup
2026-05-21T01:57:47Z [4,432ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.experimental.prims. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/articulation.py", line 32, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:47Z [4,432ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.experimental.prims' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:47Z [4,432ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.experimental.prims-0.8.1] Failed to startup python extension.
[4.490s] [ext: isaacsim.core.nodes-3.4.3] startup
2026-05-21T01:57:48Z [4,496ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.nodes. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.nodes/isaacsim/core/nodes/__init__.py", line 15, in <module>
    from .impl import BaseResetNode, BaseWriterNode, Extension, WriterRequest
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.nodes/isaacsim/core/nodes/impl/__init__.py", line 24, in <module>
    from .extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.nodes/isaacsim/core/nodes/impl/extension.py", line 22, in <module>
    from isaacsim.core.nodes.scripts.utils import register_annotator_from_node_with_telemetry
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.nodes/isaacsim/core/nodes/scripts/utils.py", line 19, in <module>
    from isaacsim.core.utils.prims import set_targets
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 18, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:48Z [4,496ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.nodes' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.nodes' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [4,496ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.nodes-3.4.3] Failed to startup python extension.
[4.553s] [ext: isaacsim.robot.surface_gripper-3.3.1] startup
2026-05-21T01:57:48Z [4,602ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:48Z [4,623ms] [Error] [omni.ext._impl._internal] Failed to import python module isaacsim.robot.surface_gripper from /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper. Error: module 'torch' has no attribute 'jit'. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 196, in _custom_importer
    return _import_public(ext_module.path, ext_module.name, reload_enabled)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 103, in _import_public
    module = import_module(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/__init__.py", line 17, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/impl/__init__.py", line 18, in <module>
    from .gripper_view import GripperView
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/impl/gripper_view.py", line 22, in <module>
    from isaacsim.core.experimental.prims import XformPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/articulation.py", line 32, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 23, in <module>
    @torch.jit.script
     ^^^^^^^^^
AttributeError: module 'torch' has no attribute 'jit'

2026-05-21T01:57:48Z [4,623ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.robot.surface_gripper' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [4,623ms] [Error] [omni.ext.plugin] [ext: isaacsim.robot.surface_gripper-3.3.1] Failed to startup python extension.
[4.789s] [ext: isaacsim.sensors.camera-1.3.6] startup
Warp DeprecationWarning: The `warp.sim` module is deprecated and will be removed in v1.10. Please transition to using the forthcoming Newton library instead.
2026-05-21T01:57:48Z [4,983ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: cannot import name 'torch' from 'isaacsim.core.utils' (/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/__init__.py)
2026-05-21T01:57:48Z [4,984ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.sensors.camera. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.camera/isaacsim/sensors/camera/__init__.py", line 16, in <module>
    from .camera import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.camera/isaacsim/sensors/camera/camera.py", line 23, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:48Z [4,984ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.sensors.camera' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.camera' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [4,985ms] [Error] [omni.ext.plugin] [ext: isaacsim.sensors.camera-1.3.6] Failed to startup python extension.
[5.075s] [ext: isaacsim.robot.surface_gripper.ui-3.0.2] startup
2026-05-21T01:57:48Z [5,067ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:48Z [5,067ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.robot.surface_gripper.ui. Error: cannot import name 'torch' from 'isaacsim.core.utils' (/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/__init__.py). Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1126, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/__init__.py", line 17, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/impl/__init__.py", line 18, in <module>
    from .gripper_view import GripperView
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/impl/gripper_view.py", line 22, in <module>
    from isaacsim.core.experimental.prims import XformPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/articulation.py", line 32, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
ImportError: cannot import name 'torch' from 'isaacsim.core.utils' (/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/__init__.py)

2026-05-21T01:57:48Z [5,067ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.robot.surface_gripper.ui' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper.ui' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [5,068ms] [Error] [omni.ext.plugin] [ext: isaacsim.robot.surface_gripper.ui-3.0.2] Failed to startup python extension.
[5.130s] [ext: isaacsim.sensors.camera.ui-0.2.2] startup
2026-05-21T01:57:48Z [5,145ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: cannot import name 'torch' from 'isaacsim.core.utils' (/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/__init__.py)
2026-05-21T01:57:48Z [5,145ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.sensors.camera.ui. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1126, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.camera/isaacsim/sensors/camera/__init__.py", line 16, in <module>
    from .camera import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.camera/isaacsim/sensors/camera/camera.py", line 23, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:48Z [5,146ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.sensors.camera.ui' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.camera.ui' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [5,146ms] [Error] [omni.ext.plugin] [ext: isaacsim.sensors.camera.ui-0.2.2] Failed to startup python extension.
[5.280s] [ext: omni.kit.core.collection-0.2.3] startup
[5.286s] [ext: isaacsim.core.experimental.materials-0.4.0] startup
2026-05-21T01:57:48Z [5,247ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:48Z [5,247ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.experimental.materials. Error: cannot import name 'torch' from 'isaacsim.core.utils' (/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/__init__.py). Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.materials/isaacsim/core/experimental/materials/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.materials/isaacsim/core/experimental/materials/impl/__init__.py", line 16, in <module>
    from .physics_materials import PhysicsMaterial, RigidBodyMaterial, SurfaceDeformableMaterial, VolumeDeformableMaterial
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.materials/isaacsim/core/experimental/materials/impl/physics_materials/__init__.py", line 16, in <module>
    from .physics_material import PhysicsMaterial
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.materials/isaacsim/core/experimental/materials/impl/physics_materials/physics_material.py", line 22, in <module>
    from isaacsim.core.experimental.prims import Prim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/articulation.py", line 32, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
ImportError: cannot import name 'torch' from 'isaacsim.core.utils' (/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/__init__.py)

2026-05-21T01:57:48Z [5,248ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.experimental.materials' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.materials' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [5,248ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.experimental.materials-0.4.0] Failed to startup python extension.
[5.383s] [ext: omni.kit.widget.zoombar-1.0.6] startup
[5.386s] [ext: omni.kit.widget.stage_icons-1.0.8] startup
[5.387s] [ext: omni.kit.browser.core-2.3.13] startup
[5.397s] [ext: isaacsim.core.experimental.objects-0.4.0] startup
2026-05-21T01:57:48Z [5,358ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.experimental.objects. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.objects/isaacsim/core/experimental/objects/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.objects/isaacsim/core/experimental/objects/impl/__init__.py", line 16, in <module>
    from .ground_plane import GroundPlane
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.objects/isaacsim/core/experimental/objects/impl/ground_plane.py", line 25, in <module>
    from isaacsim.core.experimental.prims import GeomPrim, XformPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/articulation.py", line 32, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:48Z [5,358ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.experimental.objects' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.objects' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:48Z [5,358ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.experimental.objects-0.4.0] Failed to startup python extension.
[5.494s] [ext: omni.kit.usd.collect-2.4.5] startup
[5.503s] [ext: omni.kit.window.stage-2.6.1] startup
[5.508s] [ext: omni.kit.browser.folder.core-1.10.9] startup
[5.520s] [ext: isaacsim.util.debug_draw-3.1.0] startup
[5.529s] [ext: isaacsim.robot_motion.lula-4.0.8] startup
[5.536s] [ext: omni.kit.tool.collect-2.2.18] startup
[5.543s] [ext: omni.kit.menu.stage-1.2.7] startup
[5.545s] [ext: omni.kit.usdz_export-1.0.9] startup
[5.549s] [ext: isaacsim.robot.manipulators-3.3.6] startup
2026-05-21T01:57:49Z [5,512ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.robot.manipulators. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/__init__.py", line 16, in <module>
    from .manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/__init__.py", line 17, in <module>
    from isaacsim.robot.manipulators.manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/single_manipulator.py", line 18, in <module>
    from isaacsim.core.prims import SingleArticulation, SingleRigidPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/articulation.py", line 27, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:49Z [5,512ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.robot.manipulators' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [5,512ms] [Error] [omni.ext.plugin] [ext: isaacsim.robot.manipulators-3.3.6] Failed to startup python extension.
[5.650s] [ext: isaacsim.sensors.physx-2.3.2] startup
2026-05-21T01:57:49Z [5,614ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:49Z [5,615ms] [Error] [omni.ext._impl._internal] Failed to import python module isaacsim.sensors.physx from /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx. Error: module 'torch' has no attribute 'Tensor'. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 196, in _custom_importer
    return _import_public(ext_module.path, ext_module.name, reload_enabled)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 103, in _import_public
    module = import_module(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx/isaacsim/sensors/physx/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx/isaacsim/sensors/physx/impl/__init__.py", line 16, in <module>
    from .commands import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx/isaacsim/sensors/physx/impl/commands.py", line 23, in <module>
    from isaacsim.core.utils.xforms import reset_and_set_xform_ops
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/xforms.py", line 18, in <module>
    from isaacsim.core.utils.prims import (
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 95, in <module>
    class XFormPrimViewState(object):
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 104, in XFormPrimViewState
    self, positions: Union[np.ndarray, torch.Tensor], orientations: Union[np.ndarray, torch.Tensor]
                                       ^^^^^^^^^^^^
AttributeError: module 'torch' has no attribute 'Tensor'

2026-05-21T01:57:49Z [5,615ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.sensors.physx' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [5,615ms] [Error] [omni.ext.plugin] [ext: isaacsim.sensors.physx-2.3.2] Failed to startup python extension.
[5.753s] [ext: isaacsim.robot_motion.motion_generation-8.0.26] startup
2026-05-21T01:57:49Z [5,715ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:49Z [5,716ms] [Error] [omni.ext._impl._internal] Failed to import python module isaacsim.robot_motion.motion_generation from /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot_motion.motion_generation. Error: module 'torch' has no attribute 'jit'. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 196, in _custom_importer
    return _import_public(ext_module.path, ext_module.name, reload_enabled)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 103, in _import_public
    module = import_module(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot_motion.motion_generation/isaacsim/robot_motion/motion_generation/__init__.py", line 16, in <module>
    from isaacsim.robot_motion.motion_generation.articulation_kinematics_solver import ArticulationKinematicsSolver
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot_motion.motion_generation/isaacsim/robot_motion/motion_generation/articulation_kinematics_solver.py", line 20, in <module>
    from isaacsim.core.api.articulations import ArticulationSubset
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/__init__.py", line 17, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/__init__.py", line 15, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/physics_context.py", line 20, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 23, in <module>
    @torch.jit.script
     ^^^^^^^^^
AttributeError: module 'torch' has no attribute 'jit'

2026-05-21T01:57:49Z [5,716ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.robot_motion.motion_generation' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot_motion.motion_generation' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [5,716ms] [Error] [omni.ext.plugin] [ext: isaacsim.robot_motion.motion_generation-8.0.26] Failed to startup python extension.
[5.853s] [ext: isaacsim.asset.browser-1.3.23] startup
2026-05-21T01:57:49Z [5,817ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
[5.934s] [ext: omni.kit.tool.asset_importer-4.3.2] startup
[5.946s] [ext: omni.isaac.nucleus-1.0.6] startup
2026-05-21T01:57:49Z [5,896ms] [Warning] [omni.isaac.nucleus] omni.isaac.nucleus has been deprecated in favor of isaacsim.storage.native. Please update your code accordingly.
2026-05-21T01:57:49Z [5,897ms] [Warning] [omni.isaac.nucleus.nucleus] omni.isaac.nucleus.nucleus has been deprecated in favor of isaacsim.storage.native. Please update your code accordingly.
[5.948s] [ext: omni.isaac.range_sensor-4.0.6] startup
2026-05-21T01:57:49Z [5,899ms] [Warning] [omni.isaac.range_sensor] omni.isaac.range_sensor has been deprecated in favor of isaacsim.sensors.physx. Please update your code accordingly.
2026-05-21T01:57:49Z [5,910ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.isaac.range_sensor. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.range_sensor/omni/isaac/range_sensor/__init__.py", line 26, in <module>
    from isaacsim.sensors.physx import _range_sensor
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx/isaacsim/sensors/physx/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx/isaacsim/sensors/physx/impl/__init__.py", line 16, in <module>
    from .commands import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physx/isaacsim/sensors/physx/impl/commands.py", line 23, in <module>
    from isaacsim.core.utils.xforms import reset_and_set_xform_ops
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/xforms.py", line 18, in <module>
    from isaacsim.core.utils.prims import (
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 18, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:49Z [5,910ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.range_sensor' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.range_sensor' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [5,910ms] [Error] [omni.ext.plugin] [ext: omni.isaac.range_sensor-4.0.6] Failed to startup python extension.
[6.053s] [ext: isaacsim.robot.manipulators.examples-1.1.2] startup
2026-05-21T01:57:49Z [6,003ms] [Warning] [omni.isaac.range_sensor] omni.isaac.range_sensor has been deprecated in favor of isaacsim.sensors.physx. Please update your code accordingly.
2026-05-21T01:57:49Z [6,014ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:49Z [6,025ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.robot.manipulators.examples. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1126, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/__init__.py", line 16, in <module>
    from .manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/__init__.py", line 17, in <module>
    from isaacsim.robot.manipulators.manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/single_manipulator.py", line 18, in <module>
    from isaacsim.core.prims import SingleArticulation, SingleRigidPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/articulation.py", line 29, in <module>
    from isaacsim.core.simulation_manager import IsaacEvents, SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:49Z [6,025ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.robot.manipulators.examples' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators.examples' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [6,025ms] [Error] [omni.ext.plugin] [ext: isaacsim.robot.manipulators.examples-1.1.2] Failed to startup python extension.
[6.167s] [ext: omni.isaac.asset_browser-1.0.6] startup
2026-05-21T01:57:49Z [6,129ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:49Z [6,129ms] [Warning] [omni.isaac.asset_browser] omni.isaac.asset_browser has been deprecated in favor of isaacsim.asset.browser. Please update your code accordingly.
[6.182s] [ext: isaacsim.asset.importer.mjcf-2.5.13] startup
[6.217s] [ext: isaacsim.core.cloner-1.4.10] startup
2026-05-21T01:57:49Z [6,181ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.core.cloner. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.cloner/isaacsim/core/cloner/__init__.py", line 16, in <module>
    from .impl.cloner import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.cloner/isaacsim/core/cloner/impl/cloner.py", line 21, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:49Z [6,181ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.core.cloner' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.cloner' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [6,181ms] [Error] [omni.ext.plugin] [ext: isaacsim.core.cloner-1.4.10] Failed to startup python extension.
[6.324s] [ext: omni.isaac.assets_check-0.3.13] startup
2026-05-21T01:57:49Z [6,274ms] [Warning] [omni.isaac.assets_check] omni.isaac.assets_check has been deprecated in favor of isaacsim.asset.browser. Please update your code accordingly.
[6.325s] [ext: isaacsim.cortex.framework-1.0.12] startup
[6.327s] [ext: isaacsim.examples.browser-0.2.1] startup
[6.333s] [ext: isaacsim.asset.importer.urdf-2.4.30] startup
[6.370s] [ext: omni.isaac.cloner-1.0.7] startup
2026-05-21T01:57:49Z [6,320ms] [Warning] [omni.isaac.cloner] omni.isaac.cloner has been deprecated in favor of isaacsim.core.cloner. Please update your code accordingly.
2026-05-21T01:57:49Z [6,337ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.isaac.cloner. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.cloner/omni/isaac/cloner/__init__.py", line 25, in <module>
    from isaacsim.core.cloner.impl.cloner import Cloner
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.cloner/isaacsim/core/cloner/impl/cloner.py", line 21, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:49Z [6,337ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.cloner' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.cloner' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:49Z [6,337ms] [Error] [omni.ext.plugin] [ext: omni.isaac.cloner-1.0.7] Failed to startup python extension.
[6.486s] [ext: omni.importer.onshape-1.0.1] startup
[6.501s] [ext: omni.kit.widget.collection-0.3.1] startup
[6.522s] [ext: omni.isaac.core_nodes-2.0.6] startup
2026-05-21T01:57:50Z [6,472ms] [Warning] [omni.isaac.core_nodes] omni.isaac.core_nodes has been deprecated in favor of isaacsim.core.nodes. Please update your code accordingly.
[6.524s] [ext: omni.isaac.cortex-1.0.5] startup
2026-05-21T01:57:50Z [6,475ms] [Warning] [omni.isaac.cortex] omni.isaac.cortex has been deprecated in favor of isaacsim.cortex.framework. Please update your code accordingly.
[6.528s] [ext: isaacsim.core.throttling-2.2.2] startup
[6.538s] [ext: omni.kit.window.collection-0.3.1] startup
2026-05-21T01:57:50Z [6,492ms] [Warning] [omni.kit.window.collection.collection_watch] Get collection from usdrt stage failed: Attach(): incompatible function arguments. The following argument types are supported:
    1. (stageId: int) -> usdrt.Usd._Usd.Stage
    2. (fabricId: usdrt.helpers._helpers.FabricId) -> usdrt.Usd._Usd.Stage

Invoked with: -1
[6.543s] [ext: omni.anim.shared.core-107.0.1] startup
[6.557s] [ext: omni.sensors.nv.common-3.0.0] startup
[6.565s] [ext: omni.kit.viewport.menubar.lighting-107.3.1] startup
[6.585s] [ext: omni.isaac.franka-1.0.7] startup
2026-05-21T01:57:50Z [6,537ms] [Warning] [omni.isaac.franka] omni.isaac.franka has been deprecated in favor of isaacsim.robot.manipulators.examples.franka. Please update your code accordingly.
2026-05-21T01:57:50Z [6,538ms] [Warning] [omni.isaac.franka.franka] omni.isaac.franka has been deprecated in favor of isaacsim.robot.manipulators.examples.franka. Please update your code accordingly.
2026-05-21T01:57:50Z [6,560ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.isaac.franka. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.franka/omni/isaac/franka/__init__.py", line 29, in <module>
    from .franka import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.franka/omni/isaac/franka/franka.py", line 22, in <module>
    from isaacsim.robot.manipulators.examples.franka.franka import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/__init__.py", line 16, in <module>
    from .manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/__init__.py", line 17, in <module>
    from isaacsim.robot.manipulators.manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/single_manipulator.py", line 18, in <module>
    from isaacsim.core.prims import SingleArticulation, SingleRigidPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/articulation.py", line 27, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:50Z [6,560ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.franka' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.franka' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [6,561ms] [Error] [omni.ext.plugin] [ext: omni.isaac.franka-1.0.7] Failed to startup python extension.
[6.648s] [ext: isaacsim.cortex.behaviors-2.0.14] startup
2026-05-21T01:57:50Z [6,599ms] [Warning] [omni.isaac.franka] omni.isaac.franka has been deprecated in favor of isaacsim.robot.manipulators.examples.franka. Please update your code accordingly.
2026-05-21T01:57:50Z [6,600ms] [Warning] [omni.isaac.franka.franka] omni.isaac.franka has been deprecated in favor of isaacsim.robot.manipulators.examples.franka. Please update your code accordingly.
[6.652s] [ext: omni.sensors.nv.materials-2.0.0] startup
[6.658s] [ext: omni.sensors.nv.wpm-3.0.0] startup
[6.659s] [ext: omni.sensors.net-1.0.0] startup
[6.665s] [ext: omni.isaac.cortex.sample_behaviors-2.0.5] startup
2026-05-21T01:57:50Z [6,617ms] [Warning] [omni.isaac.cortex.sample_behaviors] omni.isaac.cortex.sample_behaviors has been deprecated in favor of isaacsim.cortex.behaviors. Please update your code accordingly.
[6.670s] [ext: isaacsim.sensors.physics-0.4.3] startup
2026-05-21T01:57:50Z [6,634ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:50Z [6,662ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.sensors.physics. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics/isaacsim/sensors/physics/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics/isaacsim/sensors/physics/impl/__init__.py", line 16, in <module>
    from .commands import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics/isaacsim/sensors/physics/impl/commands.py", line 21, in <module>
    from isaacsim.core.utils.prims import delete_prim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 18, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:50Z [6,662ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.sensors.physics' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [6,664ms] [Error] [omni.ext.plugin] [ext: isaacsim.sensors.physics-0.4.3] Failed to startup python extension.
[6.774s] [ext: omni.sensors.nv.radar-3.0.0] startup
[6.785s] [ext: omni.sensors.nv.lidar-3.0.0] startup
[6.790s] [ext: omni.sensors.nv.ids-2.0.0] startup
[6.791s] [ext: isaacsim.simulation_app-2.12.2] startup
[6.796s] [ext: isaacsim.robot.policy.examples-4.1.11] startup
2026-05-21T01:57:50Z [6,756ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
[6.809s] [ext: isaacsim.sensors.rtx-15.8.4] startup
2026-05-21T01:57:50Z [6,810ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module isaacsim.sensors.rtx. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.rtx/isaacsim/sensors/rtx/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.rtx/isaacsim/sensors/rtx/impl/__init__.py", line 16, in <module>
    from .commands import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.rtx/isaacsim/sensors/rtx/impl/commands.py", line 26, in <module>
    from isaacsim.core.utils.xforms import reset_and_set_xform_ops
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/xforms.py", line 18, in <module>
    from isaacsim.core.utils.prims import (
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 18, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:50Z [6,810ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.sensors.rtx' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.rtx' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [6,810ms] [Error] [omni.ext.plugin] [ext: isaacsim.sensors.rtx-15.8.4] Failed to startup python extension.
[6.867s] [ext: omni.isaac.kit-2.0.6] startup
2026-05-21T01:57:50Z [6,819ms] [Warning] [omni.isaac.kit] omni.isaac.kit has been deprecated in favor of isaacsim.simulation_app. Please update your code accordingly.
[6.870s] [ext: omni.isaac.quadruped-3.0.7] startup
2026-05-21T01:57:50Z [6,821ms] [Warning] [omni.isaac.quadruped] omni.isaac.quadruped has been deprecated in favor of isaacsim.robot.policy.examples. Please update your code accordingly.
[6.872s] [ext: omni.isaac.lula-4.0.6] startup
2026-05-21T01:57:50Z [6,825ms] [Warning] [omni.isaac.lula] omni.isaac.lula has been deprecated in favor of isaacsim.robot_motion.lula. Please update your code accordingly.
[6.877s] [ext: isaacsim.gui.sensors.icon-2.0.3] startup
2026-05-21T01:57:50Z [6,849ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
[6.952s] [ext: isaacsim.gui.content_browser-0.1.11] startup
[6.961s] [ext: omni.isaac.sensor-13.0.7] startup
2026-05-21T01:57:50Z [6,913ms] [Warning] [omni.isaac.sensor] omni.isaac.sensor has been deprecated in favor of isaacsim.sensors.camera, isaacsim.sensors.physics, isaacsim.sensors.physx, and isaacsim.sensors.rtx. Please update your code accordingly.
2026-05-21T01:57:50Z [6,942ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.isaac.sensor. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.sensor/omni/isaac/sensor/__init__.py", line 25, in <module>
    from isaacsim.sensors.physics import _sensor
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics/isaacsim/sensors/physics/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics/isaacsim/sensors/physics/impl/__init__.py", line 16, in <module>
    from .commands import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.sensors.physics/isaacsim/sensors/physics/impl/commands.py", line 21, in <module>
    from isaacsim.core.utils.prims import delete_prim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/prims.py", line 31, in <module>
    from isaacsim.core.utils.types import SDF_type_to_Gf
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/types.py", line 18, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:50Z [6,942ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.sensor' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.sensor' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [6,942ms] [Error] [omni.ext.plugin] [ext: omni.isaac.sensor-13.0.7] Failed to startup python extension.
[6.999s] [ext: omni.isaac.surface_gripper-2.0.6] startup
2026-05-21T01:57:50Z [6,949ms] [Warning] [omni.isaac.surface_gripper] omni.isaac.surface_gripper has been deprecated in favor of isaacsim.robot.surface_gripper. Please update your code accordingly.
2026-05-21T01:57:50Z [6,952ms] [Warning] [omni.isaac.sensor] omni.isaac.sensor has been deprecated in favor of isaacsim.sensors.camera, isaacsim.sensors.physics, isaacsim.sensors.physx, and isaacsim.sensors.rtx. Please update your code accordingly.
2026-05-21T01:57:50Z [6,980ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:50Z [6,982ms] [Error] [omni.ext._impl._internal] Failed to import python module omni.isaac.surface_gripper from /home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.surface_gripper. Error: module 'torch' has no attribute 'jit'. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 196, in _custom_importer
    return _import_public(ext_module.path, ext_module.name, reload_enabled)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 103, in _import_public
    module = import_module(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.surface_gripper/omni/isaac/surface_gripper/__init__.py", line 26, in <module>
    from isaacsim.robot.surface_gripper import _surface_gripper
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/__init__.py", line 17, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/impl/__init__.py", line 18, in <module>
    from .gripper_view import GripperView
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.surface_gripper/isaacsim/robot/surface_gripper/impl/gripper_view.py", line 22, in <module>
    from isaacsim.core.experimental.prims import XformPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.experimental.prims/isaacsim/core/experimental/prims/impl/articulation.py", line 32, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 23, in <module>
    @torch.jit.script
     ^^^^^^^^^
AttributeError: module 'torch' has no attribute 'jit'

2026-05-21T01:57:50Z [6,982ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.surface_gripper' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.surface_gripper' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [6,982ms] [Error] [omni.ext.plugin] [ext: omni.isaac.surface_gripper-2.0.6] Failed to startup python extension.
[7.069s] [ext: omni.isaac.universal_robots-1.0.6] startup
2026-05-21T01:57:50Z [7,019ms] [Warning] [omni.isaac.surface_gripper] omni.isaac.surface_gripper has been deprecated in favor of isaacsim.robot.surface_gripper. Please update your code accordingly.
2026-05-21T01:57:50Z [7,019ms] [Warning] [omni.isaac.universal_robots] omni.isaac.universal_robots has been deprecated in favor of isaacsim.robot.manipulators.examples.universal_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,020ms] [Warning] [omni.isaac.universal_robots.kinematics_solver] omni.isaac.franka has been deprecated in favor of isaacsim.robot.manipulators.examples.universal_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,047ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:50Z [7,071ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.isaac.universal_robots. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.universal_robots/omni/isaac/universal_robots/__init__.py", line 26, in <module>
    from .kinematics_solver import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.universal_robots/omni/isaac/universal_robots/kinematics_solver.py", line 23, in <module>
    from isaacsim.robot.manipulators.examples.universal_robots.kinematics_solver import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/__init__.py", line 16, in <module>
    from .manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/__init__.py", line 17, in <module>
    from isaacsim.robot.manipulators.manipulators.single_manipulator import SingleManipulator
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.manipulators/isaacsim/robot/manipulators/manipulators/single_manipulator.py", line 18, in <module>
    from isaacsim.core.prims import SingleArticulation, SingleRigidPrim
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/__init__.py", line 16, in <module>
    from .impl import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/__init__.py", line 16, in <module>
    from .articulation import Articulation
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.prims/isaacsim/core/prims/impl/articulation.py", line 29, in <module>
    from isaacsim.core.simulation_manager import IsaacEvents, SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:50Z [7,071ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.universal_robots' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.universal_robots' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [7,071ms] [Error] [omni.ext.plugin] [ext: omni.isaac.universal_robots-1.0.6] Failed to startup python extension.
[7.131s] [ext: isaacsim.robot.wheeled_robots-4.0.24] startup
2026-05-21T01:57:50Z [7,082ms] [Warning] [omni.isaac.universal_robots] omni.isaac.universal_robots has been deprecated in favor of isaacsim.robot.manipulators.examples.universal_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,082ms] [Warning] [omni.isaac.universal_robots.kinematics_solver] omni.isaac.franka has been deprecated in favor of isaacsim.robot.manipulators.examples.universal_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,111ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:50Z [7,115ms] [Error] [omni.ext._impl._internal] Failed to import python module isaacsim.robot.wheeled_robots from /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.wheeled_robots. Error: module 'torch' has no attribute 'jit'. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 196, in _custom_importer
    return _import_public(ext_module.path, ext_module.name, reload_enabled)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py", line 103, in _import_public
    module = import_module(module_name)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/carb/profiler/__init__.py", line 99, in wrapper
    r = f(*args, **kwds)
        ^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/__init__.py", line 15, in <module>
    from .controllers import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/controllers/__init__.py", line 15, in <module>
    from .ackermann_controller import AckermannController
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/controllers/ackermann_controller.py", line 19, in <module>
    from isaacsim.core.api.controllers.base_controller import BaseController
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/__init__.py", line 17, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/__init__.py", line 15, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/physics_context.py", line 20, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 23, in <module>
    @torch.jit.script
     ^^^^^^^^^
AttributeError: module 'torch' has no attribute 'jit'

2026-05-21T01:57:50Z [7,115ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'isaacsim.robot.wheeled_robots' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.wheeled_robots' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [7,115ms] [Error] [omni.ext.plugin] [ext: isaacsim.robot.wheeled_robots-4.0.24] Failed to startup python extension.
[7.172s] [ext: omni.isaac.utils-2.0.6] startup
[7.177s] [ext: isaacsim.app.about-2.0.11] startup
[7.183s] [ext: omni.isaac.version-2.0.7] startup
2026-05-21T01:57:50Z [7,135ms] [Warning] [omni.isaac.version] omni.isaac.version has been deprecated in favor of isaacsim.core.version. Please update your code accordingly.
[7.186s] [ext: omni.isaac.wheeled_robots-3.0.7] startup
2026-05-21T01:57:50Z [7,137ms] [Warning] [omni.isaac.wheeled_robots] omni.isaac.wheeled_robots has been deprecated in favor of isaacsim.robot.wheeled_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,138ms] [Warning] [omni.isaac.wheeled_robots.controllers] omni.isaac.wheeled_robots has been deprecated in favor of isaacsim.robot.wheeled_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,138ms] [Warning] [omni.isaac.wheeled_robots.controllers.ackermann_controller] omni.isaac.wheeled_robots has been deprecated in favor of isaacsim.robot.wheeled_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,160ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
2026-05-21T01:57:50Z [7,195ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module omni.isaac.wheeled_robots. Error: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12. Traceback:
Traceback (most recent call last):
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.wheeled_robots/omni/isaac/wheeled_robots/__init__.py", line 27, in <module>
    from .controllers import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.wheeled_robots/omni/isaac/wheeled_robots/controllers/__init__.py", line 27, in <module>
    from .ackermann_controller import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.wheeled_robots/omni/isaac/wheeled_robots/controllers/ackermann_controller.py", line 23, in <module>
    from isaacsim.robot.wheeled_robots.controllers.ackermann_controller_deprecated import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.robot.wheeled_robots/isaacsim/robot/wheeled_robots/controllers/ackermann_controller_deprecated.py", line 19, in <module>
    from isaacsim.core.api.controllers.base_controller import BaseController
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/__init__.py", line 17, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/__init__.py", line 15, in <module>
    from isaacsim.core.api.physics_context.physics_context import PhysicsContext
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.api/isaacsim/core/api/physics_context/physics_context.py", line 20, in <module>
    from isaacsim.core.simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/__init__.py", line 15, in <module>
    from .impl.extension import Extension
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/__init__.py", line 15, in <module>
    from .extension import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/extension.py", line 21, in <module>
    from .simulation_manager import SimulationManager
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.simulation_manager/isaacsim/core/simulation_manager/impl/simulation_manager.py", line 20, in <module>
    import isaacsim.core.utils.torch as torch_utils
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/__init__.py", line 15, in <module>
    from .maths import *
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/isaacsim.core.utils/isaacsim/core/utils/torch/maths.py", line 19, in <module>
    import torch
  File "/home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/__init__.py", line 409, in <module>
    from torch._C import *  # noqa: F403
    ^^^^^^^^^^^^^^^^^^^^^^
ImportError: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12

2026-05-21T01:57:50Z [7,195ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'omni.isaac.wheeled_robots' in '/home/gotree94/isaacsim/_build/linux-x86_64/release/extsDeprecated/omni.isaac.wheeled_robots' failed to load.

At:
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/gotree94/.cache/packman/chk/kit-kernel/107.3.3+isaac.229672.69cbf6ad.gl.manylinux_2_35_x86_64.release/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>

2026-05-21T01:57:50Z [7,195ms] [Error] [omni.ext.plugin] [ext: omni.isaac.wheeled_robots-3.0.7] Failed to startup python extension.
[7.263s] [ext: omni.kit.widget.imageview-1.0.4] startup
2026-05-21T01:57:50Z [7,212ms] [Warning] [omni.isaac.wheeled_robots] omni.isaac.wheeled_robots has been deprecated in favor of isaacsim.robot.wheeled_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,212ms] [Warning] [omni.isaac.wheeled_robots.controllers] omni.isaac.wheeled_robots has been deprecated in favor of isaacsim.robot.wheeled_robots. Please update your code accordingly.
2026-05-21T01:57:50Z [7,213ms] [Warning] [omni.isaac.wheeled_robots.controllers.ackermann_controller] omni.isaac.wheeled_robots has been deprecated in favor of isaacsim.robot.wheeled_robots. Please update your code accordingly.
[7.265s] [ext: omni.isaac.window.about-2.0.7] startup
2026-05-21T01:57:50Z [7,217ms] [Warning] [omni.isaac.window.about] omni.isaac.window.about has been deprecated in favor of isaacsim.app.about. Please update your code accordingly.
2026-05-21T01:57:50Z [7,217ms] [Warning] [omni.isaac.window.about.about] omni.isaac.window.about.about has been deprecated in favor of isaacsim.app.about.about. Please update your code accordingly.
[7.269s] [ext: omni.kit.property.audio-1.0.16] startup
[7.275s] [ext: omni.kit.property.camera-1.0.10] startup
[7.278s] [ext: omni.kit.window.quicksearch-2.4.4] startup
[7.294s] [ext: omni.kit.property.geometry-2.0.4] startup
[7.300s] [ext: omni.hydra.scene_api-0.1.2] startup
2026-05-21T01:57:50Z [7,259ms] [Error] [omni.graph.core._impl.extension] OGN node registration completed with errors: /home/gotree94/isaacsim/_build/linux-x86_64/release/exts/omni.isaac.ml_archive/pip_prebundle/torch/lib/../../nvidia/cusparse/lib/libcusparse.so.12: undefined symbol: __nvJitLinkCreate_12_8, version libnvJitLink.so.12
[7.312s] [ext: omni.kit.property.light-1.0.12] startup
Inconsistency detected by ld.so: ../elf/dl-tls.c: 618: _dl_allocate_tls_init: Assertion `listp != NULL' failed!
(base) gotree94@gotree94-ROG-Strix-SCAR-16-G635LX-G635LX:~/isaacsim$ 

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
