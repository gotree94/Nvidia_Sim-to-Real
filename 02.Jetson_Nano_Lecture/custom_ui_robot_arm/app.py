"""
Main application window.

Layout:
   ┌─────────────────────────────────────────┐
   │  [Render]                │ [Control Panel]  │
   │  3D Viewport            │ J1 ──●── 0.000  │
   │  (RobotViewer)           │ J2 ──●── 0.000  │
   │                          │ ...              │
   │                          │ EEF: x y z q     │
   │                          │ Gripper: ████    │
   │                          │ Speed: ██ 1.0x   │
   │                          │ [IK] [Pose] [▶]  │
   │                          │ [Rec] [Save]     │
   │                          │ subtask btns     │
   │                          │ Status log       │
   └─────────────────────────────────────────┘

Keyboard map:
   Joint mode (default):
     W/S  J1   E/D  J2   R/F  J3   T/G  J4
     Y/H  J5   U/J  J6   I/K  J7
     Z    close gripper   X    open gripper
   IK mode (toggle M):
     W/S  EEF Z+/-   A/D  EEF X-/+
     E/Q  EEF Y+/-   R/F  Roll
     T/G  Pitch      Y/H  Yaw
   Global:
     Space   Record on/off       Shift   Fast mode
     1/2/3   Subtask toggle      V      Cube attach
     M       Toggle IK/Joint     F1     Help
     Backspace Reset home        P      Open playback
     Ctrl+S  Save HDF5
"""

import os
import json
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QGroupBox, QLabel, QSlider, QPushButton,
    QCheckBox, QTextEdit, QFileDialog, QMessageBox,
    QApplication, QDoubleSpinBox, QDialog,
    QListWidget, QLineEdit,
)
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from PyQt5.QtGui import QFont, QKeyEvent, QCloseEvent

from config import (
    NUM_JOINTS, JOINT_LIMITS, HOME_POSITION,
    PRESET_POSITIONS, PRESET_NAMES,
    GRIPPER_DEFAULT, GRIPPER_OPEN, GRIPPER_CLOSED,
    JOINT_STEP_SLOW, JOINT_STEP_FAST, GRIPPER_STEP,
    EEF_POS_STEP, EEF_ROT_STEP,
    NUM_CUBES, CUBE_INITIAL_POSITIONS, SUBTASK_NAMES,
    DEFAULT_FPS, SPEED_MIN, SPEED_MAX, SPEED_DEFAULT,
)
from kinematics import (
    forward_kinematics, get_eef_pose, inverse_kinematics,
    clamp_joints, quat_to_matrix, quat_from_matrix,
    rot_x, rot_y, rot_z,
)
from renderer import RobotViewer
from recorder import Recorder
from playback import PlaybackDialog


# ═══════════════════════════════════════════════
# Help Overlay Dialog
# ═══════════════════════════════════════════════

class HelpOverlay(QDialog):
    """F1 keyboard shortcut reference overlay."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setFixedSize(540, 500)
        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; color: #d4d4d4; }
            QLabel { color: #d4d4d4; padding: 2px 10px; }
            QPushButton {
                background: #0e639c; color: white; border: none;
                padding: 6px; border-radius: 3px; font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        title = QLabel("Keyboard & Mouse Controls")
        title.setFont(QFont("Segoe UI", 13, QFont.Bold))
        layout.addWidget(title)

        help_text = QLabel(self._help_content())
        help_text.setFont(QFont("Consolas", 9))
        help_text.setWordWrap(True)
        help_text.setStyleSheet(
            "background: #252526; border: 1px solid #333; padding: 10px;")
        layout.addWidget(help_text)

        close_btn = QPushButton("Close  (F1)")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    @staticmethod
    def _help_content():
        return (
            "═══════════════════════════════════════\n"
            "  JOINT CONTROL MODE  (default)\n"
            "═══════════════════════════════════════\n"
            "  W/S  Joint 1        E/D  Joint 2\n"
            "  R/F  Joint 3        T/G  Joint 4\n"
            "  Y/H  Joint 5        U/J  Joint 6\n"
            "  I/K  Joint 7\n"
            "  Z    Close gripper  X    Open gripper\n"
            "\n"
            "═══════════════════════════════════════\n"
            "  IK MODE  (M to toggle)\n"
            "═══════════════════════════════════════\n"
            "  W/S  EEF Z+/- (up/down)\n"
            "  A/D  EEF X-/+ (left/right)\n"
            "  E/Q  EEF Y+/- (forward/back)\n"
            "  R/F  Roll +/-   T/G  Pitch +/-\n"
            "  Y/H  Yaw +/-\n"
            "\n"
            "═══════════════════════════════════════\n"
            "  GLOBAL\n"
            "═══════════════════════════════════════\n"
            "  Space     Record on/off\n"
            "  1/2/3     Subtask grasp_1/2/stack_1\n"
            "  C/B/N     Subtask (alt keys)\n"
            "  V         Attach/detach cube\n"
            "  M         Toggle IK / Joint mode\n"
            "  Shift     Fast mode (joint ctrl)\n"
            "  F1        Toggle this help\n"
            "  Backspace Reset to home\n"
            "  P         Open playback viewer\n"
            "  Ctrl+S    Save HDF5\n"
            "\n"
            "═══════════════════════════════════════\n"
            "  MOUSE\n"
            "═══════════════════════════════════════\n"
            "  Left drag  Orbit camera\n"
            "  Scroll     Zoom in/out\n"
        )


# ═══════════════════════════════════════════════
# Pose Preset Manager Dialog
# ═══════════════════════════════════════════════

class PoseManager(QDialog):
    """Save / load named joint-angle presets to/from JSON."""

    PRESETS_FILE = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".pose_presets.json")

    def __init__(self, current_joints, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pose Presets")
        self.setFixedSize(380, 340)
        self.current_joints = np.asarray(current_joints)
        self.presets = self._load_presets()
        self.selected_name = None

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        title = QLabel("Save / Load Joint Presets")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("Consolas", 10))
        self.list_widget.addItems(self.presets.keys())
        layout.addWidget(self.list_widget)

        nr = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Preset name...")
        self.name_input.setFont(QFont("Consolas", 10))
        save_btn = QPushButton("Save Current")
        save_btn.clicked.connect(self._save_preset)
        nr.addWidget(self.name_input)
        nr.addWidget(save_btn)
        layout.addLayout(nr)

        br = QHBoxLayout()
        load_btn = QPushButton("Load Selected")
        load_btn.clicked.connect(self._load_selected)
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._delete_selected)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        br.addWidget(load_btn)
        br.addWidget(delete_btn)
        br.addWidget(cancel_btn)
        layout.addLayout(br)

        self._apply_dark_style()

    def _apply_dark_style(self):
        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; color: #d4d4d4; }
            QLabel, QLineEdit { color: #d4d4d4; }
            QListWidget {
                background: #252526; color: #d4d4d4;
                border: 1px solid #3c3c3c;
            }
            QListWidget::item:selected { background: #094771; }
            QLineEdit {
                background: #252526; border: 1px solid #3c3c3c;
                padding: 4px;
            }
            QPushButton {
                background: #0e639c; color: white; border: none;
                padding: 5px 12px; border-radius: 3px;
            }
            QPushButton:hover { background: #1177bb; }
        """)

    def _load_presets(self):
        try:
            with open(self.PRESETS_FILE, "r") as f:
                d = json.load(f)
                return {k: np.array(v, dtype=np.float64).tolist()
                        for k, v in d.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_presets_to_disk(self):
        os.makedirs(os.path.dirname(self.PRESETS_FILE) or ".", exist_ok=True)
        serializable = {
            k: (v.tolist() if isinstance(v, np.ndarray) else v)
            for k, v in self.presets.items()
        }
        with open(self.PRESETS_FILE, "w") as f:
            json.dump(serializable, f, indent=2)

    def _save_preset(self):
        name = self.name_input.text().strip()
        if not name:
            return
        self.presets[name] = self.current_joints.tolist()
        self._save_presets_to_disk()
        self.list_widget.clear()
        self.list_widget.addItems(self.presets.keys())
        self.name_input.clear()

    def _load_selected(self):
        item = self.list_widget.currentItem()
        if item is None:
            return
        self.selected_name = item.text()
        self.accept()

    def _delete_selected(self):
        item = self.list_widget.currentItem()
        if item is None:
            return
        name = item.text()
        if name in self.presets:
            del self.presets[name]
            self._save_presets_to_disk()
            self.list_widget.clear()
            self.list_widget.addItems(self.presets.keys())

    def get_selected_pose(self):
        if self.selected_name and self.selected_name in self.presets:
            return np.array(self.presets[self.selected_name], dtype=np.float64)
        return None


# ═══════════════════════════════════════════════
# Control Panel
# ═══════════════════════════════════════════════

class ControlPanel(QWidget):
    """Right-side panel with all controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(320)
        self.setMaximumWidth(420)

        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(6, 6, 6, 6)

        font = QFont("Consolas", 9)
        bf = QFont("Segoe UI", 10, QFont.Bold)

        # ── Joint sliders + spin boxes ───────────
        jg = QGroupBox("Joint Angles (rad)")
        jg.setFont(bf)
        jl = QVBoxLayout(jg)
        jl.setSpacing(1)

        self.joint_sliders = []
        self.joint_spinboxes = []
        self.joint_labels = []
        self.joint_values = []

        for i in range(NUM_JOINTS):
            row = QHBoxLayout()
            row.setSpacing(4)
            lbl = QLabel(f"J{i+1}:")
            lbl.setFont(font)
            lbl.setFixedWidth(24)

            sld = QSlider(Qt.Horizontal)
            sld.setRange(0, 1000)
            sld.setValue(500)
            sld.setTickPosition(QSlider.TicksBelow)
            sld.setTickInterval(200)

            spn = QDoubleSpinBox()
            spn.setRange(JOINT_LIMITS[i, 0], JOINT_LIMITS[i, 1])
            spn.setDecimals(3)
            spn.setSingleStep(0.01)
            spn.setFont(font)
            spn.setFixedWidth(72)
            spn.setStyleSheet(
                "QDoubleSpinBox { background: #2d2d2d; color: #d4d4d4; "
                "border: 1px solid #3c3c3c; padding: 2px; }")

            val = QLabel("0.000")
            val.setFont(font)
            val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            val.setFixedWidth(55)

            row.addWidget(lbl)
            row.addWidget(sld)
            row.addWidget(spn)
            row.addWidget(val)
            jl.addLayout(row)

            self.joint_sliders.append(sld)
            self.joint_spinboxes.append(spn)
            self.joint_labels.append(val)
            self.joint_values.append(0.0)

            sld.valueChanged.connect(lambda v, idx=i: self._on_slider(idx, v))
            spn.valueChanged.connect(lambda v, idx=i: self._on_spin(idx, v))

        layout.addWidget(jg)

        # ── EEF pose readout ─────────────────────
        eg = QGroupBox("End-Effector Pose")
        eg.setFont(bf)
        el = QVBoxLayout(eg)
        el.setSpacing(1)

        self.eef_pos_label = QLabel("pos: (0.000, 0.000, 0.000)")
        self.eef_pos_label.setFont(font)
        self.eef_quat_label = QLabel("quat: (0.000, 0.000, 0.000, 1.000)")
        self.eef_quat_label.setFont(font)
        el.addWidget(self.eef_pos_label)
        el.addWidget(self.eef_quat_label)

        grip_row = QHBoxLayout()
        grip_row.addWidget(QLabel("Gripper:"))
        self.gripper_slider = QSlider(Qt.Horizontal)
        self.gripper_slider.setRange(0, 100)
        self.gripper_slider.setValue(100)
        self.gripper_value_label = QLabel("0.040")
        self.gripper_value_label.setFont(font)
        self.gripper_value_label.setFixedWidth(55)
        grip_row.addWidget(self.gripper_slider)
        grip_row.addWidget(self.gripper_value_label)
        el.addLayout(grip_row)
        self.gripper_slider.valueChanged.connect(self._on_gripper_slider)
        layout.addWidget(eg)

        # ── Speed control ────────────────────────
        sg = QGroupBox("Control Speed")
        sg.setFont(bf)
        sgl = QHBoxLayout(sg)
        sgl.setContentsMargins(8, 16, 8, 4)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(int(SPEED_MIN*10), int(SPEED_MAX*10))
        self.speed_slider.setValue(int(SPEED_DEFAULT*10))
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(5)

        self.speed_label = QLabel(f"{SPEED_DEFAULT:.1f}x")
        self.speed_label.setFont(QFont("Consolas", 11, QFont.Bold))
        self.speed_label.setFixedWidth(42)
        self.speed_label.setAlignment(Qt.AlignCenter)

        sgl.addWidget(QLabel("Slow"))
        sgl.addWidget(self.speed_slider)
        sgl.addWidget(self.speed_label)
        sgl.addWidget(QLabel("Fast"))
        self.speed_slider.valueChanged.connect(self._on_speed)
        layout.addWidget(sg)

        # ── Mode toggle + special buttons ────────
        mg = QGroupBox("Control Mode")
        mg.setFont(bf)
        ml = QHBoxLayout(mg)
        ml.setContentsMargins(8, 16, 8, 4)

        self.ik_mode_cb = QCheckBox("IK Mode (M)")
        self.ik_mode_cb.setFont(font)
        self.ik_mode_cb.setChecked(False)
        self.ik_mode_cb.toggled.connect(self._on_ik_toggle)

        self.pose_btn = QPushButton("Pose")
        self.pose_btn.clicked.connect(self._on_pose)

        self.play_btn = QPushButton("\u25b6 Play")
        self.play_btn.clicked.connect(self._on_playback)

        ml.addWidget(self.ik_mode_cb)
        ml.addWidget(self.pose_btn)
        ml.addWidget(self.play_btn)
        layout.addWidget(mg)

        # ── Subtask signals ──────────────────────
        subg = QGroupBox("Subtask Signals")
        subg.setFont(bf)
        subl = QVBoxLayout(subg)
        subl.setSpacing(1)

        self.subtask_checks = []
        for name in SUBTASK_NAMES:
            cb = QCheckBox(name)
            cb.setFont(font)
            subl.addWidget(cb)
            self.subtask_checks.append(cb)
        layout.addWidget(subg)

        # ── Recording controls ───────────────────
        rg = QGroupBox("Recording")
        rg.setFont(bf)
        rl = QHBoxLayout(rg)
        rl.setContentsMargins(6, 16, 6, 6)

        self.rec_btn = QPushButton("\u25cf Record")
        self.rec_btn.setStyleSheet(
            "QPushButton { background: #5a1a1a; color: #ff4444; "
            "font-weight: bold; padding: 5px 10px; }"
            "QPushButton:hover { background: #7a2a2a; }")
        self.rec_btn.clicked.connect(self._on_record)

        self.save_btn = QPushButton("\U0001f4be Save")
        self.save_btn.clicked.connect(self._on_save)
        self.cancel_btn = QPushButton("\u2715 Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel)
        self.reset_btn = QPushButton("\u21ba Reset")
        self.reset_btn.clicked.connect(self._on_reset)

        rl.addWidget(self.rec_btn)
        rl.addWidget(self.save_btn)
        rl.addWidget(self.cancel_btn)
        rl.addWidget(self.reset_btn)
        layout.addWidget(rg)

        # ── Status log ───────────────────────────
        stg = QGroupBox("Status")
        stg.setFont(bf)
        stl = QVBoxLayout(stg)
        stl.setSpacing(2)

        self.status_label = QLabel("Ready.  FPS: --")
        self.status_label.setFont(font)
        stl.addWidget(self.status_label)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont("Consolas", 8))
        self.log.setMaximumHeight(90)
        self.log.setStyleSheet(
            "QTextEdit { background: #1a1a1a; color: #ccc; "
            "border: 1px solid #333; }")
        stl.addWidget(self.log)
        layout.addWidget(stg)
        layout.addStretch()

        # callbacks (wired by MainWindow)
        self.on_record_clicked = None
        self.on_save_clicked = None
        self.on_cancel_clicked = None
        self.on_reset_clicked = None
        self.on_pose_clicked = None
        self.on_playback_clicked = None
        self.on_ik_toggled = None

    # ── Internal ────────────────────────────────

    def _on_slider(self, idx, value):
        norm = value / 1000.0
        jv = JOINT_LIMITS[idx, 0] + norm * (
            JOINT_LIMITS[idx, 1] - JOINT_LIMITS[idx, 0])
        self.joint_values[idx] = jv
        self.joint_labels[idx].setText(f"{jv:.3f}")
        self.joint_spinboxes[idx].blockSignals(True)
        self.joint_spinboxes[idx].setValue(jv)
        self.joint_spinboxes[idx].blockSignals(False)

    def _on_spin(self, idx, value):
        self.joint_values[idx] = value
        self.joint_labels[idx].setText(f"{value:.3f}")
        cv = np.clip(value, JOINT_LIMITS[idx, 0], JOINT_LIMITS[idx, 1])
        norm = (cv - JOINT_LIMITS[idx, 0]) / (
            JOINT_LIMITS[idx, 1] - JOINT_LIMITS[idx, 0])
        self.joint_sliders[idx].blockSignals(True)
        self.joint_sliders[idx].setValue(int(norm * 1000))
        self.joint_sliders[idx].blockSignals(False)

    def _on_gripper_slider(self, value):
        gv = GRIPPER_CLOSED + (value / 100.0) * (GRIPPER_OPEN - GRIPPER_CLOSED)
        self.gripper_value_label.setText(f"{gv:.3f}")

    def _on_speed(self, value):
        self.speed_label.setText(f"{value/10:.1f}x")

    def _on_record(self):
        if self.on_record_clicked:
            self.on_record_clicked()

    def _on_save(self):
        if self.on_save_clicked:
            self.on_save_clicked()

    def _on_cancel(self):
        if self.on_cancel_clicked:
            self.on_cancel_clicked()

    def _on_reset(self):
        if self.on_reset_clicked:
            self.on_reset_clicked()

    def _on_pose(self):
        if self.on_pose_clicked:
            self.on_pose_clicked()

    def _on_playback(self):
        if self.on_playback_clicked:
            self.on_playback_clicked()

    def _on_ik_toggle(self, checked):
        if self.on_ik_toggled:
            self.on_ik_toggled(checked)

    # ── Public API ──────────────────────────────

    def set_joint(self, idx, value):
        cv = np.clip(value, JOINT_LIMITS[idx, 0], JOINT_LIMITS[idx, 1])
        norm = (cv - JOINT_LIMITS[idx, 0]) / (
            JOINT_LIMITS[idx, 1] - JOINT_LIMITS[idx, 0])
        self.joint_sliders[idx].blockSignals(True)
        self.joint_sliders[idx].setValue(int(norm * 1000))
        self.joint_sliders[idx].blockSignals(False)
        self.joint_spinboxes[idx].blockSignals(True)
        self.joint_spinboxes[idx].setValue(cv)
        self.joint_spinboxes[idx].blockSignals(False)
        self.joint_values[idx] = cv
        self.joint_labels[idx].setText(f"{cv:.3f}")

    def set_gripper(self, value):
        cv = np.clip(value, GRIPPER_CLOSED, GRIPPER_OPEN)
        norm = (cv - GRIPPER_CLOSED) / (GRIPPER_OPEN - GRIPPER_CLOSED)
        self.gripper_slider.blockSignals(True)
        self.gripper_slider.setValue(int(norm * 100))
        self.gripper_slider.blockSignals(False)
        self.gripper_value_label.setText(f"{cv:.3f}")

    def update_eef_display(self, pos, quat):
        self.eef_pos_label.setText(
            f"pos: ({pos[0]:.3f}, {pos[1]:.3f}, {pos[2]:.3f})")
        self.eef_quat_label.setText(
            f"quat: ({quat[0]:.3f}, {quat[1]:.3f}, "
            f"{quat[2]:.3f}, {quat[3]:.3f})")

    def get_speed(self):
        return self.speed_slider.value() / 10.0

    def set_recording_state(self, on: bool):
        if on:
            self.rec_btn.setText("\u25a0 Stop")
            self.rec_btn.setStyleSheet(
                "QPushButton { background: #5a1a1a; color: #ff6666; "
                "font-weight: bold; padding: 5px 10px; }")
        else:
            self.rec_btn.setText("\u25cf Record")
            self.rec_btn.setStyleSheet(
                "QPushButton { background: #5a1a1a; color: #ff4444; "
                "font-weight: bold; padding: 5px 10px; }"
                "QPushButton:hover { background: #7a2a2a; }")

    def log_message(self, msg):
        self.log.append(msg)


# ═══════════════════════════════════════════════
# Main Window
# ═══════════════════════════════════════════════

class MainWindow(QMainWindow):
    """Main application window orchestrating everything."""

    def __init__(self, initial_pose=None, pose_name=None):
        super().__init__()
        self.setWindowTitle(
            f"Custom UI Robot Arm Simulator — {pose_name or ''}")
        self.setMinimumSize(1150, 720)

        # core
        self.viewer = RobotViewer()
        self.control = ControlPanel()
        self.recorder = Recorder()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.viewer)
        splitter.addWidget(self.control)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        # state
        self.home_pose = initial_pose if initial_pose is not None else HOME_POSITION
        self.pose_name = pose_name or "Custom"
        self.joint_angles = self.home_pose.copy()
        self.gripper_width = GRIPPER_DEFAULT
        self.key_states = {}
        self.fast_mode = False
        self.ik_mode = False

        # cubes
        self.cube_positions = CUBE_INITIAL_POSITIONS.copy()
        self.cube_orientations = np.zeros((NUM_CUBES, 4), dtype=np.float64)
        self.cube_orientations[:, 3] = 1.0
        self.cube_attached = [False] * NUM_CUBES
        self.gripper_closed = False

        # IK target
        self._ik_target_pos = None
        self._ik_target_quat = None

        # wire callbacks
        self.control.on_record_clicked = self._toggle_recording
        self.control.on_save_clicked = self._save_hdf5
        self.control.on_cancel_clicked = self._cancel_recording
        self.control.on_reset_clicked = self._reset_all
        self.control.on_pose_clicked = self._open_pose_manager
        self.control.on_playback_clicked = self._open_playback
        self.control.on_ik_toggled = self._set_ik_mode

        # game loop 60 fps
        self.dt = 1.0 / 60.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(int(self.dt * 1000))

        # fps counter
        self._elapsed = QElapsedTimer()
        self._elapsed.start()
        self._fc = 0
        self._fps = 0.0
        self._fps_t = 0.0

        # help overlay
        self._help_dlg = None

        # init
        self._sync_renderer()
        self._sync_sliders()
        self._update_ik_target()
        self._apply_dark_theme()
        self.control.log_message(
            f"Simulator ready — pose: {self.pose_name}.  "
            "F1 for help, Space to record.")

    # ── Game loop ───────────────────────────────

    def _update(self):
        self._handle_keys()
        self._update_cubes()

        if self.ik_mode and self._ik_target_pos is not None:
            self._run_ik()

        self._sync_renderer()

        T_all = forward_kinematics(self.joint_angles)
        pos, quat, _ = get_eef_pose(T_all)
        self.control.update_eef_display(pos, quat)

        if self.recorder.recording:
            self.recorder.record_frame(
                self.joint_angles, self.gripper_width,
                pos, quat, T_all[-1],
                self.cube_positions, self.cube_orientations, self.dt)

        self._fc += 1
        t = self._elapsed.elapsed() / 1000.0
        if t - self._fps_t >= 1.0:
            self._fps = self._fc / (t - self._fps_t)
            self._fc = 0
            self._fps_t = t
            mode = "IK" if self.ik_mode else "Joint"
            st = "REC" if self.recorder.recording else "Ready"
            self.control.status_label.setText(
                f"{st}  FPS: {self._fps:.0f}  {mode}  "
                f"Ep:{self.recorder.num_episodes}  "
                f"Frames:{self.recorder.total_frames}")

    # ── Keyboard ────────────────────────────────

    def _handle_keys(self):
        q = self.joint_angles.copy()
        speed = self.control.get_speed()
        step = (JOINT_STEP_FAST if self.fast_mode else JOINT_STEP_SLOW) * speed
        changed = False

        if self.ik_mode:
            ee_d = np.zeros(3)
            rot_d = np.zeros(3)
            ee_s = EEF_POS_STEP * speed
            rot_s = EEF_ROT_STEP * speed

            for k, st in self.key_states.items():
                if not st:
                    continue
                if k == Qt.Key_W:   ee_d[2] += ee_s
                elif k == Qt.Key_S: ee_d[2] -= ee_s
                elif k == Qt.Key_A: ee_d[0] -= ee_s
                elif k == Qt.Key_D: ee_d[0] += ee_s
                elif k == Qt.Key_E: ee_d[1] += ee_s
                elif k == Qt.Key_Q: ee_d[1] -= ee_s
                elif k == Qt.Key_R: rot_d[0] += rot_s
                elif k == Qt.Key_F: rot_d[0] -= rot_s
                elif k == Qt.Key_T: rot_d[1] += rot_s
                elif k == Qt.Key_G: rot_d[1] -= rot_s
                elif k == Qt.Key_Y: rot_d[2] += rot_s
                elif k == Qt.Key_H: rot_d[2] -= rot_s

            if np.any(ee_d != 0) or np.any(rot_d != 0):
                self._ik_target_pos += ee_d
                if np.any(rot_d != 0):
                    R = quat_to_matrix(self._ik_target_quat)
                    dR = rot_x(rot_d[0]) @ rot_y(rot_d[1]) @ rot_z(rot_d[2])
                    self._ik_target_quat = quat_from_matrix(R @ dR)
                changed = True
        else:
            for k, st in self.key_states.items():
                if not st:
                    continue
                if k == Qt.Key_W:  q[0] += step; changed = True
                elif k == Qt.Key_S: q[0] -= step; changed = True
                elif k == Qt.Key_E: q[1] += step; changed = True
                elif k == Qt.Key_D: q[1] -= step; changed = True
                elif k == Qt.Key_R: q[2] += step; changed = True
                elif k == Qt.Key_F: q[2] -= step; changed = True
                elif k == Qt.Key_T: q[3] += step; changed = True
                elif k == Qt.Key_G: q[3] -= step; changed = True
                elif k == Qt.Key_Y: q[4] += step; changed = True
                elif k == Qt.Key_H: q[4] -= step; changed = True
                elif k == Qt.Key_U: q[5] += step; changed = True
                elif k == Qt.Key_J: q[5] -= step; changed = True
                elif k == Qt.Key_I: q[6] += step; changed = True
                elif k == Qt.Key_K: q[6] -= step; changed = True

            if changed:
                self.joint_angles = clamp_joints(q)
                self._sync_sliders()

        # gripper (both modes)
        g = self.gripper_width
        gc = False
        if self.key_states.get(Qt.Key_Z, False):
            g = max(GRIPPER_CLOSED, g - GRIPPER_STEP * speed); gc = True
        if self.key_states.get(Qt.Key_X, False):
            g = min(GRIPPER_OPEN, g + GRIPPER_STEP * speed); gc = True
        if gc:
            self.gripper_width = g
            self.control.set_gripper(g)

    def keyPressEvent(self, e: QKeyEvent):
        k = e.key()
        self.key_states[k] = True

        if k == Qt.Key_Space:          self._toggle_recording()
        elif k == Qt.Key_1:            self._toggle_subtask(0)
        elif k == Qt.Key_2:            self._toggle_subtask(1)
        elif k == Qt.Key_3:            self._toggle_subtask(2)
        elif k == Qt.Key_V:            self._toggle_cube_attach()
        elif k == Qt.Key_Shift:        self.fast_mode = True
        elif k == Qt.Key_Backspace:    self._reset_all()
        elif k == Qt.Key_M:            self._toggle_ik_mode()
        elif k == Qt.Key_F1:           self._toggle_help()
        elif k == Qt.Key_P:            self._open_playback()
        elif k == Qt.Key_C:            self._toggle_subtask(0)
        elif k == Qt.Key_B:            self._toggle_subtask(1)
        elif k == Qt.Key_N:            self._toggle_subtask(2)

        if k == Qt.Key_S and e.modifiers() & Qt.ControlModifier:
            self._save_hdf5()

    def keyReleaseEvent(self, e: QKeyEvent):
        self.key_states[e.key()] = False
        if e.key() == Qt.Key_Shift:
            self.fast_mode = False

    # ── IK mode ────────────────────────────────

    def _toggle_ik_mode(self):
        self._set_ik_mode(not self.ik_mode)

    def _set_ik_mode(self, on: bool):
        self.ik_mode = on
        self.control.ik_mode_cb.setChecked(on)
        if on:
            self._update_ik_target()
            self.control.log_message(
                "IK mode ON  \u2014 W/S Z, A/D X, E/Q Y, R/F/T/G/Y/H rot")
        else:
            self.control.log_message("Joint mode ON")

    def _update_ik_target(self):
        T_all = forward_kinematics(self.joint_angles)
        pos, quat, _ = get_eef_pose(T_all)
        self._ik_target_pos = pos.copy()
        self._ik_target_quat = quat.copy()

    def _run_ik(self):
        sol = inverse_kinematics(
            self._ik_target_pos, self._ik_target_quat,
            q_initial=self.joint_angles, num_attempts=1)
        if sol is not None:
            self.joint_angles = clamp_joints(sol)
            self._sync_sliders()

    # ── Subtask ────────────────────────────────

    def _toggle_subtask(self, idx):
        if idx >= len(SUBTASK_NAMES):
            return
        nv = not self.recorder.subtask_signals[idx]
        self.recorder.set_subtask(idx, nv)
        self.control.subtask_checks[idx].setChecked(nv)
        self.control.log_message(
            f"Subtask {SUBTASK_NAMES[idx]} {'ON' if nv else 'OFF'}")

    # ── Cubes ──────────────────────────────────

    def _toggle_cube_attach(self):
        if not self.gripper_closed:
            self.control.log_message("Close gripper (Z) first")
            return
        T_all = forward_kinematics(self.joint_angles)
        eef_p = T_all[-1][:3, 3]
        ai = next((i for i, a in enumerate(self.cube_attached) if a), None)
        if ai is not None:
            self.cube_attached[ai] = False
            self.control.log_message(f"Cube {ai} detached")
            return
        dists = [np.linalg.norm(self.cube_positions[i] - eef_p)
                 for i in range(NUM_CUBES)]
        md = min(dists)
        if md < 0.12:
            idx = int(np.argmin(dists))
            self.cube_attached[idx] = True
            self.control.log_message(f"Cube {idx} attached ({md:.3f}m)")
        else:
            self.control.log_message(f"No cube near EEF ({md:.3f}m)")

    def _update_cubes(self):
        T_all = forward_kinematics(self.joint_angles)
        eef_p = T_all[-1][:3, 3]
        R = T_all[-1][:3, :3]
        self.gripper_closed = self.gripper_width < 0.01
        for i in range(NUM_CUBES):
            if self.cube_attached[i]:
                self.cube_positions[i] = eef_p + R @ np.array([0, 0, 0.05])

    # ── Recording ──────────────────────────────

    def _toggle_recording(self):
        if not self.recorder.recording:
            self.recorder.start_recording()
            self.control.set_recording_state(True)
            self.control.log_message("Recording started")
        else:
            ep = self.recorder.stop_recording()
            self.control.set_recording_state(False)
            if ep:
                self.control.log_message(
                    f"Episode saved: {ep.num_samples} frames")
            else:
                self.control.log_message("Recording discarded (<5 frames)")

    def _cancel_recording(self):
        self.recorder.cancel_recording()
        self.control.set_recording_state(False)
        self.control.log_message("Recording cancelled")

    def _save_hdf5(self):
        if self.recorder.num_episodes == 0:
            QMessageBox.information(self, "Save", "No episodes recorded.")
            return
        fp, _ = QFileDialog.getSaveFileName(
            self, "Save HDF5",
            os.path.join(os.path.expanduser("~"), "Desktop",
                         "robot_demonstrations.hdf5"),
            "HDF5 Files (*.hdf5 *.h5);;All Files (*)")
        if not fp:
            return
        try:
            n = self.recorder.save(fp)
            QMessageBox.information(self, "Saved",
                                    f"{n} episodes -> {fp}")
            self.control.log_message(f"Saved {n} episodes")
        except Exception as ex:
            QMessageBox.critical(self, "Error", str(ex))
            self.control.log_message(f"ERROR: {ex}")

    def _reset_all(self):
        self.joint_angles = self.home_pose.copy()
        self.gripper_width = GRIPPER_DEFAULT
        self.cube_positions = CUBE_INITIAL_POSITIONS.copy()
        self.cube_orientations[:] = 0.0
        self.cube_orientations[:, 3] = 1.0
        self.cube_attached = [False] * NUM_CUBES
        self.gripper_closed = False
        self.recorder.clear_subtasks()
        for cb in self.control.subtask_checks:
            cb.setChecked(False)
        self._sync_sliders()
        self.control.set_gripper(self.gripper_width)
        self._update_ik_target()
        self.control.log_message(f"Reset \u2192 {self.pose_name}")

    # ── Pose manager ──────────────────────────

    def _open_pose_manager(self):
        dlg = PoseManager(self.joint_angles, self)
        if dlg.exec_() == QDialog.Accepted:
            pose = dlg.get_selected_pose()
            if pose is not None:
                self.joint_angles = clamp_joints(pose)
                self._sync_sliders()
                self._update_ik_target()
                self.control.log_message(f"Loaded pose: {dlg.selected_name}")

    # ── Playback ──────────────────────────────

    def _open_playback(self):
        dlg = PlaybackDialog(self.viewer, self)
        dlg.exec_()

    # ── Help ──────────────────────────────────

    def _toggle_help(self):
        if self._help_dlg is None or not self._help_dlg.isVisible():
            self._help_dlg = HelpOverlay(self)
            self._help_dlg.show()
        else:
            self._help_dlg.close()

    # ── Sync ──────────────────────────────────

    def _sync_renderer(self):
        self.viewer.update_robot(
            self.joint_angles, self.gripper_width,
            [(self.cube_positions[i], self.cube_orientations[i],
              self.cube_attached[i]) for i in range(NUM_CUBES)])

    def _sync_sliders(self):
        for i in range(NUM_JOINTS):
            self.control.set_joint(i, self.joint_angles[i])

    # ── Theme ─────────────────────────────────

    def _apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background: #1e1e1e; }
            QWidget { color: #d4d4d4; }
            QGroupBox {
                background: #252526; border: 1px solid #3c3c3c;
                border-radius: 4px; margin-top: 12px; padding-top: 16px;
                font-weight: bold; color: #ccc;
            }
            QGroupBox::title {
                subcontrol-origin: margin; left: 10px; padding: 0 4px;
            }
            QSlider::groove:horizontal {
                height: 6px; background: #3c3c3c; border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #007acc; width: 14px; height: 14px;
                margin: -4px 0; border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #0e639c; border-radius: 3px;
            }
            QPushButton {
                background: #0e639c; color: white; border: none;
                padding: 4px 10px; border-radius: 3px; font-weight: bold;
            }
            QPushButton:hover { background: #1177bb; }
            QPushButton:pressed { background: #094771; }
            QCheckBox { spacing: 6px; }
            QCheckBox::indicator { width: 14px; height: 14px; }
        """)

    def closeEvent(self, e: QCloseEvent):
        self.timer.stop()
        if self._help_dlg is not None:
            self._help_dlg.close()
        e.accept()
