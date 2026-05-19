"""
QOpenGLWidget-based 3D viewer for the robot arm.

Renders:
  - Ground grid
  - Table surface
  - Robot base, links (cylinders), joints (spheres)
  - Gripper fingers (two boxes)
  - Cubes (coloured boxes)
  - EEF coordinate axes

Camera: orbit (azimuth/elevation) + zoom.
"""

import math
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent, QWheelEvent
from OpenGL.GL import (
    glClear, glClearColor, glEnable, glDisable, glDepthFunc,
    glBlendFunc, glHint, glMatrixMode, glLoadIdentity, glViewport,
    glBegin, glEnd, glVertex3f, glColor3f, glColor4f, glNormal3f,
    glTranslatef, glRotatef, glScalef, glPushMatrix, glPopMatrix, glMultMatrixf,
    glLightfv, glMaterialfv, glLineWidth, glPolygonMode, glShadeModel,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_LEQUAL, GL_NICEST, GL_LIGHTING, GL_LIGHT0, GL_LIGHT1,
    GL_PERSPECTIVE_CORRECTION_HINT,
    GL_POSITION, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR,
    GL_FRONT_AND_BACK, GL_FILL, GL_LINE, GL_BLEND, GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA, GL_FLAT, GL_SMOOTH,
    GL_QUADS, GL_TRIANGLES, GL_LINES, GL_TRIANGLE_FAN,
    GL_PROJECTION, GL_MODELVIEW, GL_AMBIENT_AND_DIFFUSE,
)
from OpenGL.GLU import gluPerspective, gluCylinder, gluSphere, gluDisk, gluNewQuadric, gluQuadricNormals, gluDeleteQuadric, GLU_SMOOTH

from config import (
    NUM_JOINTS, LINK_RADIUS, LINK_SEGMENTS, JOINT_RADIUS,
    BASE_RADIUS, BASE_HEIGHT, TABLE_SIZE, TABLE_HEIGHT,
    GRIPPER_LENGTH, GRIPPER_WIDTH, GRIPPER_HEIGHT,
    NUM_CUBES, CUBE_SIZE, CUBE_COLORS,
    COLOR_BG, COLOR_GRID, COLOR_TABLE, COLOR_BASE,
    COLOR_LINK, COLOR_JOINT, COLOR_GRIPPER,
    COLOR_EEF_MARK, COLOR_EEF_MARK_Y, COLOR_EEF_MARK_Z,
)


class RobotViewer(QOpenGLWidget):
    """Interactive 3D viewport for robot arm simulation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 480)
        self.setMouseTracking(True)

        # Camera state
        self._azimuth = 35.0      # degrees
        self._elevation = 25.0
        self._distance = 1.6
        self._last_mouse = None

        # Robot state (set externally)
        self.joint_angles = np.zeros(NUM_JOINTS, dtype=np.float64)
        self.gripper_width = 0.04
        self.cube_positions = np.zeros((NUM_CUBES, 3), dtype=np.float64)
        self.cube_orientations = np.zeros((NUM_CUBES, 4), dtype=np.float64)
        self.cube_attached = [False] * NUM_CUBES

        # FK transforms (updated by update_robot)
        self.T_all = None

        # Enable auto-refresh via timer (for smooth animation)
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self.update)
        self._refresh_timer.start(16)  # ~60 fps

    # ── Public API ──────────────────────────────

    def set_joint_angles(self, q):
        self.joint_angles = np.asarray(q, dtype=np.float64)
        self._update_fk()

    def set_gripper(self, width):
        self.gripper_width = float(width)

    def set_cube(self, idx, pos, quat=None, attached=False):
        self.cube_positions[idx] = np.asarray(pos, dtype=np.float64)
        if quat is not None:
            self.cube_orientations[idx] = np.asarray(quat, dtype=np.float64)
        self.cube_attached[idx] = attached

    def update_robot(self, q, gripper, cubes_data=None):
        """Batch update from external timer."""
        self.joint_angles = np.asarray(q, dtype=np.float64)
        self.gripper_width = float(gripper)
        if cubes_data is not None:
            for idx, (pos, quat, att) in enumerate(cubes_data):
                self.cube_positions[idx] = np.asarray(pos)
                self.cube_orientations[idx] = np.asarray(quat)
                self.cube_attached[idx] = att
        self._update_fk()

    # ── Internal ────────────────────────────────

    def _update_fk(self):
        from kinematics import forward_kinematics, get_eef_pose
        self.T_all = forward_kinematics(self.joint_angles)

    def _camera_transform(self):
        glTranslatef(0.0, -0.1, -self._distance)
        glRotatef(self._elevation, 1, 0, 0)
        glRotatef(self._azimuth, 0, 1, 0)

    # ── Qt OpenGL overrides ─────────────────────

    def initializeGL(self):
        glClearColor(*COLOR_BG)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glShadeModel(GL_SMOOTH)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        # Light 0: key light (upper-right-front)
        glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 3.0, 4.0, 0.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])

        # Light 1: fill (lower-left-back)
        glLightfv(GL_LIGHT1, GL_POSITION, [-1.0, -2.0, -1.0, 0.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.4, 0.4, 0.4, 1.0])

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / max(h, 1)
        gluPerspective(45.0, aspect, 0.01, 10.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self._camera_transform()

        self._draw_grid()
        self._draw_table()
        self._draw_base()
        self._draw_robot()
        self._draw_gripper()
        self._draw_cubes()
        self._draw_eef_axes()

    # ── Drawing helpers ─────────────────────────

    def _draw_grid(self):
        glDisable(GL_LIGHTING)
        glColor3f(*COLOR_GRID[:3])
        glLineWidth(1.0)
        half = 0.5
        step = 0.1
        glBegin(GL_LINES)
        x = -half
        while x <= half + 1e-6:
            glVertex3f(x, -half, 0.0)
            glVertex3f(x,  half, 0.0)
            x += step
        y = -half
        while y <= half + 1e-6:
            glVertex3f(-half, y, 0.0)
            glVertex3f( half, y, 0.0)
            y += step
        glEnd()
        glEnable(GL_LIGHTING)

    def _draw_table(self):
        glPushMatrix()
        glTranslatef(0.0, 0.0, -TABLE_HEIGHT / 2)
        self._draw_box(TABLE_SIZE, TABLE_SIZE, TABLE_HEIGHT, COLOR_TABLE)
        glPopMatrix()

    def _draw_base(self):
        """Draw a flat horizontal base disc (solid cylinder with caps)."""
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0)
        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                     [*COLOR_BASE[:3], 1.0])
        # Bottom flat face (horizontal disc)
        gluDisk(quadric, 0, BASE_RADIUS, 24, 1)
        # Side wall (vertical)
        gluCylinder(quadric, BASE_RADIUS, BASE_RADIUS, BASE_HEIGHT, 24, 1)
        # Top flat face (horizontal disc)
        glTranslatef(0.0, 0.0, BASE_HEIGHT)
        gluDisk(quadric, 0, BASE_RADIUS, 24, 1)
        gluDeleteQuadric(quadric)
        glPopMatrix()

    def _draw_robot(self):
        """Draw links (cylinders) and joint spheres along kinematic chain."""
        if self.T_all is None:
            return

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)

        for i in range(NUM_JOINTS):
            T_i = self.T_all[i]
            T_next = self.T_all[i + 1]

            p_i = T_i[:3, 3]
            p_next = T_next[:3, 3]
            direction = p_next - p_i
            length = np.linalg.norm(direction)
            if length < 1e-8:
                continue

            # Draw joint sphere at pivot
            glPushMatrix()
            glTranslatef(*p_i)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                         [*COLOR_JOINT[:3], 1.0])
            gluSphere(quadric, JOINT_RADIUS, 16, 12)
            glPopMatrix()

            # Draw link cylinder along direction
            centre = 0.5 * (p_i + p_next)
            axis = direction / length
            glPushMatrix()
            glTranslatef(*centre)

            # Rotate cylinder to align Z with direction axis
            z_axis = np.array([0.0, 0.0, 1.0])
            if np.abs(np.dot(axis, z_axis)) < 0.9999:
                rot_axis = np.cross(z_axis, axis)
                rot_axis = rot_axis / np.linalg.norm(rot_axis)
                angle = np.degrees(np.arccos(np.clip(np.dot(z_axis, axis), -1.0, 1.0)))
                glRotatef(angle, *rot_axis)
            elif np.dot(axis, z_axis) < 0:
                glRotatef(180.0, 1, 0, 0)

            radius = LINK_SEGMENTS[i][0] if i < len(LINK_SEGMENTS) else LINK_RADIUS
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                         [*COLOR_LINK[:3], 1.0])
            gluCylinder(quadric, radius, radius, length, 16, 1)
            glPopMatrix()

        gluDeleteQuadric(quadric)

    def _draw_gripper(self):
        if self.T_all is None or len(self.T_all) < 8:
            return

        T_ee = self.T_all[-1]
        pos = T_ee[:3, 3]
        R = T_ee[:3, :3]

        half_open = self.gripper_width / 2.0
        finger_offset = GRIPPER_WIDTH + half_open

        # Two fingers
        for side in [-1, 1]:
            offset = R @ np.array([0.0, side * finger_offset, 0.0])
            centre = pos + offset
            glPushMatrix()
            glTranslatef(*centre)

            # Orient gripper aligned with EEF frame (Z along gripper axis)
            # EEF frame: Z = approach, Y = sliding axis
            forward = R[:, 2]
            side_axis = R[:, 1]
            up = R[:, 0]

            # Build rotation from standard orientation
            mat = np.eye(4)
            mat[:3, 0] = side_axis
            mat[:3, 1] = up
            mat[:3, 2] = forward
            glMultMatrixf(mat.T.flatten())

            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                         [*COLOR_GRIPPER[:3], 1.0])
            self._draw_box(GRIPPER_WIDTH, GRIPPER_HEIGHT, GRIPPER_LENGTH,
                           COLOR_GRIPPER)
            glPopMatrix()

    def _draw_cubes(self):
        for i in range(NUM_CUBES):
            pos = self.cube_positions[i]
            glPushMatrix()
            glTranslatef(*pos)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
                         [*CUBE_COLORS[i], 1.0])
            self._draw_box(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE, CUBE_COLORS[i])
            glPopMatrix()

    def _draw_eef_axes(self):
        if self.T_all is None:
            return
        T_ee = self.T_all[-1]
        pos = T_ee[:3, 3]
        R = T_ee[:3, :3]
        axis_len = 0.05

        glDisable(GL_LIGHTING)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        for i, col in enumerate([COLOR_EEF_MARK, COLOR_EEF_MARK_Y, COLOR_EEF_MARK_Z]):
            glColor3f(*col[:3])
            glVertex3f(*pos)
            glVertex3f(*(pos + R[:, i] * axis_len))
        glEnd()
        glEnable(GL_LIGHTING)

    @staticmethod
    def _draw_box(w, h, d, colour):
        """Axis-aligned box centred at origin."""
        hw, hh, hd = w / 2, h / 2, d / 2
        vertices = [
            # Each face: (position, normal)
            ([-hw, -hh, -hd, -hw, -hh,  hd, -hw,  hh,  hd, -hw,  hh, -hd], [-1, 0, 0]),
            ([ hw, -hh, -hd,  hw,  hh, -hd,  hw,  hh,  hd,  hw, -hh,  hd], [ 1, 0, 0]),
            ([-hw, -hh, -hd,  hw, -hh, -hd,  hw, -hh,  hd, -hw, -hh,  hd], [ 0,-1, 0]),
            ([-hw,  hh, -hd, -hw,  hh,  hd,  hw,  hh,  hd,  hw,  hh, -hd], [ 0, 1, 0]),
            ([-hw, -hh, -hd, -hw,  hh, -hd,  hw,  hh, -hd,  hw, -hh, -hd], [ 0, 0,-1]),
            ([-hw, -hh,  hd,  hw, -hh,  hd,  hw,  hh,  hd, -hw,  hh,  hd], [ 0, 0, 1]),
        ]
        glBegin(GL_QUADS)
        for verts, norm in vertices:
            glNormal3f(*norm)
            for k in range(4):
                i3 = k * 3
                glVertex3f(verts[i3], verts[i3 + 1], verts[i3 + 2])
        glEnd()

    # ── Mouse camera control ────────────────────

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._last_mouse = (event.pos().x(), event.pos().y())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._last_mouse is None:
            return
        dx = event.pos().x() - self._last_mouse[0]
        dy = event.pos().y() - self._last_mouse[1]
        self._azimuth += dx * 0.5
        self._elevation = np.clip(self._elevation - dy * 0.5, -89, 89)
        self._last_mouse = (event.pos().x(), event.pos().y())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._last_mouse = None

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        self._distance *= (1.0 - delta * 0.001)
        self._distance = np.clip(self._distance, 0.3, 4.0)
