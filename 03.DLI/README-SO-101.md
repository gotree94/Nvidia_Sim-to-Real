# Train an SO-101 Robot From Sim-to-Real With NVIDIA Isaac

https://docs.nvidia.com/learning/physical-ai/sim-to-real-so-101/latest/index.html

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

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---




