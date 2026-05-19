"""
Robot kinematics: Forward Kinematics, Jacobian, Inverse Kinematics.

Uses Modified DH (Craig) convention.
All transforms are 4×4 numpy arrays.

Frame convention:
  Base frame (0) : origin at robot base mount
  World frame     : table centre = (0, 0, 0), Z up
"""

import numpy as np
from config import (
    DH_ALPHA, DH_A, DH_D, NUM_JOINTS,
    JOINT_LIMITS, IK_DAMPING, IK_MAX_ITER,
    IK_POS_TOLERANCE, IK_ORI_TOLERANCE, IK_STEP_SIZE,
)

# ──────────────────────────────────────────────
# Helper: homogeneous transforms
# ──────────────────────────────────────────────

def dh_transform(alpha, a, d, theta):
    """Single Modified DH transformation matrix."""
    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    return np.array([
        [ct,      -st,      0,     a],
        [st*ca,   ct*ca,   -sa,  -d*sa],
        [st*sa,   ct*sa,    ca,   d*ca],
        [0,        0,        0,    1],
    ])


def rot_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,  0],
        [0, c, -s],
        [0, s,  c],
    ])


def rot_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c],
    ])


def rot_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1],
    ])


# ──────────────────────────────────────────────
# Quaternion utilities
# ──────────────────────────────────────────────

def quat_from_matrix(R):
    """Rotation matrix (3×3) → unit quaternion (x, y, z, w)."""
    m = np.asarray(R, dtype=np.float64)
    trace = m[0, 0] + m[1, 1] + m[2, 2]
    if trace > 0:
        S = np.sqrt(trace + 1.0) * 2
        qw = 0.25 * S
        qx = (m[2, 1] - m[1, 2]) / S
        qy = (m[0, 2] - m[2, 0]) / S
        qz = (m[1, 0] - m[0, 1]) / S
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        S = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        qw = (m[2, 1] - m[1, 2]) / S
        qx = 0.25 * S
        qy = (m[0, 1] + m[1, 0]) / S
        qz = (m[0, 2] + m[2, 0]) / S
    elif m[1, 1] > m[2, 2]:
        S = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        qw = (m[0, 2] - m[2, 0]) / S
        qx = (m[0, 1] + m[1, 0]) / S
        qy = 0.25 * S
        qz = (m[1, 2] + m[2, 1]) / S
    else:
        S = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        qw = (m[1, 0] - m[0, 1]) / S
        qx = (m[0, 2] + m[2, 0]) / S
        qy = (m[1, 2] + m[2, 1]) / S
        qz = 0.25 * S
    return np.array([qx, qy, qz, qw])


def quat_to_matrix(q):
    """Unit quaternion (x, y, z, w) → rotation matrix (3×3)."""
    x, y, z, w = q
    return np.array([
        [1 - 2*y*y - 2*z*z,   2*x*y - 2*w*z,     2*x*z + 2*w*y],
        [2*x*y + 2*w*z,       1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y,       2*y*z + 2*w*x,     1 - 2*x*x - 2*y*y],
    ])


def quat_multiply(q1, q2):
    """Hamilton product of two quaternions (x, y, z, w)."""
    x1, y1, z1, w1 = q1
    x2, y2, z2, w2 = q2
    return np.array([
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2,
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
    ])


def quat_inverse(q):
    x, y, z, w = q
    return np.array([-x, -y, -z, w])


def quat_error(q_target, q_current):
    """Rotation error as angle-axis (3-vector)."""
    q_rel = quat_multiply(quat_inverse(q_current), q_target)
    eps = 1e-12
    angle = 2.0 * np.arccos(np.clip(q_rel[3], -1.0 + eps, 1.0 - eps))
    if np.abs(angle) < 1e-10:
        return np.zeros(3)
    axis = q_rel[:3] / np.linalg.norm(q_rel[:3])
    return angle * axis


# ──────────────────────────────────────────────
# Forward Kinematics
# ──────────────────────────────────────────────

def forward_kinematics(joint_angles):
    """
    Compute FK for all links.

    Parameters
    ----------
    joint_angles : (7,) array of joint angles (rad).

    Returns
    -------
    T_all : list of (4,4) transforms  T_world_{i} for i=0..7
            T_all[0] = world→base
            T_all[i] = world→link_i  (i=1..7)
    """
    # Base offset: robot mount is at (0, 0, TABLE_HEIGHT+0.01) in world
    # The base of the robot sits on the table.
    T_base = np.eye(4)
    T_base[2, 3] = 0.03   # small base height above table

    T_all = [T_base.copy()]
    T = T_base.copy()

    for i in range(NUM_JOINTS):
        Ti = dh_transform(DH_ALPHA[i], DH_A[i], DH_D[i], joint_angles[i])
        T = T @ Ti
        T_all.append(T.copy())

    return T_all


def compute_jacobian(joint_angles, T_all=None):
    """
    Geometric Jacobian (6 × 7).

    Returns
    -------
    J : (6, 7)  J[:3,:] = position,  J[3:,:] = orientation
    """
    if T_all is None:
        T_all = forward_kinematics(joint_angles)

    J = np.zeros((6, NUM_JOINTS))
    p_ee = T_all[-1][:3, 3]

    for i in range(NUM_JOINTS):
        p_i = T_all[i][:3, 3]
        z_i = T_all[i][:3, 2]   # z-axis of joint frame
        J[:3, i] = np.cross(z_i, p_ee - p_i)
        J[3:, i] = z_i

    return J


def inverse_kinematics(target_pos, target_quat,
                       q_initial=None, num_attempts=3):
    """
    Damped least-squares IK.

    Parameters
    ----------
    target_pos    : (3,) desired EEF position in world frame.
    target_quat   : (4,) desired EEF orientation (x, y, z, w).
    q_initial     : (7,) initial guess.  None → HOME_POSITION.

    Returns
    -------
    q_solution : (7,) array or None if not converged.
    """
    if q_initial is None:
        from config import HOME_POSITION
        q_initial = HOME_POSITION.copy()

    best_q = None
    best_err = np.inf

    for attempt in range(num_attempts):
        # Add random perturbation for multiple attempts
        if attempt == 0:
            q = q_initial.copy()
        else:
            q = q_initial.copy()
            q += np.random.uniform(-0.3, 0.3, size=NUM_JOINTS)

        for _ in range(IK_MAX_ITER):
            T_all = forward_kinematics(q)
            T_ee = T_all[-1]

            pos_err = target_pos - T_ee[:3, 3]
            quat_err = quat_error(target_quat,
                                  quat_from_matrix(T_ee[:3, :3]))

            err = np.concatenate([pos_err, quat_err])
            err_norm = np.linalg.norm(err)
            if err_norm < best_err:
                best_err = err_norm
                best_q = q.copy()

            if (np.linalg.norm(pos_err) < IK_POS_TOLERANCE
                    and np.linalg.norm(quat_err) < IK_ORI_TOLERANCE):
                return q

            J = compute_jacobian(q, T_all)
            JJt = J @ J.T
            damped = JJt + IK_DAMPING * IK_DAMPING * np.eye(6)
            dq = J.T @ np.linalg.solve(damped, err)
            q = q + IK_STEP_SIZE * dq
            q = np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])

    if best_q is not None:
        return best_q
    return None


def clamp_joints(q):
    """Clamp joint angles to valid range."""
    return np.clip(q, JOINT_LIMITS[:, 0], JOINT_LIMITS[:, 1])


def get_eef_pose(T_all):
    """
    Extract EEF pose from the final FK transform.

    Returns
    -------
    pos  : (3,)  position
    quat : (4,)  orientation quaternion (x, y, z, w)
    R    : (3,3) rotation matrix
    """
    T = T_all[-1]
    pos = T[:3, 3].copy()
    R = T[:3, :3].copy()
    quat = quat_from_matrix(R)
    return pos, quat, R
