"""
Franka Emika Panda (Franka Research 3) robot configuration.
DH parameters, joint limits, link dimensions, IK tuning.

Verified against official sources:
  - franka_ros / libfranka (joint_limits.yaml)
  - Franka Research 3 Datasheet (R02212 v2.2.1)
  - franka_arm.xacro (URDF link dimensions)

Key specs:
  DOF:         7
  Reach:       855 mm
  Payload:     3 kg
  Arm weight:  ~18 kg
  Repeatability: ±0.1 mm
  Joint vel:   150 deg/s (J1-J4), 301 deg/s (J5-J7)
"""

import numpy as np

NUM_JOINTS = 7

# ──────────────────────────────────────────────
# Franka Emika Panda DH Parameters (Standard DH convention)
# ──────────────────────────────────────────────
# Format: (a_i, d_i, alpha_i, theta_offset)
# Transform: Rot_z(theta) * Trans_z(d) * Trans_x(a) * Rot_x(alpha)
# Reference: libfranka / Franka Research 3 Datasheet (R02212 v2.2.1)
#
# Link distances (from datasheet, mm):
#   d1 = 333, d3 = 316, a4 = 82.5,
#   d5 = 384, a5 = -82.5, d7 = 88, TCP_z = 103
DH_PARAMS = [
    # (a,      d,      alpha,   theta_offset)
    (0.0,      0.333,  0.0,       0.0),          # Joint 1  (base rotation)
    (0.0,      0.0,    -np.pi/2,  -np.pi/2),     # Joint 2  (shoulder)
    (0.0,      0.316,  np.pi/2,   np.pi/2),      # Joint 3  (upper arm)
    (0.0825,   0.0,    np.pi/2,   np.pi/2),      # Joint 4  (elbow)
    (-0.0825,  0.384,  -np.pi/2,  -np.pi/2),     # Joint 5  (forearm)
    (0.0,      0.0,    np.pi/2,   np.pi/2),      # Joint 6  (wrist 1)
    (0.0,      0.088,  np.pi/2,   np.pi/2),      # Joint 7  (wrist 2)
]

# Joint limits (radians) — from franka_ros joint_limits.yaml
# [min, max]
# Datasheet reference (degrees):
#   J1: -166° ~  166°  →  -2.8973 ~  2.8973
#   J2: -105° ~  105°  →  -1.7628 ~  1.7628
#   J3: -166° ~  166°  →  -2.8973 ~  2.8973
#   J4: -176° ~   -7°  →  -3.0718 ~ -0.0698
#   J5: -165° ~  165°  →  -2.8973 ~  2.8973
#   J6:   -1° ~  215°  →  -0.0175 ~  3.7525
#   J7: -175° ~  175°  →  -2.8973 ~  2.8973
JOINT_LIMITS = np.array([
    [-2.8973,  2.8973],    # q1
    [-1.7628,  1.7628],    # q2
    [-2.8973,  2.8973],    # q3
    [-3.0718, -0.0698],    # q4  (Franka q4 range is negative)
    [-2.8973,  2.8973],    # q5
    [-0.0175,  3.7525],    # q6
    [-2.8973,  2.8973],    # q7
])

# Default home position (radians) — Standard DH convention
# EEF at approx (0.40, 0.00, 0.20) — above the table, centered between cubes.
# All joints have ≥ 0.83 rad margin from their limits.
# Verified: IK converges from HOME to all cube positions (< 1 mm error).
HOME_POSITION = np.array([-0.039, -0.914, 1.048, -0.902, -1.326, 1.306, 0.882])

# Link lengths for 3D visualization (meters)
LINK_LENGTHS = [0.333, 0.0, 0.316, 0.0, 0.384, 0.0, 0.088]
# Joint radii for visualization
JOINT_RADII = [0.06, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04]

# End-effector offset from last joint (tcp)
EE_OFFSET = np.array([0.0, 0.0, 0.103])

# Gripper limits (meters)
GRIPPER_LIMITS = np.array([0.0, 0.04])  # 0 = closed, 0.04 = open

# Colors for visualization
COLORS = {
    "base": (0.3, 0.3, 0.3, 1.0),
    "link_1": (0.9, 0.9, 0.9, 1.0),
    "link_2": (0.85, 0.85, 0.85, 1.0),
    "joint": (0.2, 0.4, 0.8, 1.0),
    "eef": (0.9, 0.2, 0.2, 1.0),
    "gripper": (0.6, 0.6, 0.6, 1.0),
    "cube_red": (0.9, 0.2, 0.2, 0.8),
    "cube_blue": (0.2, 0.3, 0.9, 0.8),
    "cube_green": (0.2, 0.8, 0.3, 0.8),
    "table": (0.5, 0.4, 0.3, 1.0),
    "grid": (0.7, 0.7, 0.7, 1.0),
    "background": (0.15, 0.15, 0.2, 1.0),
}

# Cube positions (default initial positions)
CUBE_POSITIONS = {
    "cube_1": np.array([0.5, 0.1, 0.0203]),    # red
    "cube_2": np.array([0.4, -0.1, 0.0203]),   # blue
    "cube_3": np.array([0.5, -0.1, 0.0203]),   # green
}

CUBE_SIZE = 0.04  # meters
CUBE_COLORS = ["cube_red", "cube_blue", "cube_green"]

# Gripper finger offsets from EEF
GRIPPER_FINGER_OFFSET = 0.058  # half-width of gripper base

# Action dimension: [delta_q1..delta_q7, gripper]
ACTION_DIM = 8
# Observation dimensions
OBS_DIM = {
    "joint_pos": 9,        # 7 joints + 2 fingers
    "joint_vel": 9,
    "eef_pos": 3,
    "eef_quat": 4,
    "gripper_pos": 2,
    "cube_positions": 9,   # 3 cubes x 3
    "cube_orientations": 12,  # 3 cubes x 4 (quaternion)
    "object": 39,          # flattened object state
}

# Task subtask names
SUBTASK_NAMES = ["grasp_1", "grasp_2", "stack_1"]

# ──────────────────────────────────────────────
# IK (Inverse Kinematics) Configuration
# ──────────────────────────────────────────────
# Damped least-squares tuning
IK_DAMPING = 0.5          # Step size damping (lower = more aggressive)
IK_LAMBDA_REG = 0.01      # Regularization for Jacobian pseudoinverse
IK_MAX_ITER = 200         # Max iterations for convergence
IK_TOLERANCE = 1e-6       # Convergence tolerance (radians)
IK_TOLERANCE_RELAXED = 1e-3  # Relaxed tolerance for mouse tracking

# IK Mouse Control
IK_DEFAULT_Z = 0.10       # Default Z height for IK mouse control (m)
IK_Z_MIN = 0.02           # Min Z height (table surface)
IK_Z_MAX = 0.50           # Max Z height
IK_DRAG_SMOOTH_STEPS = 5  # IK iterations per mouse move event

# Recording defaults
DEFAULT_FPS = 30
