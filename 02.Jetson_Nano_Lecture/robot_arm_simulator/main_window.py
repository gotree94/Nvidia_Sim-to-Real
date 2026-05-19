"""
Main application window with control panel.
Joint sliders, EEF display, recording controls, subtask buttons.
"""

import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QGroupBox, QSlider, QLabel, QPushButton, QGridLayout,
    QProgressBar, QStatusBar, QMessageBox, QFileDialog, QCheckBox,
    QTextEdit, QFrame, QApplication,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from config import JOINT_LIMITS, HOME_POSITION, SUBTASK_NAMES, DEFAULT_FPS
from kinematics import franka_fk, rotation_matrix_to_quat
from recorder import DemonstrationRecorder
from playback import PlaybackDialog


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, robot_viewer, recorder):
        super().__init__()
        self.viewer = robot_viewer
        self.recorder = recorder

        # Robot state
        self.joint_angles = HOME_POSITION.copy()
        self.gripper_width = 0.04  # open
        self.prev_joint = self.joint_angles.copy()

        # Cube state
        from config import CUBE_POSITIONS
        self.cube_positions = {k: v.copy() for k, v in CUBE_POSITIONS.items()}
        self.cube_orientations = {k: np.array([1.0, 0.0, 0.0, 0.0])
                                   for k in CUBE_POSITIONS}
        self.cube_attached = {k: False for k in CUBE_POSITIONS}
        self.attached_cube = None

        # Subtask states
        self.subtask_states = {name: False for name in SUBTASK_NAMES}

        # Key repeat
        self.key_states = {}  # key_code → bool

        self._setup_ui()
        self._setup_timers()

    def _setup_ui(self):
        self.setWindowTitle("Synthetic Manipulation - Robot Arm Simulator")
        self.setMinimumSize(1200, 750)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)

        # Splitter: 3D view (left) + Controls (right)
        splitter = QSplitter(Qt.Horizontal)

        # ── Left: 3D Viewport ──
        splitter.addWidget(self.viewer)

        # ── Right: Control Panel ──
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(8)
        right_layout.setContentsMargins(4, 4, 4, 4)

        # --- Joint Controls ---
        joint_group = QGroupBox("Joint Angles")
        joint_grid = QGridLayout(joint_group)
        self.joint_sliders = []
        self.joint_labels = []

        for i in range(7):
            lbl_name = QLabel(f"J{i+1}:")
            lbl_name.setFixedWidth(30)
            lbl_name.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 1000)
            min_val, max_val = JOINT_LIMITS[i]
            init_val = HOME_POSITION[i]
            slider.setValue(int(1000 * (init_val - min_val) / (max_val - min_val)))
            slider.valueChanged.connect(lambda v, idx=i: self._on_joint_slider(idx, v))

            lbl_val = QLabel(f"{init_val:.3f}")
            lbl_val.setFixedWidth(80)
            lbl_val.setFont(QFont("Consolas", 9))

            joint_grid.addWidget(lbl_name, i, 0)
            joint_grid.addWidget(slider, i, 1)
            joint_grid.addWidget(lbl_val, i, 2)

            self.joint_sliders.append(slider)
            self.joint_labels.append(lbl_val)

        right_layout.addWidget(joint_group)

        # --- EEF Position Display ---
        eef_group = QGroupBox("End-Effector Pose")
        eef_layout = QGridLayout(eef_group)
        self.eef_pos_label = QLabel("pos: (0.00, 0.00, 0.00)")
        self.eef_quat_label = QLabel("quat: (1.00, 0.00, 0.00, 0.00)")
        self.eef_pos_label.setFont(QFont("Consolas", 9))
        self.eef_quat_label.setFont(QFont("Consolas", 9))
        eef_layout.addWidget(self.eef_pos_label, 0, 0)
        eef_layout.addWidget(self.eef_quat_label, 1, 0)
        right_layout.addWidget(eef_group)

        # --- Gripper Control ---
        gripper_group = QGroupBox("Gripper")
        gripper_layout = QHBoxLayout(gripper_group)
        self.gripper_slider = QSlider(Qt.Horizontal)
        self.gripper_slider.setRange(0, 100)
        self.gripper_slider.setValue(100)  # open
        self.gripper_slider.valueChanged.connect(self._on_gripper_slider)
        self.gripper_label = QLabel("0.040")
        self.gripper_label.setFixedWidth(60)
        self.gripper_label.setFont(QFont("Consolas", 9))
        gripper_layout.addWidget(QLabel("Close ◀"))
        gripper_layout.addWidget(self.gripper_slider)
        gripper_layout.addWidget(QLabel("▶ Open"))
        gripper_layout.addWidget(self.gripper_label)
        right_layout.addWidget(gripper_group)

        # --- Recording Controls ---
        rec_group = QGroupBox("Recording")
        rec_layout = QHBoxLayout(rec_group)

        self.record_btn = QPushButton("⏺ Record")
        self.record_btn.setCheckable(True)
        self.record_btn.setStyleSheet("""
            QPushButton { font-weight: bold; padding: 6px 16px; }
            QPushButton:checked { background-color: #cc3333; color: white; }
        """)
        self.record_btn.toggled.connect(self._on_record_toggle)

        self.save_btn = QPushButton("💾 Save HDF5")
        self.save_btn.clicked.connect(self._on_save)

        self.cancel_btn = QPushButton("✕ Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel)

        self.frame_label = QLabel("Frames: 0")
        self.frame_label.setFont(QFont("Consolas", 10))

        rec_layout.addWidget(self.record_btn)
        rec_layout.addWidget(self.save_btn)
        rec_layout.addWidget(self.cancel_btn)
        rec_layout.addStretch()
        rec_layout.addWidget(self.frame_label)
        right_layout.addWidget(rec_group)

        # --- Episode Count ---
        ep_layout = QHBoxLayout()
        self.ep_count_label = QLabel("Episodes recorded: 0")
        self.ep_count_label.setFont(QFont("Consolas", 10))
        ep_layout.addWidget(self.ep_count_label)
        ep_layout.addStretch()
        right_layout.addLayout(ep_layout)

        # --- Subtask Controls ---
        subtask_group = QGroupBox("Subtask Signals (Keyboard: 1/2/3)")
        subtask_layout = QHBoxLayout(subtask_group)
        self.subtask_btns = {}
        for name in SUBTASK_NAMES:
            btn = QPushButton(f"[{name}]")
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton { padding: 4px 12px; }
                QPushButton:checked { background-color: #ff8800; color: white; font-weight: bold; }
            """)
            btn.toggled.connect(lambda checked, n=name: self._on_subtask_toggle(n, checked))
            self.subtask_btns[name] = btn
            subtask_layout.addWidget(btn)
        subtask_layout.addStretch()
        right_layout.addWidget(subtask_group)

        # --- Playback Button ---
        pb_layout = QHBoxLayout()
        self.playback_btn = QPushButton("▶ Playback (P)")
        self.playback_btn.clicked.connect(self._on_playback)
        pb_layout.addWidget(self.playback_btn)
        pb_layout.addStretch()
        right_layout.addLayout(pb_layout)

        # --- Status Display ---
        self.status_display = QTextEdit()
        self.status_display.setReadOnly(True)
        self.status_display.setMaximumHeight(100)
        self.status_display.setFont(QFont("Consolas", 9))
        self.status_display.append("Ready. Press R to reset, Space to record.")
        right_layout.addWidget(self.status_display)

        # Add right panel to splitter
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 400])
        main_layout.addWidget(splitter)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _setup_timers(self):
        """Update loop for real-time state sync."""
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_loop)
        self.update_timer.start(16)  # ~60 Hz

    def _update_loop(self):
        """Sync internal state with viewer and UI."""
        # Apply key repeat states (smooth key-hold movement)
        self._apply_key_repeat()

        # Update viewer
        self.viewer.update_robot(self.joint_angles, self.gripper_width)
        self.viewer.update_cubes(self.cube_positions, self.cube_orientations,
                                 self.cube_attached)

        # Update EEF display
        T_ee = franka_fk(self.joint_angles)
        pos = T_ee[:3, 3]
        quat = rotation_matrix_to_quat(T_ee[:3, :3])
        self.eef_pos_label.setText(f"pos: ({pos[0]:.4f}, {pos[1]:.4f}, {pos[2]:.4f})")
        self.eef_quat_label.setText(f"quat: ({quat[0]:.4f}, {quat[1]:.4f}, {quat[2]:.4f}, {quat[3]:.4f})")

        # Record if active
        if self.recorder.is_recording:
            self.recorder.record_frame(
                self.joint_angles, self.gripper_width,
                self.cube_positions, self.cube_orientations,
                self.cube_attached
            )
            self.frame_label.setText(f"Frames: {self.recorder.frame_count}")
            self.ep_count_label.setText(f"Episodes recorded: {self.recorder.get_episode_count()}")

    # ───── UI Callbacks ─────

    def _on_joint_slider(self, idx, value):
        min_val, max_val = JOINT_LIMITS[idx]
        joint_val = min_val + (max_val - min_val) * value / 1000.0
        self.joint_angles[idx] = joint_val
        self.joint_labels[idx].setText(f"{joint_val:.3f}")

    def _on_gripper_slider(self, value):
        self.gripper_width = value / 100.0 * 0.04
        self.gripper_label.setText(f"{self.gripper_width:.3f}")

    def _on_record_toggle(self, checked):
        if checked:
            # Start recording new episode
            self.recorder.start_episode()
            for name in SUBTASK_NAMES:
                self.recorder.set_subtask(name, self.subtask_states[name])
            self.status_bar.showMessage("🔴 Recording...")
            self.frame_label.setText("Frames: 0")
        else:
            # Stop and save episode
            idx = self.recorder.finish_episode(success=True)
            if idx >= 0:
                self.status_bar.showMessage(f"✅ Episode {idx} saved ({self.recorder.frame_count} frames)")
            else:
                self.status_bar.showMessage("Episode discarded (too short)")
            self.frame_label.setText(f"Frames: 0")
            self.ep_count_label.setText(f"Episodes recorded: {self.recorder.get_episode_count()}")

    def _on_save(self):
        """Save all episodes to HDF5 file."""
        if self.recorder.get_episode_count() == 0:
            QMessageBox.warning(self, "No Data", "No episodes recorded yet. Record some demonstrations first.")
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save HDF5 Dataset", "annotated_dataset.hdf5",
            "HDF5 files (*.hdf5);;All files (*)"
        )
        if filepath:
            self.recorder.save_to_hdf5(filepath, env_name="Franka-CubeStack-Custom-v0")
            self.status_bar.showMessage(f"✅ Saved to {filepath}")
            self.status_display.append(f"Saved {self.recorder.get_episode_count()} episodes to {filepath}")

    def _on_cancel(self):
        """Cancel current recording."""
        if self.recorder.is_recording:
            self.recorder.cancel_episode()
            self.record_btn.setChecked(False)
            self.status_bar.showMessage("Recording cancelled")
            self.frame_label.setText("Frames: 0")

    def _on_playback(self):
        """Open playback dialog."""
        dlg = PlaybackDialog(self.viewer, self)
        dlg.exec_()

    def _on_subtask_toggle(self, name, checked):
        self.subtask_states[name] = checked
        if self.recorder.is_recording:
            self.recorder.set_subtask(name, checked)
        state_str = "ON" if checked else "OFF"
        self.status_display.append(f"Subtask '{name}': {state_str}")

    # ───── Keyboard Control ─────

    def keyPressEvent(self, event):
        key = event.key()
        self.key_states[key] = True
        self._handle_key_action(key)

    def keyReleaseEvent(self, event):
        key = event.key()
        self.key_states[key] = False

    def _apply_key_repeat(self):
        """Apply smooth movement for held keys."""
        step = 0.005
        pressed_keys = {k for k, v in self.key_states.items() if v}

        q_step = 0.0
        if Qt.Key_W in pressed_keys:
            self.joint_angles[0] += step * 3  # rotate base
            q_step += 1
        if Qt.Key_S in pressed_keys:
            self.joint_angles[0] -= step * 3
            q_step += 1
        if Qt.Key_A in pressed_keys:
            self.joint_angles[1] += step * 2
            q_step += 1
        if Qt.Key_D in pressed_keys:
            self.joint_angles[1] -= step * 2
            q_step += 1
        if Qt.Key_Q in pressed_keys:
            self.joint_angles[2] += step * 2
            q_step += 1
        if Qt.Key_E in pressed_keys:
            self.joint_angles[2] -= step * 2
            q_step += 1

        # Clamp joints
        for i in range(7):
            self.joint_angles[i] = np.clip(self.joint_angles[i],
                                           JOINT_LIMITS[i, 0],
                                           JOINT_LIMITS[i, 1])

        # Update sliders to match
        if q_step > 0:
            self._sync_sliders()

    def _handle_key_action(self, key):
        # ── Joint discrete control ──
        step = 0.02
        if key == Qt.Key_W:
            self.joint_angles[0] += step * 1.5
        elif key == Qt.Key_S:
            self.joint_angles[0] -= step * 1.5
        elif key == Qt.Key_A:
            self.joint_angles[1] += step
        elif key == Qt.Key_D:
            self.joint_angles[1] -= step
        elif key == Qt.Key_Q:
            self.joint_angles[2] += step
        elif key == Qt.Key_E:
            self.joint_angles[2] -= step
        elif key == Qt.Key_Z:
            self.joint_angles[3] += step
        elif key == Qt.Key_X:
            self.joint_angles[3] -= step
        elif key == Qt.Key_T:
            self.joint_angles[4] += step
        elif key == Qt.Key_G:
            self.joint_angles[4] -= step
        elif key == Qt.Key_C:
            self.joint_angles[5] += step
        elif key == Qt.Key_V:
            self.joint_angles[5] -= step
        elif key == Qt.Key_F:
            self.joint_angles[6] += step
        elif key == Qt.Key_H:
            self.joint_angles[6] -= step

        # Clamp
        for i in range(7):
            self.joint_angles[i] = np.clip(self.joint_angles[i],
                                           JOINT_LIMITS[i, 0],
                                           JOINT_LIMITS[i, 1])
        self._sync_sliders()

        # ── Gripper ──
        if key == Qt.Key_K:
            self.gripper_width = 0.0 if self.gripper_width > 0.02 else 0.04
            self.gripper_slider.setValue(int(self.gripper_width / 0.04 * 100))
            self._update_cube_attachment()

        # ── Playback ──
        if key == Qt.Key_P:
            self._on_playback()

        # ── Recording ──
        if key == Qt.Key_Space:
            self.record_btn.toggle()

        # ── Subtask signals (1/2/3) ──
        subtask_keys = {Qt.Key_1: "grasp_1", Qt.Key_2: "grasp_2", Qt.Key_3: "stack_1"}
        if key in subtask_keys:
            name = subtask_keys[key]
            self.subtask_states[name] = not self.subtask_states[name]
            self.subtask_btns[name].setChecked(self.subtask_states[name])
            if self.recorder.is_recording:
                self.recorder.set_subtask(name, self.subtask_states[name])

        # ── Reset ──
        if key in (Qt.Key_R,):
            self.joint_angles = HOME_POSITION.copy()
            self.gripper_width = 0.04
            self.gripper_slider.setValue(100)
            self._sync_sliders()
            self.status_display.append("Reset to home position")

        # ── Save shortcut ──
        if key == Qt.Key_S and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self._on_save()

    def _sync_sliders(self):
        """Sync slider positions to joint angles."""
        for i in range(7):
            min_val, max_val = JOINT_LIMITS[i]
            val = int(1000 * (self.joint_angles[i] - min_val) / (max_val - min_val))
            self.joint_sliders[i].blockSignals(True)
            self.joint_sliders[i].setValue(val)
            self.joint_sliders[i].blockSignals(False)
            self.joint_labels[i].setText(f"{self.joint_angles[i]:.3f}")

    def _update_cube_attachment(self):
        """Simple cube attachment: if gripper closed and near cube, attach."""
        T_ee = franka_fk(self.joint_angles)
        eef_pos = T_ee[:3, 3]

        if self.gripper_width < 0.005:  # closed
            # Find closest cube within grasp range
            min_dist = 0.08
            nearest = None
            for name, pos in self.cube_positions.items():
                if self.cube_attached.get(name, False):
                    nearest = name  # already attached
                    break
                dist = np.linalg.norm(eef_pos - pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest = name

            if nearest and not self.cube_attached.get(nearest, False):
                # Attach
                for n in self.cube_attached:
                    self.cube_attached[n] = (n == nearest)
                self.attached_cube = nearest
                self.status_display.append(f"📦 Attached {nearest}")
        else:
            # Detach all
            for n in self.cube_attached:
                if self.cube_attached[n]:
                    # Place cube at EEF position (drop)
                    self.cube_positions[n] = eef_pos.copy()
                    self.cube_orientations[n] = np.array([1.0, 0.0, 0.0, 0.0])
                    self.status_display.append(f"📦 Detached {n} at ({eef_pos[0]:.3f}, {eef_pos[1]:.3f}, {eef_pos[2]:.3f})")
                self.cube_attached[n] = False
            self.attached_cube = None

        # If cube attached, move it with EEF
        if self.attached_cube:
            self.cube_positions[self.attached_cube] = eef_pos.copy()
