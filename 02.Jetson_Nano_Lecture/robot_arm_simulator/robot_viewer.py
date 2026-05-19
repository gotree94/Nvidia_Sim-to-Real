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

from kinematics import franka_fk_with_ee, rotation_matrix_to_quat
from config import COLORS, JOINT_RADII, LINK_LENGTHS, CUBE_POSITIONS, CUBE_SIZE, CUBE_COLORS
from config import GRIPPER_FINGER_OFFSET, EE_OFFSET


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

        # Timer for continuous rendering
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
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
        self.cam_dist = np.clip(self.cam_dist - delta * 0.002, 0.5, 8.0)
        self.update()

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

    # ───── Public API for external control ─────

    def update_robot(self, joint_angles, gripper_width):
        """Update robot configuration from external controller."""
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
