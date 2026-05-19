"""
3D Robot Arm Viewer using PyQt5 + PyOpenGL.
Renders Franka arm, cubes, table, and grid.
"""

import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent, QWheelEvent

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import glutInit
except ImportError:
    raise ImportError("PyOpenGL required. pip install PyOpenGL PyOpenGL_accelerate")

from kinematics import franka_fk_with_ee, franka_fk, rotation_matrix_to_quat
from kinematics import franka_ik_toward_target
from config import COLORS, JOINT_RADII, LINK_LENGTHS, CUBE_POSITIONS, CUBE_SIZE, CUBE_COLORS
from config import GRIPPER_FINGER_OFFSET, EE_OFFSET
from config import IK_DEFAULT_Z, IK_Z_MIN, IK_Z_MAX, IK_DRAG_SMOOTH_STEPS


# Joint axis colors for rotation-axis arrows (distinct per joint)
# Each joint rotates about its z-axis; drawing these axes shows
# co-located joints (J1+J2 at shoulder, J5+J6 at wrist) as separate DOFs.
JOINT_AXIS_COLORS = [
    (0.2, 0.5, 1.0, 1.0),   # J1 - base rotation (blue)
    (0.2, 1.0, 0.7, 1.0),   # J2 - shoulder pitch (cyan)
    (0.5, 1.0, 0.2, 1.0),   # J3 - upper arm roll (green)
    (1.0, 0.8, 0.2, 1.0),   # J4 - elbow pitch (yellow)
    (1.0, 0.5, 0.2, 1.0),   # J5 - forearm roll (orange)
    (1.0, 0.2, 0.5, 1.0),   # J6 - wrist pitch (pink)
    (0.6, 0.3, 1.0, 1.0),   # J7 - wrist roll (purple)
]

AXIS_ARROW_LENGTH = 0.10  # meters (visual scale, not a kinematic parameter)


class Robot3DViewer(QOpenGLWidget):
    """OpenGL 3D viewport for robot arm visualization."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 500)
        self.setFocusPolicy(Qt.StrongFocus)

        # Camera state
        self.cam_dist = 2.5
        self.cam_azimuth = 45.0   # degrees
        self.cam_elevation = 30.0
        self.last_mouse_pos = None
        self.is_dragging = False

        # Robot state (reference to external)
        self.joint_angles = np.zeros(7)
        self.gripper_width = 0.04  # open

        # Cubes state
        self.cube_positions = {k: v.copy() for k, v in CUBE_POSITIONS.items()}
        self.cube_orientations = {k: np.array([1.0, 0.0, 0.0, 0.0]) 
                                  for k in CUBE_POSITIONS}
        self.cube_attached = {k: False for k in CUBE_POSITIONS}
        self.attached_to_gripper = None  # which cube is held

        # Display lists
        self._init_done = False

        # ── IK (Inverse Kinematics) Control Mode ──
        self.ik_mode = False          # When True, mouse drags the EEF via IK
        self.ik_target_pos = None     # (3,) current target position or None
        self.ik_target_z = IK_DEFAULT_Z  # Z height for IK plane intersection
        self.ik_dragging = False      # Mouse is currently dragging in IK mode
        self.ik_visible = True        # Show the IK target indicator

        # Callbacks (set by MainWindow)
        self._ik_target_callback = None  # called when target changes: f(pos)
        self._ik_joint_callback = None   # called when joints update: f(angles)

        # Timer for continuous rendering
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer)
        self.timer.start(16)  # ~60 FPS

    def initializeGL(self):
        glutInit([])  # safety init
        glClearColor(*COLORS["background"])
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_NORMALIZE)

        # Lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 10.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

        # Material
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self._init_done = True

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / max(h, 1), 0.05, 20.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera positioning
        rad_a = np.radians(self.cam_azimuth)
        rad_e = np.radians(self.cam_elevation)
        cx = self.cam_dist * np.cos(rad_e) * np.sin(rad_a)
        cy = self.cam_dist * np.cos(rad_e) * np.cos(rad_a)
        cz = self.cam_dist * np.sin(rad_e)
        gluLookAt(cx, cy, cz, 0, 0, 0.3, 0, 0, 1)

        # Draw scene
        self._draw_grid()
        self._draw_table()
        self._draw_cubes()
        self._draw_robot()
        self._draw_ik_target()

    # ───── Mouse & Wheel Events ─────

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.last_mouse_pos = None

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_dragging and self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.cam_azimuth += dx * 0.5
            self.cam_elevation = np.clip(self.cam_elevation + dy * 0.5, -80, 80)
            self.last_mouse_pos = event.pos()
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if self.ik_mode:
            # In IK mode: scroll adjusts Z height of the control plane
            self.ik_target_z = np.clip(
                self.ik_target_z + delta * 0.002, IK_Z_MIN, IK_Z_MAX)
            # If we already have a target, re-project it to the new Z
            if self.ik_target_pos is not None:
                # Re-project the current mouse position to the new Z plane
                self.ik_target_pos[2] = self.ik_target_z
            if self._ik_target_callback:
                self._ik_target_callback(self.ik_target_pos, self.ik_target_z)
        else:
            # Normal mode: zoom
            self.cam_dist = np.clip(self.cam_dist - delta * 0.002, 0.5, 8.0)
        self.update()

    # ───── IK Mode: Mouse Events ─────

    def _on_timer(self):
        """Main update: render + run IK toward target if dragging."""
        if self.ik_mode and self.ik_dragging and self.ik_target_pos is not None:
            # Run IK toward current target with smooth, limited iterations
            new_q = franka_ik_toward_target(
                self.ik_target_pos, self.joint_angles,
                steps=IK_DRAG_SMOOTH_STEPS)
            self.joint_angles[:] = new_q
            if self._ik_joint_callback:
                self._ik_joint_callback(new_q)
        self.update()

    def _screen_to_world_ray(self, mouse_pt):
        """
        Convert a mouse QPoint to a world-space ray (origin, direction).
        Requires a current OpenGL context (called during mouse event).
        Returns (origin_3, direction_3) or (None, None) on failure.
        """
        self.makeCurrent()
        try:
            viewport = glGetIntegerv(GL_VIEWPORT)
            mv = glGetDoublev(GL_MODELVIEW_MATRIX)
            proj = glGetDoublev(GL_PROJECTION_MATRIX)
        except Exception:
            return None, None

        win_x = float(mouse_pt.x())
        win_y = float(viewport[3] - mouse_pt.y())

        try:
            near = gluUnProject(win_x, win_y, 0.0, mv, proj, viewport)
            far = gluUnProject(win_x, win_y, 1.0, mv, proj, viewport)
        except Exception:
            return None, None

        origin = np.array([near[0], near[1], near[2]], dtype=np.float64)
        far_pt = np.array([far[0], far[1], far[2]], dtype=np.float64)
        direction = far_pt - origin
        norm = np.linalg.norm(direction)
        if norm < 1e-12:
            return None, None
        direction /= norm
        return origin, direction

    def _ray_plane_intersection_z(self, ray_origin, ray_dir, plane_z):
        """
        Intersect ray with horizontal plane z = plane_z.
        Returns (3,) point or None.
        """
        if abs(ray_dir[2]) < 1e-10:
            return None
        t = (plane_z - ray_origin[2]) / ray_dir[2]
        if t < 0:
            return None
        return ray_origin + t * ray_dir

    def _compute_ik_target_from_mouse(self, mouse_pt):
        """
        Compute the world position the mouse is pointing at on
        the horizontal plane at the current IK target Z height.
        Returns (3,) point or None.
        """
        origin, direction = self._screen_to_world_ray(mouse_pt)
        if origin is None:
            return None
        plane_z = self.ik_target_z
        pt = self._ray_plane_intersection_z(origin, direction, plane_z)
        if pt is None:
            return None
        # Clip to a reasonable workspace radius (~0.7m from base)
        dist = np.linalg.norm(pt[:2])
        if dist > 0.75:
            scale = 0.75 / dist
            pt[0] *= scale
            pt[1] *= scale
        return pt

    # ── Override mouse events for IK mode ──

    def mousePressEvent(self, event: QMouseEvent):
        if self.ik_mode and event.button() == Qt.LeftButton:
            # In IK mode, left click/drag moves the EEF
            target = self._compute_ik_target_from_mouse(event.pos())
            if target is not None:
                self.ik_target_pos = target
                self.ik_dragging = True
                self.last_mouse_pos = event.pos()
                # Do an initial IK solve immediately
                new_q = franka_ik_toward_target(
                    self.ik_target_pos, self.joint_angles,
                    steps=IK_DRAG_SMOOTH_STEPS * 2)
                self.joint_angles[:] = new_q
                if self._ik_joint_callback:
                    self._ik_joint_callback(new_q)
                if self._ik_target_callback:
                    self._ik_target_callback(self.ik_target_pos, self.ik_target_z)
                self.update()
            return

        # Default behavior (orbit camera)
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.ik_mode and self.ik_dragging and self.last_mouse_pos:
            # IK drag: update target position
            target = self._compute_ik_target_from_mouse(event.pos())
            if target is not None:
                self.ik_target_pos = target
                # IK solving happens in _on_timer (each frame)
                if self._ik_target_callback:
                    self._ik_target_callback(self.ik_target_pos, self.ik_target_z)
            return

        # Default: orbit camera
        if self.is_dragging and self.last_mouse_pos:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            self.cam_azimuth += dx * 0.5
            self.cam_elevation = np.clip(
                self.cam_elevation + dy * 0.5, -80, 80)
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.ik_mode and self.ik_dragging:
            self.ik_dragging = False
            self.last_mouse_pos = None
            return
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.last_mouse_pos = None

    # ───── IK Mode Public API ─────

    def set_ik_mode(self, enabled: bool):
        """Enable or disable IK control mode."""
        self.ik_mode = enabled
        self.ik_dragging = False
        if not enabled:
            self.ik_target_pos = None
        else:
            # Initialize target at current EEF position
            T = franka_fk(self.joint_angles)
            self.ik_target_pos = T[:3, 3].copy()
            self.ik_target_z = np.clip(self.ik_target_pos[2], IK_Z_MIN, IK_Z_MAX)
        self.update()

    def set_ik_z(self, z: float):
        """Set IK control plane Z height."""
        self.ik_target_z = np.clip(z, IK_Z_MIN, IK_Z_MAX)
        if self.ik_target_pos is not None:
            self.ik_target_pos[2] = self.ik_target_z
        self.update()

    def get_ik_target(self):
        """Return current IK target (pos, z) or (None, z)."""
        return self.ik_target_pos, self.ik_target_z

    def set_ik_callbacks(self, target_cb=None, joint_cb=None):
        """
        target_cb(pos_3, z): called when IK target/Z changes
        joint_cb(angles_7): called when joint angles are updated by IK
        """
        self._ik_target_callback = target_cb
        self._ik_joint_callback = joint_cb

    # ───── IK Target indicator rendering ─────

    def _draw_ik_target(self):
        """Draw the IK target crosshair and guide line in 3D viewport."""
        if not self.ik_mode or self.ik_target_pos is None or not self.ik_visible:
            return

        target = self.ik_target_pos
        T_ee = franka_fk(self.joint_angles)
        eef_pos = T_ee[:3, 3]

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)

        # ── Guide line: current EEF → target ──
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glColor4f(1.0, 0.9, 0.1, 0.6)
        glVertex3f(eef_pos[0], eef_pos[1], eef_pos[2])
        glVertex3f(target[0], target[1], target[2])
        glEnd()

        # ── Plane indicator: transparent ring at the control plane ──
        glColor4f(1.0, 0.9, 0.1, 0.15)
        glBegin(GL_LINE_LOOP)
        radius = 0.15
        segments = 32
        for i in range(segments):
            angle = 2.0 * np.pi * i / segments
            gx = target[0] + radius * np.cos(angle)
            gy = target[1] + radius * np.sin(angle)
            glVertex3f(gx, gy, self.ik_target_z)
        glEnd()

        # ── Target crosshair ──
        glLineWidth(3.0)
        glBegin(GL_LINES)
        size = 0.025
        # X arms
        glColor4f(1.0, 0.2, 0.2, 0.9)
        glVertex3f(target[0] - size, target[1], target[2])
        glVertex3f(target[0] + size, target[1], target[2])
        # Y arms
        glColor4f(0.2, 1.0, 0.2, 0.9)
        glVertex3f(target[0], target[1] - size, target[2])
        glVertex3f(target[0], target[1] + size, target[2])
        # Z arms (drawn slightly above)
        glColor4f(0.2, 0.2, 1.0, 0.9)
        glVertex3f(target[0], target[1], target[2] - size)
        glVertex3f(target[0], target[1], target[2] + size)
        glEnd()

        # ── Target sphere ──
        glPointSize(8.0)
        glBegin(GL_POINTS)
        glColor4f(1.0, 0.9, 0.1, 1.0)
        glVertex3f(*target)
        glEnd()

        # ── Z distance label (floating line from target to plane) ──
        if abs(target[2] - self.ik_target_z) > 0.005:
            glLineWidth(1.0)
            glBegin(GL_LINES)
            glColor4f(0.5, 0.5, 1.0, 0.3)
            glVertex3f(target[0], target[1], target[2])
            glVertex3f(target[0], target[1], self.ik_target_z)
            glEnd()

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glLineWidth(1.0)

    # ───── Drawing helpers ─────

    def _draw_grid(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor4f(*COLORS["grid"])
        size = 1.0
        steps = 10
        for i in range(-steps, steps + 1):
            x = size * i / steps
            glVertex3f(x, -size, 0.0)
            glVertex3f(x, size, 0.0)
            glVertex3f(-size, x, 0.0)
            glVertex3f(size, x, 0.0)
        glEnd()
        glEnable(GL_LIGHTING)

    def _draw_table(self):
        glPushMatrix()
        glColor4f(*COLORS["table"])
        glTranslatef(0.4, 0.0, -0.01)
        glScalef(0.5, 0.35, 0.02)
        self._draw_unit_cube()
        glPopMatrix()

    def _draw_unit_cube(self):
        """Draw a unit cube centered at origin."""
        verts = [
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5],  [0.5, -0.5, 0.5],  [0.5, 0.5, 0.5],  [-0.5, 0.5, 0.5],
        ]
        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5),
        ]
        normals = [
            (0, 0, -1), (0, 0, 1), (0, -1, 0),
            (0, 1, 0), (-1, 0, 0), (1, 0, 0),
        ]
        glBegin(GL_QUADS)
        for face, normal in zip(faces, normals):
            glNormal3fv(normal)
            for idx in face:
                glVertex3fv(verts[idx])
        glEnd()

    def _draw_cubes(self):
        for idx, (name, pos) in enumerate(self.cube_positions.items()):
            # Skip if attached to gripper (render at EEF)
            if self.cube_attached.get(name, False):
                continue

            glPushMatrix()
            glColor4f(*COLORS[CUBE_COLORS[idx % 3]])
            glTranslatef(pos[0], pos[1], pos[2] + CUBE_SIZE / 2)
            # Apply orientation
            q = self.cube_orientations[name]
            if q is not None and np.linalg.norm(q) > 0:
                glRotatef(2 * np.degrees(np.arccos(np.clip(q[0], -1, 1))),
                          q[1], q[2], q[3])
            glScalef(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
            self._draw_unit_cube()
            glPopMatrix()

    def _draw_robot(self):
        """Draw the robot arm using FK chain."""
        transforms = franka_fk_with_ee(self.joint_angles)

        # Draw base
        glPushMatrix()
        glColor4f(*COLORS["base"])
        glTranslatef(0, 0, -0.02)
        glScalef(0.15, 0.15, 0.04)
        self._draw_unit_cube()
        glPopMatrix()

        # Draw links and joints
        prev_pos = np.array([0.0, 0.0, 0.0])
        for i in range(7):
            joint_pos = transforms[i][:3, 3]
            next_pos = transforms[i + 1][:3, 3] if i < 6 else transforms[6][:3, 3]

            # Link (cylinder from prev joint to current joint)
            if i == 0:
                start = prev_pos
            else:
                start = transforms[i - 1][:3, 3]

            end = joint_pos
            self._draw_cylinder(start, end, 0.025 + (7 - i) * 0.003,
                                COLORS["link_1"] if i % 2 == 0 else COLORS["link_2"])

            # Joint (sphere)
            glPushMatrix()
            glColor4f(*COLORS["joint"])
            glTranslatef(joint_pos[0], joint_pos[1], joint_pos[2])
            quadric = gluNewQuadric()
            gluSphere(quadric, JOINT_RADII[i], 12, 12)
            gluDeleteQuadric(quadric)
            glPopMatrix()

            # Rotation axis arrow (shows the DOF axis direction)
            # Joint i+1 rotates about z_i:
            #   z_0 = base z-axis = [0,0,1]  (constant)
            #   z_i = transforms[i-1][:3,2]  for i >= 1
            if i == 0:
                axis_dir = np.array([0.0, 0.0, 1.0])
            else:
                axis_dir = transforms[i - 1][:3, 2]
            self._draw_axis_arrow(joint_pos, axis_dir,
                                  AXIS_ARROW_LENGTH, JOINT_AXIS_COLORS[i])

            prev_pos = joint_pos

        # End-effector
        ee_pos = transforms[-1][:3, 3]
        glPushMatrix()
        glColor4f(*COLORS["eef"])
        glTranslatef(ee_pos[0], ee_pos[1], ee_pos[2])
        quadric = gluNewQuadric()
        gluSphere(quadric, 0.03, 10, 10)
        gluDeleteQuadric(quadric)
        glPopMatrix()

        # Gripper fingers
        self._draw_gripper(transforms[-1])

        # Draw attached cube at EEF
        for name, attached in self.cube_attached.items():
            if attached:
                idx = list(self.cube_attached.keys()).index(name)
                glPushMatrix()
                glColor4f(*COLORS[CUBE_COLORS[idx % 3]])
                glTranslatef(ee_pos[0], ee_pos[1], ee_pos[2] - CUBE_SIZE / 2)
                glScalef(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
                self._draw_unit_cube()
                glPopMatrix()

    def _draw_gripper(self, ee_transform):
        """Draw two gripper fingers."""
        half_open = self.gripper_width / 2
        ee_pos = ee_transform[:3, 3]
        R = ee_transform[:3, :3]
        
        # Finger directions (perpendicular to gripper approach direction)
        # Franka gripper opens along y-axis of EEF frame
        finger_dir = R[:, 1]  # y-axis
        approach_dir = R[:, 2]  # z-axis (approach direction)

        for sign in [-1, 1]:
            finger_pos = ee_pos + finger_dir * sign * (GRIPPER_FINGER_OFFSET + half_open)
            self._draw_cylinder(
                ee_pos + finger_dir * sign * GRIPPER_FINGER_OFFSET,
                finger_pos,
                0.01,
                COLORS["gripper"]
            )
            # Finger tip
            glPushMatrix()
            glColor4f(*COLORS["gripper"])
            glTranslatef(finger_pos[0], finger_pos[1], finger_pos[2])
            quadric = gluNewQuadric()
            gluSphere(quadric, 0.012, 8, 8)
            gluDeleteQuadric(quadric)
            glPopMatrix()

    def _draw_cylinder(self, p1, p2, radius, color):
        """Draw a cylinder between two 3D points."""
        p1 = np.asarray(p1, dtype=np.float64)
        p2 = np.asarray(p2, dtype=np.float64)
        direction = p2 - p1
        height = np.linalg.norm(direction)
        if height < 1e-6:
            return

        direction = direction / height

        # Rotation axis to align Z with direction
        z_axis = np.array([0.0, 0.0, 1.0])
        if np.abs(np.dot(direction, z_axis)) > 0.999:
            rot_axis = np.array([1.0, 0.0, 0.0])
            angle = 0.0 if np.dot(direction, z_axis) > 0 else np.pi
        else:
            rot_axis = np.cross(z_axis, direction)
            rot_axis = rot_axis / np.linalg.norm(rot_axis)
            angle = np.arccos(np.clip(np.dot(z_axis, direction), -1, 1))

        glPushMatrix()
        glColor4f(*color)
        glTranslatef(p1[0], p1[1], p1[2])
        glRotatef(np.degrees(angle), rot_axis[0], rot_axis[1], rot_axis[2])
        quadric = gluNewQuadric()
        gluCylinder(quadric, radius, radius, height, 16, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def _draw_axis_arrow(self, origin, direction, length, color):
        """Draw a 3D arrow indicating a rotation axis.

        The shaft is a thin cylinder; the head is a cone.
        The arrow points from ``origin`` along ``direction`` for ``length`` meters.
        The direction vector is the exact rotation axis from the DH model.
        """
        direction = np.asarray(direction, dtype=np.float64)
        dir_norm = np.linalg.norm(direction)
        if dir_norm < 1e-6:
            return
        direction = direction / dir_norm

        shaft_len = length * 0.7
        head_len = length * 0.3
        shaft_radius = 0.006
        head_base_radius = 0.022

        shaft_end = origin + direction * shaft_len
        head_end = origin + direction * length  # noqa (tip, not used directly)

        # Shaft (thin cylinder)
        self._draw_cylinder(origin, shaft_end, shaft_radius, color)

        # Align Z-axis with arrow direction for gluCylinder
        z_axis = np.array([0.0, 0.0, 1.0])
        if np.abs(np.dot(direction, z_axis)) > 0.9999:
            rot_axis = np.array([1.0, 0.0, 0.0])
            angle = 0.0 if np.dot(direction, z_axis) > 0 else np.pi
        else:
            rot_axis = np.cross(z_axis, direction)
            rot_axis = rot_axis / np.linalg.norm(rot_axis)
            angle = np.arccos(np.clip(np.dot(z_axis, direction), -1.0, 1.0))

        glPushMatrix()
        glColor4f(*color)
        glTranslatef(shaft_end[0], shaft_end[1], shaft_end[2])
        glRotatef(np.degrees(angle), rot_axis[0], rot_axis[1], rot_axis[2])
        quadric = gluNewQuadric()
        gluCylinder(quadric, head_base_radius, 0.0, head_len, 12, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    # ───── Public API for external control ─────

    def update_robot(self, joint_angles, gripper_width):
        """Update robot configuration from external controller.
        In IK mode, the viewer owns the joint angles (IK solver writes them),
        so external updates are ignored to avoid overwriting IK results.
        """
        if not self.ik_mode:
            self.joint_angles = joint_angles.copy()
            self.gripper_width = gripper_width

    def update_cubes(self, positions, orientations=None, attached=None):
        """Update cube states."""
        for name, pos in positions.items():
            if name in self.cube_positions:
                self.cube_positions[name] = pos.copy()
        if orientations:
            for name, q in orientations.items():
                if name in self.cube_orientations:
                    self.cube_orientations[name] = q.copy()
        if attached:
            self.cube_attached.update(attached)

    def get_eef_pose(self):
        """Get current EEF position for IK targeting."""
        transforms = franka_fk_with_ee(self.joint_angles)
        return transforms[-1]
