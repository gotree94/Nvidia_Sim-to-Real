"""
Franka Emika Panda robot configuration.
DH parameters, joint limits, link dimensions.
"""

import numpy as np

NUM_JOINTS = 7

# ──────────────────────────────────────────────
# Franka Emika Panda DH Parameters (standard)
# ──────────────────────────────────────────────
# Format: (theta_offset, d, a, alpha)
# Reference: franka_ros / libfranka
DH_PARAMS = [
    (0.0,      0.333,  0.0,     0.0),       # Joint 1
    (-np.pi/2, 0.0,    0.0,    -np.pi/2),    # Joint 2
    (np.pi/2,  0.316,  0.0,     np.pi/2),    # Joint 3
    (np.pi/2,  0.0,    0.0825,  np.pi/2),    # Joint 4
    (-np.pi/2, 0.384, -0.0825, -np.pi/2),    # Joint 5
    (np.pi/2,  0.0,    0.0,     np.pi/2),    # Joint 6
    (np.pi/2,  0.088,  0.0,     np.pi/2),    # Joint 7
]

# Joint limits (radians)
# [min, max]
JOINT_LIMITS = np.array([
    [-2.8973,  2.8973],    # q1
    [-1.7628,  1.7628],    # q2
    [-2.8973,  2.8973],    # q3
    [-3.0718, -0.0698],    # q4  (Note: Franka q4 range is negative)
    [-2.8973,  2.8973],    # q5
    [-0.0175,  3.7525],    # q6
    [-2.8973,  2.8973],    # q7
])

# Default home position (radians) — slightly extended upright
HOME_POSITION = np.array([0.0, -0.3, 0.0, -2.0, 0.0, 2.0, 0.8])

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

# Recording defaults
DEFAULT_FPS = 30
