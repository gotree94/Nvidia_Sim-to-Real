# Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac

https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/index.html
https://github.com/TheRobotStudio/SO-ARM100

SO-101 Robot

---
Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac
Welcome to this hands-on learning path. The material is organized into self-paced sections you can work through in order. Duration depends on how deeply you run each exercise and whether you collect your own simulation data.

Overview
You’ll train and deploy a vision-language-action (VLA) model to perform unstructured pick-and-place of centrifuge vials into a rack using an SO-101 robot arm - first in sim, where we can iterate quickly and validate behavior, then in reality.

Through this workflow you’ll experience the sim-to-real gap firsthand and how to apply systematic strategies to close it.


Robot Calibration


Domain Randomization


Sim Teleoperation


Data Collection


Cosmos Augmentation


Real Robot Autonomous Tests

Learning Objectives
By the end of this learning path, you’ll be able to:

Configure and calibrate an SO-101 robot for sim-to-real experiments

Collect demonstration data using teleoperation and augment with domain randomization

Train vision-language-action (VLA) models using GR00T for robot manipulation

Evaluate trained policies in simulation

Deploy policies to physical robots and observe the sim-to-real gap

Apply four sim-to-real strategies: Domain Randomization, Co-training, Cosmos Augmentation, and SAGE+GapONet (actuator gap estimation)

---

Overview
This learning path will teach you how to train and deploy a physical AI model to a physical robot, starting in simulation then moving to the real world.


Teleoperation example in simulation.


Autonomous execution based on model trained with teleoperation data.


What Is Physical AI?
Physical AI refers to AI systems that interact with and manipulate the physical world. Unlike generative or agentic AI (think image generators, chatbots), Physical AI has the ability to:

Perceive the real world through sensors

Reason about physics, objects, and spatial relationships

Act through motors, actuators, and end-effectors

Adapt to the unpredictability of real environments

This learning path teaches a complete Physical AI workflow with physical robots, from simulation to a robot acting autonomously, right in front of you.

The Task: Centrifuge Vial Pick-and-Place
Vial to rack task performed by SO-101 robot
Vial to rack pick-and-place task performed autonomously by an SO-101 robot.
The task we’ll use today is unstructured pick-and-place of centrifuge vials. The vials are scattered on a table and need to be placed into a designated rack.

We’ve simplified some of the constraints with a lightbox, and with some of the parameters of the task, to make it more approachable.

But the tools and techniques you’ll learn are applicable to more complex tasks and production robots. The focus of this learning path is the sim-to-real workflow.


Why This Task?
So why did we pick this task? Let’s imagine we are engineers solving a laboratory problem.

In our fictional problem, these vials are dropped down a chute or otherwise scattered in an unstructured way, but need to be organized into a rack for processing by automated machinery - a line that already exists.

Real-world relevance: this is an analogy for workflows where items must be prepared for autonomous analysis machines.

Safety implications: think of use cases where potentially hazardous samples are handled, so minimizing human exposure is critical, hence the use of robotics. The ability to teach the task in simulation also saves time and reduces exposure.

Technical challenge: adaptation to change, ability for the robot to adapt and retry.

Approachable: for learning, this task is simple enough to gather objects for and perform teleoperation.

Why Is This Problem Interesting?
Our policy will work from 2D camera information, and the placement of the vials in the rack requires re-orienting the vials and placing them fairly precisely.

As you’ll likely find from teleoperating the task yourself, it’s not easy at first. One major issue is that the robot’s gripper camera will become occluded after the robot grasps a vial, so the policy will need to be able to operate without this information.

You’ll experience this challenge first-hand when you do teleoperation yourself.

Note

The SO-101 isn’t a production robot, but it’s a fun, approachable platform for learning these tools before you apply them to production robots. Again, the focus here is a workflow that you can apply to other tasks, or to production robots.

Why Simulation Matters
Task wireframe: vials on table, target rack outlined.
Task wireframe: vials are scattered on a table, to be placed into a rack by the robot.
Testing robots in the real world is expensive, risky, and sometimes dangerous.

Simulation addresses these fundamental limitations:

Time: Real-world data collection is slow—one trajectory takes the same time whether you have one robot or one thousand

Cost: Robot hardware is expensive, and failures during exploration can cause damage

Safety: Exploring failure modes on real hardware can be dangerous

Diversity: Creating varied training scenarios (different lighting, objects, positions) is labor-intensive

Simulation addresses all of these:

Challenge

Real World

Simulation

Training speed

1x real-time

1000x+ parallel environments

Hardware cost

$10K-$100K+ per robot

Marginal compute cost

Failure consequence

Damage, downtime

Reset and continue

Scenario diversity

Manual setup

Procedural generation

Privileged Information
Simulation also provides access to information that might be impossible to obtain in the real world:

Exact object poses: No perception noise or occlusion

Contact forces: Precise measurements at every contact point

Ground truth labels: Perfect segmentation and object identity

State derivatives: Exact velocities and accelerations

This privileged information can accelerate learning, even when the final policy only uses realistic sensor inputs.

Key Takeaways
Simulation enables fast, safe, diverse training that can be impossible in the real world

The sim-to-real gap is a fundamental challenge that requires systematic approaches

This learning path provides hands-on experience with NVIDIA Isaac and multiple gap-closing strategies

Success comes from iteration and combining approaches

Using a VLA (Vision Language Action) model called Isaac GR00T, our system will receive a language command like “pick up the vial and place it on the rack”, and use joint feedback and camera observations as policy inputs. The policy then outputs motor positions to execute the task.

---
How to Take This Course
Learning Strategies
There are several ways to work through this learning path, depending on your goals, how much time you want to invest, and how much of a challenge you want to take on.

Option 1: As-Is
If you’re not sure, just take the course as-is!

Buy the workspace materials from the Bill of Materials, use our pre-trained checkpoints and pre-collected datasets, and follow the course as-is.

Tip

This is the fastest way to experience the full sim-to-real workflow end-to-end.

Option 2: Use Your Own Data
Same as option 1, except you collect your own teleoperation data and train your own models on the same vial-to-rack task.

Tip

This will take more time and work, but will help you experience the value of good demonstration data, watch how this affects policy performance, and more. Prove you can replicate the results independently.

Option 3: Bring Your Own Task
Get more creative with this learning path as a base for your own exploration.

Buy the workspace, but swap out the props and task. Define a new manipulation problem, collect data for it, and apply the same sim-to-real strategies covered in this course.

Tip

This will take some creativity, or maybe you already have a task in mind. But it will ultimately teach you the most, to build and apply the process to a new task.

Option 4: Going Further
Train a robust enough model that you can completely remove the lightbox enclosure and run the task in an uncontrolled environment.

Computer Hardware Prerequisites
We have tested this workshop on:

Ubuntu Linux 24.04 with an RTX 5090 Laptop edition, 64GB RAM

Ubuntu Linux 24.04 with an RTX PRO 6000 Blackwell Workstation Edition, 125GB RAM

Details on the robot and workspace requirements can be found in Building the Workspace.
---
What Is Sim-to-Real?
Learning Objectives
By the end of this session, you’ll be able to:

Define sim-to-real transfer and its goals

Identify the four major categories of sim-to-real gaps

Explain why transfer is difficult even with high-fidelity simulation

Sim-to-Real Defined
Sim-to-real refers to the process of training a policy in simulation and deploying it on real hardware. The goal is a policy that performs well in the real world despite being trained entirely (or primarily) in simulation.

Sim-to-Real
Sim-to-Real with Unitree H1
The Sim-to-Real Gap
The sim-to-real gap is the performance difference between simulation and reality. A policy achieving high success rates in simulation may perform significantly worse on real hardware.

Warning

The sim-to-real gap is often larger than expected. And while colloquially we may discuss “the gap” as if it’s a single entity, the gap is a complex combination of gaps in sensing, actuation, physics, and modeling.

Never assume a policy will “just work” on real hardware without systematic testing and iteration.

Sources of the Gap
Sensing Gaps
Camera models lack real sensor noise, blur, and distortion

Depth sensors have idealized measurements without artifacts

Simulated lighting differs from real lighting conditions

Actuation Gaps
Motor models lack friction, backlash, and thermal effects

Joint dynamics are simplified

Control loop timing differs between simulation and hardware

Physics Gaps
Contact dynamics (friction, restitution) are approximations

Deformable objects are difficult to simulate accurately

Fluid dynamics and granular materials are computationally expensive

Modeling Gaps
CAD models differ from as-built hardware

Mass and inertia properties are estimates

What Makes Transfer Hard?
The sim-to-real gap isn’t just about simulation fidelity. Even with perfect simulation, transfer is challenging because:

Distribution shift: Real-world conditions vary from training

Compounding errors: Small perception errors lead to large action errors

Unmodeled dynamics: Real physics has effects that may not be represented in simulation

Temporal differences: Real-time constraints affect behavior

Summary
Gap Category

Examples

Sensing

Camera noise, lighting, depth artifacts

Actuation

Friction, backlash, thermal effects

Physics

Contact dynamics, deformables

Modeling

CAD errors, mass/inertia estimates

Understanding these gaps is essential—throughout this learning path, you’ll learn strategies to address each category.
---
LeRobot: Background and Community
In this session, we’ll explore the background of the SO-101 robot in front of you, the Hugging Face LeRobot project, and the community resources available to support your work.

This framework is an approachable way to learn robotics, and become familiar with the same practices used on industrial robots, in an affordable way you can even try yourself at home.

Learning Objectives
By the end of this session, you’ll be able to:

Describe the SO-101 robot and its capabilities

Explain the LeRobot project and its role in the robotics community

Identify community resources for continued learning

The SO-101 Robot
The SO-101 is a 6-DOF (degrees of freedom) robot arm designed for research and education in manipulation tasks.

While we colloquially refer to the SO-101 as a single robot, it’s typically sold or made as a pair:

Teleop arm (also called the “leader”): You move this arm by hand to perform demonstrations. The encoder positions can be recorded or used to directly manipulate the robot arm, or both.

Robot arm (also called the “follower”): During teleoperation it mirrors the teleop arm; during evaluation it is driven by a policy.

SO-101 Follower Arm
SO-101 Robot, also known as the “follower arm”.
The typical kit also includes a teleoperation arm, which is used to control either simulated robots or the “follower” arm.

SO-101 Leader Arm
SO-101 Teleoperation Arm, also known as the “leader arm” or “teleop arm”. Notice the gripper on the end of the arm for your hand to manipulate the robot.
Joint Configuration
The SO-101 has six joints:

Base (J1): Rotation around vertical axis

Shoulder (J2): First arm segment elevation

Elbow (J3): Second arm segment elevation

Wrist Pitch (J4): Wrist up/down rotation

Wrist Roll (J5): Wrist rotation around arm axis

Gripper (J6): Parallel jaw gripper

Why SO-101?
The SO-101 is ideal for this learning path because:

Accessible: Affordable for education and research

Well-documented: Strong community support

LeRobot integration: First-class support in the LeRobot ecosystem

Sim-ready: Accurate simulation models available

The LeRobot Project
LeRobot is an open-source library from Hugging Face which includes tools for data collection, training, robot control, and evaluation of robot policies.

Community Datasets
LeRobot hosts community-contributed datasets on the Hugging Face Hub with the LeRobot Dataset Format.

Thousands of robot demonstrations

Multiple robot platforms

Various manipulation tasks

Standardized formats for interoperability

Why LeRobot for This Course
LeRobot is the foundation of this course for several practical reasons:

Seamless Data Flow With Hugging Face Hub
Getting data into and out of the system is straightforward:

# Example command

# Push your collected dataset to the Hub
hf upload ${HF_USER}/my_robot_dataset ./datasets/my_robot_dataset

# Pull datasets for training or co-training
hf download lerobot/community_dataset
This Hub integration means you can share datasets with collaborators, version your data, and access community contributions with minimal friction.

Post-Training Pipeline
LeRobot wraps established training pipelines (including NVIDIA Isaac GR00T, SmolVLA, and more):

# Example command
# Fine-tune a policy on your data
python lerobot/scripts/train.py \
    --policy.type=gr00t \
    --dataset.repo_id=${HF_USER}/my_dataset
You spend time on your task, not on infrastructure.

Real Robot Evaluation
The same framework used for data collection handles policy deployment:

# Example command
# Evaluate a trained policy on the real robot
lerobot-eval \
    --robot.type=so101_follower \
    --robot.port=$ROBOT_PORT \
    --policy_path ${HF_USER}/my_trained_policy
This closes the loop: collect data → train → deploy → evaluate → iterate. All within one system.

Community Resources
Dataset Visualizer
LeRobot provides an interactive dataset visualizer on Hugging Face Spaces:

LeRobot Dataset Visualizer

Use this tool to explore any LeRobot dataset on the Hub. You can scrub through episodes, view camera feeds, and inspect action/state trajectories—useful for debugging data quality issues or understanding what a dataset contains before training.

Documentation
LeRobot Documentation

SO-101 Getting Started Guide

Examples and Tutorials
GR00T N1.5 SO-101 Tuning

Community notebooks and examples

Community Channels
Hugging Face Discord

GitHub Discussions

Community forums

Hugging Face Hub Integration
LeRobot leverages the Hugging Face Hub for:

Dataset Sharing
# Example command
# Download a community dataset
hf download lerobot/so101_pickplace
Model Sharing
# Example command
# Download a pre-trained model
hf download lerobot/groot_so101_vial_pickup
Experiment Tracking
Integration with Weights & Biases and other experiment tracking tools.

How We Used Hugging Face in This Course
1. Dataset format for gathering demonstrations

We used the LeRobot dataset format for all teleoperation data. Episodes are stored with observations (e.g. camera images), robot state, and actions in a consistent schema. Recording is done with lerobot_agent (or lerobot_record on real hardware) using --repo_id and --repo_root so that data lands in the correct structure for training and for upload to the Hub.

2. Sharing datasets

Datasets were pushed to the Hugging Face Hub so they could be reused for training, shared with others, and versioned. We used --dataset.repo_id=${HF_USER}/dataset_name and --dataset.push_to_hub=true when recording, or hf upload for existing local datasets. The LeRobot Dataset Visualizer on the Hub was used to inspect episodes and verify quality before training.

3. Merging datasets for co-training (sim + real, sim + Cosmos)

For co-training we combined multiple data sources into a single training dataset. Sim + real: we merged simulation teleop datasets with real-robot teleop datasets (e.g. so101_teleop_vials_rack_left with so101_teleop_vials_rack_left_real_50) so the policy could learn from both. Sim + Cosmos: we combined base sim data with Cosmos-augmented synthetic data. Merging was done via the Hub (download multiple repos, merge locally) or by pointing the training script at a single merged repo so that one run could use sim, real, and augmented data together.

4. Sharing evaluations

Evaluation results and policy checkpoints were shared via the Hub. Trained models were uploaded (e.g. as GR00T checkpoints or LeRobot policy repos) so others could reproduce evaluations or run the same policy in sim and on the real robot. Links to specific datasets and model repos were used in this learning path to align everyone on the same baselines and co-trained models.

Key Takeaways
SO-101 is an accessible, well-supported robot for learning sim-to-real

LeRobot provides open-source tools, datasets, and models

The Hugging Face community offers ongoing support and resources

You’re joining a growing community of robot learners and practitioners
---
Building the Workspace
This module is about constructing and standardizing the real-world task area. This includes a lightbox enclosure, lighting, cameras, mat, vials, and rack—so it matches the Isaac Lab scene used for training and evaluation.

Building the lightbox this way gives you a consistent environment, so you can use our models and datasets.

You can also keep using it after this learning path, to do more of your own robot experiments!

Video Tutorial

Important

Why are we starting with the physical workspace?

When you do Physical AI work in the real world, you might not have a physical workspace available to you when you start out. We often start in sim, for all the reasons we discussed earlier (ease of testing, cost, safety, ease of iteration).

For this workshop, we will set up the physical space first for three reasons:

We give you this info early on, so you can order parts or build your workspace in prep for finishing the learning path

To give you experience with the physical robot and teleoperation. It’s fun!

To give you a sense of how “hard” the task is, when using the same inputs the AI model will have (two cameras, joint positions)

The Lightbox Environment
Let’s start by building a white lightbox enclosure that includes:

Cameras — one on the robot (wrist / gripper view), one stationary (external / scene view)

Lights — diffuse light with controllable brightness

Props — centrifuge vials, yellow rack, foam mat.

Lightbox

Vial Rack

Bill of Materials
The complete robot + workspace setup should cost less than $500 USD, estimated based on the options below.

We recommend getting the SO-101 pre-assembled, as it comes with a teleop arm and is easier to assemble. You can also build it yourself, but it’s a bit more work.

Robot
Approximate cost: $300 USD

Item

Description

Model/Specs

Quantity

Details

SO-101 Robot Arm and Teleop Arm

6-DoF collaborative robot arm (SO-101 or similar)

SO-101 package 3, orange

1

Main robot for pick-and-place task; Teleop arm optional for demonstration recording. We recommend this kit because of the included gripper camera, which will match our datasets. Alternatively, you can print and build your own SO-101!

Workspace
Approximate cost: $130 USD

Item

Description

Model/Specs

Quantity

Details

Camera (External)

USB webcam, fixed mount, ~78° horizontal FoV

Logitech C920 or equivalent

1

Fixed perspective to capture overview of workspace; must be stable and aligned as in simulation.

Lightbox Enclosure Panels

White foam board box, approx. 30” wide, 20” tall, 20” deep.

Assemble from 5 sheets of 20x30” foam board, 3/16” thick

5

Provides consistent, diffuse lighting and neutral background for images. Other white lightboxes can be substituted. Thicker or thinner foam board works.

Light Source

LED tube light, diffuse, CRI >90, ~4000K, adjustable

Neewer Dimmable LED Bar

1

Ensures workspace is brightly and uniformly illuminated.

Black Work Mat

Foam mat for workspace

Black EVA foam

1

Non-slip surface for vials and rack; color matches simulation environment.

Centrifuge Vials

50ml with screw cap, clear plastic

Falcon tube or similar

1-4

Props manipulated by robot; clear sides allow for visual consistency with simulation.

Vial Rack

Yellow, fits 4+ vials, similar to simulation asset

3D printed in yellow - models available here

1

Holds vials upright, target for pick and place. Yellow color to match digital twin is best, as low as 5% infill can work.

USB-C Charging Block

To power the light

Anker 25W USB-C Charging Block

as needed

21W or greater. Sufficient power for all lights and accessories; ensure safety and compliance with device specs.

USB-C Cable

To power the light

USB-C to USB-C cable, 6ft

1

Suggested light above is battery powered, but this will keep it powered

(optional) Foam board joints

To assemble lightbox

3D printed, model here

8

Allows assembly of lightbox without tearing the foam board during disassembly. Alternatively, you can use tape.

Props
Approximate cost: $20 USD.

Item

Description

Model/Specs

Quantity

Details

Centrifuge Vials

50ml with screw cap, clear plastic

Falcon tube or similar

1-4

Props manipulated by robot; clear sides allow for visual consistency with simulation.

Vial Rack

Yellow, fits 4 vials, same model used to create simulation USD asset

3D printed, model here

1

Holds vials upright; color/shape should closely match digital asset.

Build the Workspace
In short, we’ll:

Cut the foam board to size

Cut a hole for the external camera

Mount the light

Clamp and position the props and robot.

Assemble the Lightbox
Cut 2 of the 5 foam board panels down to 20” x 20” (50.8 cm x 50.8 cm). These will become the sides.

On one of the 20” x 20” (50.8 cm x 50.8 cm) panels, cut a rectangular hole for the external camera. The Logitech webcam arm is approximately 5 cm × 1.5 cm — size the hole to slide it through snugly.

Now assemble the box - there are two options:


Option A — Tape (fast)
White duct tape or gaffer tape along the seams.

Pros: cheap, fast, no tools required

Cons: removing the tape later will damage the foam board

Keep foam board edges flush when taping. Running tape along the full length of each seam produces the strongest bond; small pieces work but are weaker.


Option B — 3D-printed corners (reusable)
Camera Placement Measurements
Camera placement diagram
Camera placement diagram
Parameter

Value

Height

40 cm from back of lightbox

Distance from back wall

27 cm from back of robot to center of camera lens

Angle

45 deg downward, aimed at the workspace. Make sure the camera has a good view of both the robot, the vials, and the rack.

Tip

Verify the camera view matches the sample images before finalizing the slot position. A few centimeters of error is acceptable; large deviations change what the policy sees and degrade performance.

Set Up the Light
The light should be bright, diffuse, and daylight-temperature. If you use the lights listed in the BOM, they are already diffuse.

Warning

These lights can get warm over extended use. Do not leave them on overnight, and monitor temperature during long sessions.


Foam board top — interior mount
If you use foam board for the top panel, mount a diffuse panel light inside the lightbox facing down. Zip ties through small holes in the foam board are the most reliable attachment; tape can work but may release from heat.


Open top — external mount
Turning on and adjusting lightbox lighting
Turn on the light and set brightness before teleoperation or policy runs.
Press the power button on the light.

Press and hold the power button again until the travel lock progress bar completes and the light stays on.

Use the brightness controls; for evaluations and data collection, target roughly 50–100 %.

Plug in the light if AC power is available; battery-only runs may not last a full session.

Mount the Robot
Clamp the SO-101 to a solid table. Position it so the base sits inside the lightbox at the position shown in the reference photo below.

This gives it good range-of-motion and lets the external camera see the robot well.

Verify the clamps do not restrict the robot’s range of motion—test by manually moving each joint through its range before powering on.

Lightbox

Arrange the Mat, Vials, and Rack
Our simulation environment and checkpoint models are overfit to the rack generally being on the left side and vials on the right. Use the reference photo above for positioning.

If you customize the Isaac Lab environment we’ll use later, you could try out other configurations!

Rack Placement Measurements
Place the foam mat flat under the vials, and scatter 1–3 vials on the mat in varied poses (same general layout as in simulation).

Physical Layout Checklist
Before you place the robot in the enclosure or run any real-robot software:

Enclosure — Lightbox panels assembled; interior clear of stray objects.

Mat and props — Foam mat flat; yellow rack in its designated spot; 1–3 vials on the mat in varied poses (same general layout as in simulation).

Cameras — Wrist and external cameras mounted and aimed so both the mat/rack and gripper workspace are visible; no heavy occlusion or glare.

Cables — Route camera and robot cables so they do not snag or limit joint motion (cables can create false calibration limits; see Troubleshooting, Calibration Fails).

Lighting — Light on and bright enough (previous section).

Re-check this checklist before Real Evaluation and before each Strategy 2 / Strategy 3 deployment if anything was moved.

Key Takeaways
Workspace setup is critical for successful training and deployment.

---
Get the Code and Models
In this module, you’ll clone the workshop repository and build the Docker containers used throughout the rest of the course.

The current version of this content uses:

Isaac Sim 5.1.0

Isaac Lab 2.3.0

LeRobot 0.4.3

GR00T N1.6

Clone the Repository
git clone https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop.git
cd Sim-to-Real-SO-101-Workshop
Build the Teleop and Simulation Container
docker build -t teleop-docker -f docker/sim/Dockerfile .
Build the Real Robot and Inference Server
This build takes significantly longer than the teleop container.


Blackwell GPUs
For NVIDIA GPUs based on the Blackwell architecture (e.g. RTX PRO 6000):

./docker/real/build.sh blackwell

Ada GPUs
Get the Models
You can either download these now, or as you go.

From the root of the course repository:

mkdir -p models
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left

hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real

hf download aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02 \
  --local-dir ./models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02

hf download aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70 \
  --local-dir ./models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
---
Calibrating the SO-101
In this session, you’ll power up the SO-101 robot, run through the calibration process, and verify the calibration is correct.

While calibration can be a bit tedious, it is essential for accurate robot control and for our AI model to perform well.

Tip

If you encounter hardware issues during this session, see the Troubleshooting Guide for solutions to common problems.

Learning Objectives
By the end of this session, you’ll be able to:

Power on and safely operate the SO-101 robot arm

Calibrate the teleop and robot arms for accurate positioning

Safety Guidelines
Review the Safety protocol before powering on the robot.

Workspace Setup
You should already have assembled and staged the physical task environment in Building the Workspace. Keep that lightbox layout, lighting, mat, vials, and rack consistent while you power on, calibrate, and teleoperate here—and again whenever you run real-robot evaluation later.

Powering On the Robot
Physical Inspection
Before powering on:

Inspect the robot for any visible damage

Verify all cables are securely connected

Warning

The teleop arm uses a lower voltage power supply (5V) compared to the follower (12V).

It is very important to not mix these up.

We recommend labeling or color coding them, so it’s easy to tell them apart.

Connect the power cables.

Verify the power LED illuminates on the control board at the back of the robot.

Run the Docker Container for This Course
When USB devices are plugged and re-plugged, the port assignments from your operating system may change.

Use the LeRobot port finder to find the address assigned to the robot, and to the teleop arm. After you’ve found the ports, we’ll assign them to environment variables in your terminal. This way when we run commands, we don’t have to keep typing the ports manually.

Open a new terminal window (CTRL+ALT+T).

Run the teleop-docker container:

xhost + 
docker run --name teleop -it --privileged --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
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
   -v ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/env:/root/env \
   -v ~/sim2real/Sim-to-Real-SO-101-Workshop:/workspace/Sim-to-Real-SO-101-Workshop \
   teleop-docker:latest
Identify the Teleop Arm Port
Run this command to start port identification:

lerobot-find-port
The tool will prompt you to remove the USB cable from the robot and press Enter when done. Let’s start with the teleop arm.

Finding all available ports for the MotorBus.
['/dev/ttyACM0', '/dev/ttyACM1']
Remove the usb cable from your MotorsBus and press Enter when done.
After removing the cable, press Enter.

The port of this MotorsBus is '/dev/ttyACM2'
Reconnect the USB cable.
In this example, /dev/ttyACM2 is the port assigned by the host computer.

Using this info, set environment variables for the teleop arm - make sure to make the port match the output of the last command.

setenv TELEOP_PORT=/dev/ttyACM # !! make sure to update
setenv TELEOP_ID=orange_teleop # use this line as-is
Note

We are using a special method called setenv to export the environment variables, this will help us keep them persistent across sessions and across containers. The variables will be saved into the ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/env file

Identify the Robot Arm Port
Repeat again for the robot arm, and note the port.

lerobot-find-port
Using this info, set environment variables for the robot arm - make sure to make the port match the output of the last command.

setenv ROBOT_PORT=/dev/ttyACM # !! make sure to update
setenv ROBOT_ID=orange_robot # use this as-is
Note

The ID determines where calibration data is stored (~/.cache/huggingface/lerobot/calibration). Use consistent IDs across sessions so calibration persists.

(Optional) to double check the values, run this command and confirm the values are what you expect.

echo "Teleop port is ${TELEOP_PORT} with id ${TELEOP_ID}"
echo "Robot port is ${ROBOT_PORT} with id ${ROBOT_ID}"
Keep this terminal open.

If you close it, restart the docker container and reset these environment variables. It’s a good idea to write down these ports in a notebook, if you have it.

Important

If you re-connect multiple USB cables at once, the ports may change. These common tasks can be easily re-found on the Quick Reference page. You can identify which port corresponds to which arm by disconnecting one and pressing Enter.

Calibration Process
Calibration ensures that the leader and follower arms have the same position values when they are in the same physical position.

The process is the same for both arms, just a slightly different command.

Don’t worry, calibrating the SO-101 is a simple process once you’ve done it a few times.

Let’s start by calibrating the teleop arm.

Calibrate the Teleop Arm (Leader)
Run the calibration command for the leader arm (the robot that teleoperates). Make sure you have already assigned $TELEOP_PORT in the earlier step.

lerobot-calibrate \
    --teleop.type=so101_leader \
    --teleop.port=$TELEOP_PORT \
    --teleop.id=$TELEOP_ID
The calibration script output will guide you through the process:

Move to the middle of the range: When instructed, manually move each joint to the middle of its range of motion. This is what that looks like:

Teleop Arm Calibration Pose Example
Teleop Arm: Calibration Pose Example
Important

Pay particular attention to the wrist axis here. This axis uses almost the entire motor rotation, so if it’s not properly centered, you may encounter encoder overflow / underflow. Note how the gripper handle is oriented.

We added two black dots to the gripper to help you find this position. Otherwise, just make your robot match the image.

Once you’ve confirmed the neutral pose, press Enter to begin calibration process.

Move each joint through its entire range of motion, moving until the joint stops or hits its end point. You can repeat to make sure you found it.

Teleop Arm Calibration Process Animation
Animated example: Teleop Arm Calibration process. Move each joint to the center, confirm, then sweep to end stops one by one to complete calibration.
Hit Enter when done.

Tip

We recommend moving each joint through its entire range, one by one, to ensure you’ve met its full range of motion and didn’t miss one.

It’s okay to move an axis more than once. The script records min and max positions for each joint.

And if you make a mistake or aren’t sure, you can always run the calibration again.

Calibrate the Follower Arm (Robot)
This is the same process, the command flags just change to reflect the follower arm.

Run the same command, but note the change in arguments:

lerobot-calibrate \
    --robot.type=so101_follower \
    --robot.port=$ROBOT_PORT \
    --robot.id=$ROBOT_ID
Move the robot to the calibration pose. This is what that pose looks like. Each joint is in the middle of its range of motion.


Calibration Pose Example


Pay particular attention to the wrist axis here. This is what the centered position looks like. This axis uses almost the entire motor rotation, so if it’s not properly centered, you may encounter encoder overflow / underflow.

Press Enter to begin calibration.

Move the robot through its entire range of motion, moving until the joint stops or hits its end point. You can repeat to make sure you found it.

Tip

True end stops only. Move each joint until it reaches its mechanical end stop, not a cable or obstacle. If a cable is pinched between links or the robot hits a cable, you will record a false min/max limit and calibration will be wrong. Check cable routing so the arm can reach its real limits.

Hit Enter when done.

Full SO-101 Calibration Sequence
Full calibration workflow example: moving all joints through their ranges on the SO-101.
The calibration file will then be saved in the ~/.cache/huggingface/lerobot/calibration directory, using the type for the folder name, and the id parameter as the filename.

Warning

Calibration File Warning

When running the robot after calibration, you may see this message if the calibration file is not correct for your robot. If you are recalibrating, this message is expected and you can proceed.

Press ENTER to use provided calibration file associated with the id leader_arm_1, or type 'c' and press ENTER to run calibration
Take caution when you see this message. It may indicate:

The calibration file is not correct for your robot

The robot and teleop arm are mixed up (wrong ID assignment)

A previous calibration that doesn’t match the current hardware state

When in doubt, press CTRL+C to cancel the command, and double check the robot assignments. If they are correct, you can run the calibration again.

Check Your Work
How do you know if your calibration is correct?

We have a small script that will compare your calibration to a small dataset of calibrations we collected.

Run this command:

python docker/real/scripts/so101_check_calibration.py 
Example output:

============================================================================
  SO101 CALIBRATION CHECK REPORT
  File:  /root/.cache/huggingface/lerobot/calibration/robots/so101_follower/orange_robot.json
  Stats: /workspace/Sim-to-Real-SO-101-Workshop/real_robot/calibration_stats.json
============================================================================

[1] Motion Range vs Stats (threshold ±2.0σ)

  Joint               Range     Mean    Std  Deviation    Offset  Status
  --------------------------------------------------------------------------
  shoulder_pan         2718     2725     32     -0.23σ      -174  ✓ PASS
  shoulder_lift        2353     2350     77     +0.04σ       710  ✓ PASS
  elbow_flex           2230     2222      9     +0.90σ     -1659  ✓ PASS
  wrist_flex           2331     2329     17     +0.11σ      -330  ✓ PASS
  wrist_roll           3857     4026    114     -1.48σ      -555  ✓ PASS
  gripper              1483     1475     33     +0.23σ      -845  ✓ PASS

[2] Live Encoder Positions

  Joint               Position    Calibrated Range     In Range
  --------------------------------------------------------------------------
  shoulder_pan            2174       857 – 3575       ✓ OK
  shoulder_lift            888       872 – 3225       ✓ OK
  elbow_flex              3059       861 – 3091       ✓ OK
  wrist_flex              1871       838 – 3169       ✓ OK
  wrist_roll               100       77 – 3934        ✓ OK
  gripper                 1763      1727 – 3210       ✓ OK

============================================================================
  Overall: ✓ PASS — calibration looks good.
============================================================================
Make sure you see Overall: ✓ PASS — calibration looks good. in the output. If not, try re-calibrating.

Tip

If you need help, see the Troubleshooting Guide for common issues and diagnostic steps.

Key Takeaways
Proper calibration is essential for sim-to-real correspondence

LeRobot provides unified commands for robot control

Always verify hardware before data collection or deployment
---
Operating the SO-101
In this session, you’ll teleoperate the SO-101 using the leader arm, configure cameras, and run teleoperation with live camera views in Rerun.

This will give you hands-on practice operating the robot in general, but also with this specific task.

Make sure you have completed Calibrating the SO-101 first. You’ll need a calibrated robot and the Docker container running with environment variables set.

Tip

If you encounter hardware issues during this session, see the Troubleshooting Guide for solutions to common problems.

Learning Objectives
By the end of this session, you’ll be able to:

Teleoperate the robot using the teleoperation arm

Configure cameras so you can teleoperate using the same camera views our AI models will use, and Rerun for debugging

Safety
Before powering on or running policies:

Keep hands clear of robot pinch zones while motors are enabled.

Verify cables are routed to avoid snagging during motion.

Be ready to stop execution with CTRL+C or unplug power cables if needed.

Re-check workspace placement after moving any equipment.

Teleoperation
Now that both arms are calibrated, we’re ready to begin teleoperating!

Begin the teleoperation process. It’s a good idea to make sure both arms are in similar poses, because the robot will move to match the teleop arm.

lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=$ROBOT_PORT \
    --robot.id=$ROBOT_ID \
    --teleop.type=so101_leader \
    --teleop.port=$TELEOP_PORT \
    --teleop.id=$TELEOP_ID
Move the teleop arm and watch how the robot arm moves to match.

Try to pick up a vial and place it in the rack!

Press Ctrl+C in the terminal to stop the teleoperation.

Camera Setup
The teleoperation you just did used an incredible vision system: your human perception system.

Our AI model will not have this information, so we need to use the cameras instead when we collect demonstrations.

Each robot workspace today is equipped with two cameras:

Gripper camera: Mounted on the robot’s wrist/gripper

External camera: Stationary camera viewing the workspace from above or the side

And because the policy works off of these visual images, camera assignment is critical to policy performance. If they are swapped (gripper cam thinks it’s the external cam, or vice versa), the policy will fail.

Finding Available Cameras
Similar to the port finder, LeRobot has a tool for identifying available cameras.

We need to determine the id of both the camera on the robot, and the external stationary camera.

Make sure the two cameras’ USB cables are plugged into your computer.

Run the command:

lerobot-find-cameras opencv
This command captures an image from each available camera, allowing you to determine the index of each camera.

Example output:

Searching for cameras...
Found 3 cameras:
  Camera 0: /dev/video0 (USB 2.0 Camera)
  Camera 1: /dev/video2 (USB 2.0 Camera)  
  Camera 2: /dev/video4 (Integrated Webcam)
  
Capturing test frames...
  Camera 0: 640x480 @ 30fps - saved to ./camera_test/cam_0.jpg
  Camera 1: 640x480 @ 30fps - saved to ./camera_test/cam_1.jpg
  Camera 2: 1280x720 @ 30fps - saved to ./camera_test/cam_2.jpg
Open a new terminal outside of the docker container.

Navigate to the task repository:

cd ~/Sim-to-Real-SO-101-Workshop
Run this command to open the folder with the images:

open ./outputs/captured_images
Open each image, and note which index correlates to wrist and stationary camera. For instance opencv__dev_video0.png indicates an index of 0.

Return to the terminal inside the teleop-docker container.

Assign these to environment variables in your terminal - make sure to update the values to match what you saw in the last command.

setenv CAMERA_GRIPPER=4 # make sure to update to your values
setenv CAMERA_EXTERNAL=6 # make sure to update to your values
Important

Camera Index Warning

Camera indices may change any time cameras are unplugged or replugged into your computer. Always verify camera assignments before collecting data or running policies.

If you see unexpected behavior during teleoperation or policy execution, camera index reassignment is a common cause.

Tip

Having camera or hardware issues? See the Troubleshooting Guide, also available on the sidebar, for common solutions and detailed diagnostic steps.

See the Quick Reference for common commands.

Note

Notice what makes this task challenging:

the gripper camera becomes occluded after grasp

the rack requires precise placement

lack of depth data makes rack alignment difficult

Run Teleoperation With Cameras
Now that we have the camera indices, we can run teleoperation with the real cameras in your workspace.

Run the command:

lerobot-teleoperate \
  --robot.type=so101_follower \
  --robot.port=$ROBOT_PORT \
  --robot.id=$ROBOT_ID \
  --teleop.type=so101_leader \
  --teleop.port=$TELEOP_PORT \
  --teleop.id=$TELEOP_ID \
  --display_data=true \
  --robot.cameras='{
    "wrist": {
      "type": "opencv",
      "index_or_path": '"$CAMERA_GRIPPER"',
      "width": 640,
      "height": 480,
      "fps": 30
    },
    "front": {
      "type": "opencv",
      "index_or_path": '"$CAMERA_EXTERNAL"',
      "width": 640,
      "height": 480,
      "fps": 30
    }
  }'
Rerun Viewer Teleop Example
Rerun Viewer Teleop Example
This will launch the teleoperation interface. You should see two cameras, one on the wrist and one externally mounted on the lightbox. Make sure your camera views and props roughly match this setup.

This is a valuable tool for both teleoperation and debugging.

Now using the Rerun viewer that opened, try picking up vials and placing them in the rack only using the camera views, not your eyes. See if your partner and you can perform the task a few times.

We’ll spend some time here - try to do several picks. Emphasize smooth, direct movements.

Press Ctrl+C to stop the teleoperation.

Close the Rerun viewer if it’s still open.

Key Takeaways
Camera assignment directly affects policy performance

How tricky this task is - gripper camera becomes occluded after grasp, external camera provides continuous visibility

The Rerun viewer is a valuable debugging tool for verifying camera views and robot state

Resources
SO-101 Getting Started Guide — Full assembly, motor setup, and calibration instructions

Rerun — A tool for visualizing camera views and robot actions
---
Sim-to-Real Strategy 1: Domain Randomization
Now that you’ve done teleoperation on a real robot, let’s try it in simulation with Isaac Lab.

In this module, you’ll use the teleop arm to drive a simulated SO-101 robot, allowing us to collect demonstrations with Isaac Lab.

Because it’s simulation, we have control of the world and can manipulate it in interesting ways, like using domain randomization to ensure our dataset will be sufficiently varied.

Teleoperation in Simulation
Teleoperation in Simulation
Learning Objectives
By the end of this session, you’ll be able to:

Explain domain randomization and why it improves sim-to-real transfer

Collect demonstration data through teleoperation, in simulation

Apply domain randomization to augment demonstrations

What Is Domain Randomization?
Domain randomization (DR) is a sim-to-real strategy based on this idea: instead of making simulation perfectly match reality, randomize simulation parameters during training so the policy becomes robust to any value in the range, including real-world values.

Put in simple terms: think about how you might learn to catch a ball.

If you always catch it in the same pose, you might not learn to reach and catch the ball, or hold the glove in different orientations. By varying where the ball is thrown to you when you practice, you will likely learn a better “policy” for catching the ball.

Teleoperation: Collecting Human Demonstrations
In this lesson we’ll apply domain randomization during teleoperation. We will use these to perform a kind of robot learning known as imitation learning.

Hands-On: Collecting Demonstrations
Here is a video of the task:

Teleoperation example in the LeRobot Dataset Visualizer
Example: Teleoperation of SO-101, being replayed through the LeRobot Dataset Visualizer.
On top are the observations from cameras, and below are the positions of robot joints.
See this dataset on Hugging Face, using the Dataset Visualizer

Tip

Having trouble with cameras or robot connection? See the Troubleshooting Guide.

Launch Simulation Environment (Docker)
If you still have the teleop-docker container’s terminal open from the last module, you can skip this step. If not, expand the dropdown and run the command.

Practice Teleoperation in Simulation
Let’s launch the simulation environment to practice teleoperation without recording.

This is a good way to get familiar with the teleop controls and camera views before collecting data.

(Optional) Run this quick sanity check to make sure your environment variables are set correctly.

echo "Teleop port is ${TELEOP_PORT} with id ${TELEOP_ID}"
If they aren’t set, find the ports using lerobot-find-port and assign them again:

Move the teleop arm to a packed position. If the robot is in a strange starting position, it may run into items in simulation on startup.

Run the following command to open Isaac Lab, with our pre-configured simulation environment. You can choose between two options: Lerobot-So101-Teleop-Vials-To-Rack which has no domain randomization or Lerobot-So101-Teleop-Vials-To-Rack-DR, which has domain randomization enabled.

lerobot_agent --task Lerobot-So101-Teleop-Vials-To-Rack-DR
This will launch Isaac Sim and load the training environment.

Note

The first time this launches, it will take about 2 minutes to load.

If it gets stuck, check the console for errors. It’s likely the robot isn’t fully connected. Power cycle the robot (plug/replug power on the back) if you have issues.



Keep Isaac Lab open for the next step.

Setup Cameras
We need our simulation to show us the same camera views our AI model will use.

When doing teleoperation for training VLAs, it’s crucial that we use the same camera views for teleoperation that the model will use for autonomous operation.

Otherwise, we may introduce biases or advantages the model won’t have.

Important

Only look through the gripper and external cameras when teleoperating.

When looking at the scene with your own eyes, or other cameras in the simulation scene, you may introduce perceptual affordances that the model will not have access to during inference.

The policy will only see what the cameras see. Train yourself to rely solely on the camera views displayed on your screen. This ensures your demonstrations reflect what the policy can actually perceive.

By default you’ll just see the general perspective camera. Let’s fix that.

Go to Window > Viewports, and enable both viewport Viewport 1 and Viewport 2 so we can see two cameras rendered at once.

 

In one viewport, go to the camera menu, and choose the gripper_cam.



In the other viewport, go to the camera menu, and choose the Camera_OmniVision_9782_Color camera.

For each viewport, set the aspect ratio to 4:3 to match the cameras.

Go to the settings menu in the viewport.

Under Viewport > Aspect Ratio on the right side you’ll see 16:9. Change it to 4:3.  

Now try teleoperating, and take some time to get familiar with the teleop controls and camera views before collecting data in episodic format.

Press R to reset the environment with domain randomization. If it doesn’t work, click on the viewport to give the application focus, and try again.

Notice in the terminal, you will see status updates about the subtask success, such as when the vials are grasped or placed in the rack.

Controls (click in Viewport to use these commands)

Press R to reset the environment (also stops recording)

Episodes are queued for processing while you continue working

When finished, stop Isaac Lab by pressing CTRL+C in the terminal.

Start Recording Demonstrations
When ready to collect data, we’ll add a few extra arguments for where to save the data we collect.

Before launching the teleop agent, set your Hugging Face username as an environment variable. This is used to organize your datasets in a unique namespace.

If you don’t have one, or don’t want to login, you can make up a username for local data collection.

Run this, replacing your-hf-username with your actual Hugging Face username:

export HF_USER=your-hf-username
You only need to do this once per terminal session before running the following commands. Feel free to use a made up username if you don’t want to login and upload your demos.

Overall Flow
For each episode we will:

Reset the environment: Press R to randomize vial positions, rack position, camera poses, and lighting. You can do this every episode, or every few episodes.

Record: Press S to start recording.

Execute: Immediately begin the demonstration. For each episode, perform one pick-and-place operation, which means picking up one vial and placing it into one open slot on the rack.

Complete: Press S to stop recording

How many demonstrations should you collect? If you’re going to train your own policy, try collecting at least 70 demonstrations based on our experience. More could be better. If you’re just exploring, you can collect less.

Demonstration Quality Guidelines:

Good demonstrations:

Smooth, deliberate motions

Clear grasp contact with vial

Successful placement in rack

Avoid:

Jerky, hesitant motions

Missed grasps or drops

Including more than the actual task execution

Recording Demonstrations
Launch recording session. This will be just like the environment before, but we have additional controls to cancel, start recording, and stop recording.

lerobot_agent --task Lerobot-So101-Teleop-Vials-To-Rack-DR \
    --repo_id ${HF_USER}/so101_teleop_vials \
    --repo_root $(pwd)/datasets/so101_teleop_vials \
    --task_name "Pick up the vial and place it in the rack"
Set up the window, viewports, and cameras (same as in Practice Teleoperation):

Window > Viewport: Enable both viewports so you see two camera views at once.

In one viewport, open the camera menu and choose gripper_cam.

In the other viewport, open the camera menu and choose Camera_OmniVision_9782_Color.

For each viewport: open the viewport settings, go to Viewport > Aspect Ratio, and set to 4:3 (instead of 16:9).

Recording Controls: Isaac Sim viewport must be in “focus” (click the app’s UI)

Press S to start/stop recording an episode

Press C to cancel the current recording (useful for mistakes)

Press R to reset the environment (also stops recording)

Completed episodes are queued for processing so you can continue working.

Example terminal output:

[INFO]: Started recording.
[INFO]: Stopped recording.
[INFO]: Copy episode to CPU...
[INFO]: Episode added to queue.
[INFO]: [ASYNC] received episode from queue...
[INFO]: Cleared buffers
Repeat the recording process until you have collected the desired number of demonstrations.

When completely finished with all demonstrations, make sure you see the message [INFO]: No More episodes in queue. Wait a few seconds if you don’t see it. This means all the episodes have been processed and saved.

Stop Isaac Lab by pressing CTRL+C in the terminal.

Review Collected Data
Optional: if you recorded a demonstration, use the LeRobot dataset visualizer to review your recorded episodes:

lerobot-dataset-viz \
    --repo-id ${HF_USER}/so101_teleop_vials \
    --root $(pwd)/datasets/so101_teleop_vials \
    --episode-index 0
Change --episode-index to view different episodes.

Domain Randomization in Simulation
To maximize domain randomization benefits, collect demonstrations across multiple sessions. The environment randomizes conditions between episodes automatically.

Let’s take a look at the code.

Code Tour: Domain Randomization Implementation
The Isaac Lab environment implements DR through reset event handlers. Here’s a tour of the key randomization methods from the teleop environment codebase.

In the workshop repo, these randomizations are applied in DR task variants (for example, Lerobot-So101-Teleop-Vials-To-Rack-DR). The base Lerobot-So101-Teleop-Vials-To-Rack task keeps the sky light off and uses a fixed orange robot color.

Lighting Randomization (randomize_sky_light)

File: sim_to_real_so101/source/sim_to_real_so101/mdp/resets.py

Randomizes the environment’s dome light on each reset—exposure, color temperature, and HDRI texture:

def randomize_sky_light(
    env,
    env_ids: torch.Tensor | None,
    exposure_range: tuple[float, float],
    temperature_range: tuple[float, float],
    textures_root: str,
    asset_cfg: SceneEntityCfg = None,
):
    # Sample random exposure and color temperature
    exposure = math_utils.sample_uniform(*exposure_range, (1,), device="cpu").item()
    temperature = math_utils.sample_uniform(*temperature_range, (1,), device="cpu").item()

    # Select random HDRI texture from available options
    textures = glob.glob(os.path.join(textures_root, "*.exr"))
    texture = textures[torch.randint(0, len(textures), (1,)).item()]

    # Apply to the dome light
    prim.GetAttribute("inputs:exposure").Set(exposure)
    prim.GetAttribute("inputs:colorTemperature").Set(temperature)
    prim.GetAttribute("inputs:texture:file").Set(Sdf.AssetPath(texture))
Camera Pose Randomization (randomize_camera_pose)

File: sim_to_real_so101/source/sim_to_real_so101/mdp/resets.py

Adds small position and rotation offsets to the external camera:

def randomize_camera_pose(
    env,
    env_ids: torch.Tensor | None,
    prim_path_pattern: str,
    pos_range: dict[str, tuple[float, float]] = None,  # e.g., {"x": (-0.02, 0.02)}
    rot_range: dict[str, tuple[float, float]] = None,  # e.g., {"pitch": (-0.05, 0.05)}
):
    # Sample random offsets relative to USD default pose
    x = base_pos[0] + math_utils.sample_uniform(*pos_range.get("x", (0, 0)), (1,)).item()
    y = base_pos[1] + math_utils.sample_uniform(*pos_range.get("y", (0, 0)), (1,)).item()
    z = base_pos[2] + math_utils.sample_uniform(*pos_range.get("z", (0, 0)), (1,)).item()
    
    # Combine base quaternion with random delta rotation
    delta_quat = math_utils.quat_from_euler_xyz(roll, pitch, yaw)
    final_quat = math_utils.quat_mul(base_quat_tensor, delta_quat)
Object Pose Randomization (reset_vials_rack)

File: sim_to_real_so101/source/sim_to_real_so101/mdp/resets.py

Randomizes vial and rack positions, with probability of pre-placing vials in slots:

def reset_vials_rack(
    env,
    env_ids: torch.Tensor,
    vials: list[str],
    rack: str,
    rack_pose_range: dict[str, tuple[float, float]],
    pose_range: dict[str, tuple[float, float]],
    rack_placement_prob: float = 0.33,
):
    # Randomize rack position and orientation
    new_rack_positions, new_rack_orientations = random_asset_pose(
        env, env_ids, rack, rack_pose_range, {}
    )
    
    # With some probability, pre-place a vial in a random slot
    if torch.rand(1).item() < rack_placement_prob:
        vial_idx = torch.randint(0, len(vial_objects), (1,)).item()
        slot_idx = torch.randint(0, total_slots, (1,)).item()
        # Transform slot position from rack local frame to world frame
        slot_position, slot_orientation = math_utils.combine_frame_transforms(
            new_rack_positions, new_rack_orientations, 
            slot_position_local, slot_orientation_local
        )
        vial.write_root_pose_to_sim(slot_pose, env_ids=env_ids)
Wiring It Up: Event Configuration

File: sim_to_real_so101/source/sim_to_real_so101/tasks/task_env_cfg.py

These randomization functions are registered as reset events in the environment config:

@configclass
class TaskEventCfg(EventCfg):
    
    reset_sky_light = EventTerm(
        func=randomize_sky_light,
        mode="reset",
        params={
            "exposure_range": (-4.0, 3.0),
            "temperature_range": (2500.0, 9500.0),
            "textures_root": f"{assets_path}/hdri",
            "asset_cfg": SceneEntityCfg("sky_light"),
        },
    )

    reset_camera_external_pose = EventTerm(
        func=randomize_camera_pose,
        mode="reset",
        params={
            "prim_path_pattern": "{ENV_REGEX_NS}/LightStudio/LightBox/camera_mount",
            "pos_range": {"x": (-0.02, 0.02), "y": (-0.02, 0.02), "z": (-0.01, 0.01)},
            "rot_range": {"roll": (-0.05, 0.05), "pitch": (-0.05, 0.05), "yaw": (-0.05, 0.05)},
        },
    )
Every time an episode resets, Isaac Lab calls each registered EventTerm with mode="reset", applying fresh randomization.

For this workshop migration, the mat yaw randomization range is tightened to (-0.1, 0.1) in DR task configs.

Tip

You can experiment with domain randomization by changing the ranges or which resets run. In task_env_cfg.py, the TaskEventCfg class registers each randomization as an EventTerm with a params dict. For example, adjust exposure_range or temperature_range in reset_sky_light, or pos_range / rot_range in reset_camera_external_pose, to widen or narrow variation. Commenting out an EventTerm disables that randomization.

Note where you’re editing - if inside the container, changes might be lost on restart.

Subtask Rating
Notice in the terminal output, that our simulation can detect when the vial is grasped, and when it is placed in the rack.

[GRASP] Vial grasped in env(s): [0]
[RELEASE] Vial released in env(s): [0]
[RACK] vial_2 placed in rack in env(s): [0]
This strategy is useful when we start policy inference, because we can automatically score how well the policy is performing.

Sim vs. Real Teleoperation Comparison
Aspect

Simulation

Real Robot

Domain randomization

Automatic

Manual, limited to what you can physically change in the environment

Data collection speed

Faster reset, parallel envs possible

Real-time only

Hardware wear

None

Accumulates over time

Visual diversity

Procedural generation

Requires manual variation

Physics accuracy

Approximated

Ground truth

When to Use Each
Use simulation when:

Building initial dataset with DR

Hardware is limited or shared

Exploring task or policy variations quickly and safely

Real environment isn’t ready, accessible, or during development

Use real robot when:

Collecting high-quality ground truth

Validating sim-trained policies

Capturing real-world nuances (friction, lighting)

Key Takeaways
Domain randomization makes policies robust by training on varied conditions

Teleoperation captures human expertise in demonstration form

Always teleoperate using only camera views—not your eyes

DR augmentation multiplies your dataset with varied conditions

Combined real demonstrations + DR augmentation is a powerful baseline
---
Isaac GR00T: Vision-Language-Action Models
In this session, we’ll explore the VLA model called NVIDIA Isaac GR00T, how it works, and see examples of it in action.

Learning Objectives
By the end of this session, you’ll be able to:

Explain what vision-language-action models are and why they’re powerful

Describe the GR00T architecture and its components

Understand how VLAs differ from traditional robot learning approaches

What Is GR00T?
NVIDIA Isaac GR00T (Generalist Robot 00 Technology) is a research initiative and development platform for developing general-purpose robot foundation models and data pipelines to accelerate humanoid robotics research and development.

It provides:

Pre-trained visual understanding from large-scale data

Language-conditioned behavior for flexible task specification

Action generation suitable for real-time robot control

In this course, we’ll use GR00T N1.6 models post-trained for the SO-101 robot.

Note

Training time in this course

GR00T post-training requires several hours on GPU hardware. We have pre-trained a set of policies on various datasets that you can use as a start. This lets you focus on understanding the workflow, evaluating results, and iterating on strategies rather than waiting for training jobs to complete.

The commands and scripts shown here are the same ones used to produce those policies, so you can replicate the process on your own hardware after you finish this learning path.

What Is a Vision-Language-Action Model?
Vision-Language-Action (VLA) models are foundation models that take visual input and language instructions and output low-level or mid-level actions for an embodied agent, such as a robot.

Input: Camera image (1 or more) + "Pick up the red vial and place it in the rack"
Output: Sequence of joint positions/velocities to execute the task
Defining Terminology
Understanding VLA Training Stages
VLA models are not trained in a single step. They go through distinct phases, each building on the previous one.

Understanding these stages helps explain how a model progresses from broad world knowledge to task-specific robot behavior, and why each phase matters for sim-to-real transfer.

Pre-training is the first and largest training phase. The model learns general representations from internet-scale data, including images, text, video, and increasingly, robot demonstrations.

No specific robot task is being taught yet. Instead, the model develops broad capabilities such as object recognition, spatial reasoning, and grounding language in visual context. You can think of this as building a world model before the model ever sees your specific robot task.

Post-training is the umbrella term for everything that happens after pre-training to make a general model useful for a specific robot, task, or environment.

This is where a pretrained foundation model is adapted to a specific embodiment and task using demonstrations that map observations and language instructions to robot actions. Post-training is computationally intensive and typically requires several hours on GPU hardware.

Note

This is the stage you run in this course: taking the pretrained GR00T N1.6 foundation model and adapting it to SO-101 data collected in simulation.

Fine-tuning is a specific form of post-training where you continue training on a smaller, targeted dataset to improve performance in a specific setting.

For example, after post-training on simulation data, you might fine-tune on a small set of real-robot demonstrations to reduce the sim-to-real gap. Fine-tuning aims to preserve general capabilities while adapting behavior to new conditions.

Inference is when the trained model runs in real time. It receives camera frames and a language instruction, then outputs joint position commands.

No learning happens during inference because model weights are frozen. Speed matters here. Techniques such as action chunking, where the model predicts multiple timesteps at once, reduce forward passes and produce smoother motion. On modern GPU hardware, this supports real-time closed-loop control.

Architecture Overview
VLA Model Architecture

Key Components
Vision Encoder: Processes camera images into rich feature representations

Pre-trained on large image datasets (ImageNet, etc.)

Understands objects, spatial relationships, affordances

Language Encoder: Processes task instructions

Maps natural language to task embeddings

Enables zero-shot generalization to new task descriptions

Cross-Modal Fusion: Combines vision and language

Attention mechanisms to relate visual features to language

Grounds language concepts in visual observations

Action Decoder: Generates robot actions

Conditioned on fused visual-language features

Outputs appropriate action representation (joint positions, velocities, etc.)

Action Space and Control
Action Representations
GR00T supports several action representations:

Joint Position Actions

Direct control over robot configuration

Requires learning full arm coordination

End-Effector Actions

Inverse kinematics computes joint commands

Abstracts away arm configuration

Action Chunking

Predict multiple future actions at once

Smoother execution, temporal consistency

In this course, we use joint position actions with action chunking.

Action Horizon Parameter
The action_horizon parameter controls how many future actions the model predicts at once. This is a critical hyperparameter that affects both training and deployment.

What it controls:

Training: The model learns to predict action_horizon timesteps into the future

Inference: The model outputs a chunk of action_horizon actions per forward pass

Trade-offs:

Horizon

Pros

Cons

Short (4-8)

More reactive, corrects quickly

Choppy motion, frequent replanning

Medium (16)

Balanced smoothness and reactivity

Good default for most tasks

Long (32+)

Very smooth trajectories

Slow to correct errors, may overshoot

Tip

Start with the default action_horizon=16. Only adjust if you observe specific issues: reduce if the robot overshoots targets, increase if motion is too jerky.

Example: GR00T in Action
Post-Training GR00T
set -x -e

export NUM_GPUS=1

DATASET_PATH= #set path to your model

# torchrun --nproc_per_node=$NUM_GPUS --master_port=29500 \
CUDA_VISIBLE_DEVICES=0 python \
    gr00t/experiment/launch_finetune.py \
    --base_model_path nvidia/GR00T-N1.6-3B \
    --dataset_path $DATASET_PATH \
    --modality_config_path examples/SO100/so100_config.py \
    --embodiment_tag NEW_EMBODIMENT \
    --num_gpus $NUM_GPUS \
    --output_dir /tmp/so100_finetune \
    --save_steps 1000 \
    --save_total_limit 5 \
    --max_steps 10000 \
    --warmup_ratio 0.05 \
    --weight_decay 1e-5 \
    --learning_rate 1e-4 \
    --use_wandb \
    --global_batch_size 32 \
    --color_jitter_params brightness 0.3 contrast 0.4 saturation 0.5 hue 0.08 \
    --dataloader_num_workers 4
Practical Considerations
Data Requirements
VLA training typically requires:

50-200 demonstrations per task for basic competence

Language annotations describing each demonstration

Diverse conditions to enable generalization

Tip

Quality matters more than quantity. 50 high-quality, diverse demonstrations often outperform 500 redundant ones.

Compute Requirements
GR00T training benefits from:

GPU memory: 24GB+ for full model training

Training time: 2-8 hours depending on dataset size

Inference: Real-time on modern GPUs (RTX 3080+)

Key Takeaways
VLA models combine vision, language, and action in a unified architecture

GR00T provides pre-trained components for accelerated learning

Language conditioning enables flexible task specification

Action chunking provides smooth, temporally consistent control

Pre-trained vision encoders enable visual generalization

Resources
NVIDIA Isaac GR00T GitHub — Source code, model weights, and documentation
---
Sim Evaluation
In this session, you’ll run policy evaluation in simulation using the same GR00T-based setup you’ll use later on the real robot.

Learning Objectives
By the end of this session, you’ll be able to:

Run policy evaluation in simulation using the GR00T server + client (Docker) setup

Compare how policies trained with different data quantities and augmentation behave

Identify common failure modes in simulation

What Policy Are We Going to Evaluate?
You’ll have the choice of either using policies we trained for you, or training your own. If you use ours, make sure the workspace is set up correctly and the robot is carefully calibrated.

Tip

To use GR00T with LeRobot, follow the official LeRobot GR00T documentation for setup and integration guides. GR00T N1.5 models are natively supported and can be evaluated directly within the LeRobot framework. For GR00T N1.6, integration into LeRobot is still in progress. In the meantime, you’ll need to run training and inference using the official Isaac GR00T repository or provided Docker images for the latest model features.

We used this dataset of 75 sim demonstrations. View it on Hugging Face with the dataset visualizer. This is a sim only dataset, meaning it was trained entirely in simulation, without any real-world data. Our first strategy is to rely solely on simulation and domain randomization.

Visualization of the SO-101 sim teleop vials-to-rack-left dataset
Sample episodes visualized from the sim-only demonstration dataset used for training evaluation policies.
Running Policy Evaluation in Simulation
Throughout this course, when we run evaluations there will be two terminals involved:

The host terminal, where we will start the GR00T container and policy server

The client terminal, where we will run the evaluation rollout and actually control the robot

For sim, the client is our simulator. For the real robot, our client is the robot itself.

Terminal 1 (real-robot container) — Start the GR00T policy server
Open a new terminal window (CTRL+ALT+T).

Run the docker real-robot container.

xhost +
docker run -it --rm --name real-robot --network host --privileged --gpus all \
    -e DISPLAY \
    -v /dev:/dev \
    -v /run/udev:/run/udev:ro \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
    -v ~/sim2real/models:/workspace/models \
    -v ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/env:/root/env \
    -v ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/real/scripts:/Isaac-GR00T/gr00t/eval/real_robot/SO100 \
    real-robot \
    /bin/bash
Inside this container, run the following to set which model to evaluate.

export MODEL=aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left/checkpoint-10000
Run the policy server with that model.

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
When you see Server is ready and listening on tcp://0.0.0.0:5555 the policy server is ready to accept connections.

Terminal 2 (teleop-docker container) — Evaluation rollout
If you still have the teleop-docker container’s terminal open from the last module, you can skip this step. If not, expand the dropdown and run the command.

This command will begin moving the robot in simulation, using an environment with less lighting variation to start.

lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --rerun
This will launch both Isaac Sim, and Rerun.

Note

The --rerun flag is optional.

It adds Rerun into the loop for debugging, so you can see joint actions and the camera feeds while the policy is running. This lets you confirm the camera views are reasonable and the assignments are correct.

(Alternatively) You can run the evaluation headlessly, meaning there is no Isaac Sim UI or Rerun visualization:

lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack" \
    --headless
Watching the Evaluation
Watch the terminal for evaluation of the model’s performance. The scene resets either after a timeout, or when the vial starts to enter the rack slots.

Depending on how much the vials roll around, and how dark the lighting is, expect the evaluation success rate to be between 50-70%.

Remember this dataset has a fairly low number of demonstrations (75 pick and place demos), so the policy may not be able to generalize as much as we’d ultimately need.

Visualization of the Evaluation rollout
Example output:

Rollout (ep 7, success: 66.7%):  33%|█████████████████████▉                                             | 131/400 [00:06<00:15][GRASP] Vial grasped in env(s): [0]
Rollout (ep 7, success: 66.7%):  70%|██████████████████████████████████████████████▉                    | 280/400 [00:14<00:06][RACK] vial_1 placed in rack in env(s): [0]
Rollout (ep 7, success: 66.7%):  70%|███████████████████████████████████████████████▏                   | 282/400 [00:14<00:06]
Rollout (ep 8, success: 71.4%):  34%|
Testing Against More Lighting Variation
We’ve preconfigured another environment with more lighting randomization. This is an example of how you can use simulation to stress test a policy against different conditions, by changing just a bit of code.

You can use that evaluation environment by running this command instead:

lerobot_eval \
    --task Lerobot-So101-Teleop-Vials-To-Rack-DR-Eval \
    --rename_map '{"external_D455": "front", "ego": "wrist"}' \
    --action_horizon 16 \
    --lang_instruction "Pick up the vial and place it in the yellow rack"
Cleanup
When you’re done trying model evaluations:

In the teleop-docker container, press CTRL+C to stop Isaac Lab.

In the same terminal, type exit and press Enter to exit the teleop-docker container.

In the real-robot container, press CTRL+C to stop the policy server. You can leave this terminal open.

Tip

If you want to see which containers are running, you can run docker ps to list all containers.

Common Failure Modes
When observing evaluation runs, notice the failure modes. Remember that this policy was trained from a limited amount of data, only 75 demonstrations (~1 hour of teleoperation time for a seasoned operator).

Key Takeaways
Policies trained on few demonstrations aren’t able to generalize

Domain randomization is essential for robust policies

More diverse training data beats more identical training data

These sim-only policies provide a baseline for comparison when you run on the real robot
---
Real Evaluation
In this session, you’ll run policy evaluation on the physical SO-101 robot using the same GR00T-based setup you used in simulation.

The client is now the real robot instead of the simulator!

Learning Objectives
By the end of this session, you’ll be able to:

Run policy evaluation on the real robot using the GR00T server + client (Docker) setup

Observe the sim-to-real gap firsthand

Stop and restart the evaluation safely

What Policy Are We Running?
We use the same policy you evaluated in simulation. The exact MODEL (checkpoint path) is set in the commands below.

Workspace Prep
Before running real-robot evaluation:

Place 1-3 vials on the mat and keep the rack in its reference location.

Ensure both cameras have a clear view of the workspace.

Turn on the light and set brightness (see Set Up the Light).

Running Policy Evaluation on the Real Robot
Throughout this course, when we run evaluations there will be two terminals involved:

The host terminal, where we start the GR00T container and policy server

The client terminal, where we run the evaluation rollout and actually control the robot

For sim, the client is our simulator. For the real robot, our client is the robot itself.

Terminal 1 (real-robot container) — Start the GR00T policy server
Locate the terminal already running the real-robot container.

Inside this container, run the following. This is where we choose which model to evaluate.

export MODEL=aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left/checkpoint-10000
Run the policy server with that model.

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
Terminal 2 (real-robot container) — Evaluation rollout
Open a second terminal. You will attach to the same real-robot container and run the robot client. This step assumes your robot has been calibrated already (likely you already did this).

Attach a second terminal to the real-robot container.

docker exec -it real-robot /bin/bash
Once inside the container, run the evaluation script:

python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py \
  --robot.type=so101_follower \
  --robot.port="$ROBOT_PORT" \
  --robot.id="$ROBOT_ID" \
  --robot.cameras="{
      wrist:  {type: opencv, index_or_path: $CAMERA_GRIPPER, width: 640, height: 480, fps: 30},
      front:  {type: opencv, index_or_path: $CAMERA_EXTERNAL, width: 640, height: 480, fps: 30}
  }" \
  --policy_host=localhost \
  --policy_port=5555 \
  --lang_instruction="Pick up the vial and place it in the yellow rack" \
  --rerun True
Note

The --rerun flag is optional.

It adds Rerun into the loop for debugging, so you can see joint actions and the camera feeds while the policy is running. This lets you confirm the camera views are reasonable and the assignments are correct.

Watching the Evaluation
Watch the robot and the terminal during execution. The policy will run until you stop it or it completes the evaluation. Watch closely but stay clear; note any unexpected behavior and be ready to intervene.

To stop the robot: Press CTRL+C in Terminal 2 (robot client). The policy server in Terminal 1 keeps running.

To run again: Simply run the command again python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py ... in Terminal 2

To switch model or fully restart:

Stop both terminals’ commands (CTRL+C)

Set MODEL environment variable to the model you want to evaluate

Restart the commands for each terminal (model server, robot client)

Note

At evaluation start, the robot will slowly rise to its initial pose, then enter into inference mode.

At robot stop (CTRL+C), it will slowly drive itself back to its home pose.

Tip

Keep the policy server running between evaluation attempts. Only restart it if you want to load a different model checkpoint.

Common Failure Modes
When observing real evaluation runs, notice how perception and actuation differ from simulation. The same policy may miss grasps, overshoot, or behave differently under real lighting and dynamics. These differences are the sim-to-real gap you’ll address with the strategies in the modules that follow.

Key Takeaways
Real robot evaluation uses the same GR00T server + client architecture as sim evaluation; only the client (robot vs. simulator) changes

The gap between sim and real performance is often visible immediately—perception and actuation both matter

Safe shutdown is CTRL+C in the robot client terminal first
---
Sim-to-Real Strategy 2: Co-Training With Real Data
In this session, you’ll learn the theory of co-training approaches and then deploy your first policy to the physical robot.

Learning Objectives
By the end of this session, you’ll be able to:

Explain co-training strategies for mixing sim and real data

Deploy trained policies safely to the physical SO-101 robot

Observe and document real-world policy behavior

Identify initial sim-to-real gap symptoms

What Is Co-Training?
Co-training combines data from multiple sources—simulation and real-world—during policy training.

In our examples, we’ll show the power of combining a small amount of real demonstration data (5 episodes) with a much larger set of simulation demonstrations (70-100).

You’ll have a chance to experience policies trained with various mixes of data.

Physical demonstration
Physical demonstration of the task with teleoperation.
Tip

View a dataset of real-only demonstrations using the Hugging Face Dataset Visualizer here.

The Data Challenge
Data Source

Quantity

Quality

Reality Match

Simulation

Abundant

Consistent

Approximate

Real teleop

Limited

Variable

Exact

Neither source alone is ideal:

Sim-only: Abundant but doesn’t match real-world distribution

Real-only: Matches reality but quantity is limited

Co-training leverages both.

(Optional) Collecting Real Demonstrations With LeRobot
We will provide both a real dataset and a post-trained GR00T model trained on this sim+real dataset. But if you’d like, you can collect your own real demonstrations below.

Note

Since you’ll likely use our dataset / model, for now this section is a bit less detailed.

Run the teleop-docker container.

Log into the hf cli application: hf auth login

Set your Hugging Face username as an environment variable.

export HF_USER=your-hf-username
Run the following command - make sure to set the dataset.repo_id argument.

lerobot-record \
  --robot.type=so101_follower \
  --robot.port=$ROBOT_PORT \
  --robot.id=$ROBOT_ID \
  --robot.cameras='{
    "wrist": {
      "type": "opencv",
      "index_or_path": '"$CAMERA_GRIPPER"',
      "width": 640,
      "height": 480,
      "fps": 30
    },
    "front": {
      "type": "opencv",
      "index_or_path": '"$CAMERA_EXTERNAL"',
      "width": 640,
      "height": 480,
      "fps": 30
    }
  }' \
  --teleop.type=so101_leader \
  --teleop.port=$TELEOP_PORT \
  --teleop.id=$TELEOP_ID \
  --display_data=true \
  --dataset.repo_id=${HF_USER}/so101-teleop-vials-to-rack-real \
  --dataset.num_episodes=5 \
  --dataset.single_task="Pick up the vial and place it in the yellow rack" \
  --play_sounds=false
Use these controls to control recording:

Press Right Arrow (→): Early stop the current episode or reset time and move to the next.

Press Left Arrow (←): Cancel the current episode and re-record it.

Press Escape (ESC): Immediately stop the session, encode videos, and upload the dataset.

Read more about LeRobot Record here: lerobot-record

Upload this dataset to the Hugging Face Hub: hf upload ${HF_USER}/so101-teleop-vials-to-rack-real

Merge this dataset with your simulation dataset.

Train GR00T on this merged dataset.

Hands-On: Deploy Co-Trained Policy to Robot
Now let’s deploy the sim-and-real co-trained policy to the physical robot—the same two-terminal GR00T server + client setup you used for sim and real evaluation earlier.

Tip

For hardware issues or unexpected policy behavior, consult the Troubleshooting Guide.

What Policy Are We Running?
We use the sim-and-real co-trained checkpoint: trained on both simulation demonstrations and a small set of real teleoperation episodes. The exact MODEL (checkpoint path) is set in the commands below; you can change it to evaluate a different strategy or checkpoint.

Workspace Prep
Review the Safety protocol before proceeding.

Verify robot connection: lerobot-find-port

Place 1–3 vials randomly on the foam mat; position the rack in its designated location

Ensure cameras have clear view of workspace and clear any obstacles

Turn on the lightbox to suitable brightness (see Building the Workspace if needed)

Running Policy Evaluation on the Real Robot
Throughout this course, when we run evaluations there will be two terminals involved:

The host terminal, where we start the GR00T container and policy server

The client terminal, where we run the evaluation rollout and control the robot

For real robot evaluation, the client is the physical robot.

Terminal 1 (real-robot container) — Start the GR00T policy server
Locate the terminal already running the real-robot container.

Inside this container, run the following. This is where we choose which model to evaluate (co-trained for Strategy 2).

export MODEL=aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real/checkpoint-10000
Run the policy server with that model.

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
Terminal 2 (real-robot container) — Evaluation rollout
Open a second terminal. You will attach to the same real-robot container and run the robot client.

On the host, attach to the container you started in the last step:

docker exec -it real-robot /bin/bash
Inside the container, run the evaluation script:

python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py \
  --robot.type=so101_follower \
  --robot.port="$ROBOT_PORT" \
  --robot.id="$ROBOT_ID" \
  --robot.cameras="{
      wrist:  {type: opencv, index_or_path: $CAMERA_GRIPPER, width: 640, height: 480, fps: 30},
      front:  {type: opencv, index_or_path: $CAMERA_EXTERNAL, width: 640, height: 480, fps: 30}
  }" \
  --policy_host=localhost \
  --policy_port=5555 \
  --lang_instruction="Pick up the vial and place it in the yellow rack" \
  --rerun True
Note

The --rerun flag is optional.

It adds Rerun into the loop for debugging, so you can see joint actions and the camera feeds while the policy is running. This lets you confirm the camera views are reasonable and the assignments are correct.

Watching the Evaluation
Watch the robot and the terminal during execution. The policy will run until you stop it or it completes the evaluation. Watch closely but stay clear; note any unexpected behavior and be ready to intervene.

To stop the robot: Press CTRL+C in Terminal 2 (robot client). The policy server in Terminal 1 keeps running.

To run again: Simply run the command again python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py ... in Terminal 2

To switch model or fully restart:

Stop both terminals’ commands (CTRL+C)

Set MODEL environment variable to the model you want to evaluate

Restart the commands for each terminal (model server, robot client)

Note

At evaluation start, the robot will slowly rise to its initial pose, then enter into inference mode.

At robot stop (CTRL+C), it will slowly drive itself back to its home pose.

Tip

Keep the policy server running between evaluation attempts. Only restart it if you want to load a different model checkpoint.

Key Takeaways
Co-training combines sim and real data for better policies

Safety is paramount when deploying to real hardware

Document observations systematically—they guide improvement

The sim-to-real gap is real and often significant

Different policies exhibit different failure modes

Resources
Isaac-GR00T Repository — Source code for GR00T deployment including SO-101 evaluation scripts

SO-101 Finetuning Guide — Full instructions for finetuning and evaluation

Sim-and-Real Co-Training: A Simple Recipe for Vision-Based Robotic Manipulation — RSS 2025 paper on co-training strategies
---
Sim-to-Real Strategy 3: Augmenting Datasets With Cosmos
In this session, you’ll learn how Cosmos can create diverse synthetic training data and deploy Cosmos-augmented policies to the real robot.

Learning Objectives
By the end of this session, you’ll be able to:

Explain how Cosmos and world models generate synthetic robot data

Deploy policies trained with Cosmos augmentation

Compare performance across different training data strategies

Beyond Domain Randomization and Co-Training
In Strategy 1, you used domain randomization to vary simulation parameters. This is effective, but limited:

Only varies what you explicitly randomize

Simulation rendering still looks “synthetic”

Can’t generate truly novel scenarios

Cosmos addresses these limitations through generative modeling.

What Is Cosmos?
Cosmos is NVIDIA’s world foundation model for physical AI. It can:

Generate realistic video sequences from prompts or initial frames

Simulate plausible physical interactions

Augment robot training data with diverse synthetic scenarios

How Cosmos Works
Input: Robot demonstration video + prompt
       "Same task, different lighting, different vial positions"

Cosmos generates: Multiple variations of the scenario
                  with consistent physics and new visual appearance

Output: Augmented training data with diverse conditions
Prompt:

prompt: Photorealistic first-person view from a robotic arm's orange claw-like gripper. The prongs are visible at the bottom edge, hovering over a heavily corroded, textured rusty steel plate showing oxidation and wear mat. To the left is a yellow rectangular vial rack; to the right, two white opaque centrifuge tubes with blue caps, filled with a white substance, lie horizontally. Plain white wall background with {bright, diffused clinical LED lighting. Sharp macro focus, realistic plastic finishes, and fluid mechanical motion.
{
  "name": "so101",
  "prompt_path": "prompt_test2.txt",
  "video_path": "ego_rgb_001.mp4",
  "guidance": 3,
  "depth": {
    "control_weight": 0.2,
    "control_path": "ego_depth_001.mp4"
  },
  "edge": {
    "control_weight": 1.0
  },
  "seg": {
    "control_weight": 0.3,
    "control_path": "ego_instance_id_segmentation_001.mp4"
  },
  "vis": {
    "control_weight": 0.1
  }
}
Cosmos Augmentation Example 1
Cosmos Augmentation Example 1
Key Capabilities
Visual Diversity

Photorealistic rendering variations

Natural lighting changes

Background and texture diversity

Scenario Variation

Object position changes

Different object instances

Environmental modifications

Physical Consistency

Maintains plausible physics

Preserves task structure

Coherent object interactions

Hands-On: Using Cosmos-Augmented Data
We’ve pre-generated Cosmos-augmented datasets for this learning path.

Compare to the DR-augmented data:

Notice the visual difference in rendering

Observe lighting and texture variations

Check for physical plausibility

Policies to Evaluate
Deploy a policy trained with Cosmos-augmented data using the same two-terminal GR00T server + client setup as in Strategy 2 and Real Evaluation.

Tip

See the Troubleshooting Guide for help with deployment issues.

What Policy Are We Running?
We have two Cosmos-augmented policies to test. Set MODEL in Terminal 1 to the checkpoint you want to evaluate:

Training Data Mix

Visualize Dataset

Model Checkpoint

75 sim episodes + 7 Cosmos-augmented episodes

visualize on Hugging Face

aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02/

75 sim episodes + 70 Cosmos-augmented episodes

visualize on Hugging Face

aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70

Workspace Prep
Same as Strategy 2: verify robot connection, place vials and rack, ensure cameras have a clear view, turn on the lightbox. See Building the Workspace, Strategy 2: Workspace prep, and Real Evaluation: Workspace prep.

Running Policy Evaluation on the Real Robot
Throughout this course, when we run evaluations there will be two terminals involved:

The host terminal, where we start the GR00T container and policy server

The client terminal, where we run the evaluation rollout and control the robot

For real robot evaluation, the client is the physical robot.

Terminal 1 (real-robot container) — Start the GR00T policy server
Locate the terminal already running the real-robot container.

Inside this container, run the following. Set MODEL to the Cosmos-augmented checkpoint you want to test (e.g. 75+70 Cosmos).

export MODEL=aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
Run the policy server with that model.

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py \
    --model-path /workspace/models/$MODEL
Terminal 2 (real-robot container) — Evaluation rollout
Open a second terminal. You will attach to the same real-robot container and run the robot client.

On the host, attach to the container:

docker exec -it real-robot /bin/bash
Inside the container, run the evaluation script:

python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py \
  --robot.type=so101_follower \
  --robot.port="$ROBOT_PORT" \
  --robot.id="$ROBOT_ID" \
  --robot.cameras="{
      wrist:  {type: opencv, index_or_path: $CAMERA_GRIPPER, width: 640, height: 480, fps: 30},
      front:  {type: opencv, index_or_path: $CAMERA_EXTERNAL, width: 640, height: 480, fps: 30}
  }" \
  --policy_host=localhost \
  --policy_port=5555 \
  --lang_instruction="Pick up the vial and place it in the yellow rack" \
  --rerun True
Note

The --rerun flag is optional.

It adds Rerun into the loop for debugging, so you can see joint actions and the camera feeds while the policy is running. This lets you confirm the camera views are reasonable and the assignments are correct.

Watching the Evaluation
Watch the robot and the terminal during execution. Compare behavior to the sim-only and co-trained policies: Cosmos-augmented policies may show different robustness to lighting and visual variation.

To stop the robot: Press CTRL+C in Terminal 2 (robot client). The policy server in Terminal 1 keeps running.

To run again: Simply run the command again python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py ... in Terminal 2

To switch model or fully restart:

Stop both terminals’ commands (CTRL+C)

Set MODEL environment variable to the model you want to evaluate

Restart the commands for each terminal (model server, robot client)

To Try the Other Policy Trained on Cosmos-Augmented Data
In terminal 1, press CTRL+C to stop the policy server.

In terminal 2, press CTRL+C to stop the robot client.

Set MODEL environment variable to the model you want to evaluate.

export MODEL=aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02/checkpoint-10000
Restart the policy server by running the same command again.

python Isaac-GR00T/gr00t/eval/run_gr00t_server.py --model-path /workspace/models/$MODEL
Run the robot client again by running the same command again.

python Isaac-GR00T/gr00t/eval/real_robot/SO100/so101_eval.py \
  --robot.type=so101_follower \
  --robot.port="$ROBOT_PORT" \
  --robot.id="$ROBOT_ID" \
  --robot.cameras="{
      wrist:  {type: opencv, index_or_path: $CAMERA_GRIPPER, width: 640, height: 480, fps: 30},
      front:  {type: opencv, index_or_path: $CAMERA_EXTERNAL, width: 640, height: 480, fps: 30}
  }" \
  --policy_host=localhost \
  --policy_port=5555 \
  --lang_instruction="Pick up the vial and place it in the yellow rack" \
  --rerun True
Note

At evaluation start, the robot will slowly rise to its initial pose, then enter into inference mode.

At robot stop (CTRL+C), it will slowly drive itself back to its home pose.

Tip

Keep the policy server running between evaluation attempts. Only restart it when you want to load a different model checkpoint.

Comparing Policies
After running the Cosmos-augmented policy, compare with your notes from Strategy 2 (co-trained) and your earlier real evaluation baseline (sim-only policy). Note whether Cosmos augmentation improves consistency, grasp success, or placement accuracy on the real robot.

Key Takeaways
Cosmos generates photorealistic synthetic data beyond DR capabilities

Different approaches address different aspects of the sim-to-real gap

Combining strategies often works better than any single approach

Visual diversity from Cosmos can unlock performance gains

Resources
Cosmos Transfer 2.5 — NVIDIA Research page on Cosmos video-to-video transfer capabilities

Cosmos Cookbook — Recipes and examples for Cosmos world foundation models
---
Sim-to-Real Strategy 4: Measuring and Closing the Gap With SAGE + GapONet
SAGE GapONet Comparison
SAGE GapONet Comparison
In this session, you’ll learn how to quantify the actuation gap precisely using SAGE, and how GapONet can model complex actuation dynamics that aren’t captured by simple parameter tuning.

Learning Objectives
By the end of this session, you’ll be able to:

Explain how SAGE quantifies the sim-to-real gap per joint

Interpret SAGE analysis results to guide improvement

Describe how GapONet models complex actuation dynamics

The Problem: Unknown Gap Sources
You’ve seen the improvements made by these strategies so far:

Domain randomization (Strategy 1)

Co-training with real data (Strategy 2)

Cosmos augmentation (Strategy 3)

But we haven’t addressed actuation gaps yet. To close them systematically, let’s first understand some of the sources:

Sources of the Sim-to-Real Gap
During Sensing:

Simplified or inaccurate sensor models for cameras

Physics modeling gaps in the simulator

During Actuation:

Inaccurate or missing actuator models

Physics modeling gaps (contact nuances, friction, closed-loop linkages)

Uncharacterized dynamic effects at system level (changing inertial behavior with payload, varying friction)

Inaccurate URDF (missing component details, missing properties, user input error)

CAD → URDF → USD format conversion errors

To close these gaps, you need to know:

Where exactly are the gaps?

How large are they?

What causes them?

Specifically for the SO-101, one challenge is that the actuators are hobby servos that can introduce significant backlash into the system, and this backlash adds up through the kinematic chain of the robot.

SAGE can help us visualize and collect data related to this gap.

What Is SAGE?
SAGE (Sim-to-Real Actuation Gap Estimation) is a collaborative project by Tongji University (TJU), Peking University (PKU), and NVIDIA to demonstrate an approach for sim-to-real gap perception, measurement, and bridging.

SAGE provides a systematic way of collecting real and sim paired datasets, analyzing, estimating, and visualizing the sim-to-real gap.

Repository: isaac-sim2real/sage

SAGE systematically:

Collects paired real and simulation data for the same motions

Compares position, velocity, and torque across domains

Quantifies the gap per joint

Visualizes where the gap is largest

Enables targeted improvement via GapONet or parameter tuning

SAGE Overview
SAGE pipeline overview: from diverse motion sources through gap estimation to gap bridging.
SAGE Workflow
┌─────────────────┐     ┌─────────────────┐
│  Motion Files   │     │  Real Robot     │
│  (retargeted    │────▶│  Data Collection│
│   sequences)    │     │  (pos, vel, τ)  │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
┌─────────────────┐     ┌─────────────────┐
│  Same Motions   │     │   Simulation    │
│   in Isaac Sim  │────▶│  Data Collection│
│                 │     │  (pos, vel, τ)  │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Gap Analysis   │
                        │  Per-Joint      │
                        │  Visualization  │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Gap Bridging   │
                        │  (GapONet, etc.)│
                        └─────────────────┘
Case Study: SO-101 SAGE Pipeline Overview
The following gives you an intuitive overview of the full pipeline; the step-by-step walkthrough comes later in this document.

Pipeline in brief. For the SO-101 we (1) collect sim data, (2) collect real robot data, and (3) train a gap-bridging model (GapONet; its details are covered later). Our SO-101 setup collected 8 hours of real trajectory data for such training.

SO-101 during real-robot data collection
SO-101 during real-robot data collection.
Below we show two ways to see the effect of GapONet after it is trained.

1. Visual comparison in the simulation environment.
In Isaac Sim we overlay real-robot motion with sim replay. The GUI screenshot below shows: top — real result vs sim without GapONet; bottom — real result vs sim with GapONet. With GapONet, the sim trace matches the real motion much more closely.

Real vs sim without GapONet (top) and real vs sim with GapONet (bottom) in Isaac Sim
Top: real vs sim without GapONet. Bottom: real vs sim with GapONet.
2. Quantitative joint-level error.
We measure error between real and sim at each joint. In the plot below, orange is the error for real vs sim without GapONet; green is the error for real vs sim with GapONet. Lower green bars show that GapONet reduces the gap.

Joint-level error: orange = real vs sim without GapONet, green = real vs sim with GapONet
Joint error: orange = real vs sim without GapONet; green = real vs sim with GapONet.
SAGE Repository Structure
Understanding the file layout helps navigate the framework. See the SAGE repository for the current structure; a simplified overview:

sage/
├── assets/                    # Robot USD files
│   └── {robot_name}/
├── configs/
│   ├── {robot_name}_joints.yaml       # Complete joint list
│   └── {robot_name}_valid_joints.txt  # Motion-relevant joints
├── docs/                      # Robot-specific guides (e.g. LEROBOT_REAL for SO-101)
├── motion_files/
│   └── {robot_name}/{source}/         # Retargeted motion files
├── output/
│   ├── sim/{robot_name}/{source}/{motion_name}/   # Simulation results
│   └── real/{robot_name}/{source}/{motion_name}/  # Real robot results
├── sage/                      # Python package
│   ├── assets.py              # Robot configuration (USD path, PD gains, etc.)
│   ├── simulation.py          # Isaac Sim simulation code
│   ├── analysis.py            # Sim vs. real comparison and metrics
│   ├── real_unitree/          # Unitree H1-2 real robot code
│   ├── real_realman/          # Realman WR75S real robot code
│   └── real_so101/            # LeRobot SO-101 real robot code
└── scripts/
    ├── run_simulation.py      # Run simulation data collection
    ├── run_analysis.py        # Compare sim vs real, generate metrics and plots
    └── run_real.py            # Run real robot data collection
Walkthrough: Running SAGE on an Action Sequence in Simulation
This walkthrough demonstrates the complete SAGE pipeline: running the same motion in simulation and on real hardware, then analyzing the gap.

Important

This walkthrough is for reference; we won’t be doing this hands-on today for time.

Startup
First, clone the SAGE repository:

git clone git@github.com:isaac-sim2real/sage.git
cd sage
Start the SAGE container:

xhost +
docker run --name isaac-lab --entrypoint bash -it --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
   -e "PRIVACY_CONSENT=Y" \
   -e DISPLAY \
   -v /tmp/.X11-unix:/tmp/.X11-unix \
   -v $HOME/.Xauthority:/root/.Xauthority \
   -v ~/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
   -v ~/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
   -v ~/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
   -v ~/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
   -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
   -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
   -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
   -v ~/docker/isaac-sim/documents:/root/Documents:rw \
   -v $(pwd):/app:rw \
   sage
Choose Motion File
Motion files contain retargeted action sequences. SAGE supports diverse motion sources:

Teleoperation: Human-guided motions

Remote control: Joystick or keyboard controlled

Retargeted motions: From motion capture or other robots

For SO-101, motion files live under motion_files/so101/custom/, including pick-and-place and other trajectories:

# Motion files location
ls motion_files/so101/custom/

# Example output (subset):
# actuator_bandwidth.txt
# pick_place.txt
# oscillation_low_freq.txt
# random_waypoints.txt
# ...
Each .txt file contains joint angle positions over time (format: first line joint names, then comma-separated angles in radians per line).

Verify the Robot Configuration
Verifying robot configuration in sage/assets.py:

# SO-101 entry in ROBOT_CONFIGS
"so101": {
    "usd_path": "assets/so101/SO-ARM101-USD.usd",
    "offset": (0.0, 0.0, 0.0),
    "default_kp": 100.0,   # PD controller stiffness
    "default_kd": 2.0,     # PD controller damping
    "default_control_freq": 50.0,  # Control frequency (Hz)
}
Verifying the valid joints list:

cat configs/so101_valid_joints.txt

# Example output:
# Rotation
# Pitch
# Elbow
# Wrist_Pitch
# Wrist_Roll
# Jaw
Run Simulation Data Collection
From within the same terminal in the SAGE container, we’d now execute the motion sequence in Isaac Sim:

${ISAACSIM_PATH}/python.sh scripts/run_simulation.py \
    --robot-name so101 \
    --motion-source custom \
    --motion-files motion_files/so101/custom/pick_place.txt \
    --valid-joints-file configs/so101_valid_joints.txt \
    --output-folder output \
    --fix-root \
    --physics-freq 200 \
    --render-freq 200 \
    --control-freq 50 \
    --kp 100 \
    --kd 2
This collects:

Commanded joint positions

Actual joint positions (from simulation)

Joint velocities

Joint torques

Run Real Robot Data Collection
Now to create a paired dataset, we’ll execute the same motion on the physical SO-101. This will actually move the robot and record data.

Follow the instructions here: LEROBOT_REAL.md

Analyze the Gap
Compare the paired sim-real data:

python scripts/run_analysis.py \
    --robot-name so101 \
    --motion-source custom \
    --motion-names "pick_place" \
    --output-folder output \
    --valid-joints-file configs/so101_valid_joints.txt
SAGE Elbow Axis Analysis
Analysis of SAGE data to quantify the gap for a given axis, and a given motion.
Using Paired Data for Gap Bridging
Once you have sim-real paired data, you can train a neural network that bridges the actuation gap. This gap-bridging model can be used in two ways:

1. Integrate into the simulation environment.
Use the model inside sim so that the environment better matches real actuation. Policies trained in this gap-corrected sim are more likely to achieve seamless sim-to-real deployment. The figure below illustrates this use.

2. Use at real-robot deployment.
Apply the model on the real robot at inference time so that the policy’s actions are corrected for the actuation gap before execution. This is the idea behind the future work on GapONet + GR00T integration: a policy trained in sim benefits from gap bridging when deployed on hardware.

Gap-bridging model inside simulation
Using a gap-bridging model inside the simulation environment so that policies are trained with more realistic actuation.
What Is GapONet?
GapONet, developed by Peking University (PKU), learns a neural network model of actuator behavior that captures effects not easily modeled analytically. GapONet is part of the SAGE ecosystem, and its integration in SAGE is in progress.

How GapONet Works
Training Phase:
  Input:  Commanded action sequences (from motions)
  Target: Actual resulting motion (from real robot)
  Learns: Mapping from command → actual behavior

Inference Phase:
  Input:  Policy's intended action
  Output: Compensated action that achieves intended behavior
Training GapONet
Note

This section is for reference; we won’t be doing this training hands-on today for time.

The GapONet repository provides an Isaac Lab–based implementation with DeepONet, Transformer, and MLP architectures for sim-to-real humanoid control. After installing the repo and required assets (see the repo README), train with the operator environment:

python scripts/rsl_rl/train.py --task Isaac-Humanoid-Operator-Delta-Action \
  --num_envs=4080 --max_iterations 100000 --experiment_name Sim2Real \
  --letter amass --run_name delta_action_mlp_payload --device cuda env.mode=train --headless
Adjust --num_envs, --max_iterations, and --run_name as needed. For other architectures or tasks, see the repo’s Usage and Adding a New Robot sections.

Evaluation and export. Evaluate a checkpoint:

python scripts/rsl_rl/play.py --task Isaac-Humanoid-Operator-Delta-Action \
   --model ./model/model_17950.pt --num_envs 20 --headless
Export to JIT for lightweight inference without Isaac Sim:

python scripts/rsl_rl/inference_jit.py \
    --export \
    --checkpoint ./model/model_17950.pt \
    --task Isaac-Humanoid-Operator-Delta-Action \
    --output ./model/policy.pt \
    --device cuda:0 \
    --num_envs 20
Then run inference on test data (no Isaac Sim required):

python scripts/rsl_rl/deploy.py \
    --model ./model/policy.pt \
    --test_data ./source/sim2real/sim2real/tasks/humanoid_operator/motions/motion_amass/edited_27dof/test.npz
For SO-101 or other arms, SAGE’s gap-bridging training typically focuses on joints with the largest sim-to-real gaps (e.g. gripper, wrist) using paired SAGE data; the exact scripts depend on the SAGE repository and any GapONet integration there.

Pre-Collected Dataset
For humanoid research, SAGE provides pre-collected datasets:

Unitree Dataset (H1-2 humanoid):

Upper-body motions under varying payloads (0-3 kg)

Motions adapted from AMASS dataset

Paired sim-real data

RealMan Dataset (WR75S arms):

Four arms tested under four payload conditions

Cross-robot generalization studies

The PKU Disk link for downloading these datasets is in the SAGE repository’s Processed Sim2Real Datasets section.

Community-Driven Future
SAGE is designed to become a community-driven effort where roboticists around the world come together to collectively work on solutions.

Community Contributions:

Paired datasets: Real-sim motion data for new robots and tasks

Sim-Ready assets: Robot USD files calibrated for accurate simulation

Novel NN architectures: New models for gap estimation and compensation

Hybrid solutions: Combinations of analytical and learned approaches

Planned Community Features:

Leaderboards: Rank trained networks by quality, enabled task space, and robot models

OEM Feedback: Guide humanoid manufacturers in improving their assets and APIs

Contributing your own data and models helps the entire robotics community close the sim-to-real gap faster.

Future Work: GapONet + GR00T Integration
A key next step is integrating GapONet inference directly into the GR00T deployment loop for our SO-101 task:

GR00T Policy → Action Command → GapONet Compensation → Robot Execution
This would allow the VLA policy to output its intended actions while GapONet automatically compensates for actuator dynamics in real-time—combining the generalization of foundation models with the precision of learned actuator models.

This integration is under active development.

Key Takeaways
SAGE provides quantitative, per-joint gap analysis

The pipeline: same motion → sim + real → compare → quantify

Knowing where gaps are enables targeted improvement

Small gaps: tune parameters; large gaps: use GapONet

GapONet models complex dynamics that resist simple tuning

Isaac Lab integration enables direct use in simulation workflows

Resources
SAGE Repository: isaac-sim2real/sage

GapONet Repository: jiemingcui/gaponet
---
Conclusion
This session provides time for remaining questions, continued experimentation, and a conclusion for this learning path.

Learning Path Summary
What You Accomplished
Learned why simulation matters and what the sim-to-real gap is

Built and standardized the physical lightbox workspace to match the sim task

Got hands-on time with the SO-101 robot and LeRobot tools

Applied Strategy 1: Domain randomization with teleoperation

Explored NVIDIA GR00T, vision-language-action models

Evaluated policies in simulation and on the real robot (sim-to-real gap)

Applied Strategy 2: Co-training with real data, deployed to robot

Applied Strategy 3: Cosmos synthetic data augmentation

Explored Strategy 4: SAGE + GapONet (actuator gap estimation)

The Four Strategies We Covered
Strategy

Approach

Key Benefit

1. Domain Randomization

Vary simulation parameters

Robust to physics variations

2. Co-training

Mix sim and real data

Better real-world distribution

3. Cosmos Augmentation

Synthetic visual diversity

Robust to visual variations

4. SAGE + GapONet

Measure and model the gap

Targeted actuation fixes

Key Lessons
The gap is real — simulation success doesn’t guarantee real-world success

Multiple strategies combine — no single approach solves everything

Measurement enables improvement — SAGE shows you where to focus

Iteration is essential — systematic improvement beats one-shot attempts

Documentation matters — recorded observations guide decisions

Resources
Courses
Getting Started with Isaac Lab - Transferring Robot Learning Policies from Simulation to Reality

Documentation
LeRobot Documentation

Isaac Sim Documentation

Isaac Lab Documentation

GR00T Developer Guide

SAGE Repository

Community
Hugging Face Discord

NVIDIA Developer Forums

LeRobot GitHub

Papers
The Reality Gap in Robotics: Challenges, Solutions, and Best Practices

Conclusion
Congratulations on finishing this course “Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac.”

We hope this will enable and inspire you to keep learning and practicing your skills in Physical AI!

Feedback
Taking a few minutes to fill out our survey gives us valuable feedback to improve the course for future participants.

If you have any feedback, suggestions, or ran into issues, please visit this survey.
---
Quick Reference
Quick commands for common tasks. For detailed explanations, see Calibrating the SO-101 and Operating the SO-101.

Simulation (teleop and eval) — Docker
Launch the Isaac Sim container for sim teleop and sim policy evaluation:

xhost + 
docker run --name teleop -it --privileged --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
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
   -v ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/env:/root/env \
   -v ~/sim2real/Sim-to-Real-SO-101-Workshop:/workspace/Sim-to-Real-SO-101-Workshop \
   teleop-docker:latest
Run this container for the client/server GR00T inference workflow.

xhost +
docker run -it --rm --name real-robot --network host --privileged --gpus all \
    -e DISPLAY \
    -v /dev:/dev \
    -v /run/udev:/run/udev:ro \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.cache/huggingface/lerobot/calibration:/root/.cache/huggingface/lerobot/calibration \
    -v ~/sim2real/models:/workspace/models \
    -v ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/env:/root/env \
    -v ~/sim2real/Sim-to-Real-SO-101-Workshop/docker/real/scripts:/Isaac-GR00T/gr00t/eval/real_robot/SO100 \
    real-robot \
    /bin/bash
Find Robot Ports
Inside the teleop-docker container:

lerobot-find-port
When prompted, disconnect USB cable and press Enter. The tool reports the port (e.g., /dev/ttyACM0).

You can either write these down to use for future commands, or assign them to environment variables in your terminal.

# Save to environment variables
setenv ROBOT_PORT=/dev/ttyACM0
setenv TELEOP_PORT=/dev/ttyACM1

# Set robot IDs (based on your station label)
setenv ROBOT_ID=orange_robot
setenv TELEOP_ID=orange_teleop
Find Cameras
Inside the teleop-docker container:

lerobot-find-cameras opencv
Review captured images in ./output/captured_images to identify gripper vs. external camera indices.

Similar to the robot ports, you can save these to environment variables in your terminal or enter them manually into commands.

# Save to environment variables
setenv CAMERA_GRIPPER=0
setenv CAMERA_EXTERNAL=2
Calibrate Leader Arm (Teleop)
Inside teleop-docker container:

lerobot-calibrate \
    --teleop.type=so101_leader \
    --teleop.port=$TELEOP_PORT \
    --teleop.id=$TELEOP_ID
Follow prompts to move joints to middle-of-range, then through full range of motion.

Calibrate Follower Arm (Robot)
Inside teleop-docker container:

lerobot-calibrate \
    --robot.type=so101_follower \
    --robot.port=$ROBOT_PORT \
    --robot.id=$ROBOT_ID
Teleoperation of Real Robot
Inside teleop-docker container:

lerobot-teleoperate \
    --robot.type=so101_follower \
    --robot.port=$ROBOT_PORT \
    --robot.id=$ROBOT_ID \
    --teleop.type=so101_leader \
    --teleop.port=$TELEOP_PORT \
    --teleop.id=$TELEOP_ID
Common Issues
See Troubleshooting Guide for detailed solutions.

Symptom

Likely Cause

All motors missing

Power not connected

One motor missing

Loose motor cable, or just needs restart

Torque_Enable error

Power cycle robot

Camera index changed

Re-run lerobot-find-cameras

Port not found

Check USB, run lerobot-find-port
---
Datasets and Models
Pre-collected datasets and pre-trained model checkpoints used in this course, hosted on Hugging Face.

Datasets
Dataset

Description

Used In

Link to Visualizer

sreetz-nv/so101_teleop_vials_rack_left

75 sim-only teleoperation demonstrations

Strategy 1, Sim Evaluation, Real Evaluation

See episodes

sreetz-nv/so101_teleop_vials_rack_left_sim_and_real

75 sim-only demonstrations (same dataset as above) + 5 real-world teleoperation demonstrations

Strategy 2

See episodes

sreetz-nv/so101_teleop_vials_rack_left_augment_02

75 sim + 7 Cosmos-augmented episodes

Strategy 3

See episodes

sreetz-nv/so101_teleop_vials_rack_left_cosmos_70

75 sim + 70 Cosmos-augmented episodes

Strategy 3

See episodes

Models
Model

Description

Used In

aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left

Sim-only fine-tuned (75 sim episodes)

Sim Evaluation, Real Evaluation

aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real

Sim + real co-trained (75 sim + 50 real)

Strategy 2

aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02

Cosmos-augmented (75 sim + 7 Cosmos)

Strategy 3

aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70

Cosmos-augmented (75 sim + 70 Cosmos)

Strategy 3

Download Models
From the root of the course repository:

mkdir -p models
hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left

hf download aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real \
  --local-dir ./models/aravindhs-NV/grootn16-finetune_sreetz-so101_teleop_vials_rack_left_sim_and_real

hf download aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02 \
  --local-dir ./models/aravindhs-NV/sreetz-so101_teleop_vials_rack_left_augment_02

hf download aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70 \
  --local-dir ./models/aravindhs-NV/so100-orig-groot-vials-rack-left-cosmos-70
---
Troubleshooting Guide
This page consolidates troubleshooting information from across this learning path for easy access.

This learning path uses Docker for teleoperation in sim, real-robot evaluation, and GR00T inference.

Commands such as lerobot-find-port and lerobot-find-cameras opencv are run inside the teleop-docker container.

GR00T inference and real-robot evaluation are run inside the real-robot container.

Hardware Issues
First Thing to Try
Unplug power, and replug the power cable. Do this 2X if the next command doesn’t run. If that doesn’t solve, proceed to the next steps.

Camera Issues
Policy Deployment Issues
Dataset and Recording Issues
Getting Help

If you’re stuck:

Check this guide for your specific error message

Power cycle the robot (fixes many transient issues)

Re-run camera detection if visual behavior is unexpected

Re-run the diagnostic steps above if the issue persists
---

Workshop Code

https://github.com/isaac-sim/Sim-to-Real-SO-101-Workshop

---
Video Tutorials Playlist
https://www.youtube.com/watch?v=3TL3ALQxQX8&list=PL2bKqBZg-pzVQspO8-wieuIFctBdz_Tr_

---
Physical AI Learning
https://docs.nvidia.com/learning/physical-ai/
---
