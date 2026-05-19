"""
Franka Emika Panda kinematics module.
- Forward Kinematics (DH-based)
- Inverse Kinematics (Jacobian pseudoinverse)
- Jacobian computation
- Helper: quaternion operations
"""

import numpy as np
from config import DH_PARAMS, JOINT_LIMITS, HOME_POSITION, EE_OFFSET
from config import IK_DAMPING, IK_LAMBDA_REG, IK_MAX_ITER, IK_TOLERANCE
from config import IK_TOLERANCE_RELAXED, IK_DRAG_SMOOTH_STEPS


# ──────────────────────────────────────────────
# Standard DH Transform
# ──────────────────────────────────────────────
def dh_transform(a, d, alpha, theta):
    """
    Standard Denavit-Hartenberg transformation matrix (4x4).
    Transform from frame i-1 to frame i:
      Rot_z(theta_i) * Trans_z(d_i) * Trans_x(a_i) * Rot_x(alpha_i)

    Matrix:
      [cos(th)  -sin(th)*cos(alpha)   sin(th)*sin(alpha)   a*cos(th)]
      [sin(th)   cos(th)*cos(alpha)  -cos(th)*sin(alpha)   a*sin(th)]
      [0         sin(alpha)           cos(alpha)            d         ]
      [0         0                    0                     1         ]
    """
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)
    return np.array([
        [ct,      -st * ca,  st * sa,   a * ct],
        [st,       ct * ca, -ct * sa,   a * st],
        [0,        sa,       ca,        d     ],
        [0,        0,        0,         1     ],
    ])


# ──────────────────────────────────────────────
# Forward Kinematics
# ──────────────────────────────────────────────
def franka_fk(joint_angles):
    """
    Forward Kinematics: joint angles → EEF 4x4 transform.
    Uses Standard DH convention (Rot_z * Trans_z * Trans_x * Rot_x).

    Args:
        joint_angles: (7,) array of joint angles in radians

    Returns:
        4x4 transformation matrix of end-effector in base frame
    """
    T = np.eye(4)
    for i, (a, d, alpha, theta_offset) in enumerate(DH_PARAMS):
        theta = joint_angles[i] + theta_offset
        T = T @ dh_transform(a, d, alpha, theta)
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
    for i, (a, d, alpha, theta_offset) in enumerate(DH_PARAMS):
        theta = joint_angles[i] + theta_offset
        T = T @ dh_transform(a, d, alpha, theta)
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

    Joint i+1 rotates about z_i (z-axis of frame {i}):
      - Frame {0} = base frame, z_0 = [0,0,1], p_0 = [0,0,0]
      - Frame {i} for i>=1 = transforms[i-1] (from franka_fk_all_joints)

    Returns:
        6x7 matrix: [linear_velocity; angular_velocity] / joint_velocity
    """
    transforms = franka_fk_all_joints(joint_angles)
    T_ee = franka_fk(joint_angles)
    p_ee = T_ee[:3, 3]

    J = np.zeros((6, 7))

    # Joint 1 (column 0): uses base frame {0} — z_0 = [0,0,1], p_0 = [0,0,0]
    z_0 = np.array([0.0, 0.0, 1.0])
    p_0 = np.zeros(3)
    J[:3, 0] = np.cross(z_0, p_ee - p_0)
    J[3:, 0] = z_0

    # Joints 2..7 (columns 1..6): use frame {i} from transforms[i-1]
    for i in range(1, 7):
        z_i = transforms[i - 1][:3, 2]  # z-axis of frame {i}
        p_i = transforms[i - 1][:3, 3]  # origin of frame {i}
        J[:3, i] = np.cross(z_i, p_ee - p_i)
        J[3:, i] = z_i

    return J


# ──────────────────────────────────────────────
# Inverse Kinematics (Jacobian pseudoinverse)
# ──────────────────────────────────────────────
def franka_ik(T_target, q_init=None, max_iter=200, tol=1e-6, damping=0.5):
    """
    Inverse Kinematics: target 4x4 → joint angles.
    Uses damped least-squares with step limiting.

    For position-only control, use franka_position_ik instead,
    which uses a 3x7 sub-Jacobian for faster convergence.

    Args:
        T_target: target 4x4 transformation matrix
        q_init: initial guess (default: home position)
        max_iter: maximum iterations
        tol: convergence tolerance (position error in meters)
        damping: step size damping factor (0-1)

    Returns:
        q_solution: (7,) joint angles, or None if failed
    """
    if q_init is None:
        q_init = HOME_POSITION.copy()

    q = q_init.copy()
    q = np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])

    MAX_STEP = 0.2  # max rad per joint per iteration
    best_q = q.copy()
    best_err = np.inf

    for i in range(max_iter):
        T_cur = franka_fk(q)
        error = _se3_error(T_target, T_cur)
        err_norm = np.linalg.norm(error)

        if err_norm < tol:
            return q

        if err_norm < best_err:
            best_q = q.copy()
            best_err = err_norm

        J = franka_jacobian(q)
        JJT = J @ J.T
        lambda_reg = IK_LAMBDA_REG * np.trace(JJT) / 6.0
        dq = J.T @ np.linalg.inv(JJT + lambda_reg * np.eye(6)) @ error

        # Limit max joint step
        max_abs = np.max(np.abs(dq))
        if max_abs > MAX_STEP:
            dq = dq * (MAX_STEP / max_abs)

        # Backtracking line search
        accepted = False
        for scale in [damping, damping * 0.5, damping * 0.25]:
            q_new = q + scale * dq
            q_new = np.clip(q_new, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
            new_err = np.linalg.norm(_se3_error(T_target, franka_fk(q_new)))
            if new_err < err_norm:
                q = q_new
                accepted = True
                break

        if not accepted:
            # Can't improve — try reduced step then exit
            q_new = q + 0.1 * dq
            q_new = np.clip(q_new, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
            new_err = np.linalg.norm(_se3_error(T_target, franka_fk(q_new)))
            if new_err < err_norm:
                q = q_new
            break

    # Return best found
    final_err = np.linalg.norm(_se3_error(T_target, franka_fk(best_q)))
    if final_err < max(tol * 100, 0.05):
        return best_q
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


# ──────────────────────────────────────────────
# Position-Only IK (for mouse control)
# ──────────────────────────────────────────────
def franka_position_ik(target_pos, current_joint_angles, max_iter=100, tol=1e-4):
    """
    IK for position target only — keeps current EEF orientation fixed.
    Uses the position sub-Jacobian (3x7) for faster convergence.

    Useful for mouse-based end-effector dragging where we want
    the arm to follow the cursor while maintaining orientation.

    Args:
        target_pos: (3,) target position [x, y, z] in world frame
        current_joint_angles: (7,) current joint angles (initial guess)
        max_iter: max iterations per call
        tol: convergence tolerance (meters)

    Returns:
        (7,) joint angles or None if failed
    """
    q = current_joint_angles.copy()
    q = np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])

    MAX_STEP = 0.25  # max rad per joint per iteration
    best_q = q.copy()
    best_err = np.inf

    for i in range(max_iter):
        T_cur = franka_fk(q)
        pos_cur = T_cur[:3, 3]
        pos_error = target_pos - pos_cur
        err_norm = np.linalg.norm(pos_error)

        if err_norm < tol:
            return q

        if err_norm < best_err:
            best_q = q.copy()
            best_err = err_norm

        # Position-only Jacobian (3x7) and DLS
        J = franka_jacobian(q)
        J_pos = J[:3, :]  # 3x7 position Jacobian
        JJT = J_pos @ J_pos.T  # 3x3
        lambda_reg = IK_LAMBDA_REG * np.trace(JJT) / 3.0
        dq = J_pos.T @ np.linalg.inv(JJT + lambda_reg * np.eye(3)) @ pos_error

        # Limit max joint step
        max_abs = np.max(np.abs(dq))
        if max_abs > MAX_STEP:
            dq = dq * (MAX_STEP / max_abs)

        # Line search
        accepted = False
        for scale in [IK_DAMPING, IK_DAMPING * 0.5, IK_DAMPING * 0.25]:
            q_new = q + scale * dq
            q_new = np.clip(q_new, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
            new_err = np.linalg.norm(target_pos - franka_fk(q_new)[:3, 3])
            if new_err < err_norm:
                q = q_new
                accepted = True
                break

        if not accepted:
            break

    if best_err < max(tol * 10, 0.02):
        return best_q
    return None


def franka_ik_toward_target(target_pos, current_joint_angles, steps=5):
    """
    Run a small number of IK iterations toward a position target.
    Designed for smooth real-time mouse tracking — runs few iterations
    per call and relies on being called repeatedly.

    Uses position-only Jacobian (3x7) for faster convergence
    and step-size limiting for stability.

    Args:
        target_pos: (3,) target world position
        current_joint_angles: (7,) current guess (joint angles)
        steps: number of damped least-squares iterations to run

    Returns:
        (7,) updated joint angles (clamped to limits, may not be fully converged)
    """
    q = current_joint_angles.copy()
    q = np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
    MAX_STEP = 0.2  # max rad per joint per iteration

    for _ in range(steps):
        pos_cur = franka_fk(q)[:3, 3]
        pos_error = target_pos - pos_cur
        err_norm = np.linalg.norm(pos_error)

        if err_norm < IK_TOLERANCE_RELAXED:
            break

        # Position-only Jacobian (3x7)
        J = franka_jacobian(q)
        J_pos = J[:3, :]
        JJT = J_pos @ J_pos.T
        lambda_reg = IK_LAMBDA_REG * np.trace(JJT) / 3.0
        dq_raw = J_pos.T @ np.linalg.inv(JJT + lambda_reg * np.eye(3)) @ pos_error

        # Limit max joint step
        max_abs = np.max(np.abs(dq_raw))
        dq = dq_raw * (MAX_STEP / max_abs) if max_abs > MAX_STEP else dq_raw

        # Try step, line search if needed
        for scale in [IK_DAMPING, IK_DAMPING * 0.5, IK_DAMPING * 0.3]:
            q_new = q + scale * dq
            q_new = np.clip(q_new, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])
            new_err = np.linalg.norm(target_pos - franka_fk(q_new)[:3, 3])
            if new_err < err_norm:
                q = q_new
                break
        else:
            # Accept anyway with small step (better than no movement)
            q = q + 0.1 * dq
            q = np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])

    return q


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
