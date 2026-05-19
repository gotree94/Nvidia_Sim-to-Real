"""
Franka Emika Panda kinematics module.
- Forward Kinematics (DH-based)
- Inverse Kinematics (Jacobian pseudoinverse)
- Jacobian computation
- Helper: quaternion operations
"""

import numpy as np
from config import DH_PARAMS, JOINT_LIMITS, HOME_POSITION, EE_OFFSET


# ──────────────────────────────────────────────
# DH Transform
# ──────────────────────────────────────────────
def dh_transform(theta, d, a, alpha):
    """Denavit-Hartenberg transformation matrix (4x4)."""
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct, -st * ca,  st * sa, a * ct],
        [st,  ct * ca, -ct * sa, a * st],
        [0.0,      sa,      ca,      d],
        [0.0,     0.0,     0.0,    1.0],
    ])


# ──────────────────────────────────────────────
# Forward Kinematics
# ──────────────────────────────────────────────
def franka_fk(joint_angles):
    """
    Forward Kinematics: joint angles → EEF 4x4 transform.
    
    Args:
        joint_angles: (7,) array of joint angles in radians
        
    Returns:
        4x4 transformation matrix of end-effector in base frame
    """
    T = np.eye(4)
    for i, (theta_offset, d, a, alpha) in enumerate(DH_PARAMS):
        theta = joint_angles[i] + theta_offset
        T = T @ dh_transform(theta, d, a, alpha)
    # Apply EEF offset
    T_offset = np.eye(4)
    T_offset[:3, 3] = EE_OFFSET
    T = T @ T_offset
    return T


def franka_fk_all_joints(joint_angles):
    """
    Forward Kinematics for ALL joint frames.
    
    Returns:
        list of 7 (4x4) matrices, where transforms[i] is the frame of joint i+1
    """
    transforms = []
    T = np.eye(4)
    for i, (theta_offset, d, a, alpha) in enumerate(DH_PARAMS):
        theta = joint_angles[i] + theta_offset
        T = T @ dh_transform(theta, d, a, alpha)
        transforms.append(T.copy())
    return transforms


def franka_fk_with_ee(joint_angles):
    """
    FK including end-effector frame.
    
    Returns:
        list of 8 (4x4) matrices: [joint_1_frame, ..., joint_7_frame, eef_frame]
    """
    transforms = franka_fk_all_joints(joint_angles)
    T_ee = transforms[-1].copy()
    T_offset = np.eye(4)
    T_offset[:3, 3] = EE_OFFSET
    T_ee = T_ee @ T_offset
    transforms.append(T_ee)
    return transforms


# ──────────────────────────────────────────────
# Jacobian
# ──────────────────────────────────────────────
def franka_jacobian(joint_angles):
    """
    Compute the geometric Jacobian (6x7) at current joint configuration.
    
    Returns:
        6x7 matrix: [linear_velocity; angular_velocity] / joint_velocity
    """
    transforms = franka_fk_all_joints(joint_angles)
    T_ee = franka_fk(joint_angles)
    p_ee = T_ee[:3, 3]
    
    J = np.zeros((6, 7))
    for i in range(7):
        z_i = transforms[i][:3, 2]  # z-axis of joint i frame
        p_i = transforms[i][:3, 3]  # origin of joint i frame
        
        # Linear velocity part
        J[:3, i] = np.cross(z_i, p_ee - p_i)
        # Angular velocity part
        J[3:, i] = z_i
    
    return J


# ──────────────────────────────────────────────
# Inverse Kinematics (Jacobian pseudoinverse)
# ──────────────────────────────────────────────
def franka_ik(T_target, q_init=None, max_iter=200, tol=1e-6, damping=0.5):
    """
    Inverse Kinematics: target 4x4 → joint angles.
    Uses damped least-squares (Levenberg-Marquardt style).
    
    Args:
        T_target: target 4x4 transformation matrix
        q_init: initial guess (default: home position)
        max_iter: maximum iterations
        tol: convergence tolerance (radians)
        damping: step size damping factor
        
    Returns:
        q_solution: (7,) joint angles, or None if failed
    """
    if q_init is None:
        q_init = HOME_POSITION.copy()
    
    q = q_init.copy()
    T_current = franka_fk(q)
    
    for i in range(max_iter):
        # Compute error in SE(3)
        error = _se3_error(T_target, T_current)
        error_norm = np.linalg.norm(error)
        
        if error_norm < tol:
            return q
        
        # Jacobian and damped pseudoinverse
        J = franka_jacobian(q)
        JJT = J @ J.T
        lambda_reg = 0.01 * np.trace(JJT) / 6.0
        dq = J.T @ np.linalg.inv(JJT + lambda_reg * np.eye(6)) @ error
        
        # Apply damping and update
        q = q + damping * dq
        # Clamp to joint limits
        q = np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
        
        T_current = franka_fk(q)
    
    # Check final error
    error = _se3_error(T_target, T_current)
    if np.linalg.norm(error) < tol * 10:
        return q
    return None


def _se3_error(T_target, T_current):
    """
    Compute SE(3) error vector (6,): [position_error; orientation_error].
    """
    # Position error
    pos_error = T_target[:3, 3] - T_current[:3, 3]
    
    # Orientation error (axis-angle from rotation difference)
    R_target = T_target[:3, :3]
    R_current = T_current[:3, :3]
    R_error = R_current.T @ R_target
    orient_error = _rotation_matrix_to_axis_angle(R_error)
    
    return np.concatenate([pos_error, orient_error])


def _rotation_matrix_to_axis_angle(R):
    """Convert 3x3 rotation matrix to axis-angle vector (3,)."""
    angle = np.arccos(np.clip((np.trace(R) - 1.0) / 2.0, -1.0, 1.0))
    if angle < 1e-10:
        return np.zeros(3)
    rx = R[2, 1] - R[1, 2]
    ry = R[0, 2] - R[2, 0]
    rz = R[1, 0] - R[0, 1]
    axis = np.array([rx, ry, rz])
    axis_norm = np.linalg.norm(axis)
    if axis_norm < 1e-10:
        return np.zeros(3)
    return (angle / axis_norm) * axis


# ──────────────────────────────────────────────
# Quaternion utilities
# ──────────────────────────────────────────────
def rotation_matrix_to_quat(R):
    """3x3 rotation matrix → (w, x, y, z) quaternion."""
    trace = np.trace(R)
    if trace > 0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (R[2, 1] - R[1, 2]) * s
        y = (R[0, 2] - R[2, 0]) * s
        z = (R[1, 0] - R[0, 1]) * s
    else:
        if R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
            s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
            w = (R[2, 1] - R[1, 2]) / s
            x = 0.25 * s
            y = (R[0, 1] + R[1, 0]) / s
            z = (R[0, 2] + R[2, 0]) / s
        elif R[1, 1] > R[2, 2]:
            s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
            w = (R[0, 2] - R[2, 0]) / s
            x = (R[0, 1] + R[1, 0]) / s
            y = 0.25 * s
            z = (R[1, 2] + R[2, 1]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
            w = (R[1, 0] - R[0, 1]) / s
            x = (R[0, 2] + R[2, 0]) / s
            y = (R[1, 2] + R[2, 1]) / s
            z = 0.25 * s
    return np.array([w, x, y, z])


def quat_to_rotation_matrix(q):
    """(w, x, y, z) quaternion → 3x3 rotation matrix."""
    w, x, y, z = q
    return np.array([
        [1 - 2*y*y - 2*z*z,   2*x*y - 2*w*z,     2*x*z + 2*w*y],
        [2*x*y + 2*w*z,       1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y,       2*y*z + 2*w*x,     1 - 2*x*x - 2*y*y],
    ])


def quat_multiply(q1, q2):
    """Multiply two quaternions (w, x, y, z)."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
    ])
