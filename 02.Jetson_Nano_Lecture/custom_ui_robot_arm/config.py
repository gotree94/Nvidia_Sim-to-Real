"""
Franka Emika Panda robot configuration.

All dimensions in metres, angles in radians, masses in kg.
DH convention: Modified (Craig) parameters [alpha, a, d, theta].
"""

import numpy as np

# ──────────────────────────────────────────────
# Franka Panda Modified DH Parameters (7-DOF)
#   i | alpha_{i-1} | a_{i-1} | d_i | theta_i
# ──────────────────────────────────────────────
DH_ALPHA = np.array([0.0, -np.pi / 2, np.pi / 2, np.pi / 2,
                     -np.pi / 2, np.pi / 2, np.pi / 2])
DH_A = np.array([0.0, 0.0, 0.0, 0.0825, -0.0825, 0.0, 0.088])
DH_D = np.array([0.333, 0.0, 0.316, 0.0, 0.384, 0.0, 0.107])

NUM_JOINTS = 7

# ──────────────────────────────────────────────
# Joint limits [radians]  (from libfranka)
# ──────────────────────────────────────────────
JOINT_LIMITS = np.array([
    [-2.8973,  2.8973],   # J1
    [-1.7628,  1.7628],   # J2
    [-2.8973,  2.8973],   # J3
    [-3.0718, -0.0698],   # J4  (slightly positive range → negative)
    [-2.8973,  2.8973],   # J5
    [-0.0175,  3.7525],   # J6
    [-2.8973,  2.8973],   # J7
], dtype=np.float64)

# ──────────────────────────────────────────────
# Home posture presets
# ──────────────────────────────────────────────
PRESET_POSITIONS = {
    "Vertical Extended": np.array(
        [0.0, -1.2, 0.0, -1.8, 0.0, 1.5, 0.8], dtype=np.float64),
    "Fully Vertical": np.array(
        [0.0, -np.pi/2, 0.0, -np.pi/2, 0.0, 0.0, 0.0], dtype=np.float64),
}
HOME_POSITION = PRESET_POSITIONS["Vertical Extended"]
PRESET_NAMES = list(PRESET_POSITIONS.keys())

# ──────────────────────────────────────────────
# Link rendering dimensions  [radius, length]
# ──────────────────────────────────────────────
LINK_RADIUS = 0.035
LINK_SEGMENTS = (
    (0.07, 0.333),   # link 0 (base → J1)
    (0.05, 0.200),   # link 1
    (0.05, 0.316),   # link 2
    (0.08, 0.150),   # link 3 (elbow)
    (0.05, 0.384),   # link 4
    (0.05, 0.100),   # link 5
    (0.06, 0.107),   # link 6
    (0.04, 0.060),   # link 7 (wrist → flange)
)

JOINT_RADIUS = 0.055      # joint sphere radius
BASE_RADIUS  = 0.10       # base cylinder radius
BASE_HEIGHT  = 0.05       # base cylinder height
TABLE_SIZE   = 0.8        # table half-size
TABLE_HEIGHT = 0.02       # table thickness

# ──────────────────────────────────────────────
# End-effector → gripper fingers  (two prisms)
# ──────────────────────────────────────────────
GRIPPER_LENGTH = 0.08
GRIPPER_WIDTH  = 0.025
GRIPPER_HEIGHT = 0.005
GRIPPER_OPEN   = 0.04      # fully open (m)
GRIPPER_CLOSED = 0.0       # fully closed (m)
GRIPPER_DEFAULT = 0.04     # starting width

# ──────────────────────────────────────────────
# Cubes for stacking task
# ──────────────────────────────────────────────
NUM_CUBES = 3
CUBE_SIZE = 0.045  # 4.5 cm
CUBE_MASS = 0.1    # kg

# Cube initial positions  [x, y, z]  relative to table centre
CUBE_INITIAL_POSITIONS = np.array([
    [0.0,  -0.10, 0.025],
    [0.0,   0.00, 0.025],
    [0.10, -0.05, 0.025],
], dtype=np.float64)

CUBE_COLORS = [
    (1.0, 0.3, 0.3),   # red
    (0.3, 0.6, 1.0),   # blue
    (0.3, 1.0, 0.3),   # green
]

# ──────────────────────────────────────────────
# Colors
# ──────────────────────────────────────────────
COLOR_BG       = (0.12, 0.12, 0.14, 1.0)   # dark background
COLOR_GRID     = (0.30, 0.30, 0.35, 1.0)   # grid lines
COLOR_TABLE    = (0.60, 0.55, 0.50, 1.0)   # wood-ish
COLOR_BASE     = (0.25, 0.25, 0.28, 1.0)   # dark grey base
COLOR_LINK     = (0.50, 0.50, 0.55, 1.0)   # link grey
COLOR_JOINT    = (0.40, 0.40, 0.45, 1.0)   # joint sphere grey
COLOR_GRIPPER  = (0.60, 0.60, 0.65, 1.0)   # gripper
COLOR_EEF_MARK = (1.0,  0.0,  0.0,  1.0)   # EEF coordinate X
COLOR_EEF_MARK_Y = (0.0, 1.0, 0.0, 1.0)    # EEF coordinate Y
COLOR_EEF_MARK_Z = (0.0, 0.0, 1.0, 1.0)    # EEF coordinate Z

# ──────────────────────────────────────────────
# Subtask signal names  (mirror Isaac Lab Mimic)
# ──────────────────────────────────────────────
SUBTASK_NAMES = ["grasp_1", "grasp_2", "stack_1"]

# ──────────────────────────────────────────────
# Recording defaults
# ──────────────────────────────────────────────
DEFAULT_FPS  = 30
ACTION_DIM   = 8       # Δq₁..₇ + gripper_cmd

# ──────────────────────────────────────────────
# IK solver parameters
# ──────────────────────────────────────────────
IK_DAMPING       = 0.1    # damped least-squares λ
IK_MAX_ITER      = 50
IK_POS_TOLERANCE = 0.005  # m
IK_ORI_TOLERANCE = 0.02   # rad
IK_STEP_SIZE     = 0.3

# ──────────────────────────────────────────────
# Keyboard control step sizes
# ──────────────────────────────────────────────
JOINT_STEP_SLOW   = 0.003   # rad/frame (fine control)
JOINT_STEP_FAST   = 0.012   # rad/frame (coarse)
GRIPPER_STEP      = 0.002   # m/frame
EEF_POS_STEP      = 0.006   # m/frame (EEF Cartesian translation)
EEF_ROT_STEP      = 0.03    # rad/frame (EEF Cartesian rotation)

# ──────────────────────────────────────────────
# Speed multiplier
# ──────────────────────────────────────────────
SPEED_MIN     = 0.1
SPEED_MAX     = 3.0
SPEED_DEFAULT = 1.0
